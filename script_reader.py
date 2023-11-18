#!/usr/bin/env python3

import sys
import re
from pipeclient import PipeClient
from pprint import pprint

REGEX_COMMENT = "$|^#.*"

client = PipeClient()
inpfile = sys.stdin

script_commands = []

#with open('scripted.txt','r') as inpfile:
def test():
    while buffer := inpfile.readline():
        #buffer = buffer.strip()
        if not re.match(REGEX_COMMENT,buffer):
            script_commands.append(buffer.strip())
        else:
            print(f'COMMENT: {buffer}',file=sys.stderr)
    pprint(script_commands)

test()