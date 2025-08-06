#!/bin/bash
echo "Setting up Messaging OSINT Toolkit"
echo "Educational and authorized use only!"

# Install dependencies
pip install -r requirements.txt

# Set permissions
chmod +x tools/*.py
chmod +x examples/*.py

echo "Setup complete!"
echo "Read legal/compliance_guide.md before use"

# Install additional dependencies
pip install Pillow

# Set permissions for new tools
chmod +x tools/breach_checker.py
chmod +x tools/metadata_extractor.py
chmod +x tools/crypto_analyzer.py
chmod +x osint_master.py

echo "All OSINT tools ready!"
echo "Run: python osint_master.py"
