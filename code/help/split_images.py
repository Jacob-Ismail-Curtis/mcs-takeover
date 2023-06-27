import cv2
import os

folder_path = '/Users/jacobcurtis/Desktop/Coursework/graphics/robots/drone4/move'
image_count=4

for filename in os.listdir(folder_path):
    if filename.endswith('.png'):
        im = cv2.imread(os.path.join(folder_path, filename), cv2.IMREAD_UNCHANGED)
        width, height = im.shape[1], im.shape[0]
        for i in range(image_count):
            left = int(i * (width / image_count))
            right = int((i + 1) * (width / image_count))
            im_cropped = im[:, left:right, :]
            cv2.imwrite(os.path.join(folder_path, f"{filename}_{i}.png"), im_cropped, [cv2.IMWRITE_PNG_COMPRESSION, 9])
