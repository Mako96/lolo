import pandas as pd
from googletrans import Translator
from sys import argv


LANGUAGES_TO_TRANSLATE = ["de", "es"]

def translate_data(file):
    """Translates all the words from a csv in a new column """

    #load the csv file
    df = pd.read_csv(file, index_col=None, header=0)
    for lang in LANGUAGES_TO_TRANSLATE:
        translator = Translator()
        translations = []
        #iterate on all the words to translate them
        for index, row in df.iterrows():
            word = row[0]
            translation = translator.translate(word, src="en", dest=lang).text
            translations.append(translation)

        df[lang] = translations

    df.to_csv(file, index=None, header=0)


if __name__ == '__main__':

    #translate all the files given in argument
    files = argv[1:]
    for file in files:
        translate_data(file)






