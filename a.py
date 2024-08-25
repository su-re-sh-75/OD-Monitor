from camelot import read_pdf
p = '2024_08_20_Onebill OD STUDENTS.pdf'
p2 = '2024_07_24_MULTICOREWARE_STUDENTS_OD.pdf'
p3 = 'Rootquotient_OD_Students_HALL.pdf'
abc = read_pdf(p3)
for i in range(len(abc)):
    print(abc[i].df)