import streamlit as st
import requests
import json
import os
import urllib3

# ביטול אזהרות SSL עבור נטפרי
os.environ['CURL_CA_BUNDLE'] = ''
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# הגדרות API
API_KEY = "AIzaSyCFBw11fNWD4w72cJK2SXuJ67ssP8NI1Oo"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite-preview:generateContent?key={API_KEY}"

# הגדרות דף - שימוש במצב רחב כדי לנצל את צדי המסך אם צריך
st.set_page_config(page_title="Task Master AI", page_icon="🎯", layout="centered")

# הזרקת CSS דחוס למניעת גלילה
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;700&display=swap');

    /* צמצום מרווחי המערכת של Streamlit */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        max-width: 700px;
    }

    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Assistant', sans-serif;
        direction: rtl;
        text-align: right;
        overflow: hidden; /* מניעת גלילה כללית */
    }

    /* תיקון כותרות */
    h1 { margin-bottom: 0.5rem !important; font-size: 2rem !important; }
    h4 { margin-top: 0 !important; margin-bottom: 1rem !important; }

    h1, h2, h3, h4, p, span, label {
        text-align: right !important;
        direction: rtl !important;
    }

    /* עיצוב כפתור וקלט בצורה קומפקטית */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background: linear-gradient(90deg, #4A90E2 0%, #357ABD 100%);
        color: white;
        font-weight: bold;
        border: none;
        margin-top: 5px;
    }

    /* כרטיס תוצאה קומפקטי */
    .result-container {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 15px;
        border-right: 6px solid #4A90E2;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        margin-top: 15px;
        max-height: 400px; /* הגבלת גובה */
        overflow-y: auto; /* גלילה פנימית רק אם ממש חייב */
    }

    .task-step {
        background-color: #f0f7ff;
        margin-bottom: 8px;
        padding: 8px 15px;
        border-radius: 8px;
        border: 1px solid #e1eefb;
        font-size: 0.95rem;
    }

    /* צמצום רווחים בין אלמנטים */
    .stTextInput { margin-bottom: -10px; }
    
    /* הסתרת תפריטים מיותרים לחיסכון במקום */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# כותרת הממשק
st.title("🎯 Task Master AI")
st.markdown("#### פירוק משימות מהיר לצעדים פשוטים")

# אזור הקלט
task_title = st.text_input("מה המשימה שתרצה לפרק?", placeholder="למשל: ארגון אירוע משפחתי")
generate_btn = st.button("פרק לי את המשימה! ✨")

if generate_btn:
    if task_title:
        with st.spinner("מנתח..."):
            prompt = f"פרק את המשימה '{task_title}' ל-5 שלבים אופרטיביים קצרים מאוד בעברית. החזר רק את השלבים בשורות חדשות."
            
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.4, "maxOutputTokens": 150}
            }
            
            try:
                response = requests.post(URL, headers={'Content-Type': 'application/json'}, data=json.dumps(payload), verify=False)
                
                if response.status_code == 200:
                    result = response.json()
                    ai_text = result['candidates'][0]['content']['parts'][0]['text']
                    steps = [s.strip() for s in ai_text.strip().split('\n') if s.strip()]

                    st.markdown("##### 📋 תוכנית הפעולה שלך:")
                    
                    html_output = '<div class="result-container">'
                    for i, step in enumerate(steps[:5], 1):
                        html_output += f'<div class="task-step"><b>{i}.</b> {step}</div>'
                    html_output += '</div>'
                    
                    st.markdown(html_output, unsafe_allow_html=True)
                else:
                    st.error("שגיאה בתקשורת.")
            except Exception as e:
                st.error(f"שגיאה טכנית: {e}")
    else:
        st.warning("נא להזין משימה.")

# הערת שוליים צמודה לתחתית
st.markdown("<div style='text-align: center; color: gray; font-size: 0.8rem; margin-top: 10px;'>© 2026 Task Master AI</div>", unsafe_allow_html=True)
