import csv

def readFile(filename,delimeter):
    """ Opens and reads a file. Then returns the contents as a string.

    :param filename: String: name of file to be read
    :return: String: contents of the file
    """

    file = open(filename, 'r')
    contents = file.read()
    contents = contents.split(delimeter)
    return contents

def writeFile(filename, film):
    """ Output contents from film dictionary to a csv file

    :param filename:    String: name of the csv file to be written
    :param film:        Dictionary: Contains values of each field of a film
    :return: None
    """
    file = open(filename, 'a')
    values = getListFieldValues(film)
    for val in values:
        if val==values[-1]:
            file.write('"'+str(val)+'"')
        else:
            file.write('"'+str(val)+'"'+',')
    file.write("\n")

def getListFieldValues(film):
    """

    :param film: Dictionary: containing fields from a movie
    :return: list of values from movie
    """
    fields = ['title','date','year','duration','age_rating','genre','country','director','writer','actor','imdb_rating','num_rates','description','keywords']
    values = []

    for field in fields:
        values.append(film[field])
    print(values)
    return values

def saveToFile(film):
    """ Writes to file by calling the writeFile method

    :param film: Dictionary: contains attribute values for a given film
    :return: None
    """
    filename = "movielist.csv"
    writeFile(filename,film)


def main():
    print("Hi")
    filename = "movielist.csv"
    # content = readCSV(filename)
    values = getListFieldValues()
    writeFile(filename,)


if __name__ == "__main__":
    main()