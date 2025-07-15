import logging
from pathlib import Path
from typing import List, Dict, Optional
from urllib.parse import urlparse, unquote
import re

from config.config import *

class URLProcessor:
    def __init__(self):
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(LOGS_DIR / 'url_processor.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def load_urls_from_file(self, file_path: Path) -> List[str]:
        """Load URLs from a text file"""
        urls = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    
                    # Skip empty lines and comments
                    if not line or line.startswith('#'):
                        continue
                    
                    # Basic URL validation
                    if self.is_valid_url(line):
                        urls.append(line)
                    else:
                        self.logger.warning(f"Invalid URL on line {line_num}: {line}")
            
            self.logger.info(f"Loaded {len(urls)} valid URLs from {file_path}")
            return urls
            
        except FileNotFoundError:
            self.logger.error(f"URL file not found: {file_path}")
            return []
        except Exception as e:
            self.logger.error(f"Error reading URL file: {e}")
            return []
    
    def is_valid_url(self, url: str) -> bool:
        """Validate if string is a proper URL"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
    
    def extract_filename_from_url(self, url: str) -> str:
        """Extract potential filename from URL"""
        try:
            parsed = urlparse(url)
            path = unquote(parsed.path)
            
            # Get the last part of the path
            filename = Path(path).name
            
            # Remove query parameters and fragments
            if '?' in filename:
                filename = filename.split('?')[0]
            if '#' in filename:
                filename = filename.split('#')[0]
            
            return filename
        except Exception:
            return ""
    
    def categorize_from_url(self, url: str) -> str:
        """Categorize image based on URL path and filename"""
        url_lower = url.lower()
        filename = self.extract_filename_from_url(url)
        filename_lower = filename.lower()
        
        # Combine URL and filename for analysis
        text = f"{url_lower} {filename_lower}"
        
        # Check each category for keywords
        for category, keywords in IMAGE_CATEGORIES.items():
            if any(keyword in text for keyword in keywords):
                return category
        
        return "general"
    
    def create_descriptive_name_from_url(self, url: str, category: str) -> str:
        """Create descriptive name from URL components"""
        parsed = urlparse(url)
        domain = parsed.netloc.replace('www.', '')
        
        # Extract filename without extension
        filename = self.extract_filename_from_url(url)
        name_part = Path(filename).stem if filename else ""
        
        # Clean up the name
        name_part = re.sub(r'[^\w\s-]', '', name_part)
        name_part = re.sub(r'[-\s]+', '_', name_part)
        
        # Extract potential year
        year_match = re.search(r'(191[4-8])', url)
        year = year_match.group(1) if year_match else ''
        
        # Build descriptive name
        parts = []
        
        if name_part and len(name_part) > 3:
            parts.append(name_part[:40])  # Limit length
        else:
            parts.append(f"{category}_image")
        
        if year:
            parts.append(year)
        
        # Add domain as source
        clean_domain = re.sub(r'[^\w]', '', domain)[:15]
        if clean_domain:
            parts.append(clean_domain)
        
        return '_'.join(parts).lower()
    
    def process_urls(self, urls: List[str]) -> List[Dict]:
        """Process list of URLs and create image data structures"""
        processed_images = []
        
        for i, url in enumerate(urls, 1):
            if not self.is_valid_url(url):
                self.logger.warning(f"Skipping invalid URL: {url}")
                continue
            
            category = self.categorize_from_url(url)
            descriptive_name = self.create_descriptive_name_from_url(url, category)
            
            image_data = {
                'url': url,
                'category': category,
                'descriptive_name': descriptive_name,
                'filename': self.extract_filename_from_url(url),
                'source': urlparse(url).netloc,
                'index': i
            }
            
            processed_images.append(image_data)
        
        # Group by category
        categorized_results = {}
        for image in processed_images:
            category = image['category']
            if category not in categorized_results:
                categorized_results[category] = []
            categorized_results[category].append(image)
        
        self.logger.info(f"Processed {len(processed_images)} URLs into {len(categorized_results)} categories")
        return categorized_results
    
    def create_sample_urls_file(self) -> None:
        """Create a sample URLs file for demonstration"""
        sample_urls = [
            "# WWI Image URLs - one per line",
            "# Lines starting with # are comments",
            "",
            "# Battle scenes",
            "https://example.com/battle-of-somme-1916.jpg",
            "https://example.com/trench-warfare-western-front.png",
            "",
            "# Equipment and weapons", 
            "https://example.com/wwi-tank-mark-iv.jpg",
            "https://example.com/artillery-cannon-1917.jpg",
            "",
            "# Aircraft",
            "https://example.com/sopwith-camel-fighter.jpg",
            "https://example.com/red-baron-aircraft.png",
            "",
            "# Portraits and soldiers",
            "https://example.com/british-soldier-uniform.jpg",
            "https://example.com/general-haig-portrait.jpg",
        ]
        
        with open(URLS_FILE, 'w', encoding='utf-8') as f:
            f.write('\n'.join(sample_urls))
        
        self.logger.info(f"Created sample URLs file: {URLS_FILE}")
        print(f"Sample URLs file created at: {URLS_FILE}")
        print("Please edit this file with your actual image URLs.")