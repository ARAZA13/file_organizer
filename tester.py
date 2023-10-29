import os
import csv
from datetime import datetime
from shutil import copy2
import matplotlib.pyplot as plt

# Step 1: Get the user's home directory and append "Downloads" to it
directory_path = os.path.expanduser("~") + "/Downloads"

# Step 2: Print directory_path
print("Directory path:", directory_path)

# Step 3: Create a table with columns for file name, file type, and date added
files_data = []

for filename in os.listdir(directory_path):
    file_path = os.path.join(directory_path, filename)
    if os.path.isfile(file_path):
        file_name, file_extension = os.path.splitext(filename)
        date_added = datetime.fromtimestamp(os.path.getctime(file_path))
        files_data.append((file_name, file_extension, date_added, file_path))

# Step 4: Create the "DD" directory
file_type_directory = os.path.join(directory_path, "DD")
os.makedirs(file_type_directory, exist_ok=True)

# Step 5: Create subfolders for each file type and copy files
# Create the "missing" folder
missing_directory = os.path.join(file_type_directory, "missing")
os.makedirs(missing_directory, exist_ok=True)

for file_data in files_data:
    file_name, file_extension, _, file_path = file_data

    if file_extension:
        # Create subfolder for each file type
        file_type_folder = os.path.join(file_type_directory, file_extension[1:])
        os.makedirs(file_type_folder, exist_ok=True)

        # Copy the file to the relevant subfolder
        destination_path = os.path.join(file_type_folder, file_name + file_extension)
        copy2(file_path, destination_path)
    else:
        # Copy files without a file type to the "missing" folder
        destination_path = os.path.join(missing_directory, file_name)
        copy2(file_path, destination_path)

# Step 6: Save the table as a .csv file inside the "DD" folder
csv_file_path = os.path.join(file_type_directory, "file_stats.csv")

with open(csv_file_path, mode='w', newline='') as csv_file:
    fieldnames = ["File Name", "File Type", "Date Added"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for file_data in files_data:
        writer.writerow({
            "File Name": file_data[0],
            "File Type": file_data[1],
            "Date Added": file_data[2].strftime("%Y-%m-%d %H:%M:%S")
        })

print(f"Table saved to {csv_file_path}")



# Step 7: Plot and save a bar graph
file_types = [file_data[1] if file_data[1] else "Missing" for file_data in files_data]
file_type_counts = {}
for file_type in file_types:
    if file_type in file_type_counts:
        file_type_counts[file_type] += 1
    else:
        file_type_counts[file_type] = 1

# Add the bar for files with missing file types
file_type_counts["Missing"] = file_type_counts.get("Missing", 0)

plt.bar(file_type_counts.keys(), file_type_counts.values())
plt.xlabel("File Type")
plt.ylabel("Number of Files")
plt.title("Number of Files by File Type")

# Save the bar graph in the "DD" folder
bar_graph_path = os.path.join(file_type_directory, "file_type_bar_graph.png")
plt.savefig(bar_graph_path)
plt.show()

print(f"Bar graph saved to {bar_graph_path}")
