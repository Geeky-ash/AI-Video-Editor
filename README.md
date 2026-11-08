# 🎬 AI Video Editor

An automated, intelligent video editing workstation powered by AI agent workflows, Remotion, HyperFrames, FFmpeg, and Whisper.cpp.

Designed to turn raw camera/phone footage into high-retention, polished vertical short-form videos (Instagram Reels, YouTube Shorts, and TikTok) following professional editing standards and custom brand kits.

---

## ⚡ Features & Capabilities

- **Automated Pacing & Dead-Air Removal**: Precision cutting of silences and pauses $> 0.1\text{s}$ using speech boundary and transcript alignment.
- **Brand System Integration**: Live brand kit enforcement (`brand.config.json`) specifying palette tokens, header/body typography, drop shadows, and platform safe zones.
- **Audio Mastering**: Broadcast-standard loudness normalization to `-14 LUFS` integrated loudness with automatic background music ducking.
- **Motion Graphics & Dynamic Badging**: Remotion and native graphic components including punch-in zooms, floating badges, kinetic subtitles, and smooth transitions.
- **Automated Verification Loop**: Frame sampling and quality checks across entry, middle, and exit cut points prior to export.

---

## 🛠️ Stack & Tooling

- **FFmpeg**: Video decoding, scaling, CFR normalization, audio filtering (`loudnorm`, `afade`), and multi-track compositing.
- **Whisper.cpp**: Fast, local C++ AI transcription and word-level alignment with `ggml-base.en.bin`.
- **Remotion**: Programmatic React-based video generation and kinetic motion design.
- **HyperFrames**: High-performance HTML-to-video rendering framework.
- **yt-dlp**: Ingestion and reference reel analysis pipeline.

---

## 📂 Repository Structure

```
├── .agent/              # Agent skills (build, edit, virality, video-editor-pro)
├── .agents/             # Remotion & HyperFrames agent skills and registries
├── Exports/
│   └── proof/           # Verifiable frame snapshots from final video exports
├── References/
│   ├── frames/          # Sampled style frames from viral benchmarks
│   ├── transcripts/     # Benchmark transcription & timing files
│   └── music_track.m4a  # Extracted background audio stem
├── AGENTS.md            # Agent editing guidelines & craft rules
├── GEMINI.md            # LLM prompt & operational loop specifications
├── brand.config.json    # Adaptable brand palette, typography, and styling config
└── skills-lock.json     # Installed skill lockfile
```

---

## 🚀 Quick Start

### 1. Prerequisites
Ensure you have the following installed:
- [Node.js](https://nodejs.org/) (v18+)
- [FFmpeg](https://ffmpeg.org/) (configured in system PATH)
- [Python 3.10+](https://www.python.org/) & `yt-dlp`

### 2. Configure Your Brand Sheet
Edit `brand.config.json` to define your brand identity:
```json
{
  "brand_name": "My Brand",
  "colors": {
    "primary_accent": "#F3C93E",
    "text_dark": "#18181B",
    "text_light": "#FFFFFF"
  },
  "typography": {
    "heading_font": "Georgia",
    "body_font": "Arial"
  }
}
```

### 3. Run Editing Workflow
Place raw video clips in `Raw footage/` and trigger your automated editing workflow to generate cuts, captions, music mixes, and exported reels directly into `Exports/`.
