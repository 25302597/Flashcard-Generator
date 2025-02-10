import fitz
from playwright.sync_api import Playwright, sync_playwright
import os
import gradio as gr
import uuid
import time

#prompt = "Create simple Questions with simple Answers flashcards whilst including everything from the context, Don't repeat similar Questions, Don't use Questions from the context, Don't include any other text and make sure it's like this Question  Answer in tsv format: "
#prompt = "Create definition front with simple definition at the back flashcards whilst including everything from the context, Don't repeat similar Questions, Don't use Questions from the context, Don't include any other text and make sure it's like this Question       Answer in tsv format: "
prompt = "Create definition front with simple Answers flashcards whilst including everything from the context, Don't repeat similar/same Front, Don't use Questions from the context, Don't include any other text and make sure you seperate Front and answer with : like this Distributed denial-of-service:(DDoS)	An attempt to make a digital or network system unavailable by flooding it with traffic from multiple compromised systems. "

def reader(path, start_page, end_page):
    text = []
    with fitz.open(path) as pdf:
        for i in range(start_page, end_page, 4):
            text1 = pdf[i].get_text()
            text2 = ""
            if i + 1 < len(pdf):
                text2 = pdf[i + 1].get_text()
            text.append(text1 + " " + text2)
    return text

def generator(playwright: Playwright, text) -> list:
    flashcards = []
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://deepai.org/chat")
    page.wait_for_selector("iframe[title=\"SP Consent Message\"]")
    page.locator("iframe[title=\"SP Consent Message\"]").content_frame.get_by_label("Accept").click()
    page.locator("#headerLoginButton").click()
    page.get_by_role("button", name="Or login with email").click()
    page.get_by_placeholder("Enter valid email address").click()
    page.get_by_placeholder("Enter valid email address").fill("keen112@e-record.com")
    page.get_by_placeholder("Enter your password", exact=True).click()
    page.get_by_placeholder("Enter your password", exact=True).fill("keen112@e-record.com")
    page.get_by_role("button", name="Login").click()
    time.sleep(2)

    # Fill the first prompt
    first_placeholder = page.get_by_placeholder("Chat with AI...").first
    first_placeholder.fill(prompt + text[0])
    page.get_by_role("button", name="Go").click()
    time.sleep(1)
    page.wait_for_selector("button#chatSubmitButton[style*='display: block;']")
    container = page.query_selector("div.markdownContainer")
    flashcards.append(container.inner_text())

    for i in range(1, len(text)):
        # Fill the next prompts by selecting the nth placeholder
        page.get_by_placeholder("Chat with AI...").nth(i).fill(prompt + text[i])
        page.get_by_role("button", name="Go").click()
        page.wait_for_selector("button#chatSubmitButton[style*='display: block;']")
        containers = page.query_selector_all("div.markdownContainer")
        for container in containers[i:]:
            flashcards.append(container.inner_text())

    context.close()
    browser.close()
    return flashcards

def writer(flashcards, folder, text_name):
    os.makedirs(folder, exist_ok=True)
    remove_list = ['Question', 'Answer', 'Copy']
    file_name = os.path.join(folder, f'{text_name}.txt')
    written = set()
    with open(file_name, 'a', encoding='utf-8') as file:
        for flashcard in flashcards:
            cleaned_flashcard = flashcard
            for word in remove_list:
                cleaned_flashcard = cleaned_flashcard.replace(word, '')
            if cleaned_flashcard not in written:
                file.write(cleaned_flashcard + '\n')
                written.add(cleaned_flashcard)
    return file_name  # Return the filename for reading

def read_file_contents(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        return file.read()

def process_input(pdf_file, start_page, end_page, text_name):
    if not text_name:
        text_name = str(uuid.uuid4())
    
    folder = "output"

    # Validate PDF and page inputs
    try:
        with fitz.open(pdf_file.name) as pdf:
            num_pages = len(pdf)
            if start_page < 0 or end_page <= start_page or end_page > num_pages:
                return "Error: Invalid page range. Check the start and end pages.", ""

        with sync_playwright() as playwright:
            text = reader(pdf_file.name, int(start_page), int(end_page))
            flashcards = generator(playwright, text)
            file_name = writer(flashcards, folder, text_name)  # Get the file name

            contents = read_file_contents(file_name)  # Read the file contents

        return file_name, contents  # Return both the file name and contents

    except Exception as e:
        return f"Error: {str(e)}", ""

iface = gr.Interface(
    fn=process_input,
    inputs=[
        gr.File(type="filepath", label="Upload PDF"),
        gr.Number(label="Start Page"),
        gr.Number(label="End Page"),
        gr.Textbox(label="File Name (optional)")
    ],
    outputs=[
        gr.File(label="Download Flashcards"),
        gr.Textbox(label="Flashcards Contents")  # New output to show flashcard contents
    ],
    title="Flashcard Generator V2",
    description="<p style='text-align: center'>Easily create flashcards from the text in your PDF file!</p><p>1. Upload a PDF file<br>2. Specify the range of pages to extract text from<br>3. Optionally provide a custom file name for your flashcards.</p>",
    examples=[
        ["Digital T Level.pdf", 254, 260, ""],
    ]
)

iface.launch()
