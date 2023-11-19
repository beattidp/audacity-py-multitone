#!/usr/bin/env python3

import sys
import re
from pipeclient import PipeClient
from pprint import pprint
import json
from jinja2 import Environment, FileSystemLoader
import time

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

def run_scripted():
    with open('expanded_template.txt','r') as inpfile:
        while buffer := inpfile.readline():
            reply = ''
            if re.match(REGEX_COMMENT,buffer):
                print(f'COMMENT: {buffer}',file=sys.stderr)
            else:
                script_commands.append(buffer.strip())
                message = buffer.strip()
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
                if not reply.endswith('OK'):
                    break

if __name__ == "__main__":
    do_expand_template()
    run_scripted()
