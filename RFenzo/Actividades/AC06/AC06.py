from datetime import datetime as dt
from functools import reduce

def set_id():
    i = 0
    while True:
        yield i
        i+=1

class Cast:
    def __init__(self, movie_title, name, character):
        self.name = name
        self.movie = movie_title
        self.character = character


class Movie:
    get_id = set_id()

    def __init__(self, idpelicula,title, rating, release, *args):
        self.id = next(Movie.get_id)
        self.title = title
        self.rating = float(rating)
        self.idpelicula = idpelicula
        self.release = dt.strptime(release, '%Y-%m-%d')  # 2015-03-04
        self.genres = [x for x in args]

def popular(valor):
    return list(filter(lambda x: float(x.rating) >valor, peliculas))

def with_genres(n):
    return list(filter(lambda x: len(x.genres) >= n, peliculas))

def tops_of_genre(genre):
    return sorted([x for x in peliculas if genre in x.genres],key= lambda x: float(x.rating),reverse= True)[:10]

def actor_rating(actor):
    peliculas_actor = [y.movie for y in artistas if y.name == actor]
    largo = len(peliculas_actor)
    suma = reduce(lambda x,y: x + y, [x.rating for x in peliculas if x.title in peliculas_actor])
    return suma/largo

def compare_actors(actor1,actor2):
    rat1 = actor_rating(actor1)
    rat2 = actor_rating(actor2)
    return [actor1 if rat1 >rat2 else actor2][0]

def movies_of(actor):
    return [(y.movie,y.character) for y in artistas if y.name == actor]

def from_year(ano):
    return [x for x in peliculas if x.release.year  == ano]

if __name__ == "__main__":
    with open('movies.txt', 'r') as f:
        peliculas = [Movie(*line.replace('\n','').split(',')) for line in f]
    with open('cast.txt', 'r') as f:
        artistas = [Cast(*line.replace('\n','').split(',')) for line in f]

print('-'*40)
print('popular 6')
print('-'*40)
for j in popular(6):
    print(j.title)
print('-'*40)
print('with_genres 3')
print('-'*40)
for j in with_genres(3):
    print(j.title)
print('-'*40)
print('tops_of_genres Mystery')
print('-'*40)
for j in tops_of_genre('Mystery'):
    print(j.title)
print('-'*40)
print('actor_rating Kaley Cuoco')
print('-'*40)
print(actor_rating('Kaley Cuoco'))
print('-'*40)
print('compare_actors Kaley Cuoco, Hugh Jackman')
print('-'*40)
print(compare_actors('Kaley Cuoco','Hugh Jackman'))
print('-'*40)
print('movies_of Hugh Jackman')
print('-'*40)
for j in movies_of('Hugh Jackman'):
    print(j)
print('-'*40)
print('from_year 2016')
print('-'*40)
for j in from_year(2016):
    print(j.title)
print('-'*40)
