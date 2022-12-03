from src.events import Events
from src.advent_of_code import Leaderboard
from flask import render_template
import os


events = Events(
    guild_id="818251363012182023",
    token=os.environ.get('DISCORD_TOKEN')
)

leaderboard = Leaderboard(
    os.environ.get('AOC_API'),
    os.environ.get('AOC_COOKIE')
)


def index():
    return render_template('index.html', events=events.list[:4], leaderboard=leaderboard.table)
