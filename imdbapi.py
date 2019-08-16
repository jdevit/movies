from bs4 import BeautifulSoup
import requests
import re
import json
import fileops

def checkURL(url):
    """ Check if the url domain is IMDB

    :param url: String: Passing in the url to check
    :return: Boolean: True if is IMDB domain
    """
    if "imdb.com" in url:
        return True
    else:
        return False


def formatURL(url):
    """ Formats the given url so it any leading characters are displaced

    :param url: String: url of IMDB film page
    :return: String: returns a formatted url
    """
    pattern = r'(imdb\.com\/title\/(.*/))'
    urls = re.findall(pattern,url)
    urls = urls[0]
    new_url = urls[0]
    new_url = "https://www."+new_url
    title_code = urls[1].replace("/","")
    return new_url

def formatRuntime(duration):
    """ Converts duration from format: 'PThhHmmM' to 'mmm mins'

    :param duration:  String: duration given in Hours and Minutes
    :return: String duration is now all in minutes
    """
    pass

def getSoup(url):
    """ Gets the BeautifulSoup object of a webpage when parsed in URL.

    :param url: String: url of IMDB film page
    :return: BeautifulSoup object: Contains html code for web page
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup

def getCountry(soup):
    """ Extracts the country of origin for film by finding it in Details section of page

    :param soup: BeautifulSoup object: contains html code for web page
    :return: List: returns a list containing Strings of country/countries the film was produced in
    """
    title_details = getAdditionalDetails(soup)
    pattern = r'country_of_origin.*?>(.*?)<'
    country = re.findall(pattern,str(title_details))
    return country

def getAdditionalDetails(soup):
    """ Returns Details section of IMDB film page

    :param soup: BeautifulSoup object: contains html code for web page
    :return: BeautifulSoup object: contains small section of page
    """
    title_details = soup.find('div', id="titleDetails")
    title_details = title_details.findAll('div', class_="txt-block")
    return title_details

def getJson(soup):
    """ Retrieve JSON file located in the scripts tag which is present in all film pages

    :param soup: BeautifulSoup object: contains html code for web page
    :return: Dictionary: contains details of film from given web page
    """
    script = soup.find('script', type='application/ld+json')
    json_text = BeautifulSoup.get_text(script)
    print(json_text)
    return json.loads(json_text)

def getPeopleNames(the_list):
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

def getFields(mov_dict, soup):
    """ Get all fields required for a single film record.

    :param mov_dict: Dictionary: JSON text containg film information retrieved from web page
    :param soup: BeautifulSoup object: contains html code for web page
    :return: Dictionary: containing all fields and values of the record added
    """
    film = {}

    title = mov_dict['name']
    print(title)

    ##### Date published is not film date released #####
    date = mov_dict['datePublished']
    year = date[0:4]
    print(year)

    duration = mov_dict['duration']
    print(duration)

    age_rating = mov_dict['contentRating']
    print(age_rating)

    genre = mov_dict['genre']
    print(genre)

    country = getCountry(soup)
    print(country)

    directors = mov_dict['director']
    director = getPeopleNames(directors)
    print(director)

    writers = mov_dict['creator']
    writer = getPeopleNames(writers)
    print(writer)

    actors = mov_dict['actor']
    actor = getPeopleNames(actors)
    print(actor)

    imdb_rating = mov_dict['aggregateRating']['ratingValue']
    print(imdb_rating)

    num_rates = mov_dict['aggregateRating']['ratingCount']
    print(num_rates)

    description = mov_dict['description']
    keywords = mov_dict['keywords'].split(",")
    print(keywords)

    film['title'] = title
    film['date'] = date
    film['year'] = year
    film['duration'] = duration
    film['age_rating'] = age_rating
    film['genre'] = genre
    film['country'] = country
    film['director'] = director
    film['writer'] = writer
    film['actor'] = actor
    film['imdb_rating'] = imdb_rating
    film['num_rates'] = num_rates
    film['description'] = description
    film['keywords'] = keywords

    return film


def retrieveData(url):
    """ Contains ordered instructions for each method to be run

    :param url: String: URL given via app.py
    :return: None
    """
    if checkURL(url) == False:
        return None
    url = formatURL(url)
    soup = getSoup(url)
    json = getJson(soup)
    more = getAdditionalDetails(soup)
    film = getFields(json,soup)
    fileops.saveToFile(film)


def main():
    print("Hi")
    exampleurl = "https://www.imdb.com/title/tt1596363/?ref_=wl_li_tt" #The Big Short (2015)
    nocountry = "https://www.imdb.com/title/tt0477348/"
    silverliningsplaybook = "https://www.imdb.com/title/tt1045658/?ref_=tt_sims_tt"
    daysofsummer = "https://www.imdb.com/title/tt1022603/?ref_=tt_sims_tt"
    oldboy = "https://www.imdb.com/title/tt0364569/?ref_=nv_sr_1?ref_=nv_sr_1"
    lobster = "https://www.imdb.com/title/tt3464902/?ref_=rt_li_tt"
    fivecm = "https://www.imdb.com/title/tt0983213/?ref_=tt_sims_tt"
    gardenwords = "https://www.imdb.com/title/tt2591814/?ref_=tt_sims_tt"

    retrieveData(gardenwords)

if __name__=="__main__":
    main()