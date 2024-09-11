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
        if not re.match(r'^7176(21|22)05(\d){3}$', reg_no):
            print("Invalid register number. Re-enter")
        else:
            break
    track_od.create_files_and_folders()
    for pdf_name in os.listdir("All ODs"):
        filename, od_date, cmp_name, folder_name = track_od.extract_details_from_filename(pdf_name)
        if not need_pc and 'PC' in filename.upper():
            print(f"{pdf_name} is PC OD file. So skipped.. ")
            continue
        if track_od.is_checked(pdf_name):
            print(f"{pdf_name} is already checked. So skipped.. ")
            continue
        pdf_path = os.path.join("All ODs",pdf_name)
        print("Processing:", pdf_name)
        track_od.process_file(pdf_path, filename, cmp_name, od_date, '71762105055', folder_name)
    