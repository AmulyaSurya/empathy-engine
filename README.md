# Empathy Engine - Giving AI a Human Voice 🎙️

## Project Description
The Empathy Engine is a text-to-speech service that dynamically modulates vocal characteristics based on the detected emotion of the input text. It bridges the gap between text-based sentiment and expressive, human-like audio output by analyzing text sentiment and adjusting speech parameters like rate, volume, and pitch to match the emotional context.

### Features
- **Emotion Detection**: Identifies 7 distinct emotions (Happy, Excited, Neutral, Sad, Frustrated, Inquisitive, Calm)
- **Voice Modulation**: Adjusts speech rate and volume based on detected emotion
- **Intensity Scaling**: Stronger emotions produce more pronounced voice changes
- **Dual Interface**: CLI for quick testing and Web UI for interactive use
- **Real-time Audio**: Generates downloadable MP3 files with emotional expression

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git (for cloning the repository)

### Installation Steps

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd empathy-engine