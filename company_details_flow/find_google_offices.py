import requests
from bs4 import BeautifulSoup
import json
import time
import re

# =============================================================================
# STEP 1: Find URLs where addresses are likely to be found
# =============================================================================

def find_urls_with_addresses(company_name="Google"):
    """
    Step 1: Identify URLs where office addresses are likely to be found
    Returns a list of URLs to scrape
    """
    urls = []
    
    # Wikipedia - Often has comprehensive office listings
    urls.append({
        'url': f"https://en.wikipedia.org/wiki/List_of_{company_name}_offices",
        'type': 'wikipedia',
        'priority': 1
    })
    
    # Company careers/locations page
    urls.append({
        'url': f"https://careers.{company_name.lower()}.com/locations/",
        'type': 'careers',
        'priority': 2
    })
    
    # Company about page
    urls.append({
        'url': f"https://about.{company_name.lower()}.com/locations/",
        'type': 'about',
        'priority': 2
    })
    
    print(f"Step 1: Found {len(urls)} potential URLs to scrape")
    for url_info in urls:
        print(f"  - {url_info['url']} (type: {url_info['type']})")
    
    return urls


# =============================================================================
# STEP 2: Parse URLs to get potential address data
# =============================================================================

def parse_url_for_addresses(url, url_type, company_name="Google"):
    """
    Step 2: Parse a given URL to extract potential address data
    Returns raw address data found on the page
    """
    addresses = []
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    
    try:
        print(f"\n  Parsing: {url}")
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code != 200:
            print(f"  ✗ Failed to access (status: {response.status_code})")
            return addresses
        
        soup = BeautifulSoup(response.content, 'html.parser')
        print(f"  ✓ Successfully fetched page")
        
        # Parse based on URL type
        if url_type == 'wikipedia':
            addresses = parse_wikipedia_table(soup, company_name)
        elif url_type == 'careers':
            addresses = parse_careers_page(soup, company_name)
        elif url_type == 'about':
            addresses = parse_about_page(soup, company_name)
        
        print(f"  ✓ Extracted {len(addresses)} address(es)")
            
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    return addresses


def parse_wikipedia_table(soup, company_name):
    """Parse Wikipedia tables for office information"""
    addresses = []
    
    # Find all tables
    tables = soup.find_all('table', class_='wikitable')
    
    for table in tables:
        rows = table.find_all('tr')[1:]  # Skip header
        for row in rows:
            cells = row.find_all(['td', 'th'])
            if len(cells) >= 2:
                location = cells[0].get_text().strip()
                address = cells[1].get_text().strip() if len(cells) > 1 else ''
                
                if location:
                    addresses.append({
                        'raw_location': location,
                        'raw_address': address,
                        'source_type': 'wikipedia'
                    })
    
    return addresses


def parse_careers_page(soup, company_name):
    """Parse company careers page for office locations"""
    addresses = []
    
    # Find all links that might contain location info
    links = soup.find_all('a', href=True)
    location_links = [link for link in links if '/locations/' in link['href'] or 'office' in link.get_text().lower()]
    
    for link in location_links:
        text_content = link.get_text().strip()
        if text_content and len(text_content) > 2 and len(text_content) < 50:
            addresses.append({
                'raw_location': text_content,
                'raw_address': '',
                'source_type': 'careers'
            })
    
    return addresses


def parse_about_page(soup, company_name):
    """Parse company about page for office addresses"""
    addresses = []
    
    # Try to find structured data
    scripts = soup.find_all('script', type='application/ld+json')
    for script in scripts:
        try:
            data = json.loads(script.string)
            if isinstance(data, dict) and 'location' in str(data).lower():
                # Found structured location data
                pass
        except:
            pass
    
    # Look for address patterns in text
    text = soup.get_text()
    address_pattern = r'(\d+[^,\n]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr|Way|Lane|Ln|Parkway|Pkwy)[^,\n]*(?:,\s*[^,\n]+){1,3})'
    found_addresses = re.findall(address_pattern, text)
    
    for addr in found_addresses[:20]:  # Limit results
        if len(addr) > 30:
            addresses.append({
                'raw_location': '',
                'raw_address': addr.strip(),
                'source_type': 'about'
            })
    
    return addresses

# =============================================================================
# STEP 3: Organize information into a standard format without repetitions
# =============================================================================

def organize_office_data(raw_data_list, company_name="Google"):
    """
    Step 3: Organize raw address data into standard format
    Schema: company_name, source, address_location
    Removes duplicates
    """
    organized_offices = []
    seen_addresses = set()
    
    for raw_data in raw_data_list:
        # Extract fields
        location = raw_data.get('raw_location', '').strip()
        address = raw_data.get('raw_address', '').strip()
        source_type = raw_data.get('source_type', 'unknown')
        
        # Create unique key for deduplication
        unique_key = f"{location}|{address}".lower()
        
        if unique_key in seen_addresses or not (location or address):
            continue
        
        seen_addresses.add(unique_key)
        
        # Organize into standard schema
        office = {
            'company_name': company_name,
            'source': source_type,
            'address_location': address if address else location
        }
        
        organized_offices.append(office)
    
    return organized_offices

# =============================================================================
# MAIN WORKFLOW: Orchestrates the 3-step process
# =============================================================================

def find_google_offices(company_name="Google"):
    """
    Main workflow to find company office addresses
    Follows the 3-step process from context.md:
    1. Find URLs where addresses are likely to be found
    2. Parse URLs to get potential address data
    3. Organize information into a standard format without repetitions
    """
    print("="*80)
    print(f"FINDING {company_name.upper()} OFFICE LOCATIONS")
    print("="*80 + "\n")
    
    # STEP 1: Find URLs
    print("="*80)
    print("STEP 1: Finding URLs where addresses are likely to be found")
    print("="*80)
    urls = find_urls_with_addresses(company_name)
    print(f"✓ Step 1 complete: {len(urls)} URLs identified\n")
    
    # STEP 2: Parse URLs
    print("="*80)
    print("STEP 2: Parsing URLs to get potential address data")
    print("="*80)
    all_raw_data = []
    for url_info in urls:
        raw_data = parse_url_for_addresses(
            url_info['url'], 
            url_info['type'],
            company_name
        )
        all_raw_data.extend(raw_data)
    print(f"\n✓ Step 2 complete: {len(all_raw_data)} address entries extracted\n")
    
    # STEP 3: Organize data
    print("="*80)
    print("STEP 3: Organizing information into standard format")
    print("="*80)
    print("Schema: company_name, source, address_location")
    organized_offices = organize_office_data(all_raw_data, company_name)
    print(f"✓ Step 3 complete: {len(organized_offices)} unique offices organized")
    print(f"✓ Removed {len(all_raw_data) - len(organized_offices)} duplicate entries\n")
    
    return organized_offices

def save_to_json(offices, filename="google_offices.json"):
    """Save offices to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(offices, f, indent=2, ensure_ascii=False)
    print(f"\nSaved {len(offices)} office locations to {filename}")

def save_to_csv(offices, filename="google_offices.csv"):
    """Save offices to CSV file"""
    import csv
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        if offices:
            writer = csv.DictWriter(f, fieldnames=offices[0].keys())
            writer.writeheader()
            writer.writerows(offices)
    print(f"Saved {len(offices)} office locations to {filename}")

def print_offices(offices):
    """Print offices in a readable format following the standard schema"""
    print("\n" + "="*80)
    print(f"OFFICE LOCATIONS ({len(offices)} offices found)")
    print("="*80)
    print("Schema: company_name | source | address_location")
    print("="*80 + "\n")
    
    # Group by source for better readability
    by_source = {}
    for office in offices:
        source = office.get('source', 'unknown')
        if source not in by_source:
            by_source[source] = []
        by_source[source].append(office)
    
    # Print grouped by source
    for source, source_offices in sorted(by_source.items()):
        print(f"\n{source.upper()} ({len(source_offices)} locations)")
        print("-" * 80)
        
        for i, office in enumerate(source_offices, 1):
            company = office.get('company_name', 'Unknown')
            address = office.get('address_location', 'N/A')
            
            print(f"{i}. 📍 {company}")
            print(f"   Address: {address}")
            print(f"   Source: {source}")
        print()
    
    print("="*80)

if __name__ == "__main__":
    # Configuration
    COMPANY_NAME = "Google"
    
    # Run the 3-step process
    offices = find_google_offices(COMPANY_NAME)
    
    if offices:
        # Display results
        print_offices(offices)
        
        # Save to files
        save_to_json(offices)
        save_to_csv(offices)
        
        # Final summary
        print("\n" + "="*80)
        print("FINAL SUMMARY")
        print("="*80)
        print(f"✓ Total unique offices found: {len(offices)}")
        
        # Count by source
        sources = {}
        for office in offices:
            source = office.get('source', 'unknown')
            sources[source] = sources.get(source, 0) + 1
        
        print(f"\n✓ Data sources used:")
        for source, count in sorted(sources.items()):
            print(f"  • {source}: {count} location(s)")
        
        print(f"\n✓ Output files:")
        print(f"  • google_offices.json (JSON format - standard schema)")
        print(f"  • google_offices.csv (CSV format - standard schema)")
        
        print(f"\n✓ Schema structure:")
        print(f"  • company_name: Company name")
        print(f"  • source: Data source (wikipedia/careers/about)")
        print(f"  • address_location: Office address or location")
        
        print("\n" + "="*80)
        print("Process completed successfully!")
        print("="*80)
    else:
        print("\n" + "="*80)
        print("⚠  WARNING: No offices found")
        print("="*80)
        print("Possible reasons:")
        print("  • Network connectivity issues")
        print("  • Website structure has changed")
        print("  • URLs are not accessible")
        print("\nPlease check your network connection and try again.")
        print("="*80)

