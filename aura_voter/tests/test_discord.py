from unittest.mock import MagicMock

from discord import InvalidArgument

from aura_voter.constants import BOT_USERNAME
from aura_voter.discord import send_code_block_to_discord
from aura_voter.discord import send_message_to_discord


def test_send_code_block_to_discord_happy(mocker):
    discord = mocker.patch(
        "voter.discord.Webhook.from_url",
        MagicMock()
    )
    send_code_block_to_discord(msg="message", username=BOT_USERNAME)
    assert discord.called
    assert discord.return_value.send.called


def test_send_code_block_to_discord_bad_url(mocker):
    discord = mocker.patch(
        "voter.discord.Webhook.from_url",
        side_effect=InvalidArgument()
    )
    send_code_block_to_discord(msg="message", username=BOT_USERNAME)
    assert discord.called
    assert not discord.return_value.send.called


def test_send_mesage_to_discord_happy(mocker):
    discord = mocker.patch(
        "voter.discord.Webhook.from_url",
        MagicMock()
    )
    send_message_to_discord(msg="message", username=BOT_USERNAME)
    assert discord.called
    assert discord.return_value.send.called


def test_send_send_mesage_to_discord_bad_url(mocker):
    discord = mocker.patch(
        "voter.discord.Webhook.from_url",
        side_effect=InvalidArgument()
    )
    send_message_to_discord(msg="message", username=BOT_USERNAME)
    assert discord.called
    assert not discord.return_value.send.called
