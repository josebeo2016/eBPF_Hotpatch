########################################################
# Author: Phucdt
# Updated: Sept 14th, 2021
#
#
#
# Main program is the the "front-end" of the application
# All function for processing is in bpf.py
#########################################################



from argparse import ArgumentParser
import logging
import argparse
import colorlog
import os
import libs.container
import libs.utils as utils
import bpf
import sys
VERSION = "1.0"
DESCRIPTION = "Kubernetes dynamic eBPF policy security"
logger = logging.getLogger("log")

class CLI():
    description = DESCRIPTION
    def __init__(self):
        # self.args contains all parameter for bpf.run()
        opt = ArgumentParser(
            description=self.description,
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        opt.add_argument(
            "-V", "--version", action="store_true",
            help="Show version"
        )
        opt.add_argument(
            "-d", "--debug", action="store_true",
            help="Enable debug log"
        )
        opt.add_argument('-L', '--log-file', help='save log to file')

        #######################################
        # Functional option
        #######################################

        opt.add_argument(
            '-p', '--pid',
            help="container pid"
        )    

        opt.add_argument(
            '-N', '--namespace',
            help="Mount namespace ID follow the reference: bcc/docs/special_filtering.md"
        )

        opt.add_argument(
            '--dockerid',
            help='Docker container ID to apply rule'
        )

        opt.add_argument(
            '--hook',
            help='LSM probe to be used to hook eBPF program'
        )

        opt.add_argument(
            '-f', '--file', type=str,
            # required=True,
            help='Rule file in YAML format'
        )

        opt.add_argument(
            '-F', '--fullpath', type=str,
            help='Full path of inspecting file.'
        )

        opt.add_argument(
            '--inode',
            action="store_true",
            help="Return inode of file given with -F and container ID with --dockerid."
        )



        opt.set_defaults(func=self.run)
        self.args = opt.parse_args()
        if (len(sys.argv)==1):
            opt.print_help()
            sys.exit(1)
        self.setup_logging()

    def setup_logging(self):
        # Setup environment:
        utils.mkpdirs("./log/")
        # logger = logging.getLogger('parser')
        console_formatter = colorlog.ColoredFormatter(
            '%(log_color)s%(asctime)s|%(levelname)s|%(message)s')
        file_formatter = logging.Formatter(
            '%(asctime)s|%(levelname)s| %(message)s')
        stdout = colorlog.StreamHandler(sys.stdout)
        stdout.setFormatter(console_formatter)
        logger.addHandler(stdout)
        logger.setLevel(logging.INFO)
        if self.args.debug:
            # print("OK")
            logger.setLevel(logging.DEBUG)
        if self.args.log_file:
            handler = logging.FileHandler(self.args.log_file, 'w', delay=True)
            handler.setFormatter(file_formatter)
            logger.addHandler(handler)
    
    def run(self):
        if (self.args.version):
            logger.info(VERSION)
            return 0
        bpf.run(self.args)
        return 0

def main():
    cli = CLI()
    sys.exit(cli.run())

if __name__ == "__main__":
    main()