#!/usr/bin/python3
import logging
import random


class IRCBot:
    """ IRC Bot """

    def __init__(self, irc_socket, param):
        self._irc_socket = irc_socket
        self._channel = param['main_bot']['channel']
        self._admin_name = param['main_bot']['admin_name']
        self._name = param['main_bot']['bot_name']
        self._exitcode = param['main_bot']['exitcode'] + self._name
        self._exitmsg = param['main_bot']['exitmsg']
        self._entermsg = param['main_bot']['entermsg']
        self._greetings = ["Hello", "Bonjour", "Hallo", "Buongiorno", "Hola", "Namaste"]

    def _get_admin_name(self):
        """ Function to get admin name"""
        return self._admin_name

    def _get_exitcode(self):
        """ Function to get exitcode"""
        return self._exitcode

    def _get_exitmsg(self):
        """ Function to get exitmsg"""
        return self._exitmsg

    def join_channel(self):
        """ Joining Channel and eventually changing nickname if already used """

        logging.debug("joining channel: " + self._channel)

        self._irc_socket.send(
            bytes("USER " + self._name + " " + self._name + " " + self._name + " " + self._name +
                  "\n", "UTF-8"))
        self._irc_socket.send(bytes("NICK " + self._name + "\n", "UTF-8"))
        self._irc_socket.sendall(bytes("JOIN " + self._channel + "\n", "UTF-8"))

        irc_msg = ""
        nick_attempts = 0
        while irc_msg.find("End of /NAMES list.") == -1:
            irc_msg = self._irc_socket.recv(2048).decode("UTF-8")
            irc_msg = irc_msg.strip('\n\r')
            logging.info(irc_msg)

            if nick_attempts > 2:
                logging.info("All nickname changes failed. Quiting...")
                return False
            elif irc_msg.find("Nickname is already in use") != -1:
                self._name += "_"
                self._exitcode += "_"
                nick_attempts += 1
                logging.info("Changing nickname, attempt n°{}: {}".format(nick_attempts,
                             self._name))
                self._irc_socket.send(bytes("NICK " + self._name + "\n", "UTF-8"))
                self._irc_socket.sendall(bytes("JOIN " + self._channel + "\n", "UTF-8"))

        self.send_message(self._entermsg)
        return True

    def quit_channel(self):
        self.send_message(self._exitmsg)
        self._irc_socket.send(bytes("QUIT \n", "UTF-8"))

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

        # greetings
        if message.find('Hi ' + self._name) != -1 or \
           message.find('Hello ' + self._name) != -1:
            i = random.randint(0, 5)
            self.send_message(self._greetings[i] + " " + name + "!")

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

    def analyse_msg(self, irc_msg):
        # check if the message is a private message
        if irc_msg.find("PRIVMSG") != -1:
            logging.debug("PRIVMSG")
            name = irc_msg.split('!', 1)[0][1:]
            message = irc_msg.split('PRIVMSG', 1)[1].split(':', 1)[1]

            # Usernames (at least for Freenode) are limited to 16 characters.
            if len(name) < 17:
                logging.debug("Name from valid usernames")

                if name.lower() == self._admin_name.lower() and message.rstrip() == \
                        self._exitcode:
                    self.quit_channel()
                    return None
                else:
                    self.privmsg_actions(message, name)

        elif irc_msg.find("PING :") != -1:
            self.ping()
        return True


    admin_name = property(_get_admin_name)
    exitcode = property(_get_exitcode)
    exitmsg = property(_get_exitmsg)
