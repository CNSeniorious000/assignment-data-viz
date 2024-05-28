from contextlib import suppress

with suppress(ModuleNotFoundError):
    from dotenv import load_dotenv

    load_dotenv(override=True)
