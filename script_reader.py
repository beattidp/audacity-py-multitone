#!/usr/bin/env python3

import sys
import re
from pipeclient import PipeClient
from pprint import pprint
import json
from jinja2 import Environment, FileSystemLoader
import time
from datetime import datetime

''' render jinja2 template and feed result to Audacity scripting socket interface
'''
REGEX_COMMENT = "$|^#.*"

timeout = 10 # seconds
client = PipeClient()
inpfile = sys.stdin
oupfile_name = 'expanded_template.txt'
script_commands = []

def do_expand_template():
    with open('templates/multitone_config.json','r') as json_file:
        config_data = json.load(json_file)

    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template('iterate_multitone.j2')
    #raise Exception
    output = template.render(config_data)
    with open(oupfile_name,'w') as oupfile:
        print(output,file=oupfile)
    print(output,file=sys.stderr)

def do_parse_template():
    with open(oupfile_name,'r') as inpfile:
        while len(buffer := inpfile.readline()):
            buffer_item = buffer.strip()
            reply = ''
            if re.match(REGEX_COMMENT,buffer):
                print(f'COMMENT: {buffer}',file=sys.stderr)
            else:
                if len(buffer_item):
                    script_commands.append(buffer_item)

def run_scripted(commands):
    print(f'number of commands: {len(commands)}')
    for message in commands:
        reply = ''
        print(f'COMMAND: {message}',file=sys.stderr)
        start = time.time()
        client.write(message)
        while reply == '':
            time.sleep(0.1)  # allow time for reply
            if time.time() - start > timeout:
                reply = 'PipeClient: Reply timed-out.'
            else:
                reply = client.read()
        print(f'RESPONSE: {reply}',file=sys.stderr)
        if not reply.split('\n')[0].endswith('OK'):
            break
        time.sleep(0.2)


if __name__ == "__main__":
    timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    print(f'{timestamp} -- Begin Execution --------------------', file=sys.stderr)
    do_expand_template()
    do_parse_template()
    #from pprint import pprint as pp
    #pp(script_commands)

    run_scripted(script_commands)
