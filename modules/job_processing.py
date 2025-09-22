import requests
import json
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import pandas as pd

import openai
import json
import streamlit as st

openai.api_key = st.secrets["OPENAI_API_KEY"]

def api_url(offre_url: str) -> str:
    """
    Extrait l'ID du job depuis l'URL de l'offre et construit l'URL de l'API.
    
    Args:
        offre_url: URL de l'offre d'emploi
        
    Returns:
        Dictionnaire contenant l'ID et l'URL de l'API
    """
    # Nettoyage de l'URL et extraction de l'ID
    job_id = offre_url.strip().split("/")[-1]
    api_url = f"https://parlym.nos-recrutements.fr/api/job/{job_id}"
    
    return api_url


def fetch_job_data(api_url: str) -> dict:
    """
    Récupère les données de l'offre depuis l'API.
    
    Args:
        api_url: URL de l'API pour récupérer les données
        
    Returns:
        Données JSON de l'offre
    """
    try:
        response = requests.get(api_url, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération des données: {e}")
        return None
    

def extract_description_mission(job_json_data: dict) -> dict:
    """
    Extrait et nettoie la description de mission depuis les données JSON.
    
    Args:
        job_json_data: Données JSON retournées par l'API
        
    Returns:
        Dictionnaire avec la description mission nettoyée
    """
    # Récupération du HTML depuis le JSON (équivalent à "JSON Property: descriptionMission")
    description_mission_html = job_json_data.get('descriptionMission', '')
    
    if not description_mission_html:
        return {
            "descriptionMissionClean": ""
        }
    
    # Parse le HTML avec BeautifulSoup (équivalent au CSS Selector: *)
    soup = BeautifulSoup(description_mission_html, 'html.parser')
    
    # Extraction du texte en gardant la structure (Return Value: Text)
    text_content = soup.get_text(separator=' ', strip=True)
    
    # Nettoyage supplémentaire - suppression des espaces multiples
    cleaned_text = ' '.join(text_content.split())
    
    return {
        "descriptionMissionClean": cleaned_text
    }


def extract_description_profile(job_json_data: dict) -> dict:
    """
    Extrait et nettoie la description de profil depuis les données JSON.
    Reproduit le comportement du second node HTML de n8n.
    
    Args:
        job_json_data: Données JSON retournées par l'API
        
    Returns:
        Dictionnaire avec la description profil nettoyée
    """
    # Récupération du HTML depuis le JSON (équivalent à "JSON Property: descriptionProfile")
    description_profile_html = job_json_data.get('descriptionProfile', '')
    
    if not description_profile_html:
        return {
            "descriptionProfileClean": ""
        }
    
    # Parse le HTML avec BeautifulSoup (équivalent au CSS Selector: *)
    soup = BeautifulSoup(description_profile_html, 'html.parser')
    
    # Extraction du texte en gardant la structure (Return Value: Text)
    text_content = soup.get_text(separator=' ', strip=True)
    
    # Nettoyage supplémentaire - suppression des espaces multiples
    cleaned_text = ' '.join(text_content.split())
    
    return {
        "descriptionProfileClean": cleaned_text
    }


def combine_job_descriptions(mission_result: dict, profile_result: dict) -> str:
    """
    Combine les descriptions mission et profil avec un formatage structuré.
    
    Args:
        mission_result: Résultat de extract_description_mission()
        profile_result: Résultat de extract_description_profile()
        
    Returns:
        Texte formaté avec les deux sections
    """
    mission_text = mission_result.get('descriptionMissionClean', '')
    profile_text = profile_result.get('descriptionProfileClean', '')
    
    formatted_text = f"""**Présentation du poste :**
{mission_text}

**Profil Recherché :**
{profile_text}"""
    
    return formatted_text


def process_job_offer_workflow(offre_url: str) -> str:
    """
    Workflow complet de traitement d'une offre d'emploi.
    Orchestre toutes les étapes du traitement.
    
    Args:
        offre_url: URL de l'offre d'emploi
        
    Returns:
        Description formatée complète de l'offre
    """
    api_endpoint = api_url(offre_url)
    job_data = fetch_job_data(api_endpoint)
    
    if not job_data:
        return "Erreur lors de la récupération des données de l'offre."
    
    mission_result = extract_description_mission(job_data)
    profile_result = extract_description_profile(job_data)
    
    combined_description = combine_job_descriptions(mission_result, profile_result)
    
    return combined_description

