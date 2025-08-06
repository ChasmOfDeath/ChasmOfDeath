#!/usr/bin/env python3
"""
Advanced Phone Number OSINT
Educational and authorized use only
"""
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import requests
import json
import re
from datetime import datetime

class AdvancedPhoneOSINT:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def analyze_phone_number(self, phone_str: str) -> dict:
        """Comprehensive phone number analysis"""
        try:
            # Parse phone number
            phone = phonenumbers.parse(phone_str, None)
            
            analysis = {
                'number': phone_str,
                'is_valid': phonenumbers.is_valid_number(phone),
                'is_possible': phonenumbers.is_possible_number(phone),
                'country_code': phone.country_code,
                'national_number': phone.national_number,
                'international_format': phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
                'national_format': phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.NATIONAL),
                'e164_format': phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.E164),
                'location': geocoder.description_for_number(phone, "en"),
                'carrier': carrier.name_for_number(phone, "en"),
                'timezones': timezone.time_zones_for_number(phone),
                'number_type': self.get_number_type(phone),
                'line_type': self.determine_line_type(phone)
            }
            
            return analysis
            
        except Exception as e:
            return {'error': f"Phone analysis failed: {e}"}
    
    def get_number_type(self, phone):
        """Determine phone number type"""
        number_type = phonenumbers.number_type(phone)
        types = {
            0: "FIXED_LINE",
            1: "MOBILE", 
            2: "FIXED_LINE_OR_MOBILE",
            3: "TOLL_FREE",
            4: "PREMIUM_RATE",
            5: "SHARED_COST",
            6: "VOIP",
            7: "PERSONAL_NUMBER",
            8: "PAGER",
            9: "UAN",
            10: "VOICEMAIL",
            99: "UNKNOWN"
        }
        return types.get(number_type, "UNKNOWN")
    
    def determine_line_type(self, phone):
        """Advanced line type detection"""
        carrier_name = carrier.name_for_number(phone, "en").lower()
        
        if any(keyword in carrier_name for keyword in ['mobile', 'wireless', 'cellular']):
            return "MOBILE"
        elif any(keyword in carrier_name for keyword in ['landline', 'fixed', 'wire']):
            return "LANDLINE"
        elif any(keyword in carrier_name for keyword in ['voip', 'internet', 'digital']):
            return "VOIP"
        else:
            return "UNKNOWN"
    
    def check_spam_databases(self, phone: str) -> dict:
        """Check against known spam databases (public APIs only)"""
        results = {
            'spam_score': 0,
            'reports': [],
            'databases_checked': []
        }
        
        # Note: This would integrate with public spam databases
        # For demo purposes, showing structure
        print(f"[INFO] Checking spam databases for {phone}")
        print("[INFO] This requires API keys for spam detection services")
        
        return results
    
    def social_media_footprint(self, phone: str) -> dict:
        """Check social media presence (public info only)"""
        footprint = {
            'platforms_found': [],
            'public_profiles': [],
            'associated_usernames': []
        }
        
        # WhatsApp presence check (limited)
        footprint['whatsapp'] = self.check_whatsapp_presence(phone)
        
        # Telegram check
        footprint['telegram'] = self.check_telegram_phone(phone)
        
        return footprint
    
    def check_whatsapp_presence(self, phone: str) -> dict:
        """Check WhatsApp presence (ethical methods only)"""
        return {
            'has_whatsapp': "Unknown - requires proper API access",
            'last_seen': "Not available",
            'profile_info': "Requires authorization"
        }
    
    def check_telegram_phone(self, phone: str) -> dict:
        """Check Telegram association"""
        return {
            'has_telegram': "Unknown - phone privacy protected",
            'username': "Not publicly available",
            'method': "Respects privacy settings"
        }
    
    def generate_comprehensive_report(self, phone: str) -> dict:
        """Generate detailed OSINT report"""
        print(f"\n{'='*60}")
        print(f"COMPREHENSIVE PHONE OSINT REPORT")
        print(f"{'='*60}")
        print(f"Target: {phone}")
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")
        
        # Phone analysis
        phone_analysis = self.analyze_phone_number(phone)
        
        # Spam check
        spam_check = self.check_spam_databases(phone)
        
        # Social media footprint
        social_footprint = self.social_media_footprint(phone)
        
        report = {
            'target': phone,
            'timestamp': datetime.now().isoformat(),
            'phone_analysis': phone_analysis,
            'spam_analysis': spam_check,
            'social_footprint': social_footprint,
            'risk_assessment': self.assess_risk(phone_analysis, spam_check)
        }
        
        # Display formatted results
        self.display_report(report)
        
        return report
    
    def assess_risk(self, phone_analysis, spam_check) -> dict:
        """Assess potential security risks"""
        risk_factors = []
        risk_score = 0
        
        if phone_analysis.get('number_type') == 'VOIP':
            risk_factors.append("VOIP number - easier to spoof")
            risk_score += 2
        
        if spam_check.get('spam_score', 0) > 5:
            risk_factors.append("High spam score")
            risk_score += 3
        
        if not phone_analysis.get('is_valid'):
            risk_factors.append("Invalid number format")
            risk_score += 1
        
        return {
            'risk_score': risk_score,
            'risk_level': 'HIGH' if risk_score >= 5 else 'MEDIUM' if risk_score >= 2 else 'LOW',
            'risk_factors': risk_factors
        }
    
    def display_report(self, report):
        """Display formatted report"""
        phone_analysis = report['phone_analysis']
        
        print(f"\n📱 PHONE NUMBER ANALYSIS:")
        print(f"   Valid: {phone_analysis.get('is_valid', 'Unknown')}")
        print(f"   Country: {phone_analysis.get('location', 'Unknown')}")
        print(f"   Carrier: {phone_analysis.get('carrier', 'Unknown')}")
        print(f"   Type: {phone_analysis.get('number_type', 'Unknown')}")
        print(f"   Line Type: {phone_analysis.get('line_type', 'Unknown')}")
        print(f"   Timezones: {phone_analysis.get('timezones', [])}")
        
        print(f"\n🛡️ SECURITY ASSESSMENT:")
        risk = report['risk_assessment']
        print(f"   Risk Level: {risk['risk_level']}")
        print(f"   Risk Score: {risk['risk_score']}/10")
        print(f"   Risk Factors: {risk['risk_factors']}")
        
        print(f"\n🌐 SOCIAL MEDIA FOOTPRINT:")
        social = report['social_footprint']
        print(f"   WhatsApp: {social['whatsapp']['has_whatsapp']}")
        print(f"   Telegram: {social['telegram']['has_telegram']}")

def main():
    print("Advanced Phone OSINT Tool")
    print("Educational and authorized use only!")
    
    consent = input("\nDo you have explicit permission to analyze this number? (yes/no): ")
    if consent.lower() != 'yes':
        print("Exiting - proper authorization required")
        return
    
    phone = input("Enter phone number (with country code): ")
    
    osint = AdvancedPhoneOSINT()
    report = osint.generate_comprehensive_report(phone)
    
    # Save detailed report
    filename = f"advanced_report_{phone.replace('+', '').replace(' ', '').replace('-', '')}.json"
    with open(filename, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"\nDetailed report saved to {filename}")

if __name__ == "__main__":
    main()
