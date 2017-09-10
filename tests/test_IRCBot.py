import loadparam
from ircbot.classes.ircbot import IRCBot
from ircbot.classes.ircsocket import IRCSocket


param = loadparam.loading_param()
irc_socket = IRCSocket(param['main_bot']['irc_server'], param['main_bot']['irc_port'])
irc_socket.connect()


def test_bot_init(caplog):
    main_bot = IRCBot(irc_socket.irc_socket,
                      param['main_bot']['channel'],
                      param['main_bot']['admin_name'],
                      param['main_bot']['bit_name'],
                      param['main_bot']['exitcode'],
                      param['main_bot']['exitmsg'])
    i = len(caplog.records) - 1
    assert caplog.records[i].message.find(":End of /NAMES list")
