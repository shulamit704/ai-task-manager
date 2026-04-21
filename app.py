import streamlit as st
import requests
import json
import os
import urllib3

# ביטול אזהרות SSL עבור נטפרי
os.environ['CURL_CA_BUNDLE'] = ''
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# הגדרות API
API_KEY = "your API_KEY"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite-preview:generateContent?key={API_KEY}"

# הגדרות דף
st.set_page_config(page_title="Task Master AI", page_icon="🎯", layout="centered")

# הזרקת CSS מתקדם לתיקון יישור מלא לימין (RTL)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;700&display=swap');

    /* הגדרות גופן וכיווניות גלובלית */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Assistant', sans-serif;
        direction: rtl;
        text-align: right;
    }

    /* תיקון יישור לכותרות וטקסט */
    h1, h2, h3, h4, h5, h6, p, span, label {
        text-align: right !important;
        direction: rtl !important;
        display: block;
    }

    /* יישור תיבת הקלט והכפתור */
    [data-testid="stTextField"] {
        direction: rtl;
    }
    
    /* יישור ספציפי לכפתור Streamlit */
    .stButton {
        text-align: right;
    }

    /* עיצוב כפתור הפעלה */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background: linear-gradient(90deg, #4A90E2 0%, #357ABD 100%);
        color: white;
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 15px rgba(74, 144, 226, 0.3);
        transition: all 0.3s ease;
        margin-top: 10px;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(74, 144, 226, 0.4);
        color: white;
    }

    /* עיצוב כרטיס התוצאה */
    .result-container {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 20px;
        border-right: 8px solid #4A90E2;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        margin-top: 30px;
        line-height: 1.8;
        color: #333;
        text-align: right;
    }

    .task-step {
        background-color: #f0f7ff;
        margin-bottom: 10px;
        padding: 12px 18px;
        border-radius: 10px;
        border: 1px solid #e1eefb;
        font-weight: 500;
        text-align: right;
    }
    </style>
    """, unsafe_allow_html=True)

# כותרת הממשק
st.title("🎯 Task Master AI")
st.markdown("#### בוא נהפוך את המשימה הגדולה שלך לצעדים פשוטים")

# אזור הקלט
task_title = st.text_input("מה המשימה שתרצה לפרק?", placeholder="למשל: ארגון אירוע משפחתי", help="הזן משימה וה-AI יפרק אותה עבורך")
generate_btn = st.button("פרק לי את המשימה! ✨")

if generate_btn:
    if task_title:
        with st.spinner("מנתח את המשימה..."):
            prompt = f"פרק את המשימה '{task_title}' ל-5 שלבים אופרטיביים בעברית. החזר רק את השלבים, כל שלב בשורה חדשה, ללא מספור."
            
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.4, "maxOutputTokens": 200}
            }
            
            try:
                response = requests.post(URL, headers={'Content-Type': 'application/json'}, data=json.dumps(payload), verify=False)
                
                if response.status_code == 200:
                    result = response.json()
                    ai_text = result['candidates'][0]['content']['parts'][0]['text']
                    steps = [s.strip() for s in ai_text.strip().split('\n') if s.strip()]

                    st.markdown("### 📋 תוכנית הפעולה שלך:")
                    
                    # בניית פלט ה-HTML
                    html_output = '<div class="result-container">'
                    for i, step in enumerate(steps[:5], 1):
                        html_output += f'<div class="task-step"><b>{i}.</b> {step}</div>'
                    html_output += '</div>'
                    
                    st.markdown(html_output, unsafe_allow_html=True)
                    # st.balloons() # הוסר לבקשתך
                else:
                    st.error("שגיאה בתקשורת עם השרת.")
            except Exception as e:
                st.error(f"שגיאה טכנית: {e}")
    else:
        st.warning("נא להזין משימה.")

st.markdown("<br><br>", unsafe_allow_html=True)
st.caption("© 2026 Task Master AI • חווית משתמש מותאמת")