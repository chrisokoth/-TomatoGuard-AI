#!/usr/bin/env python3
"""
Tomato Disease Detection Chatbot - Local Version
Refactored from Colab notebook for local execution
"""

import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import requests
import json
from PIL import Image

class TomatoDiseaseBot:
    def __init__(self, model_path="tomato_model.keras", api_key=None):
        try:
            self.model = load_model(model_path)
        except (ValueError, TypeError) as e:
            if "batch_shape" in str(e):
                # Load with custom objects to handle batch_shape compatibility
                import tensorflow as tf
                self.model = tf.keras.models.load_model(
                    model_path,
                    custom_objects=None,
                    compile=False
                )
                # Recompile the model
                self.model.compile(
                    optimizer='adam',
                    loss='categorical_crossentropy',
                    metrics=['accuracy']
                )
            else:
                raise e
        self.class_labels = ['Tomato_Early_blight', 'Tomato_Late_blight', 'Tomato_healthy']
        self.api_key = api_key or "1d5af17ac5484fae2f35780c93a44fb7"
        
        # Disease explanations
        self.disease_guide = {
            "Tomato_Early_blight": {
                "english": """🌿 Early Blight (Alternaria solani)
📌 Fungal disease with brown leaf spots on leaves/stems.
🛠️ Use fungicides like chlorothalonil or mancozeb.
🛡️ Avoid overhead watering and rotate crops.""",
                "swahili": """🌿 Early Blight (Alternaria solani)
📌 Ugonjwa wa kuvu unaosababisha madoa ya kahawia kwenye majani na mashina.
🛠️ Tumia dawa ya kuvu kama chlorothalonil au mancozeb.
🛡️ Epuka kumwagilia juu na fanya mzunguko wa mazao."""
            },
            "Tomato_Late_blight": {
                "english": """☁️ Late Blight (Phytophthora infestans)
📌 Gray patches on leaves, spreads quickly in wet conditions.
🛠️ Use copper-based fungicides.
🛡️ Ensure spacing, remove infected plants.""",
                "swahili": """☁️ Late Blight (Phytophthora infestans)
📌 Madoa ya kijivu yanayoenea haraka wakati wa unyevu.
🛠️ Tumia dawa zenye copper.
🛡️ Panda kwa nafasi, ondoa mimea iliyoambukizwa."""
            },
            "Tomato_healthy": {
                "english": """✅ Your tomato plant looks healthy!
🛡️ Keep monitoring regularly and avoid overwatering.""",
                "swahili": """✅ Mimea yako ya nyanya iko salama!
🛡️ Endelea kufuatilia na epuka kumwagilia kupita kiasi."""
            }
        }

    def predict_disease(self, img_path):
        """Predict disease from image path"""
        img = image.load_img(img_path, target_size=(256, 256))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        prediction = self.model.predict(img_array)
        predicted_index = np.argmax(prediction)
        predicted_label = self.class_labels[predicted_index]
        confidence = float(np.max(prediction))
        
        return predicted_label, confidence, img

    def get_weather(self, location):
        """Fetch weather data for location"""
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.api_key}&units=metric"
            response = requests.get(url)
            data = response.json()
            
            return {
                'humidity': data["main"]["humidity"],
                'temperature': data["main"]["temp"],
                'success': True
            }
        except:
            return {'success': False, 'error': f"Could not fetch weather for '{location}'"}

    def explain_diagnosis(self, label, humidity, lang="english"):
        """Generate diagnosis explanation with weather context"""
        explanation = f"\n🧪 Predicted Class: {label.replace('_', ' ')}\n"
        
        if label == 'Tomato_Early_blight':
            if lang == 'swahili':
                explanation += "\n🦠 Ugonjwa: Early Blight (Alternaria solani)\n"
                if humidity > 80:
                    explanation += "🚨 Unyevu mwingi! Hatari ya kuenea kwa ugonjwa huu ni kubwa.\n"
                    explanation += "🛠️ Tumia dawa ya kuvu kama chlorothalonil. Epuka kunyunyiza majani.\n"
                else:
                    explanation += "⚠️ Tibu ugonjwa, lakini hali ya hewa si hatari sana.\n"
                    explanation += "🧼 Hakikisha majani ni makavu na mimea iko na nafasi.\n"
            else:
                explanation += "\n🦠 Disease: Early Blight (Alternaria solani)\n"
                if humidity > 80:
                    explanation += "🚨 High humidity detected! Favors early blight spread.\n"
                    explanation += "🛠️ Apply chlorothalonil fungicide. Avoid wetting leaves.\n"
                else:
                    explanation += "⚠️ Treat early blight, but weather risk is moderate.\n"
                    explanation += "🧼 Maintain dry leaves and good spacing.\n"

        elif label == 'Tomato_Late_blight':
            if lang == 'swahili':
                explanation += "\n🦠 Ugonjwa: Late Blight (Phytophthora infestans)\n"
                if humidity > 80:
                    explanation += "🚨 Unyevu mwingi sana! Hatari ya kuenea kwa late blight.\n"
                    explanation += "🛠️ Tumia dawa za copper. Hakikisha upenyo wa hewa upo.\n"
                else:
                    explanation += "⚠️ Tibu ugonjwa. Hali ya hewa ni ya wastani.\n"
                    explanation += "🌬️ Weka nafasi ya hewa na epuka unyevu mwingi.\n"
            else:
                explanation += "\n🦠 Disease: Late Blight (Phytophthora infestans)\n"
                if humidity > 80:
                    explanation += "🚨 ALERT: Ideal conditions for late blight outbreak.\n"
                    explanation += "🛠️ Apply copper-based fungicide. Ensure airflow.\n"
                else:
                    explanation += "⚠️ Weather is stable, but treatment is still necessary.\n"
                    explanation += "🌬️ Maintain airflow and reduce moisture.\n"

        elif label == 'Tomato_healthy':
            if lang == 'swahili':
                explanation += "\n✅ Mimea ina afya!\n"
                if humidity > 80:
                    explanation += "⚠️ Lakini unyevu ni mwingi. Hatari ya ugonjwa wa kuvu ipo.\n"
                    explanation += "🛡️ Tumia dawa za kinga na fuatilia hali ya mimea.\n"
                else:
                    explanation += "🌞 Hali ya hewa ni nzuri. Endelea na usafi na nafasi.\n"
            else:
                explanation += "\n✅ Plant Status: Healthy\n"
                if humidity > 80:
                    explanation += "⚠️ But humidity is high — fungal risk is elevated.\n"
                    explanation += "🛡️ Preventive tip: Spray light fungicide & monitor.\n"
                else:
                    explanation += "🌞 All conditions favorable. Keep up hygiene & spacing.\n"

        return explanation

    def analyze_image(self, img_path, location="Kerugoya", lang="english"):
        """Complete analysis: predict + weather + explanation"""
        # Predict disease
        label, confidence, img = self.predict_disease(img_path)
        
        # Get weather
        weather = self.get_weather(location)
        
        # Generate explanation
        humidity = weather.get('humidity', 0) if weather['success'] else 0
        explanation = self.explain_diagnosis(label, humidity, lang)
        
        return {
            'prediction': label,
            'confidence': confidence,
            'weather': weather,
            'explanation': explanation,
            'image': img
        }

def main():
    """CLI interface for testing"""
    bot = TomatoDiseaseBot()
    
    print("🍅 Tomato Disease Detection Bot")
    print("=" * 40)
    
    img_path = input("📷 Enter image path: ")
    location = input("📍 Enter location (default: Kerugoya): ") or "Kerugoya"
    lang = input("🌍 Language (english/swahili): ") or "english"
    
    try:
        result = bot.analyze_image(img_path, location, lang)
        
        print(f"\n🔍 Prediction: {result['prediction']}")
        print(f"📊 Confidence: {result['confidence']:.2%}")
        
        if result['weather']['success']:
            print(f"🌡️ Temperature: {result['weather']['temperature']}°C")
            print(f"💧 Humidity: {result['weather']['humidity']}%")
        
        print(result['explanation'])
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()