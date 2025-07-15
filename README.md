# WWI Image Download System

A Python system to download World War I images from provided URLs with automatic categorization and descriptive naming.

## Features

- **URL-Based Download**: No API keys required - simply provide a list of image URLs
- **Smart Categorization**: Automatically categorizes images into battles, equipment, portraits, trenches, aircraft, ships, and general
- **Descriptive Naming**: Generates meaningful filenames based on URL analysis and content
- **Duplicate Detection**: Prevents downloading duplicate images using hash comparison
- **Image Validation**: Ensures downloaded images meet quality standards
- **Comprehensive Logging**: Tracks all operations for debugging and monitoring

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Prepare Your Image URLs

The system will create a sample `image_urls.txt` file on first run. Edit this file with your actual image URLs:

```
# WWI Image URLs - one per line
# Lines starting with # are comments

https://example.com/battle-of-somme-1916.jpg
https://example.com/trench-warfare-western-front.png
https://example.com/wwi-tank-mark-iv.jpg
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
│   ├── url_processor.py   # URL processing and categorization
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
├── image_urls.txt         # Your list of image URLs
├── requirements.txt       # Python dependencies
└── .env.example          # Environment variables template
```

## Configuration

Edit `config/config.py` to customize:

- **Image Categories**: Keywords for automatic categorization
- **Download Limits**: Maximum total images
- **Image Requirements**: Minimum size, supported formats

## URL Input Format

The `image_urls.txt` file supports:
- One URL per line
- Comments starting with #
- Empty lines for organization
- Any valid image URL format

## Image Categories

Images are automatically categorized into:

- **Battles**: Combat scenes, warfare, battles
- **Equipment**: Tanks, artillery, weapons, rifles
- **Portraits**: Soldiers, officers, uniforms, generals
- **Trenches**: Trench warfare, dugouts, no man's land
- **Aircraft**: Planes, fighters, bombers, aviation
- **Ships**: Naval vessels, submarines, destroyers
- **General**: Other WWI-related images

## Download Limits

- **Total Images**: Configurable limit (default: 1000)
- **Image Quality**: Minimum size validation (default: 200x200)
- **Supported Formats**: .jpg, .jpeg, .png, .gif, .bmp

## Logs

The system creates detailed logs in the `logs/` directory:

- `main.log`: General application logs
- `url_processor.log`: URL processing logs
- `download.log`: Download operation logs

## Troubleshooting

1. **Invalid URLs**: Check that URLs are properly formatted and accessible
2. **Download Failures**: Review download logs for specific error messages
3. **No Images Found**: Verify that your `image_urls.txt` file contains valid URLs
4. **Image Quality Issues**: Adjust minimum size requirements in `config.py`

## Legal Considerations

- Ensure you have the right to download images from the provided URLs
- Always verify image rights before use
- Respect copyright and fair use guidelines
- Consider the historical nature and sensitivity of WWI imagery
- Be respectful of source websites and their terms of service