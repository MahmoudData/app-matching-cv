# Import des fonctions principales de chaque module
from .cv_extraction import (
    extract_text_from_pdf,
    extract_multiple_cvs
)

from .ai_analysis import (
    analyze_cv_parlym,
)

from .export_utils import (
    export_to_excel,
)

# Définition de ce qui est accessible quand on fait : from modules import *
__all__ = [
    # CV extraction
    'extract_text_from_pdf',
    'extract_multiple_cvs',
    
    # AI analysis
    'analyze_cv_parlym',

    # Export
    'export_to_excel'
]

