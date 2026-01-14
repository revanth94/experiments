# Raw GIS Data Directory

This directory stores raw, unprocessed GIS data from various sources.

## Directory Structure

```
raw/
├── wdpa/        # Protected Planet (World Database on Protected Areas)
├── bhuvan/      # Bhuvan Geoportal (ISRO)
├── ntca/        # National Tiger Conservation Authority
├── wii/         # Wildlife Institute of India
├── states/      # State Forest Departments
├── osm/         # OpenStreetMap
└── academic/    # Academic research papers and institutions
```

## Usage Guidelines

### When Downloading Data

1. **Create source-specific subfolders** if needed
   ```
   raw/wdpa/download_2026_01_14/
   raw/ntca/received_2026_02_01/
   ```

2. **Keep original filenames** or document name changes

3. **Save metadata** - Create a text file with:
   - Download date
   - Source URL
   - Contact person (if applicable)
   - Any usage restrictions
   - Data version/vintage

4. **Example metadata file** (`raw/wdpa/metadata.txt`):
   ```
   Source: Protected Planet (WDPA)
   URL: https://www.protectedplanet.net
   Download Date: 2026-01-14
   Version: January 2026 release
   Coverage: India protected areas including tiger reserves
   Format: Shapefile
   CRS: WGS84 (EPSG:4326)
   License: CC BY 4.0
   Notes: Downloaded all protected areas in India, need to filter for tiger reserves
   ```

## Source-Specific Notes

### wdpa/ (Protected Planet)
- **What**: Global protected area database
- **Access**: Free download, registration required
- **Format**: Shapefile, GeoPackage
- **Update Frequency**: Monthly
- **Keep**: Original download + filtered tiger reserves

### bhuvan/ (ISRO Bhuvan)
- **What**: Indian satellite imagery and GIS layers
- **Access**: Free, registration required
- **Format**: Various (Shapefile, GeoTIFF, KML)
- **Keep**: Downloaded layers + screenshots of what's available

### ntca/ (NTCA)
- **What**: Official tiger reserve boundaries
- **Access**: Formal request required
- **Format**: Likely Shapefile or PDF maps
- **Keep**: Everything received + correspondence

### wii/ (WII)
- **What**: Research-grade GIS data
- **Access**: Formal request / collaboration
- **Format**: Shapefile, GeoTIFF
- **Keep**: All data + research papers

### states/ (State Forest Departments)
- **What**: State-specific tiger reserve data
- **Access**: Varies by state (request or RTI)
- **Format**: Shapefile, PDF maps, CAD files
- **Organization**: Create subfolder per state
  ```
  states/
  ├── madhya_pradesh/
  ├── karnataka/
  ├── uttarakhand/
  └── ...
  ```

### osm/ (OpenStreetMap)
- **What**: Crowd-sourced map data
- **Access**: Free, immediate
- **Format**: Shapefile, GeoJSON, OSM XML
- **Keep**: Downloaded extracts + query used

### academic/ (Research Papers)
- **What**: GIS data from published research
- **Access**: Varies (contact authors)
- **Format**: Shapefile, supplementary files
- **Organization**: Create folder per paper/author
  ```
  academic/
  ├── sharma_2025_tiger_corridors/
  ├── karanth_2024_habitat_analysis/
  └── ...
  ```

## File Naming Convention

Use descriptive names with date stamps:

```
[source]_[description]_[date].[ext]

Examples:
- wdpa_india_protected_areas_20260114.shp
- ntca_all_tiger_reserves_core_buffer_20260201.gpkg
- bhuvan_corbett_reserve_satellite_20260115.tif
- karnataka_forest_nagarhole_boundaries_20260120.shp
```

## Data Processing Workflow

1. **Download** → Save to appropriate `raw/[source]/` folder
2. **Document** → Create/update metadata file
3. **Inspect** → Open in QGIS, check attributes, CRS, quality
4. **Process** → Clean, standardize, merge (results go to `processed/`)
5. **Archive** → Keep raw data unchanged for reference

## Do NOT Delete Raw Data

- Always preserve original downloads
- Raw data = backup if processing goes wrong
- Document any issues found in metadata files

## Questions?

See parent folder README.md for complete documentation.

