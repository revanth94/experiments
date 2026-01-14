# Historical Census Data - India Tigers

## About This Data

This directory contains historical tiger census data for India from the **National Tiger Conservation Authority (NTCA)**.

### Data Files

| File | Description | Format |
|------|-------------|--------|
| `india_tiger_census_national.csv` | National-level census data (2006-2022) | CSV |
| `india_tiger_census_states_2022.csv` | State-level breakdown for 2022 census | CSV |
| `india_tiger_census.json` | Complete dataset with metadata and conservation notes | JSON |

### Documentation

| File | Purpose |
|------|---------|
| `DATA_SOURCES.md` | Complete source documentation, verification process, and access instructions |
| `SOURCES_QUICK_REFERENCE.md` | Quick reference guide for data sources |

### Scripts

| File | Purpose |
|------|---------|
| `ingest_tiger_data.py` | Python script to load, query, and analyze census data |

## Quick Start

### Load and Analyze Data

```bash
python ingest_tiger_data.py
```

### Use in Your Own Code

```python
from ingest_tiger_data import TigerCensusDataLoader

# Initialize loader
loader = TigerCensusDataLoader()

# Get national census data
national_data = loader.load_national_census()

# Get state breakdown
states_data = loader.load_state_breakdown(year=2022)

# Get complete dataset
complete_data = loader.load_complete_dataset()

# Query specific data
latest_population = loader.get_latest_population()
top_5_states = loader.get_top_states(n=5)
```

## Data Overview

### National Trend (2006-2022)

| Year | Population | Change | % Change |
|------|-----------|--------|----------|
| 2006 | 1,411 | - | - |
| 2010 | 1,706 | +295 | +20.9% |
| 2014 | 2,226 | +520 | +30.5% |
| 2018 | 2,967 | +741 | +33.3% |
| 2022 | 3,682 | +715 | +24.1% |

### Top 5 States (2022)

1. **Madhya Pradesh**: 785 tigers (21.3%)
2. **Karnataka**: 563 tigers (15.3%)
3. **Uttarakhand**: 560 tigers (15.2%)
4. **Maharashtra**: 444 tigers (12.1%)
5. **Tamil Nadu**: 306 tigers (8.3%)

## Data Source

**National Tiger Conservation Authority (NTCA)**
- **Website**: https://ntca.gov.in
- **Organization**: Government of India, Ministry of Environment, Forest and Climate Change
- **Census Frequency**: Every 4 years
- **Methodology**: Camera trap surveys with spatially explicit capture-recapture (SECR) statistical models
- **Latest Census**: 2022 (3,682 tigers)
- **Next Expected**: 2026

## Data Quality

- ✅ **Official Source**: Government of India data
- ✅ **Verified**: Cross-checked against WWF, IUCN, and GTF
- ✅ **Methodology**: Consistent camera trap surveys across all census years
- ✅ **Coverage**: 18 states, 53 tiger reserves, 26,000+ camera traps (2022)

## License & Attribution

- Data source: National Tiger Conservation Authority (NTCA), Government of India
- Census reports are public information for conservation, research, and educational purposes
- Please credit NTCA and the respective census year when using this data

## Updates

- **Last Updated**: January 14, 2026
- **Dataset Version**: 1.0
- **Coverage**: 2006, 2010, 2014, 2018, 2022
- **Next Update**: After 2026 census (likely 2027)

## More Information

📚 See [DATA_SOURCES.md](DATA_SOURCES.md) for complete documentation including:
- Detailed methodology
- All official report titles and dates
- Verification sources
- Access instructions for downloading official reports
- Data limitations and caveats
- Update procedures

