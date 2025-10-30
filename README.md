# Roadmap - Interactive Gantt Chart Manager

A Python-based interactive CLI tool for creating and managing project roadmap timelines with professional Gantt chart visualizations.

## Features

- **Interactive Menu System** - Easy-to-use numbered menu for all operations
- **Category Management** - Organize projects into categories with multiple subcategories
- **Timeline Planning** - Define start dates and durations for each task
- **Visual Gantt Charts** - Generate high-quality PNG charts with automatic layout
- **Persistent Storage** - All changes automatically saved to JSON
- **Professional Output** - 300 DPI charts with color-coded categories and legends

## Quick Start

### Prerequisites

```bash
# Python 3.x required
python3 --version

# Install dependencies
pip install matplotlib numpy
```

### Running the Application

```bash
python3 gantt_chart_interactive_1.py
```

This launches an interactive menu where you can:
1. View your project structure
2. Add/delete/rename categories and tasks
3. Edit timelines (start dates and durations)
4. Generate Gantt chart visualizations

## Usage

### Main Menu

```
GANTT CHART MANAGER - MAIN MENU
======================================================================
1. View current project structure
2. Add category
3. Delete category
4. Rename category
5. Add subcategory
6. Delete subcategory
7. Rename subcategory
8. Edit subcategory details (date/duration)
9. Generate Gantt chart
0. Exit
======================================================================
```

### Example Workflow

**Creating a New Project:**

1. Run the script: `python3 gantt_chart_interactive_1.py`
2. Press `2` to add a new category (e.g., "Backend Development")
3. Press `5` to add subcategories/tasks:
   - Name: "API Design"
   - Start date: 2026-01-01
   - Duration: 30 days
4. Repeat for more tasks
5. Press `9` to generate the Gantt chart
6. View the chart at `~/gantt_outputs/gantt_chart_2026.png`

### Default Categories

The application comes with sample project data:
- **Models Page** - 3 subcategories
- **Scheme It** - 3 subcategories
- **Compare Page** - 3 subcategories
- **XREF** - 3 subcategories
- **RDL** - 3 subcategories
- **Calculators** - 3 subcategories

You can modify or delete these to create your own project structure.

## Data Files

### Location

All data is stored in your home directory:

```
~/gantt_outputs/
├── gantt_data.json       # Your project data (auto-saved)
└── gantt_chart_2026.png  # Generated Gantt chart
```

### Data Format

The project data is stored as JSON:

```json
{
  "Category Name": [
    {
      "name": "Task Name",
      "start": "2026-01-01",
      "duration": 60
    }
  ]
}
```

- **start**: ISO date format (YYYY-MM-DD)
- **duration**: Integer representing days

## Customization

### Changing the Timeline

By default, charts display January 1, 2026 - January 1, 2027.

To modify, edit `gantt_chart_interactive_1.py`:
- Line 371: Change `ax.set_xlim(datetime(2026, 1, 1), datetime(2027, 1, 1))`
- Line 387: Update the chart title to reflect new dates

### Adjusting Chart Appearance

**Colors:**
- Line 336: Change `plt.cm.Set3` to another colormap (e.g., `plt.cm.Paired`, `plt.cm.tab20`)

**Size:**
- Line 339: Modify `figsize=(16, 10)` for different dimensions

**Resolution:**
- Line 405: Adjust `dpi=300` for higher/lower quality

## Tips

- **Quick Updates**: Edit `~/gantt_outputs/gantt_data.json` directly for bulk changes
- **Date Format**: Always use YYYY-MM-DD format for dates
- **Auto-Save**: All changes are automatically saved - no manual save needed
- **Confirmations**: Destructive operations (delete) require confirmation
- **Timeline View**: Press `1` frequently to verify your structure

## Troubleshooting

**Missing Dependencies:**
```bash
pip install matplotlib numpy
```

**Chart Not Generating:**
- Check that you have at least one category with subcategories
- Verify dates are in correct format (YYYY-MM-DD)
- Ensure `~/gantt_outputs/` directory is writable

**Data Not Persisting:**
- Check file permissions on `~/gantt_outputs/gantt_data.json`
- Verify you're not running the script from a read-only location

## Output Example

Generated charts include:
- Color-coded bars for each category
- Timeline grid with monthly markers
- Category legend
- Task labels with spacing
- Professional formatting

## Documentation

For detailed technical documentation, see [CLAUDE.md](CLAUDE.md) which includes:
- Complete code architecture
- Data flow diagrams
- Modification guides
- API reference

## License

MIT License

## Contributing

Feel free to fork and customize for your needs!
