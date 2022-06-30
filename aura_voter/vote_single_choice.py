from aura_voter.cast_vote import cast_single_choice_vote
from aura_voter.constants import BOT_USERNAME
from aura_voter.discord import send_message_to_discord

# Hardcoded params for one-time needs
SNAPSHOT_IDS = [
    ("0x2670c901433a452b9622268bc637bbc9a74f052717c89326c63e8a053581bea9", 1),
    ("0x0592d89a5efea91cc463b44a4df26fe5572b06b196f1e8b70e5b66b0b83efa86", 1),
    ("0x220eb8dc6f09ae0a89481590978fe69bdaca7d1afaf9586d51bdc9dc6fc7af18", 1),
    ("0x113b565b39737b810cec5ef98371c437a656a07c2aed13c83d0b5e38ec5963fd", 1),
]


def vote_single_choice():
    for snapshot_id, choice in SNAPSHOT_IDS:
        send_message_to_discord(
            f"🗳️🗳️🗳️🗳️ Voting for single choice on snapshot {snapshot_id} 🗳️🗳️🗳️🗳️",
            username=BOT_USERNAME
        )
        cast_single_choice_vote(choice, snapshot_id)
        send_message_to_discord(
            "👍👍👍👍 Voting succeeded 👍👍👍👍",
            username=BOT_USERNAME
        )
