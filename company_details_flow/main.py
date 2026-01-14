"""
Main orchestrator for finding company office locations

This script follows the 3-step process defined in context.md:
1. Find URLs where addresses are likely to be found
2. Parse URLs to get potential address data
3. Organize information into a standard format without repetitions

Each step is implemented in a separate module for modularity and maintainability.
"""

from step1_find_urls import find_urls_with_addresses
from step2_parse_urls import parse_url_for_addresses
from step3_organize_data import organize_office_data, validate_schema
from utils import save_to_json, save_to_csv, print_offices, print_summary


def find_company_offices(company_name="Google"):
    """
    Main workflow to find company office addresses
    
    Orchestrates the 3-step process:
    1. Find URLs where addresses are likely to be found
    2. Parse URLs to get potential address data
    3. Organize information into a standard format without repetitions
    
    Args:
        company_name: Name of the company to search for
    
    Returns:
        List of organized office dictionaries following the standard schema
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
    print(f"✓ Removed {len(all_raw_data) - len(organized_offices)} duplicate entries")
    
    # Validate schema
    is_valid, errors = validate_schema(organized_offices)
    if is_valid:
        print(f"✓ Schema validation passed\n")
    else:
        print(f"⚠ Schema validation warnings:")
        for error in errors[:5]:  # Show first 5 errors
            print(f"  • {error}")
        print()
    
    return organized_offices


if __name__ == "__main__":
    # Configuration
    COMPANY_NAME = "Google"
    
    # Run the 3-step process
    offices = find_company_offices(COMPANY_NAME)
    
    if offices:
        # Display results
        print_offices(offices)
        
        # Save to files
        save_to_json(offices)
        save_to_csv(offices)
        
        # Print summary
        print_summary(offices)
        
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

