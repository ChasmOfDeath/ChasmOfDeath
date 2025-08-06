#!/usr/bin/env python3
"""
Phone Number Validation and Basic OSINT
Educational purposes only - requires explicit consent
"""
import re
import requests
import json
from typing import Dict, List, Optional

class PhoneOSINT:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def validate_phone_format(self, phone: str) -> Dict:
        """Validate phone number format"""
        # Remove all non-digits
        clean_phone = re.sub(r'\D', '', phone)
        
        results = {
            'original': phone,
            'cleaned': clean_phone,
            'valid_format': False,
            'country_code': None,
            'possible_countries': []
        }
        
        # Basic validation (10-15 digits)
        if 10 <= len(clean_phone) <= 15:
            results['valid_format'] = True
            
            # Common country code detection
            country_codes = {
                '1': ['US', 'CA'],
                '44': ['UK'],
                '49': ['DE'],
                '33': ['FR'],
                '91': ['IN'],
                '86': ['CN'],
                '81': ['JP'],
                '7': ['RU'],
                '55': ['BR'],
                '61': ['AU']
            }
            
            for code, countries in country_codes.items():
                if clean_phone.startswith(code):
                    results['country_code'] = code
                    results['possible_countries'] = countries
                    break
        
        return results
    
    def check_whatsapp_business(self, phone: str) -> Dict:
        """
        Check if number has WhatsApp Business (public info only)
        Note: This uses publicly available business directory info
        """
        results = {
            'has_whatsapp_business': False,
            'business_info': None,
            'method': 'public_directory_check'
        }
        
        # This would require WhatsApp Business API access
        # For educational purposes, showing structure only
        print(f"[INFO] Checking WhatsApp Business status for {phone}")
        print("[INFO] This requires proper API access and authorization")
        
        return results
    
    def check_telegram_username(self, username: str) -> Dict:
        """Check if Telegram username exists (public channels/bots only)"""
        results = {
            'username_exists': False,
            'is_channel': False,
            'is_bot': False,
            'public_info': None
        }
        
        try:
            # Check public Telegram info (t.me links)
            url = f"https://t.me/{username}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                results['username_exists'] = True
                
                # Basic parsing of public info
                if 'telegram-channel' in response.text:
                    results['is_channel'] = True
                if 'telegram-bot' in response.text:
                    results['is_bot'] = True
                    
        except Exception as e:
            print(f"[ERROR] Telegram check failed: {e}")
        
        return results
    
    def generate_report(self, phone: str) -> Dict:
        """Generate comprehensive OSINT report"""
        print(f"\n{'='*50}")
        print(f"MESSAGING APP OSINT REPORT")
        print(f"{'='*50}")
        print(f"Target: {phone}")
        print(f"Timestamp: {json.dumps(None, default=str)}")
        print(f"{'='*50}")
        
        report = {
            'target': phone,
            'phone_validation': self.validate_phone_format(phone),
            'whatsapp_business': self.check_whatsapp_business(phone),
            'telegram_check': None,
            'recommendations': []
        }
        
        # Display results
        validation = report['phone_validation']
        print(f"\n📱 PHONE VALIDATION:")
        print(f"   Format Valid: {validation['valid_format']}")
        print(f"   Country Code: {validation['country_code']}")
        print(f"   Possible Countries: {validation['possible_countries']}")
        
        print(f"\n💬 WHATSAPP BUSINESS:")
        wb = report['whatsapp_business']
        print(f"   Business Account: {wb['has_whatsapp_business']}")
        print(f"   Method: {wb['method']}")
        
        # Add recommendations
        if validation['valid_format']:
            report['recommendations'].append("Phone number format is valid")
        else:
            report['recommendations'].append("Invalid phone number format")
            
        report['recommendations'].append("Always obtain proper authorization")
        report['recommendations'].append("Respect privacy laws and ToS")
        
        return report

def main():
    print("Messaging App OSINT Toolkit")
    print("Educational and authorized use only!")
    
    # Get user consent
    consent = input("\nDo you have explicit permission to test this number? (yes/no): ")
    if consent.lower() != 'yes':
        print("Exiting - proper authorization required")
        return
    
    phone = input("Enter phone number (with country code): ")
    
    osint = PhoneOSINT()
    report = osint.generate_report(phone)
    
    # Save report
    with open(f'report_{phone.replace("+", "").replace(" ", "")}.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\nReport saved to report_{phone.replace('+', '').replace(' ', '')}.json")

if __name__ == "__main__":
    main()
