# 🎯 InterviewEnglish AI

An AI-powered web app that helps engineering and college students practice spoken and written English for job interviews — built using Python, Streamlit, and Google Gemini API.

🔗 **Live App:** [interview-english-ai-yb3sdvslhs5tic2kzf4x28.streamlit.app](https://interview-english-ai-yb3sdvslhs5tic2kzf4x28.streamlit.app)

---

## 📌 About the Project

Many engineering and college students in Tamil Nadu struggle with spoken English during job interviews, even when they have strong technical skills. **InterviewEnglish AI** was built to bridge that gap — giving students an AI conversation partner to practice with, anytime, for free.

This project was built as a self-taught, hands-on learning exercise in AI application development, from idea to live deployment.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📝 **Self-Introduction Builder** | Generates a confident, natural self-introduction based on your details |
| ✅ **Grammar Check** | Instantly checks any sentence for grammar mistakes with explanations |
| 🎤 **Mock Interview Chat** | AI asks common interview questions and gives feedback on your answers |
| 📚 **Vocabulary Builder** | Professional words and phrases for interview topics |
| 💬 **Daily Conversation Practice** | Casual AI chat practice on topics like friends, family, meetings, and sports |
| 🎯 **Daily Challenge** | A new word, idiom, or grammar question every day |
| ⚠️ **Common Mistakes (Tamil Speakers)** | Common English mistakes Tamil speakers make, with corrections |
| 🎓 **Grammar Lessons** | Structured lessons on Tenses, Articles, Prepositions, and more |
| 📊 **Progress Tracker** | Tracks practice streaks and session history |

---

## 🛠️ Tech Stack

- **Frontend & App Framework:** Streamlit
- **AI Model:** Google Gemini API (`gemini-2.5-flash`)
- **Language:** Python
- **Data Storage:** JSON (local progress tracking)
- **Deployment:** Streamlit Community Cloud

---

## 🚀 Getting Started (Run Locally)

```bash
# Clone the repository
git clone https://github.com/prathushamuralie-bot/interview-english-ai.git
cd interview-english-ai

# Create a virtual environment
python -m venv venv
venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Add your Gemini API key in a .env file
echo GEMINI_API_KEY=your_key_here > .env

# Run the app
streamlit run app.py
```

---

## 📖 What I Learned

- Building and structuring a multi-page AI application with Streamlit
- Integrating and prompt-engineering with the Google Gemini API
- Managing local state and session data for interactive features
- Debugging real-world deployment issues (firewall, virtual environments, dependency management)
- Deploying a Python app to the cloud and managing secrets/environment variables

---

## 👩‍💻 About Me

Built by **Prathusha Muralie (Jee)** — B.Tech Information Science and Engineering student, passionate about AI/ML and software engineering.

- 🔗 [LinkedIn](https://linkedin.com/in/prathusha-muralie-15137b372)
- 💻 [Portfolio](https://prathushamuralie-bot.github.io)
- 📧 prathusha524@gmail.com

---

## 🔮 Future Improvements

- User accounts and login system
- Premium features with payment integration
- Pronunciation practice using speech input
- Mobile app version using Flutter