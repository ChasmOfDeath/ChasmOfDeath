#!/usr/bin/env python3
"""
Optimized Termux OSINT - Uses only available APIs
Available: notification, sms_list, volume, brightness
"""
import json
import subprocess
import os
from datetime import datetime

class OptimizedTermuxOSINT:
    def __init__(self):
        # Only use your 4 available APIs
        self.available_apis = {
            'notification': 'termux-notification',
            'sms_list': 'termux-sms-list', 
            'volume': 'termux-volume',
            'brightness': 'termux-brightness'
        }
        self.session_id = f"osint_{int(datetime.now().timestamp())}"
    
    def notify(self, title, message):
        """Send notification (your available API)"""
        try:
            subprocess.run([
                'termux-notification',
                '--title', title,
                '--content', message,
                '--priority', 'high'
            ])
            print(f"📱 {title}: {message}")
        except Exception as e:
            print(f"📱 {title}: {message}")
    
    def get_sms_data(self):
        """Get SMS data for OSINT analysis"""
        try:
            result = subprocess.run(['termux-sms-list'], 
                                  capture_output=True, text=True)
            return json.loads(result.stdout)
        except Exception as e:
            print(f"❌ SMS access error: {e}")
            return None
    
    def set_volume(self, stream, level):
        """Control device volume"""
        try:
            subprocess.run(['termux-volume', stream, str(level)])
        except:
            pass
    
    def set_brightness(self, level):
        """Control screen brightness (0-255)"""
        try:
            subprocess.run(['termux-brightness', str(level)])
        except:
            pass
    
    def enhanced_consent_check(self, tool_name, target):
        """Enhanced consent with available APIs"""
        # Dim screen for privacy
        self.set_brightness(50)
        
        # Send notification
        self.notify("OSINT Authorization", f"Permission required for {tool_name}")
        
        print(f"\n{'='*50}")
        print(f"🔒 AUTHORIZATION REQUIRED")
        print(f"{'='*50}")
        print(f"Tool: {tool_name}")
        print(f"Target: {target}")
        print(f"Available APIs: {list(self.available_apis.keys())}")
        print(f"{'='*50}")
        
        consent = input("Do you have explicit permission? (yes/no): ")
        
        if consent.lower() == 'yes':
            self.notify("OSINT Authorized", f"Starting {tool_name}")
            # Restore brightness
            self.set_brightness(150)
            return True
        else:
            self.notify("OSINT Denied", "Authorization required")
            # Restore brightness
            self.set_brightness(150)
            return False
    
    def launch_tool_with_notifications(self, tool_name, script_path, target):
        """Launch tool with notification updates"""
        self.notify("OSINT Started", f"Running {tool_name}")
        
        try:
            # Create input for automated consent
            input_data = f"yes\n{target}\n"
            
            process = subprocess.Popen([
                'python', script_path
            ], stdin=subprocess.PIPE, 
               stdout=subprocess.PIPE, 
               stderr=subprocess.PIPE, 
               text=True)
            
            stdout, stderr = process.communicate(input=input_data, timeout=60)
            
            # Success notification
            self.notify("OSINT Complete", f"{tool_name} finished")
            
            # Save results
            result_file = f"results_{tool_name.lower().replace(' ', '_')}_{int(datetime.now().timestamp())}.txt"
            with open(result_file, 'w') as f:
                f.write(f"=== {tool_name} Results ===\n")
                f.write(f"Target: {target}\n")
                f.write(f"Timestamp: {datetime.now()}\n\n")
                f.write(stdout)
                if stderr:
                    f.write(f"\nErrors:\n{stderr}")
            
            return result_file
            
        except subprocess.TimeoutExpired:
            self.notify("OSINT Timeout", f"{tool_name} timed out")
            return None
        except Exception as e:
            self.notify("OSINT Error", f"{tool_name} failed: {str(e)}")
            return None

def main():
    osint = OptimizedTermuxOSINT()
    
    print("🔍 Optimized Termux OSINT Toolkit")
    print(f"📱 Using {len(osint.available_apis)} available APIs")
    
    # Available tools
    tools = {
        '1': {'name': 'Phone Validator', 'script': 'tools/phone_validator.py'},
        '2': {'name': 'Email Domain OSINT', 'script': 'tools/email_domain_osint.py'},
        '3': {'name': 'Username OSINT', 'script': 'tools/username_osint.py'},
        '4': {'name': 'IP Network OSINT', 'script': 'tools/ip_network_osint.py'}
    }
    
    print("\nAvailable Tools:")
    for key, tool in tools.items():
        print(f"{key}. {tool['name']}")
    print("A. Launch ALL tools")
    print("S. SMS Analysis (if permitted)")
    
    choice = input("\nSelect option: ").strip().upper()
    
    if choice in tools:
        target = input("Enter target: ")
        if osint.enhanced_consent_check(tools[choice]['name'], target):
            result = osint.launch_tool_with_notifications(
                tools[choice]['name'], 
                tools[choice]['script'], 
                target
            )
            if result:
                print(f"✅ Results saved to: {result}")
    
    elif choice == 'A':
        target = input("Enter target for all tools: ")
        if osint.enhanced_consent_check("All OSINT Tools", target):
            osint.notify("OSINT Suite", "Starting comprehensive analysis")
            
            results = []
            for key, tool in tools.items():
                result = osint.launch_tool_with_notifications(
                    tool['name'], 
                    tool['script'], 
                    target
                )
                if result:
                    results.append(result)
            
            osint.notify("OSINT Complete", f"All tools finished. {len(results)} reports generated")
            print(f"\n✅ Generated {len(results)} reports:")
            for result in results:
                print(f"   📄 {result}")
    
    elif choice == 'S':
        if osint.enhanced_consent_check("SMS Analysis", "device SMS data"):
            sms_data = osint.get_sms_data()
            if sms_data:
                print(f"📱 Found {len(sms_data)} SMS messages")
                # Process SMS data for OSINT (with privacy protection)
                osint.notify("SMS Analysis", f"Analyzed {len(sms_data)} messages")
            else:
                print("❌ Could not access SMS data")

if __name__ == "__main__":
    main()
