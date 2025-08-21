#!/usr/bin/env python3
import os
import re
import csv
import ast
from frontmatter import Post, dump

# bags of notes: Consideration/ Dataset/  Domain/  Need/  Organisation/  Role/	Theme/	User/

fixup = {
    "Tag": {
        "Bng": {"name": "BNG"},
        "Nsip": {"name": "NSIP"},
        "Nist": {"name": "NIST"},
        "Odp": {"name": "ODP"},
        "Pdr": {"name": "PDR"},
    }
}


def asTag(name, prefix=""):
    name = "".join(name.title().split())
    return prefix + fixup["Tag"].get(name, {"name": name})["name"]


def asNoteName(name):
    return name.replace("/", "~")


if __name__ == "__main__":

    # create Considerations
    for row in csv.DictReader(
        open(f"var/cache/planning-considerations.csv", newline="")
    ):
        folder = "wiki/Consideration/"

        # headers
        headers = {
            k: v
            for k, v in sorted(row.items())
            if k not in ["description", "datasets", "public"] and v != ""
        }

        for k in ["useful-links", "os-declaration"]:
            if k in headers:
                # invalid json, so needs ast to parse
                headers[k] = ast.literal_eval(headers[k])

        if row.get("datasets", ""):
            headers["datasets"] = [
                # parse urls back into dataset references
                # not sure what ?plain=1 is about
                re.sub("^.*/([^/]*)(.md)(\\?plain=1)?/*$", "\\1", dataset)
                for dataset in row["datasets"].split(";")
            ]

        headers["tags"] = []
        for tag in row["tags"].split(";"):
            headers["tags"].append(asTag(tag, "Tag/"))

        headers["tags"] = sorted(headers["tags"])

        links = "\n## Links\n\n"
        links += f"* [{headers['name']} consideration](https://design.planning.data.gov.uk/planning-consideration/{headers['slug']})\n"

        if "github-discussion-number" in headers:
            links += f"* [GitHub discussion](https://github.com/digital-land/data-standards-backlog/discussions/{headers['github-discussion-number']})\n"
        if "legislation" in headers:
            links += f"* [Legislation]({headers['legislation']})\n"

        if "os-declaration" not in headers:
            os_status = None
        else:
            os_status = headers['os-declaration']['status']
            links += f"* [{os_status}]({headers['os-declaration']['further_information_url']})\n"

        if "useful-links" in headers:
            for link in headers["useful-links"]:
                links += f"* [{link['link_text']}]({link['link_url']})\n"

        # cited datasets
        if not headers.get("datasets", ""):
            datasets = "" 
        else:
            datasets = "\n## Datasets\n\n"
            for dataset in headers["datasets"]:
                datasets += f"* [[{dataset}]]\n"

        tags = "#Consideration"
        tags += " #" + asTag(headers.get("stage", "Unknown"), "Stage/")
        tags += " #" + asTag(headers.get("prioritised", "Unknown"), "Prioritised/")
        tags += " #" + asTag(
            headers.get("frequency-of-updates", "Unknown"), "UpdateFrequency/"
        )
        tags += " #" + asTag(os_status or "Unknown", "OS/")
        #tags += " " + " ".join([f"#{tag}" for tag in headers["tags"]])

        # content
        content = f"{tags}\n\n{row['description']}\n{links}{datasets}"


        # create note
        post = Post(content, **headers)
        os.makedirs(folder, exist_ok=True)
        dump(post, f"{folder}{asNoteName(row['name'])}.md")
