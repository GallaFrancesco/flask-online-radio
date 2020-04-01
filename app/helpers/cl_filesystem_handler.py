# This module is respnsile for all types of filesystem changes. In particular it means:
#  
#  - it sorts audio folders [albums] to proper place
#  - it deletes empty audio folders 
  
import os, shutil, requests
from bs4 import BeautifulSoup


class Deleter():
    """ Class deleting empty audiofolders recursively bottom up. It uses the 'audio_extensions.txt' where all audio extensions are specified (this file was scrapped from wikipedia and is saved in the same folder as this script and in case it will be lost, the scrapping function will run to replace it) """

    def scrap_audio_formats_table() -> list:
        """ scrap the table form wiki containing audioformat details """
        
        data = []
        try:
            website = requests.get("https://en.wikipedia.org/wiki/Audio_file_format").text
        except Exception as e:
            print("We are offline: ", e)
        else:
            soap = BeautifulSoup(website, "html.parser")
            table_body = soap.find("tbody")
            rows = table_body.find_all("tr")
            for row in rows:
                cols = row.find_all("td")
                cols_textonly = [i.text.strip() for i in cols]
                if cols_textonly:
                    data.append(cols_textonly)
            return data


    def parse_audio_extensions(col: list) -> None:
        """ Save audio extension to a file """
        extensions = [i[0] for i in col]
        final_list = []
        for i in extensions:
            if " " not in i: 
                final_list.append(i)
            else:
                temp = i.split(", ")
                for i in temp:
                    final_list.append(i)
        app_dir = os.getcwd()
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        print("succesfully made up audio_extensions.txt file\nplease rerun the script")
        with open(r"audio_extensions.txt", "w") as f:
            for i in final_list:
                print(i, file=f)
        os.chdir(app_dir)


    def count_audiofiles(directory: str) -> int:
        """ Count audiofiles in a directory """
        filename = "audio_extensions.txt"
        try:
            with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), filename)) as f:
                extensions = set(f.read().splitlines())
        except FileNotFoundError:
            print("audio_extiensions.txt file does not exists.. trying to get one from web.. ")
            Deleter.parse_audio_extensions(Deleter.scrap_audio_formats_table())
        else:
            counter = 0
            for item in os.listdir(directory):
                if any(ext in item for ext in extensions):
                    counter += 1
                else:
                    continue
            return counter


    def delete_folders_without_audio(directory: str) -> int:
        """ Delete folders where no audio files are left, recursively from botom up """
        counter = 0
        for path, dirs, _ in os.walk(directory):
            if len(dirs) == 0 and Deleter.count_audiofiles(path) == 0:
                counter += 1
                print(f"deleting.. {path}")
                shutil.rmtree(path)
        if counter > 0:
            return Deleter.delete_folders_without_audio(directory)
        else:
            return None

class Sorter():
    """ Class for sorting audio folders in a tree structure following this pattern:
        [a/name_of_composer_starting_from_letter_a/albums...]
        [b/name_of_composer_starting_from_letter_b/albums...]
        [c/name_of_composer_starting_from_letter_c/albums...]
        etc.. """

    def sort_audiofolders(source: str, target: str) -> None:
        """ Move audio folders into correct path in alphabetical structure """
        for composer in os.listdir(source):
            os.chdir(source)
            composer_path = os.path.abspath(composer)
            os.chdir(composer_path)
            for album in os.listdir(composer_path):
                if os.path.isdir(os.path.abspath(album)):
                    album_path = os.path.abspath(album)
                    dir_path = os.path.dirname(album_path)
                    target_dir = os.path.join(target, composer[0].lower(), composer, album)
                    if os.path.exists(target_dir):
                        print(f"album '{album}' on path '{album_path}' is existing on target path, skipping..")
                        continue
                    else:
                        print(f"album '{album}' on path '{album_path}' is not existing on target path '{target_dir}', moving now.. ")
                        shutil.move(album_path, target_dir)