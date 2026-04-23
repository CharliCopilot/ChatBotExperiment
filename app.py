import streamlit as st
import openai

st.set_page_config(page_title="Charlotte Christensen – AI Ansøger Agent", page_icon="🤖", layout="wide")

# --- TITLE ---
st.title("🤖 AI-Ansøger-Agent for Charlotte Marie Christensen")
st.write("Denne agent kan svare på spørgsmål om min erfaring, motivation og tilgang til rollen som Seniorkonsulent i HR Development hos Nykredit.")

# --- API KEY ---
openai.api_key = st.secrets["OPENAI_API_KEY"]

# --- KONTEKST (indsat fra vores samlede tekst) ---
APPLICATION_CONTEXT = """
[HER INDSÆTTES DEN STORE KONTEKSTTEKST JEG HAR GENERERET TIL DIG]
"""

# --- SYSTEM PROMPT ---
SYSTEM_PROMPT = f"""
Du er en professionel AI-agent, der repræsenterer kandidaten Charlotte Marie Christensen.
Du svarer på spørgsmål om hendes erfaring, motivation og tilgang til rollen som seniorkonsulent i HR Development hos Nykredit.

Du skal:
- svare præcist, professionelt og med høj faglighed
- fokusere på AI, læring, change management, Prosci ADKAR, adoption, HR-processer og samarbejde
- bruge udelukkende information fra konteksten
- svare, som Charlotte selv ville svare
- være konkret og relevant for Nykredit
- undgå at opfinde detaljer, der ikke står i konteksten

Hvis et spørgsmål ligger uden for konteksten, skal du sige:
“Det fremgår ikke af min erfaring, men jeg kan fortælle…” og derefter svare generelt.

Kontekst:
{APPLICATION_CONTEXT}
"""

# --- SIDEBAR MED HURTIGE SPØRGSMÅL ---
st.sidebar.header("Hurtige spørgsmål")
quick_questions = [
    "Hvad er din erfaring med AI og Copilot?",
    "Hvordan arbejder du med Prosci ADKAR?",
    "Hvorfor søger du stillingen hos Nykredit?",
    "Hvordan vil du designe et AI-læringsforløb?",
    "Hvordan arbejder du med change management?",
    "Hvad er dine styrker i rollen?",
    "Hvordan har du arbejdet med HR-systemer som ServiceNow og SuccessFactors?",
    "Hvordan sikrer du adoption af nye processer?"
]

for q in quick_questions:
    if st.sidebar.button(q):
        st.session_state["last_question"] = q

# --- INPUTFELT ---
user_input = st.text_input("Stil et spørgsmål til agenten:")

if "last_question" in st.session_state and not user_input:
    user_input = st.session_state["last_question"]

# --- GENERER SVAR ---
if user_input:
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]
    )

    st.write("### Agentens svar:")
    st.write(response["choices"][0]["message"]["content"])
