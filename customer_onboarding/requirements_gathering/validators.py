"""
Validators for customer requirements
Add your custom validation logic here
"""

from typing import List, Dict, Any, Tuple


class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass


def validate_location(location: str) -> Tuple[bool, str]:
    """
    Validate the location input
    
    Args:
        location: The location string to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not location or not location.strip():
        return False, "Location cannot be empty"
    
    if len(location) < 3:
        return False, "Location must be at least 3 characters long"
    
    # Add your custom validation logic here
    # Example: Check if it contains numbers only
    if location.strip().isdigit():
        return False, "Location cannot be only numbers"
    
    return True, ""


def validate_ecological_impacts(impacts: List[str]) -> Tuple[bool, str]:
    """
    Validate the ecological impacts list
    
    Args:
        impacts: List of impact types
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not impacts or len(impacts) == 0:
        return False, "At least one ecological impact must be specified"
    
    # Check for empty strings
    if any(not impact.strip() for impact in impacts):
        return False, "Impact types cannot be empty"
    
    # Check minimum length for each impact
    if any(len(impact.strip()) < 2 for impact in impacts):
        return False, "Each impact type must be at least 2 characters long"
    
    # Add your custom validation logic here
    # Example: Check against a known list of valid impacts
    valid_impacts = {
        "air quality", "water pollution", "deforestation", "wildlife habitat",
        "carbon emissions", "soil degradation", "biodiversity loss", "noise pollution",
        "water quality", "habitat loss", "climate change", "ecosystem disruption"
    }
    
    # Normalize and check (optional - you can remove this if you want to allow any impact)
    # for impact in impacts:
    #     if impact.lower().strip() not in valid_impacts:
    #         return False, f"Unknown impact type: {impact}. Please use recognized environmental impact categories."
    
    return True, ""


def validate_purpose(purpose: str) -> Tuple[bool, str]:
    """
    Validate the purpose of analysis
    
    Args:
        purpose: The purpose string
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not purpose or not purpose.strip():
        return False, "Purpose cannot be empty"
    
    if len(purpose.strip()) < 10:
        return False, "Purpose must be at least 10 characters long (please provide more detail)"
    
    # Add your custom validation logic here
    # Example: Check for certain keywords
    # required_keywords = ["assessment", "analysis", "research", "compliance", "study"]
    # if not any(keyword in purpose.lower() for keyword in required_keywords):
    #     return False, "Purpose should describe the type of analysis or study being conducted"
    
    return True, ""


def validate_customer_name(name: str) -> Tuple[bool, str]:
    """
    Validate customer name (optional field)
    
    Args:
        name: The customer name
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Customer name is optional, but if provided, should meet criteria
    if not name or name.strip() == "":
        return True, ""  # Empty is acceptable for optional field
    
    if len(name.strip()) < 2:
        return False, "Customer name must be at least 2 characters long"
    
    # Add your custom validation logic here
    
    return True, ""


def validate_all_requirements(requirements: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate all requirements at once
    
    Args:
        requirements: Dictionary containing all requirement fields
        
    Returns:
        Tuple of (is_valid, list_of_error_messages)
    """
    errors = []
    
    # Validate customer name
    is_valid, error = validate_customer_name(requirements.get('customer_name', ''))
    if not is_valid:
        errors.append(f"Customer name: {error}")
    
    # Validate location
    is_valid, error = validate_location(requirements.get('location', ''))
    if not is_valid:
        errors.append(f"Location: {error}")
    
    # Validate ecological impacts
    is_valid, error = validate_ecological_impacts(requirements.get('ecological_impacts', []))
    if not is_valid:
        errors.append(f"Ecological impacts: {error}")
    
    # Validate purpose
    is_valid, error = validate_purpose(requirements.get('purpose', ''))
    if not is_valid:
        errors.append(f"Purpose: {error}")
    
    # Add any cross-field validation here
    # Example: If location is in certain regions, require specific impact types
    
    return len(errors) == 0, errors


def sanitize_requirements(requirements: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sanitize and clean up the requirements data
    
    Args:
        requirements: Raw requirements dictionary
        
    Returns:
        Cleaned requirements dictionary
    """
    sanitized = {}
    
    # Clean customer name
    sanitized['customer_name'] = requirements.get('customer_name', 'Anonymous').strip()
    if not sanitized['customer_name']:
        sanitized['customer_name'] = 'Anonymous'
    
    # Clean location
    sanitized['location'] = requirements.get('location', '').strip()
    
    # Clean ecological impacts - remove duplicates and empty strings
    impacts = requirements.get('ecological_impacts', [])
    if isinstance(impacts, str):
        impacts = [i.strip() for i in impacts.split(',')]
    sanitized['ecological_impacts'] = list(set([
        impact.strip() for impact in impacts 
        if impact and impact.strip()
    ]))
    
    # Clean purpose
    sanitized['purpose'] = requirements.get('purpose', '').strip()
    
    # Clean additional info
    additional = requirements.get('additional_info', '').strip()
    sanitized['additional_info'] = additional if additional else 'None provided'
    
    # Preserve other fields
    for key in ['timestamp', 'status']:
        if key in requirements:
            sanitized[key] = requirements[key]
    
    return sanitized

