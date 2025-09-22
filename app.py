import streamlit as st
import tempfile
import os
from pathlib import Path
from PIL import Image

# Import du workflow
from backend import run_complete_matching_workflow
from modules.export_utils import export_to_excel

def setup_page_config():
    """Configure la page Streamlit avec les paramètres de base."""
    st.set_page_config(
        page_title="Matching CV IA",
        page_icon="🔍",
        layout="centered"
    )

def validate_inputs(offer_link: str, uploaded_files) -> tuple[bool, str]:
    """
    Valide les entrées utilisateur.
    
    Args:
        offer_link: Lien vers l'offre d'emploi
        uploaded_files: Liste de fichiers CV uploadés
    
    Returns:
        Tuple contenant (is_valid, error_message)
    """
    if not offer_link or not offer_link.strip():
        return False, "Veuillez saisir le lien de l'offre d'emploi"
    
    if not uploaded_files or len(uploaded_files) == 0:
        return False, "Veuillez sélectionner au moins un fichier CV"
    for file in uploaded_files:
        if file.type not in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/plain"]:
            return False, "Format de fichier non supporté. Utilisez PDF, DOCX ou TXT"
    return True, ""

def save_uploaded_file(uploaded_file) -> str:
    """
    Sauvegarde le fichier uploadé temporairement.
    
    Args:
        uploaded_file: Fichier uploadé par l'utilisateur
    
    Returns:
        Chemin vers le fichier sauvegardé
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        return tmp_file.name

def render_form():
    """Affiche le formulaire principal de l'application."""
    logo = Image.open("parlym_logo.png")
    st.image(logo, width=300)

    st.title("Matching CV / offre d'emploi")
    
    with st.form("cv_matching_form", clear_on_submit=False):
        st.subheader("Informations")
        
        offer_link = st.text_input(
            "Offre *",
            placeholder="Lien de l'offre",
            help="Collez ici le lien vers l'offre d'emploi"
        )
        
        uploaded_files = st.file_uploader(
            "CV *",
            type=['pdf'],
            help="Sélectionnez votre CV (PDF uniquement)",
            accept_multiple_files=True
        )
        
        submitted = st.form_submit_button(
            "Soumettre",
            type="secondary",
            use_container_width=True
        )
        
        return submitted, offer_link, uploaded_files

def process_matching(offer_link: str, cv_file_info: list[tuple]):
    """
    Lance le processus de matching entre le CV et l'offre.
    
    Args:
        offer_link: Lien vers l'offre d'emploi
        cv_file_info: Liste de tuples (chemin_temporaire, nom_original)
    """
    # Indicateur d'analyse en cours
    with st.spinner("Analyse en cours..."):
        # On passe uniquement les chemins temporaires au workflow
        cv_file_paths = [info[0] for info in cv_file_info]
        original_filenames = {Path(info[0]).name: info[1] for info in cv_file_info}
        results = run_complete_matching_workflow(offer_link, cv_file_paths)
        # Remplacer le nom du fichier temporaire par le nom original dans les résultats
        for result in results:
            temp_name = result.get('cv_filename', '')
            if temp_name in original_filenames:
                result['cv_filename'] = original_filenames[temp_name]

    # Générer le fichier Excel
    excel_filename = export_to_excel(results)
    # Bouton de téléchargement
    with open(excel_filename, "rb") as file:
        st.download_button(
            label="Télécharger le rapport Excel",
            data=file.read(),
            file_name="rapport_matching.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    # Nettoyage du fichier Excel temporaire
    try:
        os.unlink(excel_filename)
    except OSError:
        pass

def main():
    """Fonction principale de l'application."""
    setup_page_config()
    
    submitted, offer_link, uploaded_files = render_form()
    if submitted:
        is_valid, error_message = validate_inputs(offer_link, uploaded_files)
        if not is_valid:
            st.error(error_message)
            return
        try:
            # Sauvegarder tous les fichiers 
            cv_file_info = []  # Liste de tuples (chemin_temporaire, nom_original)
            for uploaded_file in uploaded_files:
                cv_path = save_uploaded_file(uploaded_file)
                cv_file_info.append((cv_path, uploaded_file.name))
            process_matching(offer_link, cv_file_info)
        except Exception as e:
            st.error(f"Erreur lors du traitement : {str(e)}")

if __name__ == "__main__":
    main()