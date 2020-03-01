from flask import Flask, render_template, request, url_for
from api.imdbAPI import ImdbAPI

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
            return self.generate_page('home.html')

        @self.app.route('/get_imdb_url', methods=['GET', 'POST'])
        def get_imdb_url():
            """ Method to send URL entered in text box to be used

            :return: main index page
            """
            if request.method == 'POST':
                url = request.form['url']

                print(url)

                # If not valid URL then return and show nothing

                imdb_api = ImdbAPI(url)
                film = imdb_api.get_movie_details()
                print(film)

                # Save movie details to db

                # If successful add: return new page with movie details

                return self.get_header() + render_template('movie.html', film=film) + self.get_footer()
            return self.generate_page('home.html')

    def generate_page(self, page):
        return self.get_header() + render_template(page) + self.get_footer()

    def get_header(self):
        return render_template('head.html',
                               css=url_for('static', filename='styles.css'),
                               scripts_js=url_for('static', filename='scripts.js'),
                               bootstrap_css=url_for('static', filename='bootstrap.css'),
                               bootstrap_js=url_for('static', filename='bootstrap.js')
                               )

    def get_footer(self):
        return render_template('foot.html')

    def run(self):
        self.app.run()
