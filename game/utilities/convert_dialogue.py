#!/usr/bin/env python
"""Convert YAML dialogue files from the Techdemo1 format to the new Techdemo2
format.

@author: M. George Hansen <technopolitica@gmail.com>
"""
import os.path
import sys
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(sys.argv[0]),
                                 os.path.pardir)))
import shutil
import logging

from scripts.common.optionparser import OptionParser
from scripts.dialogueparser import (OldYamlDialogueParser, YamlDialogueParser,
    DialogueFormatError)

def backup_file(filepath):
    dirpath = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    
    shutil.copy2(filepath, os.path.join(dirpath,
                                        '.'.join([filename, 'backup'])))

def convert_dialogue_file(filepath, backup):
    logging.info('processing {0}...'.format(filepath))
    dummy, extension = os.path.splitext(filepath)
    if (not extension == '.yaml'):
        logging.info('    skipping {0}: not a yaml file'.format(filepath))
        return 1
    with file(filepath, 'r') as dialogue_file:
        old_parser = OldYamlDialogueParser()
        new_parser = YamlDialogueParser()
        try:
            dialogue = old_parser.load(dialogue_file)
        except DialogueFormatError as error:
            logging.info(
                '    unable to convert {0}: unrecognized dialogue format'
                .format(filepath)
            )
            return 1
    if (backup):
        backup_file(filepath)
    logging.info('    backed up {0} as {0}.backup'.format(filepath))
    with file(filepath, 'w') as dialogue_file:
        new_parser.dump(dialogue, dialogue_file)
    logging.info('    successfully converted {0}!'.format(filepath))

usage_message = '''\
usage: convert_dialogue.py [-h] [-n] [-v] [-q] file_or_dir
Convert YAML dialogue files written in Techdemo1 syntax to the new Techdemo2
syntax.

    -h, --help             show this help message
    -n, --no-backup        don't backup files before converting them
    -v, --verbose          increase the verbosity of the script logger; may be
                               specified multiple times to increase the logger
                               output
    -q, --quiet            decrease the verbosity of the script logger; may be
                              specified multiple times to decrease the logger
                              output

If the file_or_dir argument is a directory, then this script will attempt to
convert all .yaml files in the directory that contain valid dialogues.

By default all processed files are first backed up by adding a ".backup" suffix
to the filename + extension. Backups can be disabled by passing the -n option
to the script.
'''

def main(argv=sys.argv):
    # Options.
    backup = True
    logging_level = logging.WARNING
    
    option_parser = OptionParser(usage=usage_message, args=argv[1:])
    for option in option_parser:
        if (option == '-h' or option == '--help'):
            print(option_parser.usage)
            sys.exit(0)
        elif (option == '-n' or option == '--no-backup'):
            backup = False
        elif (option == '-v' or option == '--verbose'):
            logging_level -= 10
        elif (option == '-q' or option == '--quiet'):
            logging_level += 10
        else:
            # invalid option
            message = '"{0}" is not a valid argument or option'.format(option)
            option_parser.error(message)
    logging.basicConfig(format='%(message)s', level=logging_level,
                        stream=sys.stdout)
    
    path = option_parser.get_next_prog_arg()
    if (os.path.isdir(path)):
        for filepath in os.listdir(path):
            qualified_filepath = os.path.join(path, filepath)
            if (not os.path.isfile(qualified_filepath)):
                continue
            convert_dialogue_file(qualified_filepath, backup=backup)
    else:
        convert_dialogue_file(path, backup=backup)

if __name__ == '__main__':
    main()