# 🎵 MP4 → MP3 Converter

A clean, fast Streamlit web app that extracts and converts audio from video files into compressed MP3s — powered by FFmpeg's **libmp3lame** encoder.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B?logo=streamlit&logoColor=white)
![FFmpeg](https://img.shields.io/badge/FFmpeg-required-green?logo=ffmpeg&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## ✨ Features

- 🎬 **Multi-format input** — MP4, MKV, AVI, MOV, WEBM
- 🎵 **High-quality MP3 output** — using FFmpeg's libmp3lame encoder
- 📦 **Smart compression** — choose from preset quality levels or dial in a custom bitrate
- 🗂️ **Batch conversion** — upload and convert multiple files at once
- 📊 **Conversion stats** — see original size, output size, % reduction, and time taken per file
- ⬇️ **Instant download** — download button appears right after each conversion
- 🔒 **Privacy-first** — no files are stored server-side; all processing happens in temporary directories that are deleted after each conversion

---

## 🖥️ Screenshots

> _Add your own screenshots here after running the app._

---

## ⚙️ Quality Settings

| Preset | Bitrate | Best For |
|---|---|---|
| High | 320 kbps | Music, high-fidelity audio |
| Standard | 192 kbps | General video, balanced quality/size |
| Compact | 128 kbps | Podcasts, casual listening |
| Custom | 64–320 kbps | Full manual control |

Additional controls:

- **Sample Rate** — 44100 Hz (CD), 48000 Hz (Studio), 22050 Hz (smaller file)
- **Channels** — Stereo or Mono (mono halves file size, ideal for voice/speech)

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- FFmpeg installed on your system

#### Install FFmpeg

**Ubuntu / Debian**
```bash
sudo apt update && sudo apt install ffmpeg
```

**macOS**
```bash
brew install ffmpeg
```

**Windows**

Download the latest build from [ffmpeg.org/download.html](https://ffmpeg.org/download.html), extract it, and add the `bin` folder to your system `PATH`.

Verify installation:
```bash
ffmpeg -version
```

---

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/mp4-to-mp3-converter.git
   cd mp4-to-mp3-converter
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**
   ```bash
   streamlit run mp4_to_mp3_converter.py
   ```

4. Open your browser at `http://localhost:8501`

---

## 📁 Project Structure

```
mp4-to-mp3-converter/
├── mp4_to_mp3_converter.py   # Main Streamlit application
├── requirements.txt          # Python dependencies
├── packages.txt              # System packages (for cloud deployment)
└── README.md                 # This file
```

---

## ☁️ Deploy to Streamlit Community Cloud

1. Push the repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect your repo
3. Make sure both files below are present in the root of your repo:

**`requirements.txt`**
```
streamlit>=1.35.0
```

**`packages.txt`**
```
ffmpeg
```

Streamlit Cloud will install FFmpeg as a system package automatically before starting the app.

---

## 🛠️ How It Works

1. The user uploads one or more video files via the Streamlit file uploader
2. Each file is saved to a secure temporary directory
3. FFmpeg is invoked via Python's `subprocess` module with the following flags:
   - `-vn` — strips the video stream, keeping only audio
   - `-c:a libmp3lame` — encodes audio using the libmp3lame MP3 encoder
   - `-b:a` — sets the target bitrate (e.g. `192k`)
   - `-ar` — sets the sample rate
   - `-ac` — sets the number of audio channels
   - `-q:a 2` — applies a VBR quality hint for optimal encoding
4. The output MP3 is served back to the user as a download
5. Temporary files are deleted immediately after the conversion

---

## 📋 Requirements

| Package | Version |
|---|---|
| streamlit | >= 1.35.0 |
| ffmpeg _(system)_ | any recent version |

---

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request for:

- Additional output formats (OGG, WAV, AAC)
- Audio waveform preview after conversion
- Progress bar tied to FFmpeg's real-time output
- Drag-and-drop reordering for batch jobs

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙏 Acknowledgements

- [FFmpeg](https://ffmpeg.org/) — the backbone of the conversion pipeline
- [Streamlit](https://streamlit.io/) — for making Python web apps effortless
- [libmp3lame](https://lame.sourceforge.io/) — the LAME MP3 encoder library
