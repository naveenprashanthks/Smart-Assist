from flask import Flask, render_template
from gtts import gTTS
import pygame
import cv2
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

app = Flask(__name__)

# Load BLIP model
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/capture', methods=['POST'])
def capture():
    # Use OpenCV to capture from default camera (rear camera on mobile browser will work via HTML5, not here)
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        return "Failed to capture image", 500

    # Convert to PIL Image
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    # Generate caption
    inputs = processor(image, return_tensors="pt")
    out = model.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True)

    # Convert caption to speech
    speech_text = f"{caption} is before you"
    tts = gTTS(text=speech_text, lang="en")
    tts.save("description.mp3")

    # Play audio
    pygame.mixer.init()
    pygame.mixer.music.load("description.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue
    pygame.mixer.quit()

    return speech_text

if __name__ == '__main__':
    app.run(debug=True)
