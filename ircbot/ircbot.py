#!/usr/bin/python3
import logging


class IRCBot:
    """ IRC Bot """

    def __init__(self, irc_socket, channel, admin_name, botname, exitcode):
        self._irc_socket = irc_socket
        self._channel = channel
        self._admin_name = admin_name
        self._name = botname
        self._exitcode = exitcode + botname
        self._irc_socket.send(
            bytes("USER " + self._name + " " + self._name + " " + self._name + " " + self._name + "\n",
                  "UTF-8"))
        self._irc_socket.send(bytes("NICK " + self._name + "\n", "UTF-8"))
        self.join_channel()

    def _get_admin_name(self):
        """ Function to get admin name"""
        return self._admin_name

    def _get_exitcode(self):
        """ Function to get exitcode"""
        return self._exitcode

    def join_channel(self):
        self._irc_socket.sendall(bytes("JOIN " + self._channel + "\n", "UTF-8"))
        irc_msg = ""
        while irc_msg.find("End of /NAMES list.") == -1:
            irc_msg = self._irc_socket.recv(2048).decode("UTF-8")
            irc_msg = irc_msg.strip('\n\r')
            logging.info(irc_msg)

    def ping(self):
        """ respond to server pings."""
        self._irc_socket.send(bytes("PONG :pingis\n", "UTF-8"))

    def send_message(self, msg, target=None):
        """ sends messages to the target. """
        logging.debug("sending message: " + msg)
        if target is None:
            target = self._channel
        self._irc_socket.send(bytes("PRIVMSG " + target + " :" + msg + "\n", "UTF-8"))

    def privmsg_actions(self, message, name):
        """ PRIVMSG actions """

        print(message, name)

        # greetings
        if message.find('Hi ' + self._name) != -1:
            self.send_message("Hello " + name + "!")

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

            self.send_message(message, target)

    admin_name = property(_get_admin_name)
    exitcode = property(_get_exitcode)
