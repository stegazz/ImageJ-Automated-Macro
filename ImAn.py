import imagej
import pandas as pd
import os
import json

print("Work in progress")
# Opening the JSON file containing configuration variables
with open('variables.json', 'r') as f:
    variables = json.load(f)

# Assigning variables from the JSON file
distance = variables['distance']
known = variables['known']
unit = variables['unit']
threshold = variables['threshold']
size = variables['size']
circularity = variables['circularity']
exclude = variables['exclude']

# Initializing ImageJ in interactive mode
ij = imagej.init(mode='interactive')

# Defining paths for folders containing images and tables
image_folder_path = os.path.abspath("folders")
tables_folder_path = os.path.abspath("tables")

# Selecting all folders in the "folders" directory
folders = [f for f in os.listdir(image_folder_path) if os.path.isdir(os.path.join(image_folder_path, f))]

# Replacing backslashes with forward slashes in the folder paths
image_folder_path = image_folder_path.replace("\\", "/")
tables_folder_path = tables_folder_path.replace("\\", "/")

# Iterating over each folder in the "folders" directory
for folder in folders:
    print(f'Processing folder: {folder}')

    # Defining the macro to be executed for each folder
    macro = fr"""run("Image Sequence...", 
    "dir=[{image_folder_path}/{folder}/] sort");
    run("Set Scale...", "distance={distance} known={known} unit={unit} global");
    run("8-bit");
    setAutoThreshold("Default ");
    //run("Threshold...");
    setThreshold({threshold[0]},{threshold[1]});
    setOption("BlackBackground", false);
    run("Convert to Mask", "method=Default background=Light ");
    run("Analyze Particles...", "size={size} circularity={circularity} display {exclude} clear in_situ stack");
    saveAs("Results", "{tables_folder_path}/{folder}.csv");
    run("Close");
    close();
    """

    # Executing the macro for the current folder
    ij.py.run_macro(macro)

    # Loading the CSV file
    df = pd.read_csv(f"{tables_folder_path}/{folder}.csv")

    # Writing an Excel file
    df.to_excel(f"{tables_folder_path}/{folder}.xlsx", index=False)

print('Tables ready')

