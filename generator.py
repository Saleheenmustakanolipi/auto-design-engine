import os
import random
import re
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# ===== SETTINGS =====
SHEET_ID = "PASTE_YOUR_SHEET_ID"
SHEET_NAME = "Sheet1"
IMAGE_SIZE = 1080

FONTS = [
    "fonts/Montserrat-Bold.ttf",
    "fonts/Poppins-SemiBold.ttf",
    "fonts/PlayfairDisplay-Bold.ttf"
]

SOLID_COLORS = [
    (255,255,255),        # White
    (0,0,0),              # Black
    (255,204,0),          # Yellow
    (10,25,80),           # Deep Blue
    (48,25,52),           # Deep Purple
    (245,245,220),        # Beige
    (0,100,0)             # Deep Green
]

GRADIENTS = [
    ((0,0,0),(0,100,0)),      # Black → Deep Green
    ((0,0,0),(139,0,0)),      # Black → Deep Red
    ((0,0,0),(10,25,80))      # Black → Deep Blue
]
# =======================

def create_horizontal_gradient(size, color1, color2, reverse=False):
    img = Image.new("RGB", (size, size))
    draw = ImageDraw.Draw(img)
    for x in range(size):
        ratio = x / size
        if reverse:
            ratio = 1 - ratio
        r = int(color1[0]*(1-ratio) + color2[0]*ratio)
        g = int(color1[1]*(1-ratio) + color2[1]*ratio)
        b = int(color1[2]*(1-ratio) + color2[2]*ratio)
        draw.line([(x,0),(x,size)], fill=(r,g,b))
    return img

def clean_filename(text):
    text = re.sub(r'[^\w\s-]', '', text)
    return text.strip().replace(" ", "_")[:100] + ".png"

def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = current + " " + word if current else word
        w = draw.textlength(test, font=font)
        if w <= max_width:
            current = test
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines

# Load Google Sheet as CSV
csv_url = f"https://docs.google.com/spreadsheets/d/1YfpDVqaxkUB4NxE9l336I95707Ajchjhwz3MUM-X2_8/gviz/tq?tqx=out:csv&sheet=Sheet 1"
df = pd.read_csv(csv_url)

if not os.path.exists("output"):
    os.makedirs("output")

for _, row in df.iterrows():
    text = str(row["text"]).strip()
    
    # Choose background
    if random.choice([True, False]):
        bg_color = random.choice(SOLID_COLORS)
        img = Image.new("RGB", (IMAGE_SIZE, IMAGE_SIZE), bg_color)
    else:
        g = random.choice(GRADIENTS)
        reverse = random.choice([True, False])
        img = create_horizontal_gradient(IMAGE_SIZE, g[0], g[1], reverse)

    draw = ImageDraw.Draw(img)
    
    # Choose font
    font_path = random.choice(FONTS)
    font_size = random.randint(70,100)
    font = ImageFont.truetype(font_path, font_size)
    
    # Wrap text
    max_width = IMAGE_SIZE * 0.8
    lines = wrap_text(draw, text, font, max_width)
    
    # Center vertical
    total_height = sum(draw.textbbox((0,0), line, font=font)[3] for line in lines) + (len(lines)-1)*15
    current_y = (IMAGE_SIZE - total_height)/2
    
    for line in lines: 
