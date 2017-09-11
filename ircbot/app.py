#!/usr/bin/python3
""" Main app """
import logging
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists
from sqlalchemy.orm import sessionmaker
import yaml
from classes.ircbot import IRCBot
from classes.ircsocket import IRCSocket
import classes.db as dbclass


def load_config_file():
    with open('config.yml', 'r') as stream:
        try:
            PARAM = yaml.safe_load(stream)
        except yaml.YAMLError as error:
            PARAM = None
            logging.error(error)

    if PARAM is None:
        logging.error("Parameters not defined")
        return False
    else:
        return PARAM


def create_and_load_database(db_url):
    engine = dbclass.generate_db(db_url)
    if not engine:
        return False
    else:
        param = load_config_file()
        if not param:
            return False
        else:
            if not dbclass.load_db(engine, param):
                return False
            else:
                return engine


def loading_param():
    """ Load parameters. If database doesn't exist, it creates it"""

    SQLALCHEMY_DATABASE_URI = "sqlite:///db/ircbot.db"
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    if not database_exists(engine.url):
        engine = create_and_load_database(SQLALCHEMY_DATABASE_URI)

    if not engine:
        return False
    else:
        return engine


def main():
    """ Main function """

    logging.basicConfig(filename='ircbot.log', level=logging.DEBUG)
    logging.debug("Entering main()")

    logging.debug("Loading parameters")
    engine = loading_param()

    dbclass.Base.metadata.bind = engine
    DBSession = sessionmaker()
    DBSession.bind = engine
    session = DBSession()
    irc_socket_param = session.query(dbclass.Ircsocket).first()

    logging.info("Connection to the socket")
    irc_socket = IRCSocket(irc_socket_param.irc_server, irc_socket_param.irc_port)
    if not irc_socket.connect():
        return

    logging.info("Main Bot init")
    # only one bot for now
    irc_bot_param = session.query(dbclass.Ircbot).first()
    greetings = session.query(dbclass.Greetings).all()
    main_bot = IRCBot(irc_socket.irc_socket,
                      irc_bot_param, greetings)
    if not main_bot.join_channel():
        return

    while 1:
        irc_msg = irc_socket.irc_socket.recv(2048).decode("UTF-8")

        # Message format: “:[Nick]!~[hostname]@[IP Address] PRIVMSG [CHANNEL] :[message]”
        irc_msg = irc_msg.strip('\n\r')
        logging.debug(irc_msg)

        if main_bot.analyse_msg(irc_msg) is None:
            return

main()
