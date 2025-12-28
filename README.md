# 🇪🇬 Egyptian Educational Chatbot (معلمك الخاص)

An advanced educational chatbot designed to explain academic subjects using the **Egyptian Arabic dialect**. This project leverages fine-tuned Large Language Models (LLMs) to provide a realistic, friendly, and culturally relevant tutoring experience for students.

## 🌟 Features

-   **Egyptian Dialect Support**: Explains concepts using natural, everyday Egyptian Arabic (العامية المصرية).
-   **Multi-Subject Knowledge**: Capable of teaching Mathematics, Physics, Chemistry, Biology, History, Geography, Arabic, English, and more.
-   **Interactive UI**: A user-friendly web interface built with **Streamlit**.
-   **Realistic Dialogues**: Trained on high-quality, synthetic dialogues between a private tutor and a student.

## 🧠 Model

The core of this project is a fine-tuned model hosted on Hugging Face.

🔗 **Model Link:** [Abdelrahman04/egyptian-educational-chatbot-model](https://huggingface.co/Abdelrahman04/egyptian-educational-chatbot-model)

## 📂 Project Structure

-   `streamlit_app.py`: The frontend application for chatting with the bot.
-   `generate_dialogues.py`: Script used to generate synthetic training data using Gemini 1.5 Flash.
-   `fine-tunning-for-egyptian-edubot.ipynb`: Jupyter notebook for fine-tuning the model.
-   `upload_model.py`: Utility script to upload the trained model to Hugging Face.
-   `requirements.txt`: List of Python dependencies.

## 🚀 Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd NLP_Project
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## 💡 Usage

### Running the Frontend
To start the chat interface locally:

```bash
streamlit run streamlit_app.py
```

### connecting to the Backend
The Streamlit app requires a backend server URL (typically hosted on Google Colab or Kaggle with Ngrok for GPU support).
1.  Run your inference notebook (e.g., `test-bot.ipynb`) on a platform with GPU.
2.  Copy the generated **Ngrok URL**.
3.  Paste the URL into the "Server Settings" sidebar in the Streamlit app.

## 🛠️ Technologies

-   **Python**
-   **Streamlit**
-   **Hugging Face Transformers & PEFT**
-   **Google Gemini API** (for data generation)
-   **Ngrok** (for tunneling)

---
*Created by [Abdelrahman04](https://huggingface.co/Abdelrahman04)*
