# Import des fonctions principales de chaque module
from .job_processing import (
    api_url,
    fetch_job_data,
    process_job_offer_workflow
)

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
    # Job processing
    'api_url',
    'fetch_job_data', 
    'process_job_offer_workflow',
    
    # CV extraction
    'extract_text_from_pdf',
    'extract_multiple_cvs',
    
    # AI analysis
    'analyze_cv_parlym',

    # Export
    'export_to_excel'
]

