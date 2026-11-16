import streamlit as st
import ollama

# ==========================================
# 1. CONFIGURATION DE LA PAGE & DESIGN
# ==========================================
st.set_page_config(
    page_title="PJE 17 - Usine-Ecole 4.0",
    layout="wide"
)

# ==========================================
# 2. MODULE CONNEXION LLM (Isole pour modularite)
# ==========================================
def query_local_llm(prompt: str, model_name: str, system_prompt: str = "") -> str:
    """
    Envoie le prompt au LLM local via Ollama.
    Cette fonction est conçue pour être remplacée plus tard par l'appel à l'Orchestrateur LangGraph.
    """
    try:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})

        response = ollama.chat(
            model=model_name,
            messages=messages
        )
        return response['message']['content']
    except Exception as e:
        return f"Erreur de communication avec Ollama : {e}. Assure-toi que le service tourne en local."

# ==========================================
# 3. INTERFACE UTILISATEUR (UI) - STREAMLIT
# ==========================================
st.title("PJE 17 — Plateforme IA Agentique (PoC Interface)")
st.markdown("*Assistant d'aide au pilotage pour l'usine-école 4.0 (Point d'entrée unique)*")

# Barre latérale pour la configuration modulaire du PoC
with st.sidebar:
    st.header("Paramètres du PoC")
    
    # Choix du modèle local
    selected_model = st.selectbox(
        "Modèle Ollama (Open Weights)",
        ["llama3.2:3b"],
        index=0
    )
    
    st.divider()
    
    # Zone pour tester des prompts système prédéfinis
    st.subheader("Scénarios de Test / Prompts")
    prompt_mode = st.radio(
        "Mode d'interaction :",
        ["Libre (Chat direct)", "Simulateur d'Agent Diagnostique", "Simulateur d'Agent Actions Correctives"]
    )
    
    if prompt_mode == "Simulateur d'Agent Diagnostique":
        system_prompt = "Tu es l'Agent Diagnostique de l'usine-école 4.0. Tu analyses les pannes à partir des données capteurs."
        st.info("Mode Agent actif : Le LLM adoptera une posture de diagnostic technique.")
    elif prompt_mode == "Simulateur d'Agent Actions Correctives":
        system_prompt = "Tu es l'Agent Actions Correctives. Tu proposes des procédures Lean et tu cites tes sources."
        st.info("Mode Agent actif : Le LLM fournira des plans d'action sourcés.")
    else:
        system_prompt = "Tu es l'assistant général de l'usine-école 4.0."
        st.info("Mode Chat standard.")

    if st.button("Réinitialiser la conversation"):
        st.session_state.messages = []
        st.rerun()

# Initialisation de l'historique de conversation
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage des messages de l'historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrée utilisateur (Point d'entrée unique conversationnel)
if user_input := st.chat_input("Posez votre question sur l'état d'un poste ou une anomalie..."):
    
    # Enregistrement et affichage du message utilisateur
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Génération de la réponse via le module LLM isolé
    with st.chat_message("assistant"):
        with st.spinner("L'orchestrateur analyse votre demande..."):
            
            bot_response = query_local_llm(
                prompt=user_input, 
                model_name=selected_model, 
                system_prompt=system_prompt
            )
            
            st.markdown(bot_response)
            
            st.session_state.messages.append({"role": "assistant", "content": bot_response})