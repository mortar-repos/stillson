#!/usr/local/bin/python

import os
import sys
from optparse import OptionParser
from mako.template import Template

def get_content(template_file):
    template_file = open(template_file,mode='r')
    template_lines = template_file.readlines()
    template_content = ''
    for line in template_lines:
        template_content = template_content + line
    return template_content


def main():
    parser = OptionParser(usage="usage: %prog template_file [options]",
                          version="%prog 1.0.0")
    parser.add_option('-o', '--output',
                      action='store',
                      dest='output',
                      default='client.cfg',
                      help='[DEFAULT: %default] the path for the output file that gets created')
    (options,args ) = parser.parse_args()

    if len(args) < 1:
        error_msg = 'ERROR: You must specify a template file'
        print error_msg
        sys.exit(1)

    template_file = args[0]
    try:
       with open(template_file):
           pass
    except IOError:
        print 'ERROR: The template file of %s does not exist'%template_file
        sys.exit(1)

    template_content = get_content(template_file)
    output_content = Template(template_content).render(**os.environ)
    template_output = open(options.output,mode='w')
    template_output.write(output_content)


if __name__ == '__main__':
    main()
