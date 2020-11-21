import glob
import pathlib
import argparse
import pytesseract

from PIL import Image
from tqdm import tqdm

ap = argparse.ArgumentParser()
ap.add_argument("--images_folder", help="Path to folder with images")
ap.add_argument("--output_folder", help="Path to save the output files")
ap.add_argument("--images_extension", default='jpg', help="extension of images eg. jpg")


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

    for i, image_file in enumerate(tqdm(image_files)):
        converted_image = convert_function(image_file)
        image_name = pathlib.Path(image_file).stem
        save_txt_file_fullpath = f"{str(output_folder_path)}/{image_name}.{output_file_format}"
        save_function(converted_image, save_txt_file_fullpath)
        # print(f"Saving {i}/{len(image_files)} -> {image_name}.{output_file_format}")

    return str(output_folder_path)


def combine_pdf(folder: str, output_folder: str, output_file_name='combined'):
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

    output_file_name = pathlib.Path(output_folder).joinpath(f"{output_file_name}.pdf")
    merger.write(str(output_file_name))
    merger.close()

    return output_file_name


def create_pdf_from_folder(images_folder, output_folder, images_extension='jpg', txt_files=True):
    image_filename_search = f"{images_folder}/*.{images_extension}"
    image_files = glob.glob(image_filename_search)
    if len(image_files) == 0:
        raise ValueError(f"No Images Found in {images_folder}")
    print(f"Found {len(image_files)} {images_extension} images in {images_folder}")
    pdfs_saved_path = convert_images_and_save(image_files, pathlib.Path(output_folder), output_file_format='pdf')
    print(f'PDF equivalent of images saved in {pdfs_saved_path}')
    final_pdf = combine_pdf(pdfs_saved_path, output_folder=output_folder, output_file_name=pathlib.Path(images_folder).stem)
    print(f'Final single searchable pdf is saved at {final_pdf}')
    if txt_files:
        txts_saved_path = convert_images_and_save(image_files, pathlib.Path(output_folder), output_file_format='txt')
        print(f"The text extracted from images are saved at {txts_saved_path}")


if __name__ == '__main__':
    args = ap.parse_args()
    images_folder = args.images_folder
    output_folder = args.output_folder
    if output_folder is None:
        output_folder = images_folder
    images_extension = args.images_extension
    create_pdf_from_folder(images_folder, output_folder, images_extension)
