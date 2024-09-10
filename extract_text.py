from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import re
import os

def extract_cmp_name(pdf_path):
    rem = re.match(r'(\d{4}_\d{2}_\d{2})_([A-Za-z0-9]+)', pdf_path)
    date_part = "/".join(rem.group(1).split('_')[::-1])
    return rem.group(0), date_part, rem.group(2)

def delete_folder(folder):
    if os.path.exists(folder):
        for file_name in os.listdir(folder):
            os.remove(os.path.join(folder, file_name))
        os.rmdir(folder)
    
def create_folders():
    '''Create required folders'''
    if not os.path.isfile('OD.txt'):
        with open("OD.txt", 'w') as fp:
            text = 'SNO\tCOMPANY_NAME\tDATE\tSTORED_DATE'
            fp.write(text)

    if not os.path.isfile('checked.txt'):
        open("checked.txt", 'x')

def is_checked(pdfname):
    with open('checked.txt', 'r') as fp:
        text = fp.readlines()
        text = list(map(lambda x: x.strip('\n'), text))
        return pdfname in text

def process_file(pdf_path, filename, cmp_name, od_date):
    '''Convert pdf pages to jpegs, convert each jpeg to text and find reg num in text'''
    pages = convert_from_path(pdf_path, poppler_path=r'C:\poppler-24.07.0\Library\bin')
    if not os.path.exists(filename):
        os.mkdir(filename)
    found = False
    for i, page in enumerate(pages):
        jpeg_name = os.path.join(filename, f"Page_{i}.jpg")
        if not os.path.exists(jpeg_name):
            page.save(jpeg_name, "JPEG")
            print(f"Saved: {jpeg_name}")
        found = find_name(jpeg_name)
        if found:
            print(f"Reg. No is present in page {i+1} in {filename}")
            with open("OD.txt", 'r') as fd:
                linenum = len(fd.readlines())
            with open("OD.txt", 'a') as fp:
                text = f'\n{linenum}\t{cmp_name}\t{od_date}'
                fp.write(text)
            break
    if not found:
        print(f"Reg. No is not present in {filename}")
        
    with open("checked.txt", 'a') as fp:
        name = f'{pdf_path.split("\\")[1]}'
        if not is_checked(name):
            fp.write(f'{name}\n')

    delete_folder(filename)

def find_name(filename):
    image = Image.open(filename)
    text = pytesseract.image_to_string(image)
    rnumpresent = re.search(r'71762105055', text)
    if rnumpresent:
        return True
    else:
        return False

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
    # filename = without extension .pdf
    # pdf_path = with extension .pdf
    os.environ['PATH'] += ';C:\\Program Files\\Tesseract-OCR\\'
    create_folders()
    for pdf_path in os.listdir("All ODs"):
        filename, od_date, cmp_name = extract_cmp_name(pdf_path)
        if 'PC' in filename.upper():
            print(f"{pdf_path} is PC OD file. So skipping.. ")
            continue
        if is_checked(pdf_path):
            print(f"{pdf_path} already checked. So skipping.. ")
            continue
        pdf_path = os.path.join("All ODs",pdf_path)
        process_file(pdf_path, filename, cmp_name, od_date)
        delete_folder(filename)