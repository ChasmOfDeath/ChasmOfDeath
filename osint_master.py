#!/usr/bin/env python3
"""
OSINT Master Control Panel
Educational and authorized use only
"""
import sys
import os
from datetime import datetime

def display_menu():
    print(f"\n{'='*60}")
    print("🔍 COMPREHENSIVE OSINT TOOLKIT")
    print(f"{'='*60}")
    print("1. Phone Number Analysis")
    print("2. Advanced Phone OSINT")
    print("3. Email & Domain Analysis")
    print("4. Username Search")
    print("5. IP Address & Network Analysis")
    print("6. Social Media Lookup")
    print("7. Generate Combined Report")
    print("8. View Legal Guidelines")
    print("9. Exit")
    print(f"{'='*60}")

def run_tool(choice):
    tools = {
        '1': 'tools/phone_validator.py',
        '2': 'tools/advanced_phone_osint.py',
        '3': 'tools/email_domain_osint.py',
        '4': 'tools/username_osint.py',
        '5': 'tools/ip_network_osint.py',
        '6': 'tools/social_lookup.py'
    }
    
    if choice in tools:
        os.system(f'python {tools[choice]}')
    elif choice == '7':
        generate_combined_report()
    elif choice == '8':
        os.system('cat legal/compliance_guide.md')
    elif choice == '9':
        print("Exiting OSINT Toolkit")
        sys.exit(0)
    else:
        print("Invalid choice")

def generate_combined_report():
    print("Combined Report Generator")
    print("This would aggregate results from multiple tools")
    # Implementation for combined reporting

def main():
    print("🔍 OSINT Master Control Panel")
    print("Educational and authorized use only!")
    
    while True:
        display_menu()
        choice = input("\nSelect option (1-9): ")
        run_tool(choice)
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
