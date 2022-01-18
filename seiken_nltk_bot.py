import numpy as np
import nltk
#nltk.download('punkt')
import numpy as np

from nltk.stem import SnowballStemmer

def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s


stemmer = SnowballStemmer('spanish')


def tokenize(frase):
    return nltk.word_tokenize(frase)


def stem(palabra):
    return normalize(stemmer.stem(palabra.lower()))


def bag_of_words(tokenized_sentence, words):
    sentence_words = [stem(word) for word in tokenized_sentence]
    bag = np.zeros(len(words), dtype=np.float32)
    for idx, w in enumerate(words):
        if w in sentence_words: 
            bag[idx] = 1

    return bag

def calorias():
    peso = int(input("Ingresa tu peso: "))
    edad = int(input("Ingresa tu edad: "))
    altura = int(input("Ingresa tu altura: "))

    calorias = peso * edad * altura 

    print(f"Tus calorias diarias son {calorias}")

# sentence = ["hola", "como", "estas", "tu"]
# palabras_totales = ["hola", "como", "estas", "tu", "chau", "gracias", "bien"]
# bog = bag_of_words(sentence,palabras_totales)

# print(bog)
    



# frase = "Hola bro cómo estas"

# print(tokenize(frase))

# palabras = ["Universidad", "Unívérso", "universos"]

# palabras_stemed = [stem(palabra) for palabra in palabras]
# print(palabras_stemed)