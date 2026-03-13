#!/usr/bin/env python3
"""
Demo script for NBA Stats Tool

This script demonstrates all the features of the NBA Stats tool:
- Fetching recent game scores
- Getting upcoming game schedules
- Retrieving detailed stats for specific games
- Filtering by team
"""

from nba_stats import NBAStats


def main():
    # Initialize the NBA Stats client
    nba = NBAStats()
    
    print("=" * 80)
    print("NBA STATS TOOL - COMPREHENSIVE DEMO")
    print("=" * 80)
    
    # Example 1: Get recent games from the last 3 days
    print("\n\n1. RECENT GAMES (Last 3 Days)")
    print("-" * 80)
    recent_games = nba.get_recent_games(days=3)
    nba.display_recent_games(recent_games)
    
    # Example 2: Get recent games for a specific team (Lakers)
    print("\n\n2. RECENT GAMES FOR A SPECIFIC TEAM (Lakers)")
    print("-" * 80)
    lakers_games = nba.get_recent_games(days=7, team='LAL')
    nba.display_recent_games(lakers_games)
    
    # Example 3: Get upcoming games
    print("\n\n3. UPCOMING GAMES (Next 5 Days)")
    print("-" * 80)
    upcoming_games = nba.get_upcoming_games(days=5)
    nba.display_upcoming_games(upcoming_games)
    
    # Example 4: Get upcoming games for a specific team (Warriors)
    print("\n\n4. UPCOMING GAMES FOR A SPECIFIC TEAM (Warriors)")
    print("-" * 80)
    warriors_upcoming = nba.get_upcoming_games(days=7, team='GSW')
    nba.display_upcoming_games(warriors_upcoming)
    
    # Example 5: Get detailed stats for a specific game
    if recent_games and len(recent_games) > 0:
        game_id = recent_games[0]['id']
        print(f"\n\n5. DETAILED GAME STATISTICS (Game ID: {game_id})")
        print("-" * 80)
        game_stats = nba.get_game_stats(game_id)
        nba.display_game_stats(game_stats)
    
    # Example 6: Get all NBA teams
    print("\n\n6. ALL NBA TEAMS")
    print("-" * 80)
    teams = nba.get_teams()
    print(f"\nTotal Teams: {len(teams)}")
    print("\nTeam Abbreviations:")
    for i, team in enumerate(teams, 1):
        print(f"  {team['abbreviation']:4s} - {team['displayName']}", end="")
        if i % 2 == 0:
            print()
        else:
            print(" " * 10, end="")
    print("\n")
    
    # Example 7: Working with raw data
    print("\n\n7. WORKING WITH RAW DATA")
    print("-" * 80)
    print("\nYou can also work with the raw data returned by the methods:")
    print(f"\nExample - First recent game data:")
    if recent_games and len(recent_games) > 0:
        game = recent_games[0]
        print(f"  Game ID: {game['id']}")
        print(f"  Date: {game['date']}")
        print(f"  {game['visitor_team_abbr']} ({game['visitor_score']}) @ {game['home_team_abbr']} ({game['home_score']})")
        print(f"  Status: {game['status']}")
        print(f"  Venue: {game.get('venue', 'N/A')}")


def team_specific_example():
    """Example: Track a specific team's recent performance and upcoming schedule."""
    nba = NBAStats()
    
    team_abbr = 'BOS'  # Boston Celtics
    
    print("\n" + "=" * 80)
    print(f"TEAM-SPECIFIC EXAMPLE: {team_abbr}")
    print("=" * 80)
    
    # Recent games
    print(f"\n{team_abbr} - Last 7 Days:")
    recent = nba.get_recent_games(days=7, team=team_abbr)
    for game in recent:
        if game['home_team_abbr'] == team_abbr:
            result = "W" if game['home_score'] > game['visitor_score'] else "L"
            print(f"  {result} - vs {game['visitor_team_abbr']} ({game['home_score']}-{game['visitor_score']})")
        else:
            result = "W" if game['visitor_score'] > game['home_score'] else "L"
            print(f"  {result} - @ {game['home_team_abbr']} ({game['visitor_score']}-{game['home_score']})")
    
    # Upcoming games
    print(f"\n{team_abbr} - Next 7 Days:")
    upcoming = nba.get_upcoming_games(days=7, team=team_abbr)
    for game in upcoming:
        if game['home_team_abbr'] == team_abbr:
            print(f"  vs {game['visitor_team_abbr']} - {game['date'][:10]}")
        else:
            print(f"  @ {game['home_team_abbr']} - {game['date'][:10]}")


if __name__ == "__main__":
    # Run main demo
    main()
    
    # Run team-specific example
    team_specific_example()
    
    print("\n" + "=" * 80)
    print("DEMO COMPLETE!")
    print("=" * 80)
