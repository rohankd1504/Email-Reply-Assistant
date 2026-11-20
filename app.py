
import streamlit as st
import ollama
import json
import html

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="MailMate - AI Email Reply Assistant",
    page_icon="✦",
    layout="wide"
)

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(120deg, #f7f5ff, #f5f8ff);
}

.block-container {
    max-width: 1250px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

footer {
    visibility: hidden;
}

.mailmate-header {
    display: flex;
    align-items: center;
    padding: 12px 0 20px;
    margin-bottom: 25px;
}

.mailmate-logo {
    font-size: 28px;
    font-weight: 800;
    color: #29234f;
    letter-spacing: -1px;
}

.brand-highlight {
    color: #8062ed;
}

.hero {
    text-align: center;
    padding: 25px 10px 55px;
}

.hero h1 {
    color: #29234f;
    font-size: 42px;
    font-weight: 850;
    line-height: 1.2;
    letter-spacing: -1.5px;
}

.hero p {
    color: #77758f;
    font-size: 16px;
}

.section-label {
    color: #7056df;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 2px;
    margin-bottom: 18px;
}

.input-heading {
    color: #292929;
    font-size: 27px;
    font-weight: 750;
    margin-bottom: 12px;
}

/* Email input */
.stTextArea textarea {
    background: #ffffff !important;
    border: 1px solid #c9c1e5 !important;
    border-radius: 12px !important;
    font-size: 16px !important;
    padding: 16px !important;
    color: #29234f !important;
    line-height: 1.7 !important;
}

/* Email placeholder */
.stTextArea textarea::placeholder {
    color: #77718f !important;
    opacity: 1 !important;
}

.stButton button {
    min-height: 48px;
    border-radius: 11px;
    font-weight: 650;
    transition: all 0.2s ease;
}

.stButton button[kind="primary"] {
    background: linear-gradient(90deg, #7960ef, #a064ed);
    border: none;
    color: white;
}

.stButton button:hover {
    border-color: #8062ed;
    transform: translateY(-1px);
}

/* Helper text */
.helper-text {
    color: #51496f !important;
    font-size: 15px;
    font-weight: 600;
    margin-top: 10px;
}

.mailmate-footer {
    text-align: center;
    color: #89869d;
    font-size: 13px;
    padding-top: 35px;
    margin-top: 45px;
    border-top: 1px solid #e4e0ee;
}

@media (max-width: 650px) {
    .hero h1 {
        font-size: 32px;
    }

    .mailmate-logo {
        font-size: 24px;
    }
}

/* AI generating message */
[data-testid="stSpinner"] {
    color: #49358e !important;
}

[data-testid="stSpinner"] p {
    color: #49358e !important;
    font-size: 16px !important;
    font-weight: 650 !important;
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# SESSION STATE
# ==========================================

if "replies" not in st.session_state:
    st.session_state.replies = None

if "email_input" not in st.session_state:
    st.session_state.email_input = ""


# ==========================================
# CLEAR FUNCTION
# ==========================================

def clear_form():
    st.session_state.email_input = ""
    st.session_state.replies = None


# ==========================================
# OLLAMA AI FUNCTION
# ==========================================

def generate_replies(email_text):

    prompt = f"""
You are MailMate, an intelligent professional email
reply assistant.

Read the complete received email carefully.

RECEIVED EMAIL:
{email_text}

Generate exactly THREE different email replies.

1. FORMAL:
Professional, respectful and suitable for official
or workplace communication.

2. FRIENDLY:
Warm, natural and conversational.

3. SHORT:
Brief, clear and direct.

IMPORTANT RULES:

- Understand the complete context.
- Do not invent facts, dates or commitments.
- Do not assume a request has been accepted.
- Do not change the meaning of the original email.
- Use correct English grammar.
- Avoid unnecessary explanations.
- Return valid JSON only.

Use exactly this structure:

{{
    "formal": "Formal reply here",
    "friendly": "Friendly reply here",
    "short": "Short reply here"
}}
"""

    response = ollama.chat(
        model="llama3:latest",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        format="json",
        options={
            "temperature": 0.3
        }
    )

    result = json.loads(
        response["message"]["content"]
    )

    replies = {
        "Formal": result["formal"],
        "Friendly": result["friendly"],
        "Short": result["short"]
    }

    for style, reply in replies.items():

        if not isinstance(reply, str) or not reply.strip():
            raise ValueError(
                f"The {style} reply is empty or invalid."
            )

    return replies


# ==========================================
# HEADER
# ==========================================

st.markdown("""
<div class="mailmate-header">
    <div class="mailmate-logo">
        ✦ Mail<span class="brand-highlight">Mate</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ==========================================
# HERO SECTION
# ==========================================

st.markdown("""
<div class="hero">
    <h1>Write better emails,<br>in less time.</h1>
    <p>
        Your local AI-powered email assistant.
        Generate three different replies in seconds.
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()


# ==========================================
# EMAIL INPUT SECTION
# ==========================================

st.markdown("""
<div class="section-label">
    01 &nbsp; YOUR RECEIVED EMAIL
</div>

<div class="input-heading">
    Paste your email
</div>
""", unsafe_allow_html=True)

email_text = st.text_area(
    "Received email",
    height=180,
    placeholder="Paste your complete received email here...",
    label_visibility="collapsed",
    key="email_input"
)

st.markdown("""
<div class="helper-text">
    ✦ Paste the complete email to get context-aware replies.
</div>
""", unsafe_allow_html=True)


# ==========================================
# ACTION BUTTONS
# ==========================================

generate_col, clear_col = st.columns([3, 1])

with generate_col:

    generate_clicked = st.button(
        "✦ Generate Three Replies",
        type="primary",
        use_container_width=True
    )

with clear_col:

    st.button(
        "Clear",
        on_click=clear_form,
        use_container_width=True
    )


# ==========================================
# GENERATE REPLIES
# ==========================================

if generate_clicked:

    if not email_text.strip():

        st.warning("Please paste an email first.")

    else:

        try:

            with st.spinner(
                "✦ MailMate is generating your three replies..."
            ):

                st.session_state.replies = None

                generated = generate_replies(email_text)

                st.session_state.replies = generated

        except json.JSONDecodeError:

            st.error(
                "The AI returned an invalid response. "
                "Please try generating again."
            )

        except Exception as error:

            st.error(
                f"Unable to generate replies: {error}"
            )


# ==========================================
# DISPLAY RESULTS - THREE CARDS
# ==========================================

if st.session_state.replies:

    st.markdown("---")

    st.markdown("""
    <div class="section-label">
        02 &nbsp; YOUR GENERATED REPLIES
    </div>

    <p style="color:#858197; font-size:16px;">
        Compare the three writing styles and choose
        the reply that best suits your email.
    </p>
    """, unsafe_allow_html=True)

    replies = st.session_state.replies

    formal = html.escape(replies["Formal"])
    friendly = html.escape(replies["Friendly"])
    short = html.escape(replies["Short"])

    formal_js = json.dumps(replies["Formal"])
    friendly_js = json.dumps(replies["Friendly"])
    short_js = json.dumps(replies["Short"])

    st.components.v1.html(
        f"""
        <!DOCTYPE html>
        <html>
        <head>

        <meta name="viewport"
              content="width=device-width, initial-scale=1.0">

        <style>

        * {{
            box-sizing: border-box;
        }}

        body {{
            margin: 0;
            padding: 8px 0 15px;
            font-family: -apple-system, BlinkMacSystemFont,
                         "Segoe UI", sans-serif;
            color: #393747;
            background: transparent;
        }}

        .cards {{
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 18px;
            align-items: stretch;
        }}

        .card {{
            background: #ffffff;
            border: 1px solid #e5defb;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 4px 14px rgba(65,45,120,0.05);
            display: flex;
            flex-direction: column;
            min-width: 0;
        }}

        .number {{
            display: inline-block;
            background: #f0ebff;
            color: #7056df;
            padding: 6px 11px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 800;
            align-self: flex-start;
        }}

        h3 {{
            color: #49358e;
            font-size: 19px;
            margin: 17px 0 7px;
        }}

        .description {{
            color: #89869d;
            font-size: 13px;
            margin-bottom: 16px;
        }}

        .reply {{
            color: #393747;
            font-size: 14px;
            line-height: 1.8;
            white-space: pre-wrap;
            overflow-wrap: anywhere;
            word-break: normal;
            flex: 1;
            padding-bottom: 20px;
        }}

        .copy-btn {{
            width: 100%;
            padding: 12px;
            border: 1px solid #8062ed;
            border-radius: 9px;
            background: white;
            color: #7056df;
            font-size: 14px;
            font-weight: 700;
            cursor: pointer;
            transition: 0.2s;
        }}

        .copy-btn:hover {{
            background: #8062ed;
            color: white;
        }}

        .copy-status {{
            min-height: 19px;
            margin-top: 8px;
            text-align: center;
            color: #16845b;
            font-size: 12px;
        }}

        @media (max-width: 700px) {{
            .cards {{
                grid-template-columns: 1fr;
            }}
        }}

        </style>
        </head>

        <body>

        <div class="cards">

            <div class="card">
                <span class="number">REPLY 01</span>
                <h3>✦ Formal Reply</h3>

                <div class="description">
                    Professional and polite
                </div>

                <div class="reply">{formal}</div>

                <button class="copy-btn"
                    onclick='copyReply({formal_js}, "status1")'>
                    Copy Formal Reply
                </button>

                <div class="copy-status" id="status1"></div>
            </div>

            <div class="card">
                <span class="number">REPLY 02</span>
                <h3>✦ Friendly Reply</h3>

                <div class="description">
                    Warm and conversational
                </div>

                <div class="reply">{friendly}</div>

                <button class="copy-btn"
                    onclick='copyReply({friendly_js}, "status2")'>
                    Copy Friendly Reply
                </button>

                <div class="copy-status" id="status2"></div>
            </div>

            <div class="card">
                <span class="number">REPLY 03</span>
                <h3>✦ Short Reply</h3>

                <div class="description">
                    Brief and direct
                </div>

                <div class="reply">{short}</div>

                <button class="copy-btn"
                    onclick='copyReply({short_js}, "status3")'>
                    Copy Short Reply
                </button>

                <div class="copy-status" id="status3"></div>
            </div>

        </div>

        <script>

        function copyReply(text, statusId) {{

            const status = document.getElementById(statusId);

            const textarea = document.createElement("textarea");
            textarea.value = text;

            textarea.style.position = "fixed";
            textarea.style.left = "-9999px";
            textarea.style.top = "0";
            textarea.style.opacity = "0";

            document.body.appendChild(textarea);

            textarea.focus();
            textarea.select();
            textarea.setSelectionRange(0, textarea.value.length);

            try {{

                const successful = document.execCommand("copy");

                if (successful) {{
                    status.innerText = "✓ Copied to clipboard!";
                }} else {{
                    status.innerText = "Copy failed. Please copy manually.";
                }}

            }} catch (error) {{

                status.innerText = "Copy failed. Please copy manually.";

            }}

            document.body.removeChild(textarea);
        }}

        </script>

        </body>
        </html>
        """,
        height=650,
        scrolling=True
    )


# ==========================================
# FOOTER
# ==========================================

st.markdown("""
<div class="mailmate-footer">
    ✦ MailMate — Your AI-powered email writing assistant
    <br><br>
    Built with Python, Streamlit and Ollama
    <br>
    Powered by Llama 3 running locally
</div>
""", unsafe_allow_html=True)
