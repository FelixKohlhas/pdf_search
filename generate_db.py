import os
import sqlite3
import argparse
import time
from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_file):
    with open(pdf_file, 'rb') as file:
        try:
            pdf_reader = PdfReader(file)
            text = ''
            for page in pdf_reader.pages:
                    text += page.extract_text()
        except:
            return ""
    return text

def create_database(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS pdf_text (
            id INTEGER PRIMARY KEY,
            filename TEXT,
            relative_path TEXT,
            text TEXT,
            last_modified REAL
        )
    ''')
    conn.commit()
    conn.close()

def insert_text_into_database(db_name, filename, relative_path, text, last_modified):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('INSERT INTO pdf_text (filename, relative_path, text, last_modified) VALUES (?, ?, ?, ?)', (filename, relative_path, text, last_modified))
    conn.commit()
    conn.close()

def get_last_modified_from_database(db_name, filename):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('SELECT last_modified FROM pdf_text WHERE filename = ?', (filename,))
    result = c.fetchone()
    conn.close()
    return result

def main():
    parser = argparse.ArgumentParser(description="Extract text from PDF files and store it in a SQLite database.")
    parser.add_argument("pdf_folder", default=".", help="Path to the folder containing PDF files")
    parser.add_argument("-d", "--database", default="pdf_search.db", help="Path of the database")
    args = parser.parse_args()

    pdf_folder = args.pdf_folder
    database = args.database

    create_database(database)

    for root, _, files in os.walk(pdf_folder):
        for filename in files:
            if filename.endswith('.pdf'):
                pdf_file = os.path.join(root, filename)
                last_modified = os.path.getmtime(pdf_file)
                relative_path = os.path.relpath(pdf_file, pdf_folder)

                last_modified_in_db = get_last_modified_from_database(database, filename)

                if last_modified_in_db is None or last_modified > last_modified_in_db[0]:
                    text = extract_text_from_pdf(pdf_file)
                    insert_text_into_database(database, filename, relative_path, text, last_modified)
                    print(f'Extracted and stored text from: {pdf_file}')
                else:
                    print(f'Skipped {filename} as it has not been modified since the last time.')

if __name__ == '__main__':
    main()