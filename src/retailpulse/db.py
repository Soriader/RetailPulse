from sqlalchemy import create_engine, text
from retailpulse.config import DBConfig

def get_engine():
    cfg = DBConfig()
    return create_engine(cfg.sqlalchemy_url)

def smoke_test():
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1")).scalar_one()
    return result