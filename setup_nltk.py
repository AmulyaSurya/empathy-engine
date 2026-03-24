# setup_nltk.py
import nltk

print("Downloading NLTK data...")
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('brown')
print("NLTK data downloaded successfully!")