# Company Office Location Finder

A modular Python tool to find and organize company office locations from public web sources.

## 📁 Project Structure

```
company_details_flow/
├── README.md                   # This file
├── context.md                  # Guidelines for the 3-step process
├── BREAKDOWN.md                # Detailed technical documentation
├── requirements.txt            # Python dependencies
│
├── main.py                     # 🎯 Main orchestrator (RUN THIS)
├── step1_find_urls.py          # 📋 STEP 1: Find URLs
├── step2_parse_urls.py         # 🔍 STEP 2: Parse URLs for addresses
├── step3_organize_data.py      # 📊 STEP 3: Organize & deduplicate
├── utils.py                    # 🛠️ Utility functions
│
├── find_google_offices.py      # (Legacy monolithic version)
├── google_offices.json         # Output: JSON format
└── google_offices.csv          # Output: CSV format
```

## 🚀 Quick Start

### Installation

```bash
cd company_details_flow
pip install -r requirements.txt
```

### Run the Full Process

```bash
python main.py
```

This will:
1. ✅ Find URLs where office addresses are likely located
2. ✅ Parse those URLs to extract address data
3. ✅ Organize data into standard schema and remove duplicates
4. ✅ Save results to JSON and CSV files
5. ✅ Display summary with statistics

## 📋 The 3-Step Process (from context.md)

### **STEP 1: Find URLs**
- File: `step1_find_urls.py`
- Function: `find_urls_with_addresses(company_name)`
- Output: List of URLs to scrape

### **STEP 2: Parse URLs**
- File: `step2_parse_urls.py`
- Function: `parse_url_for_addresses(url, url_type, company_name)`
- Output: Raw address data extracted from URLs

### **STEP 3: Organize Data**
- File: `step3_organize_data.py`
- Function: `organize_office_data(raw_data_list, company_name)`
- Output: Standardized, deduplicated office list

## 📊 Output Schema

All output follows this standard schema:

```json
{
  "company_name": "Google",
  "source": "wikipedia",
  "address_location": "1600 Amphitheatre Parkway, Mountain View, CA"
}
```

**Fields:**
- `company_name` - Name of the company
- `source` - Data source (wikipedia/careers/about)
- `address_location` - Office address or location

## 🧪 Testing Individual Modules

Each step can be tested independently:

```bash
# Test Step 1: Find URLs
python step1_find_urls.py

# Test Step 2: Parse URLs (requires network)
python step2_parse_urls.py

# Test Step 3: Organize data
python step3_organize_data.py

# Test utilities
python utils.py
```

## 🔧 Usage as a Library

Import and use individual steps:

```python
from step1_find_urls import find_urls_with_addresses
from step2_parse_urls import parse_url_for_addresses
from step3_organize_data import organize_office_data

# Step 1: Get URLs
urls = find_urls_with_addresses("Google")

# Step 2: Parse each URL
all_data = []
for url_info in urls:
    data = parse_url_for_addresses(url_info['url'], url_info['type'], "Google")
    all_data.extend(data)

# Step 3: Organize
offices = organize_office_data(all_data, "Google")
```

Or use the main function:

```python
from main import find_company_offices

# Find Google offices
google_offices = find_company_offices("Google")

# Find Microsoft offices
microsoft_offices = find_company_offices("Microsoft")
```

## 🎯 Customization

### Change Company Name

Edit `main.py`:

```python
if __name__ == "__main__":
    COMPANY_NAME = "Microsoft"  # Change here
    offices = find_company_offices(COMPANY_NAME)
```

### Add New URL Sources

Edit `step1_find_urls.py` and add to the `urls` list:

```python
urls.append({
    'url': f"https://newsite.com/{company_name}/offices",
    'type': 'custom',
    'priority': 3
})
```

### Add New Parser

Edit `step2_parse_urls.py`:

1. Add a new parser function:
```python
def parse_custom_page(soup, company_name):
    # Your parsing logic
    return addresses
```

2. Add to the routing logic:
```python
elif url_type == 'custom':
    addresses = parse_custom_page(soup, company_name)
```

## 📦 Dependencies

- `requests` - HTTP requests
- `beautifulsoup4` - HTML parsing

Install with:
```bash
pip install -r requirements.txt
```

## 📖 Documentation

- `BREAKDOWN.md` - Detailed technical documentation
- `context.md` - Process guidelines

## ✅ Features

- ✅ Modular architecture (each step in separate file)
- ✅ Independent testing of each module
- ✅ Standard schema compliance
- ✅ Automatic deduplication
- ✅ Schema validation
- ✅ Multiple data sources (Wikipedia, careers pages, about pages)
- ✅ JSON and CSV export
- ✅ Extensible for any company
- ✅ Clear progress indicators
- ✅ Error handling

## 🎓 Example Output

```
================================================================================
FINDING GOOGLE OFFICE LOCATIONS
================================================================================

STEP 1: Finding URLs where addresses are likely to be found
✓ Step 1 complete: 3 URLs identified

STEP 2: Parsing URLs to get potential address data
✓ Step 2 complete: 17 address entries extracted

STEP 3: Organizing information into standard format
✓ Step 3 complete: 17 unique offices organized
✓ Removed 0 duplicate entries
✓ Schema validation passed

================================================================================
Process completed successfully!
================================================================================
```

## 🔍 Current Data Sources

1. **Wikipedia** - Structured tables with office information
2. **Company Careers Page** - Location listings
3. **Company About Page** - Address information

## 🚧 Future Enhancements

- [ ] Add Google Maps API integration
- [ ] Support for additional data sources
- [ ] Geocoding addresses to lat/long
- [ ] Add country/region classification
- [ ] Support for multiple companies in one run
- [ ] Cache results to avoid repeated scraping
- [ ] Add logging system

## 📝 License

This is an experimental/learning project.

## 🤝 Contributing

This is a personal learning project, but improvements are welcome!

