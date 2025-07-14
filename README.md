# WWI Image Search and Download System

A Python system to search the web for contemporary World War I images and download them with descriptive filenames.

## Features

- **Google Custom Search Integration**: Uses Google Custom Search API to find historical WWI images
- **Smart Categorization**: Automatically categorizes images into battles, equipment, portraits, trenches, aircraft, ships, and general
- **Descriptive Naming**: Generates meaningful filenames based on image metadata and content
- **Duplicate Detection**: Prevents downloading duplicate images using hash comparison
- **Image Validation**: Ensures downloaded images meet quality standards
- **Comprehensive Logging**: Tracks all operations for debugging and monitoring

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

1. **Google Custom Search API**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable "Custom Search API"
   - Create API key credentials
   - Go to [Google Custom Search Engine](https://cse.google.com/cse/all)
   - Create a new search engine
   - Enable "Image search" and "Search the entire web"
   - Copy your Search Engine ID

2. **Environment Variables**:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your API credentials:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   GOOGLE_CSE_ID=your_custom_search_engine_id_here
   ```

### 3. Run the Application

```bash
python src/main.py
```

## Project Structure

```
ww1-images/
├── src/                    # Source code
│   ├── main.py            # Main application
│   ├── image_searcher.py  # Google Custom Search integration
│   └── image_downloader.py # Image download and processing
├── config/                # Configuration files
│   └── config.py          # Application settings
├── images/                # Downloaded images (organized by category)
│   ├── battles/
│   ├── equipment/
│   ├── portraits/
│   ├── trenches/
│   ├── aircraft/
│   ├── ships/
│   └── general/
├── logs/                  # Application logs
├── requirements.txt       # Python dependencies
└── .env.example          # Environment variables template
```

## Configuration

Edit `config/config.py` to customize:

- **Search Terms**: WWI-specific search queries
- **Image Categories**: Keywords for automatic categorization
- **Download Limits**: Maximum images per search/category
- **Image Requirements**: Minimum size, supported formats

## Search Terms

The system searches for images using these WWI-specific terms:

- World War 1 1914-1918
- Great War trench warfare
- Battle of Somme 1916
- Battle of Verdun 1916
- Western Front WWI
- WWI soldiers uniforms
- WWI aircraft planes
- WWI tanks equipment
- And more...

## Image Categories

Images are automatically categorized into:

- **Battles**: Combat scenes, warfare, battles
- **Equipment**: Tanks, artillery, weapons, rifles
- **Portraits**: Soldiers, officers, uniforms, generals
- **Trenches**: Trench warfare, dugouts, no man's land
- **Aircraft**: Planes, fighters, bombers, aviation
- **Ships**: Naval vessels, submarines, destroyers
- **General**: Other WWI-related images

## API Limits

- **Google Custom Search**: 100 free queries per day
- **Rate Limiting**: 1 second delay between searches
- **Image Limits**: Configurable max images per search and total

## Logs

The system creates detailed logs in the `logs/` directory:

- `main.log`: General application logs
- `search.log`: Search operation logs
- `download.log`: Download operation logs

## Troubleshooting

1. **API Key Issues**: Ensure your Google API key is valid and Custom Search API is enabled
2. **No Images Found**: Check your Custom Search Engine configuration
3. **Download Failures**: Review download logs for specific error messages
4. **Rate Limiting**: The system includes built-in rate limiting, but you may need to adjust for your API quotas

## Legal Considerations

- This system searches for images with appropriate licensing (Creative Commons, public domain)
- Always verify image rights before use
- Respect copyright and fair use guidelines
- Consider the historical nature and sensitivity of WWI imagery