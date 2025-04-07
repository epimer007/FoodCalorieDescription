import streamlit as st

# Set page config must be the first Streamlit command
st.set_page_config(
    page_title="NutriScan - Food Calories Calculator",
    page_icon="🍎",
    layout="centered"
)

# Now load other dependencies

import google.generativeai as genai
from PIL import Image

# Configure Gemini
genai.configure(api_key="AIzaSyCWFFm7PXP4x2PAB6kImziaSs4d_ZKmN08")


# Rest of your code remains the same...
def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel('gemini-2.0-flash-lite')
    response = model.generate_content([input, image[0], prompt])
    return response.text


def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


# Custom CSS for styling
st.markdown("""
    <style>
        .main {
            background-color: #f8f9fa;
        }
        .stApp {
            background-image: linear-gradient(to bottom right, #f8f9fa, #e9ecef);
        }
        .stHeader {
            color: #2c3e50;
            text-align: center;
            padding: 1rem;
        }
        .stButton>button {
            background-color: #3498db;
            color: white;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            border: none;
            font-weight: bold;
            transition: all 0.3s;
        }
        .stButton>button:hover {
            background-color: #2980b9;
            transform: scale(1.02);
        }
        .stFileUploader>div>div>div>button {
            background-color: #2ecc71;
            color: white;
        }
        .stTextInput>div>div>input {
            border-radius: 8px;
            padding: 0.5rem;
        }
        .response-box {
            background-color: white;
            border-radius: 10px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-top: 1rem;
        }
        .footer {
            text-align: center;
            margin-top: 2rem;
            color: #7f8c8d;
            font-size: 0.8rem;
        }
    </style>
""", unsafe_allow_html=True)

# Header with logo
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("https://cdn-icons-png.flaticon.com/512/1046/1046857.png", width=100)
st.markdown("<h1 style='text-align: center; color: #2c3e50;'>NutriScan</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #7f8c8d; margin-top: -1rem;'>Food Nutrition Analyzer</h3>",
            unsafe_allow_html=True)

# Main content
with st.container():
    st.markdown("""
        <p style='text-align: center; color: #34495e;'>
            Upload an image of your meal to get detailed nutritional information
            and calorie count for each food item.
        </p>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Choose an image of your food...",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed"
    )

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(
            image,
            caption="Your meal",
            use_column_width=True,
            output_format="JPEG"
        )

    input_prompt = """
    You are an expert nutritionist. Analyze the food items from the image
    and calculate the total calories. Provide the details of every food item with calories intake
    in the following format:

    1. Item 1 - no of calories
    2. Item 2 - no of calories
    ---
    Also include:
    - Total calories
    - Macronutrient breakdown (carbs, proteins, fats)
    - Any notable vitamins or minerals
    - Healthier alternatives if applicable
    """

    if st.button("Analyze Nutrition", type="primary"):
        if uploaded_file is not None:
            with st.spinner("Analyzing your meal..."):
                try:
                    image_data = input_image_setup(uploaded_file)
                    response = get_gemini_response(input_prompt, image_data, "")

                    st.markdown("<div class='response-box'>", unsafe_allow_html=True)
                    st.markdown("### 🍽️ Nutrition Analysis")
                    st.markdown("---")
                    st.write(response)
                    st.markdown("</div>", unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please upload an image first")

# Footer
st.markdown("""
    <div class='footer'>
        <p>NutriScan - Making nutrition tracking simple and accessible</p>
    </div>
""", unsafe_allow_html=True)