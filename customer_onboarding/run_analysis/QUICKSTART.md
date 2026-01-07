# Quick Start Guide

Get started with running analysis configs in 5 minutes.

## 1. Install Dependencies

```bash
cd /Users/revanthk/Learning/experiments/customer_onboarding/run_analysis
pip install -r requirements.txt
```

## 2. Start Mock API Server

In one terminal:

```bash
python mock_api_server.py
```

You should see:

```
======================================================================
Mock Execution API Server
======================================================================

Endpoints:
  POST   /api/v1/execute/step
  GET    /api/v1/execute/status/<execution_id>
  GET    /api/v1/execute/result/<execution_id>
  GET    /api/v1/execute/stats
  GET    /api/v1/health

Starting server on http://localhost:8000...
======================================================================
```

## 3. Run Execution (Dry Run First)

In another terminal:

```bash
# See the execution plan
python execute_config.py \
  ../generate_execution_config/execution_configs/config_Biomet_20260107.json \
  --dry-run
```

Output:

```
Execution Plan for: exec_biomet_la_wildfire_20260107
Customer: Biomet
Location: Los Angeles County, California

Phases:

phase_1: Data Loading
  Groups: ['data_loading']
  Parallel: True
  Estimated: 2-3 hours (parallel)
    - data_loading: 10 steps (data_loaders)

phase_2: Data Preprocessing
  Groups: ['preprocessing']
  Parallel: True
  Estimated: 1-2 hours (parallel)
    - preprocessing: 2 steps (data_processors)

...

Total Steps: 25
Estimated Runtime: 19-30 hours (with parallelization)
```

## 4. Run Actual Execution

```bash
python execute_config.py \
  ../generate_execution_config/execution_configs/config_Biomet_20260107.json \
  --api-url http://localhost:8000
```

Watch the progress:

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
[2026-01-07 17:00:01] [INFO] Executing step: load_satellite_vegetation
[2026-01-07 17:00:01] [INFO] Step load_satellite_vegetation submitted with execution_id: exec_a1b2c3d4
...
```

## 5. Monitor Progress

### Check Execution State

While execution is running, check the state file:

```bash
cat ../generate_execution_config/execution_configs/config_Biomet_20260107_execution_state.json
```

### Check API Stats

```bash
curl http://localhost:8000/api/v1/health
curl http://localhost:8000/api/v1/execute/stats
```

## Example Output

### Successful Execution

```
[2026-01-07 19:30:45] [INFO] All 4 parallel steps completed successfully

##########################################################################
# EXECUTION COMPLETED SUCCESSFULLY
##########################################################################
Total Time: 0.12 hours (7.2 minutes)
Steps Completed: 25
Output Directory: outputs/biomet_la_wildfire_20260107
##########################################################################
```

### Execution State File

```json
{
  "config_id": "exec_biomet_la_wildfire_20260107",
  "started_at": "2026-01-07 19:23:30",
  "step_status": {
    "load_satellite_vegetation": "completed",
    "load_climate_data": "completed",
    "load_drought_data": "completed",
    ...
  },
  "step_executions": {
    "load_satellite_vegetation": "exec_a1b2c3d4",
    ...
  },
  "step_results": {
    "load_satellite_vegetation": {
      "output_path": "data/biomet_la/loaded/satellite_vegetation_2014_2024.nc",
      "duration_seconds": 67
    },
    ...
  }
}
```

## Testing with Real API

When you have a real execution API:

```bash
# Set API credentials
export EXECUTION_API_KEY='your-actual-api-key'

# Run against production API
python execute_config.py \
  ../generate_execution_config/execution_configs/config_Biomet_20260107.json \
  --api-url https://your-api-domain.com
```

## Troubleshooting

### Mock API Not Running

```
Error: Connection refused
```

**Solution**: Make sure the mock API server is running in another terminal.

### Config File Not Found

```
Error: Config file not found
```

**Solution**: Use the correct path to your config file. Use `--dry-run` first to test.

### Step Failures (Mock API)

The mock API simulates a 5% failure rate. If steps fail:

1. Check the execution state file for error details
2. The mock API logs errors to console
3. Re-run with the same config to try again

## Next Steps

- Customize the mock API behavior in `mock_api_server.py`
- Implement a real execution backend
- Add monitoring dashboards
- Set up automated execution pipelines

