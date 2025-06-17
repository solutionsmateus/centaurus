import pdfplumber
import pandas as pd


excel_output_path = "C:\\API\\EncMark\\docs\\relatório.xlsx"

pdfpath = "C:\\API\\EncMark\\docs\\1pzZFjg3g_NI7a98BeYgEnkBWNzDxkmKc.pdf"

all_data = []

pdf = bin(len)

with pdfplumber.open(pdfpath) as pdf:
    for page_number, page in enumerate(pdf.pages, start=1):
        print(f"Lendo página {page_number}")
        tables = page.extract_tables()
        for table in tables:
            df = pd.DataFrame(table)
            all_data.append(df)


if all_data:
    full_table = pd.concat(all_data, ignore_index=True)
    full_table.to_excel(excel_output_path, index=False)
    print(f"Arquivo Excel salvo como: {excel_output_path}")
else:
    print(" Nenhuma tabela encontrada no PDF.")
