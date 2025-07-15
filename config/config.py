from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
IMAGES_DIR = BASE_DIR / "images"
LOGS_DIR = BASE_DIR / "logs"
URLS_FILE = BASE_DIR / "image_urls.txt"

IMAGE_CATEGORIES = {
    "battles": ["battle", "warfare", "combat", "attack", "offensive"],
    "equipment": ["tank", "artillery", "weapon", "rifle", "equipment", "gun"],
    "portraits": ["soldier", "officer", "portrait", "uniform", "general"],
    "general": ["war", "WWI", "1914", "1915", "1916", "1917", "1918"],
    "trenches": ["trench", "dugout", "no mans land", "barbed wire"],
    "aircraft": ["plane", "aircraft", "fighter", "bomber", "aviation"],
    "ships": ["ship", "naval", "submarine", "destroyer", "battleship"]
}

MAX_TOTAL_IMAGES = 1000
IMAGE_FORMATS = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]
MIN_IMAGE_SIZE = (200, 200)