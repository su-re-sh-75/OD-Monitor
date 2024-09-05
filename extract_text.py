from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import re
import os

pdf_path = r"2024_07_29_Rootquotient_OD_Students_HALL.pdf"

def extract_cmp_name(pdf_path):
    rem = re.match(r'(\d{4}_\d{2}_\d{2})_([A-Za-z0-9]+)', pdf_path)
    return rem.group(0), rem.group(1), rem.group(2)
    
def convert_pdf_to_images(pdf_path):
    pages = convert_from_path(pdf_path, poppler_path=r'C:\poppler-24.07.0\Library\bin')
    filename, od_date, cmp_name = extract_cmp_name(pdf_path)
    for i, page in enumerate(pages):
        page.save(f"{filename}_{i}.jpg", "JPEG")
        print(f"Saved: {filename}_{i}.jpg")
    return len(pages)

def perform_ocr_on_images(num_pages, filename):
    for i in range(num_pages):
        image_path = f"{filename}_{i}.jpg"
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        with open(f'extract_{filename}_{i}.txt', 'w') as fd:
            fd.write(text)
        print(f"Page {i + 1} written to extract_{filename}_{i}.txt")
        

def store_text(num_pages):
    '''Unused'''
    combined_text = ""
    for i in range(num_pages):
        image_path = f"page_{i}.jpg"
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        combined_text += text + "\n"
        with open("extracted_text.txt", "w") as f:
            f.write(combined_text)
        print("Extraction complete. Text saved to 'extracted_text.txt'")


if __name__ == '__main__':
    os.environ['PATH'] += ';C:\\Program Files\\Tesseract-OCR\\'
    filename, od_date, cmp_name = extract_cmp_name(pdf_path)
    # print("Filename: ", filename)
    pages_cnt = convert_pdf_to_images(pdf_path)
    perform_ocr_on_images(pages_cnt, filename)

          