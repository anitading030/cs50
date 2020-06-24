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
        school = sys.argv[1]
        roster = db.execute("SELECT first, middle, last, birth FROM students WHERE house = ? ORDER BY last, first", school)
        for row in roster:
            first = row["first"]
            middle = row["middle"]
            last = row["last"]
            birth = row["birth"]
            if middle == None:
                print(f"{first} {last}, born {birth}")
            else:
                print(f"{first} {middle} {last}, born {birth}")


main()
