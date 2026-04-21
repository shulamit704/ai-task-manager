import streamlit as st
import requests
import json

# משיכת המפתח מה-Secrets של Streamlit - הדרך המאובטחת
# וודא שהגדרת API_KEY בתוך Settings > Secrets ב-Streamlit Cloud
try:
    API_KEY = st.secrets["API_KEY"]
except:
    st.error("שגיאה: מפתח ה-API לא נמצא ב-Secrets של המערכת.")
    st.stop()

# נתיב ה-API למודל Gemini 3.1 Flash Lite
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite-preview:generateContent?key={API_KEY}"

# הגדרות דף
st.set_page_config(page_title="Task Master AI", layout="centered")

# עיצוב CSS - נקי ומתאים לענן
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;700&display=swap');

    .block-container { padding-top: 2rem; max-width: 700px; }
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Assistant', sans-serif;
        direction: rtl;
        text-align: right;
    }

    h1, h4, p, span, label { text-align: right !important; direction: rtl !important; }

    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background: linear-gradient(90deg, #4A90E2 0%, #357ABD 100%);
        color: white;
        font-weight: bold;
        border: none;
    }

    .result-container {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        border-right: 6px solid #4A90E2;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        margin-top: 20px;
    }

    .task-step {
        background-color: #f0f7ff;
        margin-bottom: 10px;
        padding: 10px 15px;
        border-radius: 8px;
        border: 1px solid #e1eefb;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Task Master AI")
st.markdown("#### פירוק משימות מהיר לצעדים פשוטים")

# ממשק המשתמש
task_title = st.text_input("מה המשימה שתרצה לפרק?", placeholder="למשל: תכנון טיול לחו\"ל")
generate_btn = st.button("פרק לי את המשימה! ✨")

if generate_btn:
    if task_title:
        with st.spinner("ה-AI מנתח את המשימה..."):
            # בניית הבקשה עבור ה-API
            payload = {
                "contents": [{
                    "parts": [{"text": f"פרק את המשימה '{task_title}' ל-5 שלבים אופרטיביים קצרים בעברית. החזר רק את השלבים עצמם."}]
                }],
                "generationConfig": {
                    "temperature": 0.4,
                    "maxOutputTokens": 300
                }
            }
            headers = {'Content-Type': 'application/json'}
            
            try:
                # שליחת הבקשה (שימוש ב-Standard SSL של השרת)
                response = requests.post(URL, headers=headers, data=json.dumps(payload))
                
                if response.status_code == 200:
                    result = response.json()
                    # שליפת הטקסט מהתגובה של גוגל
                    ai_text = result['candidates'][0]['content']['parts'][0]['text']
                    steps = [s.strip() for s in ai_text.strip().split('\n') if s.strip()]

                    st.markdown("##### 📋 תוכנית הפעולה שלך:")
                    
                    # הצגת התוצאות בעיצוב יפה
                    html_output = '<div class="result-container">'
                    for i, step in enumerate(steps[:5], 1):
                        # הסרת סימני כוכביות או מספרים שה-AI עלול להוסיף
                        clean_step = step.lstrip('0123456789.-* ')
                        html_output += f'<div class="task-step"><b>{i}.</b> {clean_step}</div>'
                    html_output += '</div>'
                    
                    st.markdown(html_output, unsafe_allow_html=True)
                    st.success("השלבים מוכנים!")
                
                else:
                    # כאן השורות שביקשת לאבחון השגיאה
                    st.error(f"שגיאה מהשרת (קוד {response.status_code})")
                    with st.expander("פרטי שגיאה טכניים"):
                        st.write(response.text)
                    
            except Exception as e:
                st.error(f"שגיאה בחיבור לשרת: {e}")
    else:
        st.warning("נא להזין משימה כדי להתחיל.")

st.markdown("<br><hr><center><small>© 2026 Task Master AI - Gemini 3.1 Powered</small></center>", unsafe_allow_html=True)
