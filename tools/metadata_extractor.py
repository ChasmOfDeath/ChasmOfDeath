#!/usr/bin/env python3
"""
File Metadata Extractor
Educational and authorized use only
"""
import os
from PIL import Image
from PIL.ExifTags import TAGS
import json
from datetime import datetime

class MetadataExtractor:
    def __init__(self):
        pass
    
    def extract_image_metadata(self, image_path: str) -> dict:
        """Extract metadata from image files"""
        try:
            image = Image.open(image_path)
            exifdata = image.getexif()
            
            metadata = {
                'filename': os.path.basename(image_path),
                'format': image.format,
                'mode': image.mode,
                'size': image.size,
                'exif_data': {}
            }
            
            for tag_id in exifdata:
                tag = TAGS.get(tag_id, tag_id)
                data = exifdata.get(tag_id)
                metadata['exif_data'][tag] = str(data)
            
            return metadata
        except Exception as e:
            return {'error': f'Could not extract metadata: {e}'}
    
    def extract_gps_coordinates(self, exif_data: dict) -> dict:
        """Extract GPS coordinates from EXIF data"""
        gps_info = {}
        
        if 'GPSInfo' in exif_data:
            # GPS coordinate extraction logic
            gps_info['has_gps'] = True
            gps_info['warning'] = 'GPS coordinates found - privacy risk'
        else:
            gps_info['has_gps'] = False
        
        return gps_info

def main():
    print("Metadata Extractor")
    print("Educational and authorized use only!")
    
    consent = input("\nDo you own this file or have permission to analyze it? (yes/no): ")
    if consent.lower() != 'yes':
        print("Exiting - proper authorization required")
        return
    
    file_path = input("Enter file path: ")
    
    extractor = MetadataExtractor()
    metadata = extractor.extract_image_metadata(file_path)
    
    print(json.dumps(metadata, indent=2))

if __name__ == "__main__":
    main()
