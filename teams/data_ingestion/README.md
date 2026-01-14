
Injest the following tiger data into our system
* Historical Census Data
* Geospatial Data
* Surveillance Feeds
* Threat Logs

## Historical Census Data - India Tigers

### Directory Structure
```
census/
├── india_tiger_census_national.csv      # National census data (2006-2022)
├── india_tiger_census_states_2022.csv   # State-level breakdown for 2022
├── india_tiger_census.json              # Complete dataset with metadata
├── ingest_tiger_data.py                 # Python ingestion script
├── DATA_SOURCES.md                      # Complete source documentation
└── SOURCES_QUICK_REFERENCE.md           # Quick reference guide
```

### Data Source
**National Tiger Conservation Authority (NTCA)** - Government of India
- Website: https://ntca.gov.in
- Census Frequency: Every 4 years
- Methodology: Camera trap surveys + statistical estimation models
- Latest Census: 2022 (3,682 tigers)
- Next Expected: 2026

📚 **See [census/DATA_SOURCES.md](census/DATA_SOURCES.md) for complete source documentation, verification process, and access instructions.**

### Quick Stats
- **2006**: 1,411 tigers (baseline)
- **2022**: 3,682 tigers (latest)
- **Growth**: +161% increase over 16 years
- **Coverage**: 18 states, 53 tiger reserves

### Usage
Run the ingestion script to load and analyze the data:

```bash
cd census
python ingest_tiger_data.py
```

## Geospatial Data (GIS) - India Tigers

### Directory Structure
```
geospatial/
├── raw/                                 # Raw data from various sources
│   ├── wdpa/                           # Protected Planet downloads
│   ├── bhuvan/                         # Bhuvan geoportal (ISRO)
│   ├── ntca/                           # NTCA official data
│   ├── wii/                            # Wildlife Institute of India
│   ├── states/                         # State forest departments
│   ├── osm/                            # OpenStreetMap
│   └── academic/                       # Research publications
├── processed/                           # Cleaned & standardized data
├── GIS_DATA_SOURCES.md                 # Complete source documentation
├── QUICK_REFERENCE.md                  # Quick start guide
├── DATA_REQUEST_TEMPLATE.md            # Email templates for requests
└── README.md                           # Overview and instructions
```

### What We Need
**58 Tiger Reserves with Core and Buffer Zones**
- **Core Areas**: Strictly protected critical tiger habitat (~35,000-40,000 sq km)
- **Buffer Zones**: Peripheral areas with mixed land use (~35,000-40,000 sq km)
- **Format**: Shapefiles (.shp), GeoJSON, or GeoPackage
- **CRS**: WGS84 (EPSG:4326) or UTM zones

### Data Availability Status
⚠️ **Important**: Comprehensive GIS data is **NOT immediately available** as a single download.

**Acquisition Strategy:**
1. ✅ **Immediate** (TODAY): Download from Protected Planet, Bhuvan
2. 📧 **2-4 weeks**: Official requests to NTCA, WII
3. 📋 **4-8 weeks**: State forest departments, RTI requests
4. 🗺️ **Ongoing**: Fill gaps from academic sources, digitization

### Primary Data Sources

| Source | Type | Access | Core/Buffer | Timeline |
|--------|------|--------|-------------|----------|
| **NTCA** | Official | Request | ✅ Yes | 2-4 weeks |
| **WII** | Research | Request | ✅ Yes | 2-4 weeks |
| **Protected Planet** | Global DB | Free Download | ⚠️ Maybe | Immediate |
| **Bhuvan (ISRO)** | Satellite/GIS | Free Download | ⚠️ Partial | Immediate |
| **State Forest Depts** | Official | Request/RTI | ✅ Yes | 4-8 weeks |

📚 **See [geospatial/GIS_DATA_SOURCES.md](geospatial/GIS_DATA_SOURCES.md) for:**
- 10+ detailed data sources
- Step-by-step access instructions
- Legal and ethical considerations
- Data processing workflows

### Quick Start
```bash
# 1. Get baseline data immediately
Visit: https://www.protectedplanet.net (download India tiger reserves)
Visit: https://bhuvan.nrsc.gov.in (register and explore)

# 2. Submit official data requests
cd geospatial
# Use templates in DATA_REQUEST_TEMPLATE.md
# Email NTCA and WII (check their websites for current contacts)

# 3. Read complete documentation
# See GIS_DATA_SOURCES.md for comprehensive guide
```

### Key Contacts
- **NTCA**: https://ntca.gov.in (Bikaner House, New Delhi)
- **WII GIS Division**: https://wii.gov.in (Dehradun, Uttarakhand)
- **Bhuvan Portal**: https://bhuvan.nrsc.gov.in (ISRO)

