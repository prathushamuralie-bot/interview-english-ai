import streamlit as st
import google.generativeai as genai
import os
import json
import datetime
from dotenv import load_dotenv

# ---------------------------
# Setup
# ---------------------------
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")

st.set_page_config(page_title="InterviewEnglish AI", page_icon="🎯", layout="wide")

PROGRESS_FILE = "progress.json"


# ---------------------------
# Progress Tracker Helpers
# ---------------------------
def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    return {"total_practices": 0, "by_feature": {}, "last_practice_date": "", "streak": 0}


def save_progress(data):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(data, f)


def log_practice(feature_name):
    data = load_progress()
    today = str(datetime.date.today())

    data["total_practices"] = data.get("total_practices", 0) + 1
    data["by_feature"][feature_name] = data.get("by_feature", {}).get(feature_name, 0) + 1

    last_date = data.get("last_practice_date", "")
    if last_date != today:
        if last_date == str(datetime.date.today() - datetime.timedelta(days=1)):
            data["streak"] = data.get("streak", 0) + 1
        elif last_date != today:
            data["streak"] = 1
        data["last_practice_date"] = today

    save_progress(data)


# ---------------------------
# Sidebar Navigation
# ---------------------------
st.sidebar.title("🎯 InterviewEnglish AI")
st.sidebar.write("Your daily English practice companion")

progress_data = load_progress()
st.sidebar.metric("🔥 Day Streak", progress_data.get("streak", 0))
st.sidebar.metric("✅ Total Practices", progress_data.get("total_practices", 0))
st.sidebar.divider()

page = st.sidebar.radio(
    "Choose a feature",
    [
        "🏠 Home",
        "📝 Self-Introduction Builder",
        "✅ Grammar Check",
        "🎤 Mock Interview Chat",
        "📚 Vocabulary Builder",
        "💬 Daily Conversation Practice",
        "🎯 Daily Challenge",
        "⚠️ Common Mistakes (Tamil Speakers)",
        "🎓 Grammar Lessons",
        "📊 My Progress",
    ],
)

st.sidebar.divider()
st.sidebar.caption("Built by Jee | Practice every day to improve faster 🚀")


# ---------------------------
# Home Page
# ---------------------------
if page == "🏠 Home":
    st.title("Welcome to InterviewEnglish AI 🎯")
    st.write(
        "An AI-powered companion to help you practice spoken and written "
        "English for interviews and everyday conversations."
    )
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.subheader("📝 Build")
        st.write("Create a confident self-introduction in seconds.")
    with col2:
        st.subheader("🎤 Practice")
        st.write("Mock interviews and daily conversation topics.")
    with col3:
        st.subheader("✅ Improve")
        st.write("Instant grammar feedback to fix your mistakes.")
    with col4:
        st.subheader("📊 Track")
        st.write("Daily challenges and progress tracking to stay consistent.")
    st.info("👈 Use the sidebar to pick a feature and start practicing.")


# ---------------------------
# Self-Introduction Builder
# ---------------------------
elif page == "📝 Self-Introduction Builder":
    st.title("📝 Self-Introduction Builder")
    st.write("Fill in your details, AI will create a polished self-introduction for your interview.")

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Your Name")
        course = st.text_input("Your Course/Degree (e.g., B.Tech IT, 2024-2028)")
        skills = st.text_input("Your Key Skills (e.g., Python, Flutter, SQL)")
    with col2:
        strength = st.text_input("Your Biggest Strength")
        goal = st.text_input("Your Career Goal (e.g., become a Software Engineer)")

    if st.button("Generate My Introduction", type="primary"):
        if name and course:
            with st.spinner("Generating your introduction..."):
                prompt = f"""
                You are an interview coach helping a student prepare a confident,
                professional self-introduction for a job interview.

                Student details:
                Name: {name}
                Course: {course}
                Skills: {skills}
                Strength: {strength}
                Career Goal: {goal}

                Write a natural, confident, 60-90 second spoken self-introduction
                in simple, correct English (suitable for a student with intermediate
                English level). Keep it conversational, not robotic. Then below it,
                list 2-3 tips to deliver it confidently.
                """
                response = model.generate_content(prompt)
                st.success("Here's your self-introduction:")
                st.write(response.text)
                log_practice("Self-Introduction Builder")
        else:
            st.warning("Please fill in at least your Name and Course.")


# ---------------------------
# Grammar Check
# ---------------------------
elif page == "✅ Grammar Check":
    st.title("✅ Grammar Check")
    st.write("Type any sentence you plan to use in your interview, and get instant feedback.")

    user_sentence = st.text_area("Type your sentence here", height=100)

    if st.button("Check My Sentence", type="primary"):
        if user_sentence:
            with st.spinner("Checking..."):
                prompt = f"""
                You are an English grammar tutor for a Tamil Nadu engineering student
                preparing for job interviews.

                Check this sentence for grammar mistakes: "{user_sentence}"

                1. Point out any mistakes simply.
                2. Give the corrected sentence.
                3. Briefly explain the rule in 1-2 lines (simple English).
                """
                response = model.generate_content(prompt)
                st.success("Feedback:")
                st.write(response.text)
                log_practice("Grammar Check")
        else:
            st.warning("Please type a sentence first.")


# ---------------------------
# Mock Interview Chat
# ---------------------------
elif page == "🎤 Mock Interview Chat":
    st.title("🎤 Mock Interview Chat")
    st.write("Practice answering interview questions. AI will ask you a question, you answer, and get feedback.")

    if "current_question" not in st.session_state:
        st.session_state.current_question = ""
    if "interview_started" not in st.session_state:
        st.session_state.interview_started = False

    if st.button("Start / Next Question", type="primary"):
        with st.spinner("Thinking of a question..."):
            prompt = """
            You are a friendly HR interviewer conducting a mock interview for a
            fresher engineering student applying for a software engineering role.
            Ask ONE common interview question (e.g., about strengths, weaknesses,
            teamwork, projects, why this company, career goals).
            Just give the question, nothing else. Keep it short and natural.
            """
            response = model.generate_content(prompt)
            st.session_state.current_question = response.text
            st.session_state.interview_started = True

    if st.session_state.interview_started:
        st.info(f"**Interviewer asks:** {st.session_state.current_question}")
        user_answer = st.text_area("Your Answer", key="interview_answer", height=100)

        if st.button("Submit My Answer", type="primary"):
            if user_answer:
                with st.spinner("Reviewing your answer..."):
                    prompt = f"""
                    You are an interview coach. The student was asked:
                    "{st.session_state.current_question}"

                    Their answer: "{user_answer}"

                    1. Give brief feedback on the content (was it a good answer?).
                    2. Point out any grammar mistakes and give the corrected version.
                    3. Give one tip to make the answer stronger.
                    Keep the feedback encouraging and simple.
                    """
                    response = model.generate_content(prompt)
                    st.success("Feedback on your answer:")
                    st.write(response.text)
                    log_practice("Mock Interview Chat")
            else:
                st.warning("Please type your answer first.")


# ---------------------------
# Vocabulary Builder
# ---------------------------
elif page == "📚 Vocabulary Builder":
    st.title("📚 Interview Vocabulary Builder")
    st.write("Get useful professional words and phrases to sound more confident in interviews.")

    vocab_topic = st.selectbox(
        "Choose a topic",
        ["Describing your skills", "Talking about teamwork", "Talking about projects",
         "Talking about strengths/weaknesses", "Asking questions to the interviewer"]
    )

    if st.button("Get Vocabulary", type="primary"):
        with st.spinner("Fetching useful words and phrases..."):
            prompt = f"""
            You are an English vocabulary coach for interview preparation.
            Topic: "{vocab_topic}"

            Give 6-8 useful professional words/phrases for this topic, suitable
            for a fresher engineering student in an interview. For each one,
            give a one-line example sentence using it. Keep it simple and practical.
            """
            response = model.generate_content(prompt)
            st.success(f"Vocabulary for: {vocab_topic}")
            st.write(response.text)
            log_practice("Vocabulary Builder")


# ---------------------------
# Daily Conversation Practice (NEW)
# ---------------------------
elif page == "💬 Daily Conversation Practice":
    st.title("💬 Daily Conversation Practice")
    st.write(
        "Practice everyday spoken English with AI on topics like friends, "
        "family, meetings, and sports. AI will chat with you naturally and "
        "gently correct your mistakes."
    )

    topic = st.selectbox(
        "Choose a conversation topic",
        ["Talking with Friends", "Family Conversation", "Office Meeting",
         "Sports Discussion", "Travel Plans", "Movies & Entertainment",
         "Weekend Plans", "Current News"]
    )

    # Reset conversation if topic changes
    if "chat_topic" not in st.session_state or st.session_state.chat_topic != topic:
        st.session_state.chat_topic = topic
        st.session_state.chat_history = []

    if st.button("🔄 Start New Conversation", type="primary"):
        with st.spinner("Starting conversation..."):
            prompt = f"""
            You are a friendly English conversation partner helping a Tamil Nadu
            student practice spoken English. Start a natural, casual conversation
            on the topic: "{topic}". Ask one simple, friendly opening question or
            line to begin the chat. Keep it short, like a real conversation starter.
            """
            response = model.generate_content(prompt)
            st.session_state.chat_history = [{"role": "AI", "text": response.text}]

    # Display conversation so far
    for msg in st.session_state.get("chat_history", []):
        if msg["role"] == "AI":
            st.chat_message("assistant").write(msg["text"])
        else:
            st.chat_message("user").write(msg["text"])

    # User reply input
    if st.session_state.get("chat_history"):
        user_reply = st.chat_input("Type your reply here...")

        if user_reply:
            st.session_state.chat_history.append({"role": "user", "text": user_reply})

            with st.spinner("Thinking..."):
                # Build conversation context for the AI
                conversation_so_far = "\n".join(
                    [f"{m['role']}: {m['text']}" for m in st.session_state.chat_history]
                )
                prompt = f"""
                You are a friendly English conversation partner helping a Tamil Nadu
                student practice spoken English on the topic: "{topic}".

                Conversation so far:
                {conversation_so_far}

                Continue the conversation naturally with ONE short reply (like a
                real chat, 1-3 sentences). If the student's last message had a
                grammar mistake, gently mention the correction in brackets at the
                end, like: (Tip: say "I went to the match" instead of "I goed to
                the match"). Keep the tone warm and encouraging.
                """
                response = model.generate_content(prompt)
                st.session_state.chat_history.append({"role": "AI", "text": response.text})

            st.rerun()
    else:
        st.info("👆 Click 'Start New Conversation' to begin practicing this topic.")


# ---------------------------
# Daily Challenge
# ---------------------------
elif page == "🎯 Daily Challenge":
    st.title("🎯 Daily Challenge")
    st.write("A new English challenge every day — a word, a phrase, or a quick grammar question.")

    today_str = str(datetime.date.today())

    if "challenge_date" not in st.session_state or st.session_state.challenge_date != today_str:
        st.session_state.challenge_date = today_str
        st.session_state.challenge_text = None
        st.session_state.challenge_answer_given = False

    if st.session_state.challenge_text is None:
        with st.spinner("Preparing today's challenge..."):
            prompt = f"""
            Create today's English learning challenge for a Tamil Nadu engineering
            student preparing for interviews. Today's date: {today_str}.
            Pick ONE of these types randomly: (a) a new advanced word with meaning
            and example sentence, (b) a useful idiom/phrase with meaning and example,
            or (c) a short grammar fill-in-the-blank question.
            Present it clearly with a title like "Today's Challenge:" followed by
            the content. If it's a question, do NOT give the answer yet.
            """
            response = model.generate_content(prompt)
            st.session_state.challenge_text = response.text

    st.info(st.session_state.challenge_text)

    user_response = st.text_input("Your answer / sentence using this (optional)")

    if st.button("Submit", type="primary"):
        if user_response:
            with st.spinner("Checking..."):
                prompt = f"""
                Today's challenge was: {st.session_state.challenge_text}
                The student's response: "{user_response}"
                Give short, encouraging feedback (2-3 lines) and the correct
                answer/explanation if needed.
                """
                response = model.generate_content(prompt)
                st.success(response.text)
        log_practice("Daily Challenge")
        st.session_state.challenge_answer_given = True


# ---------------------------
# Common Mistakes by Tamil Speakers
# ---------------------------
elif page == "⚠️ Common Mistakes (Tamil Speakers)":
    st.title("⚠️ Common Mistakes Tamil Speakers Make")
    st.write("Learn the most common English mistakes made by Tamil speakers, with corrections.")

    mistake_category = st.selectbox(
        "Choose a category",
        ["Tense mistakes", "Article mistakes (a/an/the)", "Preposition mistakes",
         "Word order mistakes", "Direct translation mistakes from Tamil"]
    )

    if st.button("Show Common Mistakes", type="primary"):
        with st.spinner("Loading examples..."):
            prompt = f"""
            List 5-6 common English mistakes that Tamil speakers typically make
            in the category: "{mistake_category}".
            For each mistake, show:
            - ❌ Incorrect: (the wrong sentence as commonly spoken)
            - ✅ Correct: (the corrected sentence)
            - Why: (one simple line explaining the rule)
            Keep it practical and easy to understand for a student preparing for interviews.
            """
            response = model.generate_content(prompt)
            st.write(response.text)
            log_practice("Common Mistakes")


# ---------------------------
# Grammar Lessons (Topic-based)
# ---------------------------
elif page == "🎓 Grammar Lessons":
    st.title("🎓 Topic-based Grammar Lessons")
    st.write("Structured lessons on key grammar topics, with a quick practice exercise.")

    grammar_topic = st.selectbox(
        "Choose a grammar topic",
        ["Tenses (Past, Present, Future)", "Articles (a, an, the)",
         "Prepositions", "Subject-Verb Agreement", "Active & Passive Voice"]
    )

    if st.button("Start Lesson", type="primary"):
        with st.spinner("Preparing lesson..."):
            prompt = f"""
            Create a short, beginner-friendly grammar lesson on: "{grammar_topic}"
            for a Tamil Nadu engineering student preparing for interviews.

            Structure:
            1. Simple explanation of the rule (3-4 lines, easy English)
            2. 2-3 example sentences
            3. End with 3 practice fill-in-the-blank questions (don't give answers)
            """
            response = model.generate_content(prompt)
            st.session_state.lesson_text = response.text
            st.session_state.lesson_topic = grammar_topic

    if st.session_state.get("lesson_text"):
        st.write(st.session_state.lesson_text)

        st.divider()
        practice_answer = st.text_area("Write your answers to the practice questions here")
        if st.button("Check My Answers", type="primary"):
            if practice_answer:
                with st.spinner("Checking..."):
                    prompt = f"""
                    Lesson topic: {st.session_state.lesson_topic}
                    Lesson content: {st.session_state.lesson_text}
                    Student's answers: "{practice_answer}"

                    Check the answers, mark what's correct/incorrect, and give the
                    right answers with brief explanations. Be encouraging.
                    """
                    response = model.generate_content(prompt)
                    st.success(response.text)
                    log_practice("Grammar Lessons")
            else:
                st.warning("Please write your answers first.")


# ---------------------------
# My Progress
# ---------------------------
elif page == "📊 My Progress":
    st.title("📊 My Progress")

    data = load_progress()

    col1, col2 = st.columns(2)
    with col1:
        st.metric("🔥 Current Streak", f"{data.get('streak', 0)} days")
    with col2:
        st.metric("✅ Total Practice Sessions", data.get("total_practices", 0))

    st.divider()
    st.subheader("Practice Breakdown by Feature")

    by_feature = data.get("by_feature", {})
    if by_feature:
        for feature, count in sorted(by_feature.items(), key=lambda x: -x[1]):
            st.write(f"**{feature}**: {count} times")
            st.progress(min(count / max(by_feature.values()), 1.0))
    else:
        st.info("You haven't practiced yet. Try any feature from the sidebar to start tracking your progress!")

    st.divider()
    if data.get("total_practices", 0) == 0:
        st.write("🚀 Start practicing today to build your streak!")
    elif data.get("streak", 0) >= 3:
        st.success(f"🔥 Amazing! You're on a {data.get('streak')}-day streak. Keep it up!")
    else:
        st.write("👍 Good start! Practice daily to build your streak.")