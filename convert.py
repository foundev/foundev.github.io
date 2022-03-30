#!/usr/bin/env python3
import os
import argparse
import markdown

DRY_RUN = False


def read_md_file(md):
    found_header_start = False
    found_header = False
    read = False
    lines = []
    header = ["---"]
    for line in md.split("\n"):
        if read:
            lines.append(line)
        else:
            if line == "---":
                if found_header_start:
                    read = True
                else:
                    found_header_start = True
            else:
                header.append(line)
    header.append("---")
    header_str = "\n".join(header)
    body_str = "\n".join(lines)
    return header_str, body_str


def convert_to_html(md):
    header, markdown_only = read_md_file(md)
    html = markdown.markdown(markdown_only)
    return header + "\n" + html


def convert_file_name(file_name):
    tokens = file_name.split("-")
    year = tokens[0]
    month  = tokens[1]
    day = tokens[2]
    name = "-".join(tokens[3:])[:-3]
    dirs = "/".join([year, month, day])
    return dirs,  name + ".html"

def run():
    post_dir = "_posts"
    posts = os.listdir(post_dir)
    for post in posts:
        dirs, file_name = convert_file_name(post)
        print("making dirs " + dirs)
        os.makedirs(dirs, exist_ok=True)
        html = ""
        with open(post_dir + "/" + post, "r") as f:
            html = convert_to_html(f.read())
        print("html generated is\n" + html)
        file_to_write = dirs + "/" + file_name 
        print("writng file " + post + " to " + file_to_write)
        if not DRY_RUN:
            with open(file_to_write, mode="w") as f:
                f.write(html)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', help='do a try run and do not actually execute the script', action=argparse.BooleanOptionalAction)
    args = parser.parse_args()
    print(args)
    DRY_RUN = args.dry_run
    run()
