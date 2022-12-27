import sys
from sys import argv
from pathlib import Path
import shutil
import os
import re

dict_dir_format = {
    "images": [".jpeg", ".png", ".jpg", ".svg"],
    "video": [".avi", ".mp4", ".mov", ".mkv"],
    "documents": [".doc", ".docx", ".txt", ".pdf", ".xlsx", ".pptx"],
    "music": [".mp3", ".ogg", ".wav", ".amr"],
    "archives": [".zip", ".gz", ".tar"],
    "unknown": None
}


def normalize(name: str) -> str:
    CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    LATIN_TRANSLATION = (
        "a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
        "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja")

    TRANS = {}
    for c, l in zip(CYRILLIC_SYMBOLS, LATIN_TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()
    t_name = name.translate(TRANS)
    t_name = re.sub(r'\W', '_', t_name)
    return t_name


# створимо папки
def create_target_folders(work_dir: Path):
    for i in dict_dir_format:
        if not work_dir.joinpath(i).exists():
            work_dir.joinpath(i).mkdir(i)


# видалимо пусті папки
def remove_empty(work_dir: Path):
    create_target_folders()
    for item in work_dir.glob("**/*"):
        if item.is_file():
            sort_files(item, work_dir)

        if item.is_dir() and item.name not in dict_dir_format.keys():  # !!!!!!!!!!! або list(dict_dir_format)
            if os.path.getsize(item) == 0:
                shutil.rmtree(item)
            if item.name in dict_dir_format.keys():
                continue

# сортуємо файли


def sort_files(file: Path, work_dir: Path):

    if file.suffix in dict_dir_format["images"]:
        file.replace(work_dir.joinpath(
            "images", f"{normalize(file.stem)}{file.suffix}"))

    elif file.suffix in dict_dir_format["video"]:
        file.replace(work_dir.joinpath(
            "video", f"{normalize(file.stem)}{file.suffix}"))

    elif file.suffix in dict_dir_format["documents"]:
        file.replace(work_dir.joinpath(
            "documents", f"{normalize(file.stem)}{file.suffix}"))

    elif file.suffix in dict_dir_format["music"]:
        file.replace(work_dir.joinpath(
            "music", f"{normalize(file.stem)}{file.suffix}"))

    elif file.suffix in dict_dir_format["archives"]:
        file.replace(work_dir.joinpath(
            "archives", f"{normalize(file.stem)}{file.suffix}"))
        shutil.unpack_archive(file, rf"{work_dir}\\archives")
        os.remove(file)

    else:
        file.replace(work_dir.joinpath(
            "unknown", f"{normalize(file.stem)}{file.suffix}"))


# основа
def main():

    try:
        work_dir = sys.argv[1]
    except IndexError:
        print("No parameter entered.")

    list_result = list(work_dir.iterdir())

    remove_empty(work_dir)

    for i in list_result:
        print(i, "- sorted")

    if __name__ == "__main__":
        main()
