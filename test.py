import streamlit as st
import openai


st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded")


st.markdown(
    """
    <div style="text-align: center; padding: 10px;">
        <h1 style="color: #4CAF50;">Student Homework Checker</h1>
        <hr style="height: 3px; border: none; background: linear-gradient(to right, red, orange, yellow, green, blue, indigo, violet);">
    </div>
    """,
    unsafe_allow_html=True
)

openai.api_base = "http://localhost:8501/v1" 


def analyze_homework(file_content, file_type, teacher_type):
    input_com = st.text_input('Enter task...')
    
    if teacher_type == "Polite":
        teacher_instructions = "You are a polite teacher. Give kind and constructive feedback, focusing on encouragement while providing suggestions for improvement. Provide a score for the homework at the end. If the solution is really different from task give less score"
    elif teacher_type == "Strict":
        teacher_instructions = "You are a strict teacher. Provide critical and honest feedback, focusing on areas that need improvement. Do not sugarcoat your feedback. Provide a score for the homework at the end. If solution which is provided by user is not close to the task try to score less as much as possible! You can complain!"

    prompt = f"""
    {teacher_instructions}
    Analyze the following {file_type} homework:
    Task: {input_com}
    Solution:
    ---
    {file_content}
    ---
    """

    sample = {'role': 'user', 'content': """
              You are a homework grading assistant. Analyze the following {file_type} homework:
              Task: Research: Write a 3-sentence summary on what LLMs are and their applications.
              
              Solution:
              Large Language Models (LLMs) are advanced AI models trained on massive text data to understand and generate human-like language. They are used in applications like chatbots, text summarization, language translation, and content creation. Popular LLMs include GPT for text generation and BERT for natural language understanding tasks.
              """}
    
    sample2 = {'role': 'assistant', 'content': """
                **Feedback**:
                Your summary is clear and concise, covering the definition and applications of LLMs effectively. However, you could expand slightly on how LLMs process data to provide a deeper understanding. Adding an example for GPT or BERT in action would make it even stronger.
                **Score**: 85/100
                """}

    if input_com: 
        c = openai.OpenAI(api_key=api_key)

        response = c.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[
                {'role': 'system', 'content': 'You are a teacher and your function is to give feedback to the students homework then give a score for his/her task. Do not act like bot act natural like teacher. Score the Homework out of 100!!! At the end just give score separated from the feedback nothing else!!!'},
                sample,
                sample2,
                {'role': 'user', 'content': prompt}
            ],
            max_tokens=300
        )
        return response.choices[0].message.content

st.write("Upload your homework file to receive feedback and a score.")

api_key = st.text_input("Enter your OpenAI API key:", type="password")

uploaded_file = st.file_uploader("Upload Homework File", type=["py", "html", "css", "js", "txt", 'ipynb'])

teacher_type = st.selectbox("Choose the type of teacher to check your homework:", ["Polite", "Strict"])

if api_key:
    if uploaded_file:
        file_content = uploaded_file.read().decode("utf-8")
        file_type = uploaded_file.name.split('.')[-1]
        
        with st.spinner("Analyzing homework..."):
            try:
                feedback_and_score = analyze_homework(file_content, file_type, teacher_type)
                
                if feedback_and_score:
                    score_line = [line for line in feedback_and_score.split("\n") if "Score" in line]
                    if score_line:
                        score = int(score_line[0].split(":")[1].strip().replace("/100", ""))
                    else:
                        score = 0  
                    
                    if score < 70:
                        st.error("❌ Your homework is denied!")
                    else:
                        st.success("✅ Homework analyzed successfully!")
                    
                    st.subheader("Feedback and Score:")
                    st.write(feedback_and_score, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"An error occurred: {e}")
else:
    st.error('Firt enter api-key!!!')