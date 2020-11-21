FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get -y update
RUN apt-get install -y python3.8 python3-pip unzip
RUN ln -s /usr/bin/pip3 /usr/bin/pip
RUN ln -s /usr/bin/python3.8 /usr/bin/python
RUN apt-get install -y tesseract-ocr libtesseract-dev tesseract-ocr-tam
#RUN pip install Open-Tamil==0.97 pyocr==0.7.2 PyPDF2==1.26.0 pytesseract==0.3.4 tqdm
RUN pip install pytesseract==0.3.4 PyPDF2==1.26.0 tqdm
WORKDIR /workspace
COPY . .
CMD ["python3", "create_pdf_from_zipped_folder.py", "--source_dir", "/input_folder", "--output_dir", "/output_folder"]