#!/usr/bin/env python3
"""
NBA Stats Tool - Quick Start Script

Run this script to launch the interactive user interface.
"""

import sys
import argparse
from typing import Optional

from nba_stats import NBAStats

try:
    from nba_ui import NBAStatsUI
except Exception:
    NBAStatsUI = None


def run_interactive():
    if NBAStatsUI is None:
        print("Interactive UI is not available. Ensure nba_ui.py is present.")
        return

    ui = NBAStatsUI()
    ui.run()


def main(argv: Optional[list] = None):
    parser = argparse.ArgumentParser(description="NBA Stats Tool - CLI")
    parser.add_argument('-i', '--interactive', action='store_true', help='Run interactive menu')
    parser.add_argument('-r', '--recent', nargs='?', const=1, type=int, help='Show recent games (optional days)')
    parser.add_argument('-u', '--upcoming', nargs='?', const=1, type=int, help='Show upcoming games (optional days)')
    parser.add_argument('-t', '--team', type=str, help='Filter results by team abbreviation (e.g., LAL)')
    parser.add_argument('-s', '--stats', type=str, help='Show detailed stats for a game ID')
    parser.add_argument('--teams', action='store_true', help='List all NBA teams')
    args = parser.parse_args(argv)

    # Default: run interactive if no flags supplied
    if len(sys.argv) == 1 or args.interactive:
        run_interactive()
        return

    nba = NBAStats()

    try:
        if args.recent is not None:
            days = args.recent
            print(f"\n⏳ Fetching recent games (last {days} day(s))...")
            games = nba.get_recent_games(days=days, team=args.team)
            nba.display_recent_games(games)

        if args.upcoming is not None:
            days = args.upcoming
            print(f"\n⏳ Fetching upcoming games (next {days} day(s))...")
            games = nba.get_upcoming_games(days=days, team=args.team)
            nba.display_upcoming_games(games)

        if args.stats:
            print(f"\n⏳ Fetching detailed stats for game {args.stats}...")
            stats = nba.get_game_stats(args.stats)
            nba.display_game_stats(stats)

        if args.teams:
            teams = nba.get_teams()
            if not teams:
                print("No teams found.")
            else:
                print(f"\n📊 Total Teams: {len(teams)}\n")
                print(f"{'ABBR':<6} {'TEAM NAME':<35} {'LOCATION':<20}")
                print("-" * 80)
                for team in sorted(teams, key=lambda x: x.get('abbreviation', '')):
                    abbr = team.get('abbreviation', 'N/A')
                    name = team.get('displayName', 'N/A')
                    location = team.get('location', 'N/A')
                    print(f"{abbr:<6} {name:<35} {location:<20}")

        # If no actionable flag was provided, show help
        if not any([args.recent is not None, args.upcoming is not None, args.stats, args.teams]):
            parser.print_help()

    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
