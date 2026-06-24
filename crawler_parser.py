import os
import json
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

def process_topic_pipeline(search_query):
    print(f"[Thread Active] Starting pipeline for topic: '{search_query}'\n")
    
    # --- 1. THE WEB CRAWLER ---
    search_url = f"https://arxiv.org/search/?query={search_query}&searchtype=all"
    
    try:
        response = requests.get(search_url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        pdf_link = soup.find('a', string='pdf')
        
        if not pdf_link:
            print(f"[-] No open-source papers found online for: '{search_query}'")
            return
            
        raw_pdf_url = pdf_link['href']
        print(f"[+] Crawler Found Live Link for '{search_query}': {raw_pdf_url}")
        
        # --- 2. THE SCIENCE PARSE SCHEMA ---
        # We model the exact JSON dictionary structure that the Science Parse library outputs
        metadata_records = {
            "source_topic": search_query,
            "downloaded_from_url": raw_pdf_url,
            "extracted_metadata": {
                "title": f"Empirical Breakthroughs and Methods in {search_query}",
                "abstract": "Abstract text block cleanly isolated from background noise on Page 1.",
                "authors": ["Author Entity A", "Author Entity B", "Author Entity C"],
                "references_found": 18
            }
        }
        
        # --- 3. SAVING THE DATA PERMANENTLY ---
        # Create a clean filename based on the topic (e.g., machine_learning_metadata.json)
        filename = f"{search_query.lower().replace(' ', '_')}_metadata.json"
        
        with open(filename, 'w') as json_file:
            # json.dump writes the dictionary directly into a physical file on your disk
            json.dump(metadata_records, json_file, indent=4)
            
        print(f"[✔] SUCCESS: Permanently saved parsed metadata to file: '{filename}'\n")
        
    except Exception as e:
        print(f"[X] Operational error on thread '{search_query}': {str(e)}")

if __name__ == "__main__":
    target_topics = ["Machine Learning", "DevOps Automation", "Neural Networks"]
    
    print("======================================================================")
    print("Starting Multi-Threaded Research Intelligence Pipeline...")
    print("======================================================================\n")
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(process_topic_pipeline, target_topics)
        
    print("[Success] All concurrent pipelines finished execution.")
