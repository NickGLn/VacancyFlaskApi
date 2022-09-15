from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class VacancyModel(db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    company = db.Column(db.String(100), nullable=True)
    salary = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"vacancy \"{name}\" from company {company}, with salary = {str(salary)}"


vac_args = reqparse.RequestParser()
vac_args.add_argument("name", type=str, required=True )
vac_args.add_argument("company", type=str, required=True )
vac_args.add_argument("salary", type=int, required=False )


vac_update_args = reqparse.RequestParser()
vac_update_args.add_argument("name", type=str)
vac_update_args.add_argument("company", type=str)
vac_update_args.add_argument("salary", type=int)


def abort_if_not_exists(vacancy_id):
    if not vacancy_id:
        abort('vacancy does not exist')


resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'company': fields.String,
    'salary': fields.Integer
}


class Vacancy(Resource):

    @marshal_with(resource_fields)
    def get(self, vacancy_id):
        result = VacancyModel.query.filter_by(id=int(vacancy_id)).first()
        return result

    @marshal_with(resource_fields)
    def put(self):
        args = vac_args.parse_args()
        vacancy = VacancyModel(name=args['name'], company=args['company'], salary=args['salary'])
        db.session.add(vacancy)
        db.session.commit()
        return vacancy, 201

    @marshal_with(resource_fields)
    def patch(self, vacancy_id):
        args = vac_update_args.parse_args()
        vacancy =  VacancyModel.query.filter_by(id=int(vacancy_id)).first()
        if not vacancy:
            abort(404, message = 'Vacancy does not exist')

        if args["name"]:
            vacancy.name = args["name"]

        if args["company"]:
            vacancy.company = args["company"]

        if args["salary"]:
            vacancy.salary = args["salary"]

        db.session.commit()
        return vacancy, 204


api.add_resource(Vacancy, "/vacancy/<int:vacancy_id>", '/vacancy')

if __name__ == '__main__':
    app.run(debug=True)
