#!/usr/bin/env python3
"""
WWI Image Download System
Downloads World War I images from provided URLs with automatic categorization
"""

import sys
from pathlib import Path
import logging
from colorama import init, Fore, Style

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from config.config import *
from src.url_processor import URLProcessor
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

def print_banner():
    """Print application banner"""
    print(f"{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}    WWI Image Download System")
    print(f"{Fore.CYAN}    Download and categorize images from URL list")
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
    print_banner()
    
    logger = setup_logging()
    
    # Create directories
    IMAGES_DIR.mkdir(exist_ok=True)
    LOGS_DIR.mkdir(exist_ok=True)
    
    try:
        # Initialize URL processor and downloader
        print(f"{Fore.BLUE}Initializing URL processor...")
        url_processor = URLProcessor()
        
        print(f"{Fore.BLUE}Initializing image downloader...")
        downloader = WWIImageDownloader()
        
        # Check if URLs file exists
        if not URLS_FILE.exists():
            print(f"{Fore.YELLOW}URLs file not found. Creating sample file...")
            url_processor.create_sample_urls_file()
            print(f"{Fore.RED}Please edit {URLS_FILE} with your image URLs and run again.")
            sys.exit(1)
        
        # Load URLs from file
        print(f"{Fore.BLUE}Loading URLs from {URLS_FILE}...")
        urls = url_processor.load_urls_from_file(URLS_FILE)
        
        if not urls:
            print(f"{Fore.RED}No valid URLs found in {URLS_FILE}")
            print(f"{Fore.YELLOW}Please check the file format and ensure it contains valid URLs.")
            sys.exit(1)
        
        print(f"{Fore.GREEN}Loaded {len(urls)} URLs")
        
        # Process URLs and categorize
        print(f"{Fore.BLUE}Processing and categorizing URLs...")
        categorized_results = url_processor.process_urls(urls)
        
        # Print categorization results
        print(f"\n{Fore.GREEN}Categorization Results:")
        total_images = 0
        for category, images in categorized_results.items():
            print(f"{Fore.YELLOW}{category.capitalize()}: {Fore.WHITE}{len(images)} images")
            total_images += len(images)
        
        print(f"{Fore.GREEN}Total images to download: {Fore.WHITE}{total_images}")
        
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