from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from sqlalchemy import create_engine, inspect
from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint, ForeignKey, Index
from sqlalchemy.sql import text as sql_text
from sqlalchemy.exc import SQLAlchemyError

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


class CodeTranslateFeedback(Base):
    __tablename__ = 'code_translate_feedback'

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(256))
    input_text = Column(String(4096))
    output_text = Column(String(4096))
    type = Column(String(50))
    reaction = Column(String(50))
    timestamp = Column(DateTime(timezone=True), nullable=False,
                       server_default=sql_text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    # __table_args__ = (
    #     Index('io_pair', 'input_text', 'output_text'),
    # )


def get_session(engine):
    session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    return session()


def wrap_db_success(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
            return True
        except SQLAlchemyError as e:
            print(e.__traceback__)
            print(e)
            return False
    return wrapper


# @wrap_db_success
def insert(orm):
    with get_session(get_db_engine('db_tokens_main.json')) as session:
        session.add(orm)
        session.commit()


# @wrap_db_success
def update_reaction(filename, input_text, output_text, type: str, reaction: str):
    assert reaction in ['good', 'bad'], f'Invalid reaction: {reaction}'
    with get_session(get_db_engine('db_tokens_main.json')) as session:
        o = CodeTranslateFeedback(filename=filename,
                                  input_text=input_text,
                                  output_text=output_text,
                                  type=type)
        # res = [x for x in list(session.query(CodeTranslateFeedback).all())
        #        if x.filename == o.filename and
        #        x.input_text == o.input_text and
        #        x.output_text == o.output_text and
        #        x.type == o.type]
        res = list(session.query(CodeTranslateFeedback).filter(
            (CodeTranslateFeedback.filename == o.filename) &
            (CodeTranslateFeedback.input_text == o.input_text) &
            (CodeTranslateFeedback.output_text == o.output_text) &
            (CodeTranslateFeedback.type == o.type)
        ).all())
        if len(res) == 0:
            o.reaction = reaction
            insert(o)
        else:
            res[0].reaction = reaction
        session.commit()


if __name__ == '__main__':
    engine = get_db_engine('db_tokens_main.json')
    orms = [
        CodeTranslateResults,
        CodeTranslateFeedback,
    ]

    for orm in orms:
        if not inspect(engine).has_table(orm.__tablename__):
            orm.__table__.create(bind=engine)
