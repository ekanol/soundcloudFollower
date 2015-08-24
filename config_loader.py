import json
import logging

logger = logging.getLogger(name='config_loader')

required_root_values = ['CLIENT_ID',
                        'CLIENT_SECRET',
                        'USERNAME',
                        'PASSWORD']

def config_setup(config_file):
    logger.info('Loading: %s', config_file)

    configuration = {}

    with open(config_file) as json_data_file:
        data = json.load(json_data_file)

    failed = False

    # Test for root elements
    for required_value in required_root_values:
        if required_value not in data:
            failed = True
            logger.error('Missing required configuration value: %s', required_value)
        else:
            configuration[required_value] = data[required_value]

    if failed:
        raise Exception('Missing keys from data. See log for details.')

    logger.info('Configuration loaded')

    return configuration