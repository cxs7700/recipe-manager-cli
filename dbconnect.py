import sqlalchemy
from sqlalchemy import text
DATABASE = "postgresql://p320_13:aiyohleiCahc2xahtee1@p320_13:5432/reddwarf"
ENGINE = sqlalchemy.create_engine(DATABASE)
CONNECTION = ENGINE.connect()

def execute_query(query, **kwargs):
    statement = text(query)
    return CONNECTION.execute(query, kwargs)
