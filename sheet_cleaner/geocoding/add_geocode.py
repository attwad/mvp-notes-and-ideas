"""Script to append new geocodes to the geo_admin.tsv file"""
import argparse
import pathlib
import os
import csv

parser = argparse.ArgumentParser(
    description='Add geocode to the tsv file containig all geocodes.')
parser.add_argument('--country', required=True)
parser.add_argument('--province')
parser.add_argument('--city')
parser.add_argument('--lat', type=float, required=True)
parser.add_argument('--lng', type=float, required=True)
parser.add_argument('--location')
parser.add_argument('--admin1')
parser.add_argument('--admin2')
parser.add_argument('--admin3')

def main():
    args = parser.parse_args()

    cur_dir = pathlib.Path(__file__).parent.absolute()
    tsv_path = os.path.join(cur_dir, "geo_admin.tsv")

    num_lines = sum(1 for line in open(tsv_path, encoding="utf-8"))

    with open(tsv_path, "a") as f:
        writer = csv.writer(f, delimiter="\t")
        geo_resolution = ""
        if args.admin1:
            geo_resolution = "admin1"
        if args.admin2:
            geo_resolution = "admin2"
        if args.admin3:
            geo_resolution = "admin3"
        writer.writerow([
            f"{args.city};{args.province};{args.country}",
            args.lat,
            args.lng,
            geo_resolution,
            args.location if args.location else "",
            args.admin3 if args.admin3 else "",
            args.admin2 if args.admin2 else "",
            args.admin1 if args.admin1 else "",
            args.country if args.country else "",
            num_lines + 1,
        ])
    print("Done")

if __name__=="__main__":
    main()