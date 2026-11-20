
# MailMate - AI Email Reply Assistant

MailMate is an AI-powered email reply assistant that generates three different reply styles from a received email.

## Features

- Formal Reply – Professional and polite.
- Friendly Reply – Warm and conversational.
- Short Reply – Brief and direct.
- Simple Streamlit user interface.
- Local AI generation using Ollama and Llama 3.

## Technologies Used

- Python
- Streamlit
- Ollama
- Llama 3

## Installation and Setup

1. Clone the repository:

```bash
git clone https://github.com/rohankd1504/Email-Reply-Assistant.git
cd Email-Reply-Assistant
```

2. Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Download the AI model:

```bash
ollama pull llama3
```

5. Run MailMate:

```bash
streamlit run app.py
```

## How to Use

1. Open MailMate in your browser.
2. Paste a received email.
3. Click Generate Three Replies.
4. Compare the Formal, Friendly and Short replies.
5. Copy your preferred reply.

## Author

- **Name:** Rohan Dagade
- **Roll Number:** 06 (ADT23SOCB0864)
- **Department:** Computer Science and Engineering
- **Institution:** MIT ADT University, Pune

## Repository

https://github.com/rohankd1504/Email-Reply-Assistant
