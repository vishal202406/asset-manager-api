from flask_restful import Resource, reqparse
from models import db, Asset, Notification, Violation
from tasks import run_checks

asset_parser = reqparse.RequestParser()
asset_parser.add_argument('name', required=True)
asset_parser.add_argument('service_time')
asset_parser.add_argument('expiration_time')
asset_parser.add_argument('serviced', type=bool)

class AssetListAPI(Resource):
    def get(self):
        assets = Asset.query.all()
        return [self._serialize(asset) for asset in assets]

    def post(self):
        args = asset_parser.parse_args()
        asset = Asset(
            name=args['name'],
            service_time=self._parse_datetime(args['service_time']),
            expiration_time=self._parse_datetime(args['expiration_time']),
            serviced=args['serviced'] or False
        )
        db.session.add(asset)
        db.session.commit()
        return self._serialize(asset), 201

    def _serialize(self, asset):
        return {
            'id': asset.id,
            'name': asset.name,
            'service_time': str(asset.service_time),
            'expiration_time': str(asset.expiration_time),
            'serviced': asset.serviced
        }

    def _parse_datetime(self, dt_str):
        from datetime import datetime
        if dt_str:
            return datetime.fromisoformat(dt_str)
        return None

class AssetAPI(Resource):
    def get(self, asset_id):
        asset = Asset.query.get_or_404(asset_id)
        return {
            'id': asset.id,
            'name': asset.name,
            'service_time': str(asset.service_time),
            'expiration_time': str(asset.expiration_time),
            'serviced': asset.serviced
        }

    def put(self, asset_id):
        asset = Asset.query.get_or_404(asset_id)
        args = asset_parser.parse_args()
        asset.name = args['name']
        asset.service_time = self._parse_datetime(args['service_time'])
        asset.expiration_time = self._parse_datetime(args['expiration_time'])
        asset.serviced = args['serviced']
        db.session.commit()
        return {'message': 'Asset updated successfully.'}

    def delete(self, asset_id):
        asset = Asset.query.get_or_404(asset_id)
        db.session.delete(asset)
        db.session.commit()
        return {'message': 'Asset deleted successfully.'}

    def _parse_datetime(self, dt_str):
        from datetime import datetime
        if dt_str:
            return datetime.fromisoformat(dt_str)
        return None

class RunChecksAPI(Resource):
    def post(self):
        run_checks()
        return {"message": "Checks executed successfully."}

class NotificationListAPI(Resource):
    def get(self):
        notifications = Notification.query.all()
        return [
            {
                'id': n.id,
                'asset_id': n.asset_id,
                'type': n.type,
                'timestamp': str(n.timestamp)
            } for n in notifications
        ]

class ViolationListAPI(Resource):
    def get(self):
        violations = Violation.query.all()
        return [
            {
                'id': v.id,
                'asset_id': v.asset_id,
                'type': v.type,
                'timestamp': str(v.timestamp)
            } for v in violations
        ]
