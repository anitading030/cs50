import csv
import sys
import re

# read both dna and sample file


def main():
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")

    else:
        sample = open(sys.argv[2], "r")
        seq = sample.read()
        sample.close()

    # compute the longest run of consecutive repeats in the DNA sequence
        group1 = re.findall(r'((?:AGATC)+)', seq)
        group1.append(" ")
        largest1 = max(group1, key=len)
        s1 = len(largest1) // 5

        group2 = re.findall(r'((?:AATG)+)', seq)
        group2.append(" ")
        largest2 = max(group2, key=len)
        s2 = len(largest2) // 4

        group3 = re.findall(r'((?:TATC)+)', seq)
        group3.append(" ")
        largest3 = max(group3, key=len)
        s3 = len(largest3) // 4

        group4 = re.findall(r'((?:TTTTTTCT)+)', seq)
        group4.append(" ")
        largest4 = max(group4, key=len)
        s4 = len(largest4) // 8

        group5 = re.findall(r'((?:TCTAG)+)', seq)
        group5.append(" ")
        largest5 = max(group5, key=len)
        s5 = len(largest5) // 5

        group6 = re.findall(r'((?:GAAA)+)', seq)
        group6.append(" ")
        largest6 = max(group6, key=len)
        s6 = len(largest6) // 4

        group7 = re.findall(r'((?:TCTG)+)', seq)
        group7.append(" ")
        largest7 = max(group7, key=len)
        s7 = len(largest7) // 4

        with open(sys.argv[1]) as database:
            database = csv.DictReader(database)
            for row in database:
                if len(row) == 4 and int(row["AGATC"]) == s1 and int(row["AATG"]) == s2 and int(row["TATC"]) == s3:
                    print(row["name"])
                    return True
                elif int(row["AGATC"]) == s1 and int(row["AATG"]) == s2 and int(row["TATC"]) == s3 and int(row["TTTTTTCT"]) == s4 and int(row["TCTAG"]) == s5 and int(row["GAAA"]) == s6 and int(row["TCTG"]) == s7:
                    print(row["name"])
                    return True
            print("No match")


main()