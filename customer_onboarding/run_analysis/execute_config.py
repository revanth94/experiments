#!/usr/bin/env python3
"""
Execute Configuration
Triggers the execution API to run analysis workflows
"""

import json
import time
import os
import sys
from typing import Dict, List, Optional
from datetime import datetime
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed


class ExecutionAPI:
    """Client for the execution API"""
    
    def __init__(self, api_base_url: str, api_key: Optional[str] = None):
        """
        Initialize API client
        
        Args:
            api_base_url: Base URL of the execution API
            api_key: Optional API key for authentication
        """
        self.api_base_url = api_base_url.rstrip('/')
        self.api_key = api_key or os.environ.get('EXECUTION_API_KEY')
        self.headers = {
            'Content-Type': 'application/json'
        }
        if self.api_key:
            self.headers['Authorization'] = f'Bearer {self.api_key}'
    
    def submit_step(self, step: Dict) -> Dict:
        """
        Submit a single step for execution
        
        Args:
            step: Step configuration
            
        Returns:
            API response with execution_id and status
        """
        endpoint = f'{self.api_base_url}/api/v1/execute/step'
        
        payload = {
            'step_id': step['step_id'],
            'step_name': step['step_name'],
            'function': step['function'],
            'module': step['module'],
            'arguments': step['arguments'],
            'group': step.get('group'),
            'output': step.get('output')
        }
        
        try:
            response = requests.post(
                endpoint,
                json=payload,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': str(e),
                'step_id': step['step_id']
            }
    
    def check_status(self, execution_id: str) -> Dict:
        """
        Check execution status
        
        Args:
            execution_id: Execution ID from submit_step
            
        Returns:
            Status information
        """
        endpoint = f'{self.api_base_url}/api/v1/execute/status/{execution_id}'
        
        try:
            response = requests.get(endpoint, headers=self.headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': str(e),
                'status': 'unknown'
            }
    
    def get_result(self, execution_id: str) -> Dict:
        """
        Get execution result
        
        Args:
            execution_id: Execution ID from submit_step
            
        Returns:
            Execution result
        """
        endpoint = f'{self.api_base_url}/api/v1/execute/result/{execution_id}'
        
        try:
            response = requests.get(endpoint, headers=self.headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': str(e)
            }


class ConfigExecutor:
    """Executes configuration workflows"""
    
    def __init__(self, config_path: str, api_base_url: str, api_key: Optional[str] = None):
        """
        Initialize executor
        
        Args:
            config_path: Path to execution config JSON
            api_base_url: Base URL of execution API
            api_key: Optional API key
        """
        self.config_path = config_path
        self.api = ExecutionAPI(api_base_url, api_key)
        
        # Load config
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        # Execution tracking
        self.step_status = {}  # step_id -> status
        self.step_executions = {}  # step_id -> execution_id
        self.step_results = {}  # step_id -> result
        
        # Create steps lookup
        self.steps = {step['step_id']: step for step in self.config['steps']}
        
        # Execution log
        self.execution_log = []
    
    def log(self, message: str, level: str = 'INFO'):
        """Log a message"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] [{level}] {message}"
        print(log_entry)
        self.execution_log.append({
            'timestamp': timestamp,
            'level': level,
            'message': message
        })
    
    def save_execution_state(self):
        """Save current execution state"""
        state_file = self.config_path.replace('.json', '_execution_state.json')
        
        state = {
            'config_id': self.config['config_id'],
            'started_at': self.execution_log[0]['timestamp'] if self.execution_log else None,
            'step_status': self.step_status,
            'step_executions': self.step_executions,
            'step_results': self.step_results,
            'execution_log': self.execution_log[-50:]  # Last 50 log entries
        }
        
        with open(state_file, 'w') as f:
            json.dump(state, f, indent=2)
        
        self.log(f"Execution state saved to {state_file}")
    
    def execute_step(self, step_id: str) -> bool:
        """
        Execute a single step
        
        Args:
            step_id: ID of step to execute
            
        Returns:
            True if successful, False otherwise
        """
        step = self.steps[step_id]
        
        self.log(f"Executing step: {step_id} ({step['step_name']})")
        self.step_status[step_id] = 'running'
        
        # Submit step
        response = self.api.submit_step(step)
        
        if not response.get('success', False):
            self.log(f"Failed to submit step {step_id}: {response.get('error')}", 'ERROR')
            self.step_status[step_id] = 'failed'
            return False
        
        execution_id = response['execution_id']
        self.step_executions[step_id] = execution_id
        self.log(f"Step {step_id} submitted with execution_id: {execution_id}")
        
        # Poll for completion
        while True:
            time.sleep(5)  # Poll every 5 seconds
            
            status_response = self.api.check_status(execution_id)
            status = status_response.get('status', 'unknown')
            
            if status == 'completed':
                self.log(f"Step {step_id} completed successfully")
                self.step_status[step_id] = 'completed'
                
                # Get result
                result = self.api.get_result(execution_id)
                self.step_results[step_id] = result
                return True
            
            elif status == 'failed':
                error = status_response.get('error', 'Unknown error')
                self.log(f"Step {step_id} failed: {error}", 'ERROR')
                self.step_status[step_id] = 'failed'
                return False
            
            elif status == 'running':
                # Still running, continue polling
                continue
            
            else:
                self.log(f"Step {step_id} has unknown status: {status}", 'WARNING')
    
    def execute_steps_parallel(self, step_ids: List[str]) -> bool:
        """
        Execute multiple steps in parallel
        
        Args:
            step_ids: List of step IDs to execute
            
        Returns:
            True if all successful, False if any failed
        """
        self.log(f"Executing {len(step_ids)} steps in parallel")
        
        with ThreadPoolExecutor(max_workers=min(len(step_ids), 10)) as executor:
            futures = {
                executor.submit(self.execute_step, step_id): step_id
                for step_id in step_ids
            }
            
            results = {}
            for future in as_completed(futures):
                step_id = futures[future]
                try:
                    results[step_id] = future.result()
                except Exception as e:
                    self.log(f"Exception executing step {step_id}: {e}", 'ERROR')
                    results[step_id] = False
        
        all_success = all(results.values())
        if all_success:
            self.log(f"All {len(step_ids)} parallel steps completed successfully")
        else:
            failed = [sid for sid, success in results.items() if not success]
            self.log(f"{len(failed)} steps failed: {failed}", 'ERROR')
        
        return all_success
    
    def execute_steps_sequential(self, step_ids: List[str]) -> bool:
        """
        Execute multiple steps sequentially
        
        Args:
            step_ids: List of step IDs to execute in order
            
        Returns:
            True if all successful, False if any failed
        """
        self.log(f"Executing {len(step_ids)} steps sequentially")
        
        for step_id in step_ids:
            success = self.execute_step(step_id)
            if not success:
                self.log(f"Sequential execution failed at step {step_id}", 'ERROR')
                return False
        
        self.log(f"All {len(step_ids)} sequential steps completed successfully")
        return True
    
    def execute_group(self, group_name: str) -> bool:
        """
        Execute a step group
        
        Args:
            group_name: Name of the group to execute
            
        Returns:
            True if successful, False otherwise
        """
        if group_name not in self.config['step_groups']:
            self.log(f"Group {group_name} not found in config", 'ERROR')
            return False
        
        group = self.config['step_groups'][group_name]
        step_ids = group['step_ids']
        
        self.log(f"=== Executing group: {group_name} ===")
        self.log(f"Description: {group['description']}")
        self.log(f"Module: {group['module']}")
        self.log(f"Steps: {len(step_ids)}")
        self.log(f"Parallel: {group['parallel']}")
        
        if group['parallel']:
            success = self.execute_steps_parallel(step_ids)
        else:
            success = self.execute_steps_sequential(step_ids)
        
        return success
    
    def execute_phase(self, phase_name: str) -> bool:
        """
        Execute an execution phase
        
        Args:
            phase_name: Name of the phase
            
        Returns:
            True if successful, False otherwise
        """
        if phase_name not in self.config['execution_plan']:
            self.log(f"Phase {phase_name} not found in execution plan", 'ERROR')
            return False
        
        phase = self.config['execution_plan'][phase_name]
        
        self.log(f"\n{'='*70}")
        self.log(f"PHASE: {phase['name']}")
        self.log(f"{'='*70}")
        self.log(f"Groups: {phase['groups']}")
        self.log(f"Parallel: {phase['parallel']}")
        self.log(f"Estimated Runtime: {phase['estimated_runtime']}")
        
        # Execute each group in the phase
        for group_name in phase['groups']:
            success = self.execute_group(group_name)
            if not success:
                self.log(f"Phase {phase_name} failed at group {group_name}", 'ERROR')
                return False
            
            # Save state after each group
            self.save_execution_state()
        
        self.log(f"Phase {phase['name']} completed successfully\n")
        return True
    
    def execute(self) -> bool:
        """
        Execute the entire configuration
        
        Returns:
            True if successful, False otherwise
        """
        self.log(f"\n{'#'*70}")
        self.log(f"# STARTING EXECUTION")
        self.log(f"{'#'*70}")
        self.log(f"Config ID: {self.config['config_id']}")
        self.log(f"Customer: {self.config['customer']}")
        self.log(f"Location: {self.config['location']}")
        self.log(f"Total Steps: {len(self.config['steps'])}")
        self.log(f"Estimated Runtime: {self.config['estimated_total_runtime']}")
        self.log(f"{'#'*70}\n")
        
        start_time = time.time()
        
        # Execute each phase in order
        phase_names = sorted(self.config['execution_plan'].keys())
        
        for phase_name in phase_names:
            success = self.execute_phase(phase_name)
            if not success:
                self.log(f"Execution failed at phase {phase_name}", 'ERROR')
                self.save_execution_state()
                return False
        
        # Calculate total time
        end_time = time.time()
        total_minutes = (end_time - start_time) / 60
        total_hours = total_minutes / 60
        
        self.log(f"\n{'#'*70}")
        self.log(f"# EXECUTION COMPLETED SUCCESSFULLY")
        self.log(f"{'#'*70}")
        self.log(f"Total Time: {total_hours:.2f} hours ({total_minutes:.1f} minutes)")
        self.log(f"Steps Completed: {len([s for s in self.step_status.values() if s == 'completed'])}")
        self.log(f"Output Directory: {self.config.get('output_directory', 'N/A')}")
        self.log(f"{'#'*70}\n")
        
        # Save final state
        self.save_execution_state()
        
        return True


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Execute analysis configuration')
    parser.add_argument('config_file', help='Path to execution config JSON file')
    parser.add_argument('--api-url', default='http://localhost:8000',
                       help='Base URL of execution API (default: http://localhost:8000)')
    parser.add_argument('--api-key', help='API key for authentication')
    parser.add_argument('--dry-run', action='store_true',
                       help='Print execution plan without running')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.config_file):
        print(f"Error: Config file not found: {args.config_file}")
        sys.exit(1)
    
    if args.dry_run:
        # Just print the execution plan
        with open(args.config_file, 'r') as f:
            config = json.load(f)
        
        print(f"\nExecution Plan for: {config['config_id']}")
        print(f"Customer: {config['customer']}")
        print(f"Location: {config['location']}")
        print(f"\nPhases:")
        for phase_name, phase in sorted(config['execution_plan'].items()):
            print(f"\n{phase_name}: {phase['name']}")
            print(f"  Groups: {phase['groups']}")
            print(f"  Parallel: {phase['parallel']}")
            print(f"  Estimated: {phase['estimated_runtime']}")
            for group_name in phase['groups']:
                group = config['step_groups'][group_name]
                print(f"    - {group_name}: {len(group['step_ids'])} steps ({group['module']})")
        
        print(f"\nTotal Steps: {len(config['steps'])}")
        print(f"Estimated Runtime: {config['estimated_total_runtime']}")
        sys.exit(0)
    
    # Execute configuration
    try:
        executor = ConfigExecutor(args.config_file, args.api_url, args.api_key)
        success = executor.execute()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nExecution interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nFatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

