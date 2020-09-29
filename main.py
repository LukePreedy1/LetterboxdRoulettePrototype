from bs4 import BeautifulSoup
import requests


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


def main():
    return


if __name__ == '__main__':
    get_watchlist_from_username('LukePreedy')
    # main()
