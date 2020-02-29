from flask import Flask, render_template, request
from backend.backend import Backend

class Interface(object):
    instance = None

    @staticmethod
    def getInstance():
        if Interface.instance is None:
            Interface.instance = Interface()
        return Interface.instance

    def __init__(self):
        super().__init__()

        self.app = Flask(__name__)
        self.setRoutes()


    def setRoutes(self):
        @self.app.route("/")
        def home():
            return render_template('home.html')

        @self.app.route('/get_imdb_url', methods=['GET', 'POST'])
        def get_imdb_url():
            """ Method to send URL entered in text box to be used

            :return: main index page
            """
            if request.method == 'GET':
                url = request.form['url']

                # If not valid URL then return and show nothing

                Backend.process_url(url)

                return render_template('index.html')
            return render_template('index.html')

    def run(self):
        self.app.run()
