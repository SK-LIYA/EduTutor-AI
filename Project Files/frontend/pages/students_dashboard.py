import streamlit as st
import requests

st.set_page_config(page_title="Take Quiz", layout="centered")
st.title("📝 Take a Quiz")

# Input form for topic and number of questions
topic = st.text_input("Enter a topic to generate a quiz")
num_questions = st.number_input("Number of questions", min_value=1, max_value=20, value=10)

if st.button("Generate Quiz"):
    if topic:
        with st.spinner("Generating quiz..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/quiz/generate",  # FastAPI quiz route
                    json={"topic": topic, "num_questions": num_questions}
                )

                if response.status_code == 200:
                    quiz_data = response.json().get("questions", [])

                    if quiz_data:
                        st.success("✅ Quiz generated successfully!")
                        st.write("### 📋 Quiz Questions:")

                        # Display each question and options
                        for idx, q in enumerate(quiz_data, 1):
                            st.write(f"**Q{idx}: {q['question']}**")
                            for option in q['options']:
                                st.write(f"- {option}")
                            st.write(f"✅ **Answer:** {q['answer']}")
                            st.write("---")  # Separator line

                    else:
                        st.warning("No questions returned from server.")
                else:
                    st.error(f"❌ Server error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"⚠️ An unexpected error occurred: {str(e)}")
    else:
        st.warning("Please enter a topic to generate quiz.")
