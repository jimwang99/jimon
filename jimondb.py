import pytz

from datetime import datetime
from peewee import *

from loguru import logger

_db = SqliteDatabase("jimon.db")


class TableUpdate(Model):
    update_type = IntegerField()
    hostname = CharField()
    timestamp = IntegerField()
    temp = FloatField()
    cpu_usage = FloatField()
    mem_usage = FloatField()

    class Meta:
        database = _db


def connect():
    _db.connect()
    _db.create_tables([TableUpdate], safe=True)


def insert(
    update_type: int,
    hostname: str,
    timestamp: int,
    temp: float,
    cpu_usage: float,
    mem_usage: float,
):
    with _db.atomic():
        TableUpdate.create(
            update_type=update_type,
            hostname=hostname,
            timestamp=timestamp,
            temp=temp,
            cpu_usage=cpu_usage,
            mem_usage=mem_usage,
        )
        logger.debug(
            f"{update_type=} {hostname=} {timestamp=} {temp=:.2f} {cpu_usage=:.2f} {mem_usage=:.2f}"
        )


def query_all():
    return TableUpdate.select()


def debug():
    for update in query_all():
        logger.debug(
            f"{update.update_type=} {update.hostname=} {update.timestamp=} {update.temp=:.2f} {update.cpu_usage=:.2f} {update.mem_usage=:.2f}"
        )

def _timestamp_int_to_str(n: int) -> str:
    o = datetime.fromtimestamp(int(n))
    o = o.astimezone(pytz.timezone("America/Los_Angeles"))
    s = o.strftime("%Y-%m-%d %H:%M:%S")
    return s


def get_last_update():
    dt = {}
    for update in query_all():
        try:
            _update = dt[update.hostname]
            if _update.timestamp < update.timestamp:
                dt[update.hostname] = update
        except KeyError:
            dt[update.hostname] = update
    
    for update in dt.values():
        s_timestamp = _timestamp_int_to_str(update.timestamp)
        logger.info(
            f"{s_timestamp} hostname={update.hostname} timestamp={update.timestamp} temp={update.temp:.2f} cpu_usage={update.cpu_usage:.2f} mem_usage={update.mem_usage:.2f}"
        )
    
    return dt


def close():
    _db.close()


if __name__ == "__main__":
    connect()
    get_last_update()
    close()
