#!/usr/bin/env python3
"""
Test script for validators
Run this to test your validation logic
"""

from validators import (
    validate_location,
    validate_ecological_impacts,
    validate_purpose,
    validate_customer_name,
    validate_all_requirements,
    sanitize_requirements
)


def test_validators():
    """Test all validators with sample data"""
    
    print("Testing Validators")
    print("=" * 60)
    
    # Test location validation
    print("\n1. Testing Location Validator:")
    test_locations = [
        "Amazon Rainforest, Brazil",
        "NY",
        "123",
        "",
    ]
    for loc in test_locations:
        is_valid, error = validate_location(loc)
        status = "✓" if is_valid else "✗"
        print(f"  {status} '{loc}' - {error if error else 'Valid'}")
    
    # Test ecological impacts validation
    print("\n2. Testing Ecological Impacts Validator:")
    test_impacts = [
        ["air quality", "water pollution"],
        ["deforestation"],
        [],
        ["x"],
    ]
    for impacts in test_impacts:
        is_valid, error = validate_ecological_impacts(impacts)
        status = "✓" if is_valid else "✗"
        print(f"  {status} {impacts} - {error if error else 'Valid'}")
    
    # Test purpose validation
    print("\n3. Testing Purpose Validator:")
    test_purposes = [
        "Environmental impact assessment for conservation project",
        "Research",
        "short",
        "",
    ]
    for purpose in test_purposes:
        is_valid, error = validate_purpose(purpose)
        status = "✓" if is_valid else "✗"
        print(f"  {status} '{purpose}' - {error if error else 'Valid'}")
    
    # Test full requirements validation
    print("\n4. Testing Complete Requirements:")
    sample_requirements = {
        "customer_name": "EcoResearch Corp",
        "location": "Amazon Rainforest, Brazil",
        "ecological_impacts": ["deforestation", "wildlife habitat", "carbon emissions"],
        "purpose": "Environmental impact assessment for sustainable development",
        "additional_info": "Focus on endangered species"
    }
    
    is_valid, errors = validate_all_requirements(sample_requirements)
    if is_valid:
        print("  ✓ All validations passed!")
    else:
        print("  ✗ Validation failed:")
        for error in errors:
            print(f"    - {error}")
    
    # Test sanitization
    print("\n5. Testing Sanitization:")
    dirty_requirements = {
        "customer_name": "  John Doe  ",
        "location": "  New York  ",
        "ecological_impacts": ["air quality", "  water  ", "", "air quality"],  # duplicates and empty
        "purpose": "  Research project  ",
        "additional_info": "  ",
    }
    
    clean = sanitize_requirements(dirty_requirements)
    print(f"  Customer: '{dirty_requirements['customer_name']}' → '{clean['customer_name']}'")
    print(f"  Location: '{dirty_requirements['location']}' → '{clean['location']}'")
    print(f"  Impacts: {dirty_requirements['ecological_impacts']} → {clean['ecological_impacts']}")
    print(f"  Additional: '{dirty_requirements['additional_info']}' → '{clean['additional_info']}'")
    
    print("\n" + "=" * 60)
    print("Testing complete! Modify validators.py to add custom logic.\n")


if __name__ == "__main__":
    test_validators()

