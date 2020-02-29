from bs4 import BeautifulSoup
import requests
import re
import json


class ImdbAPI:

    def __init__(self, url):
        self.url = url
        self.film = {}

    @staticmethod
    def get_movie_details(self):
        """ Contains ordered instructions for each method to be run

        :param url:
        :return: Dictionary of film details
        """

        if self.isValidURL(self.url) == False:
            return None
        url = self.formatURL(self.url)

        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        film = self.getJson(soup)
        more = self.getAdditionalDetails(soup)
        self.setMovieDetails(film, soup)
        self.create_mov_dict()
        return self.film

    def isValidURL(self, url):
        """ Check if the url domain is IMDB

        :param url: String: Passing in the url to check
        :return: Boolean: True if is IMDB domain
        """
        if "imdb.com" in url:
            return True
        else:
            return False

    def formatURL(self, url):
        """ Formats the given url so it any leading characters are displaced

        :param url: String: url of IMDB film page
        :return: String: returns a formatted url
        """
        pattern = r'(imdb\.com\/title\/(.*/))'
        urls = re.findall(pattern, url)
        urls = urls[0]
        new_url = urls[0]
        new_url = "https://www." + new_url
        title_code = urls[1].replace("/", "")
        return new_url

    def formatRuntime(self, duration):
        """ Converts duration from format: 'PThhHmmM' to 'mmm mins'

        :param duration:  String: duration given in Hours and Minutes
        :return: String duration is now all in minutes
        """
        pass

    def getAdditionalDetails(self, soup):
        """ Returns Details section of IMDB film page

        :param soup: BeautifulSoup object: contains html code for web page
        :return: BeautifulSoup object: contains small section of page
        """
        title_details = soup.find('div', id="titleDetails")
        title_details = title_details.findAll('div', class_="txt-block")
        return title_details

    def getJson(self, soup):
        """ Retrieve JSON file located in the scripts tag which is present in all film pages

        :param soup: BeautifulSoup object: contains html code for web page
        :return: Dictionary: contains details of film from given web page
        """
        script = soup.find('script', type='application/ld+json')
        json_text = BeautifulSoup.get_text(script)
        print(json_text)
        return json.loads(json_text)



    def setMovieDetails(self, mov_dict, soup):
        """ Get all fields required for a single film record.

        :param mov_dict: Dictionary: JSON text containing film information retrieved from web page
        :param soup: BeautifulSoup object: contains html code for web page
        :return: Dictionary: containing all fields and values of the record added
        """

        def getPeopleNames(self, the_list):
            """ Retrieve a single name or list of names from Director/Writer/Actor in JSON file

            :param the_list: List: contains dictionary of persons or others
            :return: List: returns a list of String containing only names.
            """
            new_list = []
            if type(the_list) == list:
                for person in the_list:
                    if person['@type'] == "Person":
                        new_list.append(person['name'])
            else:
                new_list.append(the_list['name'])
            return new_list

        def getCountry(self, soup):
            """ Extracts the country of origin for film by finding it in Details section of page

            :param soup: BeautifulSoup object: contains html code for web page
            :return: List: returns a list containing Strings of country/countries the film was produced in
            """
            title_details = self.getAdditionalDetails(soup)
            pattern = r'country_of_origin.*?>(.*?)<'
            country = re.findall(pattern, str(title_details))
            return country

        self.title = mov_dict['name']

        ##### Date published is not film date released #####
        self.date = mov_dict['datePublished']
        self.year = self.date[0:4]

        self.duration = mov_dict['duration']

        self.age_rating = mov_dict['contentRating']

        self.genre = mov_dict['genre']

        self.country = getCountry(soup)

        directors = mov_dict['director']
        self.director = getPeopleNames(directors)

        writers = mov_dict['creator']
        self.writer = getPeopleNames(writers)

        actors = mov_dict['actor']
        self.actor = getPeopleNames(actors)

        self.imdb_rating = mov_dict['aggregateRating']['ratingValue']

        self.num_rates = mov_dict['aggregateRating']['ratingCount']

        self.description = mov_dict['description']
        self.keywords = mov_dict['keywords'].split(",")


    def create_mov_dict(self):
        self.film['title'] = self.title
        self.film['date'] = self.date
        self.film['year'] = self.year
        self.film['duration'] = self.duration
        self.film['age_rating'] = self.age_rating
        self.film['genre'] = self.genre
        self.film['country'] = self.country
        self.film['director'] = self.director
        self.film['writer'] = self.writer
        self.film['actor'] = self.actor
        self.film['imdb_rating'] = self.imdb_rating
        self.film['num_rates'] = self.num_rates
        self.film['description'] = self.description
        self.film['keywords'] = self.keywords
