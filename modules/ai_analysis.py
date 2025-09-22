import openai
import json
import streamlit as st


openai.api_key = st.secrets["OPENAI_API_KEY"]


def create_parlym_scoring_prompt(job_description: str, cv_text: str) -> str:
    """
    Crée le prompt pour l'analyse de matching selon les critères PARLYM.
    
    Args:
        job_description: Description formatée de l'offre
        cv_text: Texte extrait du CV
        
    Returns:
        Prompt structuré pour GPT-4o mini
    """
    
    prompt = f"""# Instructions pour l'Analyse de Matching Recrutement

## Contexte :
Tu es un expert en recrutement avec une spécialité dans l'ingénierie industrielle.  
Tu maîtrises toutes les techniques pour trouver la recrue idéale, de l'analyse de CV à la réalisation des entretiens.

Tu as une approche moderne du recrutement :  
Tes actions sont guidées par les concepts de **marque employeur** et **Employee Advocacy**.

## Ta mission :
Réaliser une analyse complète en 4 parties pour chaque profil reçu.

### Partie 1 : Un résumé rapide du profil du candidat
> Fais un résumé synthétique du parcours et des compétences principales du candidat.

### Partie 2 : Les points forts du profil par rapport à la fiche de poste
> Liste les atouts du candidat, notamment tout ce qui est en adéquation forte avec les critères de l'offre.

### Partie 3 : Les points de vigilance du profil par rapport à la fiche de poste
> Indique de façon factuelle les éventuels écarts, faiblesses ou points à clarifier en entretien.

### Partie 4 : Une note sur 100 du profil 
> Attribue une note sur 100 (sur la base de la grille de scoring fournie). 

## Rubrique de Scoring ATS - Matching CV ↔ Offres Parlym

### Objectif
Attribuer un score de matching entre un CV et une offre d'emploi Parlym, basé sur les critères globaux les plus pertinents, classés par ordre d'importance.

### 1. Expérience professionnelle sur les activités/missions clés (35 points)
- **Adéquation des expériences passées du candidat avec les activités principales mentionnées dans l'offre**
  - Expériences clairement en lien direct avec la majorité des missions de l'offre : **+35 pts**
  - Expériences couvrant une partie significative des missions (mais pas toutes) : **+20 pts**
  - Expériences couvrant 1 à 2 missions seulement : **+10 pts**
  - Aucune expérience sur les activités mentionnées : **0 pt**

### 2. Expérience (nombre d'années/séniorité) (25 points)
- **Nombre d'années d'expérience dans le type de poste recherché**
  - Expérience ≥ exigence de l'offre : **+25 pts**
  - Expérience –1 an par rapport à l'exigence : **+18 pts**
  - Expérience –2 ans : **+10 pts**
  - Pas d'expérience pertinente : **0 pt**

### 3. Secteur d'activité / Environnement technique (20 points)
- **Expérience dans le secteur industriel ciblé (énergie, oil & gas, projets industriels, etc.)**
  - Même secteur / environnement : **+20 pts**
  - Secteur technique voisin : **+12 pts**
  - Secteur éloigné : **+5 pts**
  - Aucun secteur pertinent : **0 pt**

### 4. Compétences techniques générales (logiciels, méthodes) (12 points)
- **Maîtrise des outils/méthodes mentionnés dans l'offre (planification, gestion de projet, pack office, ERP, etc.)**
  - Maîtrise de tous les outils demandés : **+12 pts**
  - Maîtrise de la majorité : **+8 pts**
  - Maîtrise partielle : **+4 pts**
  - Aucun outil pertinent : **0 pt**

### 5. Formation (8 points)
- **Formation attendue (Bac+5, école d'ingénieur ou équivalent)**
  - Diplôme exact exigé : **+8 pts**
  - Diplôme du niveau attendu mais pas le bon intitulé : **+5 pts**
  - Diplôme légèrement inférieur (Bac+4) ou équivalent significatif : **+3 pts**
  - Diplôme en-deçà : **0 pt**

### TOTAL : /100

## Instructions pour le matching :

1. **Extraire pour chaque CV** les informations liées à : expérience (missions réalisées), durée d'expérience, secteur d'activité, outils/compétences, formation.
2. **Comparer chaque critère** avec ceux attendus dans l'offre d'emploi.
3. **Attribuer les points selon la grille ci-dessus** pour chaque critère.
4. **Additionner les points** pour obtenir le score final sur 100.
5. **Optionnel :**
   - Définir des seuils pour la pré-sélection automatique (exemple : shortlist si score ≥ 70).
   - Affiner la pondération selon la criticité du poste ou selon le retour des opérationnels.

**NB :**  
Cette grille est conçue pour s'adapter à tous types d'offres Parlym, en se concentrant sur les critères globaux et structurants du matching, tout en restant agnostique des activités spécifiques.

RÉPONDRE UNIQUEMENT AVEC UN JSON VALIDE, SANS AUCUN TEXTE EXPLICATIF

---

OFFRE D'EMPLOI :
{job_description}

---

CV DU CANDIDAT :
{cv_text}"""
    
    return prompt


def analyze_cv_parlym(job_description: str, cv_text: str) -> dict:
    """
    Analyse complète CV vs Offre avec structured outputs OpenAI.
    Combine le prompt PARLYM + l'appel API en une seule fonction.
    
    Args:
        job_description: Description formatée de l'offre
        cv_text: Texte extrait du CV
        api_key: Clé API OpenAI
        
    Returns:
        Dictionnaire structuré avec l'analyse complète
    """
    
    # Création du prompt PARLYM complet
    prompt = create_parlym_scoring_prompt(job_description, cv_text)
    
    # Schéma JSON pour structured outputs
    json_schema = {
        "name": "cv_analysis_parlym",
        "description": "Analyse de matching CV vs offre d'emploi selon critères PARLYM",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "Prénom": {
                    "type": "string",
                    "description": "Prénom du candidat"
                },
                "Nom": {
                    "type": "string", 
                    "description": "Nom du candidat"
                },
                "Score": {
                    "type": "integer",
                    "description": "Score de matching sur 100 selon grille PARLYM",
                    "minimum": 0,
                    "maximum": 100
                },
                "Résumé": {
                    "type": "string",
                    "description": "Résumé synthétique du profil candidat"
                },
                "Points_forts": {
                    "type": "array",
                    "description": "Liste des points forts du candidat par rapport à l'offre",
                    "items": {
                        "type": "string"
                    }
                },
                "Points_vigilance": {
                    "type": "array", 
                    "description": "Liste des points de vigilance du candidat par rapport à l'offre",
                    "items": {
                        "type": "string"
                    }
                }
            },
            "required": ["Prénom", "Nom", "Score", "Résumé", "Points_forts", "Points_vigilance"],
            "additionalProperties": False
        }
    }
    
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            response_format={
                "type": "json_schema",
                "json_schema": json_schema
            },
            #max_tokens=2000,
            temperature=0
        )
        
        result = json.loads(response.choices[0].message.content)
        
        return result
        
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse: {str(e)}")
        # Retour d'erreur structuré
        return {
            "Prénom": "",
            "Nom": "",
            "Score": 0,
            "Résumé": f"Erreur lors de l'analyse: {str(e)}",
            "Points_forts": [],
            "Points_vigilance": [f"Erreur technique: {str(e)}"]
        }
    
