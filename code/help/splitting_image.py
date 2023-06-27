import os
from PIL import Image

# Set the input and output folder paths
input_folder_path = "/Users/jacobcurtis/Desktop/Coursework/graphics/robots/drone2/attack"
output_folder_path = "/Users/jacobcurtis/Desktop/Coursework/graphics/robots/drone2/attack"

# Loop through all files in the input folder
for root, dirs, files in os.walk(input_folder_path):
    for file in files:
        # Check if the file is an image
        if file.endswith(".jpg") or file.endswith(".png"):
            # Open the image
            img = Image.open(os.path.join(root, file))

            # Get the width and height of the image
            width, height = img.size

            # Calculate the number of 32x32 images that can be extracted from the image
            num_images = width // 32

            # Loop through the images, extracting and saving each one
            for i in range(num_images):
                # Extract the 32x32 image from the original image
                extracted_img = img.crop((i*32, 0, (i+1)*32, 32))

                # Save the extracted image to the output folder, with a name starting from 0
                extracted_img.save(os.path.join(output_folder_path, str(i) + ".png"))
print('Finished')