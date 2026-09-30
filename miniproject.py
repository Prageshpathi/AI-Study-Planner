import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
#load environment variables 

load_dotenv()
#get the API key from environment variables
api_key = os.getenv("GROQ_API_KEY")
#check api
if not api_key:
    st.error("Error API key not found!!!")
    st.stop()

#create groq client
client = Groq(api_key=api_key)

MODEL="openai/gpt-oss-120b"

st.set_page_config(page_title="AI Study PLANNER", page_icon="!!!", layout="centered")
st.markdown("""
<style>

.main {
    background-color: #f5f7fb;
}

.title {
    text-align: center;
    font-size: 45px;
    font-weight: bold;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #666;
    font-size: 18px;
    margin-bottom: 30px;
}

.card {
    background-color: white;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)
st.markdown(
    '<div class="title">📚 AI Study Planner</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Your personal AI-powered learning companion 🤖</div>',
    unsafe_allow_html=True
)

st.markdown('<div class="card">', unsafe_allow_html=True)

st.subheader("🎯 What do you want to learn?")

topic = st.text_input(
    "Enter a topic",
    placeholder="e.g. Artificial Intelligence"
)

col1, col2 = st.columns(2)

with col1:
    difficulty = st.selectbox(
        "📈 Difficulty",
        ["Beginner", "Intermediate", "Advanced"]
    )

with col2:
    option = st.selectbox(
        "📝 Learning Mode",
        [
            "1.Summarize",
            "2.Quiz",
            "3. 1 Month Study Plan",
            "4.Explain"
        ]
    )

st.markdown('</div>', unsafe_allow_html=True)
if st.button("Generate", type="primary"):
    if not topic:
        st.error("Please enter a topic.")
    else:
        prompt = f"""Create a {option} for {topic} at {difficulty} level.
        Explain everything clearly using simple language.
        Follow the below format:
        if option is 1.Summarize:
        1. Summary of the topic
        if option is 2.Quiz:
        1. 5 questions with answers
        if option is 3. 1 Month Study Plan:
            1. Week 1: Topics to cover
            2. Week 2: Topics to cover
            3. Week 3: Topics to cover
            4. Week 4: Topics to cover
        """

        with st.spinner("Generating..."):
            try:
                chat_completion = client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful assistant that creates study plans for students."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.7
                )
                answer = chat_completion.choices[0].message.content
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.subheader("✨ Your AI-Generated Learning Plan")
                st.markdown(answer)
                st.download_button(
                      label="📥 Download Study Plan",
                      data=answer,
                      file_name="my_study_plan.txt",
                      mime="text/plain")
                st.markdown('</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {e}")