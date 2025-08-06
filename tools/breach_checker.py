#!/usr/bin/env python3
"""
Data Breach Checker
Educational and authorized use only
"""
import hashlib
import requests
from datetime import datetime

class BreachChecker:
    def __init__(self):
        self.session = requests.Session()
    
    def check_haveibeenpwned(self, email: str) -> dict:
        """Check HaveIBeenPwned API (requires API key)"""
        return {
            'service': 'HaveIBeenPwned',
            'status': 'Requires API key',
            'recommendation': 'Visit https://haveibeenpwned.com directly'
        }
    
    def check_password_hash(self, password: str) -> dict:
        """Check password against known breaches using k-anonymity"""
        # SHA-1 hash of password
        sha1_hash = hashlib.sha1(password.encode()).hexdigest().upper()
        prefix = sha1_hash[:5]
        suffix = sha1_hash[5:]
        
        try:
            response = self.session.get(f"https://api.pwnedpasswords.com/range/{prefix}")
            if response.status_code == 200:
                hashes = response.text.split('\n')
                for hash_line in hashes:
                    if hash_line.startswith(suffix):
                        count = int(hash_line.split(':')[1])
                        return {
                            'is_pwned': True,
                            'count': count,
                            'recommendation': 'Change password immediately'
                        }
                return {
                    'is_pwned': False,
                    'count': 0,
                    'recommendation': 'Password appears safe'
                }
        except:
            return {'error': 'Could not check password'}

def main():
    print("Data Breach Checker")
    print("Educational and authorized use only!")
    
    consent = input("\nDo you have permission to check this data? (yes/no): ")
    if consent.lower() != 'yes':
        print("Exiting - proper authorization required")
        return
    
    checker = BreachChecker()
    
    choice = input("Check (e)mail or (p)assword? ")
    if choice.lower() == 'e':
        email = input("Enter email: ")
        result = checker.check_haveibeenpwned(email)
        print(f"Result: {result}")
    elif choice.lower() == 'p':
        password = input("Enter password: ")
        result = checker.check_password_hash(password)
        print(f"Password breach status: {result}")

if __name__ == "__main__":
    main()
