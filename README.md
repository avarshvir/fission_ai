![Apache License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![Flask](https://img.shields.io/badge/Backend-Flask-green.svg)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-orange.svg)
![Status](https://img.shields.io/badge/Status-In_Development-yellow.svg)
![Platform](https://img.shields.io/badge/Platform-Google_Colab-lightgrey.svg)
![Contributions](https://img.shields.io/badge/Contributions-Welcome-brightgreen.svg)
![Made with ♥](https://img.shields.io/badge/Made_with-%E2%99%A5-red.svg)

[![GitHub issues](https://img.shields.io/github/issues/avarshvir/fission_ai)](https://github.com/avarshvir/fission_ai/issues)
[![GitHub forks](https://img.shields.io/github/forks/avarshvir/fission_ai)](https://github.com/avarshvir/fission_ai/network)
[![GitHub stars](https://img.shields.io/github/stars/avarshvir/fission_ai)](https://github.com/avarshvir/fission_ai/stargazers)
[![GitHub last commit](https://img.shields.io/github/last-commit/avarshvir/fission_ai)](https://github.com/avarshvir/fission_ai)

# 🚀 Fission AI

**Fission AI** is a powerful, multimodal AI platform that combines state-of-the-art models and tools to transform text into images, videos, research reports, and more. It is designed for creators, educators, developers, and researchers who want seamless AI-powered content generation — all from a single interface.

---

## 🔮 Key Features

- **🖼️ Text to Image**  
  Generate up to 5 high-quality images using **Stable Diffusion**.  
  Captions generated with **BLIP**.

- **🎬 Text to Video**  
  Automatically stitches images into a video with generated narration using **gTTS**.

- **💬 Text to Text**  
  Uses **Gemma 3B (via Ollama)** to generate or rewrite text with LLM capabilities.

- **📚 Text to Deep Research**  
  - Extracts keywords
  - Searches the web using **DuckDuckGo API**
  - Summarizes findings using **Gemma 3B**
  - Generates a downloadable **PDF report**

---

## 🧠 Tech Stack

| Category             | Tools / Frameworks                         |
|----------------------|---------------------------------------------|
| Backend              | Flask, Python, ngrok, Google Colab         |
| Frontend             | Streamlit                                  |
| Machine Learning     | PyTorch, BLIP, Stable Diffusion, Gemma 3B  |
| Text-to-Speech       | gTTS                                        |
| LLM Integration      | Ollama (Gemma 3B)                           |
| Web Search           | DuckDuckGo API                             |
| Video & Audio Tools  | FFmpeg, MoviePy                            |
| IDE / Development    | VS Code                                    |
| Hosting / Tunnel     | ngrok                                       |

---

## 🏗️ System Architecture

```bash
User (Streamlit App)
      │
      ▼
[Frontend: Streamlit] ─────────┐
                               ▼
        [Backend: Flask server (ngrok tunnel)]
                               │
           ┌────────────┬──────┼───────────┬────────────┐
           ▼            ▼      ▼           ▼            ▼
[Stable Diffusion] [BLIP] [gTTS] [Gemma 3B] [DuckDuckGo API]
                               │
                          [Google Colab Runtime]
                               │
                         [Returns ZIP / PDF / MP4]

```
---
## ⚙️ Installation & Setup
```⚠️ Note: This project uses Google Colab as the backend runtime, tunneled using ngrok.```
#### 1. Clone the repository
```
git clone https://github.com/avarshvir/fission_ai.git
cd fission_ai
```

#### 2. Install dependencies
```
pip install -r requirements.txt
```

#### 3. Set up ngrok
```
- get ngrok token after setting your account on ngrok.
- add your token 
    - NGROK_AUTH_TOKEN = "your ngrok token" in main_model.ipynb google colab
- run the all cell of main_model.ipynb
- get ngrok url from colab output and place the url in main.py file that act as backend
    - NGROK_URL = "ngrok_url" 

```

#### 4. Make Google Drive Link Public
```
- create a folder name "GeneratedImages" inside mydrive of google drive.
- make "GeneratedImages" folder public and copy the link.
- place public link in main.py file gdrive_link = "public drive link" 2 times.
```

#### 5. Launch the Streamlit frontend
```
after cd fission_ai
cd frontend
streamlit run main.py
```

#### 6. Choose your option and see results
```
Text-to-Image
Text-to-Video
Text-to-Text
Text-to Deep Research
```

---

## ⚠️ Note:
```
make sure you download dependencies, setup your ngrok account, 
public your "GeneratedImages" folder of Google Drive, 
and choose T4 GPU of Google Colab.
```

---

## 📦 Folder Structure
```
fission_ai/
│
├── assets
|   ├── output
|   ├── final_narrated_video   # Stitch images/audio to final video
|   └── output.zip             # Stitch images/audio to final video
|
├── backend/
│   └── backend.txt
|
├── data/
│   └── dataset_links.txt
│
├── frontend/
│   ├── images
|   ├── resized_images
|   ├── videos
|   ├── keyword_search.py
|   ├── main.py               # Actual Main file
|   ├── summarizer.py
|   └── text_query.py
|
├── model/
│   ├── main_model.ipynb      # main file for google colab
|   ├── model.txt
|   └── ok8.ipynb
|
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE
├── NOTICE
├── README.md
└── requirements.txt
```

---
## 💡 Future Plans
- Add user authentication & plans (Free, Pro, AI+, Enterprise)

- Provide cloud-based persistent storage

- Rate-limited access to premium APIs

- Launch SaaS version under Jaiho Labs (Subsidiary of Jaiho Digital)

--- 
## 🤝 Contributing
Contributions are welcome! Please follow these steps:

1. Fork the repo

2. Create your feature branch (git checkout -b feature-name)

3. Commit your changes (git commit -am 'Add new feature')

4. Push to the branch (git push origin feature-name)

5. Open a pull request

---
## 📬 Contact
- Author: Arshvir 

--- 
## 🌟 Star this repo to support the project!

---

Let me know if you’d like a `LICENSE` file, `requirements.txt`, or deployment script to go along with this!

