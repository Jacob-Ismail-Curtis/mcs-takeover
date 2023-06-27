import os
from PIL import Image

folder_path = '/Users/jacobcurtis/Desktop/Coursework/graphics/guns1' # replace with the actual path to the folder containing the images

for filename in os.listdir(folder_path):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        file_path = os.path.join(folder_path, filename)
        with Image.open(file_path) as img:
            width, height = img.size
            img = img.resize((width * 2, height * 2))
            img.save(file_path)
            print(f"{filename} scaled and saved.")
    else:
        print(f"{filename} is not an image.")
