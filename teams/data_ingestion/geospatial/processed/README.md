# Processed GIS Data Directory

This directory contains cleaned, standardized, and merged GIS data ready for analysis.

## Expected Files

```
processed/
├── india_tiger_reserves_all.shp          # All reserves (core + buffer combined)
├── india_tiger_reserves_core.shp         # Core areas only
├── india_tiger_reserves_buffer.shp       # Buffer zones only
├── india_tiger_reserves_metadata.json    # Complete metadata and documentation
├── india_tiger_reserves_catalog.csv      # List of all reserves with attributes
└── processing_log.md                     # Record of processing steps
```

## Data Standards

### Coordinate Reference System
- **Primary CRS**: WGS84 (EPSG:4326)
- **Alternative**: WGS84 / UTM Zone 43N-46N (EPSG:32643-32646)
- Always include .prj file with shapefiles

### Required Attribute Fields

**For combined file (all reserves):**
```
- tr_id: Unique identifier (e.g., "TR001", "TR002")
- name: Reserve name (e.g., "Corbett Tiger Reserve")
- state: State name (e.g., "Uttarakhand")
- zone_type: "Core" or "Buffer"
- area_sqkm: Area in square kilometers
- notif_year: Year of notification
- legal_status: "National Park", "Wildlife Sanctuary", "Reserved Forest"
- management: Managing authority
- latitude: Centroid latitude
- longitude: Centroid longitude
- data_source: Where boundary came from (e.g., "NTCA", "WDPA", "WII")
- data_date: Date data was obtained
- verified: Boolean (has boundary been officially verified?)
```

### File Naming Convention

```
india_tiger_reserves_[subset]_[version]_[date].[ext]

Examples:
- india_tiger_reserves_all_v1_20260215.shp
- india_tiger_reserves_core_v1_20260215.shp
- india_tiger_reserves_buffer_v1_20260215.shp
- india_tiger_reserves_metadata_v1_20260215.json
```

## Processing Steps

### Step 1: Collect Raw Data
- Gather shapefiles from all sources (raw/ folder)
- Document what you have and what's missing

### Step 2: Standardize CRS
```python
import geopandas as gpd

# Load shapefile
gdf = gpd.read_file('raw/source/data.shp')

# Check CRS
print(gdf.crs)

# Reproject to WGS84 if needed
if gdf.crs != 'EPSG:4326':
    gdf = gdf.to_crs('EPSG:4326')
```

### Step 3: Standardize Attributes
```python
# Rename columns to standard names
gdf = gdf.rename(columns={
    'NAME': 'name',
    'STATE': 'state',
    'AREA': 'area_sqkm',
    # ... etc
})

# Add missing required fields
gdf['data_source'] = 'NTCA'
gdf['data_date'] = '2026-02-01'
```

### Step 4: Clean Geometry
```python
# Fix invalid geometries
gdf['geometry'] = gdf['geometry'].buffer(0)

# Check for gaps, overlaps, slivers
# Remove duplicates
# Ensure polygons are closed
```

### Step 5: Merge Sources
```python
# Combine data from multiple sources
ntca_data = gpd.read_file('raw/ntca/data.shp')
wdpa_data = gpd.read_file('raw/wdpa/data.shp')

# Prioritize official sources (NTCA > WII > State > WDPA > OSM)
# Use spatial joins to match reserves
# Fill gaps with secondary sources
```

### Step 6: Validate
```python
# Check completeness
print(f"Total reserves: {len(gdf)}")
print(f"Core areas: {len(gdf[gdf['zone_type']=='Core'])}")
print(f"Buffer zones: {len(gdf[gdf['zone_type']=='Buffer'])}")

# Expected: 58 core + 58 buffer = 116 features
# (Some reserves may have multiple core/buffer polygons)

# Check for missing data
print(gdf.isnull().sum())

# Validate geometry
print(gdf.is_valid.sum(), "valid geometries")
```

### Step 7: Export
```python
# Save as shapefile
gdf.to_file('processed/india_tiger_reserves_all.shp')

# Save as GeoJSON (for web use)
gdf.to_file('processed/india_tiger_reserves_all.geojson', driver='GeoJSON')

# Save as GeoPackage (modern format)
gdf.to_file('processed/india_tiger_reserves_all.gpkg', driver='GPKG')
```

### Step 8: Create Metadata
Document:
- Data sources used
- Processing date
- Known gaps or issues
- Accuracy assessment
- Usage notes

## Quality Assurance Checklist

Before finalizing processed data:

- [ ] All 58 tiger reserves included (or documented if missing)
- [ ] Core and Buffer zones distinguished
- [ ] CRS is WGS84 (EPSG:4326) or documented
- [ ] All required attribute fields present
- [ ] No invalid geometries
- [ ] No topology errors (gaps, overlaps)
- [ ] Data sources documented
- [ ] Processed file loads in QGIS without errors
- [ ] Metadata file created
- [ ] Processing log updated

## Version Control

Track changes to processed data:

**v1.0** (Initial)
- Date: YYYY-MM-DD
- Sources: [List sources used]
- Coverage: X of 58 reserves
- Notes: [Any issues or gaps]

**v1.1** (Update)
- Date: YYYY-MM-DD
- Changes: [What was added/fixed]
- Sources: [New sources added]
- Coverage: Updated count

## Sample Python Processing Script

See `process_tiger_reserves.py` (to be created) for complete processing workflow.

Quick example:
```python
import geopandas as gpd
import pandas as pd
from pathlib import Path

def process_tiger_reserves():
    """Process raw GIS data into standardized format"""
    
    # Load from multiple sources
    sources = []
    
    # WDPA data (baseline)
    if Path('raw/wdpa/india_pas.shp').exists():
        wdpa = gpd.read_file('raw/wdpa/india_pas.shp')
        wdpa = wdpa[wdpa['DESIG_ENG'].str.contains('Tiger', na=False)]
        wdpa['data_source'] = 'WDPA'
        sources.append(wdpa)
    
    # NTCA data (highest priority - overwrites others)
    if Path('raw/ntca/tiger_reserves.shp').exists():
        ntca = gpd.read_file('raw/ntca/tiger_reserves.shp')
        ntca['data_source'] = 'NTCA'
        sources.append(ntca)
    
    # Merge all sources
    if sources:
        combined = gpd.GeoDataFrame(pd.concat(sources, ignore_index=True))
        
        # Standardize CRS
        combined = combined.to_crs('EPSG:4326')
        
        # Clean and save
        combined.to_file('processed/india_tiger_reserves_all.shp')
        print(f"Processed {len(combined)} features")
        return combined
    else:
        print("No data files found in raw/ directory")
        return None

# Run processing
if __name__ == '__main__':
    process_tiger_reserves()
```

## Notes

- Keep raw data unchanged - all processing creates new files
- Document every processing step in processing_log.md
- Update version numbers when making changes
- Test processed data in QGIS before considering it final

