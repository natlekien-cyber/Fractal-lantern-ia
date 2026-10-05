"""
IA FRACTALE - Version 8.8 (Stable)
Axiome Central : [Cohérence = Survie] (Zéro spéculation, Zéro hallucination)
Développé pour l'informatique de poche déconnectée (iOS a-Shell / CPU Local).

Ce programme est un automate déterministe d'extraction et de filtrage. 
Face à l'absence de données vérifiables ou au bruit du réseau, il applique 
la clôture logique par le silence plutôt que le pari statistique.
"""

import sys
import re
import urllib.request
import urllib.parse
import json
import xml.etree.ElementTree as ET

VERSION = "8.8 - Hybride Autonome (ArXiv Enhanced)"

def nettoyer_texte(texte):
    """Nettoyage strict des balises HTML, entités XML et résidus de formatage.
    Cette fonction agit comme un scalpel pour éliminer la rhétorique."""
    if not texte:
        return ""
    # Suppression des balises HTML
    texte = re.sub(r'<[^>]*>', '', texte)
    # Résolution des entités textuelles courantes
    entites = {'&#39;': "'", '&quot;': '"', '&amp;': '&', '&lt;': '<', '&gt;': '>'}
    for entite, caractere in entites.items():
        texte = texte.replace(entite, caractere)
    # Compactage des espaces blancs parasites
    texte = re.sub(r'\s+', ' ', texte)
    return texte.strip()

def recherche_locale(query, fichier_corpus="corpus.txt"):
    """Noyau Analytique 1 : Clôture locale déterministe au sein du savoir immanent."""
    try:
        with open(fichier_corpus, 'r', encoding='utf-8') as f:
            lignes = f.readlines()
        resultats = [nettoyer_texte(l) for l in lignes if query.lower() in l.lower()]
        return [r for r in resultats if r]
    except FileNotFoundError:
        return []

def recherche_wikipedia(query):
    """Couche Réseau 2 (Secours Encyclopédique) : Interrogation brute de l'API Wikipédia."""
    url = f"https://wikipedia.org{urllib.parse.quote(query)}&format=json"
    try:
        # L'identifiant User-Agent simule un navigateur pour éviter le rejet des serveurs (Erreur 403)
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)"})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        snippets = []
        if 'query' in data and 'search' in data['query']:
            for item in data['query']['search'][:3]:
                extrait = nettoyer_texte(item['snippet'])
                if extrait:
                    snippets.append(f"[WIKI] -> {extrait}...")
        return snippets
    except Exception:
        return []

def recherche_arxiv(query):
    """Couche Réseau 3 (Validation Scientifique) : Interrogation brute d'ArXiv via XML."""
    query_encoded = urllib.parse.quote(query)
    url = f"https://arxiv.org{query_encoded}%22&max_results=2"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as response:
            xml_data = response.read()
        
        root = ET.fromstring(xml_data)
        results = []
        ns = {'atom': 'http://w3.org'}
        
        for entry in root.findall('atom:entry', ns):
            title = entry.find('atom:title', ns).text
            summary = entry.find('atom:summary', ns).text
            titre_clean = nettoyer_texte(title)
            summary_clean = nettoyer_texte(summary)
            if summary_clean:
                results.append(f"[ARXIV] -> {titre_clean} : {summary_clean[:180]}...")
        return results
    except Exception:
        return []

def executer_cycle(query):
    """Orchestrateur du Cycle d'Acquisition : Applique la cascade logique."""
    if not query.strip():
        return
    
    # 1. Tentative au sein de la clôture locale
    res = recherche_locale(query)
    if res:
        for r in res[:3]: 
            print(f"[LOCAL] -> {r}")
        return
        
    # 2. Tentative Réseau Hybride Externe (Wiki + ArXiv)
    wiki_res = recherche_wikipedia(query)
    arxiv_res = recherche_arxiv(query)
    
    total_res = wiki_res + arxiv_res
    if total_res:
        for r in total_res:
            print(r)
            print() 
    else:
        # Suprématie du silence : aucune donnée valide trouvée, l'agent se tait.
        pass

def main():
    print(f"=== IA FRACTALE {VERSION} ===")
    while True:
        try:
            query = input("Question > ")
            executer_cycle(query)
        except (KeyboardInterrupt, EOFError):
            print("\n[Clôture du système]")
            break

if __name__ == "__main__":
    main()
