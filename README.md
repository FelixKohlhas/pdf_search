<div align="center">

# PDF Search

*Web interface for searching content in PDF files*

<img src="https://github.com/FelixKohlhas/pdf_search/assets/18424307/6014cb85-703f-4adb-9431-bc1b0e246f6a" width="75%">

</div>

## Features

- Search for specific keywords within a collection of PDF files.
- View matched lines from the PDF files for each search result.
- Sort search results based on the relevance of matches.
- Display search results with a calculated relevance ratio.
- Web interface powered by Flask and SQLite database.

## Requirements

- Python 3.x
- Flask
- PyPDF2

## Getting Started

1. Clone this repository:

    ```bash
    git clone https://github.com/FelixKohlhas/pdf_search.git
    cd pdf_search
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Create the database

    ```bash
    python generate_db.py <path to pdfs>
    ```

4. Run the web interface:

    ```bash
    python app.py -f <path to pdfs>
    ```

5. Open your web browser and navigate to `http://localhost:5001` to access the PDF search.

## Usage

### generate_db.py
```
usage: generate_db.py [-h] [-d DATABASE] pdf_folder

Extract text from PDF files and store it in a SQLite database.

positional arguments:
  pdf_folder            Path to the folder containing PDF files

options:
  -h, --help            show this help message and exit
  -d DATABASE, --database DATABASE
                        Path of the database
```

### app.py
```
usage: app.py [-h] [-d DATABASE] [-u URL_PREFIX] [-f FILES] [--port PORT]

Flask web interface to search PDF files by their content.

options:
  -h, --help            show this help message and exit
  -d DATABASE, --database DATABASE
                        Path of the database
  -u URL_PREFIX, --url-prefix URL_PREFIX
                        URL to prefix to relative paths
  -f FILES, --files FILES
                        Directory of PDF files (optional; allows access to the files through webinterface)
  --port PORT           Port to run the Flask app (default: 5001)
```


## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or create a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.