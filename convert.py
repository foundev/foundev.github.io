#!/usr/bin/env python3
import os
import argparse
import markdown

DRY_RUN = False


def convert_to_html(md):
    return markdown.markdown(md)

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
