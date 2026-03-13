# NBA Stats Tool - Quick Start Guide

## Installation

```bash
pip install requests
```

## 5-Minute Quick Start

### 1. Get Today's Scores

```python
from nba_stats import NBAStats

nba = NBAStats()
games = nba.get_recent_games(days=1)
nba.display_recent_games(games)
```

### 2. See Upcoming Games

```python
from nba_stats import NBAStats

nba = NBAStats()
upcoming = nba.get_upcoming_games(days=3)
nba.display_upcoming_games(upcoming)
```

### 3. Track Your Favorite Team

```python
from nba_stats import NBAStats

nba = NBAStats()

# Replace 'LAL' with your team's abbreviation
team = 'LAL'

# Recent games
recent = nba.get_recent_games(days=7, team=team)
nba.display_recent_games(recent)

# Upcoming games
upcoming = nba.get_upcoming_games(days=7, team=team)
nba.display_upcoming_games(upcoming)
```

### 4. Get Detailed Game Stats

```python
from nba_stats import NBAStats

nba = NBAStats()

# Get a recent game
recent = nba.get_recent_games(days=1)
if recent:
    game_id = recent[0]['id']
    stats = nba.get_game_stats(game_id)
    nba.display_game_stats(stats)
```

## Common Team Abbreviations

```
LAL - Lakers        BOS - Celtics       GSW - Warriors
MIA - Heat          CHI - Bulls         NY  - Knicks
BKN - Nets          PHI - 76ers         DAL - Mavericks
DEN - Nuggets       PHX - Suns          MIL - Bucks
```

For a complete list, see README.md or run:

```python
from nba_stats import NBAStats
nba = NBAStats()
teams = nba.get_teams()
for team in teams:
    print(f"{team['abbreviation']} - {team['displayName']}")
```

## Run the Demo

```bash
python3 demo.py
```

## Getting Help

See the full README.md for:
- Complete API reference
- Advanced examples
- Troubleshooting
- All team abbreviations
