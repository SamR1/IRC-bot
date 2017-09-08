#!/usr/bin/python3
import socket
import logging


class IRCSocket:
    """  IRC Socket """

    def __init__(self, irc_server, irc_port):
        self.irc_server = irc_server
        self.irc_port = irc_port
        self.irc_socket = None

    def connect(self):
        try:
            self.irc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.irc_socket.connect((self.irc_server, 6667))
            logging.debug("Connection to the server OK")
        except Exception:
            logging.error("Cannot connect to the server")
