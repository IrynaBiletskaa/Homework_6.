
from sys import argv
from pathlib import Path
import re
import os
import shutil
from zipfile import ZipFile

work_dir = Path(sys.argv[1])
counter = 0


# зробимо фцію якщо є потрібні папки куди складати файли то пропускаємо , якщо нема - створюємо
# for i in folders:
#     if not work_dir.joinpath(i).exists():
#         work_dir.joinpath(i).mkdir()

dict_dir_format = {
    "Images": [".jpeg", ".png", ".jpg", ".svg"],
    "Video": [".avi", ".mp4", ".mov", ".mkv"],
    "Documents": [".doc", ".docx", ".txt", ".pdf", ".xlsx", ".pptx"],
    "Music": [".mp3", ".ogg", ".wav", ".amr"],
    "Archieves": [".zip", ".gz", ".tar"],
    "Unknown": None
} 
# нормалізуємо
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


# створюмо список зі всіма файлами

file_list = []
for  item in work_dir.glob("**/*"):
    if item.is_file():
        file_list.append(item)


#створимо папки для сортування
# def create_folder():    
#     for name in dict_dir_format.keys():
#         if os.path.exists(f"{work_dir}\\{name}"):
#             continue
#         else:
#             os.mkdir(f"{work_dir}\\{name}")
# -------------------------------------------------
# def create_target_folders(path: Path):
#     for i in dict_dir_format:
#         if not work_dir.joinpath(i).exists():
#             work_dir.joinpath(i).mkdir(i)
# print("Target folders are created")

#створимо папки та розкладемо файли по ним
def sort_files(file_list):
    for item in file_list:
        name, ext = item.stem, item.suffix
        global counter
        counter += 1

        if ext in dict_dir_format['Images']:
            new_foulder = os.path.join(work_dir, 'Images')
            shutil.move(item, new_foulder)
        
        elif ext in dict_dir_format['Video']:
            new_foulder = os.path.join(work_dir, 'Video')
            shutil.move(item, new_foulder)

        elif ext in dict_dir_format['Documents']:
            new_foulder = os.path.join(work_dir, 'Documents')
            shutil.move(item, new_foulder)

        elif ext in dict_dir_format['Music']:
            new_foulder = os.path.join(work_dir, 'Music')
            shutil.move(item, new_foulder)

        elif ext in dict_dir_format['Archives']:
            new_foulder = os.path.join(work_dir, 'Archives')
            with ZipFile(item, 'r') as zip_file:
                zip_file.extractall(new_foulder)
      

        else:
            new_foulder = os.path.join(work_dir, 'Unknown')
            shutil.move(item, new_foulder)






# def sort_files(path_file):
#     for  item in work_dir.glob("**/*"):
#         if item.is_file():
#             sort_files(item)
#         else:
#             sort_folder(item)




# def sort_func(work_dir):
    
#     for file in work_dir.iterdir():
#         if file.is_file():
#             for suff in dict_dir_format.value:
#                 if file.suffix.lower() == suff:
#                     dir_img = work_dir / suff
#                     dir_img.mkdir(exist_ok=True)
#                     file.rename(dir_img.joinpath(file.name))