Tamil_digibooks project is used to convert the images of a tamil book 
into a text file and/or searchable pdf using tessaract. 

#Setup

## Docker

Install docker in Windows/Linux. 

After installation of Docker, pull the tamil_img2pdf docker from docker hub by executing the
following command in terminal (Linux) or Command Prompt (Window)

```commandline
docker pull docker.io/sksenthil1/tamil_img2pdf:latest
```

## Input

Input folder should have the jpeg image of the tamil book pages. 

```
Input_folder
    |
    | -- Tamilbook_1
            |--page_1.jpg
            |--page_2.jpg
            | .
            | .
            |--page_n.jpg
    | -- Tamilbook_2
    | .
    | . 
    | -- Tamilbook_n
```
**NOTE**
* The input folder should have at least one book folder
* The name of the book and pages should be written in english
* The books can also be in the format of zipped folders

    ```
    Input_folder
        |
        | -- Tamilbook_1.zip
        | -- Tamilbook_2.zip
        | .
        | . 
        | -- Tamilbook_n.zip
    ```
  
#Running the script
If the input file have multiple tamil_book folders
```commandline
docker run -it --rm -v <path/to/input/image/folder>:/input_folder -v <path/to/output/empty/folder>:/output_folder --entrypoint "python" docker.io/sksenthil1/tamil_img2pdf:latest create_pdf_from_multiple_folders.py
```

If the input file have multiple zipped tamil_book folders, add `--zipped` to the above command at the end
```commandline
docker run -it --rm -v <path/to/input/image/folder>:/input_folder -v <path/to/output/empty/folder>:/output_folder --entrypoint "python" docker.io/sksenthil1/tamil_img2pdf:latest create_pdf_from_multiple_folders.py --zipped
```

Running the above two commands will generate output folder of structure

```
Output_folder
    |
    | -- Tamilbook_1
    |       |- pdfs
    |       |   |--page_1.pdf
    |       |   |--page_2.pdf
    |       |   | .
    |       |   | .
    |       |   |--page_n.pdf
    |       |- txts
    |       |   |--page_1.txt
    |       |   |--page_2.txt
    |       |   | .
    |       |   | .
    |       |   |--page_n.txt
    |       |-Tamilbook.pdf
    | -- Tamilbook_2
    | .
    | . 
    | -- Tamilbook_n
```

If only one book needs to be converted then,
```commandline
docker run -it --rm -v <path/to/input/image/folder>:/input_folder -v <path/to/output/empty/folder>:/output_folder --entrypoint "python" docker.io/sksenthil1/tamil_img2pdf:latest create_pdf_from_folder.py
```
Running the above command will generate
```
Output_folder
    |- pdfs
    |   |--page_1.pdf
    |   |--page_2.pdf
    |   | .
    |   | .
    |   |--page_n.pdf
    |- txts
    |   |--page_1.txt
    |   |--page_2.txt
    |   | .
    |   | .
    |   |--page_n.txt
    |-Output_folder.pdf
```
