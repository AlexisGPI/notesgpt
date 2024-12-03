import streamlit as st
from datetime import datetime, time, timedelta
import openai

# Clé API OpenAI (remplace par ta clé ou configure via une variable d'environnement)
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# Configuration de l'API OpenAI
openai.api_key = OPENAI_API_KEY

def format_notes_with_chatgpt(notes):
    """
    Fonction pour appeler l'API ChatGPT et reformater les notes.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Tu es un assistant qui formate des notes de réunion."},
                {"role": "user", "content": f"Remet en forme les notes de ma réunion : {notes}"}
            ],
            max_tokens=500
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Une erreur est survenue : {e}"

# CSS personnalisé pour styliser la sidebar et le contenu
st.markdown(
    """
    <style>
    .sidebar {
        background-color: #f8f9fa;
        padding: 10px;
        border-right: 2px solid #dedede;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Création d'onglets dans la barre latérale
st.sidebar.title("Navigation")
tabs = ["📌 Informations", "📝 Notes", "📂 Documents", "📅 Prochaine réunion"]
active_tab = st.sidebar.radio("Choisissez un onglet", tabs)

# Instructions dans la barre latérale après les onglets
st.sidebar.markdown(
    """
    <div class="sidebar">
        <h3>📝 Comment utiliser l'application</h3>
        <ul>
            <li>Entrez les informations générales dans l'onglet Informations.</li>
            <li>Ajoutez vos notes dans l'onglet Notes.</li>
            <li>Ajoutez les fichiers dans Documents.</li>
            <li>Planifiez la prochaine réunion dans Prochaine réunion.</li>
            <li>Enregistrez le tout avec le bouton en bas.</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True,
)

# Affichage des onglets actifs
if active_tab == "📌 Informations":
    st.header("📌 Informations")
    meeting_title = st.text_input("Titre de la réunion", placeholder="Exemple : Réunion de stratégie marketing")
    
    # Date et heure par défaut (10h00 pour l'heure)
    meeting_date = st.date_input("Date de la réunion :", value=datetime.today(), key="meeting_date", format="DD/MM/YYYY") 
    meeting_time = st.time_input("Heure de la réunion :", value=time(10, 0), key="meeting_time", step=1800)
    
    participants = st.text_area(
        "Participants", 
        placeholder="Exemple : Alexis, Claire, Marc...", 
        height=100
    )

elif active_tab == "📝 Notes":
    st.header("📝 Prise de notes")
    meeting_notes = st.text_area(
        "Notes de la réunion", 
        placeholder="Exemple : Discussions sur les objectifs, décisions prises, etc.",
        height=300
    )

    if st.button("📄 Mise en forme des notes"):
        if meeting_notes.strip():
            with st.spinner("Reformulation des notes..."):
                formatted_notes = format_notes_with_chatgpt(meeting_notes)
            st.success("Notes reformulées avec succès !")
            st.write("### Notes reformulées")
            st.write(formatted_notes)
        else:
            st.warning("Veuillez d'abord entrer des notes.")

elif active_tab == "📂 Documents":
    st.header("📂 Documents")
    uploaded_files = st.file_uploader("Dépose tes fichiers ici", accept_multiple_files=True)
    if uploaded_files:
        st.write("📄 Fichiers chargés :")
        for file in uploaded_files:
            st.write(f"✅ {file.name}")

elif active_tab == "📅 Prochaine réunion":
    st.header("📅 Prochaine réunion")
    next_meeting_date = st.date_input("Date de la prochaine réunion :", value=datetime.today(), key="next_meeting_date", format="DD/MM/YYYY")
    next_meeting_time = st.time_input("Heure de la prochaine réunion :", value=time(10, 0), key="next_meeting_time", step=1800)
    next_meeting_duration = st.number_input("Durée de la prochaine réunion (heures)", min_value=0.5, max_value=8.0, value=1.0, step=0.5)

    next_meeting_notes = st.text_area(
        "Préparation", 
        placeholder="Exemple : Sujets à aborder, documents à préparer...", 
        height=100
    )

# Bouton d'enregistrement en bas
st.markdown("<hr style='border:1px solid black;margin-top:20px;'>", unsafe_allow_html=True)
if st.button("✅ Enregistrer la réunion"):
    st.success("Réunion enregistrée avec succès !")
    st.write("### Récapitulatif")
    st.write(f"**Titre :** {meeting_title if 'meeting_title' in locals() else 'Non renseigné'}")
    st.write(f"**Date :** {meeting_date.strftime('%d/%m/%Y') if 'meeting_date' in locals() else 'Non renseigné'}")
    st.write(f"**Heure :** {meeting_time.strftime('%H:%M') if 'meeting_time' in locals() else 'Non renseigné'}")
    st.write(f"**Participants :** {participants if 'participants' in locals() else 'Non renseigné'}")
    if 'uploaded_files' in locals() and uploaded_files:
        st.write(f"**Fichiers chargés :** {[file.name for file in uploaded_files]}")
    st.write(f"**Notes :**\n{meeting_notes if 'meeting_notes' in locals() else 'Non renseigné'}")
    st.write(f"**Date de la prochaine réunion :** {next_meeting_date.strftime('%d/%m/%Y') if 'next_meeting_date' in locals() else 'Non renseigné'}")
    st.write(f"**Heure de la prochaine réunion :** {next_meeting_time.strftime('%H:%M') if 'next_meeting_time' in locals() else 'Non renseigné'}")
    st.write(f"**Durée de la prochaine réunion :** {next_meeting_duration if 'next_meeting_duration' in locals() else 'Non renseigné'} heure(s)")
    st.write(f"**Préparation pour la prochaine réunion :**\n{next_meeting_notes if 'next_meeting_notes' in locals() else 'Non renseigné'}")
