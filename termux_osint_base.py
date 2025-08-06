#!/usr/bin/env python3
"""
Termux-Enhanced OSINT Base Class
Provides Termux API integration for all OSINT tools
"""
import json
import subprocess
import os
from datetime import datetime

class TermuxOSINTBase:
    def __init__(self):
        self.termux_apis = self.load_termux_config()
        self.session_id = f"osint_{int(datetime.now().timestamp())}"
    
    def load_termux_config(self):
        """Load Termux API configuration"""
        try:
            with open('config/termux_api_config.json', 'r') as f:
                config = json.load(f)
                return config.get('available_apis', {})
        except:
            return {}
    
    def notify(self, title, message, priority='normal'):
        """Send Android notification"""
        if 'notification' in self.termux_apis:
            try:
                cmd = ['termux-notification', '--title', title, '--content', message]
                if priority == 'high':
                    cmd.extend(['--priority', 'high'])
                subprocess.run(cmd)
            except:
                pass
        print(f"📱 {title}: {message}")
    
    def vibrate(self, duration=500):
        """Vibrate device"""
        if 'vibrate' in self.termux_apis:
            try:
                subprocess.run(['termux-vibrate', '-d', str(duration)])
            except:
                pass
    
    def toast(self, message):
        """Show toast message"""
        if 'toast' in self.termux_apis:
            try:
                subprocess.run(['termux-toast', message])
            except:
                pass
        print(f"🍞 {message}")
    
    def speak(self, text):
        """Text-to-speech"""
        if 'tts' in self.termux_apis:
            try:
                subprocess.run(['termux-tts-speak', text])
            except:
                pass
    
    def get_clipboard(self):
        """Get clipboard content"""
        if 'clipboard_get' in self.termux_apis:
            try:
                result = subprocess.run(['termux-clipboard-get'], 
                                      capture_output=True, text=True)
                return result.stdout.strip()
            except:
                pass
        return None
    
    def set_clipboard(self, content):
        """Set clipboard content"""
        if 'clipboard_set' in self.termux_apis:
            try:
                subprocess.run(['termux-clipboard-set', content], 
                              input=content, text=True)
            except:
                pass
    
    def get_location(self):
        """Get device location"""
        if 'location' in self.termux_apis:
            try:
                result = subprocess.run(['termux-location', '-p', 'network'], 
                                      capture_output=True, text=True, timeout=10)
                return json.loads(result.stdout)
            except:
                pass
        return None
    
    def get_wifi_info(self):
        """Get WiFi information"""
        if 'wifi' in self.termux_apis:
            try:
                result = subprocess.run(['termux-wifi-connectioninfo'], 
                                      capture_output=True, text=True)
                return json.loads(result.stdout)
            except:
                pass
        return None
    
    def scan_wifi(self):
        """Scan for WiFi networks"""
        if 'wifi_scan' in self.termux_apis:
            try:
                result = subprocess.run(['termux-wifi-scaninfo'], 
                                      capture_output=True, text=True)
                return json.loads(result.stdout)
            except:
                pass
        return None
    
    def get_battery_info(self):
        """Get battery information"""
        if 'battery' in self.termux_apis:
            try:
                result = subprocess.run(['termux-battery-status'], 
                                      capture_output=True, text=True)
                return json.loads(result.stdout)
            except:
                pass
        return None
    
    def log_osint_activity(self, tool_name, target, action):
        """Log OSINT activity with device context"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'session_id': self.session_id,
            'tool': tool_name,
            'target': self.anonymize_target(target),
            'action': action,
            'device_context': {
                'battery': self.get_battery_info(),
                'wifi': self.get_wifi_info(),
                'location': self.get_location()
            }
        }
        
        # Save to log file
        os.makedirs('logs', exist_ok=True)
        with open('logs/termux_osint_activity.log', 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def anonymize_target(self, target):
        """Anonymize target for logging"""
        if not target:
            return "unknown"
        if len(target) <= 4:
            return "***"
        return f"{target[:2]}***{target[-2:]}"
    
    def enhanced_consent_check(self, tool_name, target):
        """Enhanced consent check with Termux integration"""
        self.notify("OSINT Tool", f"Authorization required for {tool_name}")
        self.vibrate(300)
        
        print(f"\n{'='*50}")
        print(f"🔒 AUTHORIZATION REQUIRED")
        print(f"{'='*50}")
        print(f"Tool: {tool_name}")
        print(f"Target: {target}")
        print(f"Device: {self.get_battery_info()}")
        print(f"{'='*50}")
        
        consent = input("Do you have explicit permission to analyze this target? (yes/no): ")
        
        if consent.lower() == 'yes':
            self.notify("OSINT Authorized", f"Starting {tool_name}")
            self.vibrate(100)
            self.log_osint_activity(tool_name, target, "authorized")
            return True
        else:
            self.notify("OSINT Cancelled", "Authorization denied")
            self.vibrate(1000)
            self.log_osint_activity(tool_name, target, "denied")
            return False
    
    def save_enhanced_report(self, tool_name, target, results):
        """Save report with device context"""
        report = {
            'tool': tool_name,
            'target': target,
            'timestamp': datetime.now().isoformat(),
            'session_id': self.session_id,
            'results': results,
            'device_context': {
                'battery': self.get_battery_info(),
                'wifi': self.get_wifi_info(),
                'termux_apis': list(self.termux_apis.keys())
            }
        }
        
        filename = f"reports/enhanced_{tool_name.lower().replace(' ', '_')}_{int(datetime.now().timestamp())}.json"
        os.makedirs('reports', exist_ok=True)
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        self.notify("Report Saved", f"{tool_name} results saved")
        self.set_clipboard(filename)  # Copy filename to clipboard
        
        return filename
