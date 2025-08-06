#!/usr/bin/env python3
"""
Verify all permissions are working
"""
import subprocess
import json

def test_permission(name, command, args=[]):
    try:
        result = subprocess.run([command] + args, 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        if result.returncode == 0:
            print(f"✅ {name}: Working")
            return True
        else:
            print(f"❌ {name}: Failed - {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {name}: Error - {e}")
        return False

def main():
    print("🔐 Verifying Termux Permissions")
    print("=" * 40)
    
    permissions = [
        ("Battery", "termux-battery-status"),
        ("Clipboard Get", "termux-clipboard-get"),
        ("Notification", "termux-notification", ["--title", "Test", "--content", "Test"]),
        ("Vibrate", "termux-vibrate", ["-d", "100"]),
        ("Location", "termux-location", ["-p", "network", "-r", "once"]),
        ("Camera Info", "termux-camera-info"),
        ("SMS List", "termux-sms-list", ["-l", "1"]),
        ("Call Log", "termux-call-log", ["-l", "1"]),
        ("Contacts", "termux-contact-list", ["-l", "1"]),
        ("WiFi Info", "termux-wifi-connectioninfo"),
        ("WiFi Scan", "termux-wifi-scaninfo"),
        ("Telephony", "termux-telephony-deviceinfo"),
        ("Volume", "termux-volume", ["music"]),
        ("Brightness", "termux-brightness", ["150"])
    ]
    
    working = 0
    total = len(permissions)
    
    for perm in permissions:
        if test_permission(*perm):
            working += 1
    
    print(f"\n📊 Results: {working}/{total} permissions working")
    
    if working == total:
        print("🎉 All permissions enabled!")
    else:
        print("⚠️  Some permissions need manual enabling")
        print("Go to: Android Settings > Apps > Termux > Permissions")

if __name__ == "__main__":
    main()
