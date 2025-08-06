#!/usr/bin/env python3
"""
IP Address and Network OSINT Tool
Educational and authorized use only
"""
import requests
import json
import socket
import subprocess
from datetime import datetime
import ipaddress

class IPNetworkOSINT:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def validate_ip(self, ip_str: str) -> dict:
        """Validate and classify IP address"""
        try:
            ip = ipaddress.ip_address(ip_str)
            return {
                'ip': str(ip),
                'is_valid': True,
                'version': ip.version,
                'is_private': ip.is_private,
                'is_global': ip.is_global,
                'is_multicast': ip.is_multicast,
                'is_reserved': ip.is_reserved,
                'is_loopback': ip.is_loopback,
                'is_link_local': ip.is_link_local
            }
        except ValueError:
            return {
                'ip': ip_str,
                'is_valid': False,
                'error': 'Invalid IP address format'
            }
    
    def get_geolocation(self, ip: str) -> dict:
        """Get IP geolocation information"""
        try:
            # Using free ipapi.co service
            response = self.session.get(f"https://ipapi.co/{ip}/json/", timeout=10)
            if response.status_code == 200:
                data = response.json()
                return {
                    'country': data.get('country_name'),
                    'country_code': data.get('country_code'),
                    'region': data.get('region'),
                    'city': data.get('city'),
                    'postal': data.get('postal'),
                    'latitude': data.get('latitude'),
                    'longitude': data.get('longitude'),
                    'timezone': data.get('timezone'),
                    'isp': data.get('org'),
                    'asn': data.get('asn'),
                    'source': 'ipapi.co'
                }
        except Exception as e:
            pass
        
        # Fallback to ip-api.com
        try:
            response = self.session.get(f"http://ip-api.com/json/{ip}", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    return {
                        'country': data.get('country'),
                        'country_code': data.get('countryCode'),
                        'region': data.get('regionName'),
                        'city': data.get('city'),
                        'postal': data.get('zip'),
                        'latitude': data.get('lat'),
                        'longitude': data.get('lon'),
                        'timezone': data.get('timezone'),
                        'isp': data.get('isp'),
                        'asn': data.get('as'),
                        'source': 'ip-api.com'
                    }
        except Exception as e:
            pass
        
        return {'error': 'Geolocation lookup failed'}
    
    def get_whois_info(self, ip: str) -> dict:
        """Get WHOIS information for IP"""
        try:
            # Using whois command if available
            result = subprocess.run(['whois', ip], capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                whois_data = result.stdout
                
                # Parse key information
                parsed = {
                    'raw_whois': whois_data,
                    'organization': self.extract_whois_field(whois_data, ['OrgName', 'org-name', 'organization']),
                    'network_range': self.extract_whois_field(whois_data, ['NetRange', 'inetnum', 'route']),
                    'country': self.extract_whois_field(whois_data, ['Country', 'country']),
                    'admin_contact': self.extract_whois_field(whois_data, ['OrgAbuseEmail', 'abuse-mailbox']),
                    'creation_date': self.extract_whois_field(whois_data, ['RegDate', 'created']),
                    'last_updated': self.extract_whois_field(whois_data, ['Updated', 'last-modified'])
                }
                
                return parsed
        except Exception as e:
            return {'error': f'WHOIS lookup failed: {e}'}
        
        return {'error': 'WHOIS command not available'}
    
    def extract_whois_field(self, whois_text: str, field_names: list) -> str:
        """Extract specific field from WHOIS text"""
        lines = whois_text.split('\n')
        for line in lines:
            for field_name in field_names:
                if line.strip().lower().startswith(field_name.lower() + ':'):
                    return line.split(':', 1)[1].strip()
        return 'Not found'
    
    def check_reputation(self, ip: str) -> dict:
        """Check IP reputation (using public APIs)"""
        reputation = {
            'is_malicious': False,
            'threat_types': [],
            'reputation_score': 0,
            'sources_checked': []
        }
        
        # Note: This would integrate with threat intelligence APIs
        # For demo purposes, showing structure
        print(f"[INFO] Checking reputation for {ip}")
        print("[INFO] This requires API keys for threat intelligence services")
        
        return reputation
    
    def port_scan_common(self, ip: str) -> dict:
        """Scan common ports (ethical scanning only)"""
        common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995]
        open_ports = []
        
        print(f"[INFO] Scanning common ports on {ip}")
        print("[WARNING] Only scan IPs you own or have permission to test")
        
        for port in common_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                result = sock.connect_ex((ip, port))
                if result == 0:
                    open_ports.append(port)
                sock.close()
            except:
                pass
        
        return {
            'scanned_ports': common_ports,
            'open_ports': open_ports,
            'total_open': len(open_ports),
            'warning': 'Only scan authorized targets'
        }
    
    def reverse_dns_lookup(self, ip: str) -> dict:
        """Perform reverse DNS lookup"""
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            return {
                'hostname': hostname,
                'has_reverse_dns': True
            }
        except socket.herror:
            return {
                'hostname': None,
                'has_reverse_dns': False
            }
    
    def check_tor_exit_node(self, ip: str) -> dict:
        """Check if IP is a Tor exit node"""
        try:
            # Check against public Tor exit node list
            response = self.session.get("https://check.torproject.org/torbulkexitlist", timeout=10)
            if response.status_code == 200:
                tor_ips = response.text.split('\n')
                is_tor = ip in tor_ips
                return {
                    'is_tor_exit': is_tor,
                    'source': 'torproject.org'
                }
        except:
            pass
        
        return {
            'is_tor_exit': 'Unknown',
            'error': 'Could not check Tor exit list'
        }
    
    def check_vpn_proxy(self, ip: str) -> dict:
        """Check if IP belongs to VPN/Proxy service"""
        # This would typically use commercial APIs
        return {
            'is_vpn': 'Unknown - requires commercial API',
            'is_proxy': 'Unknown - requires commercial API',
            'vpn_provider': 'Unknown',
            'recommendation': 'Use services like IPQualityScore or similar'
        }
    
    def generate_ip_report(self, ip: str) -> dict:
        """Generate comprehensive IP OSINT report"""
        print(f"\n{'='*60}")
        print(f"IP ADDRESS & NETWORK OSINT REPORT")
        print(f"{'='*60}")
        print(f"Target: {ip}")
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")
        
        # IP validation
        ip_validation = self.validate_ip(ip)
        
        if not ip_validation['is_valid']:
            print(f"❌ Invalid IP address: {ip}")
            return {'error': 'Invalid IP address'}
        
        # Gather information
        geolocation = self.get_geolocation(ip)
        whois_info = self.get_whois_info(ip)
        reputation = self.check_reputation(ip)
        reverse_dns = self.reverse_dns_lookup(ip)
        tor_check = self.check_tor_exit_node(ip)
        vpn_check = self.check_vpn_proxy(ip)
        
        # Port scan only if explicitly authorized
        port_scan = None
        scan_consent = input(f"\nDo you have permission to port scan {ip}? (yes/no): ")
        if scan_consent.lower() == 'yes':
            port_scan = self.port_scan_common(ip)
        
        report = {
            'target': ip,
            'timestamp': datetime.now().isoformat(),
            'ip_validation': ip_validation,
            'geolocation': geolocation,
            'whois_info': whois_info,
            'reputation': reputation,
            'reverse_dns': reverse_dns,
            'tor_check': tor_check,
            'vpn_check': vpn_check,
            'port_scan': port_scan
        }
        
        self.display_ip_report(report)
        return report
    
    def display_ip_report(self, report):
        """Display formatted IP report"""
        validation = report['ip_validation']
        geo = report['geolocation']
        
        print(f"\n🌐 IP ADDRESS INFO:")
        print(f"   IP: {validation['ip']}")
        print(f"   Version: IPv{validation['version']}")
        print(f"   Private: {validation['is_private']}")
        print(f"   Global: {validation['is_global']}")
        
        if not geo.get('error'):
            print(f"\n📍 GEOLOCATION:")
            print(f"   Country: {geo.get('country', 'Unknown')}")
            print(f"   Region: {geo.get('region', 'Unknown')}")
            print(f"   City: {geo.get('city', 'Unknown')}")
            print(f"   ISP: {geo.get('isp', 'Unknown')}")
            print(f"   ASN: {geo.get('asn', 'Unknown')}")
        
        reverse_dns = report['reverse_dns']
        print(f"\n🔍 REVERSE DNS:")
        print(f"   Hostname: {reverse_dns.get('hostname', 'None')}")
        print(f"   Has rDNS: {reverse_dns['has_reverse_dns']}")
        
        tor_check = report['tor_check']
        print(f"\n🧅 TOR CHECK:")
        print(f"   Tor Exit Node: {tor_check['is_tor_exit']}")
        
        if report['port_scan']:
            port_scan = report['port_scan']
            print(f"\n🔌 PORT SCAN:")
            print(f"   Open Ports: {port_scan['open_ports']}")
            print(f"   Total Open: {port_scan['total_open']}")

def main():
    print("IP Address & Network OSINT Tool")
    print("Educational and authorized use only!")
    
    consent = input("\nDo you have permission to analyze this IP address? (yes/no): ")
    if consent.lower() != 'yes':
        print("Exiting - proper authorization required")
        return
    
    ip = input("Enter IP address: ")
    
    osint = IPNetworkOSINT()
    report = osint.generate_ip_report(ip)
    
    if 'error' not in report:
        # Save report
        filename = f"ip_report_{ip.replace('.', '_')}.json"
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"\nReport saved to {filename}")

if __name__ == "__main__":
    main()
