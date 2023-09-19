import tkinter as tk
from tkinter import ttk
import csv
from tkinter import messagebox  # Import messagebox

name_vars = {}  # Use a dictionary to store name_vars for each equipment category
grade_vars = {}  # Use a dictionary to store grade_vars for each equipment category

def combine_skills(skill_data):
    combined_skills = {}
    for skill_entry in skill_data:
        skill_name1 = skill_entry.get("Skill1", "")  # Get skill name or empty string
        skill_level1 = int(skill_entry.get("Level1", "0"))  # Get skill level or assume 0

        if skill_name1 in combined_skills:
            combined_skills[skill_name1] += skill_level1
        else:
            combined_skills[skill_name1] = skill_level1

        skill_name2 = skill_entry.get("Skill2", "")  # Get skill name or empty string
        skill_level2 = int(skill_entry.get("Level2", "0"))  # Get skill level or assume 0

        if skill_name2 in combined_skills:
            combined_skills[skill_name2] += skill_level2
        else:
            combined_skills[skill_name2] = skill_level2

    return combined_skills


def show_results():
    results_text = []
    for equipment_name in equipment_names:
        selected_name = name_vars[equipment_name].get()
        selected_grade = grade_vars[equipment_name].get()

        result_data = None
        for row in equipment_data:
            if row["Name"] == selected_name and row["Grade"] == selected_grade and row["Equipment"] == equipment_name:
                result_data = row
                break

        if result_data:
            result_text = f"Name: {result_data['Name']}\nEquipment: {result_data['Equipment']}\nGrade: {result_data['Grade']}\n"
            result_text += f"Defense: {result_data['Defense']}\n"

            skill_data = [row for row in equipment_data if row["Name"] == selected_name and row["Grade"] == selected_grade and row["Equipment"] == equipment_name]
            combined_skills = combine_skills(skill_data)

            for skill_name, skill_level in combined_skills.items():
                result_text += f"{skill_name}: Level {skill_level}\n"

            results_text.append(result_text)

    if results_text:
        results_window = tk.Toplevel(root)
        results_window.title("Equipment Information")

        result_label = ttk.Label(results_window, text="\n".join(results_text))
        result_label.pack(padx=20, pady=20)
    else:
        messagebox.showerror("Error", "No equipment selected!")

def load_data_from_csv(filename):
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        data = list(reader)
    return data

root = tk.Tk()
root.title("Monster Hunter Now Equipment Simulator")

equipment_data = load_data_from_csv("equipment.csv")
equipment_names = ["Headpiece", "Mail", "Vambraces", "Coil", "Shoes"]

equipment_frame = ttk.Frame(root)
equipment_frame.grid(row=0, column=0, padx=20, pady=20)

for i, equipment_name in enumerate(equipment_names):
    label = ttk.Label(equipment_frame, text=f"{equipment_name}:")
    label.grid(row=i, column=0, padx=10, pady=5)

    unique_names = sorted(set(row["Name"] for row in equipment_data if row["Equipment"] == equipment_name))
    name_var = tk.StringVar()
    dropdown = ttk.Combobox(equipment_frame, textvariable=name_var, values=unique_names, state="readonly")
    dropdown.grid(row=i, column=1)
    name_vars[equipment_name] = name_var  # Store the name_var in the dictionary

    grade_label = ttk.Label(equipment_frame, text="Grade:")
    grade_label.grid(row=i, column=4, padx=10, pady=5)

    grade_var = tk.StringVar()
    grade_dropdown = ttk.Combobox(equipment_frame, textvariable=grade_var, values=[
        "Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5",
        "Grade 6", "Grade 7", "Grade 8", "Grade 9", "Grade 10"
    ], state="readonly")
    grade_dropdown.grid(row=i, column=5)
    grade_vars[equipment_name] = grade_var  # Store the grade_var in the dictionary

calculate_button = ttk.Button(root, text="Show Results", command=show_results)
calculate_button.grid(row=len(equipment_names), column=0, columnspan=6, pady=10)

root.mainloop()
