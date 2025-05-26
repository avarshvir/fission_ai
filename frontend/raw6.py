import os
import zipfile
import gdown
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
from natsort import natsorted

def download_and_unzip_from_gdrive(gdrive_url, download_dir, output_folder_name="output"):
    """Download and extract ZIP file from Google Drive"""
    # Make sure the download directory exists
    os.makedirs(download_dir, exist_ok=True)

    # Path to save the ZIP file
    zip_path = os.path.join(download_dir, "output.zip")

    # Path to extract files to
    output_path = os.path.join(download_dir, output_folder_name)
    os.makedirs(output_path, exist_ok=True)

    # Download ZIP file from Google Drive link
    print(f"Downloading ZIP file to {zip_path}...")
    gdown.download(gdrive_url, zip_path, quiet=False, fuzzy=True)

    # Extract ZIP file contents to output directory
    if zipfile.is_zipfile(zip_path):
        print(f"Unzipping file to {output_path}...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(output_path)
        print(f"Files extracted to: {output_path}")
        return output_path
    else:
        print("Downloaded file is not a valid ZIP archive.")
        return None

def create_narrated_video(image_folder, output_path):
    """Create narrated video from images and text files"""
    image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
    image_files = natsorted(image_files)

    if not image_files:
        print("No images found.")
        return

    clips = []

    for image_name in image_files:
        base_name = os.path.splitext(image_name)[0]
        image_path = os.path.join(image_folder, image_name)
        caption_path = os.path.join(image_folder, base_name + '.txt')

        # Load caption
        caption = ""
        if os.path.exists(caption_path):
            with open(caption_path, 'r', encoding='utf-8') as f:
                caption = f.read().strip()
        else:
            caption = "No caption available"

        # Convert caption to audio using gTTS
        audio_path = os.path.join(image_folder, base_name + ".mp3")
        tts = gTTS(text=caption)
        tts.save(audio_path)

        # Load audio to get duration
        audio_clip = AudioFileClip(audio_path)
        duration = audio_clip.duration

        # Create image clip and set duration/audio
        img_clip = ImageClip(image_path).set_duration(duration).set_audio(audio_clip)
        clips.append(img_clip)

    # Combine all clips
    print("Creating final video...")
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(output_path, fps=24)
    print(f"Video saved to: {output_path}")

def main():
    """Main function to download, extract, and create video"""
    # Configuration
    gdrive_link = "https://drive.google.com/file/d/1-4Z_aA8FEEjsTvVc09YzAAwgYO_VWFG1/view?usp=sharing"
    #->download_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    download_folder = "E://sbssu_arshvir_fission_ai//assets"
    output_folder_name = "output"
    video_output = os.path.join(download_folder, "final_narrated_video.mp4")
    
    # Step 1: Download and extract files
    extracted_folder = download_and_unzip_from_gdrive(gdrive_link, download_folder, output_folder_name)
    
    if extracted_folder:
        # Step 2: Create narrated video from extracted files
        create_narrated_video(extracted_folder, video_output)
    else:
        print("Failed to extract files. Cannot proceed with video creation.")

if __name__ == "__main__":
    main()