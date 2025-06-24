from flask import Flask
from flask_restful import Api
from models import db
from resources import (
    AssetListAPI,
    AssetAPI,
    RunChecksAPI,
    NotificationListAPI,
    ViolationListAPI
)
from flasgger import Swagger

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

Swagger(app)
db.init_app(app)
api = Api(app)

with app.app_context():
    db.create_all()

api.add_resource(AssetListAPI, '/assets')
api.add_resource(AssetAPI, '/assets/<int:asset_id>')
api.add_resource(RunChecksAPI, '/run-checks')
api.add_resource(NotificationListAPI, '/notifications')
api.add_resource(ViolationListAPI, '/violations')

if __name__ == '__main__':
    app.run(debug=True)

