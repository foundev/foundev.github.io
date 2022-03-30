#!/usr/bin/env python3
import os
import argparse

DRY_RUN = False


def read_md_file(md):
    found_header_start = False
    found_header = False
    read = False
    lines = []
    header = ["---"]
    title = ""
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
                if line.startswith("title:"):
                    title_text = ":".join(line.split(":")[1:]).strip().strip("'")
                    title = "<h1>"  + title_text + "</h1>"
                else:
                    header.append(line)
    header.append("---")
    header_str = "\n".join(header)
    body_str = "\n".join(lines)
    return header_str + "\n" +  title + "\n" + body_str


def run():
    post_dir = "_posts"
    posts = os.listdir(post_dir)
    for post in posts:
        html = ""
        with open(post_dir + "/" + post, "r") as f:
            html = read_md_file(f.read())
        print("html generated is\n" + html)
        print("writng file " + post)
        if not DRY_RUN:
            with open( post_dir + "/" + post, mode="w") as f:
                f.write(html)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', help='do a try run and do not actually execute the script', action=argparse.BooleanOptionalAction)
    args = parser.parse_args()
    print(args)
    DRY_RUN = args.dry_run
    run()
