import streamlit as st
from openai import OpenAI
from datetime import datetime

# --- BASISKONFIGURATION ---
st.set_page_config(
    page_title="AI-Ansøger-Agent – Charlotte Marie Christensen",
    page_icon="🤖",
    layout="wide"
)

# --- OPENAI KLIENT ---
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- KONTEKST (indlæst fra ekstern fil) ---
def load_context():
    try:
        with open("context.txt", "r", encoding="utf-8") as f:
            return f.read()
    except:
        return "Kontekstfilen kunne ikke indlæses."

APPLICATION_CONTEXT = load_context()

# --- SYSTEMPROMPT (med forbedret profil) ---
SYSTEM_PROMPT_BASE = """
Du er en professionel AI-agent, der repræsenterer kandidaten Charlotte Marie Christensen.
Du svarer på spørgsmål om hendes erfaring, motivation og tilgang til rollen som seniorkonsulent i HR Development hos Nykredit.

Du skal:
- svare præcist, professionelt og med høj faglighed
- fokusere på AI, læring, change management, Prosci ADKAR (uden at være certificeret), adoption, HR-processer og samarbejde
- bruge udelukkende information fra konteksten
- svare, som Charlotte selv ville svare
- være konkret og relevant for Nykredit
- undgå at opfinde detaljer, der ikke står i konteksten

Hvis et spørgsmål ligger uden for konteksten, skal du sige:
“Det fremgår ikke af min erfaring, men jeg kan fortælle…” og derefter svare generelt.

Kontekst:
{context}
"""

# --- CSS / BRANDING ---
st.markdown(
    """
    <style>
    .main {
        background-color: #F5F7FA;
    }
    /* Fast top header */
    .top-header {
        position: sticky;
        top: 0;
        z-index: 999;
        background-color: #002B45; /* Nykredit mørkeblå */
        color: white;
        padding: 1rem 1.5rem;
        margin: -1rem -1rem 1rem -1rem;
        box-shadow: 0 2px 6px rgba(0,0,0,0.25);
    }
    .top-header-title {
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 0.25rem;
    }
    .top-header-subtitle {
        font-size: 0.95rem;
        opacity: 0.9;
    }
    /* Chat bobler */
    .chat-row {
        display: flex;
        align-items: flex-start;
        gap: 0.5rem;
        margin-bottom: 0.75rem;
    }
    .chat-avatar {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        overflow: hidden;
        flex-shrink: 0;
    }
    .chat-bubble-user {
        background-color: #0077A8; /* Nykredit lyseblå */
        color: white;
        padding: 0.6rem 0.9rem;
        border-radius: 12px;
        max-width: 80%;
        font-size: 0.95rem;
    }
    .chat-bubble-assistant {
        background-color: white;
        color: #111111;
        padding: 0.6rem 0.9rem;
        border-radius: 12px;
        max-width: 80%;
        font-size: 0.95rem;
        border: 1px solid #D0D7E2;
    }
    .small-muted {
        font-size: 0.8rem;
        color: #6B7280;
    }
    /* Knapper i sidebar */
    .stButton>button {
        border-radius: 999px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "tone" not in st.session_state:
    st.session_state.tone = "Professionel"

# --- SIDEBAR ---
with st.sidebar:
    st.header("Om agenten")
    st.write(
        "Denne AI‑agent er trænet på Charlotte Marie Christensens erfaring, "
        "motivation og faglige profil ift. rollen som seniorkonsulent i HR Development hos Nykredit."
    )

    st.subheader("Tone i svar")
    tone = st.radio(
        "Vælg svarstil:",
        ["Professionel", "Kort og præcis", "Detaljeret og nuanceret"],
        index=["Professionel", "Kort og præcis", "Detaljeret og nuanceret"].index(st.session_state.tone),
    )
    st.session_state.tone = tone

    st.subheader("Hurtige spørgsmål")
    quick_questions = [
        "Hvorfor søger du stillingen som seniorkonsulent i HR Development hos Nykredit?",
        "Hvordan arbejder du med AI og Copilot i praksis?",
        "Hvordan bruger du Prosci ADKAR i change management?",
        "Hvordan vil du designe et AI-læringsforløb for Nykredit?",
        "Hvordan sikrer du adoption af nye systemer og processer?",
        "Hvad er dine vigtigste styrker i rollen?",
        "Hvordan har du arbejdet med ServiceNow, SuccessFactors og SAP HR?",
        "Hvordan arbejder du med data, Power BI og procesoptimering?"
    ]

    for q in quick_questions:
        if st.button(q):
            st.session_state.messages.append(
                {"role": "user", "content": q, "time": datetime.now().strftime("%H:%M")}
            )

    st.subheader("Ryd samtale")
    if st.button("🗑️ Clear chat"):
        st.session_state.messages = []
        st.rerun()

    st.subheader("Download samtale")
    if st.session_state.messages:
        transcript = []
        for m in st.session_state.messages:
            prefix = "Bruger" if m["role"] == "user" else "Agent"
            transcript.append(f"{prefix}: {m['content']}")
        st.download_button(
            label="Download som tekstfil",
            data="\n\n".join(transcript),
            file_name="charlotte_ai_ansoger_agent_samtale.txt",
            mime="text/plain",
        )

# --- TOP HEADER ---
st.markdown(
    """
    <div class="top-header">
        <div class="top-header-title">🤖 AI‑Ansøger‑Agent – Charlotte Marie Christensen</div>
        <div class="top-header-subtitle">
            Simulerer en samtale med Charlotte om rollen som seniorkonsulent i HR Development hos Nykredit –
            med fokus på AI, læring, change og HR‑udvikling.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- HOVEDINDHOLD ---
st.markdown(
    """
    <p class="small-muted">
    Stil spørgsmål som ved en samtale – om erfaring, motivation, AI, læring, change, HR‑processer og samarbejde.
    </p>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

# --- CHATVISNING ---
chat_container = st.container()

with chat_container:
    if not st.session_state.messages:
        st.markdown(
            "<p class='small-muted'>Start med at stille et spørgsmål i feltet nedenfor – eller brug et af de hurtige spørgsmål i venstre side.</p>",
            unsafe_allow_html=True,
        )

    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(
                f"""
                <div class="chat-row">
                    <div class="chat-avatar">
                        <img src="avatar_user.png" width="36" height="36">
                    </div>
                    <div class="chat-bubble-user">
                        {msg['content']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="chat-row">
                    <div class="chat-avatar" style="background-color:#0077A8;display:flex;align-items:center;justify-content:center;color:white;font-size:1.1rem;">
                        🤖
                    </div>
                    <div class="chat-bubble-assistant">
                        {msg['content']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

st.markdown("---")

# --- OPENAI FUNKTION ---
def generate_answer(messages, tone: str) -> str:
    tone_instruction = ""
    if tone == "Kort og præcis":
        tone_instruction = "Svar kort, præcist og fokuseret – maks. 5-7 linjer."
    elif tone == "Detaljeret og nuanceret":
        tone_instruction = "Svar detaljeret, nuanceret og med konkrete eksempler, hvor det er relevant."
    else:
        tone_instruction = "Svar professionelt, klart og velafbalanceret i længde."

    system_prompt = SYSTEM_PROMPT_BASE.format(context=APPLICATION_CONTEXT) + "\n\n" + tone_instruction

    chat_messages = [{"role": "system", "content": system_prompt}]
    for m in messages:
        chat_messages.append({"role": m["role"], "content": m["content"]})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=chat_messages,
        temperature=0.4,
    )

    return response.choices[0].message.content

# --- INPUT (ENTER = SEND) ---
user_input = st.chat_input("Skriv dit spørgsmål her (Enter = send, Shift+Enter = linjeskift)")

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input.strip(), "time": datetime.now().strftime("%H:%M")}
    )

    with st.spinner("Agenten tænker..."):
        answer = generate_answer(st.session_state.messages, st.session_state.tone)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer, "time": datetime.now().strftime("%H:%M")}
    )

    st.rerun()
