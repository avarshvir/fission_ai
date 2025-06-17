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
### 1. Clone the repository
```
git clone https://github.com/avarshvir/fission_ai.git
cd fission_ai
```

### 2. Install dependencies
```
pip install -r requirements.txt
```

### 3. Set up ngrok
```
- get ngrok token after setting your account on ngrok.
- add your token 
    - NGROK_AUTH_TOKEN = "your ngrok token" in main_model.ipynb google colab
- run the all cell of main_model.ipynb
- get ngrok url from colab output and place the url in main.py file that act as backend
    - NGROK_URL = "ngrok_url" 

```

### 4. Make Google Drive Link Public
```
- create a folder name "GeneratedImages" inside mydrive of google drive.
- make "GeneratedImages" folder public and copy the link.
- place public link in main.py file gdrive_link = "public drive link" 2 times.
```