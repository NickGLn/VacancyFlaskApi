from flask import Flask
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)
api = Api(app)

specializations = {"dwh": "Kimball", "cloud": "Shulz"}

vacancies = {1: {"name": "Data Engineer", "company": "Amazon", "salary": 180000},
             2: {"name": "Data Scientist", "company": "Microsoft", "salary": 200000},
             3: {"name": "Data Analyst", "company": "Apple", "salary": 160000}}

vac_args = reqparse.RequestParser()

vac_args.add_argument("name", type=str, required=True )
vac_args.add_argument("company", type=str, required=True )
vac_args.add_argument("salary", type=str, required=False )


def abort_if_not_exists(vacancy_name):
    if not vacancy_name:
        abort('vacancy does not exist')


class Vacancy(Resource):
    def get(self, vacancy_id):
        return vacancies[vacancy_id]

    def post(self):
        return {"Post Status": "Success"}

    def put(self):
        vacancy_id = len(vacancies)+1
        args = vac_args.parse_args()
        vacancies[vacancy_id] = args
        return vacancies[vacancy_id]


api.add_resource(Vacancy, "/vacancy/<int:vacancy_id>", '/vacancy')

if __name__ == '__main__':
    app.run(debug=True)
