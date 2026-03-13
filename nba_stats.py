"""
NBA Stats Tool - Real-time NBA game statistics and schedules

This module provides functionality to:
- Fetch recent game scores
- Get upcoming game schedules
- Retrieve detailed stats for specific games

Uses the ESPN API for NBA data (no API key required).
"""

import requests
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional
import json


class NBAStats:
    """Main class for fetching NBA game statistics and schedules."""
    
    BASE_URL = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the NBA Stats client.
        
        Args:
            api_key: Optional API key (not required for ESPN API)
        """
        self.api_key = api_key
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """
        Make a request to the NBA API.
        
        Args:
            endpoint: API endpoint to call
            params: Query parameters
            
        Returns:
            JSON response as dictionary
        """
        url = f"{self.BASE_URL}/{endpoint}"
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making API request: {e}")
            return {}
    
    def _convert_to_pacific_time(self, utc_time_str: str) -> str:
        """
        Convert UTC time string to Pacific time in 12-hour format.
        
        Args:
            utc_time_str: ISO format time string (e.g., '2026-03-13T23:30Z')
            
        Returns:
            Pacific time in format like '3:30 PM PT'
        """
        try:
            # Parse UTC time
            utc_time = datetime.fromisoformat(utc_time_str.replace('Z', '+00:00'))
            
            # Convert to Pacific (UTC-8 or UTC-7 for PDT)
            # Using a simple offset of -8 hours (PST)
            pacific_offset = timedelta(hours=-8)
            pacific_time = utc_time + pacific_offset
            
            # Format as 12-hour time
            hour = pacific_time.hour
            minute = pacific_time.minute
            am_pm = 'AM' if hour < 12 else 'PM'
            
            if hour == 0:
                hour = 12
            elif hour > 12:
                hour -= 12
            
            return f"{hour}:{minute:02d} {am_pm} PT"
        except:
            return ""
    
    def get_recent_games(self, days: int = 7, team: Optional[str] = None) -> List[Dict]:
        """
        Get recent game scores from the past N days.
        
        Args:
            days: Number of days to look back (default: 7)
            team: Optional team abbreviation to filter by (e.g., 'LAL', 'BOS')
            
        Returns:
            List of game dictionaries with scores and details
        """
        results = []
        
        # Get games for each day in the range
        for i in range(days):
            date = datetime.now() - timedelta(days=i)
            date_str = date.strftime('%Y%m%d')
            
            params = {'dates': date_str}
            data = self._make_request('scoreboard', params)
            
            events = data.get('events', [])
            
            for event in events:
                competitions = event.get('competitions', [{}])[0]
                competitors = competitions.get('competitors', [])
                
                # Find home and away teams
                home_team = None
                away_team = None
                for comp in competitors:
                    if comp.get('homeAway') == 'home':
                        home_team = comp
                    else:
                        away_team = comp
                
                if not home_team or not away_team:
                    continue
                
                home_abbr = home_team.get('team', {}).get('abbreviation', '')
                away_abbr = away_team.get('team', {}).get('abbreviation', '')
                
                # Filter by team if specified
                if team:
                    team_upper = team.upper()
                    if team_upper != home_abbr and team_upper != away_abbr:
                        continue
                
                # Only include completed games
                status = event.get('status', {}).get('type', {}).get('state', '')
                if status != 'post':
                    continue
                
                results.append({
                    'id': event.get('id'),
                    'date': event.get('date'),
                    'status': event.get('status', {}).get('type', {}).get('description', 'Final'),
                    'home_team': home_team.get('team', {}).get('displayName', 'Unknown'),
                    'home_team_abbr': home_abbr,
                    'home_score': int(home_team.get('score', 0)),
                    'visitor_team': away_team.get('team', {}).get('displayName', 'Unknown'),
                    'visitor_team_abbr': away_abbr,
                    'visitor_score': int(away_team.get('score', 0)),
                    'season': event.get('season', {}).get('year'),
                    'venue': competitions.get('venue', {}).get('fullName', ''),
                })
        
        return results
    
    def get_upcoming_games(self, days: int = 7, team: Optional[str] = None) -> List[Dict]:
        """
        Get upcoming game schedule for the next N days.
        
        Args:
            days: Number of days to look ahead (default: 7)
            team: Optional team abbreviation to filter by
            
        Returns:
            List of scheduled game dictionaries
        """
        results = []
        
        # Get games for each day in the range
        for i in range(days):
            date = datetime.now() + timedelta(days=i)
            date_str = date.strftime('%Y%m%d')
            
            params = {'dates': date_str}
            data = self._make_request('scoreboard', params)
            
            events = data.get('events', [])
            
            for event in events:
                competitions = event.get('competitions', [{}])[0]
                competitors = competitions.get('competitors', [])
                
                # Find home and away teams
                home_team = None
                away_team = None
                for comp in competitors:
                    if comp.get('homeAway') == 'home':
                        home_team = comp
                    else:
                        away_team = comp
                
                if not home_team or not away_team:
                    continue
                
                home_abbr = home_team.get('team', {}).get('abbreviation', '')
                away_abbr = away_team.get('team', {}).get('abbreviation', '')
                
                # Filter by team if specified
                if team:
                    team_upper = team.upper()
                    if team_upper != home_abbr and team_upper != away_abbr:
                        continue
                
                # Only include scheduled or in-progress games
                status = event.get('status', {}).get('type', {}).get('state', '')
                if status == 'post':
                    continue
                
                results.append({
                    'id': event.get('id'),
                    'date': event.get('date'),
                    'status': event.get('status', {}).get('type', {}).get('description', 'Scheduled'),
                    'home_team': home_team.get('team', {}).get('displayName', 'Unknown'),
                    'home_team_abbr': home_abbr,
                    'visitor_team': away_team.get('team', {}).get('displayName', 'Unknown'),
                    'visitor_team_abbr': away_abbr,
                    'season': event.get('season', {}).get('year'),
                    'venue': competitions.get('venue', {}).get('fullName', ''),
                })
        
        return results
    
    def get_game_stats(self, game_id: str) -> Dict:
        """
        Get detailed statistics for a specific game.
        
        Args:
            game_id: The unique game ID
            
        Returns:
            Dictionary with detailed game statistics including player stats
        """
        # Get game summary which includes box score
        data = self._make_request(f'summary?event={game_id}')
        
        if not data:
            return {}
        
        header = data.get('header', {})
        box_score = data.get('boxscore', {})
        players = box_score.get('players', [])
        
        # Get team info from header to determine home/away
        competitions = header.get('competitions', [{}])[0]
        competitors = competitions.get('competitors', [])
        
        home_team = None
        away_team = None
        home_team_id = None
        away_team_id = None
        
        for comp in competitors:
            if comp.get('homeAway') == 'home':
                home_team = comp
                home_team_id = comp.get('team', {}).get('id')
            else:
                away_team = comp
                away_team_id = comp.get('team', {}).get('id')
        
        home_stats = []
        visitor_stats = []
        
        # Process player stats from both teams
        for team_data in players:
            team_info = team_data.get('team', {})
            team_id = team_info.get('id')
            
            # Determine if this is home or away team by matching IDs
            is_home = (team_id == home_team_id)
            
            # Get statistics array - ESPN uses a single stat category with all player stats
            statistics = team_data.get('statistics', [])
            if not statistics:
                continue
                
            athletes = statistics[0].get('athletes', [])
            
            for athlete in athletes:
                stats = athlete.get('stats', [])
                player_name = athlete.get('athlete', {}).get('displayName', 'Unknown')
                
                # ESPN stats order: MIN, PTS, FG, 3PT, FT, REB, AST, TO, STL, BLK, OREB, DREB, PF, +/-
                player_stat = {
                    'player': player_name,
                    'team': team_info.get('abbreviation', ''),
                    'minutes': stats[0] if len(stats) > 0 else '0',
                    'points': stats[1] if len(stats) > 1 else '0',
                    'fg': stats[2] if len(stats) > 2 else '0-0',
                    'fg3': stats[3] if len(stats) > 3 else '0-0',
                    'ft': stats[4] if len(stats) > 4 else '0-0',
                    'rebounds': stats[5] if len(stats) > 5 else '0',
                    'assists': stats[6] if len(stats) > 6 else '0',
                    'turnovers': stats[7] if len(stats) > 7 else '0',
                    'steals': stats[8] if len(stats) > 8 else '0',
                    'blocks': stats[9] if len(stats) > 9 else '0',
                }
                
                if is_home:
                    home_stats.append(player_stat)
                else:
                    visitor_stats.append(player_stat)
        
        return {
            'game_id': game_id,
            'date': header.get('competitions', [{}])[0].get('date', ''),
            'home_team': home_team.get('team', {}).get('displayName', '') if home_team else '',
            'home_score': int(home_team.get('score', 0)) if home_team else 0,
            'visitor_team': away_team.get('team', {}).get('displayName', '') if away_team else '',
            'visitor_score': int(away_team.get('score', 0)) if away_team else 0,
            'home_player_stats': home_stats,
            'visitor_player_stats': visitor_stats
        }
    
    def get_teams(self) -> List[Dict]:
        """
        Get list of all NBA teams.
        
        Returns:
            List of team dictionaries with details
        """
        # Hardcoded list of all 30 NBA teams with their official colors
        teams = [
            {'abbreviation': 'ATL', 'displayName': 'Atlanta Hawks', 'location': 'Atlanta', 'name': 'Hawks', 'primary': 'red', 'secondary': 'yellow'},
            {'abbreviation': 'BOS', 'displayName': 'Boston Celtics', 'location': 'Boston', 'name': 'Celtics', 'primary': 'green', 'secondary': 'white'},
            {'abbreviation': 'BKN', 'displayName': 'Brooklyn Nets', 'location': 'Brooklyn', 'name': 'Nets', 'primary': 'black', 'secondary': 'white'},
            {'abbreviation': 'CHA', 'displayName': 'Charlotte Hornets', 'location': 'Charlotte', 'name': 'Hornets', 'primary': 'cyan', 'secondary': 'magenta'},
            {'abbreviation': 'CHI', 'displayName': 'Chicago Bulls', 'location': 'Chicago', 'name': 'Bulls', 'primary': 'red', 'secondary': 'black'},
            {'abbreviation': 'CLE', 'displayName': 'Cleveland Cavaliers', 'location': 'Cleveland', 'name': 'Cavaliers', 'primary': 'red', 'secondary': 'yellow'},
            {'abbreviation': 'DAL', 'displayName': 'Dallas Mavericks', 'location': 'Dallas', 'name': 'Mavericks', 'primary': 'blue', 'secondary': 'white'},
            {'abbreviation': 'DEN', 'displayName': 'Denver Nuggets', 'location': 'Denver', 'name': 'Nuggets', 'primary': 'blue', 'secondary': 'yellow'},
            {'abbreviation': 'DET', 'displayName': 'Detroit Pistons', 'location': 'Detroit', 'name': 'Pistons', 'primary': 'blue', 'secondary': 'red'},
            {'abbreviation': 'GS', 'displayName': 'Golden State Warriors', 'location': 'Golden State', 'name': 'Warriors', 'primary': 'blue', 'secondary': 'yellow'},
            {'abbreviation': 'HOU', 'displayName': 'Houston Rockets', 'location': 'Houston', 'name': 'Rockets', 'primary': 'red', 'secondary': 'white'},
            {'abbreviation': 'IND', 'displayName': 'Indiana Pacers', 'location': 'Indiana', 'name': 'Pacers', 'primary': 'blue', 'secondary': 'yellow'},
            {'abbreviation': 'LAC', 'displayName': 'LA Clippers', 'location': 'Los Angeles', 'name': 'Clippers', 'primary': 'blue', 'secondary': 'red'},
            {'abbreviation': 'LAL', 'displayName': 'Los Angeles Lakers', 'location': 'Los Angeles', 'name': 'Lakers', 'primary': 'yellow', 'secondary': 'magenta'},
            {'abbreviation': 'MEM', 'displayName': 'Memphis Grizzlies', 'location': 'Memphis', 'name': 'Grizzlies', 'primary': 'blue', 'secondary': 'yellow'},
            {'abbreviation': 'MIA', 'displayName': 'Miami Heat', 'location': 'Miami', 'name': 'Heat', 'primary': 'red', 'secondary': 'yellow'},
            {'abbreviation': 'MIL', 'displayName': 'Milwaukee Bucks', 'location': 'Milwaukee', 'name': 'Bucks', 'primary': 'green', 'secondary': 'white'},
            {'abbreviation': 'MIN', 'displayName': 'Minnesota Timberwolves', 'location': 'Minnesota', 'name': 'Timberwolves', 'primary': 'blue', 'secondary': 'green'},
            {'abbreviation': 'NO', 'displayName': 'New Orleans Pelicans', 'location': 'New Orleans', 'name': 'Pelicans', 'primary': 'blue', 'secondary': 'red'},
            {'abbreviation': 'NY', 'displayName': 'New York Knicks', 'location': 'New York', 'name': 'Knicks', 'primary': 'blue', 'secondary': 'bright_white'},
            {'abbreviation': 'OKC', 'displayName': 'Oklahoma City Thunder', 'location': 'Oklahoma City', 'name': 'Thunder', 'primary': 'blue', 'secondary': 'bright_white'},
            {'abbreviation': 'ORL', 'displayName': 'Orlando Magic', 'location': 'Orlando', 'name': 'Magic', 'primary': 'blue', 'secondary': 'white'},
            {'abbreviation': 'PHI', 'displayName': 'Philadelphia 76ers', 'location': 'Philadelphia', 'name': '76ers', 'primary': 'blue', 'secondary': 'red'},
            {'abbreviation': 'PHX', 'displayName': 'Phoenix Suns', 'location': 'Phoenix', 'name': 'Suns', 'primary': 'magenta', 'secondary': 'bright_white'},
            {'abbreviation': 'POR', 'displayName': 'Portland Trail Blazers', 'location': 'Portland', 'name': 'Trail Blazers', 'primary': 'red', 'secondary': 'white'},
            {'abbreviation': 'SAC', 'displayName': 'Sacramento Kings', 'location': 'Sacramento', 'name': 'Kings', 'primary': 'magenta', 'secondary': 'white'},
            {'abbreviation': 'SA', 'displayName': 'San Antonio Spurs', 'location': 'San Antonio', 'name': 'Spurs', 'primary': 'white', 'secondary': 'black'},
            {'abbreviation': 'TOR', 'displayName': 'Toronto Raptors', 'location': 'Toronto', 'name': 'Raptors', 'primary': 'red', 'secondary': 'white'},
            {'abbreviation': 'UTAH', 'displayName': 'Utah Jazz', 'location': 'Utah', 'name': 'Jazz', 'primary': 'blue', 'secondary': 'yellow'},
            {'abbreviation': 'WSH', 'displayName': 'Washington Wizards', 'location': 'Washington', 'name': 'Wizards', 'primary': 'blue', 'secondary': 'red'},
        ]
        
        return teams
    
    def display_recent_games(self, games: List[Dict]) -> None:
        """Pretty print recent games."""
        if not games:
            print("No games found.")
            return
        
        print("\n" + "="*80)
        print("RECENT NBA GAMES")
        print("="*80)
        
        for game in games:
            date_str = game['date'][:10] if game.get('date') else 'Unknown'
            print(f"\n{date_str} - {game.get('status', 'N/A')}")
            print(f"  {game['visitor_team_abbr']:4s} {game['visitor_score']:3d}  @  "
                  f"{game['home_team_abbr']:4s} {game['home_score']:3d}")
            print(f"  {game['visitor_team']}")
            print(f"  {game['home_team']}")
        
        print("\n" + "="*80)
    
    def display_upcoming_games(self, games: List[Dict]) -> None:
        """Pretty print upcoming games."""
        if not games:
            print("No upcoming games found.")
            return
        
        print("\n" + "="*80)
        print("UPCOMING NBA GAMES")
        print("="*80)
        
        for game in games:
            date_str = game['date'][:10] if game.get('date') else 'Unknown'
            time_str = game['date'][11:16] if game.get('date') and len(game['date']) > 11 else ''
            print(f"\n{date_str} {time_str}")
            print(f"  {game['visitor_team_abbr']:4s}  @  {game['home_team_abbr']:4s}")
            print(f"  {game['visitor_team']} @ {game['home_team']}")
        
        print("\n" + "="*80)
    
    def display_game_stats(self, stats: Dict) -> None:
        """Pretty print game statistics."""
        if not stats:
            print("No stats found.")
            return
        
        print("\n" + "="*80)
        print(f"GAME STATISTICS - {stats.get('date', 'N/A')[:10]}")
        print("="*80)
        print(f"\n{stats.get('visitor_team')} {stats.get('visitor_score')}  @  "
              f"{stats.get('home_team')} {stats.get('home_score')}")
        
        # Display visitor stats
        print(f"\n{stats.get('visitor_team')} PLAYER STATS:")
        print("-"*80)
        print(f"{'Player':<20} {'MIN':>5} {'PTS':>4} {'REB':>4} {'AST':>4} "
              f"{'FG':>7} {'3PT':>7} {'FT':>7}")
        print("-"*80)
        
        for player in stats.get('visitor_player_stats', []):
            print(f"{player['player']:<20} {player['minutes']:>5} {player['points']:>4} "
                  f"{player['rebounds']:>4} {player['assists']:>4} "
                  f"{player['fg']:>7} {player['fg3']:>7} {player['ft']:>7}")
        
        # Display home stats
        print(f"\n{stats.get('home_team')} PLAYER STATS:")
        print("-"*80)
        print(f"{'Player':<20} {'MIN':>5} {'PTS':>4} {'REB':>4} {'AST':>4} "
              f"{'FG':>7} {'3PT':>7} {'FT':>7}")
        print("-"*80)
        
        for player in stats.get('home_player_stats', []):
            print(f"{player['player']:<20} {player['minutes']:>5} {player['points']:>4} "
                  f"{player['rebounds']:>4} {player['assists']:>4} "
                  f"{player['fg']:>7} {player['fg3']:>7} {player['ft']:>7}")
        
        print("\n" + "="*80)


if __name__ == "__main__":
    # Example usage
    nba = NBAStats()
    
    print("NBA Stats Tool - Demo")
    print("=" * 80)
    
    # Get and display recent games
    print("\nFetching recent games...")
    recent = nba.get_recent_games(days=3)
    nba.display_recent_games(recent)
    
    # Get and display upcoming games
    print("\nFetching upcoming games...")
    upcoming = nba.get_upcoming_games(days=3)
    nba.display_upcoming_games(upcoming)
    
    # Get stats for a specific game (if any recent games exist)
    if recent and len(recent) > 0:
        game_id = recent[0]['id']
        print(f"\nFetching detailed stats for game ID {game_id}...")
        stats = nba.get_game_stats(game_id)
        nba.display_game_stats(stats)
