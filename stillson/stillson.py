#
# Copyright 2013 Mortar Data Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

#!/usr/bin/python
import os
import sys
from optparse import OptionParser
from mako.template import Template

class StillsonException(Exception):
    pass

class StillsonMissingEnvVariable(StillsonException):
    pass

#TODO only list environment variables relevant to template
def list_available_env_keys():
    sys.stderr.write("Available configuration variables:\n")
    for key in os.environ.keys():
        sys.stderr.write("* %s\n"%key)
    

def render(template_path,output_file,debug_level):
    template = Template(filename=template_path,strict_undefined = True)
    try:
        output_content = template.render(**os.environ)
    except NameError as template_error:
        missing_variable = str(template_error).split("'")[1]
        sys.stderr.write("Configuration Expansion Error\n\n") 
        sys.stderr.write("The configuration variable %s is not defined.\n\n"%missing_variable)
        if debug_level == "debug":
            list_available_env_keys()
        raise StillsonMissingEnvVariable()
    output_file.write(output_content)
    output_file.flush()


def main():
    parser = OptionParser(usage="usage: %prog template_path [options]",
                          version="%prog 1.0.0")
    parser.add_option('-o', '--output',
                      action='store',
                      dest='output',
                      help='[DEFAULT: %default] the path for the output file that gets created'),
    parser.add_option('-d', '--debug',
                      type='choice',
                      action='store',
                      dest='debug_level',
                      default='warn',
                      choices=['warn','debug'], #only support warn until debug TODO is done
                      help='[DEFAULT: %default] debug message level')

    (options,args ) = parser.parse_args()

    if len(args) < 1:
        error_msg = 'ERROR: You must specify a template file\n'
        sys.stderr.write(error_msg)
        sys.exit(1)

    template_path = args[0]
    if options.output:
        output_file = open(options.output,'w')
    else:
        output_file = sys.stdout

    try:
        render(template_path,output_file,options.debug_level)
        return 0
    except Exception, err:
        return 1
      
    if options.output:
        output_file.close()


if __name__ == '__main__':
    sys.exit(main())
