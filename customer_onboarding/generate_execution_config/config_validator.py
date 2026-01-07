"""
Config Validator for Execution Configurations
Validates that generated configs are correct and executable
"""

import json
from typing import Dict, List, Tuple, Any


class ConfigValidator:
    """Validates execution configurations"""
    
    def __init__(self, catalogs_dir: str = "catalogs"):
        """Initialize with function catalogs from directory"""
        self.functions = {}
        self.catalogs_dir = catalogs_dir
        self._load_catalogs()
    
    def _load_catalogs(self):
        """Load all function catalogs from the catalogs directory"""
        import os
        
        # Read catalog index
        index_path = os.path.join(self.catalogs_dir, "catalog_index.json")
        if os.path.exists(index_path):
            with open(index_path, 'r') as f:
                index = json.load(f)
            
            # Load each catalog file
            for catalog_info in index['catalogs']:
                catalog_path = os.path.join(self.catalogs_dir, catalog_info['file'])
                with open(catalog_path, 'r') as f:
                    catalog = json.load(f)
                    
                # Add module info to each function
                for func in catalog['functions']:
                    func['module'] = catalog.get('module', catalog_info['module'])
                    self.functions[func['name']] = func
        else:
            # Fallback: load from single function_catalog.json if it exists
            catalog_path = "function_catalog.json"
            if os.path.exists(catalog_path):
                with open(catalog_path, 'r') as f:
                    catalog = json.load(f)
                self.functions = {f['name']: f for f in catalog['functions']}
    
    def validate_config(self, config: Dict) -> Tuple[bool, List[str]]:
        """
        Validate entire execution config
        
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Check required top-level fields
        required_fields = ['config_id', 'analysis_id', 'steps']
        for field in required_fields:
            if field not in config:
                errors.append(f"Missing required field: {field}")
        
        if 'steps' not in config:
            return False, errors
        
        # Validate each step
        step_outputs = {}
        for i, step in enumerate(config['steps']):
            step_errors = self.validate_step(step, i, step_outputs)
            errors.extend(step_errors)
            
            # Track outputs for dependency checking
            if 'output' in step:
                step_outputs[step['step_id']] = step['output']
        
        # Check for circular dependencies
        circular_deps = self.check_circular_dependencies(config['steps'])
        if circular_deps:
            errors.append(f"Circular dependencies detected: {circular_deps}")
        
        return len(errors) == 0, errors
    
    def validate_step(self, step: Dict, step_num: int, available_outputs: Dict) -> List[str]:
        """Validate a single step"""
        errors = []
        
        # Check required step fields
        required_fields = ['step_id', 'function', 'arguments']
        for field in required_fields:
            if field not in step:
                errors.append(f"Step {step_num}: Missing required field '{field}'")
                return errors
        
        function_name = step['function']
        
        # Check function exists
        if function_name not in self.functions:
            errors.append(f"Step {step_num}: Unknown function '{function_name}'")
            return errors
        
        function_def = self.functions[function_name]
        
        # Validate arguments
        arg_errors = self.validate_arguments(
            step['arguments'],
            function_def['parameters'],
            step_num,
            available_outputs
        )
        errors.extend(arg_errors)
        
        # Check step_id is unique (would need to track across all steps)
        # Check dependencies exist if specified
        if 'depends_on' in step:
            for dep in step['depends_on']:
                if dep not in available_outputs:
                    errors.append(
                        f"Step {step_num}: Dependency '{dep}' not found in previous steps"
                    )
        
        return errors
    
    def validate_arguments(
        self,
        arguments: Dict,
        parameters: Dict,
        step_num: int,
        available_outputs: Dict
    ) -> List[str]:
        """Validate function arguments against parameter definitions"""
        errors = []
        
        # Check required parameters are provided
        for param_name, param_def in parameters.items():
            if param_def.get('required', False):
                if param_name not in arguments:
                    errors.append(
                        f"Step {step_num}: Missing required argument '{param_name}'"
                    )
        
        # Check provided arguments are valid
        for arg_name, arg_value in arguments.items():
            if arg_name not in parameters:
                errors.append(
                    f"Step {step_num}: Unknown argument '{arg_name}'"
                )
                continue
            
            param_def = parameters[arg_name]
            
            # Type checking
            expected_type = param_def['type']
            type_errors = self.check_type(arg_value, expected_type, arg_name, step_num)
            errors.extend(type_errors)
            
            # Check valid values if specified
            if 'valid_values' in param_def:
                if isinstance(arg_value, list):
                    for val in arg_value:
                        if val not in param_def['valid_values']:
                            errors.append(
                                f"Step {step_num}: Invalid value '{val}' for '{arg_name}'. "
                                f"Valid values: {param_def['valid_values']}"
                            )
                else:
                    if arg_value not in param_def['valid_values']:
                        errors.append(
                            f"Step {step_num}: Invalid value '{arg_value}' for '{arg_name}'. "
                            f"Valid values: {param_def['valid_values']}"
                        )
            
            # Check references to previous outputs
            if isinstance(arg_value, str) and arg_value.startswith('$'):
                # This is a reference to a previous step's output
                ref_step_id = arg_value[1:]  # Remove $
                if ref_step_id not in available_outputs:
                    errors.append(
                        f"Step {step_num}: Reference to undefined step output '{arg_value}'"
                    )
        
        return errors
    
    def check_type(self, value: Any, expected_type: str, arg_name: str, step_num: int) -> List[str]:
        """Check if value matches expected type"""
        errors = []
        
        # Skip type checking for step output references
        if isinstance(value, str) and value.startswith('$'):
            return errors
        
        type_map = {
            'string': str,
            'integer': int,
            'float': float,
            'list': list,
            'dict': dict,
            'boolean': bool
        }
        
        if expected_type in type_map:
            if not isinstance(value, type_map[expected_type]):
                errors.append(
                    f"Step {step_num}: Argument '{arg_name}' should be {expected_type}, "
                    f"got {type(value).__name__}"
                )
        
        return errors
    
    def check_circular_dependencies(self, steps: List[Dict]) -> List[str]:
        """Check for circular dependencies in step execution order"""
        # Build dependency graph
        graph = {}
        for step in steps:
            step_id = step['step_id']
            deps = step.get('depends_on', [])
            graph[step_id] = deps
        
        # Check for cycles using DFS
        visited = set()
        rec_stack = set()
        cycles = []
        
        def has_cycle(node, path):
            visited.add(node)
            rec_stack.add(node)
            path.append(node)
            
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    if has_cycle(neighbor, path.copy()):
                        return True
                elif neighbor in rec_stack:
                    cycle_start = path.index(neighbor)
                    cycles.append(' -> '.join(path[cycle_start:] + [neighbor]))
                    return True
            
            rec_stack.remove(node)
            return False
        
        for node in graph:
            if node not in visited:
                has_cycle(node, [])
        
        return cycles
    
    def validate_data_flow(self, config: Dict) -> Tuple[bool, List[str]]:
        """Validate that data flows correctly between steps"""
        errors = []
        
        # Track what data is produced by each step
        available_data = {}
        
        for i, step in enumerate(config['steps']):
            function_name = step['function']
            if function_name not in self.functions:
                continue
            
            # Check that input data is available
            for arg_name, arg_value in step['arguments'].items():
                if isinstance(arg_value, str) and arg_value.startswith('$'):
                    ref_step = arg_value[1:]
                    if ref_step not in available_data:
                        errors.append(
                            f"Step {i} ({step['step_id']}): References data from '{ref_step}' "
                            f"which hasn't been produced yet"
                        )
            
            # Record this step's output
            if 'output' in step:
                available_data[step['step_id']] = step['output']
        
        return len(errors) == 0, errors


def validate_execution_config(config_path: str, catalogs_dir: str = "catalogs") -> Tuple[bool, List[str]]:
    """
    Validate an execution config file
    
    Args:
        config_path: Path to config JSON file
        catalogs_dir: Path to directory containing function catalogs
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    validator = ConfigValidator(catalogs_dir)
    
    # Validate structure and functions
    is_valid, errors = validator.validate_config(config)
    
    # Validate data flow
    if is_valid:
        is_valid, flow_errors = validator.validate_data_flow(config)
        errors.extend(flow_errors)
    
    return is_valid, errors


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python config_validator.py <config_file> [catalogs_dir]")
        sys.exit(1)
    
    config_file = sys.argv[1]
    catalogs_dir = sys.argv[2] if len(sys.argv) > 2 else "catalogs"
    
    is_valid, errors = validate_execution_config(config_file, catalogs_dir)
    
    if is_valid:
        print("✓ Config is valid!")
    else:
        print("✗ Config validation failed:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)

