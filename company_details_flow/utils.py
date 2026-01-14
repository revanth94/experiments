"""
Utility functions for saving and displaying office data
"""

import json
import csv


def save_to_json(offices, filename="google_offices.json"):
    """
    Save offices to JSON file
    
    Args:
        offices: List of office dictionaries
        filename: Output filename
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(offices, f, indent=2, ensure_ascii=False)
    print(f"\nSaved {len(offices)} office locations to {filename}")


def save_to_csv(offices, filename="google_offices.csv"):
    """
    Save offices to CSV file
    
    Args:
        offices: List of office dictionaries
        filename: Output filename
    """
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        if offices:
            writer = csv.DictWriter(f, fieldnames=offices[0].keys())
            writer.writeheader()
            writer.writerows(offices)
    print(f"Saved {len(offices)} office locations to {filename}")


def print_offices(offices):
    """
    Print offices in a readable format following the standard schema
    
    Args:
        offices: List of office dictionaries
    """
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


def print_summary(offices):
    """
    Print summary statistics about the offices found
    
    Args:
        offices: List of office dictionaries
    """
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


if __name__ == "__main__":
    # Test utilities
    print("Testing Utility Functions")
    print("="*80)
    
    test_data = [
        {
            'company_name': 'Google',
            'source': 'wikipedia',
            'address_location': '1600 Amphitheatre Parkway, Mountain View, CA'
        },
        {
            'company_name': 'Google',
            'source': 'about',
            'address_location': '111 8th Avenue, New York, NY'
        }
    ]
    
    print("\nTesting print_offices...")
    print_offices(test_data)
    
    print("\nTesting print_summary...")
    print_summary(test_data)
    
    print("\nTesting save functions...")
    save_to_json(test_data, "test_offices.json")
    save_to_csv(test_data, "test_offices.csv")
    print("\n✓ Test files created")

