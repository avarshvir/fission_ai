import cv2
import os
from gtts import gTTS

def create_video_with_audio(image_folder, output_file="final_video.mp4", fps=1):
    images = sorted([img for img in os.listdir(image_folder) if img.endswith(".png")])
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    for image in images:
        img_path = os.path.join(image_folder, image)
        video.write(cv2.imread(img_path))

    video.release()
    return output_file
