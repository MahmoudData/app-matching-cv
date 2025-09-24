import PyPDF2
from pathlib import Path
import os
from docx import Document


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
            text = "\n".join([page.extract_text() for page in pdf_reader.pages])
            return text.strip()
    except Exception as e:
        raise Exception(f"Erreur lors de l'extraction PDF: {str(e)}")
    

def extract_text_from_word(file_path: str) -> str:
    """
    Extrait le texte d'un fichier Word.

    Args:
        file_path: Chemin vers le fichier Word

    Returns:
        Texte extrait du fichier Word
    """
    try:
        document = Document(file_path)
        text = "\n".join([paragraph.text for paragraph in document.paragraphs])
        return text.strip()
    except Exception as e:
        raise Exception(f"Erreur lors de l'extraction Word: {str(e)}")


def extract_text_from_file(file_path: str) -> str:
    """
    Extrait le texte d'un fichier, qu'il soit PDF ou Word.

    Args:
        file_path: Chemin vers le fichier

    Returns:
        Texte extrait du fichier
    """
    if file_path.lower().endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.lower().endswith('.docx'):
        return extract_text_from_word(file_path)
    else:
        raise ValueError("Format de fichier non supporté. Seuls les fichiers PDF et Word sont acceptés.")


def extract_multiple_cvs(cv_files_list: list) -> dict:
    """
    Extrait le texte de plusieurs CV (PDF ou Word).

    Args:
        cv_files_list: Liste des chemins vers les CV

    Returns:
        Dictionnaire {nom_fichier: texte_cv}
    """
    cvs_extracted = {}

    for cv_path in cv_files_list:
        try:
            # Extraction du nom de fichier
            filename = Path(cv_path).name

            # Extraction du texte
            cv_text = extract_text_from_file(cv_path)

            # Stockage
            cvs_extracted[filename] = cv_text

        except Exception as e:
            print(f"❌ Erreur avec {cv_path}: {str(e)}")

    return cvs_extracted


