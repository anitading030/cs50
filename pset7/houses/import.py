from cs50 import SQL
import sys
import csv

# Give access to the database, table already created in the database
db = SQL("sqlite:///students.db")


def main():
    if len(sys.argv) != 2:
        print("Wrong input")
        return

    else:
        with open(sys.argv[1], "r") as titles:
            reader = csv.DictReader(titles)

            for row in reader:
                name = row["name"].split()
                house = row["house"]
                birth = int(row["birth"])
                first = name[0]
                last = name[-1]
                if len(name) != 2:
                    middle = name[1]
                else:
                    middle = None

                db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)", first, middle, last, house, birth)


main()
