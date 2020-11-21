import pathlib

import argparse
import prepare
import create_pdf_from_folder


ap = argparse.ArgumentParser()
ap.add_argument("--source_dir", required=True)
ap.add_argument("--output_dir", required=False)


def create_new_output_folder(input_folder, output_dir):
    book_name = pathlib.Path(input_folder).stem
    op_dir = pathlib.Path(output_dir).joinpath(book_name)
    op_dir.mkdir()
    return str(op_dir)


def process_source_dir(source_dir, output_dir):
    unzipped_folders = prepare.unzip_files_in_a_dir(source_dir)

    for folder in unzipped_folders:
        f = pathlib.Path(folder)
        images_folder = f.joinpath(f.stem)
        output_folder = create_new_output_folder(images_folder, output_dir)
        create_pdf_from_folder.create_pdf_from_folder(images_folder=str(images_folder), output_folder=output_folder)


if __name__ == '__main__':
    args = ap.parse_args()
    if args.output_dir is None:
        output_dir = args.source_dir
    else:
        output_dir = args.output_dir
    process_source_dir(args.source_dir, output_dir)
