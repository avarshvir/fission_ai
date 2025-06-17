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
