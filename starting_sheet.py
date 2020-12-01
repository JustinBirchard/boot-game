#starting_sheet.py
"""Initializes the global character_sheet variable which contains
   all player data and internal notes. Also creates the temp_csheet.txt file 
   which contains a literal_eval compatible representation of character_sheet. """
#! When running boot.py, starting_sheet.py must be imported before room.py and csheet_func.py

#* character_sheet is a dictionary of dictionaries.
#* It is organized as a list of dictionaries in an attempt to make it more readable/understandble

# Below is each dictionary being assembled individually into "csheet_subX" variables:

csheet_sub0 = {'Name': '', 'Origin': '', 'Species': 'Digital', 'Bot Type': 'DLH-15'}
csheet_sub1 = {'Int': 3, 'Alt': 3, 'Itu': 3, 'Chr': 3, 'Lck': 3, 'Str': 1, 'Dex': 1}
csheet_sub2 = {'HPC': 6, 'HPT': 6, 'PC': 7, 'PT': 7, 'XP': 0, 'XPN': 500, 'LVL': 0}
csheet_sub3 = {'Inventory': {'Items': ['Map of the Whisp'], 
                             'Currency': {'Gold': 0, 'CAMs': 0}}}
csheet_sub4 = {'Internal Notes': {'Day': 1, 'Fleer Rescues': 0,
                                  'Days Worked For Orix': 0, 'Myrum Package Tracker': 0,
                                  'pc_room_password': '', 'Orix Shop': 'Closed',
                                  'Orix Hiring': 'No', 'Asked About Money': 'No',
                                  'Used MicroLodge Chest': 'No', 'Used Charging Station': 'No',
                                  'Used Hibernation Port': 'No', 'Searched Micro Lodge': 'No',
                                  'Searched Commons': 'No', 'Gleemon Holo Tran': 'No',
                                  'Myrum Step One': 'No'},
               'Active Quests': [],
               'Completed Quests': []}

# Below, the "csheet_subX" variables are combined into one list called character_sheet
# character_sheet is the heart of the game and is where each player's unique data is tracked
character_sheet = [csheet_sub0, csheet_sub1, csheet_sub2, csheet_sub3, csheet_sub4]

# temp_csheet.txt will be passed back and forth between boot_v0_9_6_0.py and p_func.py
# Creating temp_csheet.txt and writing string representation of character_sheet to file
with open('temp_csheet.txt', 'w') as starting_sheet:
    starting_sheet.write(str(character_sheet))