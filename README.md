# Empathy Engine - Giving AI a Human Voice

## Project Description

The Empathy Engine is a text-to-speech service that dynamically modulates vocal characteristics based on the detected emotion of the input text. It bridges the gap between text-based sentiment and expressive, human-like audio output by analyzing text sentiment and adjusting speech parameters like rate and volume to match the emotional context.

---

## Libraries Used

| Library  | Version | Purpose                                    |
| -------- | ------- | ------------------------------------------ |
| textblob | 0.17.1  | Emotion detection and sentiment analysis   |
| pyttsx3  | 2.90    | Offline text-to-speech engine for CLI mode |
| Flask    | 2.3.3   | Web framework for UI                       |
| gTTS     | 2.3.2   | Online text-to-speech                      |
| nltk     | 3.8.1   | NLP support for TextBlob                   |

---

## Setup Instructions

### Step 1: Clone the repository

```bash
git clone https://github.com/AmulyaSurya/empathy-engine
cd empathy-engine
```

### Step 2: Create and activate virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python -m venv venv
source venv/bin/activate
```

### Step 3: Install dependencies

```bash
pip install textblob==0.17.1 pyttsx3==2.90 Flask==2.3.3 gTTS==2.3.2 nltk==3.8.1
```

### Step 4: Download NLP corpora

```bash
python -m textblob.download_corpora
```

### Step 5: Run the application

#### CLI Mode

```bash
python empathy_engine.py
```

#### Web Mode

```bash
python web_app.py
```

Then open:

```
http://localhost:5000
```

---

## Design Choices: Emotion-to-Voice Mapping Logic

### Why These Voice Parameters?

I chose to modulate **Rate** and **Volume** because these are the two most noticeable vocal characteristics that humans naturally change based on emotion:

* **Rate (Speed):** People speak faster when excited or happy, and slower when sad or calm
* **Volume:** People speak louder when angry or excited, and softer when sad or calm

---

### Emotion Detection Approach

I used a **hybrid approach**:

* **TextBlob Sentiment Analysis**

  * Provides polarity score (-1 to +1)
  * Helps classify text as positive, negative, or neutral

* **Keyword Matching**

  * Detects specific emotions like *excited, frustrated, inquisitive*
  * Handles cases where sentiment alone is insufficient

* **Intensity Calculation**

  * Based on absolute polarity (0 to 1)
  * Stronger language → higher intensity

---

### Emotion-to-Voice Mapping

| Emotion     | Rate (wpm) | Volume | Reasoning                                |
| ----------- | ---------- | ------ | ---------------------------------------- |
| Happy       | 190        | 0.9    | Faster and louder due to positive energy |
| Excited     | 210        | 1.0    | Maximum energy, highest modulation       |
| Neutral     | 155        | 0.7    | Baseline conversational tone             |
| Sad         | 120        | 0.5    | Slower and softer tone                   |
| Frustrated  | 140        | 0.8    | Slight tension, moderately louder        |
| Inquisitive | 150        | 0.75   | Slight variation for questioning tone    |
| Calm        | 130        | 0.6    | Gentle and controlled speech             |

---

### Intensity Scaling Logic (Bonus Feature)

For stronger emotions, parameters are dynamically scaled:

```python
if intensity > 0.5:
    if emotion in ['happy', 'excited']:
        rate = base_rate * (1 + intensity * 0.2)
        volume = min(1.0, base_volume + intensity * 0.1)
    elif emotion == 'sad':
        rate = base_rate * (1 - intensity * 0.15)
        volume = max(0.4, base_volume - intensity * 0.1)
```

#### Example:

* "This is good" → Low intensity → slight modulation
* "This is the best news ever!" → High intensity → strong modulation

---

## Test Results

### CLI Mode Sample Output

```
==================================================
🤖 Empathy Engine - AI Voice with Emotional Intelligence
==================================================

Enter text to convert to speech with emotional modulation
Type 'quit' to exit

✅ Empathy Engine initialized successfully!

📝 Enter text: hello
🎭 Detected emotion: NEUTRAL (intensity: 0.00)
🎚️ Voice settings: rate=155 wpm, volume=0.70
✅ Audio saved to: speech_20260324_105035.mp3

📝 Enter text: i am feeling sad
🎭 Detected emotion: SAD (intensity: 0.50)
🎚️ Voice settings: rate=120 wpm, volume=0.50
✅ Audio saved to: speech_20260324_105111.mp3

📝 Enter text: i am very happy
🎭 Detected emotion: HAPPY (intensity: 1.00)
🎚️ Voice settings: rate=228 wpm, volume=1.00
✅ Audio saved to: speech_20260324_105126.mp3
```

---

## Conclusion

The Empathy Engine demonstrates how combining sentiment analysis with adaptive speech synthesis can significantly improve human-computer interaction. By mapping emotions to voice parameters, the system produces more natural and expressive audio output, making AI communication feel more human-like.
