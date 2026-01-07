# Execution Config Grouping Guide

## Overview

Execution configs are now organized using **catalog-based grouping** for better structure, parallelization, and maintainability.

## Key Concepts

### 1. Step Groups

Steps are organized into groups based on their catalog module:

```json
"step_groups": {
  "data_loading": {
    "description": "Load all required data sources",
    "module": "data_loaders",
    "parallel": true,
    "step_ids": ["load_step1", "load_step2", ...]
  },
  ...
}
```

### 2. Execution Phases

Phases sequence the execution of step groups:

```json
"execution_plan": {
  "phase_1": {
    "name": "Data Loading",
    "groups": ["data_loading"],
    "parallel": true,
    "estimated_runtime": "2-3 hours (parallel)"
  },
  ...
}
```

### 3. Step Assignment

Each step must be assigned to a group:

```json
{
  "step_id": "load_satellite_data",
  "group": "data_loading",
  "function": "load_satellite_data",
  "module": "data_loaders",
  ...
}
```

## Standard Groups

### 📥 data_loading
- **Module:** `data_loaders`
- **Parallel:** Yes
- **Steps:** All `load_*` functions
- **Typical Count:** 5-15 steps
- **Examples:** load_satellite_data, load_climate_data, load_drought_data

### ⚙️ preprocessing
- **Module:** `data_processors`
- **Parallel:** Yes (if processing different data types)
- **Steps:** All `preprocess_*`, `merge_*`, `extract_*`, `calculate_*`, `normalize_*` functions
- **Typical Count:** 2-5 steps
- **Examples:** preprocess_spatial_data, preprocess_temporal_data

### 🎯 core_models
- **Module:** `models`
- **Parallel:** No (sequential)
- **Steps:** Initial analysis models that others depend on
- **Typical Count:** 1-3 steps
- **Examples:** run_historical_pattern_analysis, run_wildfire_risk_index

### 🔬 individual_models
- **Module:** `models`
- **Parallel:** Yes
- **Steps:** Independent analysis models for specific impacts
- **Typical Count:** 3-7 steps
- **Examples:** run_fuel_load_assessment, run_drought_impact_model, run_air_quality_fire_impact

### 🔗 dependent_models (optional)
- **Module:** `models`
- **Parallel:** No
- **Steps:** Models that depend on other individual models
- **Typical Count:** 0-2 steps
- **Examples:** run_watershed_fire_impact_model (depends on erosion model)

### 🎓 integrated_analysis
- **Module:** `models`
- **Parallel:** No (sequential)
- **Steps:** Final synthesis models
- **Typical Count:** 1 step
- **Examples:** run_integrated_fire_risk_model

### 📊 reporting
- **Module:** `reporting`
- **Parallel:** Yes
- **Steps:** All `generate_*`, `export_*`, `create_*` functions
- **Typical Count:** 3-6 steps
- **Examples:** generate_report, export_gis_package, create_web_map

## Typical Execution Flow

```
Phase 1: Data Loading (parallel)
  ↓
Phase 2: Preprocessing (parallel)
  ↓
Phase 3: Core Models (sequential)
  ↓
Phase 4: Individual Models (parallel)
  ↓
Phase 5: Dependent Models (sequential, if needed)
  ↓
Phase 6: Integrated Analysis (sequential)
  ↓
Phase 7: Reporting (parallel)
```

## Benefits

### ✅ Clear Organization
- Steps grouped by functional purpose
- Easy to understand workflow structure
- Catalog module alignment

### ✅ Parallelization Optimization
- Groups clearly marked as parallel or sequential
- Execution engine can optimize parallel groups
- Reduced total runtime

### ✅ Dependency Management
- Dependencies within and between groups
- Clear phase sequencing
- No circular dependencies

### ✅ Maintainability
- Easy to add/remove steps within groups
- Group-level modifications don't affect other groups
- Clear separation of concerns

## Group Assignment Rules

### Rule 1: Match Catalog Module
Each step's `group` must align with its function's catalog module:

| Function Catalog | Group |
|------------------|-------|
| data_loaders | data_loading |
| data_processors | preprocessing |
| models (initial) | core_models |
| models (independent) | individual_models |
| models (final) | integrated_analysis |
| reporting | reporting |

### Rule 2: Include Group Field
Every step MUST have a `group` field:

```json
{
  "step_id": "load_climate_data",
  "group": "data_loading",  // ← Required!
  ...
}
```

### Rule 3: List in step_groups
All groups must be defined in `step_groups` at config level:

```json
{
  "step_groups": {
    "data_loading": { ... },
    "preprocessing": { ... },
    ...
  }
}
```

### Rule 4: Reference in execution_plan
All groups should be referenced in execution phases:

```json
{
  "execution_plan": {
    "phase_1": {
      "groups": ["data_loading"],
      ...
    }
  }
}
```

## Example: Complete Grouping

```json
{
  "config_id": "example_config",
  
  "step_groups": {
    "data_loading": {
      "description": "Load data sources",
      "module": "data_loaders",
      "parallel": true,
      "step_ids": ["load_satellite", "load_climate"]
    },
    "preprocessing": {
      "description": "Preprocess data",
      "module": "data_processors",
      "parallel": true,
      "step_ids": ["preprocess_spatial"]
    },
    "core_models": {
      "description": "Core analysis",
      "module": "models",
      "parallel": false,
      "step_ids": ["run_risk_assessment"]
    },
    "reporting": {
      "description": "Generate outputs",
      "module": "reporting",
      "parallel": true,
      "step_ids": ["generate_report", "export_gis"]
    }
  },
  
  "steps": [
    {
      "step_id": "load_satellite",
      "group": "data_loading",
      "function": "load_satellite_data",
      "module": "data_loaders",
      ...
    },
    {
      "step_id": "preprocess_spatial",
      "group": "preprocessing",
      "function": "preprocess_spatial_data",
      "module": "data_processors",
      "depends_on": ["load_satellite"],
      ...
    },
    {
      "step_id": "run_risk_assessment",
      "group": "core_models",
      "function": "run_wildfire_risk_index",
      "module": "models",
      "depends_on": ["preprocess_spatial"],
      ...
    },
    {
      "step_id": "generate_report",
      "group": "reporting",
      "function": "generate_report",
      "module": "reporting",
      "depends_on": ["run_risk_assessment"],
      ...
    }
  ],
  
  "execution_plan": {
    "phase_1": {
      "name": "Data Loading",
      "groups": ["data_loading"],
      "parallel": true
    },
    "phase_2": {
      "name": "Preprocessing",
      "groups": ["preprocessing"],
      "parallel": true
    },
    "phase_3": {
      "name": "Analysis",
      "groups": ["core_models"],
      "parallel": false
    },
    "phase_4": {
      "name": "Reporting",
      "groups": ["reporting"],
      "parallel": true
    }
  }
}
```

## Validation

The `config_validator.py` checks:
- ✓ All steps have a `group` field
- ✓ All groups in steps exist in `step_groups`
- ✓ All step_ids in `step_groups` exist as steps
- ✓ Module alignment is correct
- ✓ No circular dependencies

Run validation:
```bash
python config_validator.py execution_configs/your_config.json
```

## Common Patterns

### Pattern 1: Basic Workflow
```
data_loading → preprocessing → core_models → reporting
```

### Pattern 2: Complex Analysis
```
data_loading → preprocessing → core_models → individual_models → integrated_analysis → reporting
```

### Pattern 3: With Dependencies
```
data_loading → preprocessing → core_models → individual_models (parallel) → 
dependent_models → integrated_analysis → reporting
```

## Tips

1. **Keep groups focused** - Each group should have a single clear purpose
2. **Mark parallelization correctly** - Only mark groups parallel if steps are truly independent
3. **Use dependencies wisely** - Dependencies within parallel groups can reduce parallelization benefits
4. **Name phases clearly** - Phase names should describe what's happening
5. **Group similar steps** - Steps with similar runtime characteristics should be in the same group

