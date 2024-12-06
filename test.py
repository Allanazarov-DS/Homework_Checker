import streamlit as st
import openai

# Configure page layout
st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded"
)

# Header
st.markdown(
    """
    <div style="text-align: center; padding: 10px;">
        <h1 style="color: #4CAF50;">Student Homework Checker</h1>
        <hr style="height: 3px; border: none; background: linear-gradient(to right, red, orange, yellow, green, blue, indigo, violet);">
    </div>
    """,
    unsafe_allow_html=True
)

# Configure GPT-4o-mini API
openai.api_base = "http://localhost:8501/v1"  # Example for local GPT-4o-mini


# Define sample prompts for different languages
def get_samples(language):
    if language == "English":
        return {
            'sample': {'role': 'user', 'content': """
              You are a homework grading assistant. Analyze the following {file_type} homework:
              Task: Research: Write a 3-sentence summary on what LLMs are and their applications.
              
              Solution:
              Large Language Models (LLMs) are advanced AI models trained on massive text data to understand and generate human-like language. They are used in applications like chatbots, text summarization, language translation, and content creation. Popular LLMs include GPT for text generation and BERT for natural language understanding tasks.
              """},
            'sample2': {'role': 'assistant', 'content': """
                **Feedback**:
                Your summary is clear and concise, covering the definition and applications of LLMs effectively. However, you could expand slightly on how LLMs process data to provide a deeper understanding. Adding an example for GPT or BERT in action would make it even stronger.
                **Score**: 85/100
                """}
        }
    elif language == "Russian":
        return {
            'sample': {'role': 'user', 'content': """
              Вы помощник по оценке домашних заданий. Проанализируйте следующее домашнее задание {file_type}:
              Задача: Исследование: Напишите краткое 3-предложное резюме о том, что такое LLM и каковы их приложения.
              
              Решение:
              Большие языковые модели (LLM) — это продвинутые модели ИИ, обученные на огромных объемах текстовых данных для понимания и генерации языка, похожего на человеческий. Они используются в таких приложениях, как чат-боты, краткое изложение текста, машинный перевод и создание контента. Популярные LLM включают GPT для генерации текста и BERT для задач понимания естественного языка.
              """},
            'sample2': {'role': 'assistant', 'content': """
                **Отзыв**:
                Ваше резюме четкое и лаконичное, охватывает определение и приложения LLM эффективно. Однако вы могли бы немного подробнее рассказать о том, как LLM обрабатывают данные, чтобы лучше понять. Добавление примера работы GPT или BERT сделало бы его еще сильнее.
                **Оценка**: 85/100
                """}
        }
    elif language == "Uzbek":
        return {
            'sample': {'role': 'user', 'content': """
              Siz uyga vazifalarni baholovchi yordamchisiz. Quyidagi {file_type} uyga vazifani tahlil qiling:
              Vazifa: Tadqiqot: LLM nima ekanligi va ularning ilovalari haqida 3 gapdan iborat qisqa xulosa yozing.
              
              Yechim:
              Katta til modellari (LLM) bu inson tiliga o‘xshash tilni tushunish va yaratish uchun ulkan matn ma’lumotlari asosida o‘qitilgan ilg‘or sun’iy intellekt modellaridir. Ular chatbotlar, matnni qisqartirish, tilni tarjima qilish va kontent yaratish kabi ilovalarda ishlatiladi. Mashhur LLM'lar orasida GPT matn yaratish uchun va BERT tabiiy tildagi vazifalarni tushunish uchun qo‘llaniladi.
              """},
            'sample2': {'role': 'assistant', 'content': """
                **Fikr**:
                Sizning xulosangiz aniq va lo‘nda bo‘lib, LLM'larning ta'rifi va ularning ilovalari haqida samarali ma'lumot beradi. Ammo LLM qanday qilib ma'lumotlarni qayta ishlashi haqida batafsilroq ma’lumot kiritishingiz mumkin edi. GPT yoki BERT misolini qo‘shish uni yanada kuchliroq qilgan bo‘lardi.
                **Baholash**: 85/100
                """}
        }


# Function to analyze homework
def analyze_homework(file_content, file_type, teacher_type, feedback_language):
    input_com = st.text_input('Enter task...')
    
    # Teacher-specific instructions
    if teacher_type == "Polite":
        teacher_instructions = f"You are a polite teacher. Give kind and constructive feedback in {feedback_language}, focusing on encouragement while providing suggestions for improvement. Provide a score for the homework at the end. If the solution is really different from the task, give a lower score."
    elif teacher_type == "Strict":
        teacher_instructions = f"You are a strict teacher. Provide critical and honest feedback in {feedback_language}, focusing on areas that need improvement. Do not sugarcoat your feedback. Provide a score for the homework at the end. If the solution is not close to the task, give a much lower score. You can complain!"

    if input_com:
        samples = get_samples(feedback_language)
        prompt = f"""
        {teacher_instructions}
        Analyze the following {file_type} homework:
        Task: {input_com}
        Solution:
        ---
        {file_content}
        ---
        """

        try:
            c = openai.OpenAI(api_key=api_key)
            response = c.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {'role': 'system', 'content': 'You are a teacher who provides feedback to students. Adjust feedback based on selected language and teacher type.'},
                    samples['sample'],
                    samples['sample2'],
                    {'role': 'user', 'content': prompt}
                ],
                max_tokens=300
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"An error occurred while analyzing the homework: {e}"


# Sidebar
st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter your OpenAI API key:", type="password")
teacher_type = st.sidebar.selectbox("Choose the type of teacher:", ["Polite", "Strict"])
feedback_language = st.sidebar.selectbox("Choose feedback language:", ["English", "Russian", "Uzbek"])

# File uploader
uploaded_file = st.file_uploader("Upload Homework File", type=["py", "html", "css", "js", "txt", "ipynb"])

if api_key:
    if uploaded_file:
        file_content = uploaded_file.read().decode("utf-8")
        file_type = uploaded_file.name.split('.')[-1]
        
        with st.spinner("Analyzing homework..."):
            try:
                feedback_and_score = analyze_homework(file_content, file_type, teacher_type, feedback_language)
                
                if feedback_and_score:
                    # Extract score from the feedback
                    score_line = [line for line in feedback_and_score.split("\n") if "Score" in line]
                    score = int(score_line[0].split(":")[1].strip().replace("/100", "")) if score_line else 0
                    
                    if score < 70:
                        st.error("❌ Your homework is denied!")
                    else:
                        st.success("✅ Homework analyzed successfully!")
                    
                    st.subheader("Feedback and Score:")
                    st.write(feedback_and_score, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"An error occurred: {e}")
else:
    st.error("Please enter your API key in the sidebar to proceed.")
