import glob
import pathlib
import argparse
import pytesseract

from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("--images_folder", help="Path to folder with images")
ap.add_argument("--output_folder", help="Path to save the output files")
ap.add_argument("--images_extension", help="extension of images eg. jpg")
args = ap.parse_args()


def image2pdf(image: str):
    pdf = pytesseract.image_to_pdf_or_hocr(image, lang='tam', extension='pdf')
    return pdf


def image2txt(image: str):
    txt = pytesseract.image_to_string(Image.open(image), lang='tam+eng')
    return txt


def save(file, path, open_protocol='w'):
    with open(path, open_protocol) as f:
        f.write(file)


save_pdf = lambda file, path: save(file, path, open_protocol='w+b')
save_txt = lambda file, path: save(file, path, open_protocol='w')


def create_sub_folder(folder: pathlib.Path, sub_folder_name: str):
    subfolder_path = folder.joinpath(sub_folder_name)
    if not subfolder_path.exists():
        subfolder_path.mkdir()
    else:
        raise FileExistsError

    return subfolder_path


def convert_images_and_save(image_files: list, output_folder: pathlib.Path, output_file_format: str):
    image_files.sort()
    assert output_file_format in ['pdf', 'txt']
    output_folder_path = create_sub_folder(output_folder, f"{output_file_format}s")

    if output_file_format == 'pdf':
        convert_function = image2pdf
        save_function = save_pdf
    elif output_file_format == 'txt':
        convert_function = image2txt
        save_function = save_txt
    else:
        raise ValueError

    for image_file in image_files:
        converted_image = convert_function(image_file)
        image_name = pathlib.Path(image_file).stem
        save_txt_file_fullpath = f"{str(output_folder_path)}/{image_name}.{output_file_format}"
        save_function(converted_image, save_txt_file_fullpath)

    return str(output_folder_path)


def combine_pdf(folder: str, output_file_name='combined'):
    from PyPDF2 import PdfFileMerger
    import glob

    folder_path = pathlib.Path(folder)
    if not folder_path.exists():
        raise FileNotFoundError

    pdfs = glob.glob(f"{folder}/*.pdf")
    if not pdfs:
        raise ValueError(f"Empty Folder: No pdfs found in the path {folder}")
    pdfs.sort()

    merger = PdfFileMerger()
    for pdf in pdfs:
        merger.append(pdf)

    output_file_name = f"{output_file_name}.pdf"
    merger.write(output_file_name)
    merger.close()

    return output_file_name


def main():
    image_filename_search = f"{args.images_folder}/*.{args.images_extension}"
    image_files = glob.glob(image_filename_search)
    pdfs_saved_path = convert_images_and_save(image_files, pathlib.Path(args.output_folder), output_file_format='pdf')
    final_pdf = combine_pdf(pdfs_saved_path)
    txts_saved_path = convert_images_and_save(image_files, pathlib.Path(args.output_folder), output_file_format='txt')


if __name__ == '__main__':
    main()