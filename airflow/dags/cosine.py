import math
import re
from collections import Counter

WORD = re.compile(r"\w+")

def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])
    sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
    sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)
    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

def text_to_vector(text):
    words = WORD.findall(text.upper())
    return Counter(words)

def the_nearest(data:dict, target:str):
    # return max(data, key=lambda x: get_cosine(text_to_vector(x), text_to_vector(target)))
    
    cosine_scores = [(text, get_cosine(text_to_vector(text), text_to_vector(target))) for text in data.keys()]
    best_text, best_score = max(cosine_scores, key=lambda x: x[1])
    return data[best_text], best_text, best_score

if __name__ == "__main__":
    tg = "euro 2024"
    data = {'UEFA EURO 2024 (in Germany)': 'url1', 'Copa America': 'url2', 'Africa': 'url3'}
    vector_tg = text_to_vector(tg)
    vl, tg, sc = the_nearest(data, tg)
    print(vl, tg, sc)