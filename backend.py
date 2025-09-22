from modules.job_processing import process_job_offer_workflow
from modules.cv_extraction import extract_multiple_cvs
from modules.ai_analysis import analyze_cv_parlym

def run_complete_matching_workflow(offre_url: str, cv_files_list: list) -> list:
    """
    Workflow complet de matching : analyse tous les CV vs l'offre.
    
    Args:
        offre_url: URL de l'offre d'emploi PARLYM
        cv_files_list: Liste des chemins vers les CV PDF
        
    Returns:
        Liste des analyses triées par score décroissant
    """
    # Étape 1: Traitement de l'offre d'emploi
    try:
        job_description = process_job_offer_workflow(offre_url)
    except Exception as e:
        return []
    
    # Étape 2: Extraction des CV
    try:
        all_cvs = extract_multiple_cvs(cv_files_list)
    except Exception as e:
        return []
    
    # Étape 3: Analyse IA de chaque CV vs Offre
    results = []
    for filename, cv_text in all_cvs.items():
        try:
            analysis = analyze_cv_parlym(job_description, cv_text)
            analysis["cv_filename"] = filename
            results.append(analysis)
        except Exception as e:
            error_result = {
                "cv_filename": filename,
                "Prénom": "",
                "Nom": "",
                "Score": 0,
                "Résumé": f"Erreur lors de l'analyse du CV {filename}",
                "Points_forts": [],
                "Points_vigilance": [f"Erreur technique: {str(e)}"]
            }
            results.append(error_result)
    
    # Étape 4: Tri des résultats par score décroissant
    results.sort(key=lambda x: x.get('Score', 0), reverse=True)
    return results