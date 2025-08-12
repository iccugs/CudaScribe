# CudaScribe

GPU-powered audio transcription tool using faster-whisper (via CTranslate2 + CUDA/cuDNN). 

**Note:** This tool only transcribes audio files - you need to download audio separately using yt-dlp or provide your own audio files.

---

## Features
- **GPU-accelerated transcription** using NVIDIA CUDA for fast processing
- **Real-time progress** - see transcription segments as they're processed
- **Clean text output** - properly formatted paragraphs
- **Automatic file saving** as `filename.transcription.txt`
- **Supports multiple formats** - MP3, WAV, M4A, MP4 audio files

**What this tool does:** Transcribes existing audio files to text
**What this tool doesn't do:** Download videos or audio (use yt-dlp separately for that)

---

## Prerequisites

### 1) Python
Install Python 3.9+ and confirm it is on PATH:
```bash
python --version
```

### 2) NVIDIA stack (for GPU acceleration)
- NVIDIA GPU driver (current Studio or Game Ready)
- CUDA Toolkit 12.x (12.3+ recommended): https://developer.nvidia.com/cuda-downloads
- cuDNN 9.x matching your CUDA 12.x: https://developer.nvidia.com/cudnn

Windows note: After installing cuDNN, place its bin directory on your system PATH (and ensure CUDA's bin is also on PATH). Then restart your shell/PC.

### 3) FFmpeg (required by yt-dlp for audio extraction)
Install FFmpeg and ensure it’s on PATH:
- Downloads: https://ffmpeg.org/download.html

### 4) yt-dlp
Use the official project for downloads and instructions:
- Repo & releases: https://github.com/yt-dlp/yt-dlp

Quick install options:
```bash
# Python/pip (cross-platform)
pip install -U yt-dlp

# Windows single-file exe (drop it somewhere on PATH)
# Download from the Releases page above
```

---

## Setup

**Important:** Always use a virtual environment to avoid conflicts with other Python projects.

### Step 1: Create and activate a virtual environment

**Windows (PowerShell):**
```powershell
# Navigate to your project directory
cd C:\path\to\CudaScribe

# Create virtual environment
python -m venv .venv

# Activate it
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
# Navigate to your project directory
cd /path/to/CudaScribe

# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate
```

**Verify activation:** Your terminal prompt should show `(.venv)` at the beginning.

### Step 2: Install Python dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Verify GPU access (optional)
Test that CUDA is properly configured:
```python
python -c "import torch; print('CUDA available:', torch.cuda.is_available())"
```
If you get `CUDA available: True`, you're ready to go!

---

## Workflow

### Step 1: Download audio (using yt-dlp separately)

**CudaScribe does not download videos or audio.** You must first download audio files using yt-dlp or provide your own audio files.

To download audio from YouTube:
```bash
yt-dlp -x --audio-format mp3 "YOUTUBE_VIDEO_URL"
```

**Example:**
```bash
yt-dlp -x --audio-format mp3 "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
# Creates: Video Title [dQw4w9WgXcQ].mp3
```

### Step 2: Transcribe with CudaScribe

**Make sure your virtual environment is activated** (you should see `(.venv)` in your terminal prompt), then run:

```bash
python transcribe.py path/to/your/audio_file.mp3
```

**Example:**
```bash
python transcribe.py "Video Title [dQw4w9WgXcQ].mp3"
```

**Outputs:**
- Live `[SEGMENT n]` progress updates during transcription
- Pretty-printed paragraph transcript to the terminal
- Saved file: `audio_filename.transcription.txt` next to your input file

---

## Tips and performance

**Model size options** (edit `model_size` in `transcribe.py`):
- `"tiny"` - Fastest, least accurate
- `"base"` - Good for clean studio audio
- `"small"` - Default, good balance of speed/accuracy
- `"medium"` - Better accuracy, slower
- `"large-v3"` - Best accuracy, slowest

**Memory optimization** - If you hit VRAM limits, change the compute type in `transcribe.py`:
```python
WhisperModel(model_size, device="cuda", compute_type="int8_float16")
# Options: "float32" (safe), "float16" (fast), "int8_float16" (memory efficient)
```

---

## Troubleshooting

**Common Issues:**

- **`cudnn_ops64_9.dll not found` (Windows):**
  - Install cuDNN 9.x that matches your CUDA 12.x version
  - Add cuDNN `bin` directory to your system PATH
  - Restart your shell/PC after PATH changes

- **yt-dlp cannot extract audio:**
  - Ensure FFmpeg is installed and available in PATH
  - Update yt-dlp: `pip install -U yt-dlp`

- **GPU not being used / very slow transcription:**
  - Confirm NVIDIA driver + CUDA 12 + cuDNN 9 are correctly installed
  - Test CUDA visibility with: `python -c "import torch; print(torch.cuda.is_available())"`
  - Try a lighter compute type like `"int8_float16"` in the script

- **"File not found" error:**
  - Make sure your audio file path is correct
  - Use quotes around filenames with spaces: `python transcribe.py "my file.mp3"`

- **Virtual environment issues:**
  - Make sure your virtual environment is activated (should see `(.venv)` in prompt)
  - If packages aren't found, reactivate: `.\.venv\Scripts\Activate.ps1` (Windows) or `source .venv/bin/activate` (Mac/Linux)

---

## Legacy CUDA (only if you cannot upgrade to CUDA 12)
If you must stay on CUDA 11.x + cuDNN 8, pin CTranslate2 <= 4.4.0. Example:
```txt
# requirements.txt (legacy)
faster-whisper==1.0.3
ctranslate2==4.4.0
```
