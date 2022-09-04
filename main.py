from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


class Vacancy(Resource):
    def get(self):
        return {"Vacancy": "Data Engineer"}


api.add_resource(Vacancy, "/vacancy")

if __name__ == '__main__':
    app.run(debug=True)
