#!/usr/bin/env python3
"""
Mock Execution API Server
For testing the execution workflow without a real backend
"""

import json
import random
import time
import uuid
from datetime import datetime
from flask import Flask, request, jsonify
from typing import Dict

app = Flask(__name__)

# In-memory storage
executions = {}  # execution_id -> execution data


class MockExecution:
    """Mock execution that simulates step processing"""
    
    def __init__(self, step_data: Dict):
        self.execution_id = f"exec_{uuid.uuid4().hex[:8]}"
        self.step_id = step_data['step_id']
        self.step_name = step_data['step_name']
        self.function = step_data['function']
        self.module = step_data['module']
        self.arguments = step_data['arguments']
        self.output = step_data.get('output')
        
        self.status = 'pending'
        self.progress = 0
        self.submitted_at = datetime.now().isoformat()
        self.started_at = None
        self.completed_at = None
        self.error = None
        
        # Simulate varying execution times based on module
        self.duration_seconds = self._estimate_duration()
        self.elapsed = 0
    
    def _estimate_duration(self) -> int:
        """Estimate execution duration based on function type"""
        if self.module == 'data_loaders':
            return random.randint(30, 120)  # 30-120 seconds
        elif self.module == 'data_processors':
            return random.randint(15, 60)   # 15-60 seconds
        elif self.module == 'models':
            return random.randint(60, 180)  # 60-180 seconds
        elif self.module == 'reporting':
            return random.randint(20, 60)   # 20-60 seconds
        return 60
    
    def update(self):
        """Update execution status"""
        if self.status == 'pending':
            self.status = 'running'
            self.started_at = datetime.now().isoformat()
        
        elif self.status == 'running':
            self.elapsed += 5  # Update every 5 seconds
            self.progress = min(100, int((self.elapsed / self.duration_seconds) * 100))
            
            if self.elapsed >= self.duration_seconds:
                # Simulate occasional failures (5% chance)
                if random.random() < 0.05:
                    self.status = 'failed'
                    self.error = f"Simulated error in {self.function}"
                else:
                    self.status = 'completed'
                self.completed_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'execution_id': self.execution_id,
            'step_id': self.step_id,
            'step_name': self.step_name,
            'function': self.function,
            'module': self.module,
            'status': self.status,
            'progress': self.progress,
            'submitted_at': self.submitted_at,
            'started_at': self.started_at,
            'completed_at': self.completed_at,
            'error': self.error,
            'output': self.output
        }


@app.route('/api/v1/execute/step', methods=['POST'])
def submit_step():
    """Submit a step for execution"""
    try:
        step_data = request.json
        
        # Validate required fields
        required = ['step_id', 'step_name', 'function', 'module', 'arguments']
        if not all(field in step_data for field in required):
            return jsonify({
                'success': False,
                'error': 'Missing required fields'
            }), 400
        
        # Create mock execution
        execution = MockExecution(step_data)
        executions[execution.execution_id] = execution
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] "
              f"Submitted: {execution.step_id} "
              f"(execution_id: {execution.execution_id})")
        
        return jsonify({
            'success': True,
            'execution_id': execution.execution_id,
            'message': f'Step {step_data["step_id"]} submitted successfully',
            'estimated_duration': execution.duration_seconds
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/v1/execute/status/<execution_id>', methods=['GET'])
def check_status(execution_id: str):
    """Check execution status"""
    if execution_id not in executions:
        return jsonify({
            'success': False,
            'error': 'Execution not found'
        }), 404
    
    execution = executions[execution_id]
    execution.update()
    
    return jsonify({
        'success': True,
        'execution_id': execution_id,
        'status': execution.status,
        'progress': execution.progress,
        'message': f'Processing {execution.step_name}...' if execution.status == 'running' else None,
        'error': execution.error
    }), 200


@app.route('/api/v1/execute/result/<execution_id>', methods=['GET'])
def get_result(execution_id: str):
    """Get execution result"""
    if execution_id not in executions:
        return jsonify({
            'success': False,
            'error': 'Execution not found'
        }), 404
    
    execution = executions[execution_id]
    
    if execution.status == 'running':
        return jsonify({
            'success': False,
            'error': 'Execution still in progress'
        }), 400
    
    result = {
        'success': execution.status == 'completed',
        'execution_id': execution_id,
        'step_id': execution.step_id,
        'status': execution.status,
        'output_path': execution.output,
        'metadata': {
            'duration_seconds': execution.elapsed,
            'function': execution.function,
            'module': execution.module,
            'started_at': execution.started_at,
            'completed_at': execution.completed_at
        }
    }
    
    if execution.error:
        result['error'] = execution.error
    
    return jsonify(result), 200


@app.route('/api/v1/execute/stats', methods=['GET'])
def get_stats():
    """Get overall execution statistics"""
    total = len(executions)
    by_status = {}
    by_module = {}
    
    for execution in executions.values():
        # Count by status
        status = execution.status
        by_status[status] = by_status.get(status, 0) + 1
        
        # Count by module
        module = execution.module
        by_module[module] = by_module.get(module, 0) + 1
    
    return jsonify({
        'success': True,
        'total_executions': total,
        'by_status': by_status,
        'by_module': by_module
    }), 200


@app.route('/api/v1/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'status': 'healthy',
        'active_executions': len([e for e in executions.values() if e.status == 'running']),
        'timestamp': datetime.now().isoformat()
    }), 200


if __name__ == '__main__':
    print("\n" + "="*70)
    print("Mock Execution API Server")
    print("="*70)
    print("\nEndpoints:")
    print("  POST   /api/v1/execute/step")
    print("  GET    /api/v1/execute/status/<execution_id>")
    print("  GET    /api/v1/execute/result/<execution_id>")
    print("  GET    /api/v1/execute/stats")
    print("  GET    /api/v1/health")
    print("\nStarting server on http://localhost:8000...")
    print("="*70 + "\n")
    
    app.run(host='0.0.0.0', port=8000, debug=True)

