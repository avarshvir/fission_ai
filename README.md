# Fission AI
#### 🧠 Text ↔️ Images ↔️ Video Generator

This project enables users to **enter a text prompt**, which is transformed into a **series of AI-generated images**, then combined into a **slideshow-style video**, and finally **explained through NLP-based narration with synthesized audio**. It blends the power of **deep learning**, **computer vision**, and **transformer-based NLP models** to deliver an immersive visual and audio storytelling experience.

---

## 🚀 Features

- ✍️ **Text-to-Image Generation**: Produces 5–6 unique images using deep learning models based on user input.
- 🧠 **NLP-Based Description**: Analyzes the generated images and creates a meaningful explanation using advanced NLP techniques.
- 🎬 **Image-to-Video Conversion**: Combines images into a smooth, slideshow-style visual sequence using OpenCV.
- 🔊 **Text-to-Speech Narration**: Converts the generated description into speech for audio playback.
- 🖥️ **Streamlit Interface**: Interactive and user-friendly frontend for prompt input and result display.
- 🔙 **Flask Backend**: Manages API endpoints and logic for integrating various components.
- ☁️ **Colab Integration**: Trains and hosts models efficiently using Google Colab.
- 💾 **Scalable Storage Ready**: Prepared for MySQL integration to manage future user data and session history.

---

## 🧰 Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Backend**: [Flask](https://flask.palletsprojects.com/)
- **Model Training & Hosting**: Google Colab
- **Image Processing**: OpenCV
- **NLP & Transformers**: Hugging Face Transformers, RAG (Retrieval-Augmented Generation)
- **Speech Synthesis**: [pyttsx3](https://pypi.org/project/pyttsx3/) or similar TTS tool
- **Database (Future-Ready)**: MySQL

---

## 📦 Setup and Installation

### Clone the Repository

```bash
git clone https://github.com/avarshvir/fission_ai.git
cd fission_ai
```

### Create and Activate Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install required Python packages
```bash
pip install -r requirements.txt
```

## Future Enhancements

* **Real-time Video Generation:** Instead of a static video, explore dynamic video generation based on the image sequence.
* **Interactive Image Editing:** Allow users to modify the generated images or provide feedback for refinement.
* **More Advanced NLP:** Implement more sophisticated NLP techniques for deeper image understanding and more nuanced explanations.
* **User Accounts and Data Storage:** Integrate MySQL to manage user accounts, save generated images and prompts, and personalize the experience.
* **Improved Audio Quality:** Explore different text-to-speech engines for higher-quality and more natural-sounding audio.
* **Integration with External APIs:** Connect to other AI services or APIs to enhance the functionality.
* **Performance Optimization:** Optimize the image generation, video creation, and NLP processing for faster response times.

## Credits and Acknowledgements

- **Libraries and Frameworks:** TensorFlow, Scikit-Learn, Transformers, OpenCV, pyttsx3
- **ML Tech:** RAG's, CNN, GAN's

## License

* yet to specify

---
    

