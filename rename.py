import glob
import os
from pathlib import Path

book = "/home/senthil/tamil_digital_books_library/தமிழண்ணல் தமிழுக்குத் தந்த சீர்வரிசை"
book_name = Path(book).stem
book_name = book_name.replace(" ", "_")
print(book_name)
images = glob.glob(f"{book}/*.jpg")
for image_full_path in images:
    image_name = Path(image_full_path).stem
    page_number = int(image_name.replace("image", ""))
    new_image_name = f"{book_name}_{page_number:04d}"
    new_image_full_path = image_full_path.replace(image_name, new_image_name)
    os.rename(image_full_path, new_image_full_path)
