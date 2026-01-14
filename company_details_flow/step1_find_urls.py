"""
STEP 1: Find URLs where addresses are likely to be found

This module identifies potential URLs that contain office address information.
"""


def find_urls_with_addresses(company_name="Google"):
    """
    Step 1: Identify URLs where office addresses are likely to be found
    
    Args:
        company_name: Name of the company to search for
    
    Returns:
        List of URL dictionaries with metadata
        Example:
        [
            {
                'url': 'https://en.wikipedia.org/wiki/List_of_Google_offices',
                'type': 'wikipedia',
                'priority': 1
            },
            ...
        ]
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


if __name__ == "__main__":
    # Test the function
    print("Testing Step 1: Find URLs")
    print("="*80)
    urls = find_urls_with_addresses("Google")
    print(f"\nReturned {len(urls)} URLs")

