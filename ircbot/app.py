#!/usr/bin/python3
""" Main app """
import logging
import yaml
from classes.ircbot import IRCBot
from classes.ircsocket import IRCSocket


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

    logging.basicConfig(filename='ircbot.log', level=logging.DEBUG)
    logging.debug("Entering main()")

    logging.debug("Loading parameters")
    param = loading_param()

    logging.info("Connection to the socket")
    irc_socket = IRCSocket(param['main_bot']['irc_server'], param['main_bot']['irc_port'])
    if not irc_socket.connect():
        return

    logging.info("Main Bot init")
    main_bot = IRCBot(irc_socket.irc_socket,
                      param)
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
