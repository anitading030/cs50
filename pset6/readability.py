from cs50 import get_string


def main():
    texts = get_string("Text: ")

    characters = 0
    for c in range(len(texts)):
        if texts[c].isalpha() == True:
            characters += 1

    words = 1
    for w in range(len(texts)):
        if texts[w] == " " and texts[w+1] != " ":
            words += 1

    sentences = 0
    for s in range(len(texts)):
        if texts[s] == "." or texts[s] == "?" or texts[s] == "!":
            sentences += 1

    L = 100 * characters / words
    S = 100 * sentences / words
    index = 0.0588 * L - 0.296 * S - 15.8

    if index < 1:
        print("Before Grade 1")

    elif index > 16:
        print("Grade 16+")

    else:
        print(f"Grade {round(index)}")


main()
