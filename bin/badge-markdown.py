#!/usr/bin/env python

import argparse
import copy
import fileinput
import sys


def parse_args(argv):
    top_parser = argparse.ArgumentParser()
    cmd_parser = top_parser.add_subparsers(dest='command', required=True)

    markdown_parser = cmd_parser.add_parser('markdown', help='generate badges markdown')

    markdown_parser.add_argument('--repository', help='repository to be badged', type=str, required=True)
    markdown_parser.add_argument('--workflows', help='workflow file name in .github/workflow/', nargs='*', type=str, required=True)
    markdown_parser.add_argument('--badge-format', help='format of badge', type=str, required=True)

    return top_parser.parse_args(argv)

def read_branches():
    res = []
    lines = sys.stdin.readlines()
    res = [s.strip() for s in lines]
    return res

def format_badge(format, badgedic):
    res = copy.copy(format)
    for (key, val) in badgedic.items():
        res = res.replace(f"{{{key}}}", val)
    
    return res


def generate_markdown(repo, wfs, brs, badge_format):
    md = "# List of badges\n\n"
    for br in brs:    
        md += f"## Badges for {br} branch\n\n"
        for wf in wfs:
            bs = br.split("/")
            badge_ref = format_badge(badge_format, {'repository':repo , 'workflow':wf, 'branch':bs[1]})
            md += f"![]({badge_ref})\n"
    return md


def main(argv):
    _program = argv[0]

    args = parse_args(argv[1:])
    if 'markdown' == args.command :
        branches = read_branches()
        md = generate_markdown(args.repository, args.workflows, branches, args.badge_format)
        print(md)
    

if __name__ == '__main__':
    main(sys.argv)
