from dotenv import load_dotenv

from aura_voter.vote_single_choice import vote_single_choice


def main() -> None:
    load_dotenv()
    vote_single_choice()


if __name__ == '__main__':
    main()
