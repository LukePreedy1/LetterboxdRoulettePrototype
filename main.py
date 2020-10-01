from random import randint
import datetime
from bs4 import BeautifulSoup
import requests


# TODO thought: could save each movie as a duple of movie link and year, to
# avoid having to search through each one to check if the year is correct.
# The 'between' option takes a long time to search.

options = {}


# Alters the options regarding release year.
def year_options():
    choice = input('Year options:\n1. Before Year\n2. After Year\n3. Between Years\n4. Go Back\n')
    while not choice.isdigit() or int(choice) <= 0 or int(choice) > 4:
        choice = input('Please enter a valid choice.\nYear options:\n1. Before Year\n'
                       '2. After Year\n3. Between Years\n4. Go Back\n')
    if choice == '1':
        before = input('Enter year: ')
        while not before.isdigit() or int(before) > datetime.datetime.now().year:
            before = input('Enter valid year.\nEnter year: ')
        options['year'] = ('before', int(before))
    elif choice == '2':
        after = input('Enter year: ')
        while not after.isdigit() or int(after) > datetime.datetime.now().year:
            after = input('Enter valid year.\nEnter year: ')
        options['year'] = ('after', int(after))
    elif choice == '3':
        after = input('Enter earlier year: ')
        while not after.isdigit() or int(after) > datetime.datetime.now().year:
            after = input('Enter valid year.\nEnter earlier year: ')
        before = input('Enter later year: ')
        while not before.isdigit() or int(before) > datetime.datetime.now().year or int(before) < int(after):
            before = input('Enter valid year.\nEnter later year: ')
        options['year'] = ('between', (int(after), int(before)))
    return


# Alters the options regarding genres.
def genre_options():
    # TODO do this next.
    return


# Allows the user to select various options about how to select
# the random movie.
def select_options():
    while True:
        choice = input('Options:\n1. Year\n2. Genre\n3. Rating\n4. Done\n')
        # TODO alter this when you add more options
        while not choice.isdigit() or int(choice) <= 0 or int(choice) > 4:
            choice = input('Please enter a valid choice.\nOptions:\n1. Year\n2. Genre\n3. Rating\n4. Done\n')
        if choice == '1':
            year_options()
        elif choice == '2':
            genre_options()
        elif choice == '3':
            # TODO make a thing for rating options
            return
        elif choice == '4':
            return


# Given the url of a list, returns the number of pages that list
# consists of.
def get_number_of_pages(url):
    request = requests.get(url)
    soup = BeautifulSoup(request.content, 'html5lib')
    pages = soup.find_all('li', class_='paginate-page')
    return int(pages[len(pages) - 1].string)


# Given the username of a user, return an array containing all the movies
# on that user's watchlist.
def get_watchlist_from_username(username):
    movies = []
    url = 'https://letterboxd.com/' + username + '/watchlist/'
    pages_number = get_number_of_pages(url)
    for i in range(1, (pages_number + 1)):
        request = requests.get(url + 'page/' + str(i))
        soup = BeautifulSoup(request.content, 'html5lib')
        temp_movies = soup.find_all('div', class_='poster film-poster really-lazy-load')
        if len(temp_movies) == 0:
            break
        movies += temp_movies
    return list(map(lambda movie: movie['data-film-slug'], movies))

# TODO Note: it is faster to choose a movie from the list randomly,
# then check if it fits the criteria than to go through each individually
# and check, since each web call is very expensive.


# Checks if the url of the movie fits all the options.  Returns a boolean.
def check_options(movie):
    request = requests.get('https://letterboxd.com' + movie)
    movie_page = BeautifulSoup(request.content, 'html5lib')
    if 'year' in options.keys():
        header = movie_page.find(id='featured-film-header')
        year = int(header.p.small.text)
        if options['year'][0] == 'before' and options['year'][1] <= int(year):
            return False
        elif options['year'][0] == 'after' and options['year'][1] >= int(year):
            return False
        elif options['year'][0] == 'between' and \
                (options['year'][1][0] < int(year) or options['year'][1][1] > int(year)):
            return False

    # TODO just returns True for now, will fix later.
    return True


def main():
    select_options()
    username = input('Enter your letterboxd username: ')
    try:
        movies = get_watchlist_from_username(username)
        if options == {}:
            print('https://letterboxd.com' + movies[randint(0, len(movies))])
        else:
            # TODO add modifiers for options
            while True:
                if len(movies) == 0:
                    print('No movies match your criteria.')
                    return
                index = randint(0, len(movies))
                if check_options(movies[index]):
                    print('https://letterboxd.com' + movies[index])
                    break
                else:
                    del movies[index]
    except:
        print('Please enter a valid username.')
        main()
    return


if __name__ == '__main__':
    main()
