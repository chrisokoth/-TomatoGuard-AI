import streamlit as st
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os
import sys

# Add error handling for imports
try:
    from chatbot_local import TomatoDiseaseBot
except ImportError as e:
    st.error(f"Import error: {e}")
    st.stop()

# Initialize bot with error handling
@st.cache_resource
def load_bot():
    try:
        # Check if model file exists
        if not os.path.exists('tomato_model.keras'):
            st.error("Model file 'tomato_model.keras' not found!")
            return None
        return TomatoDiseaseBot()
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

def main():
    st.title("🍅 Tomato Disease Detection System")
    st.write("Upload a tomato leaf image for disease detection and treatment advice")
    
    # Check if bot loaded successfully
    bot = load_bot()
    if bot is None:
        st.error("Failed to load the disease detection model. Please check the logs.")
        st.info("Debug info:")
        st.write(f"Current directory: {os.getcwd()}")
        st.write(f"Files in directory: {os.listdir('.')}")
        return
    
    # Sidebar for settings
    st.sidebar.header("Settings")
    location = st.sidebar.text_input("📍 Location", value="Kerugoya")
    language = st.sidebar.selectbox("🌍 Language", ["english", "swahili"])
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose a tomato leaf image...", 
        type=['jpg', 'jpeg', 'png']
    )
    
    if uploaded_file is not None:
        try:
            # Display image
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded Image', use_column_width=True)
            
            # Analyze button
            if st.button("🔍 Analyze Plant"):
                with st.spinner("Analyzing image..."):
                    try:
                        # Save temp file
                        temp_path = f"temp_{uploaded_file.name}"
                        with open(temp_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        
                        # Analyze
                        result = bot.analyze_image(temp_path, location, language)
                        
                        # Display results
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("🔍 Detection Results")
                            st.write(f"**Prediction:** {result['prediction'].replace('_', ' ')}")
                            st.write(f"**Confidence:** {result['confidence']:.2%}")
                            
                            # Progress bar for confidence
                            st.progress(result['confidence'])
                        
                        with col2:
                            st.subheader("🌤️ Weather Conditions")
                            if result['weather']['success']:
                                st.write(f"**Temperature:** {result['weather']['temperature']}°C")
                                st.write(f"**Humidity:** {result['weather']['humidity']}%")
                                
                                # Humidity warning
                                if result['weather']['humidity'] > 80:
                                    st.warning("⚠️ High humidity detected - increased disease risk!")
                            else:
                                st.error("Could not fetch weather data")
                        
                        # Treatment advice
                        st.subheader("💊 Treatment & Prevention")
                        st.write(result['explanation'])
                        
                        # Clean up
                        if os.path.exists(temp_path):
                            os.remove(temp_path)
                            
                    except Exception as e:
                        st.error(f"Error analyzing image: {e}")
                        st.write("Debug info:", str(e))
        
        except Exception as e:
            st.error(f"Error processing uploaded file: {e}")

if __name__ == "__main__":
    main()