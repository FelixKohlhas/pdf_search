import os
import sqlite3
import re
from flask import Flask, render_template, request, send_from_directory
import argparse

app = Flask(__name__)

def preprocess_search_query(search_query):
    search_query = search_query.replace('*', '%').replace('?', '_')
    return search_query

def calculate_ratio(matches, text_length):
    if text_length == 0:
        return 0
    return matches / text_length

def search_database(db_name, search_query):
    search_query = preprocess_search_query(search_query)
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT filename, relative_path, text FROM pdf_text WHERE LOWER(text) LIKE LOWER(?)", ('%'+search_query+'%',))
    results = c.fetchall()
    conn.close()

    # Calculate the ratio of matches to the length of the text for each result
    results_with_ratio = []
    for filename, relative_path, text in results:
        matched_lines = print_matched_lines(text, search_query)
        num_matches = len(matched_lines)
        text_length = len(text)
        ratio = calculate_ratio(num_matches, text_length)
        results_with_ratio.append((filename, relative_path, matched_lines, ratio))

    # Sort the results based on the ratio in descending order
    results_with_ratio.sort(key=lambda x: x[3], reverse=True)

    return results_with_ratio

def print_matched_lines(file_text, search_query):
    search_query = preprocess_search_query(search_query)
    lines = file_text.split('\n')
    matched_lines = []
    for line in lines:
        if re.search(search_query, line, re.IGNORECASE):
            matched_lines.append(line)
    return matched_lines

@app.route("/", methods=["GET", "POST"])
def search_form():
    if request.method == "POST":
        search_query = request.form.get("search_query")
        db_name = args.database
        url_prefix = args.url_prefix

        search_result = search_database(db_name, search_query)
        if search_result:
            results = []
            for i, (filename, relative_path, matched_lines, ratio) in enumerate(search_result, start=1):
                # Update the relative path to the base URL
                url = url_prefix + relative_path
                results.append((i, filename, url, matched_lines, ratio))
            return render_template("results.html", search_query=search_query, results=results)
        else:
            return render_template("no_results.html", search_query=search_query)

    return render_template("search_form.html")

@app.route('/file/<path:filename>')
def serve_files(filename):
    if args.files and os.path.isdir(args.files):
        return send_from_directory(args.files, filename)
    return 404

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask web interface to search PDF files by their content.")
    parser.add_argument("-d", "--database", default="pdf_search.db", help="Path of the database")
    parser.add_argument("-u", "--url-prefix", default="/file/", help="URL to prefix to relative paths")
    parser.add_argument("-f", "--files", default=None, help="Directory of PDF files (optional; allows access to the files through webinterface)")
    parser.add_argument("--port", type=int, default=5001, help="Port to run the Flask app (default: 5001)")
    args = parser.parse_args()

    app.run(host='0.0.0.0', port=args.port, debug=True)