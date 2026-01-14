"""
STEP 2: Parse URLs to get potential address data

This module extracts raw address data from identified URLs using web scraping.
"""

import requests
from bs4 import BeautifulSoup
import json
import re


def parse_url_for_addresses(url, url_type, company_name="Google"):
    """
    Step 2: Parse a given URL to extract potential address data
    
    Args:
        url: URL to parse
        url_type: Type of URL (wikipedia/careers/about)
        company_name: Name of the company
    
    Returns:
        List of raw address data dictionaries
        Example:
        [
            {
                'raw_location': 'Mountain View',
                'raw_address': '1600 Amphitheatre Parkway, Mountain View, CA',
                'source_type': 'wikipedia'
            },
            ...
        ]
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
    """
    Parse Wikipedia tables for office information
    
    Args:
        soup: BeautifulSoup object
        company_name: Name of the company
    
    Returns:
        List of raw address dictionaries
    """
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
    """
    Parse company careers page for office locations
    
    Args:
        soup: BeautifulSoup object
        company_name: Name of the company
    
    Returns:
        List of raw address dictionaries
    """
    addresses = []
    
    # Find all links that might contain location info
    links = soup.find_all('a', href=True)
    location_links = [link for link in links if '/locations/' in link['href'] or 'office' in link.get_text().lower()]
    
    for link in location_links:
        text_content = link.get_text().strip()
        # Filter out common navigation text
        if text_content and len(text_content) > 2 and len(text_content) < 50:
            # Skip common non-location terms
            skip_terms = ['sign in', 'sign up', 'login', 'register', 'back', 'home', 'menu']
            if text_content.lower() not in skip_terms:
                addresses.append({
                    'raw_location': text_content,
                    'raw_address': '',
                    'source_type': 'careers'
                })
    
    return addresses


def parse_about_page(soup, company_name):
    """
    Parse company about page for office addresses
    
    Args:
        soup: BeautifulSoup object
        company_name: Name of the company
    
    Returns:
        List of raw address dictionaries
    """
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


if __name__ == "__main__":
    # Test the function
    print("Testing Step 2: Parse URLs")
    print("="*80)
    
    test_url = "https://about.google.com/locations/"
    result = parse_url_for_addresses(test_url, 'about', 'Google')
    
    print(f"\nExtracted {len(result)} addresses")
    if result:
        print("\nSample result:")
        print(result[0])

