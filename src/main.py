#!/usr/bin/env python3
"""
WWI Image Search and Download System
Main application to search for and download World War I images
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import logging
from colorama import init, Fore, Style

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from config.config import *
from src.image_searcher import WWIImageSearcher
from src.image_downloader import WWIImageDownloader

# Initialize colorama for colored output
init(autoreset=True)

def setup_logging():
    """Setup logging configuration"""
    LOGS_DIR.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOGS_DIR / 'main.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def check_api_keys():
    """Check if required API keys are available"""
    if not GOOGLE_API_KEY:
        print(f"{Fore.RED}Error: GOOGLE_API_KEY not found in environment variables")
        print(f"{Fore.YELLOW}Please set your Google Custom Search API key in .env file")
        return False
    
    if not GOOGLE_CSE_ID:
        print(f"{Fore.RED}Error: GOOGLE_CSE_ID not found in environment variables")
        print(f"{Fore.YELLOW}Please set your Google Custom Search Engine ID in .env file")
        return False
    
    return True

def print_banner():
    """Print application banner"""
    print(f"{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}    WWI Image Search and Download System")
    print(f"{Fore.CYAN}    Collecting historical images from World War I")
    print(f"{Fore.CYAN}{'='*60}")
    print()

def print_summary(download_stats: dict):
    """Print download summary"""
    print(f"\n{Fore.GREEN}{'='*40}")
    print(f"{Fore.GREEN}Download Summary:")
    print(f"{Fore.GREEN}{'='*40}")
    
    total_downloaded = 0
    for category, count in download_stats.items():
        print(f"{Fore.YELLOW}{category.capitalize()}: {Fore.WHITE}{count} images")
        total_downloaded += count
    
    print(f"{Fore.GREEN}{'='*40}")
    print(f"{Fore.GREEN}Total Downloaded: {Fore.WHITE}{total_downloaded} images")
    print(f"{Fore.GREEN}{'='*40}")

def main():
    """Main application function"""
    load_dotenv()
    print_banner()
    
    logger = setup_logging()
    
    # Check API keys
    if not check_api_keys():
        sys.exit(1)
    
    # Create directories
    IMAGES_DIR.mkdir(exist_ok=True)
    LOGS_DIR.mkdir(exist_ok=True)
    
    try:
        # Initialize searcher and downloader
        print(f"{Fore.BLUE}Initializing image searcher...")
        searcher = WWIImageSearcher(GOOGLE_API_KEY, GOOGLE_CSE_ID)
        
        print(f"{Fore.BLUE}Initializing image downloader...")
        downloader = WWIImageDownloader()
        
        # Search for images
        print(f"{Fore.BLUE}Searching for WWI images...")
        print(f"{Fore.YELLOW}Search terms: {len(WWI_SEARCH_TERMS)} different queries")
        
        categorized_results = searcher.search_all_terms()
        
        if not categorized_results:
            print(f"{Fore.RED}No images found. Please check your search terms and API configuration.")
            sys.exit(1)
        
        # Print search results
        print(f"\n{Fore.GREEN}Search Results:")
        total_found = 0
        for category, images in categorized_results.items():
            print(f"{Fore.YELLOW}{category.capitalize()}: {Fore.WHITE}{len(images)} images found")
            total_found += len(images)
        
        print(f"{Fore.GREEN}Total found: {Fore.WHITE}{total_found} images")
        
        # Download images
        print(f"\n{Fore.BLUE}Starting download process...")
        download_stats = downloader.download_all_images(categorized_results)
        
        # Print summary
        print_summary(download_stats)
        
        print(f"\n{Fore.GREEN}Process completed successfully!")
        print(f"{Fore.YELLOW}Images saved to: {IMAGES_DIR}")
        print(f"{Fore.YELLOW}Logs saved to: {LOGS_DIR}")
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Process interrupted by user.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"{Fore.RED}An unexpected error occurred. Check logs for details.")
        sys.exit(1)

if __name__ == "__main__":
    main()