#!/usr/bin/python3
import logging


class IRCBot:
    """ IRC Bot """

    def __init__(self, irc_socket, channel, admin_name, name, exitcode):
        self.irc_socket = irc_socket
        self.channel = channel
        self.admin_name = admin_name
        self.name = name
        self.exitcode = exitcode
        self.irc_socket.send(
            bytes("USER " + self.name + " " + self.name + " " + self.name + " " + self.name + "\n",
                  "UTF-8"))
        self.irc_socket.send(bytes("NICK " + self.name + "\n", "UTF-8"))
        self.join_channel()

    def join_channel(self):
        self.irc_socket.sendall(bytes("JOIN " + self.channel + "\n", "UTF-8"))
        irc_msg = ""
        while irc_msg.find("End of /NAMES list.") == -1:
            irc_msg = self.irc_socket.recv(2048).decode("UTF-8")
            irc_msg = irc_msg.strip('\n\r')
            logging.info(irc_msg)

    def ping(self):
        """ respond to server pings."""
        self.irc_socket.send(bytes("PONG :pingis\n", "UTF-8"))

    def send_message(self, msg):
        """ sends messages to the target. """
        self.irc_socket.send(bytes("PRIVMSG " + self.channel + " :" + msg + "\n", "UTF-8"))

    def privmsg_actions(self, message, name):
        """ PRIVMSG actions """

        # greetings
        if message.find('Hi ' + self.channel) != -1:
            self.channel.sendmsg("Hello " + name + "!")

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

            self.send_message(message)
