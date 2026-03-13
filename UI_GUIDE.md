# NBA Stats Tool - User Interface Guide

## 🚀 Quick Start

Launch the interactive interface:

```bash
python3 nba_ui.py
```

Or use the start script:

```bash
python3 start.py
```

## 📋 Main Menu Options

When you launch the app, you'll see the main menu with these options:

### 1. View Recent Game Scores
- See completed games from the past N days
- Choose from preset time ranges (today, 3 days, 7 days) or enter a custom range
- View final scores for all games
- Option to view detailed stats for any game

**Example Flow:**
```
Main Menu → View Recent Game Scores → Last 3 days → [Shows scores] → View details? (y/n)
```

### 2. View Upcoming Game Schedule
- See scheduled games for the next N days
- Choose from preset time ranges or custom
- View matchups and game times

**Example Flow:**
```
Main Menu → View Upcoming Game Schedule → Next 7 days → [Shows schedule]
```

### 3. Search by Team
- Filter games by your favorite team
- Three sub-options:
  - **Team's Recent Games** - See past games with team record (W-L)
  - **Team's Upcoming Games** - See future schedule
  - **Complete Schedule** - Both recent and upcoming games

**Example Flow:**
```
Main Menu → Search by Team → Team's Recent Games → Enter: LAL → Last 7 days → [Shows Lakers games + record]
```

**Entering Team Names:**
- Type the 3-letter abbreviation (e.g., LAL, BOS, GSW)
- Type 'list' to see all team abbreviations
- Type 'cancel' to go back

### 4. View Detailed Game Statistics
- Get player-by-player box scores for specific games
- Two ways to select a game:
  - **Choose from recent games** - Pick from a list
  - **Enter game ID manually** - If you know the ID

**Example Flow:**
```
Main Menu → View Detailed Game Statistics → Choose from recent games → Last 3 days → Select game #2 → [Shows full box score]
```

### 5. View All NBA Teams
- Display complete list of all NBA teams
- Shows abbreviation, full name, and location
- Useful reference when using team search

## 🎯 Features

### Smart Game Selection
When viewing recent games, you can:
1. See the list of games with scores
2. Choose any game to view detailed player statistics
3. Get complete box scores with all player stats

### Team Record Tracking
When viewing a team's recent games, the app automatically calculates:
- Win-Loss record
- Win percentage
- Game-by-game results

### Flexible Time Ranges
For most queries, you can choose:
- **Preset options:** 1 day, 3 days, 7 days, 14 days
- **Custom range:** Enter any number between 1-30 days

## 📊 Understanding the Output

### Recent Games Display
```
2026-03-13 - Final
  CHI  130  @  LAL  142
  Chicago Bulls
  Los Angeles Lakers
```
- Date and game status
- Visitor team (away) @ Home team
- Final scores

### Upcoming Games Display
```
2026-03-14 02:00
  MIN   @  GS  
  Minnesota Timberwolves @ Golden State Warriors
```
- Date and time (UTC)
- Team matchup
- Full team names

### Detailed Game Stats
```
Player               MIN   PTS  REB  AST     FG    3PT     FT
LeBron James        34:25   28    8    7   10-18   2-5   6-7
```
- Player name
- Minutes played
- Points, Rebounds, Assists
- Field Goals (made-attempted)
- 3-Pointers (made-attempted)
- Free Throws (made-attempted)

## 💡 Tips & Tricks

### 1. Quick Daily Check
```
Main Menu → Option 1 → Today → See scores for the day
```

### 2. Follow Your Team
```
Main Menu → Option 3 → Complete Schedule → Enter team → Last 7 days
```
This shows both recent performance and upcoming games.

### 3. Find Top Performers
```
Main Menu → Option 4 → Choose from recent games → Select a game
```
Look at the box score to see who led in scoring, rebounds, assists, etc.

### 4. Plan Your Week
```
Main Menu → Option 2 → Next 7 days → See all upcoming games
```

### 5. Team Comparison
View a recent game's detailed stats to compare team performance:
- Total points by each team
- Individual player contributions
- Shooting percentages (from FG, 3PT, FT columns)

## 🎮 Navigation

- **Numbers:** Select menu options by typing the number
- **Enter:** Press Enter to continue after viewing results
- **Ctrl+C:** Exit the application at any time
- **Back options:** Most menus have a "Back to Main Menu" option

## ⌨️ Input Examples

### Team Abbreviations
```
LAL   - Los Angeles Lakers
BOS   - Boston Celtics
GSW   - Golden State Warriors
MIA   - Miami Heat
CHI   - Chicago Bulls
```

Type 'list' when prompted for a team to see all available teams.

### Time Ranges
- Presets: Just select the number (1-4)
- Custom: Select option 5, then enter 1-30

### Game Selection
When shown a list of games, just type the number:
```
1. 2026-03-13 - CHI (130) @ LAL (142)
2. 2026-03-13 - DAL (120) @ MEM (112)
3. 2026-03-13 - DEN (136) @ SA (131)

Select an option (1-4): 2
```

## 🔄 Common Workflows

### Check Today's Scores and Pick a Game to Analyze
1. Main Menu → 1 (Recent Scores)
2. Choose 1 (Today)
3. View the scores
4. Enter 'y' when asked about detailed stats
5. Select a game number
6. View full box score

### Track Lakers Performance This Week
1. Main Menu → 3 (Search by Team)
2. Choose 1 (Recent Games)
3. Enter: LAL
4. Choose time range: 7 days
5. View games, record, and win percentage
6. Optionally view detailed stats

### Plan Upcoming Games to Watch
1. Main Menu → 2 (Upcoming Schedule)
2. Choose 3 (Next 7 days)
3. See all scheduled games
4. Note interesting matchups

## ❓ Troubleshooting

**No games found:**
- Try a different time range
- Check if it's NBA off-season (typically July-September)
- Verify your internet connection

**Invalid team abbreviation:**
- Type 'list' to see all valid abbreviations
- Make sure you're using uppercase (LAL, not lal)

**Game stats not loading:**
- Some games may not have detailed stats available yet
- Try a different game from the list

**App freezes:**
- Press Ctrl+C to exit
- Restart the application

## 🏀 Enjoy!

The NBA Stats Tool makes it easy to stay updated on all NBA action. Whether you're tracking your favorite team or checking league-wide scores, everything is just a few keystrokes away!

For programmatic access, see the main README.md for API usage.
