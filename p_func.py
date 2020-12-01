#p_func.py
"""Functions used for in-game printing and interacting with player data from character_sheet.

Note: When running boot.py, temp_csheet.txt must must be updated and packaged by running 
boot.package_player_data() in boot.py BEFORE accessing any of the character_sheet related 
functions in p_func.py . Otherwise, the character_sheet functions could display an outdated 
version of character_sheet.
"""

from ast import literal_eval
from pathlib import Path
import random
import time

# Path objects that point to folders that contain related .txt files
Path_art_txt = Path('.').joinpath('text', 'art_txt') 
Path_misc_txt = Path('.').joinpath('text', 'misc_txt') 
Path_npc_txt = Path('.').joinpath('text', 'npc_txt')
Path_room_txt = Path('.').joinpath('text', 'room_txt')

#! CRITICAL STEP:
#* Importing .txt file that was exported in boot.py and using as character_sheet within p_func.py
with open(f'temp_csheet.txt', 'r') as player_data:
    character_sheet = literal_eval(player_data.read())

#*******************************************
#* Begin character_sheet printing functions:
#*******************************************
#! character sheet printing functions rely on a freshly created temp_csheet.txt file
#! The file must be freshly exported from boot.py before using any character sheet functions from p_func.py

def print_attrib ():
    """Formatted display of player attributes.
       Also creates/updates associated string variable for use in printing to file with print_final_score()"""
    global str_attribs
    
    print(f'{" " * 11}Attribute{ "Value":>8}    Bar')
    for attrib, value in character_sheet[1].items():
        print(f'{attrib:>20}{value:>8}    {"x" * value}')

    str_attribs = f'{" " * 11}Attribute{ "Value":>8}    Bar\n'
    for attrib, value in character_sheet[1].items():
        str_attribs += f'{attrib:>20}{value:>8}    {"x" * value}\n'

def print_bio ():
    """Formatted display of player Name, Origin, Species, and Bot Type
       Also creates/updates associated string variable for use in printing to file with print_final_score()"""
    global str_bio
    
    for key, value in character_sheet[0].items():
        print(f'{key:>20} {value}')
    print('')

    str_bio = ''
    for key, value in character_sheet[0].items():
        str_bio += f'{key:>20} {value}\n'
    str_bio += '\n'

def print_csheet ():
    """Formatted print out of entire character_sheet
       Also updates associated string variables for use in printing to file with print_final_score()"""
    animate_strings([f'{"=" * 75}', f'{"=" * 75}'], .005, .1)
    print_bio()
    print_hpx()
    print_attrib()
    print_inv()
    print_quests()
    print(f'{"=" * 75}')
    print(f'{"=" * 75}')
    input('\n<<<<<<---|--->>>>>>\n')

def print_final_score ():
    """Tallies, scores, and prints out final game results for player.
       Also updates associated string variables for use in printing to file with print_final_score()"""
    
    # creating variables based on character_sheet values to make code more readable:
    final_cams = character_sheet[3]["Inventory"]["Currency"]["CAMs"]
    final_gold = character_sheet[3]["Inventory"]["Currency"]["Gold"]
    fleer_rescues = character_sheet[4]['Internal Notes']['Fleer Rescues']

    # Setting descriptive string variables for final print-outs
    final_xp_desc = f'You acquired {character_sheet[2]["XP"]} out of 6200 XP ---> '
    final_quest_desc = f'You completed {len(character_sheet[4]["Completed Quests"])} out of 11 Quests ---> '    
    final_gold_desc = f'You finished with {character_sheet[3]["Inventory"]["Currency"]["Gold"]} Gold ---> '
    final_cams_desc = f'You finished with {character_sheet[3]["Inventory"]["Currency"]["CAMs"]} CAMs ---> '
    final_reboots = f'You required {fleer_rescues} reboot(s) ---> '
    
    # XP rating (5 options):
    if character_sheet[2]["XP"] <= 1100:
        xp_rating = 'Below Average'
        
    elif character_sheet[2]["XP"] > 1101 and character_sheet[2]["XP"] <= 2200:
        xp_rating = 'Average'
        
    elif character_sheet[2]["XP"] > 2201 and character_sheet[2]["XP"] <= 3700:
        xp_rating = 'Good'
        
    elif character_sheet[2]["XP"] > 3701 and character_sheet[2]["XP"] < 6200:
        xp_rating = 'Excellent'
        
    elif character_sheet[2]["XP"] == 6200:
        xp_rating = 'Perfect!'
        
    # Quest Completion rating (5 options):
    if len(character_sheet[4]["Completed Quests"]) <= 5:
        quest_rating = 'Below Average'
        
    elif len(character_sheet[4]["Completed Quests"]) == 6 or len(character_sheet[4]["Completed Quests"]) == 7:
        quest_rating = 'Average'
        
    elif len(character_sheet[4]["Completed Quests"]) == 8 or len(character_sheet[4]["Completed Quests"]) == 9:
        quest_rating = 'Good'
        
    elif len(character_sheet[4]["Completed Quests"]) == 10:
        quest_rating = 'Excellent'
        
    elif len(character_sheet[4]["Completed Quests"]) == 11:
        quest_rating = 'Perfect!'
    
    # CAMs rating (4 options):
    if final_cams <= 5:
        cams_rating = 'Below Average'

    elif final_cams >= 6 and final_cams < 11:
        cams_rating = 'Average'

    elif final_cams >= 11 and final_cams < 16:
        cams_rating = 'Good'

    elif final_cams >= 16:
        cams_rating = 'Excellent'

    # Gold rating (4 options):
    if final_gold <= 2:
        gold_rating = 'Below Average'

    elif final_gold == 3:
        gold_rating = 'Average'

    elif final_gold >= 4 and final_gold < 6:
        gold_rating = 'Good'

    elif final_gold >= 6:
        gold_rating = 'Excellent'
        
    # Fleer Rescues scoring rating (4 options):
    if fleer_rescues >= 5:
        fleer_rescues_rating = 'Below Average'

    elif fleer_rescues == 4:
        fleer_rescues_rating = 'Average'

    elif fleer_rescues == 3:
        fleer_rescues_rating = 'Good'

    elif fleer_rescues <= 2:
        fleer_rescues_rating = 'Excellent'
        
    # HostBot rating (2 options):
    if character_sheet[2]['HPT'] > 6:
        bot_upgrades_desc = f'You upgraded the hull of your HostBot ---> '
        bot_upgrades_rating = 'Good'

    else:
        bot_upgrades_desc = "You didn't upgrade the hull of your HostBot ---> "
        bot_upgrades_rating = 'Average ' #* trailing space is intentional so that it is not scored as a 1 for final_score_tally

    # Voltage Extender rating (2 options):   
    if 'Tricipian Voltage Extender' in character_sheet[3]['Inventory']['Items']:
        volt_ext_desc = 'You acquired a Tricipian Voltage Extender ---> '
        volt_ext_rating = 'Good'

    else:
        volt_ext_desc = "You didn't acquire a Tricipian Voltage Extender ---> "
        volt_ext_rating = 'Average ' #* trailing space is intentional so that it is not scored as a 1 for final_score_tally

    # Tricipian Forged Ring rating (2 options):
    if 'Tricipian Forged Ring' in character_sheet[3]['Inventory']['Items']:
        ring_desc = 'You acquired a Tricipian Forged Ring ---> '
        ring_rating = 'Good'

    else:
        ring_desc = "You didn't acquire a Tricipian Forged Ring ---> "
        ring_rating = 'Average '

    #* Creating list of all ratings for FINAL OVERALL SCORE    
    ratings = [xp_rating, quest_rating, cams_rating, gold_rating, fleer_rescues_rating, bot_upgrades_rating, volt_ext_rating]

    # tallying final score:
    final_score_tally = 0
    for rating in ratings:
        if rating == 'Average':
            final_score_tally += 1
            
        elif rating == 'Good':
            final_score_tally += 2
            
        elif rating == 'Excellent':
            final_score_tally += 3
            
        elif rating == 'Perfect!':
            final_score_tally += 4

    if final_score_tally >= 0 and final_score_tally <= 5:
        final_score_rating = 'Below Average'
        
    elif final_score_tally >= 6 and final_score_tally <= 12:
        final_score_rating = 'Average'
        
    elif final_score_tally >= 13 and final_score_tally <= 16:
        final_score_rating = 'Good'
        
    elif final_score_tally >= 17 and final_score_tally <= 19:
        final_score_rating = 'Excellent'
        
    elif final_score_tally == 20:
        final_score_rating = 'PERFECT!!!'

    # String variable containing final score statement:    
    final_score = f'On a scale of 0 to 20 your FINAL SCORE was {final_score_tally} ---> '

    # creating formatted string variable list for final csheet printout:
    bars = f'{"=" * 75}\n{"=" * 75}\n' 
    csheet_str_list = [bars, str_bio, str_hpx, str_attribs, str_inv, str_quests, bars]

    # creating formatted txt file of final score and character_sheet
    with open(f'{character_sheet[0]["Name"]} score & character sheet.txt', 'w') as final_txt:
        for line in csheet_str_list:
            final_txt.write(line)

        final_txt.write(f'\n{" ":>57} RATING\n\n')
        final_txt.write(f'{final_score:>57} {final_score_rating}\n\n')
        final_txt.write(f'{"FINAL SCORING BREAKDOWN:      ":>57}\n\n') 
        final_txt.write(f'{final_xp_desc:>57} {xp_rating}\n')
        final_txt.write(f'{final_quest_desc:>57} {quest_rating}\n') 
        final_txt.write(f'{final_reboots:>57} {fleer_rescues_rating}\n')
        final_txt.write(f'{final_gold_desc:>57} {gold_rating}\n')
        final_txt.write(f'{final_cams_desc:>57} {cams_rating}\n')
        final_txt.write(f'{bot_upgrades_desc:>57} {bot_upgrades_rating}\n')
        final_txt.write(f'{volt_ext_desc:>57} {volt_ext_rating}\n')
        final_txt.write(f'{ring_desc:>57} {ring_rating}')      
    
    # Final scoring print out (in-game):
    print(f'{" ":>57} RATING\n')  
    print(f'{final_score:>57} {final_score_rating}\n\n')   
    print(f'{"FINAL SCORING BREAKDOWN:      ":>57}\n')  
    print(f'{final_xp_desc:>57} {xp_rating}')
    print(f'{final_quest_desc:>57} {quest_rating}\n') 
    print(f'{final_reboots:>57} {fleer_rescues_rating}')
    print(f'{final_gold_desc:>57} {gold_rating}')
    print(f'{final_cams_desc:>57} {cams_rating}\n')
    print(f'{bot_upgrades_desc:>57} {bot_upgrades_rating}')
    print(f'{volt_ext_desc:>57} {volt_ext_rating}')
    print(f'{ring_desc:>57} {ring_rating}\n')
    
def print_hpx ():   
    """Formated display of Day, Reboots, player vitals, xp, and level
       Also updates associated string variables for use in printing to file with print_final_score()"""
    global str_hpx

    print(f'{"Day":>20}{character_sheet[4]["Internal Notes"]["Day"]:>8}')
    print(f'{"Reboots":>20}{character_sheet[4]["Internal Notes"]["Fleer Rescues"]:>8}\n')
    print(f'{"Level":>20}{character_sheet[2]["LVL"]:>8}')
    print(f'{"Total XP":>20}{character_sheet[2]["XP"]:>8}')
    print(f'{"XP til next":>20}{(character_sheet[2]["XPN"] - character_sheet[2]["XP"]):>8}')
    print(f'{"Completed Quests":>20}' + f'{len(character_sheet[4]["Completed Quests"]):>6}/11\n')
    print(f'{"Health":>20}{character_sheet[2]["HPC"]:>6}/{character_sheet[2]["HPT"]}    {"x" * character_sheet[2]["HPC"]}{(character_sheet[2]["HPT"] - character_sheet[2]["HPC"]) * "-"}')
    print(f'{"Battery Power":>20}{character_sheet[2]["PC"]:>6}/{character_sheet[2]["PT"]}    {"x" * character_sheet[2]["PC"]}{(character_sheet[2]["PT"] - character_sheet[2]["PC"]) * "-"}\n')
    
    str_hpx = f'{"Day":>20}{character_sheet[4]["Internal Notes"]["Day"]:>8}\n'
    str_hpx += f'{"Reboots":>20}{character_sheet[4]["Internal Notes"]["Fleer Rescues"]:>8}\n\n'
    str_hpx += f'{"Level":>20}{character_sheet[2]["LVL"]:>8}\n'
    str_hpx += f'{"Total XP":>20}{character_sheet[2]["XP"]:>8}\n'
    str_hpx += f'{"XP til next":>20}{(character_sheet[2]["XPN"] - character_sheet[2]["XP"]):>8}\n'
    str_hpx += f'{"Completed Quests":>20}' + f'{len(character_sheet[4]["Completed Quests"]):>6}/11\n\n'
    str_hpx += f'{"Health":>20}{character_sheet[2]["HPC"]:>6}/{character_sheet[2]["HPT"]}    {"x" * character_sheet[2]["HPC"]}{(character_sheet[2]["HPT"] - character_sheet[2]["HPC"]) * "-"}\n'
    str_hpx += f'{"Battery Power":>20}{character_sheet[2]["PC"]:>6}/{character_sheet[2]["PT"]}    {"x" * character_sheet[2]["PC"]}{(character_sheet[2]["PT"] - character_sheet[2]["PC"]) * "-"}\n\n'

def print_inv ():
    """Formatted display of player's currency and items 
       Also updates associated string variables for use in printing to file with print_final_score()"""
    global str_inv

    print(f'\n            CURRENCY:')
    print(f'{"Gold":>20}{character_sheet[3]["Inventory"]["Currency"]["Gold"]:>8}')
    print(f'{"CAMs":>20}{character_sheet[3]["Inventory"]["Currency"]["CAMs"]:>8}')
    print(f'\n               ITEMS:')
    for item in character_sheet[3]['Inventory']['Items']:
        print(f'{" " * 22}{item}')
        
    str_inv = f'\n            CURRENCY:\n'
    str_inv += f'{"Gold":>20}{character_sheet[3]["Inventory"]["Currency"]["Gold"]:>8}\n'
    str_inv += f'{"CAMs":>20}{character_sheet[3]["Inventory"]["Currency"]["CAMs"]:>8}\n'
    str_inv += f'\n               ITEMS:\n'
    
    for item in character_sheet[3]['Inventory']['Items']:
        str_inv += f'{" " * 22}{item}\n'

def print_quests ():
    """Formatted display of player's Active and Completed quests
       Also updates associated string variables for use in printing to file with print_final_score()"""
    global str_quests
    
    print(f'\n       ACTIVE QUESTS:')
    for active_quest in character_sheet[4]['Active Quests']:
        print(f'{" " * 22}{active_quest}')
    print(f'\n    COMPLETED QUESTS:')
    for completed_quest in character_sheet[4]['Completed Quests']:
        print(f'{" " * 22}{completed_quest}')
        
    str_quests = f'\n       ACTIVE QUESTS:'
    
    for active_quest in character_sheet[4]['Active Quests']:
        str_quests = f'{" " * 22}{active_quest}\n'
    str_quests += f'\n    COMPLETED QUESTS:\n'
    
    for completed_quest in character_sheet[4]['Completed Quests']:
        str_quests += f'{" " * 22}{completed_quest}\n'        

def print_vitals ():
    """Quick display of power and health"""
    print(f'{"Health":>20}{character_sheet[2]["HPC"]:>6}/{character_sheet[2]["HPT"]}   {"x" * character_sheet[2]["HPC"]}{(character_sheet[2]["HPT"] - character_sheet[2]["HPC"]) * "-"}')
    print(f'{"Battery Power":>20}{character_sheet[2]["PC"]:>6}/{character_sheet[2]["PT"]}   {"x" * character_sheet[2]["PC"]}{(character_sheet[2]["PT"] - character_sheet[2]["PC"]) * "-"}\n')

#*******************************************
#* End character_sheet printing functions
#*******************************************

#*******************************************
#* Begin printing animation functions:
#*******************************************
#! Printing animation functions are safe to use anytime in any module
#! They do not rely on character_sheet or temp_csheet.txt

def animate_strings(list_of_strings, scrolling_delay=.03, newline_delay=.01):
    """Animates a list of strings by using time delay

    Args:
        list_of_strings (list): A list containing strings
        scrolling_delay (float, optional): Float representing time delay between each character. Defaults to .03.
        newline_delay (float, optional): Float representing time delay for new line. Defaults to .01.
    """
    for string in list_of_strings:
        for character in string:
            time.sleep(scrolling_delay)
            print(character, end='', flush=True)
        print('')
        time.sleep(newline_delay)

def animate_txt(txtfile, path_type, scrolling_delay=.03, newline_delay=.07):
    """Print animated .txt file. Choose from one of four folders: 'npc', 'room', 'misc', or 'art'

    Args:
        txtfile (str): string representing .txt file
        path_type (str): string, must be one of following: 'npc', 'room', 'misc', or 'art'
        optional: scrolling_delay (float) representing time delay between printing of each character
        optional: newline_delay (float) representing time it takes between line breaks
    """
    if path_type not in ['npc', 'room', 'misc', 'art']:
        raise ValueError("Arg path_type must be either 'art', 'npc', 'room', 'misc'")

    elif path_type == 'art':
        path = Path_art_txt.joinpath(f'{txtfile}.txt').resolve()

    elif path_type == 'misc':
        path = Path_misc_txt.joinpath(f'{txtfile}.txt').resolve()

    elif path_type == 'npc':
        path = Path_npc_txt.joinpath(f'{txtfile}.txt').resolve()
        
    elif path_type == 'room':
        path = Path_room_txt.joinpath(f'{txtfile}.txt').resolve()

    with open(f'{path}', 'r') as txt_file_object:
        for line in txt_file_object:
            time.sleep(newline_delay)
            clean_line = line.rstrip()    
            for character in clean_line:
                time.sleep(scrolling_delay)
                print(character, end='', flush=True)
            print('')
    print('')

def detection(detection, *messages):
    """In-game alert messages in standardized format.

    Args:
        detection (str): one or two word string description of alert
        *messages (str): strings that describe details of alert
    """
    animate_strings([f'{len(detection) * "*":^72}'], scrolling_delay=.01)
    animate_strings([f'{detection:^72}'], scrolling_delay=.01)
    animate_strings(['                ****************************************                '], scrolling_delay=.005)
    for line in messages:
        animate_strings([f'{line:^72}'], scrolling_delay=.01, newline_delay=.03)

    animate_strings(['                ****************************************                \n'], scrolling_delay=.005)

def print_txt(txtfile, path_type):
    """Uses Path object to open specified .txt file and print it.

    Args:
        txtfile (str): string representation of .txt file name
        path_type (str): must be one of following: 'npc', 'room', 'misc', or 'art'
    """
    if path_type not in ['npc', 'room', 'misc', 'art']:
        raise ValueError("Arg path_type must be either 'art', 'npc', 'room', 'misc'")

    elif path_type == 'art':
        path = Path_art_txt.joinpath(f'{txtfile}.txt').resolve()

    elif path_type == 'misc':
        path = Path_misc_txt.joinpath(f'{txtfile}.txt').resolve()

    elif path_type == 'npc':
        path = Path_npc_txt.joinpath(f'{txtfile}.txt').resolve()
        
    elif path_type == 'room':
        path = Path_room_txt.joinpath(f'{txtfile}.txt').resolve()

    with open(path, 'r') as txt_file_object:
        print(txt_file_object.read())

def rand_char_gen(txt_file_name, lines_requested, scrolling_delay, newline_delay):
    """Random character generation based on characters from within specified .txt file.
       .txt file must be in root game folder or specified using Path object in boot.py

    Args:
        txt_file_name (str): name of text file
        lines_requested (int): integer representing number of total lines to generate
        scrolling_delay (float): representing time delay between printing of each character
        newline_delay (float): representing time it takes between line breaks
    """
    
    with open(f'{txt_file_name}.txt', 'r') as txt_file_name:
        character_set = txt_file_name.read()    
        current_lines = 0
        while lines_requested > current_lines:
            current_lines += 1
            for character in(random.choice(character_set) for x in range(0, random.randrange(100))):
                time.sleep(scrolling_delay)
                print(character, end='', flush=True)
            print('')
            time.sleep(newline_delay)
        print('')

def speech_str(string): 
    """Animates string by printing each character with random time delay to emulate typing/speaking.
       Note- only used in npc.py for Q&A sets"""
    
    space_counter = 0

    for character in string:

        if character == ' ':
            time.sleep(.05)
            print(character, end='', flush=True)


            space_counter += 1
            number_of_spaces = random.randrange(7, 13)

            if space_counter >= number_of_spaces:
                time.sleep(random.uniform(.12, .2))
                space_counter = 0

        elif character in ['.', '!', '?', '\n']:
            print(character, end='', flush=True)
            time.sleep(.6)

        elif character == ',':
            print(character, end='', flush=True)
            time.sleep(.35)

        else:
            print(character, end='', flush=True)
            time.sleep(random.uniform(.015, .035)) 
   
    print('\n')
    input('<<<<<<---|--->>>>>>\n')

def speech_str_list(list_of_strings):
    """List of strings to be animated to mimic speech/typing.

    Args:
        list_of_strings (list): list containing one or more strings
    """
    space_counter = 0

    for string in list_of_strings:

        for character in string:

            if character == ' ':
                time.sleep(.05)
                print(character, end='', flush=True)


                space_counter += 1
                number_of_spaces = random.randrange(7, 13)

                if space_counter >= number_of_spaces:
                    time.sleep(random.uniform(.12, .2))
                    space_counter = 0

            elif character in ['.', '!', '?', '\n']:
                print(character, end='', flush=True)
                time.sleep(.6)

            elif character == ',':
                print(character, end='', flush=True)
                time.sleep(.35)

            else:
                print(character, end='', flush=True)
                time.sleep(random.uniform(.015, .035))
        print('')

def speech_txt(txtfile, path_type):
    """Print animated .txt file. Choose from one of four folders: 'npc', 'room', 'misc', or 'art'

    Args:
        txtfile (str): string representing .txt file
        path_type (str): string, must be one of following: 'npc', 'room', 'misc', or 'art'
        optional: scrolling_delay (float) representing time delay between printing of each character
        optional: newline_delay (float) representing time it takes between line breaks
    """
    space_counter = 0

    if path_type not in ['npc', 'room', 'misc', 'art']:
        raise ValueError("Arg path_type must be either 'art', 'npc', 'room', 'misc'")

    elif path_type == 'art':
        path = Path_art_txt.joinpath(f'{txtfile}.txt').resolve()

    elif path_type == 'misc':
        path = Path_misc_txt.joinpath(f'{txtfile}.txt').resolve()

    elif path_type == 'npc':
        path = Path_npc_txt.joinpath(f'{txtfile}.txt').resolve()
        
    elif path_type == 'room':
        path = Path_room_txt.joinpath(f'{txtfile}.txt').resolve()

    with open(f'{path}', 'r') as txt_file_object:
        for line in txt_file_object:
            time.sleep(.1)
            clean_line = line.rstrip() 

            for character in clean_line:

                if character == ' ':
                    time.sleep(.05)
                    print(character, end='', flush=True)

                    space_counter += 1
                    number_of_spaces = random.randrange(7, 13)

                    if space_counter >= number_of_spaces:
                        time.sleep(random.uniform(.12, .2))
                        space_counter = 0

                elif character in ['.', '!', '?', '\n']:
                    print(character, end='', flush=True)
                    time.sleep(.6)

                elif character == ',':
                    print(character, end='', flush=True)
                    time.sleep(.35)

                else:
                    print(character, end='', flush=True)
                    time.sleep(random.uniform(.015, .035))
            print('')

        print('')

def txt_to_str(txtfile, path_type='npc'):
    """Uses Path object to open specified .txt file and conver it to a string.
       Main use is for NPC object instantiation to keep code from getting too long.

    Args:
        txtfile (str): string representation of .txt file name
        optional: path_type (str): must be one of following: 'npc', 'room', 'misc', or 'art'

    Returns:
        str: string representation of .txt file
    """
    if path_type not in ['npc', 'room', 'misc', 'art']:
        raise ValueError("Arg path_type must be either 'art', 'npc', 'room', 'misc'")

    elif path_type == 'art':
        path = Path_art_txt.joinpath(f'{txtfile}.txt').resolve()

    elif path_type == 'misc':
        path = Path_misc_txt.joinpath(f'{txtfile}.txt').resolve()

    elif path_type == 'npc':
        path = Path_npc_txt.joinpath(f'{txtfile}.txt').resolve()
        
    elif path_type == 'room':
        path = Path_room_txt.joinpath(f'{txtfile}.txt').resolve()

    with open(path, 'r') as txt_file_object:
        return str(txt_file_object.read())

#*******************************************
#* End printing animation functions
#*******************************************