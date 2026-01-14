# Quick Reference - Tiger Reserve GIS Data Sources

## TL;DR - Where to Get Data

| Source | Access | Data Quality | Timeline | Cost |
|--------|--------|--------------|----------|------|
| **Protected Planet** | ✅ Immediate download | ⭐⭐⭐ Good | Now | Free |
| **Bhuvan (ISRO)** | ✅ Register & download | ⭐⭐⭐⭐ Very Good | Now | Free |
| **NTCA** | 📧 Formal request | ⭐⭐⭐⭐⭐ Official | 2-4 weeks | Free |
| **WII** | 📧 Formal request | ⭐⭐⭐⭐⭐ Research-grade | 2-4 weeks | Free |
| **State Forest Dept** | 📧 Request/RTI | ⭐⭐⭐⭐⭐ Official | 4-8 weeks | Free/Minimal |
| **OpenStreetMap** | ✅ Immediate download | ⭐⭐ Variable | Now | Free |
| **Academic Papers** | 📚 Search & request | ⭐⭐⭐⭐ High Quality | 1-2 weeks | Free |

---

## Quick Start (What to Do Right Now)

### Step 1: Get Baseline Data (10 minutes)
```bash
# Download from Protected Planet
1. Visit: https://www.protectedplanet.net
2. Search: "Tiger Reserve India"
3. Download: Shapefile format
4. Get: Basic boundaries for most reserves
```

### Step 2: Check Indian Portals (30 minutes)
```bash
# Bhuvan Geoportal
1. Visit: https://bhuvan.nrsc.gov.in
2. Register: Free account
3. Explore: Protected areas layer
4. Download: Available spatial data

# India Open Data
1. Visit: https://data.gov.in
2. Search: "protected areas" OR "tiger reserves"
3. Download: Any available datasets
```

### Step 3: Submit Official Requests (1 hour)
```bash
# Email NTCA
To: [Check ntca.gov.in for contact]
Subject: Request for Tiger Reserve GIS Data
Content: [Use template in this folder]

# Email WII GIS Division
To: [Check wii.gov.in for contact]
Subject: Request for Tiger Reserve Shapefiles
Content: [Use template in this folder]
```

---

## What You'll Get from Each Source

### Protected Planet (WDPA)
✅ **Pros:**
- Free, immediate download
- All tiger reserves included
- Global standard format
- Well-documented metadata

❌ **Cons:**
- May lack core/buffer distinction
- Boundaries may be generalized
- Updated periodically (not real-time)

**Format**: Shapefile, GeoPackage  
**CRS**: WGS84 (EPSG:4326)

---

### Bhuvan Geoportal (ISRO)
✅ **Pros:**
- High-resolution satellite imagery
- Official Indian government source
- Protected area overlays
- Free access

❌ **Cons:**
- May not have detailed core/buffer zones
- User interface can be complex
- Requires registration

**Format**: Various (Shapefile, KML)  
**CRS**: WGS84, UTM zones

---

### NTCA (National Tiger Conservation Authority)
✅ **Pros:**
- **MOST AUTHORITATIVE SOURCE**
- Official core/buffer boundaries
- Complete coverage (all 58 reserves)
- Legal boundary descriptions

❌ **Cons:**
- Requires formal request
- 2-4 week wait time
- May need institutional affiliation
- Not immediately downloadable

**Format**: Varies (usually Shapefile)  
**Response Time**: 2-4 weeks

---

### WII (Wildlife Institute of India)
✅ **Pros:**
- Research-quality data
- Scientific accuracy
- Habitat analysis included
- Peer-reviewed

❌ **Cons:**
- Requires formal request
- May need collaboration
- Access varies by purpose

**Format**: Shapefile, GeoTIFF  
**Response Time**: 2-4 weeks

---

### State Forest Departments
✅ **Pros:**
- Most detailed reserve-specific data
- Local accuracy
- May include recent updates
- Official boundaries

❌ **Cons:**
- Need to contact each state separately
- Variable response times
- May require RTI request
- Digital availability varies

**Format**: PDF maps, Shapefile (if digitized)  
**Response Time**: 4-8 weeks

---

## Tiger Reserve Data Checklist

When you obtain GIS data, verify it includes:

### Essential Attributes
- [ ] Reserve name
- [ ] State
- [ ] Zone type (Core/Buffer)
- [ ] Area (sq km)
- [ ] Boundary geometry

### Desirable Attributes
- [ ] Notification year
- [ ] Legal status (National Park, Sanctuary, etc.)
- [ ] Management authority
- [ ] Coordinate reference system documented

### Spatial Quality
- [ ] Boundaries are closed polygons
- [ ] No gaps between core and buffer
- [ ] CRS properly defined
- [ ] Topology is clean (no overlaps/slivers)

---

## Sample Request Email Template

```
Subject: Request for Tiger Reserve GIS Data for [Research/Conservation Purpose]

Dear Sir/Madam,

I am writing to request geospatial data (shapefiles) for India's tiger reserves, 
specifically delineating the Core Areas and Buffer Zones.

Purpose: [Educational/Research/Conservation Planning]
Institution: [Your organization if applicable]
Use Case: [Brief description of how data will be used]

Specifically, I am requesting:
1. Shapefiles for all 58 tiger reserves
2. Distinction between Core and Buffer zones
3. Attribute data including reserve names, areas, and notification details

I assure you that this data will be used solely for [stated purpose] and will 
not be redistributed without proper attribution and permission.

I would be grateful if you could guide me on the process to obtain this data 
or direct me to the appropriate department/portal.

Thank you for your time and consideration.

Best regards,
[Your Name]
[Contact Information]
[Institutional Affiliation if applicable]
```

---

## List of 58 Tiger Reserves (as of 2026)

### Madhya Pradesh (7)
1. Kanha, 2. Bandhavgarh, 3. Pench, 4. Satpura, 5. Panna, 6. Sanjay-Dubri, 7. Veerangana Durgavati

### Karnataka (5)
8. Nagarhole, 9. Bandipur, 10. Bhadra, 11. Dandeli-Anshi, 12. Biligiri Rangaswamy Temple

### Maharashtra (6)
13. Tadoba-Andhari, 14. Pench (MH), 15. Melghat, 16. Sahyadri, 17. Navegaon-Nagzira, 18. Bor

### Tamil Nadu (5)
19. Mudumalai, 20. Anamalai, 21. Kalakkad-Mundanthurai, 22. Sathyamangalam, 23. Mukurthi

### Uttarakhand (2)
24. Corbett, 25. Rajaji

### Rajasthan (4)
26. Ranthambore, 27. Sariska, 28. Mukundra Hills, 29. Ramgarh Vishdhari

### Assam (3)
30. Kaziranga, 31. Manas, 32. Orang (Rajiv Gandhi)

### And 26 more across other states...

**📋 Full list with areas available in GIS_DATA_SOURCES.md**

---

## File Naming Convention

When saving GIS data, use this structure:

```
india_tiger_reserves_[source]_[date].[ext]
Examples:
- india_tiger_reserves_wdpa_2026.shp
- india_tiger_reserves_ntca_core_2026.shp
- india_tiger_reserves_ntca_buffer_2026.shp
- corbett_tiger_reserve_detailed_2026.gpkg
```

---

## Common Issues & Solutions

### Issue: Core/Buffer zones not distinguished in downloaded data
**Solution**: 
- Request specific data from NTCA/WII
- Cross-reference with management plan maps
- Digitize from official documents

### Issue: Coordinate system not recognized
**Solution**:
- India commonly uses WGS84 (EPSG:4326) or UTM zones
- Check .prj file in shapefile
- Reproject if needed in QGIS

### Issue: Data request not responded to
**Solution**:
- Follow up after 2 weeks
- Try alternative contact methods
- Consider RTI (Right to Information) request
- Contact through institutional channels

### Issue: Boundaries seem inaccurate
**Solution**:
- Verify against Protected Planet
- Cross-check with satellite imagery (Bhuvan)
- Contact managing authority for clarification
- Use most recent/official source

---

## Useful GIS Tools

### View/Explore Data
- **QGIS** (free) - https://qgis.org
- **Google Earth** - For KML/KMZ files

### Process/Analyze Data
- **Python + GeoPandas** - Programmatic analysis
- **R + sf package** - Statistical GIS
- **QGIS** - Visual analysis and mapping

### Quick Preview
```python
# Python quick preview
import geopandas as gpd
import matplotlib.pyplot as plt

# Load shapefile
gdf = gpd.read_file('tiger_reserves.shp')

# Quick stats
print(f"Number of reserves: {len(gdf)}")
print(f"Total area: {gdf.geometry.area.sum()} sq degrees")

# Quick plot
gdf.plot(column='Zone_Type', legend=True)
plt.show()
```

---

## Priority Reserves (Start Here)

If you can't get all 58 reserves immediately, prioritize these:

### Top 5 by Tiger Population
1. **Corbett** (Uttarakhand) - 260+ tigers
2. **Nagarhole** (Karnataka) - 140+ tigers
3. **Bandipur** (Karnataka) - 150+ tigers
4. **Kanha** (Madhya Pradesh) - 120+ tigers
5. **Bandhavgarh** (Madhya Pradesh) - 100+ tigers

### Key Landscape Reserves
- **Western Ghats**: Nagarhole, Bandipur, Mudumalai, Anamalai
- **Central India**: Kanha, Pench, Tadoba
- **Terai Arc**: Corbett, Dudhwa
- **Northeast**: Kaziranga, Manas

---

**Quick Help**: See GIS_DATA_SOURCES.md for complete documentation  
**Last Updated**: January 14, 2026

