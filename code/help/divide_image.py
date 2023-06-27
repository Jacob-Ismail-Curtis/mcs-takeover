from PIL import Image
import os
# Suppress the warning
# Load the image
# Get the size of each piece
img=Image.open("/Users/jacobcurtis/Desktop/player/")
w, h = 32, 48

# Split the image into 16 pieces
for i in range(16):
    x = i % 4 * w
    y = i // 4 * h
    piece = img.crop((x, y, x + w, y + h))
    piece.save(f"{i}.jpg")
