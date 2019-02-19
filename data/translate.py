import pandas as pd
from googletrans import Translator
from sys import argv


def translate_data(file, src_language, dest_language):
    """Translates all the words from a csv to the dest_language and put the translation in a new column"""

    #load the csv file
    df = pd.read_csv(file, index_col=None, header=None)
    translations = []
    translator = Translator()
    #iterate on all the words to translate them
    for index, row in df.iterrows():
        word = row[0]
        translation = translator.translate(word, src=src_language, dest=dest_language).text
        translations.append(translation)

    df[df.shape[1]] = translations

    df.to_csv(file, index=None, header=None)


if __name__ == '__main__':

    #translate all the files given in argument
    files = argv[1:]
    for file in files:
        translate_data(file, "en", "fr")





