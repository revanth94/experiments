# Code Breakdown - Modular Structure Following context.md

## Overview
The office location finder is now organized into **separate files for each step** as defined in `context.md`, promoting modularity, maintainability, and reusability.

---

## 📁 File Structure

```
company_details_flow/
├── context.md              # Guidelines for the 3-step process
├── main.py                 # Main orchestrator
├── step1_find_urls.py      # STEP 1: Find URLs
├── step2_parse_urls.py     # STEP 2: Parse URLs
├── step3_organize_data.py  # STEP 3: Organize data
├── utils.py                # Utility functions (save, print)
├── requirements.txt        # Python dependencies
├── google_offices.json     # Output: JSON format
└── google_offices.csv      # Output: CSV format
```

---

## 📋 STEP 1: Find URLs (step1_find_urls.py)

### Function: `find_urls_with_addresses(company_name)`

**Purpose:** Identify potential URLs that contain office address information

**Input:** Company name (string)

**Output:** List of URL dictionaries
```python
[
    {
        'url': 'https://en.wikipedia.org/wiki/List_of_Google_offices',
        'type': 'wikipedia',
        'priority': 1
    },
    {
        'url': 'https://careers.google.com/locations/',
        'type': 'careers',
        'priority': 2
    },
    {
        'url': 'https://about.google.com/locations/',
        'type': 'about',
        'priority': 2
    }
]
```

**Key Features:**
- Constructs URLs based on common patterns
- Prioritizes sources (Wikipedia > company pages)
- Easily extensible to add more URL sources

**Usage:**
```python
from step1_find_urls import find_urls_with_addresses

urls = find_urls_with_addresses("Google")
```

---

## 🔍 STEP 2: Parse URLs (step2_parse_urls.py)

### Main Function: `parse_url_for_addresses(url, url_type, company_name)`

**Purpose:** Extract raw address data from each URL

**Input:**
- `url`: URL to parse (string)
- `url_type`: Type of URL (wikipedia/careers/about)
- `company_name`: Company name (string)

**Output:** Raw address data list
```python
[
    {
        'raw_location': 'Mountain View',
        'raw_address': '1600 Amphitheatre Parkway, Mountain View, CA',
        'source_type': 'wikipedia'
    },
    ...
]
```

### Specialized Parsers:

#### `parse_wikipedia_table(soup, company_name)`
- Extracts data from Wikipedia's structured tables
- Looks for `wikitable` class tables
- Extracts location and address from table cells

#### `parse_careers_page(soup, company_name)`
- Finds location links in careers pages
- Extracts city/location names from links
- Filters for reasonable-length location names
- Excludes common navigation text (sign in, login, etc.)

#### `parse_about_page(soup, company_name)`
- Attempts to find structured JSON-LD data
- Uses regex to extract street addresses
- Looks for common address patterns (Street, Avenue, etc.)

**Usage:**
```python
from step2_parse_urls import parse_url_for_addresses

raw_data = parse_url_for_addresses(
    'https://about.google.com/locations/',
    'about',
    'Google'
)
```

---

## 📊 STEP 3: Organize Data (step3_organize_data.py)

### Function: `organize_office_data(raw_data_list, company_name)`

**Purpose:** Transform raw data into standardized schema and remove duplicates

**Input:** List of raw address dictionaries from Step 2

**Output:** Clean, standardized office list
```python
[
    {
        'company_name': 'Google',
        'source': 'wikipedia',
        'address_location': '1600 Amphitheatre Parkway, Mountain View, CA'
    },
    {
        'company_name': 'Google',
        'source': 'careers',
        'address_location': 'New York'
    },
    ...
]
```

**Schema (as per context.md):**
- `company_name` - Name of the company
- `source` - Where the data came from (wikipedia/careers/about)
- `address_location` - The office address or location

### Function: `validate_schema(offices)`

**Purpose:** Validate that all offices follow the standard schema

**Output:** Tuple (is_valid, errors)

**Key Features:**
1. **Deduplication:** Uses unique key combining location and address
2. **Standardization:** Maps all raw data to consistent schema
3. **Cleaning:** Removes entries with missing critical data
4. **Validation:** Ensures schema compliance

**Usage:**
```python
from step3_organize_data import organize_office_data, validate_schema

organized = organize_office_data(raw_data_list, "Google")
is_valid, errors = validate_schema(organized)
```

---

## 🛠️ Utility Functions (utils.py)

### `save_to_json(offices, filename)`
Saves organized office data to JSON file with proper formatting

### `save_to_csv(offices, filename)`
Saves organized office data to CSV file using the standard schema keys as headers

### `print_offices(offices)`
Displays offices grouped by source, showing the standard schema fields

### `print_summary(offices)`
Displays summary statistics and source breakdown

**Usage:**
```python
from utils import save_to_json, save_to_csv, print_offices, print_summary

print_offices(offices)
save_to_json(offices)
save_to_csv(offices)
print_summary(offices)
```

---

## 🔄 Main Orchestrator (main.py)

### Function: `find_company_offices(company_name)`

**Orchestrates the entire 3-step process:**

```python
def find_company_offices(company_name="Google"):
    # STEP 1: Find URLs
    urls = find_urls_with_addresses(company_name)
    
    # STEP 2: Parse URLs
    all_raw_data = []
    for url_info in urls:
        raw_data = parse_url_for_addresses(
            url_info['url'], 
            url_info['type'],
            company_name
        )
        all_raw_data.extend(raw_data)
    
    # STEP 3: Organize data
    organized_offices = organize_office_data(all_raw_data, company_name)
    
    # Validate schema
    validate_schema(organized_offices)
    
    return organized_offices
```

---

## 🎯 Key Benefits of Modular Structure

### 1. **Separation of Concerns**
- Each step is in its own file
- Easy to understand and maintain
- Clear boundaries between modules

### 2. **Reusability**
- Each module can be imported and used independently
- Functions can be tested in isolation
- Easy to reuse for different companies

### 3. **Testability**
- Each file has a `if __name__ == "__main__"` block for testing
- Can test each step independently
- Easy to add unit tests

### 4. **Extensibility**
- Add new URL sources in `step1_find_urls.py`
- Add new parsers in `step2_parse_urls.py`
- Modify schema in `step3_organize_data.py`
- No need to touch other modules

### 5. **Maintainability**
- Changes to one step don't affect others
- Clear file structure
- Well-documented functions

---

## 📝 Usage Examples

### Basic Usage
```bash
python main.py
```

### Using Individual Modules
```python
# Step 1 only
from step1_find_urls import find_urls_with_addresses
urls = find_urls_with_addresses("Microsoft")

# Step 2 only
from step2_parse_urls import parse_url_for_addresses
data = parse_url_for_addresses(url, 'about', 'Microsoft')

# Step 3 only
from step3_organize_data import organize_office_data
offices = organize_office_data(raw_data, 'Microsoft')
```

### Testing Individual Steps
```bash
# Test Step 1
python step1_find_urls.py

# Test Step 2
python step2_parse_urls.py

# Test Step 3
python step3_organize_data.py

# Test Utilities
python utils.py
```

---

## 🔧 Customization for Other Companies

Simply modify `main.py`:

```python
if __name__ == "__main__":
    COMPANY_NAME = "Microsoft"  # Change this
    offices = find_company_offices(COMPANY_NAME)
```

Or use as a library:

```python
from main import find_company_offices

# Find Microsoft offices
microsoft_offices = find_company_offices("Microsoft")

# Find Apple offices
apple_offices = find_company_offices("Apple")
```

---

## 🧪 Testing Each Module

Each module can be tested independently:

```bash
# Test each module
python step1_find_urls.py     # Test URL finding
python step2_parse_urls.py    # Test parsing (needs network)
python step3_organize_data.py # Test organization
python utils.py               # Test utilities
```

All modules include test code in their `if __name__ == "__main__"` blocks.

---

## 📦 Dependencies

Install required packages:
```bash
pip install -r requirements.txt
```

Required:
- `requests` - HTTP requests
- `beautifulsoup4` - HTML parsing

---

## 🎓 Schema Compliance

All output follows the schema defined in `context.md`:

```json
{
  "company_name": "string",
  "source": "string (wikipedia/careers/about)",
  "address_location": "string"
}
```

This ensures consistency across all outputs (JSON, CSV, display).
