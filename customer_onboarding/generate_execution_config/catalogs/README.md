# Function Catalogs

Organized catalog of all available functions for execution configurations.

## Structure

The catalogs are separated by functional area:

### 1. **Data Loaders** (`data_loaders_catalog.json`)
Functions for loading data from external sources.

**Functions:** 10
- `load_satellite_data` - Satellite vegetation index data
- `load_climate_data` - Weather station climate data
- `load_drought_data` - US Drought Monitor
- `load_air_quality_data` - EPA air quality
- `load_wildfire_perimeters` - Historical wildfire data
- `load_wildlife_habitat_data` - Wildlife habitat database
- `load_soil_erosion_data` - Soil erosion risk maps
- `load_water_quality_data` - USGS water quality
- `load_elevation_data` - Digital elevation models
- `load_land_cover_data` - National land cover database

### 2. **Data Processors** (`data_processors_catalog.json`)
Functions for preprocessing and transforming data.

**Functions:** 6
- `preprocess_spatial_data` - Align spatial datasets to common grid
- `preprocess_temporal_data` - Resample temporal data
- `merge_datasets` - Merge multiple datasets
- `extract_region` - Extract data for specific region
- `calculate_derivatives` - Calculate spatial derivatives (slope, aspect)
- `normalize_data` - Normalize/standardize data values

### 3. **Analysis Models** (`models_catalog.json`)
Functions for executing analysis models.

**Functions:** 9
- `run_historical_pattern_analysis` - Historical fire pattern analysis
- `run_wildfire_risk_index` - Wildfire risk assessment
- `run_fuel_load_assessment` - Vegetation fuel load model
- `run_drought_impact_model` - Drought severity impact
- `run_air_quality_fire_impact` - Fire-related air quality
- `run_habitat_vulnerability_model` - Wildlife habitat vulnerability
- `run_post_fire_erosion_model` - Post-fire erosion risk
- `run_watershed_fire_impact_model` - Watershed fire impact
- `run_integrated_fire_risk_model` - Integrated multi-factor risk

### 4. **Reporting & Export** (`reporting_catalog.json`)
Functions for generating reports and exporting results.

**Functions:** 5
- `generate_report` - Generate analysis reports (executive, technical, full)
- `export_gis_package` - Export GIS data packages
- `create_web_map` - Create interactive web maps
- `generate_summary_statistics` - Generate summary statistics
- `create_visualization` - Create static visualizations

## Catalog Index

The `catalog_index.json` file provides metadata about all catalogs:
- List of all catalog files
- Module mappings
- Function counts
- Total available functions: **30**

## Function Definition Format

Each function is defined with:

```json
{
  "name": "function_name",
  "description": "What the function does",
  "parameters": {
    "param_name": {
      "type": "string|integer|float|list|dict|boolean",
      "required": true|false,
      "description": "Parameter description",
      "valid_values": ["optional", "list", "of", "valid", "values"],
      "default": "optional default value"
    }
  },
  "returns": "What the function returns"
}
```

## Adding New Functions

To add a new function:

1. **Determine the correct catalog** based on function type
2. **Add function definition** to the appropriate catalog file
3. **Update `catalog_index.json`** to increment function count
4. **Test with validator**:
   ```bash
   python ../config_validator.py your_config.json
   ```

## Benefits of Separation

- ✅ **Better organization** - Functions grouped by purpose
- ✅ **Easier maintenance** - Update one catalog at a time
- ✅ **Clear responsibilities** - Each catalog has a specific role
- ✅ **Scalability** - Easy to add new catalog modules
- ✅ **Discoverability** - Easier to find relevant functions

## Module-to-Catalog Mapping

| Module | Catalog File | Purpose |
|--------|-------------|---------|
| `data_loaders` | `data_loaders_catalog.json` | Load external data |
| `data_processors` | `data_processors_catalog.json` | Process/transform data |
| `models` | `models_catalog.json` | Execute analyses |
| `reporting` | `reporting_catalog.json` | Generate outputs |

## Validator Integration

The `config_validator.py` automatically:
1. Reads `catalog_index.json`
2. Loads all catalog files listed in the index
3. Merges function definitions into a single lookup
4. Validates configs against all available functions

**No code changes needed** when adding functions to existing catalogs!

