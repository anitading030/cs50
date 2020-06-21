from cs50 import get_int


def main():
    while True:
        height = get_int("Height: ")
        if height > 0 and height <= 8:
            break

    for h in range(1, height + 1):
        space = height - h
        block = h
        print(" " * space, end="")
        print("#" * block, end="")
        print("  ", end="")
        print("#" * block)


main()
