#!/usr/bin/env python3
"""
Email and Domain OSINT Tool
Educational and authorized use only
"""
import re
import requests
import whois
import dns.resolver
import json
from datetime import datetime

class EmailDomainOSINT:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def validate_email(self, email: str) -> dict:
        """Validate email format and extract components"""
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        result = {
            'email': email,
            'is_valid_format': bool(re.match(email_regex, email)),
            'local_part': None,
            'domain': None,
            'tld': None
        }
        
        if result['is_valid_format']:
            local, domain = email.split('@')
            result['local_part'] = local
            result['domain'] = domain
            result['tld'] = domain.split('.')[-1]
        
        return result
    
    def analyze_domain(self, domain: str) -> dict:
        """Comprehensive domain analysis"""
        analysis = {
            'domain': domain,
            'whois_info': self.get_whois_info(domain),
            'dns_records': self.get_dns_records(domain),
            'mx_records': self.get_mx_records(domain),
            'subdomains': self.find_common_subdomains(domain),
            'security_headers': self.check_security_headers(domain)
        }
        
        return analysis
    
    def get_whois_info(self, domain: str) -> dict:
        """Get WHOIS information"""
        try:
            w = whois.whois(domain)
            return {
                'registrar': str(w.registrar) if w.registrar else None,
                'creation_date': str(w.creation_date) if w.creation_date else None,
                'expiration_date': str(w.expiration_date) if w.expiration_date else None,
                'name_servers': w.name_servers if w.name_servers else [],
                'country': str(w.country) if w.country else None,
                'organization': str(w.org) if w.org else None
            }
        except Exception as e:
            return {'error': f"WHOIS lookup failed: {e}"}
    
    def get_dns_records(self, domain: str) -> dict:
        """Get DNS records"""
        records = {}
        record_types = ['A', 'AAAA', 'CNAME', 'TXT', 'NS']
        
        for record_type in record_types:
            try:
                answers = dns.resolver.resolve(domain, record_type)
                records[record_type] = [str(rdata) for rdata in answers]
            except:
                records[record_type] = []
        
        return records
    
    def get_mx_records(self, domain: str) -> list:
        """Get MX records for email servers"""
        try:
            mx_records = dns.resolver.resolve(domain, 'MX')
            return [{'priority': mx.preference, 'server': str(mx.exchange)} for mx in mx_records]
        except:
            return []
    
    def find_common_subdomains(self, domain: str) -> list:
        """Check for common subdomains"""
        common_subs = ['www', 'mail', 'ftp', 'admin', 'api', 'blog', 'dev', 'test', 'staging']
        found_subdomains = []
        
        for sub in common_subs:
            try:
                subdomain = f"{sub}.{domain}"
                dns.resolver.resolve(subdomain, 'A')
                found_subdomains.append(subdomain)
            except:
                pass
        
        return found_subdomains
    
    def check_security_headers(self, domain: str) -> dict:
        """Check security headers"""
        try:
            response = self.session.get(f"https://{domain}", timeout=10)
            headers = response.headers
            
            security_headers = {
                'strict_transport_security': headers.get('Strict-Transport-Security'),
                'content_security_policy': headers.get('Content-Security-Policy'),
                'x_frame_options': headers.get('X-Frame-Options'),
                'x_content_type_options': headers.get('X-Content-Type-Options'),
                'referrer_policy': headers.get('Referrer-Policy')
            }
            
            return security_headers
        except:
            return {'error': 'Could not check security headers'}
    
    def check_email_breach(self, email: str) -> dict:
        """Check if email appears in known breaches (ethical APIs only)"""
        # Note: This would integrate with services like HaveIBeenPwned
        # Requires proper API key and user consent
        return {
            'breach_check': 'Requires API access to breach databases',
            'recommendation': 'Use official services like HaveIBeenPwned.com'
        }
    
    def social_media_email_search(self, email: str) -> dict:
        """Search for email in social media (public info only)"""
        return {
            'platforms_checked': ['Public directories only'],
            'found_profiles': 'Requires specific platform APIs',
            'privacy_note': 'Most platforms protect email privacy'
        }
    
    def generate_email_report(self, email: str) -> dict:
        """Generate comprehensive email OSINT report"""
        print(f"\n{'='*60}")
        print(f"EMAIL & DOMAIN OSINT REPORT")
        print(f"{'='*60}")
        print(f"Target: {email}")
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")
        
        # Email validation
        email_validation = self.validate_email(email)
        
        report = {
            'target': email,
            'timestamp': datetime.now().isoformat(),
            'email_validation': email_validation,
            'domain_analysis': None,
            'breach_check': self.check_email_breach(email),
            'social_search': self.social_media_email_search(email)
        }
        
        # Domain analysis if email is valid
        if email_validation['is_valid_format']:
            domain = email_validation['domain']
            report['domain_analysis'] = self.analyze_domain(domain)
        
        self.display_email_report(report)
        return report
    
    def display_email_report(self, report):
        """Display formatted email report"""
        validation = report['email_validation']
        
        print(f"\n📧 EMAIL VALIDATION:")
        print(f"   Valid Format: {validation['is_valid_format']}")
        print(f"   Local Part: {validation['local_part']}")
        print(f"   Domain: {validation['domain']}")
        print(f"   TLD: {validation['tld']}")
        
        if report['domain_analysis']:
            domain_analysis = report['domain_analysis']
            whois_info = domain_analysis['whois_info']
            
            print(f"\n🌐 DOMAIN ANALYSIS:")
            print(f"   Registrar: {whois_info.get('registrar', 'Unknown')}")
            print(f"   Creation Date: {whois_info.get('creation_date', 'Unknown')}")
            print(f"   Country: {whois_info.get('country', 'Unknown')}")
            print(f"   MX Records: {len(domain_analysis['mx_records'])} found")
            print(f"   Subdomains: {domain_analysis['subdomains']}")

def main():
    print("Email & Domain OSINT Tool")
    print("Educational and authorized use only!")
    
    consent = input("\nDo you have permission to analyze this email/domain? (yes/no): ")
    if consent.lower() != 'yes':
        print("Exiting - proper authorization required")
        return
    
    target = input("Enter email address or domain: ")
    
    osint = EmailDomainOSINT()
    
    if '@' in target:
        report = osint.generate_email_report(target)
        filename = f"email_report_{target.replace('@', '_at_').replace('.', '_')}.json"
    else:
        report = osint.analyze_domain(target)
        filename = f"domain_report_{target.replace('.', '_')}.json"
    
    # Save report
    with open(filename, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"\nReport saved to {filename}")

if __name__ == "__main__":
    main()
