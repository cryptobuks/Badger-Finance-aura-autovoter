from dotenv import load_dotenv

from aura_voter.vote import collect_and_vote


def main() -> None:
    load_dotenv()
    collect_and_vote(dry_run=False)


if __name__ == '__main__':
    main()
