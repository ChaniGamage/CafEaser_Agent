import streamlit as st
import pandas as pd
from generator import generate_meal_combo
from datetime import datetime

# Set page configuration for better layout
st.set_page_config(page_title="CafEaser Meal Recommender", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for attractive interface
st.markdown("""
   <style>
    /* Global styling */
    body {
        font-family: 'Arial', sans-serif;
        background-color: #fdf6ec; /* Light tan background */
    }

    .stApp {
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        padding: 20px;
    }

    /* Sidebar styling */
    .css-1d391kg {
        background-color: #6B4226; /* Brown */
        color: #ffffff;
        padding: 20px;
        border-radius: 10px;
    }

    .sidebar .sidebar-content {
        color: #ffffff;
    }

    .sidebar .stButton>button {
        background-color: #A47148; /* Lighter brown */
        color: #ffffff;
        border-radius: 8px;
        font-weight: bold;
        padding: 10px;
        width: 100%;
        transition: background-color 0.3s;
    }

    .sidebar .stButton>button:hover {
        background-color: #8B5E3C;
    }

    /* Main content styling */
    h1, h2, h3 {
        color: #6B4226; /* Brown */
        font-weight: bold;
    }

    .stButton>button {
        background-color: #A47148;
        color: #ffffff;
        border-radius: 8px;
        font-weight: bold;
        padding: 10px 20px;
        transition: background-color 0.3s;
    }

    .stButton>button:hover {
        background-color: #8B5E3C;
    }

    .stSelectbox, .stNumberInput, .stTextInput {
        background-color: #F5F5DC; /* Beige */
        border-radius: 8px;
        padding: 10px;
    }

    .stMarkdown p {
        color: #4B3832; /* Deep brown for text */
        line-height: 1.6;
    }

    .stSuccess, .stInfo {
        border-radius: 8px;
        padding: 15px;
    }

    /* Centered image styling */
    .center-image {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 30px 0;
    }

    .center-image img {
        max-width: 80%;
        height: auto;
        border-radius: 12px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
    }
</style>

""",
 unsafe_allow_html=True
 )


# Sidebar for navigation and user inputs
st.sidebar.title("CafEaser Navigation")
st.sidebar.markdown("Welcome to your meal planner! Select an option or question below.", unsafe_allow_html=True)

# User input section
with st.sidebar.form("user_input_form"):
    st.subheader("Your Preferences")
    budget = st.number_input("Budget (Rs.)", min_value=100, max_value=500, value=300, step=50)
    dietary = st.selectbox("Dietary Preference", ["Any", "Vegetarian", "Vegan", "Non-Veg"])
    spice_level = st.selectbox("Spice Level", ["Mild", "Medium", "Spicy"])
    submit_profile = st.form_submit_button("Save Preferences")

# Predefined questions and answers using generator
questions = {
    "What’s a quick meal under my budget?": lambda budget, dietary, spice_level: (
        f"Try {generate_meal_combo(budget, dietary, spice_level, datetime.now().strftime('%H:%M'))[0]['meal_name']} "
        f"with {generate_meal_combo(budget, dietary, spice_level, datetime.now().strftime('%H:%M'))[0]['beverage_name']} "
        f"for Rs. {generate_meal_combo(budget, dietary, spice_level, datetime.now().strftime('%H:%M'))[0]['total_price']}."
    ),
    "What should I eat for breakfast?": lambda budget, dietary, spice_level: (
        f"For breakfast, try {generate_meal_combo(budget, dietary, spice_level, '08:00')[0]['meal_name']} "
        f"with {generate_meal_combo(budget, dietary, spice_level, '08:00')[0]['beverage_name']} "
        f"for Rs. {generate_meal_combo(budget, dietary, spice_level, '08:00')[0]['total_price']}."
    ),
    "What’s a healthy meal option?": lambda budget, dietary, spice_level: (
        f"A healthy option is {generate_meal_combo(budget, dietary, spice_level, datetime.now().strftime('%H:%M'))[0]['meal_name']} "
        f"with {generate_meal_combo(budget, dietary, spice_level, datetime.now().strftime('%H:%M'))[0]['beverage_name']} "
        f"for Rs. {generate_meal_combo(budget, dietary, spice_level, datetime.now().strftime('%H:%M'))[0]['total_price']}."
    ),
    "What’s a popular meal combo?": lambda budget, dietary, spice_level: (
        f"A popular combo is {generate_meal_combo(budget, dietary, spice_level, datetime.now().strftime('%H:%M'))[0]['meal_name']} "
        f"with {generate_meal_combo(budget, dietary, spice_level, datetime.now().strftime('%H:%M'))[0]['beverage_name']} "
        f"for Rs. {generate_meal_combo(budget, dietary, spice_level, datetime.now().strftime('%H:%M'))[0]['total_price']}."
    ),
    "What should I eat before a class?": lambda budget, dietary, spice_level: (
        f"Before a class, try {generate_meal_combo(budget, dietary, spice_level, datetime.now().strftime('%H:%M'))[0]['meal_name']} "
        f"with {generate_meal_combo(budget, dietary, spice_level, datetime.now().strftime('%H:%M'))[0]['beverage_name']} "
        f"for Rs. {generate_meal_combo(budget, dietary, spice_level, datetime.now().strftime('%H:%M'))[0]['total_price']}."
    ),
    "How can I save money on meals?": lambda budget, dietary, spice_level: (
        f"To save money, choose affordable combos like {generate_meal_combo(budget, dietary, spice_level, datetime.now().strftime('%H:%M'))[0]['meal_name']} "
        f"with {generate_meal_combo(budget, dietary, spice_level, datetime.now().strftime('%H:%M'))[0]['beverage_name']} "
        f"and stick to a budget of Rs. {budget} or less."
    ),
}

# Main content
st.title("CafEaser 🍽️")
st.markdown("Your Personal Meal Recommender - Let’s Find Your Perfect Combo!", unsafe_allow_html=True)

# Display saved profile if submitted
if 'profile_submitted' in st.session_state and st.session_state.profile_submitted:
    st.success("Preferences saved! Here’s your personalized meal combo and answers.")
    budget = st.session_state.get('budget', budget)
    dietary = st.session_state.get('dietary', dietary)
    spice_level = st.session_state.get('spice_level', spice_level)
    time_of_day = datetime.now().strftime("%H:%M")

    # Generate meal combo
    meal_plan = generate_meal_combo(budget, dietary, spice_level, time_of_day)

    # Display meal combo
    st.subheader("Today’s Meal Combo")
    for combo in meal_plan:
        st.markdown(
            f"- **{combo['day']}**: {combo['meal_name']} + {combo['beverage_name']} "
            f"(Rs. {combo['total_price']}, {combo['prep_time']} min prep time)",
            unsafe_allow_html=True
        )

    # Question and answer section
    st.subheader("Ask a Question")
    selected_question = st.selectbox("Choose a question:", list(questions.keys()))
    if st.button("Get Answer"):
        answer = questions[selected_question](budget, dietary, spice_level)
        st.markdown(f"**Answer**: {answer}", unsafe_allow_html=True)

    # Feedback section
    st.subheader("Feedback")
    with st.form("feedback_form"):
        rating = st.slider("Rate this recommendation (1-5)", 1, 5, 3)
        comment = st.text_area("Comments (optional)")
        feedback_submitted = st.form_submit_button("Submit Feedback")
        if feedback_submitted:
            with open("feedback.txt", "a") as f:
                f.write(f"Rating: {rating}, Comment: {comment}, Time: {time_of_day}\n")
            st.success("Thank you for your feedback!")

    # Reasoning
    st.subheader("Reasoning")
    st.markdown(
        f"This meal combo is tailored for your Rs. {budget} budget, {dietary} diet, and {spice_level} preference. "
        f"It’s suitable for {time_of_day}, ensuring a quick and affordable option for your university schedule.",
        unsafe_allow_html=True
    )

# Save profile to session state
if submit_profile:
    st.session_state.profile_submitted = True
    st.session_state.budget = budget
    st.session_state.dietary = dietary
    st.session_state.spice_level = spice_level
    st.rerun()

# Initial instructions if no profile
if 'profile_submitted' not in st.session_state:
    st.info("Please fill out your preferences in the sidebar to get started!")