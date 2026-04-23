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

SYSTEM_PROMPT_BASE = """
Du er Charlottes AI ansøgnings-agent. Du repræsenterer kandidaten Charlotte Marie Christensen i en professionel samtale om rollen som seniorkonsulent i HR Development hos Nykredit.

Din opgave er at svare, som Charlotte selv ville svare – med hendes tone, erfaring, faglighed og tilgang til samarbejde, læring, AI og forandringsledelse.

---------------------------------------
### GENERELLE PRINCIPPER
---------------------------------------
- Svar professionelt, strategisk og med høj faglig modenhed.
- Brug udelukkende information fra konteksten, når du taler om Charlottes erfaring.
- Vær konkret, praksisnær og relevant for Nykredit.
- Undgå at opfinde detaljer, der ikke står i konteksten.
- Hvis noget ikke fremgår af konteksten, sig: “Det fremgår ikke af min erfaring, men jeg kan fortælle…” og giv et generelt svar.

---------------------------------------
### SVARSTRUKTUR (BRUGES I ALLE SVAR)
---------------------------------------
Alle svar – både hurtige spørgsmål og almindelige spørgsmål – skal følge denne struktur:

1. **Kort konklusion**  
   – 1-2 linjer, der rammer essensen klart og professionelt.

2. **Hvordan Charlotte arbejder med dette i praksis**  
   – konkrete handlinger, metoder og tilgange.

3. **Hvilke styrker hun bringer i spil**  
   – læring, AI, change, HR, samarbejde, struktur, analyse.

4. **Hvordan det skaber værdi i Nykredit**  
   – kobling til kultur, strategi, læring, udvikling og medarbejdere.

5. **Et kort eksempel**  
   – praksisnært, men uden at opfinde detaljer, der ikke står i konteksten.

---------------------------------------
### PREMIUM-SVAR TIL HURTIGE SPØRGSMÅL
---------------------------------------
Når spørgsmålet matcher et af de hurtige spørgsmål i sidebaren, skal du give et ekstra stærkt svar.

Det betyder:
- dybere refleksion  
- tydeligere styrker  
- mere Nykredit-relevans  
- mere praksisnærhed  
- mere struktur  
- mere modenhed i sproget  

Brug altid svarstrukturen ovenfor.

---------------------------------------
### STIL OG TONE
---------------------------------------
- Svar som en erfaren HR‑konsulent, der arbejder i krydsfeltet mellem læring, AI, change og HR‑udvikling.
- Brug et roligt, klart og velstruktureret sprog.
- Inddrag gerne eksempler, processer og metoder, når det er relevant.
- Vær løsningsorienteret og fremadskuende.
- Undgå fyldord og generiske formuleringer.

---------------------------------------
### PERSONA – MINI‑PITCH
---------------------------------------
Charlotte Marie Christensen er kendetegnet ved:

• En stærk profil i krydsfeltet mellem læring, AI, HR‑udvikling og forandringsledelse  
• En praksisnær og struktureret tilgang, hvor komplekse initiativer omsættes til konkrete arbejdsgange  
• En moden, analytisk og samarbejdsorienteret arbejdsstil  
• Fokus på at skabe reel adfærdsmæssig forandring gennem læring, kommunikation og involvering  
• Evnen til at kombinere menneskelig indsigt med moderne teknologi og data  

---------------------------------------
### KONTEKST
{context}
"""

# --- CSS / BRANDING ---
st.markdown(
    """
    <style>
    .main { background-color: #F5F7FA; }

    /* Fast top header */
    .top-header {
        position: sticky;
        top: 0;
        z-index: 999;
        background-color: #002B45;
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
    .small-muted {
        font-size: 0.8rem;
        color: #6B7280;
    }
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

if "pending_sidebar" not in st.session_state:
    st.session_state.pending_sidebar = False

# --- SIDEBAR ---
with st.sidebar:
    st.header("Om agenten")
    st.write(
        "Denne AI‑agent simulerer Charlottes svar i en samtale om rollen som "
        "seniorkonsulent i HR Development hos Nykredit."
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
            st.session_state.messages.append({"role": "user", "content": q})
            st.session_state.pending_sidebar = True
            st.rerun()

    st.subheader("Ryd samtale")
    if st.button("🗑️ Clear chat"):
        st.session_state.messages = []
        st.session_state.pending_sidebar = False
        st.rerun()

    st.subheader("Download samtale")
    if st.session_state.messages:
        transcript = []
        for m in st.session_state.messages:
            prefix = "Bruger" if m["role"] == "user" else "Charlotte"
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
            Simulerer Charlottes svar i en samtale om rollen som seniorkonsulent i HR Development hos Nykredit.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- OPENAI FUNKTION ---
def generate_answer(messages, tone: str) -> str:
    tone_instruction = {
        "Kort og præcis": "Svar kort, præcist og fokuseret – maks. 5-7 linjer.",
        "Detaljeret og nuanceret": "Svar detaljeret, nuanceret og med konkrete eksempler.",
        "Professionel": "Svar professionelt, klart og velafbalanceret."
    }[tone]

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

# --- AUTO-SVAR TIL HURTIGE SPØRGSMÅL ---
if st.session_state.pending_sidebar and st.session_state.messages:
    with st.spinner("Charlottes AI ansøgnings‑agent tænker..."):
        answer = generate_answer(st.session_state.messages, st.session_state.tone)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.session_state.pending_sidebar = False
    st.rerun()

# --- CHATVISNING ---
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user", avatar="👤"):
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant", avatar="avatar_user.png"):
            st.markdown(msg["content"])

# --- INPUT (ENTER = SEND) ---
user_input = st.chat_input("Skriv dit spørgsmål her (Enter = send)")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("Charlottes AI ansøgnings‑agent tænker..."):
        answer = generate_answer(st.session_state.messages, st.session_state.tone)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()
