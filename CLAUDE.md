# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an **Interactive Gantt Chart Manager** - a Python CLI application for creating and managing project roadmap timelines. It allows users to define project categories with multiple subcategories, each having start dates and durations, then generates professional Gantt chart visualizations as PNG images.

## Running the Application

```bash
# Run the interactive menu
python3 gantt_chart_interactive_1.py

# Install dependencies if needed
pip install matplotlib numpy
```

The script launches an interactive CLI menu with numbered options. No command-line arguments are needed.

## Data Architecture

### Core Data Structure

The application uses a nested dictionary structure stored globally as `categories`:

```python
categories = {
    "Category Name": [
        {
            "name": "Subcategory Name",
            "start": "YYYY-MM-DD",  # ISO date string
            "duration": 60           # Integer (days)
        },
        # ... more subcategories
    ],
    # ... more categories
}
```

### Data Persistence

- **Storage Location**: `~/gantt_outputs/gantt_data.json`
- **Format**: JSON with 2-space indentation
- **Loading**: Automatic on startup via `load_data()`
- **Saving**: Automatic after every modification via `save_data()`
- **Default Data**: If no saved data exists, uses hardcoded default categories (Models Page, Scheme It, Compare Page, XREF, RDL, Calculators)

### Output Files

- **Gantt Chart**: `~/gantt_outputs/gantt_chart_2026.png`
- **Format**: PNG image, 300 DPI, 16x10 inch figure
- **Chart Range**: January 1, 2026 - January 1, 2027 (hardcoded)

## Application Flow

### Startup Sequence

1. Script execution begins at `if __name__ == "__main__":`
2. Calls `main_menu()` which immediately calls `load_data()`
3. If `~/gantt_outputs/gantt_data.json` exists → loads it into global `categories`
4. If file doesn't exist → uses default hardcoded data
5. Displays interactive menu in infinite loop until user exits

### Menu Operations

The application provides 9 operations organized in a numbered menu:

**Category Management:**
1. **View** - Display all categories and subcategories with details
2. **Add** - Create new category (empty, no subcategories)
3. **Delete** - Remove category and all its subcategories (with confirmation)
4. **Rename** - Change category name

**Subcategory Management:**
5. **Add** - Create subcategory within a category (prompts for name, date, duration)
6. **Delete** - Remove subcategory (with confirmation)
7. **Rename** - Change subcategory name only
8. **Edit Details** - Modify start date and/or duration

**Visualization:**
9. **Generate Chart** - Create PNG Gantt chart from current data

**Exit:**
0. Exit the application

### Data Modification Pattern

All modification functions follow this pattern:
1. Display current categories (if relevant)
2. Prompt user for selection/input
3. Validate input
4. Modify global `categories` dictionary
5. Call `save_data()` to persist changes
6. Print success/error message
7. Return to main menu

### Gantt Chart Generation

The `generate_gantt_chart()` function:

1. **Checks** if categories exist (returns if empty)
2. **Creates** matplotlib figure (16x10 inches)
3. **Assigns colors** from Set3 colormap (one per category)
4. **Iterates** through categories and subcategories:
   - Calculates start/end dates from start date + duration
   - Draws horizontal bars using `ax.barh()`
   - Positions bars on Y-axis with spacing between categories
5. **Configures axes**:
   - X-axis: Monthly ticks with week gridlines
   - Y-axis: Category names (bold) and subcategory names (indented)
6. **Adds elements**: Title, legend, grid, labels
7. **Saves** as PNG to `~/gantt_outputs/gantt_chart_2026.png`
8. **Closes** figure to free memory

## Code Organization

The script is organized as a single procedural file with these sections:

1. **Imports** (lines 1-6): matplotlib, datetime, numpy, json, os
2. **Global Data** (lines 8-40): Default `categories` structure
3. **Path Configuration** (lines 42-47): Output directory setup
4. **Persistence Functions** (lines 50-71): `load_data()`, `save_data()`
5. **Display Function** (lines 73-83): `display_categories()`
6. **Category CRUD** (lines 85-151): Add, delete, rename categories
7. **Subcategory CRUD** (lines 153-326): Add, delete, rename, edit subcategories
8. **Chart Generation** (lines 328-411): `generate_gantt_chart()`
9. **Main Menu Loop** (lines 413-458): User interface and dispatch
10. **Entry Point** (lines 460-462): Script execution

## Key Design Patterns

### Global State Pattern

- Single global `categories` dictionary serves as application state
- All functions read from and modify this global variable
- Simple but requires careful management to avoid inconsistencies

### Menu-Driven CLI Pattern

- Infinite loop with numbered menu options
- User input dispatches to specific functions
- Each function returns to menu when complete

### Immediate Persistence

- Every modification triggers automatic `save_data()`
- No "save" command needed
- Changes are durable across crashes/exits

### Defensive Input Validation

- Try/except blocks catch invalid numeric input
- Empty string checks prevent blank names
- Date format validation using `datetime.strptime()`
- Range checking for list indices
- Confirmation prompts for destructive operations

## Working with Project Data

### Date Format

All dates must be in ISO format: `YYYY-MM-DD` (e.g., "2026-01-01")

### Duration

- Integer representing number of days
- Used to calculate end date: `end_date = start_date + timedelta(days=duration)`
- No end date is stored, only calculated when needed

### Timeline Constraints

The Gantt chart is **hardcoded** to display January 1, 2026 - January 1, 2027:
- `ax.set_xlim(datetime(2026, 1, 1), datetime(2027, 1, 1))` (line 371)
- Tasks outside this range may not display properly

To change the timeline:
1. Modify line 371 to use different start/end dates
2. Update title on line 387 to reflect new date range

### Color Assignment

- Colors assigned from matplotlib's Set3 colormap
- One color per category (all subcategories share category color)
- Color is determined by category order, not name
- Reordering categories changes colors

## Modifying the Application

### Adding New Menu Options

1. Add function definition for new operation
2. Add menu item in `main_menu()` (lines 421-431)
3. Add elif branch to dispatch to new function (lines 435-457)
4. Follow existing patterns: validate input, modify `categories`, call `save_data()`

### Changing Chart Appearance

Chart styling is in `generate_gantt_chart()`:
- **Colors**: Line 336 - Change colormap (e.g., `plt.cm.Paired`)
- **Figure size**: Line 339 - Modify `figsize=(width, height)`
- **Bar height**: Line 360 - Change `height=0.6` value
- **Grid style**: Line 382 - Modify alpha, linestyle, linewidth
- **Font sizes**: Lines 385-387 - Adjust fontsize parameters
- **DPI**: Line 405 - Change `dpi=300` for resolution

### Adding New Fields

To add fields to subcategories (e.g., "owner", "status"):

1. **Modify data structure** (line 10-40): Add field to default data
2. **Update `add_subcategory()`** (lines 153-196): Prompt for new field
3. **Update `edit_subcategory_details()`** (lines 275-326): Allow editing new field
4. **Update `display_categories()`** (lines 73-83): Show new field in output
5. **Optional**: Modify `generate_gantt_chart()` to visualize new field (e.g., color by status)

## File System Layout

```
Roadmap/
├── gantt_chart_interactive_1.py    # Main application script
├── README.md                        # Basic project description
└── CLAUDE.md                        # This file

~/gantt_outputs/                     # Created automatically
├── gantt_data.json                  # Persistent project data
└── gantt_chart_2026.png            # Generated Gantt chart
```

The output directory (`~/gantt_outputs/`) is created automatically on first run if it doesn't exist.

## Dependencies

- **matplotlib**: For creating Gantt chart visualizations
- **numpy**: For color palette generation
- **datetime**: Built-in (date parsing and arithmetic)
- **json**: Built-in (data serialization)
- **os**: Built-in (file path management)

Install external dependencies:
```bash
pip install matplotlib numpy
```

## Common Use Cases

### Quick Chart Generation

1. Run script
2. Press `9` (generate chart)
3. Check `~/gantt_outputs/gantt_chart_2026.png`

### Adding a New Project Phase

1. Run script
2. Press `2` (add category)
3. Enter phase name
4. Press `5` (add subcategory)
5. Select the new category
6. Enter task details
7. Press `9` to visualize

### Bulk Data Entry

Instead of interactive menu:
1. Edit `~/gantt_outputs/gantt_data.json` directly in a text editor
2. Follow the JSON structure shown above
3. Run script → press `1` to verify data loaded
4. Press `9` to generate chart

### Adjusting Timeline

Edit a task's schedule:
1. Press `8` (edit subcategory details)
2. Select category and subcategory
3. Enter new start date and/or duration
4. Press `9` to see updated chart
