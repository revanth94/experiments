#!/usr/bin/env python3
"""
Demo Execution - Simulates the execution without requiring API server
Shows what the execution would look like
"""

import json
import time
import random
from datetime import datetime


def print_header(text, char='='):
    """Print a formatted header"""
    width = 70
    print(f"\n{char * width}")
    print(f"{text.center(width)}")
    print(f"{char * width}\n")


def print_phase_header(phase_name, phase_info):
    """Print phase header"""
    print(f"\n{'=' * 70}")
    print(f"PHASE: {phase_info['name']}")
    print(f"{'=' * 70}")
    print(f"Groups: {phase_info['groups']}")
    print(f"Parallel: {phase_info['parallel']}")
    print(f"Estimated Runtime: {phase_info['estimated_runtime']}")
    print()


def print_group_header(group_name, group_info):
    """Print group header"""
    print(f"=== Executing group: {group_name} ===")
    print(f"Description: {group_info['description']}")
    print(f"Module: {group_info['module']}")
    print(f"Steps: {len(group_info['step_ids'])}")
    print(f"Parallel: {group_info['parallel']}")
    print()


def log(message, level='INFO'):
    """Log a message with timestamp"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] [{level}] {message}")


def simulate_step(step_id, step_name):
    """Simulate executing a single step"""
    log(f"Executing step: {step_id} ({step_name})")
    
    # Simulate submission
    execution_id = f"exec_{random.randint(1000, 9999)}"
    log(f"Step {step_id} submitted with execution_id: {execution_id}")
    
    # Simulate execution time (much faster for demo)
    time.sleep(random.uniform(0.5, 2.0))
    
    # Simulate occasional progress updates
    if random.random() < 0.3:
        log(f"Step {step_id} progress: 50%")
        time.sleep(random.uniform(0.3, 0.8))
    
    # Simulate success (100% success rate for demo)
    log(f"Step {step_id} completed successfully")
    return True


def execute_steps_parallel(step_ids, steps_dict):
    """Simulate parallel execution"""
    log(f"Executing {len(step_ids)} steps in parallel")
    
    results = {}
    for step_id in step_ids:
        step = steps_dict[step_id]
        results[step_id] = simulate_step(step_id, step['step_name'])
        # Small delay between parallel starts
        time.sleep(0.1)
    
    all_success = all(results.values())
    if all_success:
        log(f"All {len(step_ids)} parallel steps completed successfully")
    else:
        failed = [sid for sid, success in results.items() if not success]
        log(f"{len(failed)} steps failed: {failed}", 'ERROR')
    
    return all_success


def execute_steps_sequential(step_ids, steps_dict):
    """Simulate sequential execution"""
    log(f"Executing {len(step_ids)} steps sequentially")
    
    for step_id in step_ids:
        step = steps_dict[step_id]
        success = simulate_step(step_id, step['step_name'])
        if not success:
            log(f"Sequential execution failed at step {step_id}", 'ERROR')
            return False
    
    log(f"All {len(step_ids)} sequential steps completed successfully")
    return True


def execute_group(group_name, group_info, steps_dict):
    """Execute a step group"""
    print_group_header(group_name, group_info)
    
    step_ids = group_info['step_ids']
    
    if group_info['parallel']:
        success = execute_steps_parallel(step_ids, steps_dict)
    else:
        success = execute_steps_sequential(step_ids, steps_dict)
    
    return success


def execute_phase(phase_name, phase_info, config):
    """Execute a phase"""
    print_phase_header(phase_name, phase_info)
    
    # Create steps lookup
    steps_dict = {step['step_id']: step for step in config['steps']}
    
    # Execute each group in the phase
    for group_name in phase_info['groups']:
        group_info = config['step_groups'][group_name]
        success = execute_group(group_name, group_info, steps_dict)
        
        if not success:
            log(f"Phase {phase_name} failed at group {group_name}", 'ERROR')
            return False
    
    log(f"Phase {phase_info['name']} completed successfully\n")
    return True


def main():
    """Main execution"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python demo_execution.py <config_file>")
        sys.exit(1)
    
    config_file = sys.argv[1]
    
    # Load config
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    # Print header
    print_header("DEMO EXECUTION (SIMULATED)")
    log(f"Config ID: {config['config_id']}")
    log(f"Customer: {config['customer']}")
    log(f"Location: {config['location']}")
    log(f"Total Steps: {len(config['steps'])}")
    log(f"Estimated Runtime: {config['estimated_total_runtime']}")
    log("NOTE: This is a simulated demo running at 10x speed")
    
    start_time = time.time()
    
    # Execute each phase
    phase_names = sorted(config['execution_plan'].keys())
    
    for phase_name in phase_names:
        phase_info = config['execution_plan'][phase_name]
        success = execute_phase(phase_name, phase_info, config)
        
        if not success:
            log(f"Execution failed at phase {phase_name}", 'ERROR')
            return False
    
    # Calculate total time
    end_time = time.time()
    total_seconds = end_time - start_time
    total_minutes = total_seconds / 60
    
    # Print completion
    print_header("EXECUTION COMPLETED SUCCESSFULLY")
    log(f"Demo Time: {total_minutes:.2f} minutes ({total_seconds:.1f} seconds)")
    log(f"Estimated Real Time: {config['estimated_total_runtime']}")
    log(f"Steps Completed: {len(config['steps'])}")
    log(f"Output Directory: {config.get('output_directory', 'N/A')}")
    print_header("", char='#')
    
    print("\n✅ Demo execution completed!")
    print("\nIn a real execution:")
    print("  - Steps would call actual data loading/processing functions")
    print("  - Execution would take 19-30 hours (not 2 minutes)")
    print("  - Results would be saved to the output directory")
    print("  - Deliverables (reports, GIS packages) would be generated")
    print("\nTo run with real API:")
    print("  1. Start: python mock_server/mock_api_server.py")
    print("  2. Execute: python execute_config.py config.json --api-url http://localhost:8000")
    
    return True


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()

