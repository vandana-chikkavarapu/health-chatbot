import streamlit as st

# Page setup
st.set_page_config(page_title="Health AI Chatbot", page_icon="💬", layout="centered")

# Apply custom CSS for light green + gray clean UI
st.markdown("""
<style>
body {
    background-color: #f3f4f6;
}
.chat-container {
    background: #ffffff;
    padding: 25px 20px 120px 20px;
    border-radius: 16px;
    max-width: 700px;
    margin: 30px auto;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    height: 70vh;
    overflow-y: auto;
}
.chat-bubble {
    padding: 12px 18px;
    margin: 10px 0;
    border-radius: 20px;
    max-width: 75%;
    font-size: 15px;
    line-height: 1.5;
}
.user {
    background-color: #d2f5c7;
    align-self: flex-end;
    margin-left: auto;
    text-align: right;
}
.bot {
    background-color: #f1f1f1;
    align-self: flex-start;
    margin-right: auto;
    text-align: left;
}
.input-row {
    position: fixed;
    bottom: 20px;
    left: 0;
    right: 0;
    display: flex;
    justify-content: center;
}
input[type="text"] {
    width: 70%;
    padding: 14px;
    border-radius: 25px;
    border: 1.5px solid #ccc;
    font-size: 16px;
}
button {
    background-color: #2563eb;
    color: white;
    font-weight: 600;
    padding: 12px 20px;
    border-radius: 25px;
    border: none;
    margin-left: 10px;
}
button:hover {
    background-color: #1d4ed8;
}
</style>
""", unsafe_allow_html=True)

# Session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Response logic (70+ global health issues)
def get_response(message):
    msg = message.lower()
    symptoms = {
        "cold": "You may have a cold. Rest and drink warm fluids.",
        "fever": "You may have a fever. Stay hydrated and monitor temperature.",
        "headache": "May be due to stress or dehydration. Take rest.",
        "cough": "Could be dry or wet cough. Try steam inhalation.",
        "sore throat": "Gargle with salt water. Avoid spicy foods.",
        "nausea": "May be due to indigestion. Avoid oily food.",
        "vomiting": "Stay hydrated. See doctor if continues.",
        "diarrhea": "Drink ORS and avoid dairy. Rest well.",
        "constipation": "Add fiber and fluids to your diet.",
        "gas": "Avoid carbonated drinks and spicy food.",
        "stomach pain": "Could be acidity or infection. Eat light food.",
        "chest pain": "Can be serious. Please seek emergency care.",
        "breathlessness": "Stop activity and rest. Emergency if worsens.",
        "fatigue": "May be due to low iron or sleep. Get tested.",
        "dizziness": "Can be low BP or dehydration. Sit down and rest.",
        "body pain": "May be viral. Rest and paracetamol can help.",
        "back pain": "Avoid heavy lifting. Use heat therapy.",
        "joint pain": "Could be arthritis. Try anti-inflammatory foods.",
        "eye pain": "Reduce screen time. Use lubricating drops.",
        "blurred vision": "Eye check-up is advised.",
        "toothache": "Rinse with salt water. See a dentist if severe.",
        "ear pain": "Avoid poking. May be infection.",
        "itching": "May be allergy. Use antihistamine cream.",
        "rash": "Could be allergic. Apply calamine lotion.",
        "burning sensation": "Could be acidity or infection. Drink water.",
        "sneezing": "Could be viral or allergy.",
        "sensitivity to light": "May be migraine. Rest in dark room.",
        "difficulty swallowing": "Gargle with warm salt water.",
        "urine pain": "May be UTI. Drink water and consult doctor.",
        "frequent urination": "Can indicate UTI or diabetes.",
        "dry skin": "Use moisturizer and drink more water.",
        "depression": "You're not alone. Please talk to a professional.",
        "anxiety": "Practice deep breathing. Talk to a therapist.",
        "insomnia": "Try reducing screen time before bed.",
        "palpitations": "Could be stress or medical. Consult doctor.",
        "acne": "Avoid oily food. Keep skin clean.",
        "weight gain": "Could be hormonal or lifestyle. Track diet.",
        "weight loss": "If sudden, consult a physician.",
        "nosebleed": "Sit upright and pinch your nose gently.",
        "hair fall": "Could be due to stress, diet, or hormones.",
        "menstrual pain": "Use heat pad and rest. Painkillers if needed.",
        "irregular periods": "May be PCOS. Track your cycle.",
        "dark circles": "Can be lack of sleep or stress.",
        "swelling": "Could be injury or infection. Apply ice.",
        "allergy": "Avoid known triggers. Try antihistamines.",
        "dry mouth": "Drink water frequently. Avoid salty food.",
        "acid reflux": "Avoid late-night meals and spicy food.",
        "dehydration": "Drink ORS or water with salt + sugar.",
        "low bp": "Eat salty snacks, hydrate, and rest.",
        "high bp": "Avoid salt. Relax and monitor regularly.",
        "stress": "Try breathing exercises or short walks.",
        "blurred thinking": "Can be due to stress or lack of sleep.",
        "covid": "Isolate, rest, and get tested. Monitor oxygen levels.",
        "malaria": "High fever and chills — consult doctor immediately.",
        "typhoid": "Prolonged fever and weakness. Needs antibiotic treatment.",
        "dengue": "Fever + joint pain. Avoid painkillers. Do CBC test.",
        "tuberculosis": "Persistent cough >2 weeks. Needs medical testing.",
        "bronchitis": "Coughing with mucus. Avoid smoke and cold drinks.",
        "asthma": "Use inhaler. Avoid dust and cold weather.",
        "migraine": "Dark room rest. Avoid triggers like loud noise.",
        "psoriasis": "Autoimmune skin issue. Use medicated creams.",
        "eczema": "Dry itchy skin. Apply moisturizer. Avoid triggers.",
        "pcos": "Irregular periods, acne. Consult gynecologist.",
        "pregnancy": "Take prenatal care. Consult OB/GYN regularly.",
        "ulcer": "Avoid spicy food. Take antacids.",
        "appendicitis": "Lower right abdomen pain. Needs emergency surgery.",
        "jaundice": "Yellow eyes/skin. Do liver test. Rest required.",
        "hepatitis": "Liver inflammation. Avoid alcohol. Do LFT tests.",
        "arthritis": "Joint stiffness and swelling. Needs long-term care.",
        "anemia": "Low hemoglobin. Eat iron-rich foods or supplements.",
        "thyroid": "Weight issues + fatigue. Do thyroid profile blood test.",
        "cholesterol": "Avoid fried foods. Get lipid profile checked."
    }

    for symptom, reply in symptoms.items():
        if symptom in msg:
            return reply

    return "Sorry, I couldn't detect a known symptom. Please describe it differently or consult a doctor."

# Show previous chat
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for role, msg in st.session_state.chat_history:
    bubble_class = "user" if role == "user" else "bot"
    st.markdown(f'<div class="chat-bubble {bubble_class}">{msg}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Chat input + submit button (fixed bottom)
with st.form("chat_input_form", clear_on_submit=True):
    st.markdown('<div class="input-row">', unsafe_allow_html=True)
    col1, col2 = st.columns([6, 1])
    with col1:
        user_msg = st.text_input(
            label="",
            placeholder="Type your health symptom...",
            label_visibility="collapsed"
        )
    with col2:
        send = st.form_submit_button("Submit")
    st.markdown('</div>', unsafe_allow_html=True)

# When user submits
if send and user_msg:
    st.session_state.chat_history.append(("user", user_msg))
    bot_reply = get_response(user_msg)
    st.session_state.chat_history.append(("bot", bot_reply))