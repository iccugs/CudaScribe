import sys
from faster_whisper import WhisperModel
from pathlib import Path
import textwrap

if len(sys.argv) < 2:
    print("Usage: python transcribe.py /path/to/audio.(mp3|wav|m4a|mp4)")
    sys.exit(1)

audio_path = Path(sys.argv[1])
assert audio_path.exists(), f"File not found: {audio_path}"

# Chose model size: tiny, base, small, medium, large-v3
model_size = "small"

# Use NVIDIA GPU
model = WhisperModel(model_size, device="cuda", compute_type="float32")

print(f"[INFO] Starting transcription with model '{model_size}'...")
print(f"[INFO] Processing file: {audio_path}\n")

segments, info = model.transcribe(
    str(audio_path),
    language="en",
    beam_size=5,
    vad_filter=True,
    vad_parameters=dict(min_silence_duration_ms=500)
)

chunks = []
for idx, s in enumerate(segments, start=1):
    t = s.text.strip()
    if t:
        # Print progress as each segment is processed
        print(f"[SEGMENT {idx}] {t}")
        chunks.append(t)

print("\n[INFO] Transcription complete. Joining segments into paragraph...")

# Join segments into one paragraph
paragraph = " ".join(chunks)
paragraph = " ".join(paragraph.split())  # cleanup extra spaces

# Pretty-print final paragraph
print("\n----- FULL PARAGRAPH TRANSCRIPT -----\n")
print(textwrap.fill(paragraph, width=100))
print("\n-------------------------------------\n")

# Save to file
out_path = audio_path.with_suffix(".transcription.txt")
out_path.write_text(paragraph, encoding="utf-8")
print(f"[INFO] Saved transcription to: {out_path}")

