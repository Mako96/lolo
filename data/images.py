import pandas as pd

from sys import argv
import os
import glob

from google_images_download import google_images_download


def download_images(word_file):
    response = google_images_download.googleimagesdownload()
    topic = word_file.split(".")[0]
    df = pd.read_csv(word_file, index_col=None, header=None)
    words = []
    for index, row in df.iterrows():
        word = row[0]
        words.append(word)
        absolute_image_paths = response.download({"keywords": word, "limit": 1, "size": "medium",
                                                  "output_directory": "pictures", "image_directory": topic})

    path = "./pictures/" + topic + "/"
    renameFiles(path,words)

def renameFiles(path, words):
    """Renames all the downloaded files <word>.<extension>"""
    files = getfiles(path)

    for filename, word in zip(files, words):
        new_filename = word + "." + filename.split('.')[-1]
        new_filename = new_filename.replace(" ", "_")
        print(new_filename)
        os.rename(path + filename, path + new_filename)

def getfiles(dirpath):
    """Return a list  files ordered by creation date"""
    files = [s for s in os.listdir(dirpath)if os.path.isfile(os.path.join(dirpath, s))]
    files.sort(key=lambda s: os.path.getmtime(os.path.join(dirpath, s)))
    return files


if __name__ == '__main__':
    files = argv[1:]
    for file in files:
        download_images(file)
