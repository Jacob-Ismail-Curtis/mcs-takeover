import os
from PIL import Image

# Set the folder path
folder_path = "/Users/jacobcurtis/Desktop/Coursework/graphics/test"

# Loop through all subfolders
for root, dirs, files in os.walk(folder_path):
    for file in files:
        #print(file)
        # Check if the file is an image
        if file.endswith(".jpg") or file.endswith(".png"):
            # Open the image
            img = Image.open(os.path.join(root, file))

            # Scale the image down to 32x32 pixels
            img = img.resize((32, 32), Image.ANTIALIAS)

            # Save the scaled image
            img.save(os.path.join(root, file))
#print('Finished')