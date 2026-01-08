import os
import requests
import pdfplumber
import pandas as pd
from rich.console import Console

os.environ["NO_PROXY"] = "127.0.0.1,localhost"
console = Console()

url = "https://s3.eu-west-3.amazonaws.com/customer-it.milanounica.www/3317/6598/5115/Milano_Unica_42_Edizione_Elenco_Espositori.pdf"

def main():
    try:
        console.print(f"[bold blue]Step 1: Downloading PDF...[/bold blue]")
        response = requests.get(url, timeout=60, stream=True)
        response.raise_for_status()
        with open("raw_exhibitors.pdf", "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        console.print(f"[bold blue]Step 2: Parsing PDF...[/bold blue]")
        exhibitors = []
        with pdfplumber.open("raw_exhibitors.pdf") as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    lines = text.split('\n')
                    for line in lines:
                        if "|" in line:
                            parts = line.split("|")
                            exhibitors.append({"name": parts[0].strip(), "booth": parts[1].strip()})
                        elif len(line.strip()) > 3:
                            # Heuristic for Milano Unica PDF layout
                            exhibitors.append({"name": line.strip(), "booth": "TBD"})
        
        df = pd.DataFrame(exhibitors)
        df.to_csv("pdf_exhibitors.csv", index=False)
        console.print(f"[green]PDF Extraction Success: {len(df)} items found.[/green]")
    except Exception as e:
        console.print(f"[red]PDF Error: {e}[/red]")

if __name__ == "__main__":
    main()
