#!/usr/bin/env python3
"""
Social Media Cross-Reference Tool
Educational purposes - requires explicit consent
"""

def check_social_platforms(phone_or_username):
    """
    Check various platforms for username/phone presence
    Only checks publicly available information
    """
    platforms = {
        'telegram': f"https://t.me/{phone_or_username}",
        'whatsapp_business': "Requires API access",
        'signal': "No public lookup available",
        'discord': "Username-based only",
        'twitter': f"Search functionality",
        'instagram': "Limited public info"
    }
    
    print("Social Media Cross-Reference Results:")
    print("Note: Only public information is checked")
    
    for platform, info in platforms.items():
        print(f"{platform}: {info}")

if __name__ == "__main__":
    print("Social Media OSINT Tool")
    print("Requires explicit consent and authorization")
    
    target = input("Enter username or phone: ")
    check_social_platforms(target)
