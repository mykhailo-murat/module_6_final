from pathlib import Path
import shutil
import sys
import file_parser
from normalize import normalize
import os

def is_empty_directory(directory):
    return not any(os.listdir(directory))

def remove_directory_contents(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            os.rmdir(dir_path)

def handle_media(file_name: Path, target_folder: Path):
    try:
        target_folder.mkdir(parents=True, exist_ok=True)
        file_name.rename(target_folder / normalize(file_name.name))
    except Exception as e:
        print(f"Error handling media file: {e}")

def handle_archive(file_name: Path, target_folder: Path):
    try:
        target_folder.mkdir(parents=True, exist_ok=True)
        folder_for_file = target_folder / normalize(file_name.stem)
        folder_for_file.mkdir(parents=True, exist_ok=True)
        shutil.unpack_archive(str(file_name.absolute()), str(folder_for_file.absolute()))
        file_name.unlink()
    except shutil.ReadError:
        folder_for_file.rmdir()
    except Exception as e:
        print(f"Error handling archive: {e}")

def main(folder: Path):
    file_parser.scan(folder)

    for file in file_parser.JPEG_IMAGES:
        handle_media(file, folder / 'IMAGES' / 'JPEG')
    for file in file_parser.JPG_IMAGES:
        handle_media(file, folder / 'IMAGES' / 'JPG')
    for file in file_parser.PNG_IMAGES:
        handle_media(file, folder / 'IMAGES' / 'PNG')
    for file in file_parser.SVG_IMAGES:
        handle_media(file, folder / 'IMAGES' / 'SVG')
    for file in file_parser.AVI_VIDEO:
        handle_media(file, folder / 'VIDEO' / 'AVI')
    for file in file_parser.MP4_VIDEO:
        handle_media(file, folder / 'VIDEO' / 'MP4')
    for file in file_parser.MOV_VIDEO:
        handle_media(file, folder / 'VIDEO' / 'MOV')
    for file in file_parser.MKV_VIDEO:
        handle_media(file, folder / 'VIDEO' / 'MKV')
    for file in file_parser.MP3_AUDIO:
        handle_media(file, folder / 'AUDIO' / 'MP3')
    for file in file_parser.OGG_AUDIO:
        handle_media(file, folder / 'AUDIO' / 'OGG')
    for file in file_parser.WAV_AUDIO:
        handle_media(file, folder / 'AUDIO' / 'WAV')
    for file in file_parser.AMR_AUDIO:
        handle_media(file, folder / 'AUDIO' / 'AMR')
    for file in file_parser.DOC_DOCUMENTS:
        handle_media(file, folder / 'DOCUMENTS' / 'DOC')
    for file in file_parser.DOCX_DOCUMENTS:
        handle_media(file, folder / 'DOCUMENTS' / 'DOCX')
    for file in file_parser.TXT_DOCUMENTS:
        handle_media(file, folder / 'DOCUMENTS' / 'TXT')
    for file in file_parser.XLSX_DOCUMENTS:
        handle_media(file, folder / 'DOCUMENTS' / 'XLSX')
    for file in file_parser.PDF_DOCUMENTS:
        handle_media(file, folder / 'DOCUMENTS' / 'PDF')
    for file in file_parser.PPTX_DOCUMENTS:
        handle_media(file, folder / 'DOCUMENTS' / 'PPTX')
    
    for file in file_parser.MY_OTHER:
        handle_media(file, folder / 'MY_OTHER')

    for file in file_parser.ARCHIVES:
        handle_archive(file, folder / 'ARCHIVES')

    for folder in file_parser.FOLDERS[::-1]:
        if is_empty_directory(folder):
            try:
                folder.rmdir()
            except OSError as e:
                print(f'Error during remove folder {folder}: {e}')
        else:
            remove_directory_contents(folder)

if __name__ == "__main__":
    folder_process = Path(sys.argv[1])
    main(folder_process.resolve())