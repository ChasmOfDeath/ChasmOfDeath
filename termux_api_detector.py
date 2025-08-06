#!/usr/bin/env python3
"""
Termux API Detection and Integration
Detects available Termux APIs and integrates them into OSINT toolkit
"""
import subprocess
import json
import os
from datetime import datetime

class TermuxAPIDetector:
    def __init__(self):
        self.available_apis = {}
        self.detect_all_apis()
    
    def test_api_command(self, command, test_args=None):
        """Test if a Termux API command is available"""
        try:
            if test_args:
                result = subprocess.run([command] + test_args, 
                                      capture_output=True, 
                                      text=True, 
                                      timeout=5)
            else:
                result = subprocess.run([command, '--help'], 
                                      capture_output=True, 
                                      text=True, 
                                      timeout=5)
            return result.returncode == 0
        except:
            return False
    
    def detect_all_apis(self):
        """Detect all available Termux APIs"""
        api_commands = {
            'battery': 'termux-battery-status',
            'clipboard_get': 'termux-clipboard-get',
            'clipboard_set': 'termux-clipboard-set',
            'notification': 'termux-notification',
            'vibrate': 'termux-vibrate',
            'toast': 'termux-toast',
            'tts': 'termux-tts-speak',
            'camera_info': 'termux-camera-info',
            'camera_photo': 'termux-camera-photo',
            'location': 'termux-location',
            'sensor': 'termux-sensor',
            'wifi': 'termux-wifi-connectioninfo',
            'wifi_scan': 'termux-wifi-scaninfo',
            'telephony': 'termux-telephony-deviceinfo',
            'contact_list': 'termux-contact-list',
            'sms_list': 'termux-sms-list',
            'call_log': 'termux-call-log',
            'storage_get': 'termux-storage-get',
            'dialog': 'termux-dialog',
            'fingerprint': 'termux-fingerprint',
            'microphone': 'termux-microphone-record',
            'torch': 'termux-torch',
            'volume': 'termux-volume',
            'brightness': 'termux-brightness'
        }
        
        print("🔍 Detecting available Termux APIs...")
        
        for api_name, command in api_commands.items():
            if self.test_api_command(command):
                self.available_apis[api_name] = command
                print(f"✅ {api_name}: {command}")
            else:
                print(f"❌ {api_name}: Not available")
        
        print(f"\n📊 Total APIs available: {len(self.available_apis)}")
        return self.available_apis
    
    def get_device_info(self):
        """Get comprehensive device information"""
        device_info = {
            'timestamp': datetime.now().isoformat(),
            'available_apis': list(self.available_apis.keys())
        }
        
        # Battery info
        if 'battery' in self.available_apis:
            try:
                result = subprocess.run(['termux-battery-status'], 
                                      capture_output=True, text=True)
                device_info['battery'] = json.loads(result.stdout)
            except:
                device_info['battery'] = 'Error getting battery info'
        
        # WiFi info
        if 'wifi' in self.available_apis:
            try:
                result = subprocess.run(['termux-wifi-connectioninfo'], 
                                      capture_output=True, text=True)
                device_info['wifi'] = json.loads(result.stdout)
            except:
                device_info['wifi'] = 'Error getting WiFi info'
        
        # Telephony info
        if 'telephony' in self.available_apis:
            try:
                result = subprocess.run(['termux-telephony-deviceinfo'], 
                                      capture_output=True, text=True)
                device_info['telephony'] = json.loads(result.stdout)
            except:
                device_info['telephony'] = 'Error getting telephony info'
        
        # Location (if permission granted)
        if 'location' in self.available_apis:
            try:
                result = subprocess.run(['termux-location', '-p', 'network'], 
                                      capture_output=True, text=True, timeout=10)
                device_info['location'] = json.loads(result.stdout)
            except:
                device_info['location'] = 'Location not available or permission denied'
        
        return device_info
    
    def save_api_config(self):
        """Save API configuration for other tools"""
        config = {
            'detected_at': datetime.now().isoformat(),
            'available_apis': self.available_apis,
            'device_info': self.get_device_info()
        }
        
        with open('config/termux_api_config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"💾 API configuration saved to config/termux_api_config.json")
        return config

def main():
    print("🔍 Termux API Detection and Integration")
    print("=" * 50)
    
    detector = TermuxAPIDetector()
    config = detector.save_api_config()
    
    print("\n📱 Device Information:")
    device_info = config['device_info']
    
    if 'battery' in device_info and isinstance(device_info['battery'], dict):
        battery = device_info['battery']
        print(f"🔋 Battery: {battery.get('percentage', 'Unknown')}% ({battery.get('status', 'Unknown')})")
    
    if 'wifi' in device_info and isinstance(device_info['wifi'], dict):
        wifi = device_info['wifi']
        print(f"📶 WiFi: {wifi.get('ssid', 'Unknown')} ({wifi.get('ip', 'No IP')})")
    
    if 'telephony' in device_info and isinstance(device_info['telephony'], dict):
        tel = device_info['telephony']
        print(f"📱 Network: {tel.get('network_operator_name', 'Unknown')}")
    
    print(f"\n✅ Configuration ready for OSINT toolkit integration!")

if __name__ == "__main__":
    main()
