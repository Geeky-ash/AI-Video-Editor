# 🎬 AI Video Editor

An automated, intelligent video editing workstation powered by AI agent workflows, Remotion, HyperFrames, FFmpeg, and Whisper.cpp.

Designed to turn raw camera/phone footage into high-retention, polished vertical short-form videos (Instagram Reels, YouTube Shorts, and TikTok) following professional editing standards, cinematic templates, and custom brand kits.

---

## ⚡ Features & Capabilities

- **Automated Pacing & Dead-Air Removal**: Precision cutting of silences and pauses $> 0.1\text{s}$ using speech boundary and transcript alignment.
- **Brand System Integration**: Live brand kit enforcement (`brand.config.json`) specifying palette tokens, header/body typography, drop shadows, and platform safe zones.
- **Cinematic Product Videos (`video-shotcraft`)**: 124 modular motion-graphics shot recipes, Ink Press promo template, and interactive workbench previewing.
- **Audio Mastering & Sound Design**: Broadcast-standard loudness normalization to `-14 LUFS` integrated loudness with automatic background music ducking, beat synchronization, and Freesound SFX sourcing.
- **Motion Graphics & Dynamic Badging**: Remotion and native graphic components including punch-in zooms, floating badges, kinetic subtitles, and smooth transitions.
- **Automated Verification Loop**: Frame sampling and quality checks across entry, middle, and exit cut points prior to export.

---

## 🧠 Integrated Agent Skills

The editor is equipped with specialized agent skill suites that automate every stage of video production:

### 🌟 Featured: Cinematic & Product Motion
- **[`video-shotcraft`](https://github.com/Vincentwei1021/video-shotcraft)**:
  - **124 Cinematic Shot Cards**: Reusable visual formulas with demo source code and dynamic previews (camera fly-throughs, counters, kinetic text, split screens, and UI reveals).
  - **Ink Press Template**: Complete, verified promo film template for web and desktop products.
  - **Sound Design & SFX Tools**: Beat sync, timing measurement, and sound effect sourcing with Freesound integration.
  - **3 Creation Modes**: *Template Replacement*, *Autonomous Free Creation*, and *Guided Co-Creation*.

### ✂️ Video Editing & Assembly
- **`video-editor-pro`**: Operating guidelines for professional video editing (Orient $\rightarrow$ Inspect $\rightarrow$ Plan $\rightarrow$ Batch Execute $\rightarrow$ Visual Verification $\rightarrow$ Proven Export).
- **`video-editing`**: AI-assisted footage cutting, jump cuts, visual enhancements, and synthesis pipelines.
- **`video-edit`**: Fast local FFmpeg commands for trimming, concatenating, resizing, speed manipulation, and compression.
- **`edit`**: End-to-end talking head editing, silence removal, subtitle timing, and audio finishing at `-14 LUFS`.
- **`virality`**: Retention analysis, hook scoring, AI-slop elimination, and viral pacing formulas.

### 🎨 Rendering & Graphics Engines
- **`remotion-*` Suite**: Full Remotion toolset including captions animation, studio preview, maps, SaaS video generation, and multi-track rendering.
- **`hyperframes` Suite**: HTML-to-video rendering framework with pre-built registry blocks, camera moves, and kinetic type.
- **`figma`**: Direct ingestion of Figma design frames, brand tokens, and vectors into animated video compositions.

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
├── .agent/skills/       # Active agent skills (video-shotcraft, edit, virality, etc.)
├── .agents/skills/      # Remotion, HyperFrames & video-shotcraft skill engines
├── Exports/
│   └── proof/           # Verifiable frame snapshots from final video exports
├── References/
│   ├── frames/          # Sampled style frames from viral benchmarks
│   ├── transcripts/     # Benchmark transcription & timing files
│   └── music_track.m4a  # Extracted background audio stem
├── AGENTS.md            # Agent editing guidelines & craft rules
├── GEMINI.md            # LLM prompt & operational loop specifications
├── brand.config.json    # Adaptable brand palette, typography, and styling config
├── skills-lock.json     # Installed skill lockfile & provenance
└── README.md            # Project documentation
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
