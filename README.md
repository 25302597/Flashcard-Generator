# Flashcard Generator

A Python application that generates flashcards from text extracted from a PDF file. The text is processed using DeepAI's AI capabilities to create flashcards in a defined format, making it suitable for studying or revising definitions.

## Features

- Upload a PDF file and specify a range of pages to extract text.
- Automatically create flashcards in a formatted text file.
- Download generated flashcards for easy use.
- Simple and intuitive web interface powered by Gradio.

## Requirements

Before running the application, ensure that you have the following installed:

- Python 3.7 or later
- Necessary Python packages:
  - `PyMuPDF` for PDF text extraction
  - `Playwright` for web automation
  - `Gradio` for the user interface

You can install the required packages using pip:

```bash
pip install PyMuPDF playwright gradio
playwright install
```

## How to Use

1. **Clone the Repository** (if applicable):

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Run the Flashcard Generator**:

   ```bash
   python flashcard_generator.py
   ```

3. **Access the Web Interface**:
   - Once the application is running, navigate to the provided URL (usually `http://127.0.0.1:7860`) in your web browser.
   
4. **Upload PDF File**:
   - Click on the "Upload PDF" button and select the PDF file you want to process.

5. **Specify Page Range**:
   - Enter the starting and ending page numbers from which text should be extracted.

6. **Optional - File Name**:
   - Provide an optional custom file name for the output flashcards.

7. **Generate Flashcards**:
   - Submit the form. The application will process the PDF, generate the flashcards based on the extracted text, and provide a downloadable link for the generated file.

## Generated Flashcards Format

Flashcards are created in a text format where each line consists of:

```
Front: Definition
```

Example:
```
Distributed denial-of-service:(DDoS)	An attempt to make a digital or network system unavailable by flooding it with traffic from multiple compromised systems.
```

## Error Handling

The application includes error handling to provide user-friendly messages for issues such as:
- Invalid page ranges
- File reading/writing errors
- Issues during AI interaction

## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE.

## Acknowledgments

- [DeepAI](https://deepai.org/) for providing the AI API.
- [Gradio](https://www.gradio.app/) for enabling quick and easy web app creation.
- [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/) for PDF handling.
- [Playwright](https://playwright.dev/) for browser automation.


### Notes

- Replace `<repository-url>` and `<repository-directory>` with the actual URL and directory name if your code is hosted in a version control system like Git.
- Ensure that any licensing information relevant to your project is included and correct. Adjust the license section accordingly.
- You may also want to add troubleshooting tips or FAQs based on potential user issues you anticipate.
