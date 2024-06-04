if __name__ == "__main__":
    from sys import argv

    from src import distributions, languages, moderations

    if "moderations" in argv:
        moderations.main()

    if "distributions" in argv:
        distributions.main()

    if "languages" in argv:
        languages.main()
