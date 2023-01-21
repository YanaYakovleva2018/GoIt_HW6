from pathlib import Path
import collections
from sort import file_sort

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
    path =r'/Users/yanayakovlieva/Desktop/just_folder'
    fold = Path(path)
    main(path)
  
       
      
