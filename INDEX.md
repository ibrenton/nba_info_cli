# NBA Stats Tool - Index & Navigation Guide

Welcome to the NBA Stats Tool! This document will help you navigate the project and find what you need.

## 🚀 Quick Start (2 Minutes)

```bash
# Install dependency
python3 -m pip install requests

# Launch the interactive UI
python3 start.py
```

That's it! Follow the menu options to:
- View recent game scores
- See upcoming schedules
- Track your favorite teams
- Get detailed player statistics

---

## 📋 Documentation Navigation

### 👤 I'm a Regular User - I Want to Use the UI

**Start here:** [UI_GUIDE.md](UI_GUIDE.md)
- Complete guide to the interactive interface
- Menu options explained
- Common workflows
- Tips and tricks

**Quick reference:** [QUICK_START.md](QUICK_START.md)
- 5-minute quick start
- Sample commands
- Common team abbreviations

**Command:** `python3 start.py`

---

### 👨‍💻 I'm a Developer - I Want to Use the Python API

**Start here:** [README.md](README.md) - API Reference section
- Complete API documentation
- All methods and parameters
- Code examples
- Data structures

**Code examples:** [examples.py](examples.py)
- 8 practical code examples
- Copy and adapt for your needs

**Sample code:**
```python
from nba_stats import NBAStats

nba = NBAStats()
games = nba.get_recent_games(days=7, team='LAL')
nba.display_recent_games(games)
```

---

### 🏗️ I Want to Understand the Architecture

**Start here:** [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)
- Project structure
- Component descriptions
- Data flow diagrams
- Class and method details
- Future enhancement ideas

---

## 📁 File Guide

### Core Application Files

| File | Purpose | Size |
|------|---------|------|
| **nba_stats.py** | Main API module with NBAStats class | 15 KB |
| **nba_ui.py** | Interactive menu-based user interface | 15 KB |
| **start.py** | Quick launcher for the UI | 755 B |

### Documentation Files

| File | Best For | Size |
|------|----------|------|
| **README.md** | Full API reference and examples | 8.5 KB |
| **UI_GUIDE.md** | Using the interactive interface | 6.0 KB |
| **QUICK_START.md** | Getting started in 5 minutes | 1.7 KB |
| **PROJECT_OVERVIEW.md** | Understanding the architecture | 11 KB |
| **INDEX.md** | This file - navigation guide | - |

### Example Files

| File | Contains | Size |
|------|----------|------|
| **demo.py** | Comprehensive feature demonstration | 4.1 KB |
| **examples.py** | 8 practical code examples | 8.9 KB |

### Configuration

| File | Purpose |
|------|---------|
| **requirements.txt** | Python dependencies (just `requests`) |

---

## 🎯 Use Cases & How to Handle Them

### "I want to check today's NBA scores"
→ Run: `python3 start.py`
→ Select: Option 1 (Recent Scores)
→ Select: Option 1 (Today)

### "I want to see what games my favorite team has coming up"
→ Run: `python3 start.py`
→ Select: Option 3 (Search by Team)
→ Select: Option 3 (Upcoming Games)
→ Enter: Your team's abbreviation (e.g., LAL)

### "I want to see detailed player stats for a specific game"
→ Run: `python3 start.py`
→ Select: Option 4 (Game Statistics)
→ Select: Option 1 (From recent games)
→ Pick the game from the list

### "I want to integrate this into my Python project"
→ Copy `nba_stats.py` to your project
→ Import: `from nba_stats import NBAStats`
→ See README.md for API details

### "I want to automate NBA data collection"
→ Use the Python API in a script
→ See examples.py for code samples
→ Schedule with cron (Linux) or Task Scheduler (Windows)

### "I want to understand how this works"
→ Read: PROJECT_OVERVIEW.md
→ Look at: nba_stats.py comments
→ Run: examples.py to see it in action

---

## 🔍 Finding Specific Information

### Team Abbreviations
- **In UI:** Type 'list' when prompted for a team
- **In docs:** See README.md "Common Team Abbreviations" section
- **In code:** `nba.get_teams()` returns all teams

### Detailed Box Scores
- **In UI:** Menu option 4 (View Detailed Game Statistics)
- **In code:** `nba.get_game_stats(game_id)`
- **See:** README.md "get_game_stats()" section

### Team Records (W-L)
- **In UI:** Menu option 3 with recent games
- Automatically calculated and displayed
- Also accessible via Python: calculate from game results

### How to Get a Game ID
- Game IDs are shown in game lists
- Returned in game data dictionaries
- Can be entered manually in UI option 4

---

## 🎓 Learning Paths

### For Non-Technical Users
1. Read: QUICK_START.md (5 min)
2. Run: `python3 start.py`
3. Explore the menu options
4. Refer to: UI_GUIDE.md if you have questions

### For Developers
1. Read: README.md (10 min)
2. Look at: examples.py (5 min)
3. Try: `python3 examples.py`
4. Read: nba_stats.py comments (optional deep dive)
5. Create: Your own script using the API

### For System Architects
1. Read: PROJECT_OVERVIEW.md (15 min)
2. Review: File structure and architecture diagrams
3. Examine: nba_stats.py and nba_ui.py code
4. Plan: How to integrate into your system

---

## 🔑 Key Concepts

### Menu Options (Interactive UI)

| Number | Feature | Time Range Options |
|--------|---------|-------------------|
| 1 | View Recent Scores | 1/3/7/custom days back |
| 2 | View Upcoming Games | 1/3/7/custom days ahead |
| 3 | Search by Team | Same + team filtering |
| 4 | Game Statistics | Detailed box scores |
| 5 | All NBA Teams | Reference list |

### API Methods

```
get_recent_games(days=7, team=None)      → List[Game]
get_upcoming_games(days=7, team=None)    → List[Game]
get_game_stats(game_id)                  → Dict[GameStats]
get_teams()                              → List[Team]
display_recent_games(games)              → None (prints)
display_upcoming_games(games)            → None (prints)
display_game_stats(stats)                → None (prints)
```

### Data You Can Access

- **Game Results:** Scores, dates, teams, final status
- **Game Schedule:** Upcoming matchups, dates, teams
- **Player Stats:** Points, rebounds, assists, shooting %, steals, blocks
- **Team Info:** Names, abbreviations, locations
- **Team Records:** Win-loss percentages (calculated)

---

## 🆘 Troubleshooting

### "I get an error about requests module"
→ Run: `python3 -m pip install requests`

### "No games found"
→ Try a different time range
→ NBA season is Oct-June; check if it's off-season
→ Verify your internet connection

### "I don't know the team abbreviation"
→ In UI: Type 'list' when prompted for a team
→ In docs: Check README.md "Common Team Abbreviations"
→ Common ones: LAL, BOS, GSW, MIA, CHI, DAL, DEN

### "The UI is frozen"
→ Press: Ctrl+C to exit
→ Restart: `python3 start.py`

### "I can't find a specific game"
→ Try: Increasing the days range
→ Check: Game might be from different time
→ Use: Menu option 4 to search by game ID if you have it

---

## 📊 Project Statistics

- **Total Files:** 10
- **Total Size:** ~75 KB
- **Lines of Code:** ~500
- **Documentation:** 4 comprehensive guides
- **Code Examples:** 8+ examples
- **API Methods:** 7 core methods
- **Features:** 13+ major features

---

## 🎯 Feature Checklist

- ✅ Interactive menu-based UI
- ✅ Recent game scores
- ✅ Upcoming schedules
- ✅ Detailed player statistics
- ✅ Team-specific filtering
- ✅ Game selection from lists
- ✅ Win-loss record calculation
- ✅ All teams reference
- ✅ Custom time ranges
- ✅ Input validation
- ✅ Error handling
- ✅ Pretty-formatted output
- ✅ Python API for developers

---

## 🚀 Next Steps

### If You Want to Use the Tool
1. Install: `pip install -r requirements.txt`
2. Run: `python3 start.py`
3. Refer to: UI_GUIDE.md if needed

### If You Want to Develop with It
1. Read: README.md API section
2. Study: examples.py
3. Import: `from nba_stats import NBAStats`
4. Build: Your own features on top

### If You Want to Understand It
1. Read: PROJECT_OVERVIEW.md
2. Review: nba_stats.py code
3. Review: nba_ui.py code
4. Run: examples.py

### If You Want to Share It
1. Compress: `zip -r nba-stats-tool.zip *.py *.md requirements.txt`
2. Share: The zip file
3. Recipients run: `python3 start.py`

---

## 📞 Support

For different issues:

| Issue | Solution | Where |
|-------|----------|-------|
| "How do I use the UI?" | Read UI_GUIDE.md | UI_GUIDE.md |
| "How do I use the API?" | Read README.md | README.md API section |
| "How does it work?" | Read PROJECT_OVERVIEW.md | PROJECT_OVERVIEW.md |
| "Show me examples" | Run examples.py | examples.py or README.md |
| "Quick start" | Read QUICK_START.md | QUICK_START.md |

---

## 🎉 Summary

You now have a complete NBA Stats Tool with:
- ✅ Fully functional interactive UI
- ✅ Powerful Python API
- ✅ Comprehensive documentation
- ✅ Working code examples
- ✅ Real-time NBA data access

**Get started now:**
```bash
python3 -m pip install requests
python3 start.py
```

**Happy tracking!** 🏀

---

**Last Updated:** March 13, 2026
**Project Status:** Complete ✅
