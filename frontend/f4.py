import streamlit as st
from streamlit_option_menu import option_menu
import base64
import requests
import zipfile
import os
import shutil
import gdown
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
from natsort import natsorted
import time

NGROK_URL = "https://8ab3-34-16-207-187.ngrok-free.app"

# List of background images for the slideshow
background_images = [
    "images/img_bg1.jpg",
    "images/img_bg2.jpg",
    #"images/img_bg3.jpg",
    "images/img_bg4.jpg",
    "images/img_bg5.jpg",
    "images/img_bg6.jpg",
    "images/img_bg7.jpg",
    "images/img_bg8.jpg"
]

#function
def download_and_unzip_from_gdrive(gdrive_url, download_dir, output_folder_name="output"):
    """Download and extract ZIP file from Google Drive (force re-download)"""
    # Make sure the download directory exists
    os.makedirs(download_dir, exist_ok=True)

    # Create unique folder name with timestamp to avoid conflicts
    timestamp = str(int(time.time()))
    unique_folder_name = f"{output_folder_name}_{timestamp}"
    
    # Path to save the ZIP file
    zip_path = os.path.join(download_dir, f"output_{timestamp}.zip")

    # Path to extract files to
    output_path = os.path.join(download_dir, unique_folder_name)
    
    # Clean up existing files
    if os.path.exists(zip_path):
        os.remove(zip_path)
    if os.path.exists(output_path):
        shutil.rmtree(output_path)

    # Download ZIP file from Google Drive link
    print(f"Downloading ZIP file to {zip_path}...")
    try:
        gdown.download(gdrive_url, zip_path, quiet=False, fuzzy=True)
    except Exception as e:
        print(f"Error downloading file: {e}")
        return None

    # Extract ZIP file contents to output directory
    if os.path.exists(zip_path) and zipfile.is_zipfile(zip_path):
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
        return False

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
        try:
            tts = gTTS(text=caption)
            tts.save(audio_path)
        except Exception as e:
            print(f"Error creating TTS for {image_name}: {e}")
            continue

        # Load audio to get duration
        try:
            audio_clip = AudioFileClip(audio_path)
            duration = audio_clip.duration

            # Create image clip and set duration/audio
            img_clip = ImageClip(image_path).set_duration(duration).set_audio(audio_clip)
            clips.append(img_clip)
        except Exception as e:
            print(f"Error processing {image_name}: {e}")
            continue

    if not clips:
        print("No valid clips created.")
        return False

    # Combine all clips
    print("Creating final video...")
    try:
        final_clip = concatenate_videoclips(clips)
        final_clip.write_videofile(output_path, fps=24)
        print(f"Video saved to: {output_path}")
        
        # Clean up clips to free memory
        for clip in clips:
            clip.close()
        final_clip.close()
        
        return True
    except Exception as e:
        print(f"Error creating final video: {e}")
        return False

# Function to add background slideshow using only CSS
def add_bg_from_local_slideshow_css(image_list, interval_sec=5):
    encoded_images = []
    for path in image_list:
        try:
            with open(path, "rb") as file:
                encoded = base64.b64encode(file.read()).decode()
                encoded_images.append(f"data:image/png;base64,{encoded}")
        except Exception as e:
            print(f"Error loading background image {path}: {e}")
            continue

    if not encoded_images:
        return

    num_images = len(encoded_images)
    percent_per_image = 100 / num_images

    keyframes = ""
    for i in range(num_images):
        percent_start = i * percent_per_image
        percent_end = (i + 1) * percent_per_image
        keyframes += f"""
        {percent_start}% {{ background-image: url('{encoded_images[i]}'); }}
        {percent_end}% {{ background-image: url('{encoded_images[i]}'); }}
        """

    css = f"""
    <style>
    .stApp {{
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        animation: bgSlide {interval_sec * num_images}s infinite;
        transition: background-image 1s ease-in-out;
    }}

    @keyframes bgSlide {{
        {keyframes}
    }}
    </style>
    """

    st.markdown(css, unsafe_allow_html=True)

def add_video_background(video_path: str):
    try:
        with open(video_path, "rb") as video_file:
            base64_video = base64.b64encode(video_file.read()).decode()

        video_html = f"""
        <style>
        .stApp {{
            background: none !important;
        }}
        video.background-video {{
            position: fixed;
            top: 0;
            left:0;
            bottom: 0;
            right: 0;
            width: 100%
        }}
        </style>
        <video class="background-video" autoplay muted loop>
            <source src="data:video/mp4;base64,{base64_video}" type="video/mp4">
        </video>
        """
        st.markdown(video_html, unsafe_allow_html=True)
    except Exception as e:
        print(f"Error loading video background: {e}")

# ----------------------------------------
# App UI starts here
# ----------------------------------------

st.set_page_config(page_title='Fission AI', page_icon='images/ai_icon.png', layout="centered")
st.markdown("## FISSION AI ✨")

# Sidebar Menu
with st.sidebar:
    selected = option_menu("Fission AI ✨", ["🖼️ Text to Image Model", '🎞️ Text to Video Model', '🌌 Image to Video Model','🗒️ Text to Text Model'],
        icons=[' ', ' ', ' ', ' '], menu_icon=" ", default_index=0)
    
    st.markdown(
    """<hr style="margin-top: -10px;">""", 
    unsafe_allow_html=True)

    col11, col22 =  st.columns((1,1))
    with col11:
        st.button("📊 VISIO AI")
    with col22:
        st.button("💻 NeuraShell")
    
    st.markdown("<br>",unsafe_allow_html= True)
    st.markdown("<br>",unsafe_allow_html= True)
    st.markdown("<br>",unsafe_allow_html= True)
    
    col33, col44 =  st.columns((1,1))
    with col33:
        if st.button("🗑️ Clear Data"):
            st.session_state.image_history = []
    with col44:
        st.button("⚙️ Account")

# Session state to hold history
if 'image_history' not in st.session_state:
    st.session_state.image_history = []

# Main Area
if selected == "🖼️ Text to Image Model":
    # Background slideshow
    add_bg_from_local_slideshow_css(background_images, interval_sec=5)

    st.subheader("AI Image Generator")
    st.write(' ')
    st.write(' ')
    st.write(' ')
    st.write(' ')
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

    # Input
    with st.form(key="image_prompt_form", clear_on_submit=True):
        prompt = st.text_input(label="Enter prompt", placeholder="e.g. cat and dog are fighting")
        submit = st.form_submit_button("Generate")

    # On submit
    if submit and prompt:
        response = f"🖼️ Generated image for: **{prompt}**"
        st.session_state.image_history.append((prompt, response))

    # Display conversation-like history
    for idx, (user_prompt, response) in enumerate(reversed(st.session_state.image_history), 1):
        with st.chat_message("user"):
            st.markdown(f"**Prompt {idx}:** {user_prompt}")
        with st.chat_message("assistant"):
            st.markdown(response)

elif selected == "🎞️ Text to Video Model":
    add_video_background("videos/backvid.mp4")
    st.subheader("AI Video Generator")
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

    # Input
    prompt = st.text_input(label="Enter prompt", placeholder="e.g. cat and dog are fighting")
    submit = st.button('Generate')

    # On submit
    if submit and prompt:
        with st.spinner("Sending prompt to backend..."):
            try:
                # Send request to backend
                response = requests.post(f"{NGROK_URL}/generate", json={"prompt": prompt}, timeout=300)
                
                if response.ok:
                    response_data = response.json()
                    
                    # ✅ GET THE GOOGLE DRIVE LINK FROM BACKEND RESPONSE
                    # Your backend should return something like:
                    # {"gdrive_link": "https://drive.google.com/file/d/NEW_FILE_ID/view?usp=sharing"}
                    
                    if "gdrive_link" in response_data:
                        gdrive_link = response_data["gdrive_link"]
                    else:
                        # Fallback - but you should fix your backend to return the link
                        st.error("Backend didn't return Google Drive link. Using fallback.")
                        gdrive_link = "https://drive.google.com/file/d/1-4Z_aA8FEEjsTvVc09YzAAwgYO_VWFG1/view?usp=sharing"
                    
                    download_folder = "E://sbssu_arshvir_fission_ai//assets"
                    timestamp = str(int(time.time()))
                    video_output = os.path.join(download_folder, f"final_narrated_video_{timestamp}.mp4")

                    # Step 1: Download and extract files
                    with st.spinner("Downloading generated content..."):
                        extracted_folder = download_and_unzip_from_gdrive(gdrive_link, download_folder, "output")
            
                    if extracted_folder:
                        # Step 2: Create narrated video from extracted files
                        with st.spinner("Creating narrated video..."):
                            success = create_narrated_video(extracted_folder, video_output)
                            
                        if success and os.path.exists(video_output):
                            st.success(f"✅ Video generated successfully for: **{prompt}**")
                            st.video(video_output)
                            
                            # Add to history
                            response_msg = f"🎞️ Generated video for: **{prompt}**"
                            st.session_state.image_history.append((prompt, response_msg))
                        else:
                            st.error("❌ Failed to create video from generated content.")
                    else:
                        st.error("❌ Failed to download or extract files from Google Drive.")
                        
                else:
                    st.error(f"❌ Error from backend: {response.status_code}")
                    
            except requests.exceptions.Timeout:
                st.error("❌ Request timed out. The backend is taking too long to respond.")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Network error: {str(e)}")
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")

    # Display conversation-like history
    for idx, (user_prompt, response) in enumerate(reversed(st.session_state.image_history), 1):
        with st.chat_message("user"):
            st.markdown(f"**Prompt {idx}:** {user_prompt}")
        with st.chat_message("assistant"):
            st.markdown(response)