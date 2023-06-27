import os
from PIL import Image

# Set the directory you want to start from
rootDir = "/Users/jacobcurtis/Desktop/Coursework/graphics/npc_characters1/npc2"

# Iterate through every subfolder
for dirName, subdirList, fileList in os.walk(rootDir):
    # Iterate through every file
    for fname in fileList:
        # Check if the file is an image
        if fname.endswith('.jpg') or fname.endswith('.png'):
            # Construct the full path to the image
            image_path = os.path.join(dirName, fname)
            # Load the image
            image = Image.open(image_path)
            # Resize the image to 28x28 pixels
            image_resized = image.resize((40, 60))
            # Construct the full path to save the resized image
            # Save the resized image
            image_resized.save(image_path)

