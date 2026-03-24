# empathy_engine.py
import os
import tempfile
from datetime import datetime
from typing import Dict, Tuple
from dataclasses import dataclass

# Core libraries
from textblob import TextBlob
import pyttsx3
from gtts import gTTS

@dataclass
class VoiceConfig:
    """Configuration for voice parameters - Rate, Volume, and Pitch"""
    rate: int      # Speed in words per minute
    volume: float  # Volume level 0.0 to 1.0
    pitch_shift: int  # Pitch adjustment
    description: str  # Voice style description

class EmpathyEngine:
    
    
    def __init__(self, use_offline=True):
        """
        Initialize the Empathy Engine
        
        Args:
            use_offline: If True, use pyttsx3 (offline)
                        If False, use gTTS (online)
        """
        self.use_offline = use_offline
        
        # Initialize offline TTS if needed
        if use_offline:
            self.tts_engine = pyttsx3.init()
        else:
            self.tts_engine = None
        
        # Create emotion-to-voice mappings
        self.emotion_mappings = self._create_emotion_mappings()
        
        print("✅ Empathy Engine initialized successfully!")

    def _create_emotion_mappings(self) -> Dict[str, VoiceConfig]:
        
        return {
            # Positive emotions
            'happy': VoiceConfig(
                rate=190,
                volume=0.9,
                pitch_shift=15,
                description="Cheerful, upbeat, energetic"
            ),
            'excited': VoiceConfig(
                rate=210,
                volume=1.0,
                pitch_shift=25,
                description="Very enthusiastic, energetic"
            ),
            'neutral': VoiceConfig(
                rate=155,
                volume=0.7,
                pitch_shift=0,
                description="Calm, balanced, professional"
            ),
            'sad': VoiceConfig(
                rate=120,
                volume=0.5,
                pitch_shift=-10,
                description="Soft, slow, melancholic"
            ),
            'frustrated': VoiceConfig(
                rate=140,
                volume=0.8,
                pitch_shift=-5,
                description="Tense, strained, urgent"
            ),
            'inquisitive': VoiceConfig(
                rate=150,
                volume=0.75,
                pitch_shift=10,
                description="Curious, questioning, thoughtful"
            ),
            'calm': VoiceConfig(
                rate=130,
                volume=0.6,
                pitch_shift=-5,
                description="Peaceful, soothing, patient"
            )
        }
    def detect_emotion(self, text: str) -> Tuple[str, float]:
        
        # Analyze sentiment with TextBlob
        blob = TextBlob(text)
        sentiment = blob.sentiment
        
        # Calculate intensity based on polarity magnitude
        intensity = abs(sentiment.polarity)
        
        # Check for keywords for granular emotions
        text_lower = text.lower()
        
        # Keyword-based emotion detection
        if any(word in text_lower for word in ['amazing', 'awesome', 'wonderful', 'fantastic', 'great', 'exciting', 'love']):
            return 'excited', max(intensity, 0.7)
        elif any(word in text_lower for word in ['frustrated', 'annoying', 'cannot', 'wrong', 'problem', 'issue', 'error']):
            return 'frustrated', max(intensity, 0.6)
        elif any(word in text_lower for word in ['why', 'how', 'what', 'when', 'where', 'curious', 'wonder']):
            return 'inquisitive', max(intensity, 0.5)
        elif any(word in text_lower for word in ['calm', 'relaxed', 'peaceful', 'quiet']):
            return 'calm', max(intensity, 0.5)
        elif sentiment.polarity > 0.2:
            return 'happy', intensity
        elif sentiment.polarity < -0.2:
            return 'sad', intensity
        else:
            return 'neutral', intensity
            
    def modulate_voice(self, emotion: str, intensity: float) -> VoiceConfig:
       
        base_config = self.emotion_mappings.get(emotion, self.emotion_mappings['neutral'])
        
        # Scale parameters based on intensity
        if intensity > 0.5:
            if emotion in ['happy', 'excited']:
                rate_scale = 1 + (intensity * 0.2)
                volume_scale = min(1.0, base_config.volume + intensity * 0.1)
            elif emotion == 'sad':
                rate_scale = 1 - (intensity * 0.15)
                volume_scale = max(0.4, base_config.volume - intensity * 0.1)
            else:
                rate_scale = 1 + (intensity * 0.1)
                volume_scale = base_config.volume
        else:
            rate_scale = 1
            volume_scale = base_config.volume
        
        modulated_rate = int(base_config.rate * rate_scale)
        
        return VoiceConfig(
            rate=modulated_rate,
            volume=volume_scale,
            pitch_shift=base_config.pitch_shift,
            description=base_config.description
        )
       
    def generate_speech(self, text: str, output_file: str = None) -> str:
       
        # Detect emotion and intensity
        emotion, intensity = self.detect_emotion(text)
        print(f"🎭 Detected emotion: {emotion.upper()} (intensity: {intensity:.2f})")
        
        # Get modulated voice configuration
        voice_config = self.modulate_voice(emotion, intensity)
        print(f"🎚️ Voice settings: rate={voice_config.rate} wpm, volume={voice_config.volume:.2f}")
        
        # Generate unique filename if not provided
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"speech_{timestamp}.mp3"
        
        if self.use_offline:
            # Use pyttsx3 (offline)
            self.tts_engine.setProperty('rate', voice_config.rate)
            self.tts_engine.setProperty('volume', voice_config.volume)
            self.tts_engine.save_to_file(text, output_file)
            self.tts_engine.runAndWait()
        else:
            # Use gTTS (online)
            tts = gTTS(text=text, lang='en', slow=(voice_config.rate < 140))
            tts.save(output_file)
        
        print(f"✅ Audio saved to: {output_file}")
        return output_file
def main():
   
    print("=" * 50)
    print("🤖 Empathy Engine - AI Voice with Emotional Intelligence")
    print("=" * 50)
    print("\nEnter text to convert to speech with emotional modulation")
    print("Type 'quit' to exit\n")
    
    engine = EmpathyEngine(use_offline=True)
    
    while True:
        text = input("📝 Enter text: ").strip()
        
        if text.lower() == 'quit':
            print("Goodbye! 👋")
            break
        
        if text:
            try:
                output_file = engine.generate_speech(text)
                print(f"🎵 Audio file created: {output_file}")
                print()
            except Exception as e:
                print(f"❌ Error: {e}\n")

if __name__ == "__main__":
    main()
    
    