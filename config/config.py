import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
IMAGES_DIR = BASE_DIR / "images"
LOGS_DIR = BASE_DIR / "logs"

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

WWI_SEARCH_TERMS = [
    "World War 1 1914-1918",
    "Great War trench warfare",
    "Battle of Somme 1916",
    "Battle of Verdun 1916", 
    "Western Front WWI",
    "WWI soldiers uniforms",
    "WWI aircraft planes",
    "WWI tanks equipment",
    "WWI naval ships",
    "WWI gas masks",
    "WWI artillery",
    "WWI propaganda posters",
    "Kaiser Wilhelm II",
    "General Haig WWI",
    "Archduke Franz Ferdinand",
    "WWI trenches no mans land"
]

IMAGE_CATEGORIES = {
    "battles": ["battle", "warfare", "combat", "attack", "offensive"],
    "equipment": ["tank", "artillery", "weapon", "rifle", "equipment", "gun"],
    "portraits": ["soldier", "officer", "portrait", "uniform", "general"],
    "general": ["war", "WWI", "1914", "1915", "1916", "1917", "1918"],
    "trenches": ["trench", "dugout", "no mans land", "barbed wire"],
    "aircraft": ["plane", "aircraft", "fighter", "bomber", "aviation"],
    "ships": ["ship", "naval", "submarine", "destroyer", "battleship"]
}

MAX_IMAGES_PER_SEARCH = 10
MAX_TOTAL_IMAGES = 100
IMAGE_FORMATS = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]
MIN_IMAGE_SIZE = (200, 200)