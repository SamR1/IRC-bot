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

    while 1:
        irc_msg = irc_socket.irc_socket.recv(2048).decode("UTF-8")

        # Message format: “:[Nick]!~[hostname]@[IP Address] PRIVMSG [CHANNEL] :[message]”
        irc_msg = irc_msg.strip('\n\r')
        logging.debug(irc_msg)

        # check if the message is a private message
        if irc_msg.find("PRIVMSG") != -1:
            name = irc_msg.split('!', 1)[0][1:]
            message = irc_msg.split('PRIVMSG', 1)[1].split(':', 1)[1]

            # Usernames (at least for Freenode) are limited to 16 characters.
            if len(name) < 17:

                if name.lower() == main_bot.admin_name and message.rstrip() == main_bot.exitcode:
                    main_bot.send_message("oh...okay. :'(")
                    irc_socket.irc_socket.send(bytes("QUIT \n", "UTF-8"))
                    return
                else:
                    main_bot.privmsg_actions(message, name)

        elif irc_msg.find("PING :") != -1:
            irc_msg.ping()

main()