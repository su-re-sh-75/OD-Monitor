import store_pdfs
import track_od
import os
import re
if __name__ == '__main__':
    os.environ['PATH'] += ';C:\\Program Files\\Tesseract-OCR\\'

    need_pc = input("Do you want to check PC ODs also?[Y/N/y/n]\nchoice: ").lower() == 'y'
    store_pdfs.download_files(need_pc)

    while True:
        reg_no = input('Enter your register number: ')
        if not re.match(r'^7176(21 | 22)05(\d){3}$', reg_no):
            print("Invalid register number. Re-enter")
        else:
            break
    track_od.create_folders()
    for pdf_path in os.listdir("All ODs"):
        filename, od_date, cmp_name = track_od.extract_cmp_name(pdf_path)
        if not need_pc and 'PC' in filename.upper():
            print(f"{pdf_path} is PC OD file. So skipping.. ")
            continue
        if track_od.is_checked(pdf_path):
            print(f"{pdf_path} already checked. So skipping.. ")
            continue
        pdf_path = os.path.join("All ODs",pdf_path)
        track_od.process_file(pdf_path, filename, cmp_name, od_date, reg_no)
        track_od.delete_folder(filename)