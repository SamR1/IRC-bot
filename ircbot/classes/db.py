from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging

Base = declarative_base()


class Ircsocket(Base):
    __tablename__ = 'ircsocket'
    id = Column(Integer, primary_key=True)
    irc_server = Column(String(250), nullable=False)
    irc_port = Column(Integer, nullable=False)


class Ircbot(Base):
    __tablename__ = 'ircbot'
    id = Column(Integer, primary_key=True)
    bot_name = Column(String(250), nullable=False)
    admin_name = Column(String(250), nullable=False)
    channel = Column(String(250), nullable=False)
    exitcode = Column(String(250), nullable=False)
    exitmsg = Column(String(250), nullable=False)
    entermsg = Column(String(250), nullable=False)
    owmapi = Column(String(250), nullable=True)


class Greetings(Base):
    __tablename__ = 'greeting'
    id = Column(Integer, primary_key=True)
    greeting = Column(String(250), nullable=False)


def generate_db(url):
    logging.info("database creation")
    try:
        engine = create_engine(url)
        Base.metadata.create_all(engine)
        return engine
    except Exception as e:
        logging.error(str(e.args))
        return False


def load_db(engine, param):
    logging.info("loading parameters in database")

    try:

        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()

        # Insert a Irc Socket in the Ircsocket table
        new_ircserver = Ircsocket(irc_server=param['main_bot']['irc_server'],
                                  irc_port=param['main_bot']['irc_port'])
        session.add(new_ircserver)
        session.commit()

        # Insert a Irc Bot in the Ircbot table
        new_bot = Ircbot(bot_name=param['main_bot']['bot_name'],
                         admin_name=param['main_bot']['admin_name'],
                         channel=param['main_bot']['channel'],
                         exitcode=param['main_bot']['exitcode'] + param['main_bot']['admin_name'],
                         exitmsg=param['main_bot']['exitmsg'],
                         entermsg=param['main_bot']['entermsg'],
                         owmapi = param['owmapi'])
        session.add(new_bot)
        session.commit()

        # Insert default greetings
        greetings = ["Hello", "Bonjour", "Hallo", "Buongiorno", "Hola", "Namaste"]
        for word in greetings:
            new_greeting = Greetings(greeting=word)
            session.add(new_greeting)
            session.commit()
        return True
    except Exception as e:
        logging.error(str(e.args))
        return False
