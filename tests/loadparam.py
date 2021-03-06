import yaml

def loading_param(filename):
    with open(filename, 'r') as stream:
        try:
            PARAM = yaml.safe_load(stream)
        except yaml.YAMLError as error:
            PARAM = None
            logging.error(error)

    if PARAM is None:
        logging.error("Parameters not defined")
        exit(1)
    else:
        return PARAM
