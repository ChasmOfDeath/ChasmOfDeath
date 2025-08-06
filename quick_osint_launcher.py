#!/usr/bin/env python3
"""
Quick OSINT Launcher - Optimized for your Termux setup
"""
import subprocess
import threading
import time
from datetime import datetime

def notify(title, message):
    """Send notification"""
    try:
        subprocess.run(['termux-notification', '--title', title, '--content', message])
    except:
        pass
    print(f"📱 {title}: {message}")

def launch_all_tools(target):
    """Launch all tools simultaneously with notifications"""
    tools = [
        'tools/phone_validator.py',
        'tools/email_domain_osint.py', 
        'tools/username_osint.py',
        'tools/ip_network_osint.py'
    ]
    
    notify("OSINT Suite", f"Starting analysis of {target}")
    
    def run_tool(script):
        try:
            input_data = f"yes\n{target}\n"
            result = subprocess.run([
                'python', script
            ], input=input_data, text=True, capture_output=True, timeout=120)
            
            tool_name = script.split('/')[-1].replace('.py', '')
            
            # Save individual results
            with open(f"quick_result_{tool_name}_{int(time.time())}.txt", 'w') as f:
                f.write(f"Tool: {script}\n")
                f.write(f"Target: {target}\n")
                f.write(f"Time: {datetime.now()}\n\n")
                f.write(result.stdout)
                if result.stderr:
                    f.write(f"\nErrors:\n{result.stderr}")
            
            notify("Tool Complete", f"{tool_name} finished")
            
        except Exception as e:
            notify("Tool Error", f"{script} failed: {e}")
    
    # Launch all tools in parallel
    threads = []
    for tool in tools:
        thread = threading.Thread(target=run_tool, args=(tool,))
        thread.start()
        threads.append(thread)
        time.sleep(1)  # Stagger launches
    
    # Wait for completion
    for thread in threads:
        thread.join()
    
    notify("OSINT Complete", "All tools finished!")
    print("✅ All tools completed! Check quick_result_* files")

def main():
    print("🚀 Quick OSINT Launcher")
    print("Optimized for your Termux setup")
    
    target = input("Enter target (phone/email/username/IP): ")
    
    print(f"🎯 Target: {target}")
    confirm = input("Launch all tools? (y/n): ")
    
    if confirm.lower() == 'y':
        launch_all_tools(target)
    else:
        print("Launch cancelled")

if __name__ == "__main__":
    main()
