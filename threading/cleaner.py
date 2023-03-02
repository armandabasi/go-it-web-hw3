from threading import Thread, RLock
from shutil import copyfile
from pathlib import Path
import re
import logging
import argparse

parser = argparse.ArgumentParser(description="The program sorts your folder by folder depending on the file extension")
parser.add_argument('-s', '--source', help="Source folder", required=True)
parser.add_argument('-o', '--output', default='Sorted_file')
args = vars(parser.parse_args())
output_folder = Path(args.get('output'))
start_folder = Path(args.get('source'))

folders = []


def normalize(name):
    """Функція робить транслітерацію строки"""
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

    TRANS = {}

    for c, t in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = t
        TRANS[ord(c.upper())] = t.upper()

    return re.sub(r'\W', '_', name.translate(TRANS))


def normalize_file(file):
    """Функція виконує транслітерацію файлу"""
    title, extension = Path(file).name, Path(file).suffix
    return normalize(re.sub(extension, '', title)) + extension


def find_right_folder(extension):
    """Функція повертає папку відповідно до розширення файлу"""
    TYPES = {
        "imeges": ["JPEG", "PNG", "JPG", "SVG"],
        "video": ["AVI", "MP4", "MOV", "MKV"],
        "documents": ["DOC", "DOCX", "TXT", "PDF", "XLSX", "PPTX"],
        "audio": ["MP3", "OGG", "WAV", "AMR"],
        "archives": ["ZIP", "GZ", "TAR"]
        }
    for key, value in TYPES.items():
        for val in value:
            if val == extension or val == extension.upper():
                return key
    return "other"


def folder_search(path: Path):
    """Функція виконує пошук всіх папок в папці"""
    for el in path.iterdir():
        if el.is_dir():
            folders.append(el)
            folder_search(el)


def sort_file(path: Path):
    """Функція копіює файли в нову папку відповідно до типу файлу"""
    for el in path.iterdir():
        if el.is_file():
            extension = el.suffix[1:]
            new_folder = output_folder/find_right_folder(extension)
            try:
                new_folder.mkdir(exist_ok=True, parents=True)
                copyfile(el, new_folder / normalize_file(el.name))

            except OSError as e:
                logging.error(e)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(threadName)s %(message)s")

    folders.append(start_folder)
    folder_search(start_folder)
    threads = []
    for folder in folders:
        th = Thread(target=sort_file, args=(folder, ))
        th.start()
        threads.append(th)

    [th.join() for th in threads]
    print(f"Finished, you can delete {start_folder} folder")
