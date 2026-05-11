import streamlit as st
import subprocess
import tempfile
import os
import shutil
import time

# ─── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MP4 → MP3 Converter",
    page_icon="🎵",
    layout="centered",
)

# ─── Styling ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #0f0f0f; }
    h1 { color: #f0f0f0; font-family: 'Segoe UI', sans-serif; }
    .subtitle { color: #888; font-size: 0.95rem; margin-top: -10px; margin-bottom: 24px; }
    .info-box {
        background: #1a1a2e;
        border: 1px solid #2a2a4a;
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 16px;
        color: #ccc;
        font-size: 0.88rem;
    }
    .info-box b { color: #7b9ef0; }
    .stat-row {
        display: flex;
        gap: 16px;
        margin-top: 12px;
    }
    .stat-card {
        flex: 1;
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 8px;
        padding: 12px 16px;
        text-align: center;
    }
    .stat-val { font-size: 1.4rem; font-weight: 700; color: #7b9ef0; }
    .stat-label { font-size: 0.75rem; color: #6b7280; margin-top: 2px; }
    .success-banner {
        background: #052e16;
        border: 1px solid #16a34a;
        border-radius: 8px;
        padding: 12px 16px;
        color: #4ade80;
        font-weight: 600;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

# ─── Header ─────────────────────────────────────────────────────────────────
st.markdown("# 🎵 MP4 → MP3 Converter")
st.markdown('<p class="subtitle">Extract audio from video with smart compression — powered by FFmpeg</p>',
            unsafe_allow_html=True)

# ─── Sidebar — Quality Settings ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Conversion Settings")

    quality_preset = st.selectbox(
        "Quality Preset",
        options=["High (320 kbps)", "Standard (192 kbps)", "Compact (128 kbps)", "Custom"],
        index=1,
        help="Higher bitrate = better quality, larger file."
    )

    if quality_preset == "Custom":
        bitrate = st.slider("Bitrate (kbps)", min_value=64, max_value=320, value=192, step=8)
    elif quality_preset == "High (320 kbps)":
        bitrate = 320
    elif quality_preset == "Standard (192 kbps)":
        bitrate = 192
    else:
        bitrate = 128

    sample_rate = st.selectbox(
        "Sample Rate",
        options=["44100 Hz (CD quality)", "48000 Hz (Studio)", "22050 Hz (Smaller file)"],
        index=0,
    )
    sr_map = {"44100 Hz (CD quality)": "44100", "48000 Hz (Studio)": "48000", "22050 Hz (Smaller file)": "22050"}
    sample_rate_val = sr_map[sample_rate]

    channels = st.radio(
        "Audio Channels",
        options=["Stereo", "Mono"],
        index=0,
        horizontal=True,
        help="Mono halves file size with minimal quality loss for speech."
    )
    channels_val = "2" if channels == "Stereo" else "1"

    st.markdown("---")
    st.markdown("**💡 Recommended settings**")
    st.markdown("""
- 🎶 **Music** → High, Stereo, 44100 Hz  
- 🎙️ **Podcasts/Voice** → Compact, Mono, 22050 Hz  
- 🎬 **General video** → Standard, Stereo, 44100 Hz  
""")

# ─── Upload ──────────────────────────────────────────────────────────────────
st.markdown("### 📂 Upload Video File")
uploaded_files = st.file_uploader(
    "Drag & drop MP4 files here",
    type=["mp4", "mkv", "avi", "mov", "webm"],
    accept_multiple_files=True,
    help="Supports MP4, MKV, AVI, MOV, WEBM"
)

# ─── Conversion ──────────────────────────────────────────────────────────────
def format_size(bytes_val):
    if bytes_val < 1024:
        return f"{bytes_val} B"
    elif bytes_val < 1024 ** 2:
        return f"{bytes_val/1024:.1f} KB"
    else:
        return f"{bytes_val/1024**2:.2f} MB"

def convert_to_mp3(input_path, output_path, bitrate_kbps, sample_rate, channels):
    """Run ffmpeg conversion with libmp3lame encoder."""
    cmd = [
        "ffmpeg",
        "-y",                          # overwrite output without asking
        "-i", input_path,              # input file
        "-vn",                         # drop video stream
        "-c:a", "libmp3lame",         # MP3 encoder (best quality)
        "-b:a", f"{bitrate_kbps}k",   # bitrate
        "-ar", sample_rate,            # sample rate
        "-ac", channels,               # channels
        "-q:a", "2",                   # VBR quality hint (fallback)
        "-id3v2_version", "3",         # proper ID3 tags
        output_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stderr

if uploaded_files:
    st.markdown(f"### 🔄 Converting {len(uploaded_files)} file(s)")
    st.markdown(
        f'<div class="info-box">Settings: <b>{bitrate} kbps</b> · <b>{sample_rate}</b> · <b>{channels}</b></div>',
        unsafe_allow_html=True
    )

    if st.button("▶️ Start Conversion", type="primary", use_container_width=True):
        results = []

        for uploaded_file in uploaded_files:
            with st.expander(f"🎬 {uploaded_file.name}", expanded=True):
                progress = st.progress(0, text="Saving upload...")
                status_placeholder = st.empty()

                # Save upload to temp dir
                tmpdir = tempfile.mkdtemp()
                input_path = os.path.join(tmpdir, uploaded_file.name)
                output_name = os.path.splitext(uploaded_file.name)[0] + ".mp3"
                output_path = os.path.join(tmpdir, output_name)

                with open(input_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                input_size = os.path.getsize(input_path)
                progress.progress(20, text="Running FFmpeg conversion...")

                start_time = time.time()
                returncode, stderr = convert_to_mp3(
                    input_path, output_path,
                    bitrate, sample_rate_val, channels_val
                )
                elapsed = time.time() - start_time

                progress.progress(90, text="Finalising...")

                if returncode == 0 and os.path.exists(output_path):
                    output_size = os.path.getsize(output_path)
                    reduction = (1 - output_size / input_size) * 100
                    progress.progress(100, text="Done!")

                    st.markdown(
                        '<div class="success-banner">✅ Conversion successful!</div>',
                        unsafe_allow_html=True
                    )

                    # Stats
                    st.markdown(f"""
<div class="stat-row">
  <div class="stat-card">
    <div class="stat-val">{format_size(input_size)}</div>
    <div class="stat-label">Original Size</div>
  </div>
  <div class="stat-card">
    <div class="stat-val">{format_size(output_size)}</div>
    <div class="stat-label">MP3 Size</div>
  </div>
  <div class="stat-card">
    <div class="stat-val">{reduction:.0f}%</div>
    <div class="stat-label">Size Reduction</div>
  </div>
  <div class="stat-card">
    <div class="stat-val">{elapsed:.1f}s</div>
    <div class="stat-label">Time Taken</div>
  </div>
</div>
""", unsafe_allow_html=True)

                    # Download button
                    with open(output_path, "rb") as f:
                        st.download_button(
                            label=f"⬇️ Download {output_name}",
                            data=f.read(),
                            file_name=output_name,
                            mime="audio/mpeg",
                            use_container_width=True,
                        )

                    results.append({"file": output_name, "success": True})
                else:
                    progress.progress(100, text="Failed.")
                    st.error(f"❌ Conversion failed for **{uploaded_file.name}**")
                    with st.expander("FFmpeg error details"):
                        st.code(stderr[-2000:] if len(stderr) > 2000 else stderr)
                    results.append({"file": uploaded_file.name, "success": False})

                shutil.rmtree(tmpdir, ignore_errors=True)

        # Summary
        succeeded = sum(1 for r in results if r["success"])
        st.markdown("---")
        st.markdown(f"**Summary:** {succeeded}/{len(results)} file(s) converted successfully.")

else:
    # Empty state
    st.markdown("""
<div class="info-box">
👆 Upload one or more video files above, adjust your quality settings in the sidebar, then click <b>Start Conversion</b>.
<br><br>
<b>Supported formats:</b> MP4 · MKV · AVI · MOV · WEBM
</div>
""", unsafe_allow_html=True)

# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    '<p style="color:#444;font-size:0.78rem;text-align:center;">Powered by FFmpeg libmp3lame encoder · No files stored server-side</p>',
    unsafe_allow_html=True
)
