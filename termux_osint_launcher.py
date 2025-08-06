#!/usr/bin/env python3
"""
Termux OSINT Multi-Tool Launcher
Uses Termux API for enhanced mobile functionality
"""
import subprocess
import threading
import json
import time
from datetime import datetime
import os

class TermuxOSINTLauncher:
    def __init__(self):
        self.tools = {
            '1': {'name': 'Phone Validator', 'script': 'tools/phone_validator.py'},
            '2': {'name': 'Advanced Phone OSINT', 'script': 'tools/advanced_phone_osint.py'},
            '3': {'name': 'Email Domain OSINT', 'script': 'tools/email_domain_osint.py'},
            '4': {'name': 'Username OSINT', 'script': 'tools/username_osint.py'},
            '5': {'name': 'IP Network OSINT', 'script': 'tools/ip_network_osint.py'},
            '6': {'name': 'Social Lookup', 'script': 'tools/social_lookup.py'},
            '7': {'name': 'Breach Checker', 'script': 'tools/breach_checker.py'},
            '8': {'name': 'Metadata Extractor', 'script': 'tools/metadata_extractor.py'},
            '9': {'name': 'Crypto Analyzer', 'script': 'tools/crypto_analyzer.py'}
        }
    
    def send_notification(self, title, message):
        """Send Android notification via Termux API"""
        try:
            subprocess.run([
                'termux-notification', 
                '--title', title,
                '--content', message
            ])
            print(f"📱 {title}: {message}")
        except:
            print(f"📱 {title}: {message}")
    
    def get_clipboard_content(self):
        """Get clipboard content for auto-input"""
        try:
            result = subprocess.run(['termux-clipboard-get'], 
                                  capture_output=True, text=True)
            return result.stdout.strip()
        except:
            return None
    
    def launch_tool_simple(self, tool_key, target):
        """Launch a single tool with target"""
        tool = self.tools[tool_key]
        print(f"🔧 Starting {tool['name']} with target: {target}")
        
        try:
            # Create a simple script to run the tool
            script_content = f"""
import subprocess
import sys

# Run the tool
process = subprocess.Popen([
    'python', '{tool['script']}'
], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# Send input
input_data = "yes\\n{target}\\n"
stdout, stderr = process.communicate(input=input_data)

print("=== {tool['name']} Results ===")
print(stdout)
if stderr:
    print("Errors:", stderr)
"""
            
            # Save and run the script
            script_file = f"temp_script_{tool_key}.py"
            with open(script_file, 'w') as f:
                f.write(script_content)
            
            # Run in background
            subprocess.Popen(['python', script_file])
            
        except Exception as e:
            print(f"❌ Error launching {tool['name']}: {e}")
    
    def launch_all_tools_simple(self, target):
        """Launch all tools with simplified approach"""
        print(f"\n{'='*50}")
        print("🚀 LAUNCHING ALL OSINT TOOLS")
        print(f"{'='*50}")
        print(f"🎯 Target: {target}")
        
        self.send_notification("OSINT Suite", f"Starting analysis of {target}")
        
        # Launch each tool
        for tool_key in self.tools.keys():
            self.launch_tool_simple(tool_key, target)
            time.sleep(1)  # Small delay between launches
        
        print(f"\n✅ All {len(self.tools)} tools launched!")
        print("📊 Check terminal output for results")
        
        self.send_notification("OSINT Suite", "All tools launched successfully!")

def main():
    launcher = TermuxOSINTLauncher()
    
    print("🔍 Termux OSINT Multi-Tool Launcher")
    print("1. Interactive Mode")
    print("2. Quick Launch (clipboard)")
    print("3. Manual Target Entry")
    
    choice = input("Select mode (1-3): ").strip()
    
    if choice == '1':
        # Interactive mode
        target = input("Enter target (phone/email/username/IP): ").strip()
        if target:
            launcher.launch_all_tools_simple(target)
        else:
            print("❌ No target provided")
            
    elif choice == '2':
        # Quick launch from clipboard
        clipboard_target = launcher.get_clipboard_content()
        if clipboard_target:
            print(f"📋 Using clipboard target: {clipboard_target}")
            launcher.launch_all_tools_simple(clipboard_target)
        else:
            print("❌ No clipboard content found")
            
    elif choice == '3':
        # Manual entry
        print("Enter target information:")
        target = input("Target: ").strip()
        if target:
            launcher.launch_all_tools_simple(target)
        else:
            print("❌ No target provided")
    else:
        print("❌ Invalid choice. Please select 1, 2, or 3")

if __name__ == "__main__":
    main()
