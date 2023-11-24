#!/usr/bin/env python

import argparse
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

def format_badge(format_str, repository, workflow, branch):
    s1 = format_str.replace("{{repository}}", repository)
    s2 = s1.replace("{{repository}}", repository)
    s3 = s2.replace("{{workflow}}", workflow)
    s4 = s3.replace("{{branch}}", branch)
    
    return s4

def generate_badge_urls(repo, wfs, brs, badge_format):
    res = []
    for wf in wfs:
        br_badges = []
        for br in brs:
            bs = br.split("/")
            badge_ref = format_badge(badge_format, repo, wf, bs[1])
            br_badges.append((badge_ref, br))
        res.append((br_badges, wf))
    return (repo, res)

def generate_markdown(urls):
    (repo, urlss) = urls
    badges = "# List of badges\n"
    for (br_badges, wf) in urlss:
        for (badge_ref, br) in br_badges:
#            print(f"{repo} {wf} {br} {badge_ref}")
            print(f"{badge_ref}")
            badges += f"![][{badge_ref}]\n"
    return badges

def main(argv):
    _program = argv[0]

    args = parse_args(argv[1:])
    if 'markdown' == args.command :
        branches = read_branches()
        urls = generate_badge_urls(args.repository, args.workflows, branches, args.badge_format)
        md = generate_markdown(urls)
        print(md)
    

if __name__ == '__main__':
    main(sys.argv)
