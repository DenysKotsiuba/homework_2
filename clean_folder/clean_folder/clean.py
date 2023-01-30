import os
from pathlib import Path
import shutil
from sys import argv

FILE_TYPES = {
    'images': ('.jpeg', '.png', '.jpg', '.svg'),
    'documents': ('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'),
    'audio': ('.mp3', '.ogg', '.wav', '.amr'),
    'video': ('.avi', '.mp4', '.mov', '.mkv'),
    'archives': ('.zip', '.gz', '.tar'),

}

for key in FILE_TYPES:
    Path(argv[1]).joinpath(key).mkdir(exist_ok=True)

    image_files = []
    documents_files = []
    audio_files = []
    video_files = []
    archives_files = []
    matching_suffixes = set()
    other_suffixes = set()


def delete_empty_directories(path):

    directory_path = Path(path)

    for elem in directory_path.iterdir():

        if elem.is_dir() and not elem.name in FILE_TYPES.keys():
            delete_empty_directories(elem)
            try:
                elem.rmdir()
            except OSError:
                continue


def normalize(file_name):
    cyrirllic_symbols = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    latin_symbols = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

    trans = {}

    for c, t in zip(cyrirllic_symbols, latin_symbols):
        trans[ord(c)] = t
        trans[ord(c.upper())] = t.capitalize()

    new_file_name = file_name.translate(trans)

    for symbol in new_file_name:

        if (not ord(symbol) in range(48, 58) 
                and not ord(symbol) in range(65, 91)
                and not ord(symbol) in range(97, 122)):
            new_file_name = new_file_name.replace(symbol, '_')
    
    return new_file_name


def sort_directory(path):

    directory_path = Path(path)
    
    for elem in directory_path.iterdir():

        new_file_name = normalize(elem.stem)
        elem = elem.rename(f'{elem.parent}\\{new_file_name}{elem.suffix}')

        if elem.is_dir() and not elem.name in FILE_TYPES.keys():
            sort_directory(elem)
        elif elem.suffix in FILE_TYPES['images']:
            image_files.append(elem.name)
            matching_suffixes.add(elem.suffix)
            shutil.move(elem, f'{argv[1]}\\images')
        elif elem.suffix in FILE_TYPES['documents']:
            documents_files.append(elem.name)
            matching_suffixes.add(elem.suffix)
            shutil.move(elem, f'{argv[1]}\\documents')
        elif elem.suffix in FILE_TYPES['audio']:
            audio_files.append(elem.name)
            matching_suffixes.add(elem.suffix)
            shutil.move(elem, f'{argv[1]}\\audio')
        elif elem.suffix in FILE_TYPES['video']:
            video_files.append(elem.name)
            matching_suffixes.add(elem.suffix)
            shutil.move(elem, f'{argv[1]}\\video')
        elif elem.suffix in FILE_TYPES['archives']:
            archives_files.append(elem.name)
            matching_suffixes.add(elem.suffix)
            shutil.unpack_archive(elem, f'{argv[1]}\\archives\\{elem.stem}')
            elem.unlink()
        else:
            other_suffixes.add(elem.suffix)

    return ( 
        documents_files, 
        audio_files, 
        image_files,
        video_files,
        archives_files,
        matching_suffixes,
        other_suffixes,
    )

def clean_folder():
    sort_directory(argv[1])
    delete_empty_directories(argv[1])