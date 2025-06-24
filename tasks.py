from datetime import datetime, timedelta
from models import Asset, Notification, Violation, db

def run_checks():
    now = datetime.utcnow()
    window = now + timedelta(minutes=15)
    assets = Asset.query.all()
    for asset in assets:
        if asset.service_time:
            if now < asset.service_time <= window:
                _log_notification(asset.id, 'service')
            if asset.service_time < now and not asset.serviced:
                _log_violation(asset.id, 'service')
        if asset.expiration_time:
            if now < asset.expiration_time <= window:
                _log_notification(asset.id, 'expiration')
            if asset.expiration_time < now:
                _log_violation(asset.id, 'expiration')

def _log_notification(asset_id, type_):
    n = Notification(asset_id=asset_id, type=type_)
    db.session.add(n)
    db.session.commit()

def _log_violation(asset_id, type_):
    v = Violation(asset_id=asset_id, type=type_)
    db.session.add(v)
    db.session.commit()
