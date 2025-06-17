import streamlit as st
from streamlit_option_menu import option_menu
import base64
import requests
import zipfile
import os
import shutil
from summarizer import summarize_text
from keyword_search import extract_keywords, search_web_articles, fetch_article_text
from fpdf import FPDF
import unicodedata
from text_query import text_query_response
import gdown
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
from natsort import natsorted
import uuid
import time

NGROK_URL = "ngrok_url"

# background images for the slideshow
background_images = [
    "images/img_bg1.jpg",
    "images/img_bg2.jpg",
    "images/img_bg4.jpg",
    "images/img_bg5.jpg",
    "images/img_bg6.jpg",
    "images/img_bg7.jpg",
    "images/img_bg8.jpg"
]

#functions
def download_and_unzip_from_gdrive(gdrive_url, download_dir, output_folder_name="output"):
    """Download and extract ZIP file from Google Drive (force re-download)"""
    os.makedirs(download_dir, exist_ok=True)

    # path of ZIP file for save
    zip_path = os.path.join(download_dir, "output.zip")

    # Path to extract files to
    output_path = os.path.join(download_dir, output_folder_name)
    if os.path.exists(zip_path):
        os.remove(zip_path)
    if os.path.exists(output_path):
        shutil.rmtree(output_path)
    
    # Download ZIP file from Google Drive link which is already public by user
    print(f"Downloading ZIP file to {zip_path}...")
    gdown.download(gdrive_url, zip_path, quiet=False, fuzzy=True)

    # Extract ZIP file contents to output local system path
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


def sanitize_text(text):
    # Normalize and replace problematic characters with closest ASCII equivalents
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')

#download
def generate_pdf(summary_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    clean_text = sanitize_text(summary_text)

    for line in clean_text.split('\n'):
        pdf.multi_cell(0, 10, line)

    pdf_output = pdf.output(dest='S').encode('latin1')  # Return PDF as byte string
    return pdf_output


# Function to add background slideshow using only CSS
def add_bg_from_local_slideshow_css(image_list, interval_sec=5):
    encoded_images = []
    for path in image_list:
        with open(path, "rb") as file:
            encoded = base64.b64encode(file.read()).decode()
            encoded_images.append(f"data:image/png;base64,{encoded}")

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


# ----------------------------------------
# App UI starts here
# ----------------------------------------

st.set_page_config(page_title='Fission AI', page_icon='images/ai_icon.png', layout="centered")
st.markdown("## FISSION AI ✨")
#st.divider()

# Sidebar Menu
with st.sidebar:
    selected = option_menu("Fission AI ✨", ["🖼️ Text to Image Model", '🎞️ Text to Video Model', '🌌 Text to Text Model','🗒️ Text to Research Model'],
        icons=[' ', ' ', ' ', ' '], menu_icon=" ", default_index=0)
        # Clear button
    #st.markdown("<hr style:margin-top :"-20px";>", unsafe_allow_html=True)
    st.markdown(
    """<hr style="margin-top: -10px;">""", 
    unsafe_allow_html=True)

    st.markdown("### <center>Other Products</center>", unsafe_allow_html=True)

    col11, col22 =  st.columns((1,1))
    with col11:
        #st.button("📊 VISIO AI")
        st.markdown(
    """
    <a href="https://visio-ai.streamlit.app/" target="_blank">
        <button style='padding:10px 20px; font-size:16px; border:none; background-color:#D1E8E2; color:black; border-radius:5px; cursor:pointer;'>
            📊 VISIO AI
        </button>
    </a>
    """,
    unsafe_allow_html=True
    )
    with col22:
        #st.button("💻 NeuraShell")
        st.markdown(
    """
    <a href="https://github.com/Jaiho-Digital/neura-shell" target="_blank">
        <button style='padding:10px 20px; font-size:16px; border:none; background-color:#D1E8E2; color:black; border-radius:5px; cursor:pointer;'>
            💻NeuraShell
        </button>
    </a>
    """,
    unsafe_allow_html=True
    )
    
    #st.markdown("<br>",unsafe_allow_html= True)
    #st.markdown("<br>",unsafe_allow_html= True)
    st.markdown("<br>",unsafe_allow_html= True)
    
    col33, col44 =  st.columns((1,1))
    with col33:
        #if st.button("🗑️ Clear Data"):
        #    st.session_state.image_history = []
        st.markdown(
    """
    <a href="https://github.com/avarshvir/SPA_AI" target="_blank">
        <button style='padding:10px 20px; font-size:16px; border:none; background-color:#D1E8E2; color:black; border-radius:5px; cursor:pointer;'>
            🤖 SPA - AI
        </button>
    </a>
    """,
    unsafe_allow_html=True
    )
    with col44:
        #st.button("⚙️ Account")
        st.markdown(
    """
    <a href="https://github.com/avarshvir/AI-VIRSA" target="_blank">
        <button style='padding:10px 20px; font-size:16px; border:none; background-color:#D1E8E2; color:black; border-radius:5px; cursor:pointer;'>
            😇 AI - VIRSA
        </button>
    </a>
    """,
    unsafe_allow_html=True
    )
    st.markdown("<br>",unsafe_allow_html= True)
    st.markdown("##### Made by <a href='https://avarshvir.github.io/arshvir/' target='_blank'>Arshvir</a> and <a href='https://jaihodigital.onrender.com' target='_blank'>jaiho Digital</a>", unsafe_allow_html=True)



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
    #with st.form(key="image_prompt_form", clear_on_submit=True):
    prompt = st.text_input(label="Enter prompt", placeholder="e.g. cat and dog are fighting")
    submit = st.button("Generate Image")
    


    # On submit
    if submit and prompt:
        #response = f"🖼️ Generated image for: **{prompt}**"
        #st.session_state.image_history.append((prompt, response))
        with st.spinner("Sending prompt to backend...."):
            response = requests.post(f"{NGROK_URL}/generate",json={"prompt": prompt})
        if response.ok:
            time.sleep(10)
            gdrive_link = "public drive link"
            download_folder = "E://fission_ai//im_assets"
            output_folder_name = "output"
            extracted_folder = download_and_unzip_from_gdrive(gdrive_link, download_folder, output_folder_name)
            if extracted_folder:
                image_files = [f for f in os.listdir(extracted_folder) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
                for image_file in image_files:
                    image_path = os.path.join(extracted_folder, image_file)
                    st.image(image_path, caption=f"Generated: {prompt}", use_container_width=True)

                    # Optional: save to session state for history
                    #st.session_state.image_history.append((prompt, f"Displayed image: {image_file}"))
            else:
                st.error("Failed to extract image files.")

    
    # Display conversation-like history
    for idx, (user_prompt, response) in enumerate(reversed(st.session_state.image_history), 1):
        with st.chat_message("user"):
            st.markdown(f"**Prompt {idx}:** {user_prompt}")
        with st.chat_message("assistant"):
            st.markdown(response)

elif selected == "🎞️ Text to Video Model":
    add_video_background("videos/backvid.mp4")  # ✅ Path to your video
    st.subheader("AI Video Generator")
    #st.markdown('<h3 style="color: white;">AI Video Generator</h3>', unsafe_allow_html=True)
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

    # Input
    #with st.form(key="video_prompt_form", clear_on_submit=True):
    prompt = st.text_input(label="Enter prompt", placeholder="e.g. cat and dog are fighting")
    #submit = st.form_submit_button("Generate")
    submit = st.button('Generate')

    # On submit
    if submit and prompt:
        #response = f"🎞️ Generated video for: **{prompt}**"
        #st.session_state.image_history.append((prompt, response))
        with st.spinner("Sending prompt to backend..."):
            response = requests.post(f"{NGROK_URL}/generate", json={"prompt": prompt})
        if response.ok:
            time.sleep(10)
            gdrive_link = "public drive link"
            download_folder = "E://fission_ai//assets"
            output_folder_name = "output"
            video_output = os.path.join(download_folder, f"final_narrated_video_{uuid.uuid4()}.mp4")
            # Step 1: Download and extract files
            extracted_folder = download_and_unzip_from_gdrive(gdrive_link, download_folder, output_folder_name)
        
            if extracted_folder:
                # Step 2: Create narrated video from extracted files
                create_narrated_video(extracted_folder, video_output)
                st.video(video_output)
            else:
                print("Failed to extract files. Cannot proceed with video creation.")
            #download_url = response.json()["download_url"]
            #zip_path = "output.zip"
        else:
            st.error("Error from backend")



    # Display conversation-like history
    for idx, (user_prompt, response) in enumerate(reversed(st.session_state.image_history), 1):
        with st.chat_message("user"):
            st.markdown(f"**Prompt {idx}:** {user_prompt}")
        with st.chat_message("assistant"):
            st.markdown(response)

if selected == "🌌 Text to Text Model":
    st.subheader("Talk to Fission AI (Text Assistant)")
    user_input = st.text_area("Enter your query", placeholder="Ask anything...")
    if st.button("Get Response"):
        if user_input.strip():
            with st.spinner("Thinking..."):
                answer = text_query_response(user_input)
                st.markdown(f"**Answer:** {answer}")
        else:
            st.warning("Please enter a query.")


if selected == "🗒️ Text to Research Model":
    # Background slideshow
    #add_bg_from_local_slideshow_css(background_images, interval_sec=5)

    st.subheader("Your AI Researcher")
    st.write(' ')
    st.write(' ')
    st.write(' ')
    st.write(' ')
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

    # Input
    #with st.form(key="image_prompt_form", clear_on_submit=True):
    prompt = st.text_input(label="Enter prompt", placeholder="e.g. What is Nuclear Bomb?")
    submit = st.button("Deep Search")
    
    # On submit
    if submit and prompt:
        if prompt.strip():
            with st.spinner("Extracting keywords..."):
                keywords = extract_keywords(prompt)
                st.write("🔑 Extracted Keywords:", ", ".join(keywords))

            with st.spinner("Searching web..."):
                urls = search_web_articles(keywords)
                st.write("🔍 Found URLs:")
                for url in urls:
                    st.write(f"- {url}")

            all_content = ""
            with st.spinner("Fetching content from articles..."):
                for url in urls:
                    content = fetch_article_text(url)
                    all_content += content + "\n\n"

            with st.spinner("Summarizing gathered content..."):
                final_summary = summarize_text(all_content)
            st.success("🔎 Summary from Web Articles:")
            st.write(final_summary)
            # Generate PDF
            pdf_data = generate_pdf(final_summary)
            st.download_button(
                label="📄 Download Summary Report as PDF",
                data=pdf_data,
                file_name="summary.pdf",
                mime="application/pdf"
            )
            
        else:
            st.warning("Please enter some text.")


    
    # Display conversation-like history
    for idx, (user_prompt, response) in enumerate(reversed(st.session_state.image_history), 1):
        with st.chat_message("user"):
            st.markdown(f"**Prompt {idx}:** {user_prompt}")
        with st.chat_message("assistant"):
            st.markdown(response)