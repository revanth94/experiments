# Generate Execution Config

This step converts analysis plans into executable configurations with specific Python function calls and arguments.

## What It Does

Takes the analysis plan from `requirement_analysis` and generates a detailed execution config containing:
- **Data loading steps** - Functions to load each required data source
- **Preprocessing steps** - Data alignment and preparation functions
- **Model execution steps** - Functions to run each analysis model in proper sequence
- **Reporting steps** - Functions to generate reports and export results
- **Dependencies** - Specifies which steps must complete before others
- **Parallelization** - Identifies which steps can run in parallel

## Files

### Input
- `../requirement_analysis/analysis_output/analysis_*.json` - Analysis plan from previous step

### Resources
- `catalogs/` - **Organized function catalogs** (data loaders, processors, models, reporting)
  - `data_loaders_catalog.json` - 10 data loading functions
  - `data_processors_catalog.json` - 6 preprocessing functions
  - `models_catalog.json` - 9 analysis model functions
  - `reporting_catalog.json` - 5 reporting/export functions
  - `catalog_index.json` - Index of all catalogs
- `llm_context.md` - Instructions for LLM to generate configs
- `config_validator.py` - Validator to ensure config correctness
- `function_catalog.json` - *(Legacy: kept for backward compatibility)*

### Output
- `execution_configs/config_*.json` - Executable configuration files

## Config Structure

Each config contains a list of steps:

```json
{
  "step_id": "load_satellite_data",
  "function": "load_satellite_data",
  "module": "data_loaders",
  "arguments": {
    "location": "Los Angeles County, California",
    "start_date": "2014-01-01",
    "end_date": "2024-12-31",
    "data_types": ["vegetation health", "fuel load"],
    "output_path": "data/loaded/satellite_vegetation.nc"
  },
  "depends_on": [],
  "output": "data/loaded/satellite_vegetation.nc"
}
```

## Validation

The validator checks:
- ✓ All functions exist in the function catalog
- ✓ All required parameters are provided
- ✓ Parameter types match specifications
- ✓ Step dependencies are valid (no circular dependencies)
- ✓ Referenced step outputs exist
- ✓ Data flow is logical

## Usage

### Generate Config (Using LLM)
Follow the instructions in `llm_context.md` with the analysis plan as input.

### Validate Config
```bash
python config_validator.py execution_configs/config_Biomet_20260107.json
```

### Example: Biomet Config

**Generated for:** Biomet wildfire risk assessment
**Steps:** 26 total steps
- 10 data loading steps (parallel)
- 2 preprocessing steps (parallel)
- 9 model execution steps (sequential with some parallelization)
- 5 reporting/export steps (parallel)

**Estimated Runtime:** 20-28 hours (with parallelization) vs 32-43 hours (sequential)

**Parallelization Groups:**
- `data_loading`: All 10 data sources load simultaneously
- `preprocessing`: Spatial and temporal preprocessing in parallel
- `individual_models`: 5 models run in parallel after core risk assessment
- `reporting`: Report generation and GIS exports in parallel

## Next Steps

After config generation:
1. ✓ Config validated
2. → Execute the workflow (run_analysis step)
3. → Monitor execution progress
4. → Collect deliverables

## Adding New Functions

The function catalogs are organized by purpose in the `catalogs/` directory.

### To add a new function:

1. **Choose the appropriate catalog**:
   - Data loading → `data_loaders_catalog.json`
   - Data processing → `data_processors_catalog.json`
   - Analysis models → `models_catalog.json`
   - Reporting/export → `reporting_catalog.json`

2. **Add function definition**:
```json
{
  "name": "new_function",
  "description": "Function description",
  "parameters": {
    "param_name": {
      "type": "string",
      "required": true,
      "description": "Parameter description"
    }
  },
  "returns": "What the function returns"
}
```

3. **Update `catalogs/catalog_index.json`** to increment the function count

4. **Test with validator**:
```bash
python config_validator.py execution_configs/your_config.json
```

The validator automatically loads all catalogs - no code changes needed!

See `catalogs/README.md` for detailed documentation.
