#!/usr/bin/env python3
"""
Username OSINT Tool
Educational and authorized use only
"""
import requests
import json
from datetime import datetime
import time

class UsernameOSINT:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Platform endpoints for username checking
        self.platforms = {
            'github': 'https://github.com/{}',
            'twitter': 'https://twitter.com/{}',
            'instagram': 'https://instagram.com/{}',
            'reddit': 'https://reddit.com/user/{}',
            'telegram': 'https://t.me/{}',
            'youtube': 'https://youtube.com/@{}',
            'tiktok': 'https://tiktok.com/@{}',
            'linkedin': 'https://linkedin.com/in/{}',
            'facebook': 'https://facebook.com/{}',
            'discord': 'Discord usernames not publicly searchable',
            'snapchat': 'https://snapchat.com/add/{}',
            'pinterest': 'https://pinterest.com/{}',
            'tumblr': 'https://{}.tumblr.com',
            'medium': 'https://medium.com/@{}',
            'twitch': 'https://twitch.tv/{}',
            'spotify': 'https://open.spotify.com/user/{}',
            'soundcloud': 'https://soundcloud.com/{}',
            'vimeo': 'https://vimeo.com/{}',
            'behance': 'https://behance.net/{}',
            'dribbble': 'https://dribbble.com/{}',
            'deviantart': 'https://{}.deviantart.com',
            'flickr': 'https://flickr.com/people/{}',
            'goodreads': 'https://goodreads.com/{}',
            'keybase': 'https://keybase.io/{}',
            'pastebin': 'https://pastebin.com/u/{}',
            'hackernews': 'https://news.ycombinator.com/user?id={}',
            'about.me': 'https://about.me/{}',
            'gravatar': 'https://gravatar.com/{}',
            'foursquare': 'https://foursquare.com/{}',
            'slideshare': 'https://slideshare.net/{}',
            'scribd': 'https://scribd.com/{}',
            'badoo': 'https://badoo.com/profile/{}',
            'last.fm': 'https://last.fm/user/{}',
            'cash.app': 'https://cash.app/${}',
            'venmo': 'https://venmo.com/{}',
            'patreon': 'https://patreon.com/{}',
            'onlyfans': 'https://onlyfans.com/{}',
            'linktree': 'https://linktr.ee/{}',
            'clubhouse': 'Clubhouse usernames not publicly searchable',
            'signal': 'Signal usernames not publicly searchable',
            'whatsapp': 'WhatsApp usernames not publicly searchable'
        }
    
    def check_username_availability(self, username: str) -> dict:
        """Check username across multiple platforms"""
        results = {
            'username': username,
            'timestamp': datetime.now().isoformat(),
            'platforms_checked': 0,
            'found_profiles': [],
            'not_found': [],
            'errors': [],
            'rate_limited': []
        }
        
        print(f"\n🔍 Checking username '{username}' across platforms...")
        print("Note: This checks public availability only")
        
        for platform, url_template in self.platforms.items():
            if isinstance(url_template, str) and '{}' in url_template:
                url = url_template.format(username)
                status = self.check_url_exists(url, platform)
                
                results['platforms_checked'] += 1
                
                if status == 'found':
                    results['found_profiles'].append({
                        'platform': platform,
                        'url': url,
                        'status': 'Profile exists'
                    })
                    print(f"   ✓ {platform}: {url}")
                elif status == 'not_found':
                    results['not_found'].append(platform)
                elif status == 'error':
                    results['errors'].append(platform)
                elif status == 'rate_limited':
                    results['rate_limited'].append(platform)
                
                # Rate limiting to be respectful
                time.sleep(0.5)
            else:
                results['not_found'].append(f"{platform}: {url_template}")
        
        return results
    
    def check_url_exists(self, url: str, platform: str) -> str:
        """Check if URL exists and profile is active"""
        try:
            response = self.session.get(url, timeout=10, allow_redirects=True)
            
            # Platform-specific checks
            if platform == 'github':
                if response.status_code == 200 and 'Not Found' not in response.text:
                    return 'found'
            elif platform == 'twitter':
                if response.status_code == 200 and 'This account doesn\'t exist' not in response.text:
                    return 'found'
            elif platform == 'instagram':
                if response.status_code == 200 and 'Sorry, this page isn\'t available' not in response.text:
                    return 'found'
            elif platform == 'reddit':
                if response.status_code == 200 and 'page not found' not in response.text.lower():
                    return 'found'
            elif platform == 'telegram':
                if response.status_code == 200 and 'If you have <strong>Telegram</strong>' in response.text:
                    return 'found'
            else:
                # Generic check
                if response.status_code == 200:
                    return 'found'
            
            if response.status_code == 429:
                return 'rate_limited'
            
            return 'not_found'
            
        except requests.exceptions.Timeout:
            return 'error'
        except requests.exceptions.RequestException:
            return 'error'
    
    def analyze_username_patterns(self, username: str) -> dict:
        """Analyze username for patterns and variations"""
        analysis = {
            'length': len(username),
            'has_numbers': any(c.isdigit() for c in username),
            'has_special_chars': any(not c.isalnum() for c in username),
            'is_all_lowercase': username.islower(),
            'is_all_uppercase': username.isupper(),
            'common_variations': self.generate_variations(username),
            'security_assessment': self.assess_username_security(username)
        }
        
        return analysis
    
    def generate_variations(self, username: str) -> list:
        """Generate common username variations"""
        variations = []
        
        # Common variations
        variations.extend([
            username + '1',
            username + '123',
            username + '2024',
            username + '_',
            '_' + username,
            username.replace('_', ''),
            username.replace('.', ''),
            username + 'official',
            'real' + username,
            username + 'real'
        ])
        
        # Case variations
        variations.extend([
            username.lower(),
            username.upper(),
            username.capitalize()
        ])
        
        return list(set(variations))[:10]  # Limit to 10 variations
    
    def assess_username_security(self, username: str) -> dict:
        """Assess username from security perspective"""
        issues = []
        score = 10
        
        if len(username) < 6:
            issues.append("Username too short")
            score -= 2
        
        if username.lower() in ['admin', 'root', 'user', 'test', 'guest']:
            issues.append("Common/predictable username")
            score -= 3
        
        if any(word in username.lower() for word in ['password', 'login', 'account']):
            issues.append("Contains security-related terms")
            score -= 2
        
        if username.isdigit():
            issues.append("Numeric-only username")
            score -= 1
        
        return {
            'security_score': max(0, score),
            'issues': issues,
            'recommendation': 'Use unique, non-predictable usernames' if issues else 'Username appears secure'
        }
    
    def generate_report(self, username: str) -> dict:
        """Generate comprehensive username OSINT report"""
        print(f"\n{'='*60}")
        print(f"USERNAME OSINT REPORT")
        print(f"{'='*60}")
        print(f"Target: {username}")
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")
        
        # Check availability
        availability = self.check_username_availability(username)
        
        # Analyze patterns
        patterns = self.analyze_username_patterns(username)
        
        report = {
            'target': username,
            'timestamp': datetime.now().isoformat(),
            'availability_check': availability,
            'pattern_analysis': patterns
        }
        
        self.display_username_report(report)
        return report
    
    def display_username_report(self, report):
        """Display formatted username report"""
        availability = report['availability_check']
        patterns = report['pattern_analysis']
        
        print(f"\n📊 AVAILABILITY SUMMARY:")
        print(f"   Platforms Checked: {availability['platforms_checked']}")
        print(f"   Profiles Found: {len(availability['found_profiles'])}")
        print(f"   Not Found: {len(availability['not_found'])}")
        print(f"   Errors: {len(availability['errors'])}")
        
        if availability['found_profiles']:
            print(f"\n✅ FOUND PROFILES:")
            for profile in availability['found_profiles'][:10]:  # Show first 10
                print(f"   • {profile['platform']}: {profile['url']}")
        
        print(f"\n🔍 PATTERN ANALYSIS:")
        print(f"   Length: {patterns['length']} characters")
        print(f"   Has Numbers: {patterns['has_numbers']}")
        print(f"   Has Special Chars: {patterns['has_special_chars']}")
        print(f"   Security Score: {patterns['security_assessment']['security_score']}/10")
        
        if patterns['security_assessment']['issues']:
            print(f"   Security Issues: {patterns['security_assessment']['issues']}")

def main():
    print("Username OSINT Tool")
    print("Educational and authorized use only!")
    
    consent = input("\nDo you have permission to search for this username? (yes/no): ")
    if consent.lower() != 'yes':
        print("Exiting - proper authorization required")
        return
    
    username = input("Enter username to search: ")
    
    osint = UsernameOSINT()
    report = osint.generate_report(username)
    
    # Save report
    filename = f"username_report_{username}.json"
    with open(filename, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"\nReport saved to {filename}")

if __name__ == "__main__":
    main()
