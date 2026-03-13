#!/usr/bin/env python3
"""
Practical examples for using the NBA Stats tool

This file contains real-world use cases and code snippets you can copy and adapt.
"""

from nba_stats import NBAStats
from datetime import datetime


def example_1_daily_scores():
    """Get and display today's NBA scores."""
    print("\n" + "="*80)
    print("EXAMPLE 1: Display Today's NBA Scores")
    print("="*80)
    
    nba = NBAStats()
    games = nba.get_recent_games(days=1)
    
    if games:
        print(f"\nGames on {games[0]['date'][:10]}:\n")
        for game in games:
            print(f"{game['visitor_team_abbr']:4s} {game['visitor_score']:3d}  @  "
                  f"{game['home_team_abbr']:4s} {game['home_score']:3d}  -  {game['status']}")
    else:
        print("No games today")


def example_2_team_record():
    """Calculate a team's record over the past week."""
    print("\n" + "="*80)
    print("EXAMPLE 2: Team Record (Last 7 Days)")
    print("="*80)
    
    nba = NBAStats()
    team_abbr = 'LAL'  # Lakers
    
    games = nba.get_recent_games(days=7, team=team_abbr)
    
    wins = 0
    losses = 0
    
    for game in games:
        is_home = game['home_team_abbr'] == team_abbr
        team_score = game['home_score'] if is_home else game['visitor_score']
        opponent_score = game['visitor_score'] if is_home else game['home_score']
        
        if team_score > opponent_score:
            wins += 1
        else:
            losses += 1
    
    print(f"\n{team_abbr} Record (Last 7 Days): {wins}-{losses}")
    print(f"Win Percentage: {(wins/(wins+losses)*100):.1f}%" if (wins+losses) > 0 else "N/A")


def example_3_next_matchups():
    """Show upcoming matchups for two teams."""
    print("\n" + "="*80)
    print("EXAMPLE 3: Upcoming Schedule for Multiple Teams")
    print("="*80)
    
    nba = NBAStats()
    teams = ['LAL', 'BOS']  # Lakers vs Celtics
    
    for team in teams:
        print(f"\n{team} - Next 5 Games:")
        upcoming = nba.get_upcoming_games(days=7, team=team)[:5]
        
        for game in upcoming:
            if game['home_team_abbr'] == team:
                opponent = game['visitor_team_abbr']
                location = "vs"
            else:
                opponent = game['home_team_abbr']
                location = "@"
            
            date_str = game['date'][:10]
            print(f"  {date_str}: {location} {opponent}")


def example_4_leading_scorers():
    """Find the leading scorers in a specific game."""
    print("\n" + "="*80)
    print("EXAMPLE 4: Top Scorers in Recent Game")
    print("="*80)
    
    nba = NBAStats()
    
    # Get a recent game
    recent = nba.get_recent_games(days=1)
    if not recent:
        print("No recent games found")
        return
    
    game = recent[0]
    game_id = game['id']
    
    # Get game stats
    stats = nba.get_game_stats(game_id)
    
    # Combine all players
    all_players = stats['home_player_stats'] + stats['visitor_player_stats']
    
    # Sort by points (convert to int for sorting)
    all_players.sort(key=lambda x: int(x.get('points', 0)), reverse=True)
    
    print(f"\n{stats['visitor_team']} {stats['visitor_score']} @ "
          f"{stats['home_team']} {stats['home_score']}")
    print(f"\nTop 10 Scorers:")
    print(f"{'Player':<25} {'Team':>6} {'PTS':>4} {'REB':>4} {'AST':>4}")
    print("-" * 45)
    
    for i, player in enumerate(all_players[:10], 1):
        print(f"{player['player']:<25} {player['team']:>6} "
              f"{player['points']:>4} {player['rebounds']:>4} {player['assists']:>4}")


def example_5_team_comparison():
    """Compare stats between two teams from a recent game."""
    print("\n" + "="*80)
    print("EXAMPLE 5: Team Stats Comparison")
    print("="*80)
    
    nba = NBAStats()
    
    # Get a recent game
    recent = nba.get_recent_games(days=1)
    if not recent:
        print("No recent games found")
        return
    
    game = recent[0]
    game_id = game['id']
    
    # Get game stats
    stats = nba.get_game_stats(game_id)
    
    # Calculate team totals
    visitor_pts = sum(int(p.get('points', 0)) for p in stats['visitor_player_stats'])
    visitor_reb = sum(int(p.get('rebounds', 0)) for p in stats['visitor_player_stats'])
    visitor_ast = sum(int(p.get('assists', 0)) for p in stats['visitor_player_stats'])
    
    home_pts = sum(int(p.get('points', 0)) for p in stats['home_player_stats'])
    home_reb = sum(int(p.get('rebounds', 0)) for p in stats['home_player_stats'])
    home_ast = sum(int(p.get('assists', 0)) for p in stats['home_player_stats'])
    
    print(f"\n{stats['visitor_team']} vs {stats['home_team']}")
    print(f"{'Stat':<15} {stats['visitor_team']:<20} {stats['home_team']:<20}")
    print("-" * 55)
    print(f"{'Score':<15} {stats['visitor_score']:<20} {stats['home_score']:<20}")
    print(f"{'Total Rebounds':<15} {visitor_reb:<20} {home_reb:<20}")
    print(f"{'Total Assists':<15} {visitor_ast:<20} {home_ast:<20}")


def example_6_players_by_stat():
    """Find top performers by specific stat category."""
    print("\n" + "="*80)
    print("EXAMPLE 6: Top Performers by Stat Category")
    print("="*80)
    
    nba = NBAStats()
    
    # Get a recent game
    recent = nba.get_recent_games(days=1)
    if not recent:
        print("No recent games found")
        return
    
    game = recent[0]
    game_id = game['id']
    
    # Get game stats
    stats = nba.get_game_stats(game_id)
    all_players = stats['home_player_stats'] + stats['visitor_player_stats']
    
    # Top Rebounders
    all_players_sorted = sorted(all_players, 
                                key=lambda x: int(x.get('rebounds', 0)), 
                                reverse=True)
    print(f"\nTop Rebounders:")
    for i, player in enumerate(all_players_sorted[:3], 1):
        print(f"  {i}. {player['player']} ({player['team']}): {player['rebounds']} rebounds")
    
    # Top Assist Makers
    all_players_sorted = sorted(all_players, 
                                key=lambda x: int(x.get('assists', 0)), 
                                reverse=True)
    print(f"\nTop Assist Makers:")
    for i, player in enumerate(all_players_sorted[:3], 1):
        print(f"  {i}. {player['player']} ({player['team']}): {player['assists']} assists")
    
    # Steals Leaders
    all_players_sorted = sorted(all_players, 
                                key=lambda x: int(x.get('steals', 0)), 
                                reverse=True)
    print(f"\nSteals Leaders:")
    for i, player in enumerate(all_players_sorted[:3], 1):
        print(f"  {i}. {player['player']} ({player['team']}): {player['steals']} steals")


def example_7_schedule_builder():
    """Build a calendar of games for your favorite team."""
    print("\n" + "="*80)
    print("EXAMPLE 7: Team Schedule Calendar")
    print("="*80)
    
    nba = NBAStats()
    team_abbr = 'LAL'
    
    # Get recent and upcoming games
    recent = nba.get_recent_games(days=7, team=team_abbr)
    upcoming = nba.get_upcoming_games(days=7, team=team_abbr)
    
    print(f"\n{team_abbr} - Schedule")
    print("\nRecent Games:")
    for game in recent:
        if game['home_team_abbr'] == team_abbr:
            result = "W" if game['home_score'] > game['visitor_score'] else "L"
            score = f"{game['home_score']}-{game['visitor_score']}"
            opponent = f"vs {game['visitor_team_abbr']}"
        else:
            result = "W" if game['visitor_score'] > game['home_score'] else "L"
            score = f"{game['visitor_score']}-{game['home_score']}"
            opponent = f"@ {game['home_team_abbr']}"
        
        print(f"  {result} {game['date'][:10]}: {opponent} ({score})")
    
    print("\nUpcoming Games:")
    for game in upcoming:
        if game['home_team_abbr'] == team_abbr:
            opponent = f"vs {game['visitor_team_abbr']}"
        else:
            opponent = f"@ {game['home_team_abbr']}"
        
        print(f"  {game['date'][:10]}: {opponent}")


def example_8_all_teams():
    """List all NBA teams and their abbreviations."""
    print("\n" + "="*80)
    print("EXAMPLE 8: All NBA Teams")
    print("="*80)
    
    nba = NBAStats()
    teams = nba.get_teams()
    
    print(f"\nTotal Teams: {len(teams)}\n")
    for i, team in enumerate(teams, 1):
        print(f"{team['abbreviation']:6s} - {team['displayName']:<30}", end="")
        if i % 2 == 0:
            print()
        else:
            print(" | ", end="")
    print()


if __name__ == "__main__":
    print("\n" + "="*80)
    print("NBA STATS TOOL - PRACTICAL EXAMPLES")
    print("="*80)
    
    # Run all examples
    example_1_daily_scores()
    example_2_team_record()
    example_3_next_matchups()
    example_4_leading_scorers()
    example_5_team_comparison()
    example_6_players_by_stat()
    example_7_schedule_builder()
    example_8_all_teams()
    
    print("\n" + "="*80)
    print("EXAMPLES COMPLETE!")
    print("="*80)
    print("\nEdit these examples or use them as templates for your own scripts.")
    print("For more information, see README.md")
