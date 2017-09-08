#!/usr/bin/python3
""" Main app """
import logging
import yaml
from ircbot import IRCBot
from ircsocket import IRCSocket

def loading_param():
    with open('config.yml', 'r') as stream:
        try:
            PARAM = yaml.safe_load(stream)
        except yaml.YAMLError as error:
            PARAM = None
            logging.error(error)

    if PARAM is None:
        logging.error("Parameters not defined")
        exit(1)
    else:
        return PARAM


def main():
    """ Main function """

    logging.basicConfig(level=logging.DEBUG)
    logging.debug("Entering main()")

    logging.debug("Loading parameters")
    param = loading_param()

    logging.info("Connection to socket")
    irc_socket = IRCSocket(param['main_bot']['irc_server'], param['main_bot']['irc_port'])
    irc_socket.connect()

    logging.debug("initializing the main Bot")
    main_bot = IRCBot(irc_socket.irc_socket,
                      param['main_bot']['channel'],
                      param['main_bot']['admin_name'],
                      param['main_bot']['bot_name'],
                      param['main_bot']['exitcode'])



main()