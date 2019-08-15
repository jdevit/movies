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

def readCSV(filename):
    with open(filename, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        x = ""
        for row in csv_reader:
            print(row)
            if line_count == 0:
                # print(f'Column names are {", ".join(row)}')
                line_count += 1
            line_count += 1
        # print(f'Processed {line_count} lines.')
    print(x)
    return csv_reader

def writeFile(filename, film):
    file = open(filename, 'a')
    line = ""
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