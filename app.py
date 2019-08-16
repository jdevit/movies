from flask import Flask, render_template, request
import imdbapi

app = Flask(__name__)

@app.route('/')
def home():
    """ Return to homepage via 'index.html'

    :return: main index page
    """
    return render_template('index.html')

@app.route('/send', methods=['GET','POST'])
def send():
    """ Method to send URL entered in text box to be used

    :return: main index page
    """
    if request.method == 'POST':
        print("Sent")
        url = request.form['url']
        print("the url:",url)
        imdbapi.retrieveData(url)


        return render_template('index.html')
    return render_template('index.html')



if __name__ == "__main__":
    app.run(debug = True)