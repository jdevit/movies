from bs4 import BeautifulSoup
import requests
import re
import json
import fileops

def checkURL(url):
    if "imdb.com" in url:
        return True
    else:
        return False


def formatURL(url):
    pattern = r'(imdb\.com\/title\/(.*/))'

    urls = re.findall(pattern,url)
    urls = urls[0]
    new_url = urls[0]
    new_url = "https://www."+new_url
    title_code = urls[1].replace("/","")

    print(new_url, title_code)
    return new_url

def getSoup(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup

def getCountry(soup):
    title_details = getAdditionalDetails(soup)
    country = title_details[1].get_text().replace("Country:", "").strip()
    return country

def getRuntime(soup):
    title_details = getAdditionalDetails(soup)
    duration = title_details[12].get_text().replace("Runtime:", "").strip()
    return duration

def getAdditionalDetails(soup):
    title_details = soup.find('div', id="titleDetails")
    title_details = title_details.findAll('div', class_="txt-block")
    return title_details

def getJson(soup):
    script = soup.find('script', type='application/ld+json')
    json_text = BeautifulSoup.get_text(script)
    print(json_text)
    return json.loads(json_text)

def getPeopleNames(the_list):
    new_list = []
    if type(the_list) == list:
        for person in the_list:
            if person['@type'] == "Person":
                new_list.append(person['name'])
    else:
        new_list.append(the_list['name'])
    return new_list

def getFields(mov_dict, soup):
    film = {}

    title = mov_dict['name']
    print(title)

    ##### Date published is not film date released #####
    date = mov_dict['datePublished']
    year = date[0:4]
    print(year)

    duration = getRuntime(soup)
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
    if checkURL(url) == False:
        return None
    url = formatURL(url)
    soup = getSoup(url)
    json = getJson(soup)
    more = getAdditionalDetails(soup)
    film = getFields(json,soup)
    fileops.saveToFile(film)
    pass


def main():
    print("Hi")
    exampleurl = "https://www.imdb.com/title/tt1596363/?ref_=wl_li_tt" #The Big Short (2015)
    nocountry = "https://www.imdb.com/title/tt0477348/"
    silverliningsplaybook = "https://www.imdb.com/title/tt1045658/?ref_=tt_sims_tt"
    daysofsummer = "https://www.imdb.com/title/tt1022603/?ref_=tt_sims_tt"
    oldboy = "https://www.imdb.com/title/tt0364569/?ref_=nv_sr_1?ref_=nv_sr_1"

    retrieveData(oldboy)

if __name__=="__main__":
    main()