import datetime
import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from src.entities.entity import Session
from src.entities.idCambioContrasenna import IdCambioContrasenna


scheduler = BackgroundScheduler()


def deleteOldPasswordChangeId():
    try:
        expireTime = datetime.datetime.now() - datetime.timedelta(minutes=10)
        session = Session()
        expiredIds = session.query(IdCambioContrasenna).filter(IdCambioContrasenna.fechaCreacion < expireTime).all()

        for id in expiredIds:
            session.delete(id)
        session.commit()
        return '', 200
    except:
        return '', 400


scheduler.add_job(func=deleteOldPasswordChangeId, trigger="interval", seconds=300)

atexit.register(lambda: scheduler.shutdown())
