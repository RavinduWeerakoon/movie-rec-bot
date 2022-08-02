import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

df = pd.read_csv('data.csv')
df['combined_features'] = df['keywords']+" "+df['cast']+" "+df['genres']+" "+df['director']

cv = CountVectorizer()
count_matrix = cv.fit_transform(df['combined_features'].fillna(''))
cosine_sim = cosine_similarity(count_matrix)


def get_similar(movie_index):

    movie_index = int(movie_index)

    similar_movies = list(enumerate(cosine_sim[movie_index]))
    sorted_similar_movies = sorted(similar_movies, key = lambda x:x[1], reverse = True)

    s = sorted_similar_movies[1:6]
    index = [x for x,y in s]
    return df.iloc[index]['title'].to_dict()



def possible_results(tag):
    results = df[df['title'].str.contains(str(tag),flags=re.IGNORECASE)]
    return results['title'].to_dict()

def get_data(index):
    data = df.iloc[int(index)].to_dict()

    title = data['title']

    genre = data.get('genres')
    text = (
        f"{title}\n"
        f"genre: {genre}"
    )
    return text