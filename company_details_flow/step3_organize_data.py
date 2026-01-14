"""
STEP 3: Organize information into a standard format without repetitions

This module transforms raw address data into a standardized schema
and removes duplicates.

Schema (as per context.md):
    - company_name: Name of the company
    - source: Data source (wikipedia/careers/about)
    - address_location: Office address or location
"""


def organize_office_data(raw_data_list, company_name="Google"):
    """
    Step 3: Organize raw address data into standard format
    
    Args:
        raw_data_list: List of raw address dictionaries from Step 2
        company_name: Name of the company
    
    Returns:
        List of organized office dictionaries following the standard schema
        Example:
        [
            {
                'company_name': 'Google',
                'source': 'wikipedia',
                'address_location': '1600 Amphitheatre Parkway, Mountain View, CA'
            },
            ...
        ]
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


def validate_schema(offices):
    """
    Validate that all offices follow the standard schema
    
    Args:
        offices: List of office dictionaries
    
    Returns:
        Tuple (is_valid, errors)
    """
    required_fields = ['company_name', 'source', 'address_location']
    errors = []
    
    for i, office in enumerate(offices):
        for field in required_fields:
            if field not in office:
                errors.append(f"Office {i}: Missing required field '{field}'")
            elif not office[field]:
                errors.append(f"Office {i}: Empty value for field '{field}'")
    
    return len(errors) == 0, errors


if __name__ == "__main__":
    # Test the function
    print("Testing Step 3: Organize Data")
    print("="*80)
    
    # Sample raw data
    raw_data = [
        {
            'raw_location': 'Mountain View',
            'raw_address': '1600 Amphitheatre Parkway, Mountain View, CA',
            'source_type': 'wikipedia'
        },
        {
            'raw_location': 'New York',
            'raw_address': '111 8th Avenue, New York, NY',
            'source_type': 'about'
        },
        # Duplicate
        {
            'raw_location': 'Mountain View',
            'raw_address': '1600 Amphitheatre Parkway, Mountain View, CA',
            'source_type': 'wikipedia'
        }
    ]
    
    organized = organize_office_data(raw_data, "Google")
    
    print(f"\nInput: {len(raw_data)} raw entries")
    print(f"Output: {len(organized)} unique offices")
    print(f"Duplicates removed: {len(raw_data) - len(organized)}")
    
    print("\nValidating schema...")
    is_valid, errors = validate_schema(organized)
    if is_valid:
        print("✓ Schema validation passed")
    else:
        print("✗ Schema validation failed:")
        for error in errors:
            print(f"  - {error}")
    
    print("\nSample output:")
    for office in organized:
        print(office)

