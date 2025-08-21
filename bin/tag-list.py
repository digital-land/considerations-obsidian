#!/usr/bin/env python3
import sys
import csv


tag = sys.argv[1]

fieldnames = ['consideration', 'slug']
writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
writer.writeheader()

for row in csv.DictReader(open(f"var/cache/planning-considerations.csv", newline="")):
    if tag in row["tags"].split(";"):
        writer.writerow({
            "consideration": row["name"],
            "slug": row["slug"],
        })
