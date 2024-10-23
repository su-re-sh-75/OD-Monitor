from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import re
import os
from copy import deepcopy
import shutil

'''Read files from All ODs, check if it's my OD, Track OD'''

def filter_cond(string: str) -> bool:
    words_set = frozenset(['od', 'pc', 'list', 'round', 'students', 'student', 'hall', 'shortlisted', 'shortlists', 'shortlist', 'ppt', 'test', 'interview', 'hr', 'pcs'])
    return string.lower() not in words_set and not string.isdigit()

def extract_cmp_name(string: str) -> str:
    words = string.split(" ")
    temp = []
    for word in words:
        arr = word.split("_")
        temp.extend(arr)
    words = deepcopy(temp)
    filtered_words = list(filter(filter_cond, words))
    return " ".join(filtered_words)

def extract_details_from_filename(pdf_path: str) -> tuple[str]:
    '''
    Returns full pdf name, OD date, company name, folder name
    full pdf name = filename = folder name
    '''
    rem = re.match(r'(\d{4}_\d{2}_\d{2})_([A-Za-z0-9_ &-]+)', pdf_path)
    date_part = "/".join(rem.group(1).split('_')[::-1])
    cmp_name = extract_cmp_name(rem.group(2))
    return rem.group(0), date_part, cmp_name, rem.group(0)

def delete_folder(folder: str) -> None:
    if os.path.exists(folder):
        for file_name in os.listdir(folder):
            os.remove(os.path.join(folder, file_name))
        os.rmdir(folder)
    
def create_files_and_folders() -> None:
    '''Create required folders'''
    if not os.path.exists('OD.txt'):
        with open("OD.txt", 'w') as fp:
            text = 'SNO\tCOMPANY_NAME\tDATE\tPDF NAME'
            fp.write(text)

    if not os.path.exists('checked.txt'):
        open("checked.txt", 'x')
    
    if not os.path.exists('My ODs'):
        os.mkdir('My ODs')

def find_name(filename: str, reg_no: str) -> bool:
    image = Image.open(filename)
    text = pytesseract.image_to_string(image)
    rnumpresent = re.search(reg_no, text)
    return bool(rnumpresent)

def is_checked(pdfname: str) -> bool:
    with open('checked.txt', 'r') as fp:
        text = fp.readlines()
        text = set(map(lambda x: x.strip('\n'), text))
        return pdfname in text

def process_file(pdf_path: str, filename: str, cmp_name: str, od_date: str, reg_no: str, folder_name: str) -> None:
    '''Convert pdf pages to jpegs, convert each jpeg to text and find reg num in text'''
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    pages = convert_from_path(pdf_path, poppler_path=r'C:\poppler-24.07.0\Library\bin')
    found = False
    for i, page in enumerate(pages):
        jpeg_name = os.path.join(folder_name, f"Page_{i}.jpg")
        if not os.path.exists(jpeg_name):
            page.save(jpeg_name, "JPEG")
        found = find_name(jpeg_name, reg_no)
        if found:
            # print(f"Register number is present in page {i+1} in {folder_name}.pdf")
            with open("OD.txt", 'r') as fd:
                linenum = len(fd.readlines())
            with open("OD.txt", 'a') as fp:
                text = f'\n{linenum}    {cmp_name}    {od_date}    {folder_name}.pdf'
                fp.write(text)
            shutil.copy2(pdf_path, 'My ODs')
            # print(f"Stored {cmp_name} in OD.txt")
            break
    if not found:
        pass
        # print(f"Register number is not present in {folder_name}.pdf")
        
    with open("checked.txt", 'a') as fp:
        name = f'{pdf_path.split("\\")[1]}'
        if not is_checked(name):
            fp.write(f'{name}\n')

    delete_folder(folder_name)