import streamlit as st
import datetime
import plotly.graph_objects as go
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Zodiac Insights",
    page_icon="✨",
    layout="centered"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 20px;
        padding: 10px 25px;
    }
    h1 {
        color: #2c3e50;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# Zodiac sign data
zodiac_data = {
    'Aries': {'date_range': 'Mar 21 - Apr 19', 'element': 'Fire', 'traits': 'Energetic, courageous, determined'},
    'Taurus': {'date_range': 'Apr 20 - May 20', 'element': 'Earth', 'traits': 'Reliable, patient, practical'},
    'Gemini': {'date_range': 'May 21 - Jun 20', 'element': 'Air', 'traits': 'Adaptable, curious, communicative'},
    'Cancer': {'date_range': 'Jun 21 - Jul 22', 'element': 'Water', 'traits': 'Emotional, intuitive, protective'},
    'Leo': {'date_range': 'Jul 23 - Aug 22', 'element': 'Fire', 'traits': 'Confident, creative, enthusiastic'},
    'Virgo': {'date_range': 'Aug 23 - Sep 22', 'element': 'Earth', 'traits': 'Analytical, practical, detail-oriented'},
    'Libra': {'date_range': 'Sep 23 - Oct 22', 'element': 'Air', 'traits': 'Diplomatic, gracious, fair-minded'},
    'Scorpio': {'date_range': 'Oct 23 - Nov 21', 'element': 'Water', 'traits': 'Passionate, resourceful, brave'},
    'Sagittarius': {'date_range': 'Nov 22 - Dec 21', 'element': 'Fire', 'traits': 'Optimistic, adventurous, honest'},
    'Capricorn': {'date_range': 'Dec 22 - Jan 19', 'element': 'Earth', 'traits': 'Responsible, disciplined, self-control'},
    'Aquarius': {'date_range': 'Jan 20 - Feb 18', 'element': 'Air', 'traits': 'Progressive, original, independent'},
    'Pisces': {'date_range': 'Feb 19 - Mar 20', 'element': 'Water', 'traits': 'Compassionate, artistic, intuitive'}
}

def get_zodiac_sign(birth_date):
    month = birth_date.month
    day = birth_date.day
    
    if (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return 'Aries'
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return 'Taurus'
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return 'Gemini'
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return 'Cancer'
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return 'Leo'
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return 'Virgo'
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return 'Libra'
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return 'Scorpio'
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return 'Sagittarius'
    elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return 'Capricorn'
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return 'Aquarius'
    else:
        return 'Pisces'

def create_element_chart(element):
    colors = {
        'Fire': '#FF6B6B',
        'Earth': '#4CAF50',
        'Air': '#64B5F6',
        'Water': '#2196F3'
    }
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=100,
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': colors[element]},
            'steps': [
                {'range': [0, 100], 'color': colors[element]}
            ]
        },
        title={'text': f"{element} Element"}
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    
    return fig

# App title
st.title("✨ Zodiac Insights ✨")

# Date input
birth_date = st.date_input(
    "Enter your birth date",
    format="DD/MM/YYYY"
)

if birth_date:
    # Get zodiac sign
    zodiac_sign = get_zodiac_sign(birth_date)
    sign_data = zodiac_data[zodiac_sign]
    
    # Display results in a nice container
    with st.container():
        st.markdown(f"### Your Zodiac Sign: {zodiac_sign} ♈")
        st.markdown(f"**Date Range:** {sign_data['date_range']}")
        st.markdown(f"**Element:** {sign_data['element']}")
        st.markdown(f"**Key Traits:** {sign_data['traits']}")
        
        # Create and display element chart
        element_chart = create_element_chart(sign_data['element'])
        st.plotly_chart(element_chart, use_container_width=True)
        
        # Add some fun facts
        st.markdown("---")
        st.markdown("### Fun Facts About Your Sign")
        if sign_data['element'] == 'Fire':
            st.markdown("🔥 Fire signs are known for their passion and leadership qualities!")
        elif sign_data['element'] == 'Earth':
            st.markdown("🌍 Earth signs are the most practical and grounded of all elements!")
        elif sign_data['element'] == 'Air':
            st.markdown("💨 Air signs are the intellectuals and communicators of the zodiac!")
        else:
            st.markdown("💧 Water signs are the most emotional and intuitive of all elements!")
