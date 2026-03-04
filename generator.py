import os
import random
import re
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

# ===== SETTINGS =====
SHEET_ID = "1YfpDVqaxkUB4NxE9l336I95707Ajchjhwz3MUM-X2_8"
SHEET_NAME = "Sheet1"
IMAGE_SIZE = 1080

# Always use Poppins
FONT_PATH = "fonts/Poppins-SemiBold.ttf"

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
            if current:
                lines.append(current)
            current = word

    if current:
        lines.append(current)

    return lines


# Load Google Sheet
csv_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"
df = pd.read_csv(csv_url)

if not os.path.exists("output"):
    os.makedirs("output")


for _, row in df.iterrows():

    text = str(row["text"]).strip()

    # Choose background
    if random.choice([True, False]):
        bg_color = random.choice(SOLID_COLORS)
        img = Image.new("RGB", (IMAGE_SIZE, IMAGE_SIZE), bg_color)
        background_type = "solid"
    else:
        g = random.choice(GRADIENTS)
        reverse = random.choice([True, False])
        img = create_horizontal_gradient(IMAGE_SIZE, g[0], g[1], reverse)
        background_type = "gradient"

    draw = ImageDraw.Draw(img)

    # TEXT COLOR RULES
    if background_type == "solid" and bg_color in [(255,255,255),(255,204,0)]:
        text_color = "black"
        stroke_width = 0
        stroke_color = None
    else:
        text_color = "white"
        stroke_width = 3
        stroke_color = "black"

    # Dynamic font scaling (≈70% width)
    font_size = 40
    font = ImageFont.truetype(FONT_PATH, font_size)
    max_width = IMAGE_SIZE * 0.7

    while True:

        lines = wrap_text(draw, text, font, max_width)

        longest = max(draw.textlength(line, font=font) for line in lines)

        if longest >= max_width:
            break

        font_size += 4
        font = ImageFont.truetype(FONT_PATH, font_size)

    # Calculate vertical centering
    line_spacing = int(font_size * 0.25)

    total_height = sum(
        draw.textbbox((0,0), line, font=font)[3] for line in lines
    ) + (len(lines)-1)*line_spacing

    current_y = (IMAGE_SIZE - total_height) / 2

    for line in lines:

        w = draw.textlength(line, font=font)
        x = (IMAGE_SIZE - w) / 2

        draw.text(
            (x, current_y),
            line,
            font=font,
            fill=text_color,
            stroke_width=stroke_width,
            stroke_fill=stroke_color
        )

        current_y += font_size + line_spacing

    # Save
    filename = clean_filename(text)
    img_path = os.path.join("output", filename)
    img.save(img_path)


print("All designs generated locally in 'output/' folder!") 
