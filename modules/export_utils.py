import pandas as pd
from datetime import datetime


def export_results_to_dataframe(results: list) -> pd.DataFrame:
    """
    Convertit les résultats de matching en DataFrame pandas.
    
    Args:
        results: Liste des résultats d'analyse
        
    Returns:
        DataFrame avec toutes les données structurées
    """
    
    # Préparation des données pour le DataFrame
    data_rows = []
    
    for result in results:
        # Conversion des listes en strings pour l'export
        points_forts_str = " | ".join(result.get('Points_forts', []))
        points_vigilance_str = " | ".join(result.get('Points_vigilance', []))
        
        row = {
            'Prénom': result.get('Prénom', ''),
            'Nom': result.get('Nom', ''),
            'Fichier_CV': result.get('cv_filename', ''),
            'Score': result.get('Score', 0),
            'Résumé': result.get('Résumé', ''),
            'Points_Forts': points_forts_str,
            'Points_Vigilance': points_vigilance_str,
        }
        data_rows.append(row)
    
    # Création du DataFrame
    df = pd.DataFrame(data_rows)
    
    return df



def export_to_excel(results: list, filename: str = None) -> str:
    """
    Exporte les résultats vers un fichier Excel.
    
    Args:
        results: Liste des résultats d'analyse
        filename: Nom du fichier (optionnel)
        
    Returns:
        Nom du fichier créé
    """
    
    # Génération du nom de fichier si non fourni
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"matching_cv_results_{timestamp}.xlsx"
    
    # Création du DataFrame
    df = export_results_to_dataframe(results)
    
    # Export Excel avec mise en forme
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Résultats_Matching', index=False)
        
        # Récupération du worksheet pour la mise en forme
        worksheet = writer.sheets['Résultats_Matching']
        
        # Ajustement automatique de la largeur des colonnes
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            
            # Limitation de la largeur max et ajustement
            adjusted_width = min(max_length + 2, 50)
            worksheet.column_dimensions[column_letter].width = adjusted_width
    
    print(f"✅ Export Excel créé: {filename}")
    return filename