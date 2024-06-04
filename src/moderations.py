from asyncio import run

from .core.moderate import ModerationPipeline


def main():
    run(ModerationPipeline().process_every_file())
