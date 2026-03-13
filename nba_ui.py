#!/usr/bin/env python3
"""
NBA Stats Tool - Interactive User Interface

Interactive command-line interface for browsing NBA game data.
"""

from nba_stats import NBAStats
import sys


class NBAStatsUI:
    """Interactive user interface for NBA Stats tool."""
    
    def __init__(self):
        self.nba = NBAStats()
        self.running = True
    
    def clear_screen(self):
        """Clear the terminal screen."""
        print("\n" * 2)
    
    def print_header(self, title):
        """Print a formatted header."""
        print("\n" + "=" * 80)
        print(f"🏀 {title}")
        print("=" * 80)
    
    def print_menu(self, title, options):
        """Print a menu with numbered options."""
        self.print_header(title)
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        print(f"{len(options) + 1}. Back to Main Menu" if title != "NBA STATS TOOL - MAIN MENU" else f"{len(options) + 1}. Exit")
        print()
    
    def get_user_choice(self, max_option):
        """Get and validate user input."""
        while True:
            try:
                choice = input(f"Select an option (1-{max_option}): ").strip()
                choice_num = int(choice)
                if 1 <= choice_num <= max_option:
                    return choice_num
                else:
                    print(f"❌ Please enter a number between 1 and {max_option}")
            except ValueError:
                print("❌ Please enter a valid number")
            except KeyboardInterrupt:
                print("\n\nExiting...")
                sys.exit(0)
    
    def pause(self):
        """Pause and wait for user to press Enter."""
        input("\nPress Enter to continue...")
    
    def main_menu(self):
        """Display and handle main menu."""
        options = [
            "View Recent Game Scores",
            "View Upcoming Game Schedule",
            "Search by Team",
            "View Detailed Game Statistics",
            "View All NBA Teams"
        ]
        
        self.print_menu("NBA STATS TOOL - MAIN MENU", options)
        choice = self.get_user_choice(len(options) + 1)
        
        if choice == 1:
            self.recent_games_menu()
        elif choice == 2:
            self.upcoming_games_menu()
        elif choice == 3:
            self.team_search_menu()
        elif choice == 4:
            self.game_stats_menu()
        elif choice == 5:
            self.show_all_teams()
        elif choice == len(options) + 1:
            self.exit_app()
    
    def recent_games_menu(self):
        """Menu for viewing recent games."""
        self.print_header("RECENT GAME SCORES")
        
        print("\nHow many days back would you like to see?")
        print("1. Today (last 24 hours)")
        print("2. Last 3 days")
        print("3. Last 7 days")
        print("4. Custom number of days")
        print("5. Back to Main Menu")
        print()
        
        choice = self.get_user_choice(5)
        
        if choice == 1:
            days = 1
        elif choice == 2:
            days = 3
        elif choice == 3:
            days = 7
        elif choice == 4:
            days = self.get_custom_days()
        else:
            return
        
        print(f"\n⏳ Fetching games from the last {days} day(s)...")
        games = self.nba.get_recent_games(days=days)
        
        if games:
            self.nba.display_recent_games(games)
            print(f"\n📊 Total games found: {len(games)}")
            
            # Ask if user wants to see detailed stats for any game
            print("\n" + "-" * 80)
            see_details = input("\nWould you like to see detailed stats for any of these games? (y/n): ").strip().lower()
            if see_details == 'y':
                self.select_game_for_stats(games)
        else:
            print("\n⚠️  No games found for the selected time period.")
        
        self.pause()
    
    def upcoming_games_menu(self):
        """Menu for viewing upcoming games."""
        self.print_header("UPCOMING GAME SCHEDULE")
        
        print("\nHow many days ahead would you like to see?")
        print("1. Today")
        print("2. Next 3 days")
        print("3. Next 7 days")
        print("4. Custom number of days")
        print("5. Back to Main Menu")
        print()
        
        choice = self.get_user_choice(5)
        
        if choice == 1:
            days = 1
        elif choice == 2:
            days = 3
        elif choice == 3:
            days = 7
        elif choice == 4:
            days = self.get_custom_days()
        else:
            return
        
        print(f"\n⏳ Fetching upcoming games for the next {days} day(s)...")
        games = self.nba.get_upcoming_games(days=days)
        
        if games:
            self.nba.display_upcoming_games(games)
            print(f"\n📊 Total games scheduled: {len(games)}")
        else:
            print("\n⚠️  No upcoming games found for the selected time period.")
        
        self.pause()
    
    def team_search_menu(self):
        """Menu for searching by team."""
        self.print_header("SEARCH BY TEAM")
        
        print("\nWhat would you like to see?")
        print("1. Team's Recent Games")
        print("2. Team's Upcoming Games")
        print("3. Team's Complete Schedule (Recent + Upcoming)")
        print("4. Back to Main Menu")
        print()
        
        choice = self.get_user_choice(4)
        
        if choice == 4:
            return
        
        # Get team abbreviation
        team_abbr = self.get_team_selection()
        if not team_abbr:
            return
        
        if choice == 1:
            days = self.get_days_selection()
            print(f"\n⏳ Fetching recent games for {team_abbr}...")
            games = self.nba.get_recent_games(days=days, team=team_abbr)
            
            if games:
                self.nba.display_recent_games(games)
                print(f"\n📊 Total games found: {len(games)}")
                
                # Show team record
                wins, losses = self.calculate_record(games, team_abbr)
                print(f"\n🏆 {team_abbr} Record: {wins}-{losses}")
                if wins + losses > 0:
                    print(f"📈 Win Percentage: {(wins/(wins+losses)*100):.1f}%")
                
                # Ask if user wants to see detailed stats
                print("\n" + "-" * 80)
                see_details = input("\nWould you like to see detailed stats for any of these games? (y/n): ").strip().lower()
                if see_details == 'y':
                    self.select_game_for_stats(games)
            else:
                print(f"\n⚠️  No recent games found for {team_abbr}.")
        
        elif choice == 2:
            days = self.get_days_selection()
            print(f"\n⏳ Fetching upcoming games for {team_abbr}...")
            games = self.nba.get_upcoming_games(days=days, team=team_abbr)
            
            if games:
                self.nba.display_upcoming_games(games)
                print(f"\n📊 Total games scheduled: {len(games)}")
            else:
                print(f"\n⚠️  No upcoming games found for {team_abbr}.")
        
        elif choice == 3:
            days = self.get_days_selection()
            print(f"\n⏳ Fetching complete schedule for {team_abbr}...")
            recent = self.nba.get_recent_games(days=days, team=team_abbr)
            upcoming = self.nba.get_upcoming_games(days=days, team=team_abbr)
            
            if recent:
                self.nba.display_recent_games(recent)
                wins, losses = self.calculate_record(recent, team_abbr)
                print(f"\n🏆 Recent Record: {wins}-{losses}")
            
            if upcoming:
                self.nba.display_upcoming_games(upcoming)
            
            if not recent and not upcoming:
                print(f"\n⚠️  No games found for {team_abbr}.")
        
        self.pause()
    
    def game_stats_menu(self):
        """Menu for viewing detailed game statistics."""
        self.print_header("DETAILED GAME STATISTICS")
        
        print("\nHow would you like to select a game?")
        print("1. Choose from recent games")
        print("2. Enter game ID manually")
        print("3. Back to Main Menu")
        print()
        
        choice = self.get_user_choice(3)
        
        if choice == 1:
            days = self.get_days_selection()
            print(f"\n⏳ Fetching recent games...")
            games = self.nba.get_recent_games(days=days)
            
            if games:
                self.select_game_for_stats(games)
            else:
                print("\n⚠️  No recent games found.")
                self.pause()
        
        elif choice == 2:
            game_id = input("\nEnter the game ID: ").strip()
            if game_id:
                self.show_game_stats(game_id)
                self.pause()
    
    def select_game_for_stats(self, games):
        """Allow user to select a game from a list to view detailed stats."""
        self.print_header("SELECT A GAME")
        
        print("\nAvailable Games:")
        for i, game in enumerate(games[:20], 1):  # Limit to 20 games
            print(f"{i}. {game['date'][:10]} - {game['visitor_team_abbr']} ({game['visitor_score']}) @ "
                  f"{game['home_team_abbr']} ({game['home_score']}) - {game['status']}")
        
        if len(games) > 20:
            print(f"\n(Showing first 20 of {len(games)} games)")
        
        print(f"\n{min(len(games), 20) + 1}. Cancel")
        print()
        
        choice = self.get_user_choice(min(len(games), 20) + 1)
        
        if choice <= len(games):
            game = games[choice - 1]
            game_id = game['id']
            self.show_game_stats(game_id)
    
    def show_game_stats(self, game_id):
        """Display detailed statistics for a specific game."""
        print(f"\n⏳ Fetching detailed statistics for game {game_id}...")
        stats = self.nba.get_game_stats(game_id)
        
        if stats and stats.get('home_team'):
            self.nba.display_game_stats(stats)
        else:
            print(f"\n⚠️  Could not retrieve statistics for game {game_id}.")
    
    def show_all_teams(self):
        """Display all NBA teams."""
        self.print_header("ALL NBA TEAMS")
        
        print("\n⏳ Fetching team information...")
        teams = self.nba.get_teams()
        
        if teams:
            print(f"\n📊 Total Teams: {len(teams)}\n")
            print(f"{'ABBR':<6} {'TEAM NAME':<35} {'LOCATION':<20}")
            print("-" * 80)
            
            for team in sorted(teams, key=lambda x: x.get('abbreviation', '')):
                abbr = team.get('abbreviation', 'N/A')
                name = team.get('displayName', 'N/A')
                location = team.get('location', 'N/A')
                print(f"{abbr:<6} {name:<35} {location:<20}")
        else:
            print("\n⚠️  Could not retrieve team information.")
        
        self.pause()
    
    def get_team_selection(self):
        """Get team abbreviation from user."""
        print("\nEnter team abbreviation (e.g., LAL, BOS, GSW)")
        print("Type 'list' to see all teams, or 'cancel' to go back")
        
        while True:
            team_input = input("\nTeam: ").strip().upper()
            
            if team_input == 'CANCEL':
                return None
            elif team_input == 'LIST':
                teams = self.nba.get_teams()
                print("\nAvailable Teams:")
                for i, team in enumerate(sorted(teams, key=lambda x: x.get('abbreviation', '')), 1):
                    abbr = team.get('abbreviation', 'N/A')
                    name = team.get('displayName', 'N/A')
                    print(f"  {abbr:<6} - {name}")
                    if i % 3 == 0:
                        print()
                print()
            elif len(team_input) >= 2:
                return team_input
            else:
                print("❌ Please enter a valid team abbreviation")
    
    def get_days_selection(self):
        """Get number of days from user."""
        print("\nSelect time range:")
        print("1. 1 day")
        print("2. 3 days")
        print("3. 7 days")
        print("4. 14 days")
        print("5. Custom")
        print()
        
        choice = self.get_user_choice(5)
        
        if choice == 1:
            return 1
        elif choice == 2:
            return 3
        elif choice == 3:
            return 7
        elif choice == 4:
            return 14
        else:
            return self.get_custom_days()
    
    def get_custom_days(self):
        """Get custom number of days from user."""
        while True:
            try:
                days = int(input("\nEnter number of days (1-30): ").strip())
                if 1 <= days <= 30:
                    return days
                else:
                    print("❌ Please enter a number between 1 and 30")
            except ValueError:
                print("❌ Please enter a valid number")
    
    def calculate_record(self, games, team_abbr):
        """Calculate wins and losses for a team."""
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
        
        return wins, losses
    
    def exit_app(self):
        """Exit the application."""
        print("\n" + "=" * 80)
        print("Thanks for using NBA Stats Tool! 🏀")
        print("=" * 80)
        self.running = False
        sys.exit(0)
    
    def run(self):
        """Main application loop."""
        self.print_header("WELCOME TO NBA STATS TOOL")
        print("\nYour one-stop shop for NBA game information!")
        print("\nFeatures:")
        print("  • View recent game scores")
        print("  • See upcoming schedules")
        print("  • Get detailed player statistics")
        print("  • Track your favorite teams")
        print()
        self.pause()
        
        while self.running:
            try:
                self.main_menu()
            except KeyboardInterrupt:
                print("\n\nExiting...")
                self.exit_app()
            except Exception as e:
                print(f"\n❌ An error occurred: {e}")
                print("Returning to main menu...")
                self.pause()


def main():
    """Entry point for the application."""
    ui = NBAStatsUI()
    ui.run()


if __name__ == "__main__":
    main()
