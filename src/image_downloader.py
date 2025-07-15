import requests
import os
import hashlib
import logging
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urlparse
from PIL import Image
import re

from config.config import *

class WWIImageDownloader:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(LOGS_DIR / 'download.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Track downloaded images to avoid duplicates
        self.downloaded_hashes = set()
    
    def generate_descriptive_name(self, image_data: Dict, category: str) -> str:
        """Generate a descriptive filename from image metadata"""
        # Use the pre-generated descriptive name if available
        if 'descriptive_name' in image_data:
            return image_data['descriptive_name']
        
        # Fallback to URL-based naming
        url = image_data.get('url', '')
        source = image_data.get('source', '')
        
        # Extract filename from URL
        from urllib.parse import urlparse
        parsed = urlparse(url)
        filename = Path(parsed.path).stem
        
        # Clean up filename
        filename = re.sub(r'[^\w\s-]', '', filename)
        filename = re.sub(r'[-\s]+', '_', filename)
        
        # Extract year if present
        year_match = re.search(r'(191[4-8])', url)
        year = year_match.group(1) if year_match else ''
        
        # Create base name
        if filename and len(filename) > 5:
            base_name = filename[:50]  # Limit length
        else:
            base_name = f"{category}_image"
        
        # Add year if found
        if year:
            base_name = f"{base_name}_{year}"
        
        # Add source if available
        if source:
            clean_source = re.sub(r'[^\w]', '', source)[:15]
            base_name = f"{base_name}_{clean_source}"
        
        return base_name.lower()
    
    def get_image_hash(self, image_path: Path) -> str:
        """Generate hash of image file to detect duplicates"""
        try:
            with open(image_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception as e:
            self.logger.error(f"Error generating hash for {image_path}: {e}")
            return ""
    
    def is_valid_image(self, image_path: Path) -> bool:
        """Validate downloaded image"""
        try:
            with Image.open(image_path) as img:
                width, height = img.size
                
                # Check minimum size
                if width < MIN_IMAGE_SIZE[0] or height < MIN_IMAGE_SIZE[1]:
                    self.logger.warning(f"Image too small: {width}x{height} - {image_path}")
                    return False
                
                # Check if image is valid
                img.verify()
                return True
                
        except Exception as e:
            self.logger.error(f"Invalid image {image_path}: {e}")
            return False
    
    def download_image(self, image_data: Dict, category: str) -> Optional[Path]:
        """Download a single image and save with descriptive name"""
        url = image_data.get('url', '')
        if not url:
            return None
        
        try:
            # Get file extension
            parsed_url = urlparse(url)
            ext = Path(parsed_url.path).suffix.lower()
            if ext not in IMAGE_FORMATS:
                ext = '.jpg'  # Default extension
            
            # Generate descriptive filename
            base_name = self.generate_descriptive_name(image_data, category)
            filename = f"{base_name}{ext}"
            
            # Create category directory if it doesn't exist
            category_dir = IMAGES_DIR / category
            category_dir.mkdir(parents=True, exist_ok=True)
            
            # Check if file already exists
            file_path = category_dir / filename
            counter = 1
            while file_path.exists():
                name_without_ext = base_name
                filename = f"{name_without_ext}_{counter}{ext}"
                file_path = category_dir / filename
                counter += 1
            
            # Download the image
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # Save image
            with open(file_path, 'wb') as f:
                f.write(response.content)
            
            # Validate image
            if not self.is_valid_image(file_path):
                file_path.unlink()  # Delete invalid image
                return None
            
            # Check for duplicates
            image_hash = self.get_image_hash(file_path)
            if image_hash in self.downloaded_hashes:
                self.logger.info(f"Duplicate image found, skipping: {filename}")
                file_path.unlink()
                return None
            
            self.downloaded_hashes.add(image_hash)
            
            self.logger.info(f"Downloaded: {filename}")
            return file_path
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error downloading {url}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error downloading {url}: {e}")
            return None
    
    def download_all_images(self, categorized_results: Dict[str, List[Dict]]) -> Dict[str, int]:
        """Download all images from search results"""
        download_stats = {}
        
        for category, images in categorized_results.items():
            self.logger.info(f"Downloading {len(images)} images for category: {category}")
            
            successful_downloads = 0
            for image_data in images:
                if successful_downloads >= MAX_TOTAL_IMAGES // len(categorized_results):
                    break
                    
                downloaded_path = self.download_image(image_data, category)
                if downloaded_path:
                    successful_downloads += 1
            
            download_stats[category] = successful_downloads
            self.logger.info(f"Downloaded {successful_downloads} images for {category}")
        
        return download_stats