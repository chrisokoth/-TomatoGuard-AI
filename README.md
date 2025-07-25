# Tomato Farming Advisory AI System: Disease Detection, Adaptive Chatbot & Early Warnings

## 🌱 Project Overview

This project aims to empower small-scale tomato farmers with AI-driven solutions for improved crop health and farm management. The system integrates a deep learning-based disease detection model, an intelligent chatbot for adaptive farming guidance, and an early warning system that provides timely alerts on potential threats like droughts and pest outbreaks. The final product is a user-friendly web application designed to work both online and offline in resource-constrained areas.

---

## 🚀 Key Features of the Project

- **Tomato Leaf Disease Detection** using a CNN model trained on annotated leaf images.
- **Chatbot Assistant** that provides personalized advice to farmers on planting, irrigation, pest control, and more.
- **Early Warning System** using remote data and user inputs to detect environmental threats.
- **User Interface** built with Flask and Streamlit, accessible via browser.
- **Modular Deployment** enabling model, chatbot, and alerts to be deployed independently or together.
- **Mobile and Desktop Compatibility**.
- **Offline Use Potential** via lightweight deployment options.

---

## 🧩 Project Implementation Steps

### 1. Define the Problem and Scope

The problem addressed is the lack of affordable, real-time agricultural extension services for tomato farmers in rural areas. The project focuses on:
- Early disease detection
- Real-time expert guidance
- Early environmental threat notifications

### 2. Data Collection

- **Tomato Leaf Dataset**: Sourced from PlantVillage and other public agricultural image datasets.
- **Farmer FAQs**: Curated text data to fine-tune chatbot responses.
- **Environmental Signals**: Simulated satellite and weather data for drought/pest prediction.

### 3. Model Selection

- **CNN (e.g., MobileNetV3)** for image classification of diseases.
- **Rule-based + NLP LLM Chatbot** for interaction.
- **Threshold/heuristic models** for early warnings (extendable with ML later).

### 4. Model Training and Evaluation

- Preprocessed tomato leaf images (resized, augmented).
- Trained CNN model in Keras with ~90%+ validation accuracy.
- Evaluated using precision, recall, F1-score, and confusion matrix.
- Tested chatbot responses for accuracy and user experience.

### 5. Build a User Interface

- Flask backend handles model logic and chatbot integration.
- HTML/CSS/JS frontend ensures usability.
- Streamlit used for quick prototyping and deployment.
- Upload image → detect disease → get advice → receive warnings.

### 6. Deployment

- Hosted using **Streamlit Cloud**.
- Option to deploy Flask app on **Render**, **Heroku**, or **Google Cloud**.
- GitHub used for version control and collaboration.
- Modular architecture allows for parts (model, chatbot, warnings) to run independently.

### 7. Testing and Validation

- Tested with sample inputs (images, text queries).
- Validated against real farmer queries.
- User testing with sample end-users for feedback.

### 8. Documentation and Reporting

- README.md
- Inline code comments and docstrings
- Deployment instructions
- Visual project workflow (diagrams included)

---

## ⚙️ Handling Challenges

- **Dataset imbalance** → Solved via image augmentation techniques.
- **Model deployment errors** → Handled through version control and simplified architecture.
- **Integration between chatbot and image model** → Decoupled modules for easier testing.
- **Streamlit limitations with interactivity** → Used combined Flask+Streamlit strategy.

---

## 🎯 Expected Outcomes

- A functional AI-driven farming assistant for tomato growers.
- Improved disease management and reduced losses.
- Time and cost-saving for farmers due to instant access to guidance.
- Foundation for scaling to other crops and regions.

---

## ❓ Why This Project?

Tomato is one of the most widely grown crops among small-scale farmers in Africa, yet remains highly susceptible to disease and climate risks. Agricultural extension services are often limited or unavailable. By leveraging AI, this project democratizes farming intelligence, reduces crop loss, and promotes food security.

---

## 📁 Repository Structure (Suggested)


Tomato-Farming-AI-Advisor/
│
├── models/ # Trained model files
├── chatbot/ # Chatbot logic and training data
├── static/ # CSS, images, assets
├── templates/ # HTML templates
├── app.py # Main Flask or Streamlit app
├── README.md # Project documentation
└── requirements.txt # Python dependencies


---

## 🌐 Live Demo

> Coming soon on [Streamlit Cloud](https://streamlit.io/)

---

## 📫 Contact

Built by **Emmanuel Ouma**  
[LinkedIn](https://www.linkedin.com/in/emmanuel-ouma-660518221) | [GitHub](https://github.com/oumaouma20)
