#!/usr/bin/env python3
"""
Full Permission OSINT Launcher
Uses all available Termux APIs
"""
import subprocess
import json
from datetime import datetime

class FullPermissionOSINT:
    def __init__(self):
        self.verify_permissions()
    
    def verify_permissions(self):
        """Verify all permissions are working"""
        print("🔐 Verifying permissions...")
        
        # Test critical permissions
        try:
            subprocess.run(['termux-notification', '--title', 'OSINT Ready', '--content', 'All systems operational'])
            subprocess.run(['termux-vibrate', '-d', '200'])
            print("✅ Core permissions working")
        except:
            print("❌ Core permissions need setup")
    
    def get_device_context(self):
        """Get full device context for OSINT"""
        context = {
            'timestamp': datetime.now().isoformat()
        }
        
        # Battery
        try:
            result = subprocess.run(['termux-battery-status'], capture_output=True, text=True)
            context['battery'] = json.loads(result.stdout)
        except:
            context['battery'] = 'unavailable'
        
        # Location
        try:
            result = subprocess.run(['termux-location', '-p', 'network', '-r', 'once'], 
                                  capture_output=True, text=True, timeout=10)
            context['location'] = json.loads(result.stdout)
        except:
            context['location'] = 'unavailable'
        
        # WiFi
        try:
            result = subprocess.run(['termux-wifi-connectioninfo'], capture_output=True, text=True)
            context['wifi'] = json.loads(result.stdout)
        except:
            context['wifi'] = 'unavailable'
        
        # Telephony
        try:
            result = subprocess.run(['termux-telephony-deviceinfo'], capture_output=True, text=True)
            context['telephony'] = json.loads(result.stdout)
        except:
            context['telephony'] = 'unavailable'
        
        return context
    
    def launch_comprehensive_osint(self, target):
        """Launch OSINT with full device context"""
        context = self.get_device_context()
        
        subprocess.run(['termux-notification', 
                       '--title', 'OSINT Started', 
                       '--content', f'Analyzing {target} with full context'])
        
        print(f"🎯 Target: {target}")
        print(f"📱 Device Context: {json.dumps(context, indent=2)}")
        
        # Launch all tools with context
        tools = [
            'tools/phone_validator.py',
            'tools/email_domain_osint.py',
            'tools/username_osint.py', 
            'tools/ip_network_osint.py'
        ]
        
        for tool in tools:
            print(f"🔧 Running {tool}...")
            try:
                input_data = f"yes\n{target}\n"
                result = subprocess.run(['python', tool], 
                                      input=input_data, 
                                      text=True, 
                                      capture_output=True, 
                                      timeout=60)
                print(f"✅ {tool} completed")
            except Exception as e:
                print(f"❌ {tool} failed: {e}")
        
        subprocess.run(['termux-notification', 
                       '--title', 'OSINT Complete', 
                       '--content', 'All tools finished'])
        subprocess.run(['termux-vibrate', '-d', '1000'])

def main():
    osint = FullPermissionOSINT()
    
    target = input("Enter target for comprehensive OSINT: ")
    osint.launch_comprehensive_osint(target)

if __name__ == "__main__":
    main()
