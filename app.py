import streamlit as st
import numpy as np
from PIL import Image
from chatbot_local import TomatoDiseaseBot
import matplotlib.pyplot as plt

# Initialize bot
@st.cache_resource
def load_bot():
    return TomatoDiseaseBot()

def main():
    st.title("🍅 Tomato Disease Detection System")
    st.write("Upload a tomato leaf image for disease detection and treatment advice")
    
    bot = load_bot()
    
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
                    import os
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                        
                except Exception as e:
                    st.error(f"Error analyzing image: {e}")

if __name__ == "__main__":
    main()