import wikipedia


def search():
    page = wikipedia.search("apple")
    print wikipedia.page(page[1])
    print page

if __name__ == "__main__":
    search()