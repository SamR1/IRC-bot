#!/usr/bin/python3
import logging
import random
from pyowm import OWM
from .db import Base, Greetings
from sqlalchemy.orm import sessionmaker


class IRCBot:
    """ IRC Bot """

    def __init__(self, irc_socket, irc_bot_param, greetings, engine):
        self._irc_socket = irc_socket
        self._channel = irc_bot_param.channel
        self._admin_name = irc_bot_param.admin_name
        self._name = irc_bot_param.bot_name
        self._exitcode = irc_bot_param.exitcode
        self._exitmsg = irc_bot_param.exitmsg
        self._entermsg = irc_bot_param.entermsg
        self._greetings = greetings
        self._engine = engine
        self._owmapi = irc_bot_param.owmapi

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

        logging.debug("Joining channel: " + self._channel)

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

    def get_info(self, message):
        """ getting weather info for now """

        pos = message.find("give me the weather for ")
        if pos != -1:
            pos += 24
            city = message[pos:]
            city = city.split(' ')[0] if city != '' else ''
            if city != '':
                self.get_weather_info(city)

    def get_weather_info(self, city):
        """ getting weather info from OpenWeatherMap from a city name """

        try:
            if self._owmapi is None or self._owmapi == '':
                self.send_message("Sorry, I can't get the weather data. OpenWeatherMap API is "
                                  "missing.")
                return

            owm = OWM(self._owmapi)
            obs_list = owm.weather_at_places(city, searchtype='accurate')
            nb = len(obs_list)
            if nb == 0:
                self.send_message("Sorry, no location found for '{}'".format(city))
            else:
                self.send_message("{} location(s) found".format(nb))
                for obs in obs_list:

                    l = obs.get_location()
                    location = l.get_name()
                    country = l.get_country()

                    w = obs.get_weather()
                    status = w.get_detailed_status()
                    temp = w.get_temperature(unit='celsius')['temp']

                    weather = "{} ({}): the current status is '{}' and the temperature is {}°C".format(
                        location, country, status, temp)
                    self.send_message(weather)
        except Exception as e:
            logging.error(str(e.args))
            self.send_message("Sorry, something wrong happened, I can't get the weather data.")

    def update_greetings(self, greeting):
        """ Adding new greeting, if not already exists """

        try:
            Base.metadata.bind = self._engine
            DBSession = sessionmaker()
            DBSession.bind = self._engine
            session = DBSession()

            greeting_already_exists = session.query(Greetings)\
                                        .filter(Greetings.greeting == greeting).first()
            if not greeting_already_exists:
                new_greeting = Greetings(greeting=greeting)
                session.add(new_greeting)
                session.commit()
                greeting_added = session.query(Greetings) \
                    .filter(Greetings.greeting == greeting).first()
                self._greetings.append(greeting_added)
                self.send_message("New greeting added, you can it now.")
            else:
                self.send_message("This greeting already exists, try another one.")

        except Exception as e:
            logging.error(str(e.args))
            self.send_message("Sorry something wrong happened, can you retry.")
            return False

    def add_greetings(self, message):

        pos = message.find("add greeting ")
        if pos != -1:
            pos += 13
            greeting = message[pos:]
            greeting = greeting.split('"')[1] if greeting != '' else ''
            if greeting != '':
                self.update_greetings(greeting)
            else:
                self.send_message("Sorry I don't understand. Can you rephrase the new greeting?")

    def privmsg_actions(self, message, name):
        """ PRIVMSG actions """

        # greetings
        if message.find('Hi ' + self._name) != -1 or \
           message.find('Hello ' + self._name) != -1:
            greeting_nb = len(self._greetings) - 1
            i = random.randint(0, greeting_nb)
            self.send_message(self._greetings[i].greeting + " " + name + "!")

        if message.find(self._name + " give me ") != -1:
            self.get_info(message)

        if message.find(self._name + " add greeting ") != -1:
            if name.lower() == self._admin_name.lower():
                self.add_greetings(message)
            else:
                self.send_message("You must be an admin to add a new greeting.")

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
        """ Analyze message in order to trigger the associated action """

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
