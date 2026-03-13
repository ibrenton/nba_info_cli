#!/usr/bin/env python3
"""
NBA Stats Tool - Enhanced Interactive User Interface with Rich Colors

Interactive command-line interface with beautiful formatting for browsing NBA game data.
"""

from nba_stats import NBAStats
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich import box
from rich.align import Align
from rich.text import Text

console = Console()


class NBAStatsUI:
    """Enhanced interactive user interface for NBA Stats tool with rich colors."""
    
    def __init__(self):
        self.nba = NBAStats()
        self.running = True
        self.selected_team = None
        self.teams_dict = {}  # Cache for team lookups
        self.primary_color = 'cyan'  # Default color
        self.secondary_color = 'yellow'  # Default color
    
    def clear_screen(self):
        """Clear the terminal screen."""
        console.clear()
    
    def print_welcome(self):
        """Print a colorful welcome banner."""
        self.clear_screen()
        
        welcome_panel = Panel(
            "[bold yellow]🏀 NBA STATS TOOL 🏀[/bold yellow]\n\n"
            "[bold white]Your One-Stop Shop for Live NBA Game Data[/bold white]",
            style="bold cyan",
            border_style="cyan",
            expand=False
        )
        console.print(welcome_panel)
    
    def print_header(self, title, emoji="🏀"):
        """Print a formatted header with color."""
        panel = Panel(
            f"[bold {self.secondary_color}]{emoji} {title}[/bold {self.secondary_color}]",
            style=f"bold {self.primary_color}",
            expand=True,
            border_style=self.primary_color
        )
        console.print(panel)
    
    def print_menu(self, title, options):
        """Print a colorful menu with numbered options."""
        self.print_header(title)
        
        table = Table(show_header=False, box=box.ROUNDED, border_style=self.primary_color)
        table.add_column("#", justify="center", style=f"bold {self.secondary_color}", width=3)
        table.add_column("Option", style="white")
        
        for i, option in enumerate(options, 1):
            table.add_row(f"[bold {self.secondary_color}]{i}[/bold {self.secondary_color}]", option)
        
        extra_num = len(options) + 1
        extra_text = "Back to Main Menu" if title != "NBA STATS TOOL - MAIN MENU" else "Exit"
        table.add_row(f"[bold red]{extra_num}[/bold red]", f"[bold red]{extra_text}[/bold red]")
        
        console.print(table)
        console.print()
    
    def get_user_choice(self, max_option):
        """Get and validate user input with color."""
        while True:
            try:
                choice = Prompt.ask(
                    f"[bold {self.primary_color}]Select an option[/bold {self.primary_color}]",
                    default="1"
                )
                choice_num = int(choice)
                if 1 <= choice_num <= max_option:
                    return choice_num
                else:
                    console.print(f"[bold red]❌ Please enter a number between 1 and {max_option}[/bold red]")
            except ValueError:
                console.print("[bold red]❌ Please enter a valid number[/bold red]")
            except KeyboardInterrupt:
                console.print(f"\n[bold {self.secondary_color}]👋 Thanks for using NBA Stats Tool![/bold {self.secondary_color}]")
                sys.exit(0)
    
    def pause(self):
        """Pause and wait for user to press Enter."""
        Prompt.ask("[grey50]Press Enter to continue[/grey50]", default="")
    
    def load_teams(self):
        """Load and cache team data."""
        if not self.teams_dict:
            teams = self.nba.get_teams()
            for team in teams:
                self.teams_dict[team['abbreviation']] = team
    
    def set_team_colors(self, team_abbr):
        """Set UI colors based on selected team."""
        if team_abbr in self.teams_dict:
            team = self.teams_dict[team_abbr]
            self.primary_color = team.get('primary', 'cyan')
            self.secondary_color = team.get('secondary', 'yellow')
    
    def reset_to_default_colors(self):
        """Reset UI colors to default scheme."""
        self.primary_color = 'cyan'
        self.secondary_color = 'yellow'
    
    def select_team_prompt(self):
        """Allow user to select a team or use all teams."""
        self.print_header("TEAM SELECTION", "🏆")
        
        console.print(f"[bold {self.primary_color}]Would you like to filter by a specific team?[/bold {self.primary_color}]\n")
        
        table = Table(show_header=False, box=box.ROUNDED, border_style=self.primary_color)
        table.add_column("#", justify="center", style=f"bold {self.secondary_color}", width=3)
        table.add_column("Option", style="white")
        
        table.add_row(f"[bold {self.secondary_color}]1[/bold {self.secondary_color}]", "View All Teams")
        table.add_row(f"[bold {self.secondary_color}]2[/bold {self.secondary_color}]", "Select Specific Team")
        table.add_row("[bold red]3[/bold red]", "Back to Main Menu")
        
        console.print(table)
        console.print()
        
        choice = self.get_user_choice(3)
        
        if choice == 1:
            self.selected_team = None
            self.reset_to_default_colors()  # Revert to default colors
            return True
        elif choice == 2:
            team = self.get_team_selection()
            if team:
                self.selected_team = team
                self.set_team_colors(team)  # Update colors when team is selected
                return True
            return False
        else:
            return False
    
    def get_team_selection(self):
        """Get team abbreviation from user with rich display."""
        self.print_header("SELECT A TEAM", "🏀")
        
        self.load_teams()
        
        console.print("[bold cyan]Enter team abbreviation (e.g., LAL, BOS, GSW)[/bold cyan]")
        console.print("[bold yellow]Type 'list' to see all teams, or 'cancel' to go back\n[/bold yellow]")
        
        while True:
            team_input = Prompt.ask("[bold green]Team[/bold green]").strip().upper()
            
            if team_input == 'CANCEL':
                return None
            elif team_input == 'LIST':
                self.show_teams_for_selection()
            elif len(team_input) >= 2:
                if team_input in self.teams_dict:
                    team_name = self.teams_dict[team_input].get('displayName', team_input)
                    console.print(f"\n[bold green]✓ Selected: {team_name}[/bold green]\n")
                    return team_input
                else:
                    console.print(f"[bold red]❌ Team '{team_input}' not found. Type 'list' to see all teams.[/bold red]\n")
            else:
                console.print("[bold red]❌ Please enter a valid team abbreviation[/bold red]\n")
    
    def show_teams_for_selection(self):
        """Display all teams in a colorful table."""
        self.print_header("ALL NBA TEAMS", "📋")
        
        self.load_teams()
        teams = sorted(self.teams_dict.values(), key=lambda x: x.get('abbreviation', ''))
        
        table = Table(title="[bold yellow]30 NBA Teams[/bold yellow]", box=box.ROUNDED, border_style="cyan")
        table.add_column("ABBR", justify="center", style="bold yellow", width=6)
        table.add_column("Team Name", style="cyan")
        table.add_column("Location", style="magenta")
        
        for team in teams:
            abbr = team.get('abbreviation', 'N/A')
            name = team.get('displayName', 'N/A')
            location = team.get('location', 'N/A')
            table.add_row(abbr, name, location)
        
        console.print(table)
        console.print()
    
    def main_menu(self):
        """Display and handle main menu."""
        self.print_header("MAIN MENU", "🏀")
        
        # Show selected team if any
        if self.selected_team:
            team_name = self.teams_dict.get(self.selected_team, {}).get('displayName', self.selected_team)
            console.print(f"[bold {self.primary_color}]📌 Currently viewing: {team_name} ({self.selected_team})[/bold {self.primary_color}]\n")
        
        options = [
            "📊 View Recent Game Scores",
            "📅 View Upcoming Game Schedule",
            "🔍 Change Team Selection",
            "📈 View Detailed Game Statistics",
            "🏀 View All NBA Teams"
        ]
        
        self.print_menu("NBA STATS TOOL - MAIN MENU", options)
        choice = self.get_user_choice(len(options) + 1)
        
        if choice == 1:
            self.recent_games_menu()
        elif choice == 2:
            self.upcoming_games_menu()
        elif choice == 3:
            if self.select_team_prompt():
                # Colors updated in select_team_prompt
                pass
        elif choice == 4:
            self.game_stats_menu()
        elif choice == 5:
            self.show_all_teams()
        elif choice == len(options) + 1:
            self.exit_app()
    
    def recent_games_menu(self):
        """Menu for viewing recent games."""
        self.print_header("RECENT GAME SCORES", "📊")
        
        console.print(f"[bold {self.primary_color}]How many days back would you like to see?[/bold {self.primary_color}]\n")
        
        options = ["1 day", "3 days", "7 days", "14 days", "Custom"]
        
        table = Table(show_header=False, box=box.ROUNDED, border_style=self.primary_color)
        table.add_column("#", justify="center", style=f"bold {self.secondary_color}", width=3)
        table.add_column("Option", style="white")
        
        for i, option in enumerate(options, 1):
            table.add_row(f"[bold {self.secondary_color}]{i}[/bold {self.secondary_color}]", option)
        table.add_row(f"[bold red]6[/bold red]", "Back to Main Menu")
        
        console.print(table)
        console.print()
        
        choice = self.get_user_choice(6)
        
        if choice == 1:
            days = 1
        elif choice == 2:
            days = 3
        elif choice == 3:
            days = 7
        elif choice == 4:
            days = 14
        elif choice == 5:
            days = self.get_custom_days()
        else:
            return
        
        console.print(f"\n[bold {self.secondary_color}]⏳ Fetching games from the last {days} day(s)...[/bold {self.secondary_color}]")
        games = self.nba.get_recent_games(days=days, team=self.selected_team)
        
        if games:
            self.display_recent_games_table(games)
            console.print(f"\n[bold {self.primary_color}]📊 Total games found: {len(games)}[/bold {self.primary_color}]")
            
            # Ask if user wants to see detailed stats
            console.print("\n" + "─" * 80)
            see_details = Prompt.ask(
                f"[bold {self.primary_color}]Would you like to see detailed stats for any of these games?[/bold {self.primary_color}]",
                choices=["y", "n"],
                default="n"
            )
            if see_details == 'y':
                self.select_game_for_stats(games)
        else:
            console.print("\n[bold red]⚠️  No games found for the selected criteria.[/bold red]")
        
        self.pause()
    
    def upcoming_games_menu(self):
        """Menu for viewing upcoming games."""
        self.print_header("UPCOMING GAME SCHEDULE", "📅")
        
        console.print("[bold cyan]How many days ahead would you like to see?[/bold cyan]\n")
        
        options = ["Today", "3 days", "7 days", "14 days", "Custom"]
        
        table = Table(show_header=False, box=box.ROUNDED, border_style="cyan")
        table.add_column("#", justify="center", style="bold yellow", width=3)
        table.add_column("Option", style="white")
        
        for i, option in enumerate(options, 1):
            table.add_row(f"[bold yellow]{i}[/bold yellow]", option)
        table.add_row(f"[bold red]6[/bold red]", "Back to Main Menu")
        
        console.print(table)
        console.print()
        
        choice = self.get_user_choice(6)
        
        if choice == 1:
            days = 1
        elif choice == 2:
            days = 3
        elif choice == 3:
            days = 7
        elif choice == 4:
            days = 14
        elif choice == 5:
            days = self.get_custom_days()
        else:
            return
        
        console.print(f"\n[bold yellow]⏳ Fetching upcoming games for the next {days} day(s)...[/bold yellow]")
        games = self.nba.get_upcoming_games(days=days, team=self.selected_team)
        
        if games:
            self.display_upcoming_games_table(games)
            print(f"\n[bold cyan]📊 Total games scheduled: {len(games)}[/bold cyan]")
        else:
            console.print("\n[bold red]⚠️  No upcoming games found for the selected criteria.[/bold red]")
        
        self.pause()
    
    def game_stats_menu(self):
        """Menu for viewing detailed game statistics."""
        self.print_header("DETAILED GAME STATISTICS", "📈")
        
        console.print("[bold cyan]How would you like to select a game?[/bold cyan]\n")
        
        table = Table(show_header=False, box=box.ROUNDED, border_style="cyan")
        table.add_column("#", justify="center", style="bold yellow", width=3)
        table.add_column("Option", style="white")
        
        table.add_row("[bold yellow]1[/bold yellow]", "Choose from recent games")
        table.add_row("[bold yellow]2[/bold yellow]", "Enter game ID manually")
        table.add_row("[bold red]3[/bold red]", "Back to Main Menu")
        
        console.print(table)
        console.print()
        
        choice = self.get_user_choice(3)
        
        if choice == 1:
            days = self.get_days_selection()
            console.print(f"\n[bold yellow]⏳ Fetching recent games...[/bold yellow]")
            games = self.nba.get_recent_games(days=days, team=self.selected_team)
            
            if games:
                self.select_game_for_stats(games)
            else:
                console.print("\n[bold red]⚠️  No recent games found.[/bold red]")
                self.pause()
        
        elif choice == 2:
            game_id = Prompt.ask("[bold green]Game ID[/bold green]").strip()
            if game_id:
                self.show_game_stats(game_id)
                self.pause()
    
    def select_game_for_stats(self, games):
        """Allow user to select a game from a list to view detailed stats."""
        self.print_header("SELECT A GAME", "🎯")
        
        console.print("[bold cyan]Available Games:[/bold cyan]\n")
        
        table = Table(box=box.ROUNDED, border_style="cyan")
        table.add_column("#", justify="center", style="bold yellow", width=3)
        table.add_column("Date", style="cyan", width=12)
        table.add_column("Away", style="magenta", width=8)
        table.add_column("Score", style="white", justify="center", width=8)
        table.add_column("Home", style="magenta", width=8)
        table.add_column("Score", style="white", justify="center", width=8)
        table.add_column("Status", style="yellow", width=10)
        
        display_games = games[:20]
        for i, game in enumerate(display_games, 1):
            date_str = game['date'][:10]
            away_abbr = game['visitor_team_abbr']
            away_score = str(game['visitor_score'])
            home_abbr = game['home_team_abbr']
            home_score = str(game['home_score'])
            status = game['status']
            
            # Color code the score
            if away_score != '' and home_score != '':
                if int(away_score) > int(home_score):
                    away_score = f"[bold green]{away_score}[/bold green]"
                    home_score = f"[red]{home_score}[/red]"
                else:
                    away_score = f"[red]{away_score}[/red]"
                    home_score = f"[bold green]{home_score}[/bold green]"
            
            table.add_row(f"[bold yellow]{i}[/bold yellow]", date_str, away_abbr, away_score, home_abbr, home_score, status)
        
        console.print(table)
        
        if len(games) > 20:
            console.print(f"\n[grey50](Showing first 20 of {len(games)} games)[/grey50]")
        
        print()
        
        choice = self.get_user_choice(min(len(games), 20) + 1)
        
        if choice <= len(games):
            game = games[choice - 1]
            game_id = game['id']
            self.show_game_stats(game_id)
    
    def show_game_stats(self, game_id):
        """Display detailed statistics for a specific game."""
        console.print(f"\n[bold yellow]⏳ Fetching detailed statistics...[/bold yellow]")
        stats = self.nba.get_game_stats(game_id)
        
        if stats and stats.get('home_team'):
            self.display_game_stats_table(stats)
        else:
            console.print(f"\n[bold red]⚠️  Could not retrieve statistics for game {game_id}.[/bold red]")
    
    def show_all_teams(self):
        """Display all NBA teams."""
        self.show_teams_for_selection()
        self.pause()
    
    def get_days_selection(self):
        """Get number of days from user."""
        self.print_header("SELECT TIME RANGE", "⏰")
        
        options = ["1 day", "3 days", "7 days", "14 days", "Custom"]
        
        table = Table(show_header=False, box=box.ROUNDED, border_style="cyan")
        table.add_column("#", justify="center", style="bold yellow", width=3)
        table.add_column("Option", style="white")
        
        for i, option in enumerate(options, 1):
            table.add_row(f"[bold yellow]{i}[/bold yellow]", option)
        table.add_row(f"[bold red]6[/bold red]", "Back")
        
        console.print(table)
        console.print()
        
        choice = self.get_user_choice(6)
        
        if choice == 1:
            return 1
        elif choice == 2:
            return 3
        elif choice == 3:
            return 7
        elif choice == 4:
            return 14
        elif choice == 5:
            return self.get_custom_days()
        else:
            return 7  # Default
    
    def get_custom_days(self):
        """Get custom number of days from user."""
        while True:
            try:
                days = int(Prompt.ask("[bold green]Number of days[/bold green] (1-30)", default="7"))
                if 1 <= days <= 30:
                    return days
                else:
                    console.print("[bold red]❌ Please enter a number between 1 and 30[/bold red]")
            except ValueError:
                console.print("[bold red]❌ Please enter a valid number[/bold red]")
    
    def display_recent_games_table(self, games):
        """Display recent games in a colorful table."""
        console.print()
        
        table = Table(title=f"[bold {self.secondary_color}]Recent Game Results[/bold {self.secondary_color}]", box=box.ROUNDED, border_style=self.primary_color)
        table.add_column("Date", style="cyan", width=12)
        table.add_column("Away Team", style="magenta", width=15)
        table.add_column("Score", style="white", justify="center", width=10)
        table.add_column("Home Team", style="magenta", width=15)
        table.add_column("Score", style="white", justify="center", width=10)
        table.add_column("Status", style="yellow", width=8)
        
        for game in games:
            date_str = game['date'][:10]
            away_team = f"{game['visitor_team_abbr']} {game['visitor_team'].split()[-1]}"
            away_score = str(game['visitor_score'])
            home_team = f"{game['home_team_abbr']} {game['home_team'].split()[-1]}"
            home_score = str(game['home_score'])
            status = game['status']
            
            # Color code winning team
            if int(away_score) > int(home_score):
                away_score = f"[bold green]{away_score}[/bold green]"
                home_score = f"[red]{home_score}[/red]"
            else:
                away_score = f"[red]{away_score}[/red]"
                home_score = f"[bold green]{home_score}[/bold green]"
            
            table.add_row(date_str, away_team, away_score, home_team, home_score, status)
        
        console.print(table)
    
    def display_upcoming_games_table(self, games):
        """Display upcoming games in a colorful table."""
        console.print()
        
        table = Table(title=f"[bold {self.secondary_color}]Upcoming Games[/bold {self.secondary_color}]", box=box.ROUNDED, border_style=self.primary_color)
        table.add_column("Date", style="cyan", width=12)
        table.add_column("Time (PT)", style="yellow", width=12)
        table.add_column("Away Team", style="magenta", width=15)
        table.add_column("vs", style="white", justify="center", width=3)
        table.add_column("Home Team", style="magenta", width=15)
        
        for game in games:
            date_str = game['date'][:10]
            # Convert UTC time to Pacific time
            time_str = self.nba._convert_to_pacific_time(game['date']) if game.get('date') else "--:-- PT"
            away_team = f"{game['visitor_team_abbr']} {game['visitor_team'].split()[-1]}"
            home_team = f"{game['home_team_abbr']} {game['home_team'].split()[-1]}"
            
            table.add_row(date_str, time_str, away_team, "vs", home_team)
        
        console.print(table)
    
    def display_game_stats_table(self, stats):
        """Display game statistics in colorful tables."""
        console.print()
        
        # Game header
        header = f"[bold yellow]{stats.get('visitor_team')}[/bold yellow] [bold white]vs[/bold white] [bold yellow]{stats.get('home_team')}[/bold yellow]"
        score = f"[bold green]{stats.get('visitor_score')}[/bold green] - [bold green]{stats.get('home_score')}[/bold green]"
        
        console.print(f"\n{header}")
        console.print(f"Final Score: {score}\n")
        
        # Visitor team stats
        visitor_table = Table(title=f"[bold magenta]{stats.get('visitor_team')} - Player Stats[/bold magenta]", 
                             box=box.ROUNDED, border_style="magenta")
        visitor_table.add_column("Player", style="cyan", width=20)
        visitor_table.add_column("MIN", justify="center", style="white", width=6)
        visitor_table.add_column("PTS", justify="center", style="yellow", width=4)
        visitor_table.add_column("REB", justify="center", style="white", width=4)
        visitor_table.add_column("AST", justify="center", style="white", width=4)
        visitor_table.add_column("FG", justify="center", style="green", width=8)
        visitor_table.add_column("3PT", justify="center", style="green", width=8)
        visitor_table.add_column("FT", justify="center", style="green", width=8)
        
        for player in stats.get('visitor_player_stats', []):
            points_color = "bold yellow" if int(player.get('points', 0)) >= 20 else "white"
            visitor_table.add_row(
                player['player'][:20],
                str(player.get('minutes', '0:00')),
                f"[{points_color}]{player['points']}[/{points_color}]",
                str(player['rebounds']),
                str(player['assists']),
                str(player.get('fg', '0-0')),
                str(player.get('fg3', '0-0')),
                str(player.get('ft', '0-0'))
            )
        
        console.print(visitor_table)
        
        # Home team stats
        home_table = Table(title=f"[bold magenta]{stats.get('home_team')} - Player Stats[/bold magenta]", 
                          box=box.ROUNDED, border_style="magenta")
        home_table.add_column("Player", style="cyan", width=20)
        home_table.add_column("MIN", justify="center", style="white", width=6)
        home_table.add_column("PTS", justify="center", style="yellow", width=4)
        home_table.add_column("REB", justify="center", style="white", width=4)
        home_table.add_column("AST", justify="center", style="white", width=4)
        home_table.add_column("FG", justify="center", style="green", width=8)
        home_table.add_column("3PT", justify="center", style="green", width=8)
        home_table.add_column("FT", justify="center", style="green", width=8)
        
        for player in stats.get('home_player_stats', []):
            points_color = "bold yellow" if int(player.get('points', 0)) >= 20 else "white"
            home_table.add_row(
                player['player'][:20],
                str(player.get('minutes', '0:00')),
                f"[{points_color}]{player['points']}[/{points_color}]",
                str(player['rebounds']),
                str(player['assists']),
                str(player.get('fg', '0-0')),
                str(player.get('fg3', '0-0')),
                str(player.get('ft', '0-0'))
            )
        
        console.print(home_table)
    
    def exit_app(self):
        """Exit the application."""
        self.clear_screen()
        exit_panel = Panel(
            "[bold yellow]Thanks for using NBA Stats Tool!  👋[/bold yellow]\n\n"
            "[bold white]Stay tuned for more NBA action!  🏀[/bold white]",
            style="bold cyan",
            border_style="cyan",
            expand=False
        )
        console.print(exit_panel)
        self.running = False
        sys.exit(0)
    
    def run(self):
        """Main application loop."""
        self.print_welcome()
        
        console.print("[bold cyan]Welcome to your NBA companion![/bold cyan]")
        console.print("[bold white]Track scores, schedules, and player stats in real-time.[/bold white]\n")
        self.pause()
        
        # Initial team selection
        if not self.select_team_prompt():
            self.exit_app()
        
        while self.running:
            try:
                self.main_menu()
            except KeyboardInterrupt:
                console.print("\n[bold yellow]👋 Exiting...[/bold yellow]")
                self.exit_app()
            except Exception as e:
                console.print(f"\n[bold red]❌ An error occurred: {e}[/bold red]")
                console.print("[bold yellow]Returning to main menu...[/bold yellow]\n")
                self.pause()


def main():
    """Entry point for the application."""
    ui = NBAStatsUI()
    ui.run()


if __name__ == "__main__":
    main()
