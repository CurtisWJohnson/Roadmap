import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import numpy as np
import json
import os

# Define the project structure
categories = {
    "Models Page": [
        {"name": "A1: Subcategory 1", "start": "2026-01-01", "duration": 60},
        {"name": "A2: Subcategory 2", "start": "2026-02-15", "duration": 90},
        {"name": "A3: Subcategory 3", "start": "2026-04-01", "duration": 120}
    ],
    "Scheme It": [
        {"name": "B1: Subcategory 1", "start": "2026-01-15", "duration": 75},
        {"name": "B2: Subcategory 2", "start": "2026-03-01", "duration": 100},
        {"name": "B3: Subcategory 3", "start": "2026-05-15", "duration": 90}
    ],
    "Compare Page": [
        {"name": "C1: Subcategory 1", "start": "2026-02-01", "duration": 80},
        {"name": "C2: Subcategory 2", "start": "2026-04-15", "duration": 85},
        {"name": "C3: Subcategory 3", "start": "2026-07-01", "duration": 120}
    ],
    "XREF": [
        {"name": "D1: Subcategory 1", "start": "2026-01-20", "duration": 95},
        {"name": "D2: Subcategory 2", "start": "2026-05-01", "duration": 110},
        {"name": "D3: Subcategory 3", "start": "2026-08-01", "duration": 90}
    ],
    "RDL": [
        {"name": "E1: Subcategory 1", "start": "2026-03-15", "duration": 70},
        {"name": "E2: Subcategory 2", "start": "2026-06-01", "duration": 95},
        {"name": "E3: Subcategory 3", "start": "2026-09-01", "duration": 100}
    ],
    "Calculators": [
        {"name": "F1: Subcategory 1", "start": "2026-02-15", "duration": 85},
        {"name": "F2: Subcategory 2", "start": "2026-05-15", "duration": 105},
        {"name": "F3: Subcategory 3", "start": "2026-10-01", "duration": 92}
    ]
}

# Use cross-platform path in user's home directory
OUTPUT_DIR = os.path.join(os.path.expanduser("~"), "gantt_outputs")
DATA_FILE = os.path.join(OUTPUT_DIR, "gantt_data.json")

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_data():
    """Load categories from JSON file if it exists"""
    global categories
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                categories = json.load(f)
            print("✓ Loaded existing project data")
        except Exception as e:
            print(f"Error loading data: {e}. Using default data.")


def save_data():
    """Save categories to JSON file"""
    try:
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, 'w') as f:
            json.dump(categories, f, indent=2)
        print("✓ Data saved successfully")
    except Exception as e:
        print(f"Error saving data: {e}")


def display_categories():
    """Display all categories and subcategories"""
    print("\n" + "="*70)
    print("CURRENT PROJECT STRUCTURE")
    print("="*70)
    for idx, (cat_name, subcats) in enumerate(categories.items(), 1):
        print(f"\n[{idx}] {cat_name}")
        for sub_idx, sub in enumerate(subcats, 1):
            print(f"    [{sub_idx}] {sub['name']} | Start: {sub['start']} | Duration: {sub['duration']} days")
    print("="*70)


def add_category():
    """Add a new category"""
    print("\n--- ADD NEW CATEGORY ---")
    cat_name = input("Enter category name: ").strip()
    if not cat_name:
        print("✗ Category name cannot be empty")
        return
    if cat_name in categories:
        print(f"✗ Category '{cat_name}' already exists")
        return
    
    categories[cat_name] = []
    print(f"✓ Category '{cat_name}' added successfully")
    save_data()


def delete_category():
    """Delete a category"""
    display_categories()
    print("\n--- DELETE CATEGORY ---")
    try:
        cat_idx = int(input("Enter category number to delete (0 to cancel): "))
        if cat_idx == 0:
            return
        
        cat_list = list(categories.keys())
        if 1 <= cat_idx <= len(cat_list):
            cat_name = cat_list[cat_idx - 1]
            confirm = input(f"Delete '{cat_name}' and all its subcategories? (y/n): ").lower()
            if confirm == 'y':
                del categories[cat_name]
                print(f"✓ Category '{cat_name}' deleted")
                save_data()
        else:
            print("✗ Invalid category number")
    except ValueError:
        print("✗ Invalid input")


def rename_category():
    """Rename a category"""
    display_categories()
    print("\n--- RENAME CATEGORY ---")
    try:
        cat_idx = int(input("Enter category number to rename (0 to cancel): "))
        if cat_idx == 0:
            return
        
        cat_list = list(categories.keys())
        if 1 <= cat_idx <= len(cat_list):
            old_name = cat_list[cat_idx - 1]
            new_name = input(f"Enter new name for '{old_name}': ").strip()
            if not new_name:
                print("✗ Name cannot be empty")
                return
            if new_name in categories and new_name != old_name:
                print(f"✗ Category '{new_name}' already exists")
                return
            
            categories[new_name] = categories.pop(old_name)
            print(f"✓ Category renamed from '{old_name}' to '{new_name}'")
            save_data()
        else:
            print("✗ Invalid category number")
    except ValueError:
        print("✗ Invalid input")


def add_subcategory():
    """Add a subcategory to a category"""
    display_categories()
    print("\n--- ADD SUBCATEGORY ---")
    try:
        cat_idx = int(input("Enter category number (0 to cancel): "))
        if cat_idx == 0:
            return
        
        cat_list = list(categories.keys())
        if 1 <= cat_idx <= len(cat_list):
            cat_name = cat_list[cat_idx - 1]
            
            sub_name = input("Enter subcategory name: ").strip()
            if not sub_name:
                print("✗ Subcategory name cannot be empty")
                return
            
            start_date = input("Enter start date (YYYY-MM-DD) [default: 2026-01-01]: ").strip()
            if not start_date:
                start_date = "2026-01-01"
            
            # Validate date format
            try:
                datetime.strptime(start_date, '%Y-%m-%d')
            except ValueError:
                print("✗ Invalid date format. Use YYYY-MM-DD")
                return
            
            duration = input("Enter duration in days [default: 60]: ").strip()
            duration = int(duration) if duration else 60
            
            categories[cat_name].append({
                "name": sub_name,
                "start": start_date,
                "duration": duration
            })
            print(f"✓ Subcategory '{sub_name}' added to '{cat_name}'")
            save_data()
        else:
            print("✗ Invalid category number")
    except ValueError:
        print("✗ Invalid input")


def delete_subcategory():
    """Delete a subcategory"""
    display_categories()
    print("\n--- DELETE SUBCATEGORY ---")
    try:
        cat_idx = int(input("Enter category number (0 to cancel): "))
        if cat_idx == 0:
            return
        
        cat_list = list(categories.keys())
        if 1 <= cat_idx <= len(cat_list):
            cat_name = cat_list[cat_idx - 1]
            subcats = categories[cat_name]
            
            if not subcats:
                print(f"✗ No subcategories in '{cat_name}'")
                return
            
            sub_idx = int(input(f"Enter subcategory number to delete (1-{len(subcats)}, 0 to cancel): "))
            if sub_idx == 0:
                return
            
            if 1 <= sub_idx <= len(subcats):
                sub_name = subcats[sub_idx - 1]['name']
                confirm = input(f"Delete '{sub_name}'? (y/n): ").lower()
                if confirm == 'y':
                    subcats.pop(sub_idx - 1)
                    print(f"✓ Subcategory '{sub_name}' deleted")
                    save_data()
            else:
                print("✗ Invalid subcategory number")
        else:
            print("✗ Invalid category number")
    except ValueError:
        print("✗ Invalid input")


def rename_subcategory():
    """Rename a subcategory"""
    display_categories()
    print("\n--- RENAME SUBCATEGORY ---")
    try:
        cat_idx = int(input("Enter category number (0 to cancel): "))
        if cat_idx == 0:
            return
        
        cat_list = list(categories.keys())
        if 1 <= cat_idx <= len(cat_list):
            cat_name = cat_list[cat_idx - 1]
            subcats = categories[cat_name]
            
            if not subcats:
                print(f"✗ No subcategories in '{cat_name}'")
                return
            
            sub_idx = int(input(f"Enter subcategory number to rename (1-{len(subcats)}, 0 to cancel): "))
            if sub_idx == 0:
                return
            
            if 1 <= sub_idx <= len(subcats):
                old_name = subcats[sub_idx - 1]['name']
                new_name = input(f"Enter new name for '{old_name}': ").strip()
                if not new_name:
                    print("✗ Name cannot be empty")
                    return
                
                subcats[sub_idx - 1]['name'] = new_name
                print(f"✓ Subcategory renamed from '{old_name}' to '{new_name}'")
                save_data()
            else:
                print("✗ Invalid subcategory number")
        else:
            print("✗ Invalid category number")
    except ValueError:
        print("✗ Invalid input")


def edit_subcategory_details():
    """Edit subcategory start date and duration"""
    display_categories()
    print("\n--- EDIT SUBCATEGORY DETAILS ---")
    try:
        cat_idx = int(input("Enter category number (0 to cancel): "))
        if cat_idx == 0:
            return
        
        cat_list = list(categories.keys())
        if 1 <= cat_idx <= len(cat_list):
            cat_name = cat_list[cat_idx - 1]
            subcats = categories[cat_name]
            
            if not subcats:
                print(f"✗ No subcategories in '{cat_name}'")
                return
            
            sub_idx = int(input(f"Enter subcategory number to edit (1-{len(subcats)}, 0 to cancel): "))
            if sub_idx == 0:
                return
            
            if 1 <= sub_idx <= len(subcats):
                sub = subcats[sub_idx - 1]
                print(f"\nCurrent details for '{sub['name']}':")
                print(f"  Start: {sub['start']}")
                print(f"  Duration: {sub['duration']} days")
                
                new_start = input(f"\nNew start date (YYYY-MM-DD) [press Enter to keep '{sub['start']}']: ").strip()
                if new_start:
                    try:
                        datetime.strptime(new_start, '%Y-%m-%d')
                        sub['start'] = new_start
                    except ValueError:
                        print("✗ Invalid date format. Keeping original date.")
                
                new_duration = input(f"New duration in days [press Enter to keep '{sub['duration']}']: ").strip()
                if new_duration:
                    try:
                        sub['duration'] = int(new_duration)
                    except ValueError:
                        print("✗ Invalid duration. Keeping original value.")
                
                print(f"✓ Subcategory '{sub['name']}' updated")
                save_data()
            else:
                print("✗ Invalid subcategory number")
        else:
            print("✗ Invalid category number")
    except ValueError:
        print("✗ Invalid input")


def generate_gantt_chart():
    """Generate and save the Gantt chart"""
    if not categories:
        print("✗ No categories to display")
        return

    try:
        # Color palette for categories
        colors = plt.cm.Set3(np.linspace(0, 1, max(len(categories), 1)))

        # Create figure and axis
        fig, ax = plt.subplots(figsize=(16, 10))

        # Y-axis position tracking
        y_pos = 0
        y_ticks = []
        y_labels = []

        # Plot each category and its subcategories
        for idx, (category, subcategories) in enumerate(categories.items()):
            # Add category label
            y_ticks.append(y_pos)
            y_labels.append(f"**{category}**")
            y_pos += 1

            # Plot subcategories
            for sub in subcategories:
                start_date = datetime.strptime(sub['start'], '%Y-%m-%d')
                end_date = start_date + timedelta(days=sub['duration'])

                # Draw the bar
                ax.barh(y_pos, (end_date - start_date).days, left=start_date,
                        height=0.6, color=colors[idx], alpha=0.8, edgecolor='black', linewidth=0.5)

                # Add task name
                y_ticks.append(y_pos)
                y_labels.append(f"  {sub['name']}")
                y_pos += 1

            # Add spacing between categories
            y_pos += 0.5

        # Configure x-axis (time)
        ax.set_xlim(datetime(2026, 1, 1), datetime(2027, 1, 1))
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        ax.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=mdates.MO))

        # Configure y-axis (tasks)
        ax.set_yticks(y_ticks)
        ax.set_yticklabels(y_labels)
        ax.invert_yaxis()

        # Add grid
        ax.grid(True, axis='x', alpha=0.3, linestyle='--', linewidth=0.5)

        # Labels and title
        ax.set_xlabel('Timeline', fontsize=12, fontweight='bold')
        ax.set_ylabel('Tasks', fontsize=12, fontweight='bold')
        ax.set_title('Gantt Chart: Project Timeline\n(January 1, 2026 - January 1, 2027)',
                     fontsize=14, fontweight='bold', pad=20)

        # Rotate x-axis labels for better readability
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

        # Add legend
        legend_elements = [plt.Rectangle((0, 0), 1, 1, fc=colors[i], alpha=0.8, edgecolor='black')
                           for i in range(len(categories))]
        ax.legend(legend_elements, categories.keys(), loc='upper left', bbox_to_anchor=(1.01, 1),
                  framealpha=0.9, title='Categories', title_fontsize=10, fontsize=9)

        # Adjust layout to prevent label cutoff
        plt.tight_layout()

        # Save the figure with cross-platform path
        output_path = os.path.join(OUTPUT_DIR, 'gantt_chart_2026.png')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"\n✓ Gantt chart saved to: {output_path}")
        plt.close()
    except Exception as e:
        print(f"✗ Error generating Gantt chart: {e}")
        plt.close()


def main_menu():
    """Display main menu and handle user input"""
    load_data()
    
    while True:
        print("\n" + "="*70)
        print("GANTT CHART MANAGER - MAIN MENU")
        print("="*70)
        print("1. View current project structure")
        print("2. Add category")
        print("3. Delete category")
        print("4. Rename category")
        print("5. Add subcategory")
        print("6. Delete subcategory")
        print("7. Rename subcategory")
        print("8. Edit subcategory details (date/duration)")
        print("9. Generate Gantt chart")
        print("0. Exit")
        print("="*70)
        
        choice = input("Enter your choice: ").strip()
        
        if choice == '1':
            display_categories()
        elif choice == '2':
            add_category()
        elif choice == '3':
            delete_category()
        elif choice == '4':
            rename_category()
        elif choice == '5':
            add_subcategory()
        elif choice == '6':
            delete_subcategory()
        elif choice == '7':
            rename_subcategory()
        elif choice == '8':
            edit_subcategory_details()
        elif choice == '9':
            generate_gantt_chart()
        elif choice == '0':
            print("\nExiting program. Goodbye!")
            break
        else:
            print("✗ Invalid choice. Please try again.")


if __name__ == "__main__":
    main_menu()
