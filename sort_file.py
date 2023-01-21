from pathlib import Path
import collections
import shutil
from pathlib import Path
import random
import string

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ?<>,!@#[]№$%^&*()-=; "
LATIN_SYMBOLS = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_","_", "_")
TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, LATIN_SYMBOLS):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()

dict = {
    "documents": [".doc", ".docx", ".xlsx", ".txt", ".pdf", ".pptx"],
    "audio": [".mp3", ".ogg", ".wav", ".amr"],
    "video": [".avi", ".mp4", ".mov", ".mkv"],
    "images": [".jpeg", ".png", ".jpg", ".svg"],
    "archives": [".zip", ".gz", ".tar"],
}

def unpack(archive_path, path_to_unpack): #unpacking archives
    return shutil.unpack_archive(archive_path, path_to_unpack)

def file_ex(i, fl): #the function checks if a file with this name already exists.
    if i in fl.iterdir():
        add = ""
        for _ in range(3):
            char = random.choice(string.ascii_letters + string.digits)
            add += str(char)
        name = i.resolve().stem + f"({add})" + i.suffix
        file_path = Path(fl, name)
        return file_path
    return i

def fold_create(i, fold): #check if the necessary folder exists, if not - create it
    if fold.exists():
        folder_sort(i, fold)
    else:
        Path(fold).mkdir() 
        folder_sort(i, fold)

def folder_sort(i, dr):#changes the name of the file and moves it to the required folder.
    latin_name = normalize(i.name)  
    new_file = Path(dr, latin_name)  
    file_path = file_ex(new_file, dr)   
    i.replace(file_path)  

def file_sort(path): #Checks each folder and file by their extension, organizes file sorting, and changes their names
    global fold 
    p = Path(path)
    for _ in range(2):
        for i in p.iterdir():
            if i.name in ("documents", "audio", "video", "images", "archives", "other"): 
                continue
            if i.is_file(): #sorting for files
                flag = False
                for f, suf in dict.items():
                    if i.suffix.lower() in suf:
                        dr = Path(fold, f)
                        fold_create(i, dr)
                        flag = True  
                    else:
                        continue
                if not flag: 
                    dr = Path(fold, "other")
                    fold_create(i, dr)
            elif i.is_dir(): #operations for folders
                if len(list(i.iterdir())) != 0:
                    file_sort(i)  #if folder is not empty - recursively run the function in it
                else:
                    shutil.rmtree(i)  ## if  folder is empty - delete it
        for a in p.iterdir(): #in this cycle we unpack the archives
            if a.name == "archives" and len(list(a.iterdir())) != 0:
                for arch in a.iterdir():
                    if arch.is_file() and arch.suffix in (".zip", ".gz", ".tar"):
                        dir_name = arch.resolve().stem  
                        path_to_unpack = Path(fold, "archives", dir_name)
                        shutil.unpack_archive(arch, path_to_unpack)
                    else:
                        continue    


def normalize(name): #replace Cyrillic characters with Latin 
    global TRANS
    new_name = name.translate(TRANS)
    return new_name

def main(path):
    file_sort(path)
    p = Path(path)
    # Output of results
    result_dict = collections.defaultdict(list)
    for item in p.iterdir():
        if item.is_dir():
            for file in item.iterdir():
                if file.is_file():
                    result_dict[item.name].append(file.suffix)
    
    for key, value in result_dict.items():
        k, a, b = key, len(value), "".join(set(value))
        print("Name folder: ", k)
        print("Number of elements: ", a)
        print( "Extensions: ", b)

if __name__ == "__main__":
    path = input('Path to the fold:') #r'/Users/yanayakovlieva/Desktop/just_folder'
    fold = Path(path)
    main(path)
  
       
      
