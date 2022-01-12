'''Entrypoint of the application'''
import sys
import textwrap
import importlib

from uuid import uuid4
from argparse import ArgumentParser, RawTextHelpFormatter

from utils.parsers import TypeParser


# Create the main parser
parser = ArgumentParser(
    description='Manipulate sports, events, markets and selections',
    formatter_class=RawTextHelpFormatter
)
# Create a subparser to split arguments per command
subparsers = parser.add_subparsers(help='sub-command help', dest='command')

# Help text
help_text = '''\
- Sport: {"name": "Football", "display_name": "Football/Soccer", "order": 0, "is_active": true}
- Event: {"sport_id": "uuid...", "name": "Event1", "type": "inplay|preplay", \
"status": "inplay|preplay|ended", "is_active": true}
- Market: {"event_id": "uuid...", "name": "Market1", "display_name": "Market 1", \
"order": 0, "schema": 1, "columns": 5, "is_active": true}
- Selection: {"market_id": "uuid...", "name": "Selection1", "price": 10.01, \
"outcome": "win|void|lose|place|unsettled", "is_active": true}
'''

# Create the parser for "create"
create_sub = subparsers.add_parser(
    'create', help='Create a resource', formatter_class=RawTextHelpFormatter)
create_sub.add_argument(
    '-t', '--type', dest='type', type=TypeParser.check_type, required=True, help='Type to impact'
)
create_sub.add_argument(
    '-d', '--data', dest='data', type=TypeParser.check_json, required=True,
    help=f'Data to insert for a resource:\n{help_text}'
)

# Create the parser for "update"
update_sub = subparsers.add_parser(
    'update', help='Update a resource', formatter_class=RawTextHelpFormatter)
update_sub.add_argument(
    '-i', '--id', dest='id', type=TypeParser.check_uuid, required=True, help='UUID of the resource'
)
update_sub.add_argument(
    '-t', '--type', dest='type', type=TypeParser.check_type, required=True, help='Type to impact'
)
update_sub.add_argument(
    '-d', '--data', dest='data', type=TypeParser.check_json, required=True,
    help=f'Data to update for a resource:\n{help_text}'
)

# Create the parser for "delete"
delete_sub = subparsers.add_parser(
    'delete', help='Delete a resource', formatter_class=RawTextHelpFormatter)
delete_sub.add_argument(
    '-i', '--id', dest='id', type=TypeParser.check_uuid, required=True, help='UUID of the resource'
)
delete_sub.add_argument(
    '-t', '--type', dest='type', type=TypeParser.check_type, required=True, help='Type to impact'
)

# Get formatted data
args_dict = parser.parse_args(sys.argv[1:])

# Dynamically instantiate the proper module and call the method associated to the command line
command = args_dict.command
if command in ['create', 'update']:
    getattr(importlib.import_module('modules'), args_dict.type.capitalize())() \
        .upsert(getattr(args_dict, 'id', uuid4()), args_dict.data)
elif command == 'delete':
    getattr(importlib.import_module('modules'), args_dict.type.capitalize())() \
        .delete(args_dict.id)
elif command == 'search':
    getattr(importlib.import_module('modules'), args_dict.type.capitalize())() \
        .search(args_dict.data)
