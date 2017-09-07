#!/usr/bin/python3
""" IRC Bot """
import logging
import socket
import yaml

with open('config.yml', 'r') as stream:
    try:
        PARAM = yaml.safe_load(stream)
    except yaml.YAMLError as error:
        PARAM = None
        logging.error(error)

if PARAM is None:
    exit(1)

IRC_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IRC_SERVER = PARAM['irc_server']
CHANNEL = PARAM['channel']
BOT_NAME = PARAM['bot_name']
ADMIN_NAME = PARAM['admin_name']
EXITCODE = PARAM['exitcode'] + PARAM['bot_name']

IRC_SOCKET.connect((IRC_SERVER, 6667))
IRC_SOCKET.send(bytes("USER " + BOT_NAME + " " + BOT_NAME + " " + BOT_NAME + " " + BOT_NAME + "\n",
                      "UTF-8"))
IRC_SOCKET.send(bytes("NICK " + BOT_NAME + "\n", "UTF-8"))


def joinchan(chan):
    """ Join function """
    IRC_SOCKET.send(bytes("JOIN " + chan + "\n", "UTF-8"))
    irc_msg = ""
    while irc_msg.find("End of /NAMES list.") == -1:
        irc_msg = IRC_SOCKET.recv(2048).decode("UTF-8")
        irc_msg = irc_msg.strip('\n\r')
        logging.info(irc_msg)


def ping():
    """ respond to server Pings."""
    IRC_SOCKET.send(bytes("PONG :pingis\n", "UTF-8"))


def sendmsg(msg, target=CHANNEL):
    """ sends messages to the target. """
    IRC_SOCKET.send(bytes("PRIVMSG " + target + " :" + msg + "\n", "UTF-8"))


def privmsg_actions(message, name):
    """ PRIVMSG actions """

    # greetings
    if message.find('Hi ' + BOT_NAME) != -1:
        sendmsg("Hello " + name + "!")

    # searching for a command ('.tell')
    if message[:5].find('.tell') != -1:

        target = message.split(' ', 1)[1]

        if target.find(' ') != -1:
            message = target.split(' ', 1)[1]
            target = target.split(' ')[0]

        else:
            target = name
            message = "Could not parse. The message should be in the format of " \
                      "‘.tell [target] [message]’ to work properly."
        sendmsg(message, target)

def main():
    """ main function """
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("Entering main()")

    joinchan(CHANNEL)
    while 1:
        irc_msg = IRC_SOCKET.recv(2048).decode("UTF-8")

        # Message format: “:[Nick]!~[hostname]@[IP Address] PRIVMSG [CHANNEL] :[message]”
        irc_msg = irc_msg.strip('\n\r')
        logging.info(irc_msg)

        # check if the message is a private message
        if irc_msg.find("PRIVMSG") != -1:
            name = irc_msg.split('!', 1)[0][1:]
            message = irc_msg.split('PRIVMSG', 1)[1].split(':', 1)[1]

            # Usernames (at least for Freenode) are limited to 16 characters.
            if len(name) < 17:

                if name.lower() == ADMIN_NAME.lower() and message.rstrip() == EXITCODE:
                    sendmsg("oh...okay. :'(")
                    IRC_SOCKET.send(bytes("QUIT \n", "UTF-8"))
                    return
                else:
                    privmsg_actions(message, name)

        elif irc_msg.find("PING :") != -1:
                ping()

main()
