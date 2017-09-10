import loadparam
from ircbot.classes.ircbot import IRCBot
from ircbot.classes.ircsocket import IRCSocket


# parameters loading, irc socket and bot init
param = loadparam.loading_param('../ircbot/config.yml')
IRC_SERVER = param['main_bot']['irc_server']
IRC_PORT = param['main_bot']['irc_port']
IRC_CHANNEL = param['main_bot']['channel']
IRC_ADMIN = param['main_bot']['admin_name']
BOT_NAME = param['main_bot']['bot_name']
EXITCODE = param['main_bot']['exitcode']
EXITMSG = param['main_bot']['exitmsg']
ENTERMSG = param['main_bot']['entermsg']

irc_socket = IRCSocket(IRC_SERVER, IRC_PORT)
irc_socket.connect()
main_bot = IRCBot(irc_socket.irc_socket, param)


def test_join_channel(caplog):
    """ testing bot init and joining channel (from parameter file)"""

    main_bot.join_channel()
    i = len(caplog.records) - 1
    assert caplog.records[i - 1].message.find(BOT_NAME + " " + IRC_CHANNEL + " :End of /NAMES list")
    assert caplog.records[i].message.find(ENTERMSG)


def test_send_message(caplog):
    """ testing bot sending PRIVMSG """

    message = "@@ unit test message @@"
    main_bot.send_message(message)
    i = len(caplog.records) - 1
    assert caplog.records[i].message.find(BOT_NAME + " " + IRC_CHANNEL + " " + message)
    main_bot.quit_channel()


def test_quit_channel(caplog):
    """ testing quitting channel """

    main_bot.quit_channel()
    i = len(caplog.records) - 1
    assert caplog.records[i - 1].message.find(BOT_NAME + " " + IRC_CHANNEL + " " + EXITMSG)
    assert caplog.records[i].message.find(EXITMSG)
