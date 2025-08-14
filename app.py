
import streamlit as st
from PIL import Image
import numpy as np
import tensorflow as tf
from tensorflow import keras
import cv2
from io import StringIO

# Set page config with enhanced visuals
st.set_page_config(
    page_title="🌿 AI-Powered Crop Weed Management",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern interface with enhanced visuals
def set_custom_style():
    st.markdown("""
    <style>
    :root {
        --primary: #2e7d32;
        --primary-light: #60ad5e;
        --primary-dark: #005005;
        --secondary: #81c784;
        --accent: #ff8f00;
        --accent-light: #ffc046;
        --accent-dark: #c56000;
        --text: #263238;
        --text-light: #4f5b62;
        --text-dark: #000a12;
        --background: #f5f5f5;
        --card-bg: rgba(255, 255, 255, 0.95);
    }
    
    .stApp {
        background-image: linear-gradient(rgba(0, 0, 0, 0.85), rgba(0, 0, 0, 0.85)),
                          url("https://images.unsplash.com/photo-1500651230702-0e2d8a49d4ad?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    .header {
        background: linear-gradient(135deg, var(--primary-dark), var(--primary));
        color: white;
        padding: 2.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        margin-bottom: 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .header::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: url("https://images.unsplash.com/photo-1585954965293-da6d927d0363?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80");
        background-size: cover;
        background-position: center;
        opacity: 0.1;
        z-index: 0;
    }
    
    .header h1, .header p {
        position: relative;
        z-index: 1;
    }
    
    .card {
        background: var(--card-bg);
        border-radius: 15px;
        padding: 1.8rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        margin-bottom: 1.8rem;
        border-left: 5px solid var(--accent);
        backdrop-filter: blur(10px);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 30px rgba(0,0,0,0.15);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.8));
        backdrop-filter: blur(10px);
        border-radius: 0 15px 15px 0;
        box-shadow: 5px 0 20px rgba(0,0,0,0.1);
        padding: 1.8rem;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, var(--primary), var(--primary-light));
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.8rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 10px rgba(46, 125, 50, 0.2);
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 15px rgba(46, 125, 50, 0.3);
        background: linear-gradient(135deg, var(--primary-dark), var(--primary));
    }
    
    .stButton>button:active {
        transform: translateY(0);
        box-shadow: 0 2px 5px rgba(46, 125, 50, 0.3);
    }
    
    /* File uploader styling */
    .stFileUploader {
        padding: 1rem;
        border-radius: 10px;
        border: 2px dashed var(--primary-light);
        background: rgba(255, 255, 255, 0.7);
        transition: all 0.3s ease;
    }
    
    .stFileUploader:hover {
        border-color: var(--primary);
        background: rgba(255, 255, 255, 0.9);
    }
    
    .stFileUploader>div>div>div>div {
        color: var(--primary);
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background-color: var(--primary);
    }
    
    /* Slider styling */
    .stSlider > div > div > div > div > div {
        background-color: var(--primary);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.7);
        border-radius: 8px;
    }
    
    /* Info, warning, error box styling */
    .stInfo, .stWarning, .stError, .stSuccess {
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .stSuccess {
        background-color: rgba(129, 199, 132, 0.2);
        border-left: 4px solid var(--primary);
    }
    
    .stWarning {
        background-color: rgba(255, 152, 0, 0.2);
        border-left: 4px solid var(--accent);
    }
    
    .stInfo {
        background-color: rgba(3, 169, 244, 0.2);
        border-left: 4px solid #03a9f4;
    }
    
    .highlight {
        background-color: rgba(129, 199, 132, 0.2);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid var(--primary);
        margin: 1rem 0;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        font-weight: 600;
        color: var(--primary-dark);
        background-color: rgba(255, 255, 255, 0.7);
        border-radius: 8px;
        padding: 0.5rem 1rem !important;
    }
    
    /* Image styling */
    .stImage img {
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Text input styling */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        padding: 0.5rem 1rem;
        background-color: rgba(255, 255, 255, 0.7);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary);
        box-shadow: 0 0 0 2px rgba(46, 125, 50, 0.2);
    }
    
    /* Custom recommendation container */
    .recommendation-container {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.8));
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
        border-left: 5px solid var(--accent);
        margin: 1.5rem 0;
    }
    
    /* Custom badges */
    .badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    .badge-primary {
        background-color: var(--primary);
        color: white;
    }
    
    .badge-secondary {
        background-color: var(--accent);
        color: white;
    }
    
    .badge-light {
        background-color: rgba(255, 255, 255, 0.9);
        color: var(--text);
        border: 1px solid #e0e0e0;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animate-fade-in {
        animation: fadeIn 0.5s ease-out forwards;
    }
    
    /* Herbicide pill style */
    .herbicide-pill {
        display: inline-block;
        background: linear-gradient(135deg, var(--primary-light), var(--primary));
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 50px;
        margin: 0.3rem;
        font-size: 0.9rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

set_custom_style()

# App header with enhanced design
st.markdown("""
<div class="header animate-fade-in">
    <h1 style="margin:0;font-size:2.8rem;font-weight:700">🌿 AI-Powered Crop Weed Management</h1>
    <p style="margin:10px 0 0;font-size:1.3rem;opacity:0.9">Smart weed identification and precision control recommendations</p>
</div>
""", unsafe_allow_html=True)

# Default model path
DEFAULT_MODEL_PATH = "crop_weed_classifier_final.keras"

# Load model function with caching
@st.cache_resource
def load_model(model_path):
    try:
        model = keras.models.load_model(model_path)
        return model
    except Exception as e:
        st.error(f"❌ Error loading model: {str(e)}")
        return None

# Enhanced image preprocessing
def preprocess_image(image, target_size=(120, 120)):
    try:
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        image = image.resize(target_size)
        image_array = np.array(image) / 255.0
        image_array = np.expand_dims(image_array, axis=0)
        return image_array
    except Exception as e:
        st.error(f"❌ Error preprocessing image: {str(e)}")
        return None

# Weed classification with confidence display
def classify_weed(model, image_array, class_names):
    try:
        if model.input_shape[1:3] != image_array.shape[1:3]:
            image_array = tf.image.resize(image_array, model.input_shape[1:3])
        
        predictions = model.predict(image_array)
        predicted_class = np.argmax(predictions[0])
        confidence = np.max(predictions[0])
        return class_names[predicted_class], confidence
    except Exception as e:
        st.error(f"❌ Error during classification: {str(e)}")
        return None, None

# Complete weed information database
WEED_INFO = {
    "Carpetweeds": {
        "description": "Low-growing summer annual weeds that form dense mats.",
        "recommendation": "Use pre-emergent herbicides like Pendimethalin or post-emergent like 2,4-D. Mulching can help prevent growth.",
        "pesticides": ["Pendimethalin", "2,4-D", "Dicamba", "Atrazine"],
        "icon": "🌱"
    },
    "Crabgrass": {
        "description": "Annual grassy weed that spreads quickly in thin lawns.",
        "recommendation": "Apply pre-emergent herbicides in early spring. For established plants, use post-emergent herbicides containing Quinclorac.",
        "pesticides": ["Quinclorac", "Dithiopyr", "Prodiamine", "Glyphosate"],
        "icon": "🌾"
    },
    "Eclipta": {
        "description": "Annual broadleaf weed with white flowers, often found in wet areas.",
        "recommendation": "Control with glyphosate or paraquat for non-selective treatment. In crops, use 2,4-D or dicamba.",
        "pesticides": ["Glyphosate", "Paraquat", "2,4-D", "Dicamba"],
        "icon": "🌼"
    },
    "Goosegrass": {
        "description": "Annual grassy weed with flattened stems that forms a rosette pattern.",
        "recommendation": "Apply pre-emergent herbicides like oxadiazon in spring. For post-emergence, use fenoxaprop or diclofop.",
        "pesticides": ["Oxadiazon", "Fenoxaprop", "Diclofop", "Glyphosate"],
        "icon": "🌿"
    },
    "Morningglory": {
        "description": "Climbing annual vine with heart-shaped leaves and trumpet-shaped flowers.",
        "recommendation": "Use pre-emergence herbicides like flumioxazin. Post-emergence control with 2,4-D or dicamba.",
        "pesticides": ["Flumioxazin", "2,4-D", "Dicamba", "Atrazine"],
        "icon": "🌸"
    },
    "Nutsedge": {
        "description": "Perennial sedge with triangular stems and yellowish-brown flower clusters.",
        "recommendation": "Apply selective herbicides containing halosulfuron or sulfentrazone. Requires persistent treatment.",
        "pesticides": ["Halosulfuron", "Sulfentrazone", "Bentazon", "Imazaquin"],
        "icon": "🌾"
    },
    "PalmerAmaranth": {
        "description": "Aggressive annual pigweed with rapid growth and prolific seed production.",
        "recommendation": "Use PPO-inhibiting herbicides and residual herbicides. Practice crop rotation and tillage.",
        "pesticides": ["Fomesafen", "Lactofen", "S-metolachlor", "Glufosinate"],
        "icon": "🌿"
    },
    "Prickly Sida": {
        "description": "Annual broadleaf weed with spiny seed pods and yellow flowers.",
        "recommendation": "Apply pre-emergent herbicides in early spring. For established plants, use 2,4-D or dicamba.",
        "pesticides": ["2,4-D", "Dicamba", "Bromoxynil", "Bentazon"],
        "icon": "🌵"
    },
    "Purslane": {
        "description": "Succulent annual with reddish stems and small yellow flowers.",
        "recommendation": "Apply mulch to suppress growth. Use glyphosate for non-selective control or 2,4-D for selective control.",
        "pesticides": ["Glyphosate", "2,4-D", "Oxadiazon", "Oryzalin"],
        "icon": "🌱"
    },
    "Ragweed": {
        "description": "Annual with deeply lobed leaves and tiny greenish flowers in terminal spikes.",
        "recommendation": "Control with pre-emergence herbicides in spring. Post-emergence, use 2,4-D or dicamba.",
        "pesticides": ["2,4-D", "Dicamba", "Atrazine", "Glyphosate"],
        "icon": "🌿"
    },
    "Sicklepod": {
        "description": "Annual legume with yellow flowers and curved seed pods.",
        "recommendation": "Apply pre-emergence herbicides like metribuzin. For post-emergence, use acifluorfen or lactofen.",
        "pesticides": ["Metribuzin", "Acifluorfen", "Lactofen", "Glyphosate"],
        "icon": "🌱"
    },
    "SpottedSpurge": {
        "description": "Low-growing annual with milky sap and distinctive red spot on each leaf.",
        "recommendation": "Use pre-emergence herbicides like isoxaben. Post-emergence, apply triclopyr or 2,4-D.",
        "pesticides": ["Isoxaben", "Triclopyr", "2,4-D", "Glyphosate"],
        "icon": "🍃"
    },
    "SpurredAnoda": {
        "description": "Annual broadleaf with maple-like leaves and lavender to purple flowers.",
        "recommendation": "Control with pre-emergence herbicides in spring. Post-emergence, use 2,4-D or dicamba.",
        "pesticides": ["2,4-D", "Dicamba", "Bromoxynil", "Glyphosate"],
        "icon": "🌸"
    },
    "Swinecress": {
        "description": "Winter annual with deeply lobed leaves and small white flowers.",
        "recommendation": "Apply post-emergence herbicides containing 2,4-D or dicamba. Pre-emergence control with isoxaben.",
        "pesticides": ["2,4-D", "Dicamba", "Isoxaben", "Glyphosate"],
        "icon": "🌿"
    },
    "Waterhemp": {
        "description": "Tall annual pigweed with lance-shaped leaves and multiple herbicide resistances.",
        "recommendation": "Use overlapping residual herbicides. Integrate mechanical and cultural control methods.",
        "pesticides": ["S-metolachlor", "Fomesafen", "Dicamba", "Glufosinate"],
        "icon": "🌱"
    }
}

# Enhanced pesticide recommendation engine
def get_pesticide_recommendation(weed_type, soil_type, temperature, crop_type):
    try:
        base_info = WEED_INFO.get(weed_type, {})
        pesticides = base_info.get("pesticides", [])
        general_rec = base_info.get("recommendation", "")
        
        recommendations = []
        
        # Soil-specific advice
        soil_advice = {
            "clay": "For clay soil, add a surfactant to improve herbicide absorption and use higher application rates.",
            "sandy": "On sandy soils, reduce application rates by 20% to prevent leaching and potential groundwater contamination.",
            "loamy": "Loamy soils provide ideal conditions for most herbicide applications.",
            "silty": "On silty soils, apply herbicides when soil moisture is optimal to prevent runoff.",
            "peaty": "For peaty soils, consider using foliar-applied herbicides for better effectiveness."
        }
        if soil_type.lower() in soil_advice:
            recommendations.append(soil_advice[soil_type.lower()])
        
        # Temperature advice
        if temperature > 30:
            recommendations.append("⚠️ Avoid herbicide application during high temperatures (>30°C) to prevent volatilization and plant damage.")
        elif temperature < 10:
            recommendations.append("⚠️ Herbicides may be less effective in cold temperatures (<10°C). Wait for warmer conditions.")
        else:
            recommendations.append("✅ Current temperature is ideal for herbicide application.")
        
        # Crop-specific advice
        crop_advice = {
            "wheat": "For wheat crops, consider using Axial or Puma Super for grass weed control.",
            "corn": "In corn fields, use atrazine-based products for broadleaf weed control.",
            "soyabean": "For soybeans, Flexstar or Roundup Ready systems work well for post-emergent control."
        }
        if crop_type.lower() in crop_advice:
            recommendations.append(crop_advice[crop_type.lower()])
        
        return pesticides, general_rec, recommendations
    except Exception as e:
        st.error(f"❌ Error generating recommendations: {str(e)}")
        return [], "", []

# Main application with enhanced modern layout
def main():
    # Sidebar with enhanced design
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center;margin-bottom:2rem">
            <h2 style="color:var(--primary);margin-bottom:0;font-size:2rem">🌾 WeedAI</h2>
            <p style="color:var(--text);opacity:0.8;font-style:italic">Precision Weed Management</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Model information
        with st.expander("⚙️ Model Information", expanded=True):
            model = load_model(DEFAULT_MODEL_PATH)
            if model:
                st.success("✅ Model loaded successfully!")
                st.markdown(f"""
                <div class="highlight">
                    <span style="font-weight:600">Input shape:</span> {model.input_shape[1:]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("Model failed to load")
        
        # Quick guide
        with st.expander("📚 How to Use", expanded=True):
            st.markdown("""
            <div style="background:rgba(255,255,255,0.7);border-radius:10px;padding:1rem">
                <p style="font-weight:600;margin-bottom:0.5rem">Follow these simple steps:</p>
                <ol style="margin-left:1rem;padding-left:0.5rem">
                    <li style="margin-bottom:0.5rem">📤 Upload a clear image of the weed</li>
                    <li style="margin-bottom:0.5rem">🔍 Click 'Identify Weed'</li>
                    <li style="margin-bottom:0.5rem">🌱 View identification results</li>
                    <li style="margin-bottom:0.5rem">🧪 Get customized recommendations</li>
                    <li style="margin-bottom:0">⚠️ Follow safety precautions</li>
                </ol>
            </div>
            """, unsafe_allow_html=True)
        
        # About section
        with st.expander("ℹ️ About", expanded=True):
            st.markdown("""
            <div style="background:rgba(255,255,255,0.7);border-radius:10px;padding:1.2rem;box-shadow:0 4px 15px rgba(0,0,0,0.05)">
                <p style="margin-top:0;font-size:1.05rem;color:var(--text-dark)">This AI-powered app helps farmers and agronomists:</p>
                <ul style="margin-left:1rem;padding-left:0.5rem;line-height:1.6">
                    <li>Identify common crop weeds with precision accuracy</li>
                    <li>Access science-backed control methods and treatment options</li>
                    <li>Receive personalized recommendations based on environmental conditions</li>
                    <li>Make data-driven decisions for sustainable weed management</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Developer credit section - separated into its own markdown call
            st.markdown("""
            <div style="background:linear-gradient(135deg, var(--primary-light), var(--primary));color:white;padding:1rem;border-radius:8px;margin-top:1.2rem;box-shadow:0 4px 10px rgba(46, 125, 50, 0.2)">
                <p style="margin:0;font-weight:600;text-align:center;letter-spacing:0.5px">Developed by AgriTech Solutions</p>
                <p style="margin:0.3rem 0 0;text-align:center;font-size:0.9rem;opacity:0.9">Empowering Precision Agriculture Since 2023</p>
            </div>
            """, unsafe_allow_html=True)

    # Main content columns
    col1, col2 = st.columns([2, 1], gap="large")
    
    with col1:
        # Weed identification card
        with st.container():
            st.markdown("""
            <h3 style="display:flex;align-items:center;gap:0.5rem">
                <span style="background:var(--primary);color:white;width:40px;height:40px;display:flex;align-items:center;justify-content:center;border-radius:50%">📷</span>
                Weed Identification
            </h3>
            """, unsafe_allow_html=True)
            
            uploaded_image = st.file_uploader("Upload crop field image", 
                                           type=['jpg', 'jpeg', 'png'],
                                           label_visibility="collapsed")
            
            if uploaded_image is not None and model:
                image = Image.open(uploaded_image)
                st.image(image, caption="Uploaded Image", use_column_width=True)
                
                # Define all weed classes
                class_names = [
                    "Carpetweeds", "Crabgrass", "Eclipta", "Goosegrass", 
                    "Morningglory", "Nutsedge", "PalmerAmaranth", "Prickly Sida",
                    "Purslane", "Ragweed", "Sicklepod", "SpottedSpurge",
                    "SpurredAnoda", "Swinecress", "Waterhemp"
                ]
                
                if st.button("🔍 Identify Weed", type="primary", use_container_width=True):
                    with st.spinner("🧠 Analyzing weed..."):
                        image_array = preprocess_image(image)
                        predicted_class, confidence = classify_weed(model, image_array, class_names)
                        
                        if predicted_class and confidence:
                            st.session_state.predicted_weed = predicted_class
                            
                            # Display results in a beautiful card
                            weed_icon = WEED_INFO.get(predicted_class, {}).get("icon", "🌿")
                            with st.container():
                                st.markdown(f"""
                                <div class="card animate-fade-in">
                                    <div style="display:flex;align-items:center;gap:1.5rem;margin-bottom:1.5rem">
                                        <div style="width:60px;height:60px;background:linear-gradient(135deg, var(--primary-light), var(--primary));color:white;display:flex;align-items:center;justify-content:center;border-radius:50%;font-size:2rem;box-shadow:0 4px 10px rgba(0,0,0,0.1)">
                                            {weed_icon}
                                        </div>
                                        <div style="flex-grow:1">
                                            <h3 style="margin:0;font-size:1.5rem;color:var(--primary-dark)">{predicted_class}</h3>
                                            <div style="display:flex;align-items:center;gap:0.8rem;margin-top:0.5rem">
                                                <div style="flex-grow:1;background:#e0e0e0;border-radius:10px;height:10px;overflow:hidden">
                                                    <div style="width:{confidence*100:.0f}%;background:linear-gradient(90deg, var(--primary), var(--primary-light));height:100%;border-radius:10px"></div>
                                                </div>
                                                <span style="font-weight:600;color:var(--primary-dark)">{confidence*100:.1f}% Confidence</span>
                                            </div>
                                        </div>
                                    </div>
                                    <div style="background:rgba(129, 199, 132, 0.1);border-radius:10px;padding:1rem;border-left:4px solid var(--primary)">
                                        <p style="margin:0;font-size:1.05rem">{WEED_INFO.get(predicted_class, {}).get('description', '')}</p>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
    
    with col2:
        # Recommendation card
        if 'predicted_weed' in st.session_state or model:
            with st.container():
                st.markdown("""
                <h3 style="display:flex;align-items:center;gap:0.5rem">
                    <span style="background:var(--accent);color:white;width:40px;height:40px;display:flex;align-items:center;justify-content:center;border-radius:50%">🧪</span>
                    Control Recommendations
                </h3>
                """, unsafe_allow_html=True)
                
                with st.form("recommendation_form"):
                    soil_type = st.selectbox("Soil Type", 
                                           ["Select", "Clay", "Loamy", "Sandy", "Silty", "Peaty"],
                                           index=0)
                    
                    temperature = st.slider("Temperature (°C)", 
                                          min_value=-10, max_value=50, value=25)
                    
                    default_weed = st.session_state.get('predicted_weed', '')
                    weed_type = st.text_input("Weed Type", 
                                             value=default_weed if default_weed else "",
                                             placeholder="Detected automatically")
                    
                    crop_type = st.text_input("Crop Type", 
                                            placeholder="e.g., Wheat, Corn, Soyabean")
                    
                    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
                    
                    if st.form_submit_button("Get Custom Recommendations", type="primary", use_container_width=True):
                        if not all([soil_type != "Select", weed_type, crop_type]):
                            st.warning("Please fill all fields")
                        else:
                            with st.spinner("🔍 Generating recommendations..."):
                                pesticides, general_rec, specific_recs = get_pesticide_recommendation(
                                    weed_type, soil_type, temperature, crop_type
                                )
                                
                                # Display recommendations with enhanced design
                                with st.container():
                                    st.markdown("""
                                    <div class="card animate-fade-in">
                                        <div style="display:flex;align-items:center;gap:1rem;margin-bottom:1rem">
<div style="width:40px;height:40px;background:linear-gradient(135deg, var(--accent-light), var(--accent));color:white;display:flex;align-items:center;justify-content:center;border-radius:50%;font-size:1.2rem">🧪</div>
                                            <h4 style="margin:0;color:var(--accent-dark);font-size:1.3rem">Recommended Treatment</h4>
                                        </div>
                                    """, unsafe_allow_html=True)
                                    
                                    if pesticides:
                                        st.markdown("""
                                        <div style="background:rgba(255, 255, 255, 0.7);border-radius:10px;padding:1rem;margin-bottom:1rem">
                                            <h5 style="margin-top:0;color:var(--primary-dark);display:flex;align-items:center;gap:0.5rem">
                                                <span style="color:var(--accent)">🧪</span> Recommended Herbicides
                                            </h5>
                                            <div style="display:flex;flex-wrap:wrap;gap:0.5rem">
                                        """, unsafe_allow_html=True)
                                        
                                        for pesticide in pesticides:
                                            st.markdown(f"""
                                                <span class="herbicide-pill">{pesticide}</span>
                                            """, unsafe_allow_html=True)
                                        
                                        st.markdown("</div></div>", unsafe_allow_html=True)
                                        
                                        st.markdown("""
                                        <div style="background:rgba(255, 255, 255, 0.7);border-radius:10px;padding:1rem;margin-bottom:1rem">
                                            <h5 style="margin-top:0;color:var(--primary-dark);display:flex;align-items:center;gap:0.5rem">
                                                <span style="color:var(--accent)">💡</span> Application Advice
                                            </h5>
                                        """, unsafe_allow_html=True)
                                        st.info(general_rec)
                                        st.markdown("</div>", unsafe_allow_html=True)
                                        
                                        if specific_recs:
                                            st.markdown("""
                                            <div style="background:rgba(255, 255, 255, 0.7);border-radius:10px;padding:1rem;margin-bottom:1rem">
                                                <h5 style="margin-top:0;color:var(--primary-dark);display:flex;align-items:center;gap:0.5rem">
                                                    <span style="color:var(--accent)">🌦️</span> Environmental Considerations
                                                </h5>
                                                <ul style="margin-bottom:0">
                                            """, unsafe_allow_html=True)
                                            
                                            for rec in specific_recs:
                                                st.markdown(f"<li>{rec}</li>", unsafe_allow_html=True)
                                            
                                            st.markdown("</ul></div>", unsafe_allow_html=True)
                                        
                                        st.markdown("""
                                        <div style="background:rgba(255, 143, 0, 0.1);border-radius:10px;padding:1rem;border-left:4px solid var(--accent)">
                                            <h5 style="margin-top:0;color:var(--accent-dark);display:flex;align-items:center;gap:0.5rem">
                                                <span style="color:var(--accent)">⚠️</span> Safety Precautions
                                            </h5>
                                            <ul style="margin-bottom:0">
                                                <li>Wear protective clothing, gloves, and eye protection</li>
                                                <li>Avoid application on windy days (wind speed > 10 mph)</li>
                                                <li>Follow manufacturer's instructions precisely</li>
                                                <li>Observe pre-harvest intervals for food safety</li>
                                                <li>Store pesticides in original containers away from children</li>
                                            </ul>
                                        </div>
                                        """, unsafe_allow_html=True)
                                    else:
                                        st.warning("No specific recommendations available for this weed type")
                                    
                                    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
  
