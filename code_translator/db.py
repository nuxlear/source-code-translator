from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from sqlalchemy import create_engine, inspect
from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint, ForeignKey

from pathlib import Path
import json
import os


Base = declarative_base()


def get_db_credentials(token_file):
    cred_path = Path(token_file)

    if cred_path.exists():
        with open(cred_path, 'r') as f:
            creds = json.load(f)
        creds = {k.upper(): v for k, v in creds.items()}

    else:
        keys = [
            'DATABASE_HOST',
            'DATABASE_PORT',
            'DATABASE_NAME',
            'DATABASE_USER',
            'DATABASE_PASSWORD',
        ]
        creds = {k: os.environ.get(k, '') for k in keys}

    return creds


def get_db_engine(token_file=None, cred=None, echo=False):
    if cred is None:
        cred = get_db_credentials(token_file)
    host = cred['DATABASE_HOST']
    port = cred['DATABASE_PORT']
    name = cred['DATABASE_NAME']
    username = cred['DATABASE_USER']
    password = cred['DATABASE_PASSWORD']
    engine = create_engine(f'mysql://{username}:{password}@{host}:{port}/{name}', echo=echo)
    return engine


class CodeTranslateResults(Base):
    __tablename__ = 'code_translate_results'

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(256), index=True)
    reaction = Column(String(50))


def get_session(engine):
    session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    return session()


if __name__ == '__main__':
    engine = get_db_engine('db_tokens_main.json')
    orms = [
        CodeTranslateResults,
    ]

    for orm in orms:
        if not inspect(engine).has_table(orm.__tablename__):
            orm.__table__.create(bind=engine)
