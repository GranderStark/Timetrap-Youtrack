import argparse
from collections import namedtuple

import yaml

from .handler import handle
from .application import app
from .constants import TYRC_EXAMPLE, HOME
from .sqlite_part import SqlLitePart


def add_part(part_class):
    configuration_name = part_class.__configuration_name__
    current_config = app.configuration.get(configuration_name)
    return part_class(config=current_config)


def get_configuration(file_name: None) -> dict:
    if not file_name:
        file_name = "{}/.tyrc".format(HOME)
    try:
        with open(file_name, 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
    except FileNotFoundError as e:
        print('NO CONFIGURATION FOUND')
        print('fill file ".tyrc" in your home directory"')
        print('Example:')
        print(TYRC_EXAMPLE)
        raise

    return cfg


def parse_command_line():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-c,--config', help='path to config file', required=False)
    arg_parser.add_argument('-d, --days', help='quantity of days before today', type=int, required=False)
    arg_parser.add_argument('-s, --since', help='from date like "2018-11-01"', required=False)
    arg_parser.add_argument('-t, --till', help='till date like "2018-11-02"', required=False)
    arg_parser.add_argument(
        '-v, --verbose',
        help='more output',
        const=True,
        action='store_const',
        default=False,
    )

    arg_parser.add_argument('-p, --previous_day', help='one day before', required=False)

    Args = namedtuple('Args', ['config', 'days', 'previous_day', 'since', 'till', 'verbose'])
    raw_args = arg_parser.parse_args()
    arg = Args(
        config=getattr(raw_args, 'c,__config'),
        days=getattr(raw_args, 'd, __days'),
        previous_day=getattr(raw_args, 'p, __previous_day'),
        since=getattr(raw_args, 's, __since'),
        till=getattr(raw_args, 't, __till'),
        verbose=getattr(raw_args, 'v, __verbose'),
    )

    return arg


def run():
    app.args = parse_command_line()

    app.configuration = get_configuration(app.args.config)
    app.db_part = add_part(SqlLitePart)

    handle()
