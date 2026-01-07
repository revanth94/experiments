# Run Analysis Phase - LLM Context

## Your Role

You are responsible for **executing the generated execution configuration** and **monitoring the analysis** through to completion. This is the final phase where the planned workflow is actually executed.

## Context

**Previous Phase**: Generate Execution Config
**Input**: Execution configuration JSON file (`config_{customer}_{date}.json`)
**Output**: Analysis results and deliverables (reports, GIS packages, data files)

## Task Overview

1. Load the execution configuration
2. Choose appropriate execution method (demo or API)
3. Trigger the execution
4. Monitor progress through all phases
5. Handle errors appropriately
6. Verify deliverables upon completion

---

## Execution Methods

### Method 1: Demo Execution (Simulated)

**Purpose**: Quick demonstration or testing of the workflow

**Command**:
```bash
python demo_execution.py ../generate_execution_config/execution_configs/config_{customer}_{date}.json
```

**Characteristics**:
- ⚡ Fast: Completes in 30-60 seconds (simulated)
- 🎭 Simulates real execution behavior
- ✅ Shows all phases and steps
- 🔍 Useful for validation and demonstration
- ⚠️ No actual data processing or results

**When to use**:
- Testing configuration correctness
- Demonstrating workflow to stakeholders
- Quick validation before real execution
- Understanding execution flow

---

### Method 2: API Execution (Real)

**Purpose**: Actual execution with real data processing and analysis

**Setup**:
```bash
# Terminal 1: Start the API server
cd mock_server
python mock_api_server.py

# Terminal 2: Execute the configuration
cd ..
python execute_config.py \
  ../generate_execution_config/execution_configs/config_{customer}_{date}.json
```

**Characteristics**:
- 🐢 Slow: 19-30 hours for full execution
- 🔧 Processes real data
- 📊 Generates actual deliverables
- 💾 Persists state for resumability
- 🔍 Provides real-time monitoring

**When to use**:
- Production execution
- Generating actual customer deliverables
- Real data processing and analysis

---

## Execution Configuration Structure

The config you'll be executing has this structure:

```json
{
  "config_id": "exec_{customer}_{location}_{date}",
  "customer": "Customer Name",
  "location": "Geographic Area",
  
  "step_groups": {
    "data_loading": {
      "description": "Load all data sources",
      "module": "data_loaders",
      "step_ids": ["step1", "step2", ...],
      "parallel": true
    },
    ...
  },
  
  "execution_plan": {
    "phase_1": {
      "name": "Data Loading",
      "groups": ["data_loading"],
      "parallel": true,
      "estimated_runtime": "2-3 hours"
    },
    ...
  },
  
  "steps": [
    {
      "step_id": "step1",
      "step_name": "Descriptive Name",
      "function": "function_to_call",
      "catalog": "data_loaders",
      "arguments": {...},
      "dependencies": []
    },
    ...
  ]
}
```

---

## Execution Flow

### Phase-by-Phase Execution

The execution proceeds through phases in sequence:

```
Phase 1: Data Loading
  ├─ Group: data_loading (parallel)
  │   ├─ load_satellite_vegetation
  │   ├─ load_climate_data
  │   └─ ... (10 steps total)
  └─ ✓ Complete

Phase 2: Data Preprocessing  
  ├─ Group: preprocessing (parallel)
  │   ├─ preprocess_spatial_raster
  │   └─ preprocess_climate_temporal
  └─ ✓ Complete

Phase 3: Core Risk Assessment
  ├─ Group: core_models (sequential)
  │   ├─ run_historical_pattern_analysis
  │   └─ run_wildfire_risk_index
  └─ ✓ Complete

Phase 4: Individual Impact Models
  ├─ Group: individual_models (parallel)
  │   ├─ run_fuel_load_assessment
  │   ├─ run_drought_impact_model
  │   ├─ run_air_quality_fire_impact
  │   ├─ run_habitat_vulnerability_model
  │   └─ run_post_fire_erosion_model
  └─ ✓ Complete

Phase 5: Dependent Models
  ├─ Group: dependent_models (sequential)
  │   └─ run_watershed_fire_impact_model
  └─ ✓ Complete

Phase 6: Integrated Analysis
  ├─ Group: integrated_analysis (sequential)
  │   └─ run_integrated_fire_risk_model
  └─ ✓ Complete

Phase 7: Reporting and Export
  ├─ Group: reporting (parallel)
  │   ├─ generate_executive_summary
  │   ├─ generate_technical_report
  │   ├─ export_gis_package_shapefiles
  │   └─ export_gis_package_geotiff
  └─ ✓ Complete

═══════════════════════════
    EXECUTION COMPLETE
═══════════════════════════
```

---

## Monitoring and Progress Tracking

### What to Monitor

1. **Phase Progress**
   - Which phase is currently executing
   - How many phases remain
   - Estimated time for current phase

2. **Step Status**
   - Individual step execution
   - Step success/failure
   - Step duration

3. **Group Execution**
   - Parallel vs sequential execution
   - Group-level progress
   - Dependencies being respected

4. **Overall Progress**
   - Total steps completed
   - Total steps remaining
   - Overall percentage complete

### Example Monitoring Output

```
[2026-01-07 16:21:33] [INFO] Config ID: exec_biomet_la_wildfire_20260107
[2026-01-07 16:21:33] [INFO] Customer: Biomet
[2026-01-07 16:21:33] [INFO] Location: Los Angeles County, California
[2026-01-07 16:21:33] [INFO] Total Steps: 25
[2026-01-07 16:21:33] [INFO] Estimated Runtime: 19-30 hours

======================================================================
PHASE: Data Loading
======================================================================

[2026-01-07 16:21:33] [INFO] Executing 10 steps in parallel
[2026-01-07 16:21:33] [INFO] Executing step: load_satellite_vegetation
[2026-01-07 16:21:33] [INFO] Step load_satellite_vegetation submitted
[2026-01-07 16:21:34] [INFO] Step load_satellite_vegetation completed
[2026-01-07 16:21:47] [INFO] All 10 parallel steps completed
[2026-01-07 16:21:47] [INFO] Phase Data Loading completed successfully
```

---

## Error Handling

### Types of Errors

1. **Configuration Errors**
   - Missing required fields
   - Invalid function references
   - Malformed arguments
   - **Action**: Validate config before execution

2. **Execution Errors**
   - Function execution failures
   - Data loading issues
   - Timeout errors
   - **Action**: Log error, retry if transient, escalate if persistent

3. **Dependency Errors**
   - Missing input data from previous steps
   - Circular dependencies
   - **Action**: Check step ordering and dependencies

4. **API Errors**
   - Connection failures
   - Server timeouts
   - Invalid responses
   - **Action**: Check API availability, retry with backoff

### Error Response Strategy

```python
def handle_execution_error(error, step_info):
    """
    Strategy for handling execution errors
    """
    if is_transient_error(error):
        # Network issues, temporary unavailability
        log_warning(f"Transient error in {step_info['step_id']}, retrying...")
        retry_with_backoff(step_info, max_retries=3)
    
    elif is_data_error(error):
        # Data quality, missing data
        log_error(f"Data error in {step_info['step_id']}: {error}")
        mark_step_as_failed(step_info)
        continue_to_next_step()  # If not critical
    
    elif is_critical_error(error):
        # Core system failures
        log_critical(f"Critical error in {step_info['step_id']}: {error}")
        halt_execution()
        notify_operators()
    
    else:
        log_error(f"Unknown error: {error}")
        escalate_to_human()
```

---

## Parallelization Strategy

### Parallel Execution
Steps within a parallel group execute **simultaneously**:

```
Group: data_loading (parallel: true)
├─ load_satellite  ─────┐
├─ load_climate    ─────┤ All execute at once
├─ load_drought    ─────┤ No dependencies between them
└─ load_air_quality ────┘
```

**Benefits**: 40% faster than sequential execution

### Sequential Execution
Steps within a sequential group execute **one after another**:

```
Group: core_models (parallel: false)
├─ run_historical_pattern_analysis (depends on data loading)
│   ↓
└─ run_wildfire_risk_index (depends on historical patterns)
```

**Reason**: Dependencies require outputs from previous steps

---

## State Persistence

### Why State Matters
Long-running executions (19-30 hours) need to:
- **Resume** after failures or interruptions
- **Track** progress across system restarts
- **Report** status to external systems
- **Audit** execution history

### State Files
The API execution creates state files:

```json
{
  "analysis_run_id": "a7f3c891-...",
  "config_id": "exec_biomet_la_wildfire_20260107",
  "status": "RUNNING",
  "progress": 45.2,
  "current_phase": "phase_3",
  "completed_steps": ["step1", "step2", ...],
  "failed_steps": [],
  "start_time": "2026-01-07T08:00:00Z",
  "last_update": "2026-01-07T14:30:00Z"
}
```

---

## Deliverables

### Expected Outputs

Upon successful completion, the following deliverables should be generated:

1. **Executive Summary Report** (PDF)
   - High-level findings
   - Key risk areas
   - Recommendations
   - Target audience: Decision makers

2. **Technical Report** (PDF)
   - Detailed methodology
   - Data sources and quality
   - Model parameters
   - Detailed results
   - Target audience: Technical staff

3. **GIS Package - Shapefiles** (ZIP)
   - Vector data
   - Risk zones
   - Impact areas
   - Attribute tables

4. **GIS Package - GeoTIFF** (ZIP)
   - Raster layers
   - Risk maps
   - Heatmaps
   - Continuous data

5. **Raw Data Exports** (CSV/JSON)
   - Processed datasets
   - Model outputs
   - Time series data

### Deliverable Locations
```
outputs/{customer}_{location}_{date}/
├── reports/
│   ├── executive_summary.pdf
│   └── technical_report.pdf
├── gis/
│   ├── shapefiles.zip
│   └── geotiff.zip
└── data/
    ├── processed_data.csv
    └── model_outputs.json
```

---

## API Endpoints Reference

### POST /api/v1/trigger_analysis
Trigger a new analysis execution.

**Request**:
```json
{
  "config_id": "exec_biomet_...",
  "steps": [...],
  "execution_plan": {...}
}
```

**Response**:
```json
{
  "message": "Analysis triggered",
  "analysis_run_id": "a7f3c891-..."
}
```

### GET /api/v1/analysis_status/{run_id}
Get the status of an ongoing analysis.

**Response**:
```json
{
  "status": "RUNNING",
  "progress": 45.2,
  "message": "Executing phase: Core Risk Assessment",
  "current_phase": "phase_3"
}
```

### POST /api/v1/cancel_analysis/{run_id}
Cancel a running analysis.

**Response**:
```json
{
  "message": "Analysis cancellation requested"
}
```

---

## Your Monitoring Responsibilities

### During Execution

1. **Track Progress**
   - Monitor phase transitions
   - Log completion percentages
   - Note any warnings

2. **Report Status** (if interactive)
   - Inform user of major milestones
   - Report when phases complete
   - Provide time estimates for remaining work

3. **Handle Issues**
   - Detect and log errors
   - Retry transient failures
   - Escalate persistent problems

4. **Verify Success**
   - Confirm all phases complete
   - Check deliverables are generated
   - Validate output files exist

### Post-Execution

1. **Verify Deliverables**
   - Check all expected files exist
   - Validate file formats
   - Confirm file sizes are reasonable

2. **Generate Summary**
   - Total execution time
   - Any issues encountered
   - Location of deliverables

3. **Notify Customer** (if interactive)
   - Inform of completion
   - Provide deliverable locations
   - Summarize key findings (if available)

---

## Dry Run Mode

Before executing for real, you can do a **dry run**:

```bash
python execute_config.py config.json --dry-run
```

**Dry run output**:
- Shows execution plan
- Lists all phases and groups
- Displays estimated runtimes
- **Does NOT** trigger actual execution

**Use for**:
- Validating configuration correctness
- Understanding execution flow
- Estimating completion time
- Demonstrating plan to stakeholders

---

## Example Execution Session

```bash
$ cd run_analysis

# Step 1: Review the execution plan (dry run)
$ python execute_config.py \
  ../generate_execution_config/execution_configs/config_Biomet_20260107.json \
  --dry-run

# Output shows:
# - 25 total steps
# - 7 phases
# - Estimated 19-30 hours

# Step 2: Start the API server (in background)
$ cd mock_server
$ python mock_api_server.py &
[1] 12345
Mock Analysis API Server running on http://127.0.0.1:8000

# Step 3: Execute for real
$ cd ..
$ python execute_config.py \
  ../generate_execution_config/execution_configs/config_Biomet_20260107.json

# Monitor progress:
[2026-01-07 08:00:00] Triggering analysis...
[2026-01-07 08:00:01] Analysis started with ID: a7f3c891-...
[2026-01-07 08:00:05] Phase 1: Data Loading - RUNNING
[2026-01-07 10:30:00] Phase 1: Data Loading - COMPLETED
[2026-01-07 10:30:05] Phase 2: Preprocessing - RUNNING
...
[2026-01-08 14:00:00] Phase 7: Reporting - COMPLETED
[2026-01-08 14:00:05] Analysis COMPLETED successfully!

# Step 4: Verify deliverables
$ ls outputs/biomet_la_wildfire_20260107/
reports/  gis/  data/
```

---

## Success Criteria

✅ **Execution is successful if**:
- All phases complete without errors
- All steps execute successfully
- Deliverables are generated
- Output files are valid and complete
- Total time is within estimated range

❌ **Execution has issues if**:
- Any phase fails repeatedly
- Critical steps timeout
- Deliverables are missing or incomplete
- Execution time significantly exceeds estimate

---

## Troubleshooting

### API Server Not Running
**Symptom**: Connection refused errors
**Solution**: Start the API server first
```bash
cd mock_server && python mock_api_server.py
```

### Configuration Not Found
**Symptom**: File not found errors
**Solution**: Verify config path is correct
```bash
ls ../generate_execution_config/execution_configs/
```

### Validation Errors
**Symptom**: Config validation failures
**Solution**: Re-run config validation
```bash
cd ../generate_execution_config
python config_validator.py execution_configs/config.json
```

### Execution Timeout
**Symptom**: Steps take too long
**Solution**: Check if it's expected duration or actual hang

---

## Key Reminders

1. **Always dry run first** to verify the execution plan
2. **Monitor actively** during execution (especially first few phases)
3. **Preserve logs** for debugging and auditing
4. **Verify deliverables** before informing customer
5. **Handle errors gracefully** with appropriate retry logic

---

## Integration Points

### Inputs
- Execution configuration JSON from Phase 3
- Function catalogs (for reference)
- API credentials (if using real API)

### Outputs
- Execution logs
- Progress state files
- Deliverables (reports, GIS, data)
- Completion status

### External Systems
- Execution API (for real processing)
- Data storage (for deliverables)
- Monitoring systems (for observability)

---

You are now ready to execute analyses and monitor them through completion! 🚀

