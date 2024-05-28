from alive_progress import alive_it

from src.core.parse import File


def test_parse():
    for file in alive_it(File.glob()):
        for i in file.example.messages:
            assert isinstance(i["content"], str)


test_parse()
