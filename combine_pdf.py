from PyPDF2 import PdfFileMerger
import glob

pdfs = glob.glob('text_files/*.pdf')
pdfs.sort()
# pdfs = ['file1.pdf', 'file2.pdf', 'file3.pdf', 'file4.pdf']

merger = PdfFileMerger()

for pdf in pdfs:
    merger.append(pdf)

merger.write("result.pdf")
merger.close()