import PyPDF2
from pathlib import Path
import os


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extrait le texte d'un fichier PDF.
    
    Args:
        file_path: Chemin vers le fichier PDF
        
    Returns:
        Texte extrait du PDF
    """
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
            
            return text.strip()
    except Exception as e:
        raise Exception(f"Erreur lors de l'extraction PDF: {str(e)}")
    

def extract_multiple_cvs(cv_files_list: list) -> dict:
    """
    Extrait le texte de plusieurs CV PDF.
    
    Args:
        cv_files_list: Liste des chemins vers les CV PDF
        
    Returns:
        Dictionnaire {nom_fichier: texte_cv}
    """
    cvs_extracted = {}
    
    for cv_path in cv_files_list:
        try:
            # Extraction du nom de fichier
            filename = Path(cv_path).name
            
            # Extraction du texte
            cv_text = extract_text_from_pdf(cv_path)
            
            # Stockage
            cvs_extracted[filename] = cv_text
                        
        except Exception as e:
            print(f"❌ Erreur avec {cv_path}: {str(e)}")
    
    return cvs_extracted


