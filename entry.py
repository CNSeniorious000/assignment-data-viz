if __name__ == "__main__":
    from multiprocessing import set_start_method

    from src import distributions, languages

    set_start_method("spawn", True)
    languages.main()
    distributions.main()
