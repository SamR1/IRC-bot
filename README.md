# IRC Bot

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/04044add92bd444d83bb1e1b8e494540)](https://www.codacy.com/app/SamR1/IRC-bot?utm_source=github.com&utm_medium=referral&utm_content=SamR1/IRC-bot&utm_campaign=badger) [![Code Climate](https://codeclimate.com/github/SamR1/IRC-bot/badges/gpa.svg)](https://codeclimate.com/github/SamR1/IRC-bot)

a simple IRC bot in Python (realized during the [CodingAcademy](http://www.coding-academy.fr/en/)
 training)  
(_work in progress_)  


## Requirements
* For basic usage
    - Python 3 (tested with 3.6)
    - [PyYAML](http://pyyaml.org)
    - [PyOWM](https://github.com/csparpa/pyowm) and a valid API key from [OpenWeatherMap](https://home.openweathermap.org/users/sign_up)
    - [SQLAlqchemy](https://www.sqlalchemy.org/) and [SqlAlchemy_utils](https://sqlalchemy-utils.readthedocs.io/en/latest/)
* For [unit tests](tests/README.md)
    - [pytest](https://docs.pytest.org/en/latest/)
    - [pytest-catchlog](https://pypi.python.org/pypi/pytest-catchlog)
* For build
    - [cx_Freeze](https://github.com/anthony-tuininga/cx_Freeze)


## Usage
* clone the repo :
```bash
$ git clone https://github.com/SamR1/IRC-bot.git
```

* install the requirements 
```bash
# for all requirements
$ sudo pip install -r requirements.txt

# for IRC BOT only (w/o tests or build)
$ sudo pip install pyyaml pyowm 
```

* rename the parameter file to `config.yml` and update it:  

| parameter |            | description                                      |  
|-----------|------------|--------------------------------------------------|  
| main_bot  |            |                                                  |
|           | irc_server | example: "chat.freenode.net"                     |
|           | irc_port   | example: 6667                                    |
|           | channel    | IRC channel                                      |
|           | bot_name   | bot name                                         |
|           | admin_name | nickname of Bot Admin                            |
|           | entermsg   | message, the bot sends when it joins the channel |
|           | exitcode   | message to to end the bot script                 |
|           | exitmsg    | message, the bot sends when it exits the channel | 
| owmapi    |            | a valid key from OpenWeatherMap                  |

* The current version of the IRC Bot can:
    * say 'Hello' (in 6 languages, randomly) when you say 'Hi' or 'Hello' to it
    ```
    <SamR1> Hello MyPyBot
    <MyPyBot> Hola SamR1!
    ```
    You can add new greetings with the following command:
    ```bash
    <SamR1> Hello MyPyBot
    <MyPyBot> Hola SamR1!
    <SamR1> MyPyBot add greeting "Ahoy"
    <MyPyBot> New greeting added, you can it now.
    <SamR1> Hello MyPyBot
    <MyPyBot> Hola SamR1!
    <SamR1> Hello MyPyBot
    <MyPyBot> Ahoy SamR1!
    ```
    * send private message with `.tell [target] [message]` command
    * get the weather (with the command: `[bot_name] give me the weather for ` ) 
     ```
    <SamR1> MyPyBot give me the weather for London
    <MyPyBot> 5 location(s) found
    <MyPyBot> London (GB): the current status is 'few clouds' and the temperature is 12.78°C
    <MyPyBot> London (US): the current status is 'scattered clouds' and the temperature is 27.0°C
    <MyPyBot> London (US): the current status is 'sky is clear' and the temperature is 20.99°C
    <MyPyBot> London (US): the current status is 'sky is clear' and the temperature is 18.54°C
    <MyPyBot> London (US): the current status is 'sky is clear' and the temperature is 28.4°C
     ```
* To stop the script, just enter the exitcode with the Bot name:
```
<SamR1> Bye MyPyBot
<MyPyBot> Why me... ? Snif... OK, I'm leaving :'(
* MyPyBot a quitté (Client Quit)
```
Only the admin can stop the script.

## Unit tests
see [README.me](tests/README.md)

## Build
To build an executable, use [cx_Freeze](https://github.com/anthony-tuininga/cx_Freeze):
```bash
[sam@sam-pc ircbot]$ python setup.py build
```
Don't forget to update the configuration file.

Warning: since the use of SQL Alchemy, an error occurs:
```bash
[sam@sam-pc exe.linux-x86_64-3.6]$ ./IRCBot 
Traceback (most recent call last):
  File "/usr/lib/python3.6/site-packages/cx_Freeze/initscripts/__startup__.py", line 14, in run
    module.run()
  File "/usr/lib/python3.6/site-packages/cx_Freeze/initscripts/Console.py", line 26, in run
    exec(code, m.__dict__)
  File "app.py", line 5, in <module>
  File "/usr/lib/python3.6/site-packages/sqlalchemy_utils/__init__.py", line 49, in <module>
    from .i18n import TranslationHybrid  # noqa
  File "/usr/lib/python3.6/site-packages/sqlalchemy_utils/i18n.py", line 10, in <module>
    import babel
  File "/usr/lib/python3.6/site-packages/babel/__init__.py", line 20, in <module>
    from babel.core import UnknownLocaleError, Locale, default_locale, \
  File "/usr/lib/python3.6/site-packages/babel/core.py", line 14, in <module>
    from babel import localedata
  File "/usr/lib/python3.6/site-packages/babel/localedata.py", line 35, in <module>
    _dirname = os.path.join(get_base_dir(), 'locale-data')
  File "/usr/lib/python3.6/site-packages/babel/localedata.py", line 27, in get_base_dir
    basedir = sys._MEIPASS
AttributeError: module 'sys' has no attribute '_MEIPASS'
```
see issue [Issue #2](https://github.com/SamR1/IRC-bot/issues/2)

## Sources
* https://linuxacademy.com/blog/geek/creating-an-irc-bot-with-python3/
