# Run Analysis

Execute the generated execution configurations by triggering the execution API.

## Overview

This step takes the execution config from `generate_execution_config` and:
1. Submits steps to the execution API
2. Monitors execution progress
3. Handles parallelization based on step groups
4. Manages execution phases
5. Saves execution state
6. Provides real-time logging

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Basic Execution

```bash
python execute_config.py path/to/config.json --api-url http://your-api-url
```

### With API Key

```bash
export EXECUTION_API_KEY='your-api-key'
python execute_config.py path/to/config.json --api-url http://your-api-url
```

Or pass directly:

```bash
python execute_config.py path/to/config.json --api-url http://your-api-url --api-key your-api-key
```

### Dry Run

See the execution plan without actually running:

```bash
python execute_config.py path/to/config.json --dry-run
```

## Example

```bash
# Execute Biomet configuration
python execute_config.py \
  ../generate_execution_config/execution_configs/config_Biomet_20260107.json \
  --api-url http://localhost:8000
```

## Features

### Phase-Based Execution

The executor runs configs in phases according to the `execution_plan`:

```
Phase 1: Data Loading (parallel)
  → All data loading steps execute simultaneously
  
Phase 2: Preprocessing (parallel)
  → Preprocessing steps execute after data loading
  
Phase 3: Core Models (sequential)
  → Core analysis models run in sequence
  
Phase 4: Individual Models (parallel)
  → Independent models execute simultaneously
  
... and so on
```

### Parallelization

Steps within parallel groups execute concurrently:
- **data_loading group**: All load operations in parallel
- **preprocessing group**: Independent preprocessing in parallel
- **individual_models group**: Multiple models in parallel
- **reporting group**: All report generation in parallel

### Execution Tracking

The executor tracks:
- **Step status**: pending → running → completed/failed
- **Execution IDs**: API-assigned IDs for each step
- **Results**: Outputs from completed steps
- **Execution log**: Timestamped log of all events

### State Persistence

Execution state is saved after each group completion to:
```
config_name_execution_state.json
```

This includes:
- Step status for all steps
- Execution IDs
- Results
- Recent log entries

### Error Handling

- **Step failures**: Logged with error details
- **API errors**: Handled gracefully with error messages
- **Interruption**: Ctrl+C saves current state
- **Phase failures**: Execution stops at failed phase

## Execution API Contract

The executor expects an API with the following endpoints:

### POST /api/v1/execute/step

Submit a step for execution.

**Request:**
```json
{
  "step_id": "load_satellite_vegetation",
  "step_name": "Load Satellite Vegetation Data",
  "function": "load_satellite_data",
  "module": "data_loaders",
  "arguments": {
    "location": "Los Angeles County, California",
    "start_date": "2014-01-01",
    "end_date": "2024-12-31",
    "data_types": ["vegetation health", "fuel load"],
    "output_path": "data/loaded/satellite_data.nc"
  },
  "group": "data_loading",
  "output": "data/loaded/satellite_data.nc"
}
```

**Response:**
```json
{
  "success": true,
  "execution_id": "exec_123456",
  "message": "Step submitted successfully"
}
```

### GET /api/v1/execute/status/{execution_id}

Check execution status.

**Response:**
```json
{
  "success": true,
  "execution_id": "exec_123456",
  "status": "running|completed|failed",
  "progress": 45,
  "message": "Processing data..."
}
```

### GET /api/v1/execute/result/{execution_id}

Get execution result.

**Response:**
```json
{
  "success": true,
  "execution_id": "exec_123456",
  "status": "completed",
  "output_path": "data/loaded/satellite_data.nc",
  "metadata": {
    "duration_seconds": 120,
    "output_size_mb": 450
  }
}
```

## Output

### Console Output

```
##########################################################################
# STARTING EXECUTION
##########################################################################
Config ID: exec_biomet_la_wildfire_20260107
Customer: Biomet
Location: Los Angeles County, California
Total Steps: 25
Estimated Runtime: 19-30 hours (with parallelization)
##########################################################################

======================================================================
PHASE: Data Loading
======================================================================
Groups: ['data_loading']
Parallel: True
Estimated Runtime: 2-3 hours (parallel)

=== Executing group: data_loading ===
Description: Load all required data sources
Module: data_loaders
Steps: 10
Parallel: True

[2026-01-07 17:00:00] [INFO] Executing 10 steps in parallel
[2026-01-07 17:00:01] [INFO] Executing step: load_satellite_vegetation (Load Satellite Vegetation Data)
[2026-01-07 17:00:01] [INFO] Step load_satellite_vegetation submitted with execution_id: exec_001
...
[2026-01-07 19:15:00] [INFO] All 10 parallel steps completed successfully
[2026-01-07 19:15:01] [INFO] Phase Data Loading completed successfully

...

##########################################################################
# EXECUTION COMPLETED SUCCESSFULLY
##########################################################################
Total Time: 21.5 hours (1290 minutes)
Steps Completed: 25
Output Directory: outputs/biomet_la_wildfire_20260107
##########################################################################
```

### Execution State File

```json
{
  "config_id": "exec_biomet_la_wildfire_20260107",
  "started_at": "2026-01-07 17:00:00",
  "step_status": {
    "load_satellite_vegetation": "completed",
    "load_climate_data": "completed",
    ...
  },
  "step_executions": {
    "load_satellite_vegetation": "exec_001",
    "load_climate_data": "exec_002",
    ...
  },
  "step_results": {
    "load_satellite_vegetation": {
      "output_path": "data/loaded/satellite_data.nc",
      "duration_seconds": 7200
    },
    ...
  },
  "execution_log": [
    {
      "timestamp": "2026-01-07 17:00:00",
      "level": "INFO",
      "message": "Executing step: load_satellite_vegetation"
    },
    ...
  ]
}
```

## Configuration

### Environment Variables

- `EXECUTION_API_KEY`: API key for authentication
- `EXECUTION_API_URL`: Default API URL (can override with --api-url)

### Polling Interval

The executor polls for step status every 5 seconds. This can be adjusted in the code:

```python
time.sleep(5)  # Poll every 5 seconds
```

### Parallel Execution Limit

Maximum 10 steps execute in parallel simultaneously:

```python
ThreadPoolExecutor(max_workers=min(len(step_ids), 10))
```

## Troubleshooting

### API Connection Issues

```
Error: Failed to submit step: Connection refused
```

**Solution**: Check that the API server is running and accessible at the specified URL.

### Authentication Failures

```
Error: 401 Unauthorized
```

**Solution**: Ensure `EXECUTION_API_KEY` is set or pass `--api-key`.

### Step Failures

```
[ERROR] Step load_satellite_vegetation failed: Data source unavailable
```

**Solution**: Check the execution log in the state file for detailed error messages.

### Interrupted Execution

If execution is interrupted (Ctrl+C), the state file contains:
- Steps completed before interruption
- Steps that were running
- Execution IDs for querying status later

You can resume by checking the state file and resubmitting failed/pending steps.

## Advanced Usage

### Custom Polling Function

For custom status checking:

```python
from execute_config import ConfigExecutor

executor = ConfigExecutor(config_path, api_url, api_key)
# Customize polling logic
executor.execute()
```

### Monitoring from Another Process

Read the state file to monitor progress:

```python
import json

with open('config_execution_state.json', 'r') as f:
    state = json.load(f)

completed = sum(1 for s in state['step_status'].values() if s == 'completed')
total = len(state['step_status'])
print(f"Progress: {completed}/{total} steps completed")
```

## Next Steps

After successful execution:
1. Review the execution state file
2. Check output files in the specified output directory
3. Verify deliverables (reports, GIS packages, etc.)
4. Share results with the customer
