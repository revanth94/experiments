# Geospatial Data - India Tiger Reserves

## Overview

This directory contains information and resources for obtaining **GIS data (shapefiles)** for India's **58 tiger reserves**, including Core Areas and Buffer Zones.

---

## 🚨 Important Note

**Comprehensive GIS data for all tiger reserves is NOT immediately available as a single download.**

You will need to:
1. Start with publicly available sources (Protected Planet, Bhuvan)
2. Submit formal requests to official authorities (NTCA, WII, State Forest Departments)
3. Wait 2-8 weeks for official responses
4. Potentially use multiple sources to compile complete dataset

---

## 📁 Directory Contents

### Documentation Files

| File | Purpose |
|------|---------|
| **GIS_DATA_SOURCES.md** | Comprehensive guide to all data sources (⭐ **START HERE**) |
| **QUICK_REFERENCE.md** | Quick start guide with TL;DR summaries |
| **DATA_REQUEST_TEMPLATE.md** | Email templates for requesting data from official sources |
| **README.md** | This file - overview and getting started |

### Data Files (To Be Added)

```
geospatial/
├── raw/                          # Raw data from various sources
│   ├── wdpa/                     # Protected Planet downloads
│   ├── bhuvan/                   # Bhuvan geoportal data
│   ├── ntca/                     # NTCA official data (when received)
│   ├── wii/                      # WII research data (when received)
│   └── states/                   # State forest department data
│
├── processed/                    # Cleaned and standardized data
│   ├── tiger_reserves_all.shp    # Combined shapefile (all reserves)
│   ├── tiger_reserves_core.shp   # Core areas only
│   ├── tiger_reserves_buffer.shp # Buffer zones only
│   └── metadata.json             # Data documentation
│
└── docs/                         # This folder (documentation)
    ├── GIS_DATA_SOURCES.md
    ├── QUICK_REFERENCE.md
    ├── DATA_REQUEST_TEMPLATE.md
    └── README.md
```

---

## 🚀 Quick Start Guide

### Step 1: Understand What You Need (5 minutes)

Read **QUICK_REFERENCE.md** for a fast overview of:
- Where to get data
- What each source provides
- How long it takes

### Step 2: Get Baseline Data NOW (15 minutes)

**Option A: Protected Planet (Easiest)**
```bash
1. Visit: https://www.protectedplanet.net
2. Search: "India Tiger Reserve" or specific reserve name
3. Register: Free account
4. Download: Shapefile format
5. Result: Basic boundaries for most/all reserves
```

**Option B: Bhuvan Geoportal (Best Indian Source)**
```bash
1. Visit: https://bhuvan.nrsc.gov.in
2. Register: Free account
3. Navigate: Thematic Services > Protected Areas
4. View/Download: Available layers
5. Result: Satellite imagery + protected area boundaries
```

### Step 3: Request Official Data (30 minutes)

**Priority: National Tiger Conservation Authority (NTCA)**
```bash
1. Open: DATA_REQUEST_TEMPLATE.md
2. Copy: Template 1 (NTCA)
3. Customize: Add your details and purpose
4. Send: Email to NTCA (check ntca.gov.in for contact)
5. Wait: 2-4 weeks for response
```

**Secondary: Wildlife Institute of India (WII)**
```bash
1. Use: Template 2 from DATA_REQUEST_TEMPLATE.md
2. Send: To WII GIS Division
3. Wait: 2-4 weeks
```

### Step 4: Read Complete Documentation (1 hour)

**Read: GIS_DATA_SOURCES.md** for detailed information on:
- 10+ data sources
- How to access each one
- Expected data formats
- Legal considerations
- Data processing workflow

---

## 📊 What You're Looking For

### Data Specifications

**Geographic Coverage:**
- All 58 designated tiger reserves in India
- Distributed across 20 states
- Total area: ~75,000 sq km

**Required Distinctions:**
1. **Core Areas** (Critical Tiger Habitat)
   - Strictly protected zones
   - National Parks or Wildlife Sanctuaries
   - Minimal human activity
   - ~35,000-40,000 sq km total

2. **Buffer Zones** (Peripheral Areas)
   - Mixed land use zones
   - Ecotourism, limited development allowed
   - Forest villages may exist
   - ~35,000-40,000 sq km total

**File Format:**
- Shapefile (.shp + associated files)
- GeoJSON (.geojson)
- GeoPackage (.gpkg)
- KML/KMZ for visualization

**Coordinate System:**
- WGS84 (EPSG:4326) - Geographic coordinates
- Or WGS84 UTM zones (EPSG:32643-32646) - Projected coordinates

---

## 🎯 Recommended Data Acquisition Strategy

### Phase 1: Immediate (TODAY)
✅ Download from Protected Planet  
✅ Register on Bhuvan and explore  
✅ Check data.gov.in for datasets  

**Expected Result:** Basic boundaries for 40-50 reserves

---

### Phase 2: Short-term (WEEK 1)
📧 Send data requests to NTCA and WII  
📚 Search academic papers for GIS data  
🔍 Review OpenStreetMap coverage  

**Expected Result:** Formal requests submitted, wait for responses

---

### Phase 3: Medium-term (WEEKS 2-4)
📨 Follow up on NTCA/WII requests  
📝 Contact specific state forest departments  
🤝 Reach out to conservation NGOs  

**Expected Result:** Start receiving official data

---

### Phase 4: Long-term (WEEKS 4-8)
📋 File RTI requests if needed  
🗺️ Digitize missing reserves from maps  
✅ Compile and standardize all data sources  

**Expected Result:** Complete or near-complete coverage

---

## 📋 Data Source Priority Matrix

| Source | Availability | Quality | Core/Buffer | Effort | Priority |
|--------|-------------|---------|-------------|--------|----------|
| **NTCA** | Request | ⭐⭐⭐⭐⭐ | ✅ Yes | Medium | 🔥 High |
| **WII** | Request | ⭐⭐⭐⭐⭐ | ✅ Yes | Medium | 🔥 High |
| **Protected Planet** | Immediate | ⭐⭐⭐ | ❌ Maybe | Low | 🔥 High |
| **Bhuvan** | Immediate | ⭐⭐⭐⭐ | ⚠️ Partial | Low | 🔥 High |
| **State Depts** | Request | ⭐⭐⭐⭐⭐ | ✅ Yes | High | Medium |
| **OpenStreetMap** | Immediate | ⭐⭐ | ❌ No | Low | Low |
| **Academic** | Variable | ⭐⭐⭐⭐ | ⚠️ Varies | Medium | Medium |

---

## ⚠️ Important Considerations

### Data Sensitivity
- Detailed location data can be sensitive for anti-poaching efforts
- Some authorities may restrict access to very precise boundaries
- Always state legitimate research/conservation purpose

### Legal Access
- Most data can be obtained under Right to Information Act (Indian citizens)
- Non-Indian researchers should work through institutions
- Commercial use may require specific permissions

### Data Quality
- Different sources may have slight boundary variations
- Official sources (NTCA, State Depts) are most authoritative
- Cross-verify boundaries when possible

### Attribution
- Always credit data source (NTCA, WII, specific state department, etc.)
- Follow any data sharing agreements
- Don't redistribute without permission

---

## 🛠️ Tools You'll Need

### View and Analyze GIS Data

**Free Options:**
- **QGIS** - https://qgis.org (Full-featured desktop GIS)
- **Google Earth** - View KML/KMZ files
- **GeoPandas** (Python) - Programmatic analysis

**Commercial:**
- **ArcGIS** - Industry standard (license required)

### Basic Python Script to Load Shapefile

```python
import geopandas as gpd
import matplotlib.pyplot as plt

# Load shapefile
reserves = gpd.read_file('tiger_reserves.shp')

# Basic info
print(f"Total reserves: {len(reserves)}")
print(f"Columns: {reserves.columns.tolist()}")

# Filter core vs buffer
core = reserves[reserves['Zone_Type'] == 'Core']
buffer = reserves[reserves['Zone_Type'] == 'Buffer']

print(f"Core areas: {len(core)}")
print(f"Buffer zones: {len(buffer)}")

# Plot
fig, ax = plt.subplots(figsize=(12, 10))
reserves.plot(column='Zone_Type', ax=ax, legend=True, 
              categorical=True, cmap='Set2')
plt.title('India Tiger Reserves - Core vs Buffer Zones')
plt.show()
```

---

## 📞 Key Contacts

### National Organizations

**National Tiger Conservation Authority (NTCA)**
- Website: https://ntca.gov.in
- Address: Bikaner House, Shahjahan Road, New Delhi - 110011

**Wildlife Institute of India (WII)**
- Website: https://wii.gov.in
- Address: Chandrabani, Dehradun - 248001, Uttarakhand
- GIS Division: Contact through website

**Forest Survey of India (FSI)**
- Website: https://fsi.nic.in
- For forest cover and vegetation data

### International Resources

**Protected Planet (WDPA)**
- Website: https://www.protectedplanet.net
- Managed by: UNEP-WCMC

**Indian Space Research Organisation (ISRO)**
- Bhuvan Portal: https://bhuvan.nrsc.gov.in
- For satellite imagery and spatial data

---

## 📚 Additional Resources

### Reference Documents
1. Tiger Reserve Management Plans (NTCA website)
2. India State of Forest Report (FSI, biennial)
3. Project Tiger Status Reports (NTCA, annual)
4. Wildlife Protection Act, 1972 (legal framework)

### Academic Papers
Search Google Scholar for:
- "Tiger reserve GIS India"
- "Tiger habitat mapping India"
- "Protected area spatial analysis India"

### Online Communities
- QGIS Users India (for GIS help)
- Wildlife conservation forums
- Geographic Information Systems Stack Exchange

---

## ✅ Success Metrics

You'll know you have good data when:
- ✅ You have shapefiles for 50+ of the 58 tiger reserves
- ✅ Core and Buffer zones are clearly distinguished
- ✅ Attribute data includes reserve names and areas
- ✅ Boundaries are properly georeferenced (CRS defined)
- ✅ Topology is clean (no gaps, overlaps, or errors)
- ✅ Data source is documented and reputable

---

## 🔄 Data Updates

Tiger reserve boundaries can change due to:
- New reserve notifications
- Expansion of existing reserves
- Reclassification of zones
- Legal amendments

**Check for updates:**
- NTCA website for new notifications
- Annual Project Tiger reports
- State forest department announcements

**Current Status (2026):**
- Total Reserves: 58
- Last Major Update: Ongoing (check NTCA)
- Next Census: 2026 (report expected 2027)

---

## 📖 Documentation Status

| Document | Status | Last Updated |
|----------|--------|--------------|
| GIS_DATA_SOURCES.md | ✅ Complete | Jan 14, 2026 |
| QUICK_REFERENCE.md | ✅ Complete | Jan 14, 2026 |
| DATA_REQUEST_TEMPLATE.md | ✅ Complete | Jan 14, 2026 |
| README.md | ✅ Complete | Jan 14, 2026 |

**Data Acquisition Status:** 🟡 In Progress (pending official responses)

---

## 🤝 Contributing

If you successfully obtain GIS data:
1. Document your source
2. Note any usage restrictions
3. Save in `raw/[source_name]/` folder
4. Update this README with acquisition details

---

**Questions?** See GIS_DATA_SOURCES.md for comprehensive documentation  
**Quick Help?** See QUICK_REFERENCE.md for fast answers  
**Ready to Request?** Use templates in DATA_REQUEST_TEMPLATE.md

