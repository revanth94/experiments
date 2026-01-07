# Function Catalog Structure

## Overview

The function catalogs have been **separated into organized modules** for better maintainability and clarity.

## Directory Structure

```
generate_execution_config/
├── catalogs/
│   ├── catalog_index.json           # Index of all catalogs
│   ├── data_loaders_catalog.json    # Data loading functions (10)
│   ├── data_processors_catalog.json # Data processing functions (6)
│   ├── models_catalog.json          # Analysis model functions (9)
│   ├── reporting_catalog.json       # Reporting/export functions (5)
│   └── README.md                    # Detailed catalog documentation
├── config_validator.py              # Updated to load from catalogs/
├── execution_configs/               # Generated configs
└── function_catalog.json            # Legacy (kept for compatibility)
```

## Catalog Breakdown

### 📥 Data Loaders (10 functions)
**Module:** `data_loaders`
**Purpose:** Load data from external sources

| Function | Description |
|----------|-------------|
| `load_satellite_data` | Satellite vegetation indices (NDVI, biomass) |
| `load_climate_data` | Weather station data (temp, humidity, wind) |
| `load_drought_data` | US Drought Monitor |
| `load_air_quality_data` | EPA air quality measurements |
| `load_wildfire_perimeters` | Historical wildfire boundaries |
| `load_wildlife_habitat_data` | Wildlife habitat database |
| `load_soil_erosion_data` | Soil erosion risk maps |
| `load_water_quality_data` | USGS water quality |
| `load_elevation_data` | Digital elevation models |
| `load_land_cover_data` | National land cover database |

### ⚙️ Data Processors (6 functions)
**Module:** `data_processors`
**Purpose:** Preprocess and transform data

| Function | Description |
|----------|-------------|
| `preprocess_spatial_data` | Align spatial datasets to common grid |
| `preprocess_temporal_data` | Resample temporal data |
| `merge_datasets` | Merge multiple datasets |
| `extract_region` | Extract data for specific region |
| `calculate_derivatives` | Calculate slope, aspect, etc. |
| `normalize_data` | Normalize/standardize values |

### 🔬 Analysis Models (9 functions)
**Module:** `models`
**Purpose:** Execute analysis models

| Function | Description |
|----------|-------------|
| `run_historical_pattern_analysis` | Historical fire patterns |
| `run_wildfire_risk_index` | Core wildfire risk assessment |
| `run_fuel_load_assessment` | Vegetation fuel load |
| `run_drought_impact_model` | Drought severity impact |
| `run_air_quality_fire_impact` | Fire-related air quality |
| `run_habitat_vulnerability_model` | Wildlife habitat vulnerability |
| `run_post_fire_erosion_model` | Post-fire erosion risk |
| `run_watershed_fire_impact_model` | Watershed fire impact |
| `run_integrated_fire_risk_model` | Integrated multi-factor risk |

### 📊 Reporting & Export (5 functions)
**Module:** `reporting`
**Purpose:** Generate reports and export results

| Function | Description |
|----------|-------------|
| `generate_report` | Generate analysis reports (PDF) |
| `export_gis_package` | Export GIS data packages |
| `create_web_map` | Create interactive web maps |
| `generate_summary_statistics` | Generate summary statistics |
| `create_visualization` | Create static visualizations |

## Benefits of Separation

### ✅ Organization
- Functions grouped by purpose
- Clear module boundaries
- Easy to navigate

### ✅ Maintainability
- Update one catalog at a time
- No need to search through large files
- Clear ownership of each module

### ✅ Scalability
- Easy to add new catalogs
- Can extend individual modules independently
- No merge conflicts when multiple people add functions

### ✅ Discoverability
- Easier to find relevant functions
- Clear documentation per module
- Better IDE support

### ✅ Validation
- Validator automatically loads all catalogs
- No code changes needed when adding functions
- Consistent validation across all modules

## How It Works

### 1. Catalog Index
`catalog_index.json` lists all available catalogs:

```json
{
  "catalogs": [
    {
      "name": "Data Loaders",
      "file": "data_loaders_catalog.json",
      "module": "data_loaders",
      "function_count": 10
    },
    ...
  ],
  "total_functions": 30
}
```

### 2. Validator Loading
The `ConfigValidator` class:
1. Reads `catalog_index.json`
2. Loads each catalog file listed
3. Merges all functions into a single lookup dictionary
4. Validates configs against all available functions

### 3. Backward Compatibility
- Legacy `function_catalog.json` kept for compatibility
- Validator falls back to it if `catalogs/` doesn't exist
- Existing configs continue to work

## Usage

### Validate a Config
```bash
python config_validator.py execution_configs/config_Biomet_20260107.json
```

### Add a New Function
1. Choose appropriate catalog (loaders/processors/models/reporting)
2. Add function definition to that catalog
3. Update function count in `catalog_index.json`
4. Test with validator

### View All Functions
```python
from config_validator import ConfigValidator

validator = ConfigValidator('catalogs')
print(f"Total functions: {len(validator.functions)}")

for name in sorted(validator.functions.keys()):
    func = validator.functions[name]
    print(f"  {func['module']}.{name}")
```

## Statistics

- **Total Functions:** 30
- **Total Catalogs:** 4
- **Lines of Code:** ~1,500 (across all catalogs)
- **Modules:** 4 (data_loaders, data_processors, models, reporting)

## Migration Notes

**No breaking changes!**
- Existing configs work without modification
- Validator automatically uses new catalog structure
- Legacy `function_catalog.json` maintained for compatibility
- All 30 functions validated successfully ✓

