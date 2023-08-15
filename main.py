# Created by Dmitri Markélov

import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from collections import defaultdict
import os


def open_link(link):
    os.system(f'start "" "{link}"')


def show_about():
    about_window = tk.Toplevel(root)
    about_window.title("About")
    about_window.geometry("400x300")
    about_window.resizable(False, False)

    # Center the window on the screen.
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (400 // 2)
    y = (screen_height // 2) - (300 // 2)
    about_window.geometry(f"400x300+{x}+{y}")

    description = "This program calculates and displays future birthday dates based on a user's date of birth and the number of years they want to look ahead."

    description_label = ttk.Label(
        about_window,
        text=description,
        background=bg_color,
        anchor=tk.W,
        wraplength=380,  # Set wraplength to 380 pixels
    )
    description_label.pack(padx=10, pady=10, anchor=tk.W)

    author = "Author: Dmitri Markélov"

    link_frame = ttk.Frame(about_window)
    link_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

    ttk.Label(link_frame, text=author, background=bg_color, anchor=tk.W).pack(
        side=tk.LEFT, padx=10, anchor=tk.W
    )

    github_link = "https://github.com/di-marko"
    linkedin_link = "https://www.linkedin.com/in/dmitri-mark%C3%A9lov/"

    linkedin_label = ttk.Label(
        link_frame,
        text="LinkedIn",
        foreground="blue",
        cursor="hand2",
        background=bg_color,
    )
    linkedin_label.pack(side=tk.RIGHT, padx=(0, 10))
    linkedin_label.bind("<Button-1>", lambda e: open_link(linkedin_link))

    github_label = ttk.Label(
        link_frame,
        text="GitHub",
        foreground="blue",
        cursor="hand2",
        background=bg_color,
    )
    github_label.pack(side=tk.RIGHT, padx=(0, 10))
    github_label.bind("<Button-1>", lambda e: open_link(github_link))


def on_calculate(event=None):
    # Clear the results text widget.
    results_text.config(state=tk.NORMAL)
    results_text.delete(1.0, tk.END)

    # Get the user's inputs.
    dob_str = dob_entry.get()
    years_ahead = years_entry.get()

    # Validate the inputs.
    try:
        dob = datetime.strptime(dob_str, "%Y-%m-%d")
    except ValueError:
        results_text.insert(
            tk.END, "Invalid date format. Please enter the date in YYYY-MM-DD format.\n"
        )
        return
    try:
        years_ahead = int(years_ahead)
    except ValueError:
        results_text.insert(
            tk.END, "Invalid number of years. Please enter an integer.\n"
        )
        return

    # Show the progress in the status bar.
    progress_bar["value"] = 0
    progress_bar["maximum"] = years_ahead

    # Create a dictionary to keep track of the count for each day of the week.
    weekdays_count = defaultdict(int)
    weekdays = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    # Calculate and display the future birthday dates.
    for i in range(1, years_ahead + 1):
        future_birthday = datetime(dob.year + i, dob.month, dob.day)
        future_birthday_str = future_birthday.strftime("%Y-%m-%d %A")
        results_text.insert(tk.END, f"{future_birthday_str}\n")
        progress_bar["value"] = i
        root.update_idletasks()

        # Update the count for the day of the week.
        weekdays_count[weekdays[future_birthday.weekday()]] += 1

    # Display the "DONE!" message and scroll to the end of the results.
    results_text.insert(tk.END, "DONE!\n")
    for weekday, count in weekdays_count.items():
        results_text.insert(tk.END, f"{weekday}s: {count}\n")
    results_text.see(tk.END)

    # Make the text widget read-only.
    results_text.config(state=tk.DISABLED)


# Create the main window.
root = tk.Tk()
root.title("Future Birthday Dates")
root.geometry("400x500")

# Center the window on the screen.
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (400 // 2)
y = (screen_height // 2) - (500 // 2)
root.geometry(f"400x500+{x}+{y}")
root.resizable(width=False, height=True)

# Get the default background color of the window.
bg_color = root.cget("bg")

# Add a label and input field for the date of birth.
dob_label = ttk.Label(root, text="Date of Birth (YYYY-MM-DD):", background=bg_color)
dob_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
dob_entry = ttk.Entry(root)
dob_entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.E)

# Add a label and input field for the number of years ahead.
years_label = ttk.Label(root, text="Number of Years Ahead:", background=bg_color)
years_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
years_entry = ttk.Entry(root)
years_entry.grid(row=1, column=1, padx=10, pady=10, sticky=tk.E)
years_entry.bind("<Return>", on_calculate)

# Add a "Calculate" button.
calculate_button = ttk.Button(
    root, text="Calculate", command=on_calculate, takefocus=False
)
calculate_button.grid(row=2, column=1, padx=10, pady=10, sticky=tk.E)

# Create a style for the frame.
style = ttk.Style()
style.theme_use("default")
style.configure("TFrame", background=bg_color)

# Create a frame to hold the text widget and scrollbar.
text_frame = ttk.Frame(root)
text_frame.grid(
    row=3,
    column=0,
    columnspan=2,
    padx=(10, 0),
    sticky=tk.W + tk.E + tk.N + tk.S,
)

# Add a text widget to display the results.
results_text = tk.Text(text_frame, width=40, height=10)
results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
results_text.config(state=tk.DISABLED)  # Set the text widget to read-only mode.

# Add a scrollbar to the text widget.
scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=results_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 10))
results_text["yscrollcommand"] = scrollbar.set

# Create a style for the progress bar.
style = ttk.Style()
style.theme_use("default")
style.configure("TProgressbar", thickness=10)

# Add a progress bar.
progress_bar = ttk.Progressbar(
    root, orient=tk.HORIZONTAL, length=200, mode="determinate"
)
progress_bar.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W + tk.E)

# Configure the row and column to expand properly.
root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(0, weight=1)

# Create a menu bar with an "About" page.
menu_bar = tk.Menu(root)
menu_bar.add_command(label="About", command=show_about)
root.config(menu=menu_bar)

# Run the main event loop.
root.mainloop()
