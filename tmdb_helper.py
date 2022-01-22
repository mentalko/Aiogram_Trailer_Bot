import io
import re
import requests
import numpy as np

from io import BytesIO
from PIL import Image
from config import TMDB_KEY

im1 = 'https://image.tmdb.org/t/p/original/q8jlA3Wc1Z987hNKRFA44g5OugC.jpg'
im2 = 'https://image.tmdb.org/t/p/original/8Fuk8FBxSefx3CunaU4OKnqtlbM.jpg'
im3 = 'https://image.tmdb.org/t/p/original/q8jlA3Wc1Z987hNKRFA44g5OugC.jpg'
# im1 = 'https://image.tmdb.org/t/p/original/wWt4JYXTg5Wr3xBW2phBrMKgp3x.jpg'
# im2 = 'https://image.tmdb.org/t/p/original/mtqqD00vB4PGRt20gWtGqFhrkd0.jpg'
# im3 = 'https://image.tmdb.org/t/p/original/nlr2oxuYsHXt0wdtmzaOuVBoNC0.jpg'

def get_poster_tmdb(movie_titles):
    url_posters = []
    url_tmdb = 'https://api.themoviedb.org/3/search/movie?api_key='+ TMDB_KEY
    
    
    for title in movie_titles:
        year = None
        if re.search(r'\s+\((\d+)\)', title):
            title, year = re.split(r'\s+\((\d+)\)', title)[:2]
            
        params = [('query', title), ('year', year) ]
        response = requests.get(url_tmdb, params=params)
        json_data = response.json()
        try:
            poster_url = "https://image.tmdb.org/t/p/original%s" % json_data["results"][0]["poster_path"] 
            url_posters.append(poster_url)
        except:
            pass
    return url_posters

def concatenate_images(url_list):
    try:
        imgs = []
        for url in url_list:
            imgs.append( Image.open(BytesIO(requests.get(url).content)) )
        # pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
        min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]
        imgs_comb = np.hstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )
        
        bytes = Image.fromarray( imgs_comb)
        bytes.save('concat.jpg', format='JPEG')
        
        
    except Exception as e:
        print(e)


def get_large_poster(movie_titles):
    poster_urls = get_poster_tmdb(movie_titles)
    return concatenate_images(poster_urls)

# concatenate_images([im1, im2, im3]).save('concat.jpg')
# poster = get_large_poster(['It takes two (1995)', 'Trading places (1983)', 'The change-up']).save('concat.jpg')