import re
from pathlib import Path
import shutil
import sys
import os

JPEG_IMAGES = []
JPG_IMAGES = []
PNG_IMAGES = []
SVG_IMAGES = []
AVI_VIDEO = []
MP4_VIDEO = []
MKV_VIDEO = []
MOV_VIDEO = []
DOC_DOCUMENTS = []
DOCX_DOCUMENTS = []
PDF_DOCUMENTS = []
TXT_DOCUMENTS = []
XLSX_DOCUMENTS = []
PPTX_DOCUMENTS = []
MP3_AUDIO = []
OGG_AUDIO = []
WAV_AUDIO = []
AMR_AUDIO = []
MY_OTHER = []
ARCHIVES = []

REGISTER_EXTENSION = {
    'JPEG': JPEG_IMAGES,
    'JPG': JPG_IMAGES,
    'PNG': PNG_IMAGES,
    'SVG': SVG_IMAGES,
    'AVI': AVI_VIDEO,
    'MP4': MP4_VIDEO,
    'MKV': MKV_VIDEO,
    'MOV': MOV_VIDEO,
    'DOC': DOC_DOCUMENTS,
    'DOCX': DOCX_DOCUMENTS,
    'PDF': PDF_DOCUMENTS,
    'TXT': TXT_DOCUMENTS,
    'XLSX': XLSX_DOCUMENTS,
    'PPTX': PPTX_DOCUMENTS,
    'MP3': MP3_AUDIO,
    'OGG': OGG_AUDIO,
    'WAV': WAV_AUDIO,
    'AMR': AMR_AUDIO,
    'ZIP': ARCHIVES,
    'GZ': ARCHIVES,
    'TAR': ARCHIVES,
}

FOLDERS = []
EXTENSIONS = set()
UNKNOWN = set()


def get_extension(name: str) -> str:
    return Path(name).suffix[1:].upper()  # suffix[1:] -> .jpg -> jpg


def scan(folder: Path):
    for item in folder.iterdir():
        # Робота з папкою
        if item.is_dir():  # перевіряємо чи обєкт папка
            if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'MY_OTHER'):
                FOLDERS.append(item)
                scan(item)
            continue
        # Робота з файлом
        extension = get_extension(item.name)  # беремо розширення файлу
        full_name = folder / item.name  # беремо повний шлях до файлу
        if not extension:
            MY_OTHER.append(full_name)
        else:
            try:
                ext_reg = REGISTER_EXTENSION[extension]
                ext_reg.append(full_name)
                EXTENSIONS.add(extension)
            except KeyError:
                UNKNOWN.add(extension)  # .mp4, .mov, .avi
                MY_OTHER.append(full_name)


def is_empty_directory(directory):
    return not any(os.listdir(directory))

CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")

TRANS = dict()

for cyrillic, latin in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(cyrillic)] = latin
    TRANS[ord(cyrillic.upper())] = latin.upper()


def normalize(name: str) -> str:
    filename = name.split(".")[0]
    extension = name.split(".")[-1]
    translate_name = re.sub(r'\W', '_', filename.translate(TRANS))
    return translate_name + '.' + extension


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
    scan(folder)

    for file in JPEG_IMAGES:
        handle_media(file, folder / 'IMAGES' / 'JPEG')
    for file in JPG_IMAGES:
        handle_media(file, folder / 'IMAGES' / 'JPG')
    for file in PNG_IMAGES:
        handle_media(file, folder / 'IMAGES' / 'PNG')
    for file in SVG_IMAGES:
        handle_media(file, folder / 'IMAGES' / 'SVG')
    for file in AVI_VIDEO:
        handle_media(file, folder / 'VIDEO' / 'AVI')
    for file in MP4_VIDEO:
        handle_media(file, folder / 'VIDEO' / 'MP4')
    for file in MOV_VIDEO:
        handle_media(file, folder / 'VIDEO' / 'MOV')
    for file in MKV_VIDEO:
        handle_media(file, folder / 'VIDEO' / 'MKV')
    for file in MP3_AUDIO:
        handle_media(file, folder / 'AUDIO' / 'MP3')
    for file in OGG_AUDIO:
        handle_media(file, folder / 'AUDIO' / 'OGG')
    for file in WAV_AUDIO:
        handle_media(file, folder / 'AUDIO' / 'WAV')
    for file in AMR_AUDIO:
        handle_media(file, folder / 'AUDIO' / 'AMR')
    for file in DOC_DOCUMENTS:
        handle_media(file, folder / 'DOCUMENTS' / 'DOC')
    for file in DOCX_DOCUMENTS:
        handle_media(file, folder / 'DOCUMENTS' / 'DOCX')
    for file in TXT_DOCUMENTS:
        handle_media(file, folder / 'DOCUMENTS' / 'TXT')
    for file in XLSX_DOCUMENTS:
        handle_media(file, folder / 'DOCUMENTS' / 'XLSX')
    for file in PDF_DOCUMENTS:
        handle_media(file, folder / 'DOCUMENTS' / 'PDF')
    for file in PPTX_DOCUMENTS:
        handle_media(file, folder / 'DOCUMENTS' / 'PPTX')

    for file in MY_OTHER:
        handle_media(file, folder / 'MY_OTHER')

    for file in ARCHIVES:
        handle_archive(file, folder / 'ARCHIVES')

    for folder in FOLDERS[::-1]:
        if is_empty_directory(folder):
            try:
                folder.rmdir()
            except OSError as e:
                print(f'Error during remove folder {folder}: {e}')
        else:
            remove_directory_contents(folder)


def start():
    if sys.argv[1]:
        folder_process = Path(sys.argv[1])
        main(folder_process)
