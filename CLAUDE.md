# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python automation tool for managing LeekWars game accounts. LeekWars is a programming game where players write JavaScript AI code for virtual leeks (characters) to fight automatically. This gardener script automates account management tasks like launching fights, spending capital points, registering for tournaments, and synchronizing AI code between accounts.

## Setup and Dependencies

**Virtual Environment Setup (Recommended):**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the script
python main.py
```

**Dependencies:**
- Python 3
- requests==2.21.0

**Note**: Always use a virtual environment to isolate dependencies and avoid conflicts with system packages.

**Command line options:**
- `-f, --fight`: Force fighting even if disabled in settings
- `-nf, --no-fight`: Disable fighting even if enabled in settings  
- `-sr, --speedrun`: Enable speedrun mode (skip waiting between fights)
- `-nsr, --no-speedrun`: Disable speedrun mode
- `-s, --sync`: Force AI synchronization
- `-ns, --no-sync`: Disable AI synchronization

## Architecture

**Core Components:**

1. **main.py** - Entry point and main execution loop
   - Handles command line arguments and global settings (fight/speedrun/sync/shutdown modes)
   - Iterates through accounts and orchestrates the automation workflow
   - Controls fight execution and capital spending

2. **lwapi.py** - LeekWars API wrapper
   - Handles authentication and HTTP requests to leekwars.com
   - Implements fight launching (solo/farmer/team), opponent selection strategies
   - Manages fight result polling and AI code synchronization
   - Contains API endpoints for tournaments, capital spending, fight purchases

3. **todolist.py** - Fight behavior and task management
   - Implements different fighting behaviors (BALANCED, EQUALIZE, FARMING, SOLO_*, etc.)
   - Generates fight sequences based on account configuration
   - Handles capital point allocation according to specified goals
   - Manages tournament registration and AI synchronization tasks

4. **settings.py** - Account configuration
   - Contains the `Accounts` class with all account credentials and behaviors
   - Defines fighting strategies, capital spending goals, and synchronization settings
   - **WARNING**: Contains credentials - never commit real passwords

5. **utils.py** - Constants and utilities
   - Defines game constants (leek IDs, fight types, behaviors, strategies, goals)
   - Color codes for terminal output formatting
   - Enums for behaviors, states, strategies, and capital allocation goals

**Key Concepts:**

- **Behaviors**: How fights are distributed (BALANCED splits between all leeks, FARMING focuses on farmer, EQUALIZE levels up weaker leeks first, TODOLIST follows exact fight counts)
- **Strategies**: How opponents are chosen (RANDOM, BEST talent, WORST talent)
- **Goals**: How capital points are spent (FOCUS_LIFE, FOCUS_STRENGTH, etc.)
- **Synchronization**: Upload/download AI code between local files and LeekWars accounts

## Configuration

Account configuration in `settings.py` requires:
- `login`, `password`: LeekWars credentials
- `behavior`: Fighting strategy (BALANCED, EQUALIZE, FARMING, SOLO_*, TODOLIST, NONE)
- `limit`: Number of fights to keep in reserve (ignored for TODOLIST behavior)
- `strategy`: Opponent selection (RANDOM, BEST, WORST)

Optional settings:
- `buy_fight`: Auto-purchase fight packs with habs
- `team_limit`: Number of team fights to reserve
- `tournaments`: List of entities to register for tournaments
- `goals`: Capital spending configuration per leek
- `synchronize`: AI code sync settings with directory and transfer direction

## Development Guidelines

**Code Style:**
- Preserve existing French variable names and comments to maintain consistency
- Use snake_case for variables and functions (existing style: `farmer_id`, `fight_id`, `nb_fight`)
- Keep existing class naming conventions (CamelCase: `Todolist`, `Accounts`)
- Maintain existing indentation style (tabs used throughout)
- Preserve color output formatting using `bcolors` class

**Python Best Practices:**
- Add type hints to new functions while preserving existing signatures
- Use context managers for file operations during AI synchronization
- Handle API exceptions gracefully with try/except blocks
- Add docstrings to new methods following existing minimal style
- Validate user input in settings.py before processing
- Use `requests.Session()` for connection pooling (already implemented)

**Security Considerations:**
- Never commit real credentials in settings.py
- Consider using environment variables for sensitive data
- Validate API responses before processing
- Add rate limiting to prevent API abuse

**Testing and Debugging:**
- Test with minimal fight limits to avoid account penalties
- Use NONE behavior for connection testing without fighting
- Verify AI synchronization on test accounts first
- Monitor API response codes for authentication issues

**Commit Message Guidelines:**
- Use sober, factual language describing what changed
- Start with action verbs (Add, Fix, Update, Remove, Refactor)
- Be succinct but comprehensive - cover all changes without verbosity
- Avoid emotional language, marketing terms, or excessive enthusiasm
- Group related changes logically (features, fixes, technical improvements)
- Example format: "Add Rich UI tables and progress bars for status display"

**Technical Notes:**
- API calls target `https://leekwars.com/api/*` endpoints
- Fight results polled with 2-second intervals (configurable via `g.DELAY`)
- Speedrun mode disables capital allocation due to timing constraints
- Team fights require user leeks in existing compositions
- AI sync preserves existing file structure and overwrites matching files

## Warnings and Reminders

- **Security Reminder**: 
  - Never commit changes in `settings.py` to prevent leaking passwords