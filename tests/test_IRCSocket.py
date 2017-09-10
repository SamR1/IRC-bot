import loadparam
from ircbot.classes import ircsocket


param = loadparam.loading_param('../../ircbot/config.yml')


def test_connexion(caplog):
    irc_socket = ircsocket.IRCSocket(param['main_bot']['irc_server'], param['main_bot']['irc_port'])
    irc_socket.connect()
    assert caplog.records[0].message == "Connection to the server OK"
