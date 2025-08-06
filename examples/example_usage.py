#!/usr/bin/env python3
"""
Example usage of messaging OSINT tools
Educational demonstration only
"""

from tools.phone_validator import PhoneOSINT

def demo_phone_validation():
    """Demonstrate phone validation features"""
    osint = PhoneOSINT()
    
    # Example with fake number for demo
    demo_numbers = [
        "+1234567890",  # US format
        "+44123456789", # UK format
        "invalid_number"
    ]
    
    for number in demo_numbers:
        print(f"\nTesting: {number}")
        result = osint.validate_phone_format(number)
        print(f"Valid: {result['valid_format']}")
        print(f"Country: {result['possible_countries']}")

if __name__ == "__main__":
    print("OSINT Toolkit Demo")
    print("This is for educational purposes only")
    demo_phone_validation()
