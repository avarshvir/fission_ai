import streamlit as st
from streamlit_option_menu import option_menu
import base64
import requests
import zipfile
import os
import shutil

NGROK_URL = "https://9f9a-34-124-221-72.ngrok-free.app"

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
    selected = option_menu("Fission AI ✨", ["🖼️ Text to Image Model", '🎞️ Text to Video Model', '🌌 Image to Video Model','🗒️ Text to Text Model'],
        icons=[' ', ' ', ' ', ' '], menu_icon=" ", default_index=0)
        # Clear button
    #st.markdown("<hr style:margin-top :"-20px";>", unsafe_allow_html=True)
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
            download_url = response.json()["download_url"]
            zip_path = os.path.join("downloads", "output.zip")

            # Create downloads folder if it doesn't exist
            os.makedirs("downloads", exist_ok=True)

            with st.spinner("Downloading and extracting files..."):
                with requests.get(download_url, stream=True) as r:
                    with open(zip_path, "wb") as f:
                        shutil.copyfileobj(r.raw, f)

                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall("downloads/output")

                st.success("Files extracted!")

            # Now call convert_video.py
            from convert_video import create_video_with_audio
            video_path = create_video_with_audio("output")

            st.video(video_path)
        else:
            st.error("Error from backend")


    # Display conversation-like history
    for idx, (user_prompt, response) in enumerate(reversed(st.session_state.image_history), 1):
        with st.chat_message("user"):
            st.markdown(f"**Prompt {idx}:** {user_prompt}")
        with st.chat_message("assistant"):
            st.markdown(response)