import requests
import json
import os
import time
import logging
from typing import List, Dict, Optional
from urllib.parse import urlparse
from pathlib import Path

from config.config import *

class WWIImageSearcher:
    def __init__(self, api_key: str, cse_id: str):
        self.api_key = api_key
        self.cse_id = cse_id
        self.base_url = "https://www.googleapis.com/customsearch/v1"
        self.session = requests.Session()
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(LOGS_DIR / 'search.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def search_images(self, query: str, num_results: int = 10) -> List[Dict]:
        """Search for images using Google Custom Search API"""
        params = {
            'key': self.api_key,
            'cx': self.cse_id,
            'q': query,
            'searchType': 'image',
            'num': min(num_results, 10),  # Max 10 per request
            'safe': 'active',
            'imgSize': 'medium',
            'imgType': 'photo',
            'fileType': 'jpg,png,gif',
            'rights': 'cc_publicdomain,cc_attribute,cc_sharealike,cc_noncommercial,cc_nonderived'
        }
        
        try:
            response = self.session.get(self.base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if 'items' not in data:
                self.logger.warning(f"No images found for query: {query}")
                return []
            
            results = []
            for item in data['items']:
                result = {
                    'title': item.get('title', ''),
                    'url': item.get('link', ''),
                    'thumbnail': item.get('image', {}).get('thumbnailLink', ''),
                    'width': item.get('image', {}).get('width', 0),
                    'height': item.get('image', {}).get('height', 0),
                    'size': item.get('image', {}).get('byteSize', 0),
                    'context': item.get('image', {}).get('contextLink', ''),
                    'source': urlparse(item.get('link', '')).netloc
                }
                results.append(result)
            
            self.logger.info(f"Found {len(results)} images for query: {query}")
            return results
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error searching for images: {e}")
            return []
        except json.JSONDecodeError as e:
            self.logger.error(f"Error parsing JSON response: {e}")
            return []
    
    def categorize_image(self, image_data: Dict) -> str:
        """Categorize image based on title and context"""
        title = image_data.get('title', '').lower()
        context = image_data.get('context', '').lower()
        text = f"{title} {context}"
        
        # Check each category for keywords
        for category, keywords in IMAGE_CATEGORIES.items():
            if any(keyword in text for keyword in keywords):
                return category
        
        return "general"
    
    def search_all_terms(self) -> Dict[str, List[Dict]]:
        """Search for all WWI terms and categorize results"""
        all_results = {}
        
        for term in WWI_SEARCH_TERMS:
            self.logger.info(f"Searching for: {term}")
            images = self.search_images(term, MAX_IMAGES_PER_SEARCH)
            
            for image in images:
                category = self.categorize_image(image)
                
                if category not in all_results:
                    all_results[category] = []
                
                all_results[category].append(image)
            
            # Rate limiting - be respectful to the API
            time.sleep(1)
        
        return all_results