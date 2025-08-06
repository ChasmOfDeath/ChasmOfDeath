#!/bin/bash
echo "🔐 Setting up Termux permissions for OSINT tools"
echo "You may see permission dialogs - please ALLOW all requests"

echo "📱 Testing basic permissions..."

# Storage (usually works)
echo "📁 Storage permission..."
termux-setup-storage

# Notification (should work)
echo "🔔 Notification permission..."
termux-notification --title "Permission Test" --content "Testing notifications"

# Battery (may need permission)
echo "🔋 Battery permission..."
termux-battery-status

# Clipboard (may need permission)
echo "📋 Clipboard permission..."
echo "test" | termux-clipboard-set
CLIPBOARD_TEST=$(termux-clipboard-get)
if [ "$CLIPBOARD_TEST" = "test" ]; then
    echo "✅ Clipboard working"
else
    echo "❌ Clipboard needs permission"
fi

# Location (needs permission)
echo "📍 Location permission..."
termux-location -p network -r once

# Camera (needs permission)
echo "📷 Camera permission..."
termux-camera-info

# Microphone (needs permission)
echo "🎤 Microphone permission..."
termux-microphone-record -f /dev/null -l 1 2>/dev/null

# SMS (needs permission)
echo "💬 SMS permission..."
termux-sms-list -l 1 2>/dev/null

# Contacts (needs permission)
echo "👥 Contacts permission..."
termux-contact-list -l 1 2>/dev/null

# Phone (needs permission)
echo "📞 Phone permission..."
termux-call-log -l 1 2>/dev/null
termux-telephony-deviceinfo 2>/dev/null

# WiFi (may need permission)
echo "📶 WiFi permission..."
termux-wifi-connectioninfo 2>/dev/null
termux-wifi-scaninfo 2>/dev/null

echo ""
echo "🔐 Permission setup complete!"
echo "If any permissions were denied, go to:"
echo "Android Settings > Apps > Termux > Permissions"
echo "And manually enable all permissions"
