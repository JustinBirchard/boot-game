# boot-game.py
# version 0.97
"""Boot is an experimental Sci-Fi text game.

   To run the game: 
   1) Download the 'boot-game' zip or clone the directory
   2) Make sure Python 3.8 or later is installed
   3) Open the 'boot-game' folder in VS Code and run the file called 'boot-game.py'

Version 0.97 was tested using Windows 10, VS Code command line terminal, and Python 3.8.5 64-bit (conda)
Built with Python Standard Library

boot-game folder contents:

                         "text" folder ---> Contains all txt files and art
                          boot-game.py ---> Main game file
                              chest.py ---> for class Chest
                                npc.py ---> for class NPC
                             p_func.py ---> for printing and character sheet related functions
                               room.py ---> for class Room
                     starting_sheet.py ---> Initializes player's character sheet

~Line index for boot-game.py (v0.97):

                                Functions: ~lines 40 to 1,450
                     Object Instantiation: ~lines 1,460 to 1,735
   Intro, Character Creation, Break Point: ~lines 1,745 to 2,170
                           Main Game Loop: ~lines 2,180 to 3,240

Functions, Objects, and While Loop conditions are in alphabetical order.

    Questions or Comments? ---> bootgamepython@gmail.com
          Additional info  ---> github.com/JustinBirchard
"""

import os.path # used in character_sheet loading sequence
import random
import time
import importlib # used to reload p_func in-line
from pathlib import Path
from ast import literal_eval # used in character loading sequence
from starting_sheet import character_sheet # imports blank character_sheet
import p_func
from room import Room
from npc import NPC
from chest import Chest

#*****************************************************************************************************************************************************************************
#*****************************************************************************************************************************************************************************
#! FUNCTIONS - In alphabetial order
#*****************************************************************************************************************************************************************************
#*****************************************************************************************************************************************************************************

def accept_quest(NPC_object=None, quest_name=None):
    """Used to accept NPC or non-NPC quests.
       Args cannot both be None, but one arg must be None.
    
       Args:
       NPC_object (NPC optional): intantiated NPC
       quest_name (str optional): string
    """
     
    if NPC_object is not None:
        p_func.detection('New Quest Available', f"""{NPC_object.name}'s "{NPC_object.available_quest}" quest is now active.""")
        character_sheet[4]['Active Quests'].append(NPC_object.available_quest)
        NPC_object.accept_quest
        package_player_data()
        input('<<<<<<---|--->>>>>>\n')

    elif quest_name is not None:
        p_func.detection('New Quest Available', f'"{quest_name}" quest is now active.')
        character_sheet[4]['Active Quests'].append(quest_name)
        package_player_data()
        input('<<<<<<---|--->>>>>>\n')

def attribute_check (player_attribute, qty_of_dice): 
    """Used for situations where player attributes should affect outcome of options/gameplay.
       The more dice are rolled, the harder the check will be for the player.
    
    Args:
        player_attribute (str): Should be one of the following: 'Int', 'Chr', 'Alt', 'Itu', 'Lck', 'Dex', or 'Str'
        qty_of_dice (int): Represents number of dice to be rolled. Must be integer value of 2, 3, or 4
    """
    global attrib_pass_fail #* created in this function and referenced globally to determine in-game outcomes
    attrib_pass_fail = ''
  
    if player_attribute == 'Chr': # assigning string to attribute variable based on player_attribute arg
        attribute = 'Charisma'

    elif player_attribute == 'Int':
        attribute = 'Intelligence'
    
    elif player_attribute == 'Itu':
        attribute = 'Intuition'
        
    elif player_attribute == 'Alt':
        attribute = 'Alertness'

    elif player_attribute == 'Lck':
        attribute = 'Luck'

    # Explaining rules of current check to the player:       
    p_func.animate_strings([f'{attribute} check!', '', f'You will roll {qty_of_dice} six-sided dice.',
                            f'The total must be less than or equal to your {attribute}.', '',
                            f'Your {attribute} value is {character_sheet[1][player_attribute]}.', ''], .03, .07)
    input('<<<<<<---|--->>>>>>\n') 
    input(f'Hit enter to roll {qty_of_dice} dice: ') #* dice rolling sequence begins
    p_func.animate_strings(['', f"{qty_of_dice * '. . . . . . '}", ''], .04, .03)

    if qty_of_dice == 2:
        die1 = random.randrange(1, 7)
        die2 = random.randrange(1, 7)
        die_total = die1 + die2
        p_func.animate_strings([f'You rolled {die1} and {die2}.', f'Your total is {die_total}.\n'], .05, .05)          
        input('<<<<<<---|--->>>>>>\n')  

    elif qty_of_dice == 3:
        die1 = random.randrange(1, 7)
        die2 = random.randrange(1, 7)
        die3 = random.randrange(1, 7)
        die_total = die1 + die2 + die3
        p_func.animate_strings([f'You rolled {die1}, {die2}, and {die3}.', f'Your total is {die_total}.\n'], .05, .05)          
        input('<<<<<<---|--->>>>>>\n')  

    elif qty_of_dice == 4:
        die1 = random.randrange(1, 7)
        die2 = random.randrange(1, 7)
        die3 = random.randrange(1, 7)
        die4 = random.randrange(1, 7)
        die_total = die1 + die2 + die3 + die4
        p_func.animate_strings([f'You rolled {die1}, {die2}, {die3}, and {die4}.', f'Your total is {die_total}.\n'], .05, .05)          
        input('<<<<<<---|--->>>>>>\n')  

    else:
        raise ValueError("Arg qty_of_dice must be 2, 3, or 4.")

    if die_total > character_sheet[1][player_attribute]: #* Pass/Fail is determined and player receives corresponding message
        attrib_pass_fail = 'Fail'
        p_func.animate_strings(['Nooooo!', 'Crap!', f'Your {attribute} failed you.', ''])
        package_player_data()
        input('<<<<<<---|--->>>>>>\n')         

    else:
        attrib_pass_fail = 'Pass'
        p_func.animate_strings(['Excellent!', 'What a break.', f'Your high level of {attribute} did you some good!', ''])
        package_player_data()
        input('<<<<<<---|--->>>>>>\n')

def battery_charge ():
    """Used to fully recharge the player's battery."""
    character_sheet[2]['PC'] += character_sheet[2]['PT'] - character_sheet[2]['PC']
    package_player_data()
    p_func.animate_strings([f'All charged up. {character_sheet[2]["PC"]} out of {character_sheet[2]["PT"]} battery power', ''])

def battery_drain (amount=1): 
    """Used to lower player's battery power. When character_sheet[2]['PC']
       reaches 3 the player will receive an alert. When it reaches 0 
       fleer_rescue() sequence will be initiated.

    Args:
        amount (int, optional): integer -- an amount to be subtracted from
                                player's battery power. Defaults to 1.
    """
    character_sheet[2]['PC'] -= amount
    package_player_data()
    if character_sheet[2]['PC'] < 1:
        p_func.animate_txt('battery_drain1', 'misc', .03, .05)
        p_func.animate_txt('going_black_art', 'art', .001, .007)
        fleer_rescue()
       
    elif character_sheet[2]['PC'] == 3:
        p_func.detection('Battery Alert', 'Urgent!', 'Recharge needed')
        p_func.print_vitals()

def complete_quest(xp=0, cams=0, gold=0, NPC_object=None, quest_name=None):
    """Used when player completes a quest. Creates custom messages for player.
       Works in tandum with quest_reward() to distribute XP, CAMs, and Gold.
       NPC methods and character_sheet are used to update data accordingly.

       Note: package_player_data() does not need to be called here because it is
       called in quest_reward().

       All args are optional with the following conditions:
       1) Either NPC_object or quest_name must be None
       2) NPC_object and quest_name cannot both be None.    

    Args:
        xp (int, optional): integer -- Amount of experience gained
        cams (int, optional): integer -- Amount of CAMs gained
        gold (int, optional): integer -- Amount of Gold gained
        NPC_object(NPC, optional): npc class object -- An instantiated NPC object
        quest_name(str, optional): string -- Name of non-NPC based quest
    """   
    if NPC_object is not None:
        for quest in NPC_object.active_quest:
            quest = quest
            p_func.detection('Alert', f"""You have completed {NPC_object.name}'s "{quest}" quest!""", 'You have received:', f'{xp} XP', f'{cams} CAMs', f'{gold} Gold')
            character_sheet[4]['Active Quests'].remove(quest)
            character_sheet[4]['Completed Quests'].append(quest)
        NPC_object.complete_quest
        quest_reward(xp, cams, gold)

    elif quest_name is not None:
        p_func.detection('Alert', f'You have completed the "{quest_name}" quest!', 'You have received:', f'{xp} XP', f'{cams} CAMs', f'{gold} Gold')
        character_sheet[4]['Active Quests'].remove(quest_name)
        character_sheet[4]['Completed Quests'].append(quest_name)
        quest_reward(xp, cams, gold)

def death():
    """Player options for after death occurs"""   

    global character_sheet
    global game_status
    global room_location

    package_player_data()
    p_func.animate_txt('loading_options', 'misc')
    restart_choice = None
    while restart_choice == None:

        try:
            restart_choice = str(input('Enter your choice: '))
            if restart_choice not in ['1', '2']:
                raise ValueError

        except ValueError:
            print('You must choose 1 or 2.')

    if restart_choice == '1':
        with open(f'{character_sheet[0]["Name"]}_original.txt', 'r') as player_data:
            character_sheet = literal_eval(player_data.read())
            game_status = 'Roaming'
            room_location = 'Digital Hospital'
            p_func.animate_strings(['Character loaded. Restart successful.', 'Welcome Back!'])  

    elif restart_choice == '2':
        p_func.animate_strings(['\nHere is a last look at your current character sheet followed by your final score for this game:\n'])
        p_func.print_csheet()
        p_func.print_final_score()
        input('<<<<<<---|--->>>>>>\n')
        p_func.animate_strings(['You will find a file in the root folder for the game called:',
                                    f""" '{character_sheet[0]["Name"]} score & character sheet.txt' """,
                                    'It is a formated version of your character sheet and score.', ''])
        input('<<<<<<---|--->>>>>>\n')
        p_func.animate_strings([f"""Your original character creation file is called '{character_sheet[0]["Name"]}_original.txt' """])
        p_func.animate_txt('goodbye_breakpoint', 'misc')
        room_location = 'Game Over'
        game_status = 'Game Over'

def fleer_healing ():
    if character_sheet[2]["HPC"] < character_sheet[2]["HPT"]:
    
        p_func.animate_strings(['Fleer says "If you are in need, I can heal you..."', ''])
        healing_choice = None
        while healing_choice == None:
            healing_choice = input('Would you like to pay 2 CAMs for 1 HP? [y or n]: ')
            
            if healing_choice == 'y':
                p_func.animate_strings(["Let's see if Fleer will charge you full price, or take pity on you...", ''])
                attribute_check('Chr', 3)

                if attrib_pass_fail == 'Pass':
                    p_func.speech_str_list(["""Fleer looks at you sympathetically "I know it's tough out there, I can eat half the cost on this one." """, ''])
                    character_sheet[3]['Inventory']['Currency']['CAMs'] -= 1
                    character_sheet[2]["HPC"] += 1
                    package_player_data()
                    p_func.speech_str_list(['', 'Fleer spends about 30 minutes repairing you.', 'Then he says,', '"Alright, you are all set."', ''])
                    p_func.print_vitals()
                    input('<<<<<<---|--->>>>>>\n')   

                elif attrib_pass_fail == 'Fail':
                    p_func.speech_str_list(['Fleer says "Sorry, but I will have to charge you full price this time."', ''])           
                    character_sheet[3]['Inventory']['Currency']['CAMs'] -= 2
                    character_sheet[2]["HPC"] += 1
                    package_player_data()
                    p_func.speech_str_list(['', 'Fleer spends about 30 minutes repairing you.', 'Then he says,', '"Alright, you are all set."', ''])
                    p_func.print_vitals()
                    input('<<<<<<---|--->>>>>>\n')                   

            elif healing_choice == 'n':
                p_func.animate_strings(['', '"Okay, come back and see me if you have any problems."', ''])
                package_player_data()

            else:
                healing_choice = None
                
    else: # condition for if player has full HP already
        p_func.animate_strings(['Fleer gives you a quick once-over and says "Good to see you have been staying out of trouble."', ''])

def fleer_rescue ():
    """If character_sheet[2]['PC'] reaches 0 as a result of power_drain(), then
       fleer_rescue() will be executed. Fleer will rescue the player, and bring them 
       back to the Digital Hospital.

       If player has less than 1 HPC then player is dead. If player has fewer than 
       2 CAMs then player is dead. Otherwise Fleer will restore power and reboot player. 
       
       Player receives chance to avoid losing 2 HP by passing attribute_check('Alt', 3),
       passing costs only 1 HP. Player also receives chance to avoid paying Fleer 2 CAMs 
       for rescue, passing costs only 1 CAMs and is based on passing attribute_check('Chr', 3).
       Finally, Fleer will offer to heal the Player at a rate of 2 CAMs for 1 HPC, player 
       can accept or decline. At the end of sequence player resumes play in the Digital Hospital.
    """      
    global game_status
    global room_location

    character_sheet[4]['Internal Notes']['Fleer Rescues'] += 1 
    character_sheet[4]['Internal Notes']['Day'] += 1 #* rescue sequence takes one game day
    function_status = 'CAM Check'    
    character_sheet[3]['Inventory']['Currency']['CAMs'] += PlayerChest.cams # Fleer takes CAMs from player chest and places in player inventory
    character_sheet[3]['Inventory']['Currency']['Gold'] += PlayerChest.gold # Fleer takes Gold from player chest and places in player inventory
    PlayerChest.cams = 0 # setting player's chest CAMs to 0
    PlayerChest.gold = 0 # setting player's chest Gold to 0

    while function_status == 'CAM Check':

        if character_sheet[3]['Inventory']['Currency']['CAMs'] < 2: #* Checking to see if player has enough CAMs, if not player is dead
            p_func.animate_strings(['Unfortunately, your power is dead and you cannot afford to pay Fleer to reboot you.'])
            death() #! player dies from lack of CAMs

        else:
            function_status = 'Alertness Check'

    while function_status == 'Alertness Check':
        attribute_check('Alt', 3) #* If player passes Alt check damage is 1 instead of 2  

        if attrib_pass_fail == 'Pass':
            character_sheet[2]["HPC"] -= 1

            if character_sheet[2]["HPC"] <= 0: #* Checking to see if player has enough HPC, if not player is dead
                function_status = 'Inactive'
                p_func.animate_strings(['Sadly, in spite of your last minute heroics, you have died.'])
                death() #! player dies from lack of HP

            else:
                p_func.animate_strings(['Your quick thinking and alertness prevented some damage...', ''])
                function_status = 'Boot Sequence & Charisma Check'

        elif attrib_pass_fail == 'Fail':
            character_sheet[2]["HPC"] -= 2

            if character_sheet[2]["HPC"] <= 0: #* Checking to see if player has enough HPC, if not player is dead
                function_status = 'Inactive'
                p_func.animate_strings(['Sadly, you have died.', ''])
                death() #! player dies from lack of HP
                
            else:
                p_func.animate_strings(["You hit the ground hard, it wasn't pretty and caused notable damage.", ''],.05, .1)
                input('<<<<<<---|--->>>>>>\n') 
                function_status = 'Boot Sequence & Charisma Check'

    while function_status == 'Boot Sequence & Charisma Check':
        p_func.rand_char_gen(Path_misc_txt.joinpath('static').resolve(), 15, .0025, .05) #* If player is still alive and has enough CAMs to afford it, the boot-up sequence begins
        p_func.detection('Alert', 'One day has passed', 'Boot sequence initiated...')
        input('<<<<<<---|--->>>>>>\n')
        p_func.rand_char_gen(Path_misc_txt.joinpath('binary').resolve(), 15, .0025, .05)
        if character_sheet[4]['Internal Notes']['Fleer Rescues'] == 1:
            p_func.speech_txt('fleer_rescue', 'npc')
            input('<<<<<<---|--->>>>>>\n')
            battery_charge()

        else:
            p_func.animate_txt('fleer_rescue_quick', 'npc')
            input('<<<<<<---|--->>>>>>\n')
            battery_charge()

        p_func.speech_str_list(['Fleer starts poking around at a touchscreen device as he says', """"Alright, let's take a look at your bill--" """, ''])
        input('<<<<<<---|--->>>>>>\n') 
        attribute_check('Chr', 3) #* if player passes Chr check reboot will cost 1 CAM instead of 2
        if attrib_pass_fail == 'Pass':
            character_sheet[3]['Inventory']['Currency']['CAMs'] -= 1
            p_func.animate_strings(['Fleer says--', """ "I know you're trying to save for a new HostBot, so I'll give you a discount. Just 1 CAMs for rescue and reboot." """, ''])
            input('<<<<<<---|--->>>>>>\n')  
            p_func.detection('Alert', 'Boot sequence complete', 'Power restored', 'Warning:', 'Damage detected',
                    f'{character_sheet[2]["HPC"]} out of {character_sheet[2]["HPT"]} health remains')
            input('<<<<<<---|--->>>>>>\n')  
            fleer_healing()
            function_status = 'Inactive'
            game_status = 'Roaming'
            room_location = 'Digital Hospital'

        elif attrib_pass_fail == 'Fail':
            character_sheet[3]['Inventory']['Currency']['CAMs'] -= 2
            p_func.animate_strings(["""Fleer says "It'll be 2 CAMs for the rescue and reboot." """, ''])
            function_status = 'Healing Option'
            input('<<<<<<---|--->>>>>>\n')  
            p_func.detection('Alert', 'Boot sequence complete', 'Power restored', 'Warning:', 'Damage detected',
                    f'{character_sheet[2]["HPC"]} out of {character_sheet[2]["HPT"]} health remains')
            input('<<<<<<---|--->>>>>>\n')  
            fleer_healing()
            function_status = 'Inactive'
            game_status = 'Roaming'
            room_location = 'Digital Hospital'

def holographic_transport ():
    global game_status
    global room_location
    
    p_func.animate_strings(['Gleemon says "Ok, I am ready when you are."', '"Just give the word and I will pull the lever..."', ''])
    input('<<<<<<---|--->>>>>>\n')
    p_func.print_txt('game_note_leaving_the_whisp', 'misc')
    input('<<<<<<---|--->>>>>>\n')
    leaving_loop = 'active'
    while leaving_loop == 'active':
        try:
            finalize_game_choice = input('Are you sure you are ready to leave the Whisp [y] or [n]: ')
            print('')

            if finalize_game_choice not in ['y', 'n']:
                raise ValueError

        except ValueError:
            print("You must enter 'y' for yes or 'n' for no.")

        else:
            if finalize_game_choice == 'n':
                p_func.animate_strings(['C o n t i n u e   O n w a r d . . .', ''])
                leaving_loop = 'complete'
                input('<<<<<<---|--->>>>>>\n')

            elif finalize_game_choice == 'y': #! GAME OVER
                package_player_data()
                save_player_data()
                p_func.animate_txt('holo_tran_goodbye_message', 'misc')
                input('<<<<<<---|--->>>>>>\n')
                p_func.animate_strings(['Here is your completed character sheet followed by your final score for this game--'])
                p_func.print_csheet()
                p_func.print_final_score()
                input('<<<<<<---|--->>>>>>\n')
                p_func.animate_strings(['You will find a file in the root folder for the game called:',
                                         f""" '{character_sheet[0]["Name"]} score & character sheet.txt' """,
                                         'It is a formated version of your character sheet and score.', ''])
                input('<<<<<<---|--->>>>>>\n')
                p_func.animate_strings([f'Your original character creation file is called {character_sheet[0]["Name"]}_original.txt'])
                p_func.animate_txt('goodbye_endofepisode', 'misc')
                leaving_loop = 'complete'
                game_status = 'Game Over'
                room_location = 'Game Over'

def key_pad (door_name, npc_name):
    """Used for keypads on doors with no associated Room object.
      
       Arg (door_name): string representing name of door. Eg- 'the Commons' or "Fleer's room"
    """

    MainHall_NoCeith.clear_decisions
    p_func.animate_strings([f"There is keypad on {door_name} door...", ''])
    input('Enter code: ')
    p_func.animate_strings(['', '. . . . . .', '', 'Hmmm...', 'Nothing happens.', ''], .05, .05)
    encounter_chance = random.randrange(1, 5)
    
    if encounter_chance == 2:
        p_func.animate_strings(['To your surpise, as you turn around you see that IG-42 is standing behind you.', ''
                               f"""Its metalic voice chimes "{character_sheet[0]['Name']}, you are not authorized to enter {door_name}." """,
                               '"Your activity has been noted. Should a crime be committed, our interaction will be used as evidence."', '',
                               'It turns its head and walks towards the Dock Shop as it says--',
                               '"It has truly been a pleasure speaking with you today."'], .05, .1)
    
    elif encounter_chance == 3:
        p_func.animate_strings(['You hear someone passing through the hall behind you...',
                                f"It's {npc_name}.", '',
                                f"Realizing you probably shouldn't be trying to get into {door_name}, you try to act cool...", '',
                                f"Thankfully {npc_name} continues walking by and doesn't take notice of you."], .05, .1)
        
    elif encounter_chance == 4:
        p_func.animate_strings([f'Suddenly {npc_name} opens the door and says--', f'"Oh hey, {character_sheet[0]["Name"]}." ', '',
                                "You're a bit startled...", '', "...But one of the perks of being a bot is that you never have to hide the look of surprise on your face.", '',
                               f"""You calmly say "Oops, I'm sorry {npc_name}, I didn't realize I was trying to open the wrong door." """, '',
                                f'{npc_name} laughs and says "No problem, it can be a bit confusing at first. See you around."'], .05, .1)

def nima_search(room, player_attribute):
    """If Nima's quest is active player is given the ability to search
       the Micro Lodge and the Commons for Nima's Adapter.

    Args:
        room (str): string representing name of Room in main game While Loop
        player_attribute (str): string representing player attribute

    Raises:
        ValueError: room arg must be either 'Micro Lodge' or 'Commons'
        ValueError: player_attribute arg must be either 'Alt or 'Lck'
    """
    
    if room not in ['Micro Lodge', 'Commons']:
        raise ValueError("room arg must be either 'Micro Lodge' or 'Commons'")
        
    elif player_attribute not in ['Alt', 'Lck']:
        raise ValueError("player_attribute arg must be either 'Alt' or 'Lck'")
        
    elif player_attribute == 'Lck':
        descriptor = 'lucky'
        
    elif player_attribute == 'Alt':
        descriptor = 'alert'                
                  
    p_func.animate_strings([f"Let's see how {descriptor} you are while searching..."])
    attribute_check(player_attribute, 3)

    if attrib_pass_fail == 'Pass' and room == 'Micro Lodge': # succesful search of Micro Lodge, player gets 1 Gold
        p_func.speech_txt('nima_search_ml_pass', 'npc')
        p_func.detection('Alert', 'You received one Gold piece')
        character_sheet[3]['Inventory']['Currency']['Gold'] += 1
        package_player_data()

    elif attrib_pass_fail == 'Fail' and room == 'Micro Lodge': # unsuccesful search of Micro Lodge
        p_func.speech_txt('nima_search_ml_fail', 'npc')         

    elif attrib_pass_fail == 'Pass' and room == 'Commons': # Successful search of Commons, player finds Nima's Adapter
        p_func.speech_txt('nima_search_c_pass', 'npc')  
        p_func.detection('Alert', "You now have Nima's Adapter in your inventory")
        character_sheet[3]['Inventory']['Items'].append("Nima's Adapter")
        package_player_data()

    elif attrib_pass_fail == 'Fail' and room == 'Commons': # Unsuccessful search of Commons
        p_func.animate_strings(['You give it your best effort, but after nearly an hour you are unable to find anything.'])

def orix_shop ():
    """Gives player opportunity to buy Tricipian Voltage Extender
    from Orix. Exists to make DockShop & Orix interactions easier."""
    p_func.speech_txt('orix_tricipian_desc', 'npc')
    orix_shop_choice = None
    while orix_shop_choice == None:
        
        try: # player chooses whether to shop or not
            orix_shop_choice = input('[y] or [n]: ')
            if orix_shop_choice not in ['y', 'n']:
                raise ValueError

        except ValueError:
            print('You must enter [y] or [n].')
            orix_shop_choice = None

    if orix_shop_choice == 'y':
        if character_sheet[3]['Inventory']['Currency']['CAMs'] < 15: # check to make sure player has enough money
            p_func.animate_strings([""" "Looks like you don't have enough CAMs right now. Come back once you've got 15." """])
            Orix.player_questions('returns to what he was doing.', 'notices a ship waiting at the dock and starts heading over to help.')

        else:
            p_func.speech_str_list(['"Great! I will install it free of charge, and top you off with power. It will just take a few moments..."', ''])
            input('<<<<<<---|--->>>>>>\n')
            character_sheet[2]["PT"] += 2 # Adding 2 onto player's Power Total
            character_sheet[3]['Inventory']['Currency']['CAMs'] -= 15 # removing CAMs from player inventory
            character_sheet[3]['Inventory']['Items'].append('Tricipian Voltage Extender') # adding item to player inventory
            character_sheet[4]['Internal Notes']['Orix Shop'] = 'Closed' # closing the shop so that it will not be available again
            battery_charge() # charging player's current battery to new full capacity
            p_func.detection('Upgrade In Progress', 'Increased voltage capacity', 'Battery charging',
                        f'{character_sheet[2]["PC"]} out of {character_sheet[2]["PT"]} battery power available',
                        '15 CAMs were removed fom inventory')
            p_func.animate_strings(['"Alright, you are all set."', '"Enjoy!"', '']) # kicks back to DockShop_E Room options
            input('<<<<<<---|--->>>>>>\n')

    elif orix_shop_choice == 'n': # kicks back to Orix.player_questions so that player has opportunity to buy later
        p_func.animate_strings(['"No problem, come back and see me later if you change your mind."'])
        Orix.player_questions('returns to what he was doing.', 'notices a ship waiting at the dock and starts heading over to help.')

def orix_work ():
    """If player has > 3 HPC they can work for Orix.
       Player can choose to work 1 day for 5 CAMs or 2 days for 1 Gold.
       If player works for CAMs they will have an Intuition check.
       Passing results in bonus of 2 extra CAMs and no damage taken.
       Failing will result in -1 health.
       If player works for Gold they will have an Intelligence check.
       Passing will result in a bonus of 2 extra CAMs and -1 health.
       Failing will result in -2 health.
    """
    
    function_status = 'Work Choice'
    p_func.speech_txt('orix_work_choice', 'npc')
    
    while function_status == 'Work Choice':
    
        try:
            player_work_choice = input('Would you like to work a shift at the Dock Shop? [y] or [n]: ')
            print('')
            if player_work_choice not in ['y', 'n']:
                raise ValueError

        except ValueError:
            print('You must enter [y] or [n].')

        if player_work_choice == 'y':
            p_func.speech_txt('orix_health_check', 'npc')
            function_status = 'Health Check'
            
        elif player_work_choice == 'n':
            p_func.animate_strings(['No worries, I will be here if you change your mind.', ''])
            function_status = 'Complete'
            Orix.player_questions('returns to what he was doing.', 'notices a ship waiting at the dock and starts heading over to help.')

    while function_status == 'Health Check':

        if character_sheet[2]['HPC'] < 3:
            p_func.speech_txt('orix_health_fail', 'npc')
            function_status = 'Complete'
            Orix.player_questions('returns to what he was doing.', 'notices a ship waiting at the dock and starts heading over to help.')
            
        else:
            p_func.speech_txt('orix_health_pass', 'npc')
            function_status = '1 or 2 days'
            
    while function_status == '1 or 2 days':

            try:
                player_work_choice = input('Would you like to work for [1] day to earn five CAMs or [2] days to earn one Gold? [1] or [2]: ')
                print('')
                if player_work_choice not in ['1', '2']:
                    raise ValueError

            except ValueError:
                print('You must enter [1] or [2].')

            if player_work_choice == '1':
                p_func.animate_strings(['You expect this to be a challenging day of work, so you take a moment to mentally prepare...', ''])
                input('<<<<<<---|--->>>>>>\n')
                attribute_check('Itu', 3)  
                
                if attrib_pass_fail == 'Pass':
                    p_func.speech_txt('orix_work_itu_pass', 'npc')
                    character_sheet[4]['Internal Notes']['Days Worked For Orix'] += 1 # Adding one day to the Orix quest internal note
                    character_sheet[4]['Internal Notes']['Day'] += 1
                    character_sheet[3]['Inventory']['Currency']['CAMs'] += 7
                    package_player_data()
                    p_func.detection('Alert', 'One day has passed', 'You received 7 CAMs for your work')
                    function_status = 'Complete'
                    
                elif attrib_pass_fail == 'Fail':                
                    p_func.speech_txt('orix_work_itu_fail', 'npc')
                    character_sheet[4]['Internal Notes']['Days Worked For Orix'] += 1 # Adding one day to the Orix quest internal note
                    character_sheet[4]['Internal Notes']['Day'] += 1
                    character_sheet[3]['Inventory']['Currency']['CAMs'] += 5
                    character_sheet[2]['HPC'] -= 1
                    package_player_data()
                    p_func.detection('Alert', 'One day has passed', 'You received minor damage while working for Orix', 'Current status:',
                                      f'{character_sheet[2]["HPC"]} out of {character_sheet[2]["HPT"]} health.',
                                       'You have received 5 CAMs for your day of work')
                    function_status = 'Complete'

            elif player_work_choice == '2':
                p_func.animate_strings(['You expect this will be a grueling couple of days, so you take a moment to mentally prepare...'])
                input('<<<<<<---|--->>>>>>\n')
                attribute_check('Int', 3)

                if attrib_pass_fail == 'Pass':
                    p_func.speech_txt('orix_work_int_pass', 'npc')
                    character_sheet[4]['Internal Notes']['Days Worked For Orix'] += 2 # Adding one day to the Orix quest internal note
                    character_sheet[4]['Internal Notes']['Day'] += 2
                    character_sheet[3]['Inventory']['Currency']['Gold'] += 1
                    character_sheet[3]['Inventory']['Currency']['CAMs'] += 2
                    character_sheet[2]['HPC'] -= 1
                    package_player_data()
                    p_func.detection('Alert', 'Two days have passed', 'You received minor damage while working for Orix', 'Current status:'
                                    f'{character_sheet[2]["HPC"]} out of {character_sheet[2]["HPT"]} health.',
                                    'You have received 1 Gold and 2 CAMS for your two days of work')
                    function_status = 'Complete'

                elif attrib_pass_fail == 'Fail':
                    p_func.speech_txt('orix_work_int_fail', 'npc')
                    character_sheet[4]['Internal Notes']['Days Worked For Orix'] += 2 # Adding one day to the Orix quest internal note
                    character_sheet[4]['Internal Notes']['Day'] += 2
                    character_sheet[3]['Inventory']['Currency']['Gold'] += 1
                    character_sheet[2]['HPC'] -= 2
                    package_player_data()
                    p_func.detection('Alert', 'Two days have passed', 'You received notable damage while working for Orix', 'Current status:',
                                    f'{character_sheet[2]["HPC"]} out of {character_sheet[2]["HPT"]} health.',
                                    'You have received 1 Gold')
                    function_status = 'Complete'

def package_player_data ():
    """Packages player data from character_sheet into temp_csheet.txt
    temp_csheet.txt can then be passed between modules while game is running.
    At conclusion of function, p_func is reloaded with updated txt file."""
    with open('temp_csheet.txt', 'w') as player_data:
        player_data.write(str(character_sheet))
    importlib.reload(p_func)

def quest_reward (amount, cams=0, gold=0):
    """Experience reward for player and check to see if player has leveled up.
       If new level reached player will get to assign three new attribute points.

    Args:
        amount (int): positive integer representing XP to give to player
        reason (str): short description of reason for XP award
    """

    character_sheet[2]['XP'] += amount
    character_sheet[3]['Inventory']['Currency']['CAMs'] += cams
    character_sheet[3]['Inventory']['Currency']['Gold'] += gold
    package_player_data()

    if character_sheet[2]['XP'] >= character_sheet[2]['XPN']: # check for level up
        character_sheet[2]["LVL"] += 1
        character_sheet[2]['XPN'] = int((character_sheet[2]['XPN'] * 2.25) // 1)
        p_func.animate_txt('level_up', 'art', .001, .007)
        p_func.animate_txt('boot_wakeup', 'art', .001, .007)
        p_func.detection('Alert', f'You now have {character_sheet[2]["XP"]} total XP',
                 f'Welcome to level {character_sheet[2]["LVL"]}!')
        input('<<<<<<---|--->>>>>>\n')
        p_func.detection('Upgrade In Progress', 'You have 3 ability points to distribute')
        input('<<<<<<---|--->>>>>>\n')
        attribute_points = 3

        while attribute_points > 0:
            package_player_data()
            p_func.animate_strings(['Which attribute would you like to improve?', '', 'Choose the corresponding number:'])
            print('1) Int\n2) Alt\n3) Itu\n4) Chr\n5) Lck\n6) View Current Attirbutes Before Deciding')

            try:
                attribute_choice = input('Enter your choice: ')
                print('')
                if attribute_choice not in ['1', '2', '3', '4', '5', '6']:
                    raise ValueError

            except ValueError:
                print('You must choose 1, 2, 3, 4, 5, or 6.')
                input('<<<<<<---|--->>>>>>\n')

            if attribute_choice == '1':
                attribute_points -= 1
                character_sheet[1]['Int'] += 1
                p_func.animate_strings(['You feel a little bit smarter! And a little better than everyone else.'])
                input('\n<<<<<<---|--->>>>>>\n')

            elif attribute_choice == '2':
                attribute_points -= 1
                character_sheet[1]['Alt'] += 1
                p_func.animate_strings(['Suddenly you feel a little more aware of everything around you.'])
                input('\n<<<<<<---|--->>>>>>\n')

            elif attribute_choice == '3':
                attribute_points -= 1
                character_sheet[1]['Itu'] += 1
                p_func.animate_strings(["You think you know what's about to happen. And you're probably right."])
                input('\n<<<<<<---|--->>>>>>\n')

            elif attribute_choice == '4':
                attribute_points -= 1
                character_sheet[1]['Chr'] += 1
                p_func.animate_strings(["You find that you are liking yourself more and more lately, seems the rest of the world finds you a bit more likable too."])
                input('\n<<<<<<---|--->>>>>>\n')

            elif attribute_choice == '5':
                attribute_points -= 1
                character_sheet[1]['Lck'] += 1
                p_func.animate_strings(["You feel a surge of luck buzzing through your wires."])
                input('\n<<<<<<---|--->>>>>>\n')

            elif attribute_choice == '6':
                p_func.animate_strings([f"{character_sheet[0]['Name']}'s current attributes:"])
                p_func.print_attrib()
                input('\n<<<<<<---|--->>>>>>\n')

        package_player_data()        
        p_func.animate_strings([f"Here are {character_sheet[0]['Name']}'s newly upgraded attributes:"])
        p_func.print_attrib()
        p_func.animate_strings(['', '. . .', ''], .2, .2) 
        p_func.animate_strings([f'{character_sheet[2]["XPN"] - character_sheet[2]["XP"]} more XP until you reach level {character_sheet[2]["LVL"] + 1}'])
        input('\n<<<<<<---|--->>>>>>\n')

    else:
        p_func.animate_strings([f'{character_sheet[2]["XPN"] - character_sheet[2]["XP"]} more XP until you reach level {character_sheet[2]["LVL"] + 1}'])
        input('\n<<<<<<---|--->>>>>>\n')

def save_original_character ():
    """Saves all original player data from character_sheet to .txt file.
    File name will be same as what player chose for their name except
    with _original as a suffix. To be used as way to reload if character dies."""
    with open(f'{character_sheet[0]["Name"]}_original.txt', 'w') as player_data:
        player_data.write(str(character_sheet))

def save_player_data ():
    """Saves all player data from character_sheet to .txt file.
    Run this at every logical save point and ALWAYS at end of game.
    File name will be same as what player chose for their name."""
    with open(f'{character_sheet[0]["Name"]}.txt', 'w') as player_data:
        player_data.write(str(character_sheet))

def slamcam():
    """A gambling game where the player can win and lose CAMs.
       If the player drains ArtupioAndCeith down to 4 or fewer CAMs then the quest is completed
    """
    
    if character_sheet[3]['Inventory']['Currency']['CAMs'] < 2: # Condition for if player doesn't have enough CAMs to play
        p_func.speech_str_list([""""Sorry bot, you don't have enough to play right now." """, 
                                """"Check back when you got more smack." """])
        
    elif ArtupioAndCeith.npc_items['CAMs'] < 4: # Condition if player tries to play after already defeating Artupio
       p_func.speech_str_list(['Artupio says, "Sorry bot, I would love to keep playing but someone cleaned me out!"'])
              
    else:
        p_func.print_txt('slam_cam_luck_check', 'misc')
        input('<<<<<<---|--->>>>>>\n') 
        attribute_check('Lck', 2) #* Luck check to see if player will receive bonuses
        character_sheet[3]['Inventory']['Currency']['CAMs'] -= 2 # player entry cost
        ArtupioAndCeith.npc_items['CAMs'] -= 4 # ArtupioAndCeith entry cost. Note that Artupio & Ceith share a pool of 16 CAMs
        prize_pot = 6 # the CAMs available to win
        player_name = character_sheet[0]['Name']
        players = [player_name, 'Artupio', 'Ceith'] # list is only used for Ceith's random choice
        player_winnings = 0 # initializing player and NPC winnings to 0
        artupio_winnings = 0
        ceith_winnings = 0
        game_status = 'Active' 
        round_status = 'First Toss'

        while game_status == 'Active': # Main game loop begins

            while round_status == 'First Toss': # Game starts here or restarts here if any players tie
                p_func.animate_strings(['Artupio says "Alright everyone, get ready for your first toss."'])
                p_func.animate_strings(['"Here we go . . . . . ."', ''], .07, .05)
                input('<<<<<<---|--->>>>>>\n')    
                
                if attrib_pass_fail == 'Pass': # if player passed Luck check player receives luck reward
                    player_score = {f'{player_name}': random.randrange((character_sheet[1]['Lck'] * 3), 101)}
                    p_func.animate_strings([f'(Your luck is giving you an unfair advantage!)', 
                                            f'(You received a bonus of {character_sheet[1]["Lck"] * 3} on your first roll.)', ''])
                
                elif attrib_pass_fail == 'Fail': # normal roll if player did not pass luck challenge       
                    player_score = {f'{player_name}': random.randrange(1, 101)} # dict created with player name key and 100 sided die roll as value                               
                
                artupio_score = {'Artupio': random.randrange(1, 101)}
                ceith_score = {'Ceith': random.randrange(1, 101)}

                first_round_scores = player_score.copy() # copying dict contents into first_round_scores
                first_round_scores.update(artupio_score) # updating first_round_scores and adding Artupio & Ceith's keys & values
                first_round_scores.update(ceith_score)            

                print(f"\n{player_name} rolled {player_score[player_name]}\n" # print out for player to see what everyone rolled
                      f"Artupio rolled {artupio_score['Artupio']}\n"
                      f"Ceith rolled {ceith_score['Ceith']}\n")            
                input('<<<<<<---|--->>>>>>\n')  

                if player_score[player_name] == artupio_score['Artupio'] or player_score[player_name] == ceith_score['Ceith'] or artupio_score['Artupio'] == ceith_score['Ceith']:
                    input('Artupio says "No ties allowed, gotta roll again...": ') # condition for if any players tied during first roll. If so, it will restart 'First Toss' loop                              

                else:
                    round_status = 'Who Will Win?'

            while round_status == 'Who Will Win?': # part of the game where players predict who they think will win
                p_func.animate_strings(['"Alright, now we make our picks on who will win"\n'])
                input('<<<<<<---|--->>>>>>\n')  
                artupio_pick = max(first_round_scores, key=first_round_scores.get) # Artupio always chooses whoever has the highest score currently
                ceith_pick = random.choice(players) # Ceith chooses at random from players list
                p_func.animate_strings([f'Artupio is picking {artupio_pick} to win.', f'Ceith thinks that {ceith_pick} will win.']) # informing player what Artupio & Ceith picked
                p_func.animate_strings(['Who do you think will win?'], .05, .1)
                print(f"1. {player_name}\n2. Artupio\n3. Ceith")
                player_pick = None
                
                while player_pick == None:

                    try: # player enters choice of who they think will win
                        player_pick = int(input('Enter your choice: '))
                        print('')
                        if player_pick not in [1, 2, 3]:
                            raise ValueError

                    except ValueError:
                        print('You must choose 1, 2, or 3.')
                        player_pick = None

                if player_pick == 1:
                      player_pick = player_name
                      round_status = 'Final Toss'

                elif player_pick == 2:
                      player_pick = 'Artupio'
                      round_status = 'Final Toss'

                elif player_pick == 3:
                      player_pick = 'Ceith'
                      round_status = 'Final Toss'

            while round_status == 'Final Toss': # Second and final toss is made
                p_func.animate_strings(['"Alright everyone, get ready for your final toss..."', ''])
                input('<<<<<<---|--->>>>>>\n')  
                
                if attrib_pass_fail == 'Pass': # if player passed Lck check player receives luck reward on 2nd toss
                    player_toss2 = random.randrange((character_sheet[1]['Lck'] * 3), 101)
                    p_func.animate_strings([f'(Your luck is giving you an unfair advantage!)', 
                                            f'(You received a bonus of {character_sheet[1]["Lck"] * 3} on your second roll.)', ''])
                
                elif attrib_pass_fail == 'Fail': # normal roll if player did not pass luck challenge       
                    player_toss2 = random.randrange(1, 101) #* note that the second toss IS NOT creating a dictionary. Just a random integer.
                    
                artupio_toss2 = random.randrange(1, 101)
                ceith_toss2 = random.randrange(1, 101)
                player_score[player_name] += player_toss2 # adding each players 2nd toss to their score dictionary
                artupio_score['Artupio'] += artupio_toss2
                ceith_score['Ceith'] += ceith_toss2

                print(f"\n{player_name} rolled {player_toss2}\n" # informing the player what each player's 2nd roll was
                      f"Artupio rolled {artupio_toss2}\n"
                      f"Ceith rolled {ceith_toss2}\n")           
                input('<<<<<<---|--->>>>>>\n')  

                final_scores = player_score.copy() # creating the final_scores dict by copying (and updating) the finalized players dictionaries
                final_scores.update(artupio_score)
                final_scores.update(ceith_score)

                if player_score[player_name] == artupio_score['Artupio'] or player_score[player_name] == ceith_score['Ceith'] or artupio_score['Artupio'] == ceith_score['Ceith']:
                    p_func.animate_strings([f"Dang, {player_name}'s final score was {final_scores[player_name]}.", # Condition for if any players tie. If so, go back to 'First Toss' loop.
                          f"Artupio's final score was {final_scores['Artupio']}.",
                          f"Ceith's final score was {final_scores['Ceith']}",
                          'Artupio says "No ties allowed, we gotta take it from the top..."'])    
                    input('<<<<<<---|--->>>>>>\n')
                    round_status = 'First Toss'

                else:
                    round_status = 'Prizes Player'

            while round_status == 'Prizes Player': # Checking to see if player wins back 1 CAMs for correctly guessing winner

                if player_pick == max(final_scores, key=final_scores.get): # looking in final_scores dict to see which key associated with max value
                    player_pick_check = 'Correct' # used for print outs and conditions later
                    player_winnings += 1 # updating the player_winnings variable
                    prize_pot -= 1 # subtracting one from the prize_pot
                    round_status = 'Prizes Artupio' # move on and do the same checks for Artupio

                elif player_pick != max(final_scores, key=final_scores.get): # Conditions for if player guessed incorrectly
                    player_pick_check = 'Incorrect' # used for print outs and conditions later
                    round_status = 'Prizes Artupio' # move on and do the same checks for Artupio

            while round_status == 'Prizes Artupio':

                if artupio_pick == max(final_scores, key=final_scores.get):
                    artupio_pick_check = 'Correct'
                    artupio_winnings += 1
                    prize_pot -= 1
                    round_status = 'Prizes Ceith'

                elif artupio_pick != max(final_scores, key=final_scores.get):
                    artupio_pick_check = 'Incorrect'
                    round_status = 'Prizes Ceith'

            while round_status == 'Prizes Ceith':

                if ceith_pick == max(final_scores, key=final_scores.get):
                    ceith_pick_check = 'Correct'
                    ceith_winnings += 1
                    prize_pot -= 1
                    round_status = 'Game & Prize Summary'             

                elif ceith_pick != max(final_scores, key=final_scores.get):
                    ceith_pick_check = 'Incorrect'
                    round_status = 'Game & Prize Summary'

            while round_status == 'Game & Prize Summary': # Final game summary and updates

                p_func.animate_strings(["""Arutpio says "Alright, let's see what we've got..." """, ''])
                input('<<<<<<---|--->>>>>>\n')  

                p_func.animate_strings([f'{max(final_scores, key=final_scores.get)} won the game with {max(final_scores.values())}!', ''], .07, .1) # Declaring winner
                input('<<<<<<---|--->>>>>>\n')
                p_func.animate_strings([f"{player_name} picked {player_pick} to win and was {player_pick_check}.", 
                                        f"{player_name}'s final score was {final_scores[player_name]}.", '',
                                        f"Artupio picked {artupio_pick} to win and was {artupio_pick_check}.", 
                                        f"Artupio's final score was {final_scores['Artupio']}.", '',
                                        f"Ceith picked {ceith_pick} to win and was {ceith_pick_check}.", 
                                        f"Ceith's final score was {final_scores['Ceith']}", ''], .05, .1)                                                      

                # Checking to see which player gets remaining contents of prize_pot:
                if final_scores[player_name] > final_scores['Artupio'] and final_scores[player_name] > final_scores['Ceith']:
                    player_winnings += prize_pot

                elif final_scores['Artupio'] > final_scores[player_name] and final_scores['Artupio'] > final_scores['Ceith']:
                    artupio_winnings += prize_pot

                elif final_scores['Ceith'] > final_scores[player_name] and final_scores['Ceith'] > final_scores['Artupio']:
                    ceith_winnings += prize_pot

                # Print out of how much each player won from the prize_pot:
                p_func.animate_strings([f'{player_name} gets {player_winnings} CAMs.', f'Artupio gets {artupio_winnings} CAMs.', f'Ceith gets {ceith_winnings} CAMs', ''], .05, .1)
                ArtupioAndCeith.npc_items['CAMs'] += artupio_winnings 
                ArtupioAndCeith.npc_items['CAMs'] += ceith_winnings // 2 #! Only adding half of Ceith's winnings back into ArtupioAndCeith to make it easier for player to defeat Artupio
                character_sheet[3]['Inventory']['Currency']['CAMs'] += player_winnings # Adding player winnings into character_sheet
                input('<<<<<<---|--->>>>>>\n')
                
                if ArtupioAndCeith.npc_items['CAMs'] < 4: #* Checking to see if Artupio has run out of CAMs. If so player complete's quest
                    p_func.speech_str_list(['Artupio exclaims--', '"Dang! You two cleaned me out!"', '"Congratulations."', '"No more for me, I am bowing out."', ''])
                    input('<<<<<<---|--->>>>>>\n')
                    complete_quest(xp=750, NPC_object=ArtupioAndCeith)
                    
                round_status = 'Complete'
                game_status = 'Inactive'

def slympto_fail_sequence ():
    """If player fails initial attribute check after encountering Slympto
       in the Charge Station, then the fail sequence begins.
       Function exists because it needs to be called in multiple places.
    """
    p_func.speech_txt('slympto_fail_intro', 'npc')
    p_func.animate_strings(["You'll have to think fast..."])
    p_func.print_txt('slympto_final_choice', 'npc')
    slympto_final_choice = None

    while slympto_final_choice == None:
        try:
            slympto_final_choice = str(input('Enter your choice: '))
            print('')
            if slympto_final_choice not in ['1', '2']:
                raise ValueError

        except ValueError:
            print('You must choose 1 or 2.')
            slympto_final_choice = None

    if slympto_final_choice == '1':
        attribute_check('Chr', 4)

        if attrib_pass_fail == 'Pass':
            p_func.speech_txt('slympto_fail_chr_pass', 'npc')
            p_func.detection('Alert', 'Threat neutralized', 'No danger detected')
            complete_quest(xp=750, NPC_object=Slympto) #* Slympto robbery quest completed FULL XP
            p_func.animate_strings(['Well that was exciting!', 'Everything seems to be fine now though...'])
            IGfortytwo.qa_set_one.append((p_func.txt_to_str('ig42_new_question'), p_func.txt_to_str('ig42_new_answer'))) #* New question added for IG-42

        elif attrib_pass_fail == 'Fail':
            p_func.speech_str_list(['Slympto laughs and says "Shut up bot! I have no need for your permission."', 
                             'He then slams you on the ground...', ''])
            character_sheet[3]['Inventory']['Currency']['Gold'] = 0
            character_sheet[3]['Inventory']['Currency']['CAMs'] = 0
            complete_quest(NPC_object=Slympto) #* Slympto robbery quest completed NO XP RECEIVED for failing all checks
            IGfortytwo.qa_set_one.append((p_func.txt_to_str('ig42_new_question'), p_func.txt_to_str('ig42_new_answer'))) #* New question added for IG-42
            battery_drain(10)

    elif slympto_final_choice == '2':
        p_func.speech_txt('slympto_give_money', 'npc')
        character_sheet[3]['Inventory']['Currency']['Gold'] = 0
        character_sheet[3]['Inventory']['Currency']['CAMs'] = 0
        p_func.animate_strings(["Welp, that was unfortunate. Let's just hope you still have some money in your chest.", ''])
        complete_quest(xp=500, NPC_object=Slympto) #* Slympto robbery quest completed ONLY 500XP for failing checks
        IGfortytwo.qa_set_one.append((p_func.txt_to_str('ig42_new_question'), p_func.txt_to_str('ig42_new_answer'))) #* New question added for IG-42

def whisp_chest(Chest_object):
    """Container interactions for player while on The Whisp.
       Note that player inventory and chest inventory are 
       only capabable of holding 10 items each.

    Args:
        Chest_object (Chest): A Chest class object
    """

    p_func.animate_strings([f"{Chest_object.name} options:\n"], .05, .03) # Presenting Chest options to the player
    print('1) View Contents\n2) Withdraw Currency\n3) Deposit Currency\n4) Place Item\n5) Retreive Item\n6) View Character Sheet\n7) Exit')

    player_choice = None
    
    while player_choice == None: 
    
        try: # Player chooses which Chest action they would like to take
            player_choice = int(input('Enter your choice: '))
            print('')
            if player_choice > 8 or player_choice < 1:
                raise ValueError
                
            elif player_choice == '':
                raise ValueError

        except ValueError:
            print('You must enter the number that corresponds with your choice.')
            player_choice = None

        else:
            if player_choice == 1: # VIEW CONTENTS
                Chest_object.view_contents()
                input('<<<<<<---|--->>>>>>\n')  
                whisp_chest(Chest_object)
                
            elif player_choice == 2: # WITHDRAW CURRENCY
                currency_choice = ''
                while currency_choice == '':
                    try: # WITHDRAW CURRENCY CHOICE
                        currency_choice = input('Would you like to withdraw [g]old or [c]ams?')
                        print('')
                        if currency_choice not in ['g', 'c']:
                            raise ValueError
                            
                    except ValueError:
                        print("You must choose 'g' for Gold or 'c' for CAMs")
                        currency_choice = ''
                        
                else:
                    
                    if currency_choice == 'g': # WITHDRAW GOLD
                        if Chest_object.gold <= 0:
                            p_func.animate_strings(['There is no Gold in this container.', ''])
                            whisp_chest(Chest_object)
                            
                        else:
                            withdraw_amount = None
                            while withdraw_amount == None:
                                
                                try: # Player chooses how much Gold to withdraw
                                    withdraw_amount = int(input('How much gold would you like to withdraw?: '))
                                    print('')
                                    if withdraw_amount < 0:
                                        print('You must enter a positive number.')
                                        raise ValueError

                                    elif withdraw_amount == '':
                                        print('You must enter a positive number.')
                                        raise ValueError                                    

                                    elif withdraw_amount > Chest_object.gold:
                                        p_func.animate_strings(['Insufficient funds.', ''], .07)
                                        raise ValueError

                                except ValueError: # Resets withdraw_amount loop
                                    withdraw_amount = None
                                    print('')
                                    
                                else:
                                    Chest_object.gold += withdraw_amount * -1 # Changing withdraw_amount to negative number to subtract desired Gold from Chest
                                    character_sheet[3]['Inventory']['Currency']['Gold'] += withdraw_amount # Adding desired Gold to player inventory
                                    p_func.animate_strings([f"You now have {character_sheet[3]['Inventory']['Currency']['Gold']} Gold in your inventory "
                                            f"and {Chest_object.gold} in this container.", ''], .05)
                                    whisp_chest(Chest_object) # Calling whisp_chest to send player back to main Chest options

                    elif currency_choice == 'c': # WITHDRAW CAMs
                        if Chest_object.cams <= 0:
                            p_func.animate_strings(['There are no CAMs in this container.', ''])
                            whisp_chest(Chest_object)

                        else:
                            withdraw_amount = None
                            while withdraw_amount == None:
                                
                                try: # Player chooses how many CAMs to withdraw
                                    withdraw_amount = int(input('How many CAMs would you like to withdraw?: '))
                                    print('')
                                    if withdraw_amount < 0:
                                        print('You must enter a positive number.')
                                        raise ValueError

                                    elif withdraw_amount == '':
                                        print('You must enter a positive number.')
                                        raise ValueError                                    

                                    elif withdraw_amount > Chest_object.cams:
                                        p_func.animate_strings(['Insufficient funds.', ''], .07)
                                        raise ValueError

                                except ValueError: # Resets withdraw_amount loop
                                    withdraw_amount = None
                                    print('')
                                    
                                else:
                                    Chest_object.cams += withdraw_amount * -1 # Changing withdraw_amount to negative number to subtract desired CAMs from Chest
                                    character_sheet[3]['Inventory']['Currency']['CAMs'] += withdraw_amount # Adding desired CAMs to player inventory
                                    p_func.animate_strings([f"You now have {character_sheet[3]['Inventory']['Currency']['CAMs']} CAMs in your inventory "
                                            f"and {Chest_object.cams} in this container.", ''], .05)
                                    whisp_chest(Chest_object) # Calling whisp_chest to send player back to main Chest options

            elif player_choice == 3: # DEPOSIT CURRENCY
                currency_choice = ''
                while currency_choice == '':
                    try: # CURRENCY DEPOSIT CHOICE
                        currency_choice = input('Would you like to deposit [g]old or [c]ams?')
                        print('')
                        if currency_choice not in ['g', 'c']:
                            raise ValueError
                            
                    except ValueError:
                        print("You must choose 'g' for Gold or 'c' for CAMs")
                        currency_choice = ''
                        
                else:
                    
                    if currency_choice == 'g': # GOLD DEPOSIT
                        if character_sheet[3]['Inventory']['Currency']['Gold'] < 1:
                            p_func.animate_strings(['You have no Gold in your inventory.', ''])
                            whisp_chest(Chest_object)
                            
                        else:
                            deposit_amount = None
                            while deposit_amount == None:
                                
                                try: # GOLD DEPOSIT AMOUNT CHOICE
                                    deposit_amount = int(input('How much gold would you like to deposit?: '))
                                    print('')
                                    if deposit_amount < 0:
                                        print('You must enter a positive number.')
                                        raise ValueError

                                    elif deposit_amount == '':
                                        print('You must enter a positive number.')
                                        raise ValueError                                    

                                    elif deposit_amount > character_sheet[3]['Inventory']['Currency']['Gold']:
                                        p_func.animate_strings(['Insufficient funds.', ''], .07)
                                        raise ValueError

                                except ValueError:
                                    deposit_amount = None
                                    print('')
                                    
                                else:
                                    Chest_object.gold += deposit_amount # Adding desired Gold into the Chest
                                    character_sheet[3]['Inventory']['Currency']['Gold'] -= deposit_amount # Removing desired Gold from inventory
                                    p_func.animate_strings([f"You now have {character_sheet[3]['Inventory']['Currency']['Gold']} Gold in your inventory "
                                            f"and {Chest_object.gold} in this container.", ''], .05)
                                    whisp_chest(Chest_object) # Recalling whisp_chest() to send player back to main Chest options

                    if currency_choice == 'c':  # CAMs Deposit
                        if character_sheet[3]['Inventory']['Currency']['CAMs'] < 1:
                            p_func.animate_strings(['You have no CAMs in your inventory.', ''])
                            whisp_chest(Chest_object)
                            
                        else:
                            deposit_amount = None
                            while deposit_amount == None:
                                
                                try: # CAM DEPOSIT AMOUNT CHOICE
                                    deposit_amount = int(input('How many CAMs would you like to deposit?: '))
                                    print('')
                                    if deposit_amount < 0:
                                        print('You must enter a positive number.')
                                        raise ValueError

                                    elif deposit_amount == '':
                                        print('You must enter a positive number.')
                                        raise ValueError                                    

                                    elif deposit_amount > character_sheet[3]['Inventory']['Currency']['CAMs']:
                                        p_func.animate_strings(['Insufficient funds.', ''], .07)
                                        raise ValueError

                                except ValueError:
                                    deposit_amount = None
                                    print('')
                                    
                                else:
                                    Chest_object.cams += deposit_amount  # Adding desired CAMs into the Chest
                                    character_sheet[3]['Inventory']['Currency']['CAMs'] -= deposit_amount  # Removing desired CAMs from player inventory
                                    p_func.animate_strings([f"You now have {character_sheet[3]['Inventory']['Currency']['CAMs']} CAMs in your inventory "
                                            f"and {Chest_object.cams} in this container.", ''], .05)
                                    whisp_chest(Chest_object) # Recalling whisp_chest() to send player back to main Chest options

            elif player_choice == 4: # PLACE ITEM IN CHEST
                if character_sheet[3]['Inventory']['Items'] == []:
                    p_func.animate_strings(['You have no items in your inventory.', ''])
                    whisp_chest(Chest_object)
                    
                else: # Presenting player with list of items in inventory that can be placed in chest                
                    p_func.animate_strings(['Which item would you like to place in the container?'])
                    print('0: Go back')
                    for index, item in zip([i for i in range(len(character_sheet[3]['Inventory']['Items']))], character_sheet[3]['Inventory']['Items']):
                        print(f'{index + 1}: {item}')

                    item_choice_loop = 'In Progress'

                    while item_choice_loop == 'In Progress':

                        try: # Player chooses which item to place in the Chest
                            player_choice = int(input('Enter your choice: '))
                            print('')
                            if player_choice == '':
                                raise ValueError

                            elif player_choice > len(character_sheet[3]['Inventory']['Items']):
                                raise ValueError

                        except ValueError:
                            print('You must choose from the options above.')

                        else:
                            item_choice_loop = 'Next Step'

                    while item_choice_loop == 'Next Step':
                        if player_choice == 0: # Gives player the option to not place anything in Chest
                            item_choice_loop = 'Complete'
                            whisp_chest(Chest_object)

                        #* BEGIN SLICING AND DICING BASED ON player_choice
                        #* Taking from player inventory and placing into the chest
                        #! Player items & chest cannot exceed 10 items each at any time or code will not work:
                        elif player_choice == 1:
                            p_func.animate_strings([f"You have moved {character_sheet[3]['Inventory']['Items'][0]} from your inventory and into the chest.", ''])
                            Chest_object.items += character_sheet[3]['Inventory']['Items'][0:1] # Adding the item to the Chest                       
                            character_sheet[3]['Inventory']['Items'][0:1] = [] # Removing the item from player's inventory
                            item_choice_loop = 'Complete'
                            whisp_chest(Chest_object)

                        elif player_choice == 2:
                            p_func.animate_strings([f"You have moved {character_sheet[3]['Inventory']['Items'][1]} from your inventory and into the chest.", ''])
                            Chest_object.items += character_sheet[3]['Inventory']['Items'][1:2]
                            character_sheet[3]['Inventory']['Items'][1:2] = []
                            item_choice_loop = 'Complete'
                            whisp_chest(Chest_object)

                        elif player_choice == 3:
                            p_func.animate_strings([f"You have moved {character_sheet[3]['Inventory']['Items'][2]} from your inventory and into the chest.", ''])
                            Chest_object.items += character_sheet[3]['Inventory']['Items'][2:3]
                            character_sheet[3]['Inventory']['Items'][2:3] = []
                            item_choice_loop = 'Complete'
                            whisp_chest(Chest_object)

                        elif player_choice == 4:
                            p_func.animate_strings([f"You have moved {character_sheet[3]['Inventory']['Items'][3]} from your inventory and into the chest.", ''])
                            Chest_object.items += character_sheet[3]['Inventory']['Items'][3:4]
                            character_sheet[3]['Inventory']['Items'][3:4] = []
                            item_choice_loop = 'Complete'
                            whisp_chest(Chest_object)

                        elif player_choice == 5:
                            p_func.animate_strings([f"You have moved {character_sheet[3]['Inventory']['Items'][4]} from your inventory and into the chest.", ''])
                            Chest_object.items += character_sheet[3]['Inventory']['Items'][4:5]
                            character_sheet[3]['Inventory']['Items'][4:5] = []
                            item_choice_loop = 'Complete'
                            whisp_chest(Chest_object)

                        elif player_choice == 6:
                            p_func.animate_strings([f"You have moved {character_sheet[3]['Inventory']['Items'][5]} from your inventory and into the chest.", ''])
                            Chest_object.items += character_sheet[3]['Inventory']['Items'][5:6]
                            character_sheet[3]['Inventory']['Items'][5:6] = []
                            item_choice_loop = 'Complete'
                            whisp_chest(Chest_object)

                        elif player_choice == 7:
                            p_func.animate_strings([f"You have moved {character_sheet[3]['Inventory']['Items'][6]} from your inventory and into the chest.", ''])
                            Chest_object.items += character_sheet[3]['Inventory']['Items'][6:7]
                            character_sheet[3]['Inventory']['Items'][4:5] = []
                            item_choice_loop = 'Complete'
                            whisp_chest(Chest_object)

                        elif player_choice == 8:
                            p_func.animate_strings([f"You have moved {character_sheet[3]['Inventory']['Items'][7]} from your inventory and into the chest.", ''])
                            Chest_object.items += character_sheet[3]['Inventory']['Items'][7:8]
                            character_sheet[3]['Inventory']['Items'][7:8] = []
                            item_choice_loop = 'Complete'
                            whisp_chest(Chest_object)

                        elif player_choice == 9:
                            p_func.animate_strings([f"You have moved {character_sheet[3]['Inventory']['Items'][8]} from your inventory and into the chest.", ''])
                            Chest_object.items += character_sheet[3]['Inventory']['Items'][8:9]
                            character_sheet[3]['Inventory']['Items'][8:9] = []
                            item_choice_loop = 'Complete'
                            whisp_chest(Chest_object)

                        elif player_choice == 10:
                            p_func.animate_strings([f"You have moved {character_sheet[3]['Inventory']['Items'][9]} from your inventory and into the chest.", ''])
                            Chest_object.items += character_sheet[3]['Inventory']['Items'][9:10]
                            character_sheet[3]['Inventory']['Items'][9:10] = []
                            item_choice_loop = 'Complete'
                            whisp_chest(Chest_object)

            elif player_choice == 5: # Remove item from Chest and place in inventory
                if Chest_object.items == []:
                    p_func.animate_strings(['There are no items in this container.', ''])
                    whisp_chest(Chest_object)
                    
                else: # presenting player with options of which items can be taken from the chest                
                    p_func.animate_strings(['Which item would you like to take from the chest?'])
                    print('0: Go back')
                    for index, item in zip([i for i in range(len(Chest_object.items))], Chest_object.items):
                        print(f'{index + 1}: {item}')

                    item_choice_loop = 'In Progress'

                    while item_choice_loop == 'In Progress':

                        try:
                            player_choice = int(input('Enter your choice: '))
                            print('')
                            if player_choice == '':
                                raise ValueError

                            elif player_choice > len(Chest_object.items):
                                raise ValueError

                        except ValueError:
                            print('You must choose from the options above.')

                        else:
                            item_choice_loop = 'Next Step'

                    while item_choice_loop == 'Next Step':
                        if player_choice == 0: # Gives player option to not take anything from Chest
                            item_choice_loop = 'Complete'
                            whisp_chest(Chest_object)

                        #* BEGIN SLICING AND DICING BASED ON player_choice
                        #* Taking from player inventory and placing into the chest
                        #! Player items & chest cannot exceed 10 items each at any time or code will not work:
                        elif player_choice == 1:
                            p_func.animate_strings([f"You have moved {Chest_object.items[0]} from the chest and into your inventory.", ''])
                            character_sheet[3]['Inventory']['Items'] += Chest_object.items[0:1] # Adding the item to the player's inventory                        
                            Chest_object.items[0:1] = [] # Removing the item from the Chest
                            item_choice_loop = 'Complete'
                            whisp_chest(Chest_object)

                        elif player_choice == 2:
                            p_func.animate_strings([f"You have moved {Chest_object.items[1]} from the chest and into your inventory.", ''])
                            character_sheet[3]['Inventory']['Items'] += Chest_object.items[1:2]                        
                            Chest_object.items[1:2] = []
                            item_choice_loop = 'Complete'
                            whisp_chest(Chest_object)

                        elif player_choice == 3:
                            p_func.animate_strings([f"You have moved {Chest_object.items[2]} from the chest and into your inventory.", ''])
                            character_sheet[3]['Inventory']['Items'] += Chest_object.items[2:3]                        
                            Chest_object.items[2:3] = []
                            item_choice_loop = 'Complete'
                            whisp_chest(Chest_object)

                        elif player_choice == 4:
                            p_func.animate_strings([f"You have moved {Chest_object.items[3]} from the chest and into your inventory.", ''])
                            character_sheet[3]['Inventory']['Items'] += Chest_object.items[3:4]                        
                            Chest_object.items[3:4] = []
                            item_choice_loop = 'Complete'
                            whisp_chest(Chest_object)

                        elif player_choice == 5:
                            p_func.animate_strings([f"You have moved {Chest_object.items[4]} from the chest and into your inventory.", ''])
                            character_sheet[3]['Inventory']['Items'] += Chest_object.items[4:5]                        
                            Chest_object.items[4:5] = []
                            item_choice_loop = 'Complete'
                            whisp_chest(Chest_object)

                        elif player_choice == 6:
                            p_func.animate_strings([f"You have moved {Chest_object.items[5]} from the chest and into your inventory.", ''])
                            character_sheet[3]['Inventory']['Items'] += Chest_object.items[5:6]                        
                            Chest_object.items[5:6] = []
                            item_choice_loop = 'Complete'
                            whisp_chest(Chest_object)

                        elif player_choice == 7:
                            p_func.animate_strings([f"You have moved {Chest_object.items[6]} from the chest and into your inventory.", ''])
                            character_sheet[3]['Inventory']['Items'] += Chest_object.items[6:7]                        
                            Chest_object.items[6:7] = []
                            item_choice_loop = 'Complete'
                            whisp_chest(Chest_object)

                        elif player_choice == 8:
                            p_func.animate_strings([f"You have moved {Chest_object.items[7]} from the chest and into your inventory.", ''])
                            character_sheet[3]['Inventory']['Items'] += Chest_object.items[7:8]                        
                            Chest_object.items[7:8] = []
                            item_choice_loop = 'Complete'
                            whisp_chest(Chest_object)

                        elif player_choice == 9:
                            p_func.animate_strings([f"You have moved {Chest_object.items[8]} from the chest and into your inventory.", ''])
                            character_sheet[3]['Inventory']['Items'] += Chest_object.items[8:9]                        
                            Chest_object.items[8:9] = []
                            item_choice_loop = 'Complete'
                            whisp_chest(Chest_object)

                        elif player_choice == 10:
                            p_func.animate_strings([f"You have moved {Chest_object.items[9]} from the chest and into your inventory.", ''])
                            character_sheet[3]['Inventory']['Items'] += Chest_object.items[9:10]                        
                            Chest_object.items[9:10] = []
                            item_choice_loop = 'Complete'
                            whisp_chest(Chest_object)

            elif player_choice == 6: # Formatted print out of character_sheet
                package_player_data() # Must always package_player_data before calling p_func
                p_func.print_csheet()
                whisp_chest(Chest_object)

            elif player_choice == 7: # EXIT BACK TO ROOM OPTIONS
                package_player_data() # Good practice to package_player_data before leaving just in case

#*****************************************************************************************************************************************************************************
#*****************************************************************************************************************************************************************************
#! OBJECT INSTANTIATION - Grouped by Type - In alphabetical order
#*****************************************************************************************************************************************************************************
#*****************************************************************************************************************************************************************************

#*==========================================================
#! Chest objects - representing containers & chests
#*==========================================================

PlayerChest = Chest('', [], 5, 0) #* chest name will be set to PC's name when PC enters MicroLodge

DockShopChest = Chest('Dock Shop Shipping Chest', [], 0, 0)

RecOfficeChest = Chest('Whisp Community Mail Delivery Container', ["Fleer's Package"], 0, 0)

MyrumJar = Chest("Myrum's Jar", ["Myrum's Order Form"], 0, 10)

#*==========================================================
#! NPC objects - representing NPC characters
#*==========================================================

Artupio = NPC(
    name='Artupio',
    quick_desc=['Artupio is a shiny, medium sized robot.', 'Seems to be missing one of its arms.'],
    qa_set_one=[('What happened to your arm?', p_func.txt_to_str("artupio_arm_answer")), 
                ('Have you always been a bot?', p_func.txt_to_str("artupio_bot_answer")),
                ('Is there anything fun to do around here?', p_func.txt_to_str("artupio_fun_answer"))])

ArtupioAndCeith = NPC(
    name='Artupio & Ceith',
    quick_desc=['Artupio is a shiny medium sized robot. Ceith is small and scrappy with a bit of rust on his frame.', 
                "They seem happy to see you. Maybe a little too happy..."],
    qa_set_one=[('Why are you two looking at me like that?', p_func.txt_to_str("artupioandceith_answer_one"))],                
    qa_set_two=[('What are the rules of the game?', p_func.txt_to_str("artupioandceith_slam_cam_rules"))],
    avlbl_quest='Win all the CAMs',
    npc_items={'CAMs': 12, 'Gold': 0})

Ceith = NPC(
    name='Ceith',
    quick_desc=["Ceith is just a few inches taller than you and clearly a bit dinged up.", "Hard to decide if he is friendly or not."],
    qa_set_one=[('If I agree to help you, what do I get out of it?', """ "Well for one thing, you'll have a new friend."\n"Also, I'll give you seven CAMs." """)],
    avlbl_quest='Power for CAMs',
    npc_items={'CAMs': 7, 'Gold': 0})

Fleer = NPC(
    name='Fleer',
    quick_desc=['Fleer is tall with light green skin and lilac colored hair.', 'He looks friendly.'],
    qa_set_one=[('What will cause my battery to drain?', '"The most common drain on your battery will be moving from room to room"'), 
                ('How can I make some money?', p_func.txt_to_str("fleer_quest_desc")), 
                ('When will you boot the other BrainChip that Myrum found?', p_func.txt_to_str("fleer_brainchip_boot")), 
                ('What should I do if I get injured?', '"You can come see me anytime and I will heal you."\n"It costs 2 CAMs for 1 HP of healing."')],
    qa_set_two=[("How long can I stay on the Whisp? And what should my objectives be while I'm here?", p_func.txt_to_str("fleer_objectives"))],
    avlbl_quest='Get Package',
    npc_items={'CAMs': 10, 'Gold': 0})

Gleemon = NPC(
    name='Gleemon',
    quick_desc=['Gleemon is slender with vine-like limbs and flourecent green skin.', 'Her hair is a shimery metalic green color.'],
    qa_set_one=[('How should I prepare for transport?', p_func.txt_to_str("gleemon_how_to_prepare")),
                ("I'd like to know more about the Merchant Market and Holographic Transportation.", p_func.txt_to_str("gleemon_holo_explanation"))],
    qa_set_two=[("What do you think I should buy while I'm there?", p_func.txt_to_str("gleemon_advice_on_purchases"))],
    qa_set_three=[("Any other advice you have for me out there?", p_func.txt_to_str("gleemon_final_advice")),
                  ("I am ready to leave. Please send me to the Tricipian Merchant Market.", '"Great, ok let me get the machine dialed in here..."')],
    avlbl_quest='',
    npc_items={'CAMs': 0, 'Gold': 3})

IGfortytwo = NPC(
    name='IG-42',
    quick_desc=['IG-42 is tall and sturdy, its eye-sensors beam intense rays of amber light.', 'It has an impressive system of hydrolics and joints allowing for a wide range of movements.'],
    qa_set_one=[('Where are you from?', '"I am from the North Tricipian Manufacturing Facility."'),
                ('What do you do here on the Whisp?', '"I am a security droid."\n"I patrol the ship and enforce the laws of the Consortium of Agreeable Merchants."')],
    qa_set_two=[('Were you ever a biological creature?', p_func.txt_to_str("ig42_differences"))],
    qa_set_three=[('What do you think about not having choices?', p_func.txt_to_str("ig42_no_free_will"))])

Myrum = NPC(
    name='Myrum',
    quick_desc=['Myrum has electric blue skin and is not much taller than you.', 'She has a thin but muscular frame, and of her hands appears to have two thumbs.'],
    qa_set_one=[('What do you do here?', p_func.txt_to_str("myrum_job_desc")),
                ("How long have you been living on the Whisp?", """"I'm part of the original crew, and this is our seventh year." """)],
    qa_set_two=[("Why did you go out of your way to rescue my BrainChip?", p_func.txt_to_str("myrum_brainchip")), 
                ("Is there something I can do to show my gratitude?", p_func.txt_to_str("myrum_quest_desc"))],
    avlbl_quest="Return the Favor")

Nima = NPC(
    name='Nima',
    quick_desc=['Nima also has the DLH-15, so she looks nearly identical to you.', "She's a bit shinier though since she's fresh out of the box."],
    qa_set_one=[("Hey there, welcome to the Micro Lodge.", '"Thank you, I feel lucky to have been booted into such a friendly environment."'), 
                ("What are you looking for?", """"This is embarrassing, but I've already lost my hibernation adapter." """)],
    qa_set_two=[("I'll help you find the adapter, where should I look?", '"I most likely dropped it in the Micro Lodge or the Commons."\n"Please let me know if you find it."')],
    avlbl_quest='Find Adapter')

Orix = NPC(
    name='Orix',
    quick_desc=['Even hidden under his bronze-colored fur, you can see that Orix is quite muscular.', 
                "He's over six feet tall with silver dreadlocks coming from his head.\nHere's hoping he's a gentle giant."],
    qa_set_one=[('Do you work here?', p_func.txt_to_str("orix_question1"))],
    qa_set_two=[("What kind of work do you need done? Why can't I do it?", p_func.txt_to_str("orix_work_desc")),
                ("What do you have for sale?", p_func.txt_to_str("orix_open_shop"))],
    avlbl_quest='Five Days of Work',
    npc_items={'CAMs': 20, 'Gold': 10})

Slympto = NPC(
    name='Slympto',
    quick_desc=['Much to your surprise, Slympto is a human!', 'He has an ill-advised brown mustache and look of discontent on his face.'],
    qa_set_one=[("You're the first human I've seen here! Where are you from?", p_func.txt_to_str("slympto_commons"))],
    qa_set_two=[],
    avlbl_quest='Survive')

SlymptoCreepy = NPC(
    name='Slympto',
    quick_desc=["You don't like the look of him...", "or his mustache."],
    qa_set_one=[("Oh, uh sorry. I didn't know anyone was here.", "Slympto glares at you from behind the counter, clearly irritated by your presence."),
                ("Don't mind me, I'll be out of your way in a minute", "Slympto ignores you. He bends down and picks up a package from behind the counter.")])

#*==========================================================
#! Path objects - for folders containing .txt files:
#*==========================================================

Path_art_txt = Path('.').joinpath('text', 'art_txt') 
Path_misc_txt = Path('.').joinpath('text', 'misc_txt') 
Path_npc_txt = Path('.').joinpath('text', 'npc_txt') 
Path_room_txt = Path('.').joinpath('text', 'room_txt') 

#*==========================================================
#! Room objects - representing rooms in the game
#*==========================================================

ChargeStation = Room(
    quick_desc=['the Charge Station', p_func.txt_to_str('charge_station_quick', 'room')],
    choices=['Use Object'],
    description_txt=str(Path_room_txt.joinpath('charge_station.txt').resolve()), 
    doors=['the Commons'],
    objects=['Micro-Bot charging adaptor'])

ChargeStation_F = Room(
    quick_desc=['the Charge Station', p_func.txt_to_str('charge_station_quick', 'room')],
    choices=['Use Object'],
    description_txt=str(Path_room_txt.joinpath('charge_station.txt').resolve()), 
    doors=['the Commons'],
    objects=['Micro-Bot charging adaptor'])

Commons = Room(
    quick_desc=['the Commons', p_func.txt_to_str('commons_quick', 'room')],
    choices=['Talk to NPC'],
    description_txt=str(Path_room_txt.joinpath('commons.txt').resolve()), 
    doors=['the Robo Lodge', 'the Digital Hospital', 'the Micro Lodge', 'the Charge Station', 'the Bio Hospital', 'the Bio Lodge', 'the Main Hall'],
    npcs=['Myrum', 'Artupio', 'Slympto'])

Commons_GameRoom = Room(
    quick_desc=['the Commons', p_func.txt_to_str('commons_quick', 'room')],
    choices=['Talk to NPC'],
    description_txt=str(Path_room_txt.joinpath('commons_game_room.txt').resolve()), 
    doors=['the Robo Lodge', 'the Digital Hospital', 'the Micro Lodge', 'the Charge Station', 'the Bio Hospital', 'the Bio Lodge', 'the Main Hall'],
    npcs=['Myrum', 'Artupio & Ceith'])

DigitalHospital = Room(
    quick_desc=['the Digital Hospital', p_func.txt_to_str('digital_hospital_quick', 'room')],
    choices=['Talk to NPC'], # Unique options 'Talk to NPC' and/or 'Use Object'. If self.npcs is not None then 'Talk to NPC' must be first in list.
    description_txt=str(Path_room_txt.joinpath('digital_hospital.txt').resolve()), # String representation of the text file that contains the Room's description
    doors=['the Commons'], # List of strings that represent doors
    npcs=['Fleer'], # optional arg, list of strings that represent npcs, default is None
    objects=None) # optional arg, list of strings that represent objects, default is None

DigitalHospital_E = Room(
    quick_desc=['the Digital Hospital', p_func.txt_to_str('digital_hospital_quick', 'room')],
    choices=['Talk to NPC'], 
    description_txt=str(Path_room_txt.joinpath('digital_hospital_e.txt').resolve()), 
    doors=['the Commons'], 
    npcs=['Fleer', 'IG-42']) 

DigitalHospital_F = Room(
    quick_desc=['the Digital Hospital', p_func.txt_to_str('digital_hospital_quick', 'room')],
    choices=['Talk to NPC'], 
    description_txt=str(Path_room_txt.joinpath('digital_hospital_f.txt').resolve()), 
    doors=['the Commons'],
    npcs=['Fleer'])

DockShop = Room(
    quick_desc=["the Dock Shop", 'an industrial, multi-purpose area.'],
    choices=[], 
    description_txt=str(Path_room_txt.joinpath('dock_shop.txt').resolve()),
    doors=['the Main Hall', 'the Receiving Office', 'the Holographic Transport Station']) 

DockShop_E = Room(
    quick_desc=["the Dock Shop", p_func.txt_to_str('dock_shop_e_quick', 'room')],
    choices=['Talk to NPC', 'Place Order or Ship Item'], 
    description_txt=str(Path_room_txt.joinpath('dock_shop.txt').resolve()), 
    doors=['the Main Hall', 'the Receiving Office', 'the Holographic Transport Station'],
    npcs=['Orix'],
    objects=['Dock Shop Chest'])

HoloTran = Room(
    quick_desc=['the Holographic Transport Station', p_func.txt_to_str('holo_tran_quick', 'room')],
    choices=['Talk to NPC'],
    description_txt=str(Path_room_txt.joinpath('holo_tran.txt').resolve()),
    doors=['the Dock Shop'],
    npcs=['Gleemon'])

HoloTran_E = Room(
    quick_desc=['the Holographic Transport Station', p_func.txt_to_str('holo_tran_quick', 'room')],
    choices=['Talk to NPC', 'Use Object'], 
    description_txt=str(Path_room_txt.joinpath('holo_tran_e.txt').resolve()), 
    doors=['the Dock Shop'],
    npcs=['Gleemon'],
    objects=['Micro Bot Holographic Transporter'])

MainHall = Room(
    quick_desc=['the Main Hall', 'long and wide with many doors lining the walls. A small, clunky robot is approaching you...'],
    choices=['Talk to NPC'],
    description_txt=str(Path_room_txt.joinpath('main_hall.txt').resolve()),
    doors=['the Commons'],
    npcs=['Ceith'])

MainHall_NoCeith = Room(
    quick_desc=['the Main Hall', 'long and surprisingly wide with many doors lining the walls.'],
    choices=[], 
    description_txt=str(Path_room_txt.joinpath('main_hall_no_ceith.txt').resolve()),
    doors=['the Commons', "Fleer's Room", "Orix's Room", 'the West Wing', 
           "Myrum's Room", "Gleemon's Room", 'the East Wing', 'the Dock Shop'])

MicroLodge = Room(
    quick_desc=['the Micro Lodge', p_func.txt_to_str('micro_lodge_quick', 'room')],
    choices=[],
    description_txt=str(Path_room_txt.joinpath('micro_lodge.txt').resolve()), 
    doors=['the Commons'])

MicroLodge_E = Room(
    quick_desc=['the Micro Lodge', p_func.txt_to_str('micro_lodge_quick', 'room')],
    choices=[],
    description_txt=str(Path_room_txt.joinpath('micro_lodge_e.txt').resolve()), 
    doors=['the Commons'])

MyrumRoom = Room(
    quick_desc=["Myrum's Room", p_func.txt_to_str('myrum_room_quick', 'room')],
    choices=["Use Myrum's Step Stool"],
    description_txt=str(Path_room_txt.joinpath('myrum_room.txt').resolve()), 
    doors=['the Main Hall'],
    objects=["Myrum's Cabinet"])

MyrumRoom_E = Room(
    quick_desc=["Myrum's Room", "a cozy little spaceship apartment."],
    choices=["Myrum's Step-Stool"],
    description_txt=str(Path_room_txt.joinpath('myrum_room.txt').resolve()),
    doors=['the Main Hall'], 
    objects=["Myrum's Cabinet", "Myrum's Bulletin Board"])

PCRoom = Room(
    quick_desc=['your room', 'quite small but perfectly comfortable for somone your size.'],
    choices=['Use Object'], #* populated with choices once the player enters PCRoom for first time
    description_txt=str(Path_room_txt.joinpath('pc_room.txt').resolve()), 
    doors=['the Micro Lodge'],
    objects=['Book titled "Tips for First Time Bots"']) #* populated with objects once the player enters MircoLodge for first time

RecOffice = Room(
    quick_desc=['the Receiving Office', p_func.txt_to_str("rec_office_quick", 'room')],
    choices=[],
    description_txt=str(Path_room_txt.joinpath('rec_office.txt').resolve()), 
    doors=['the Dock Shop'])

RecOffice_E = Room(
    quick_desc=['the Receiving Office', p_func.txt_to_str("rec_office_e_quick", 'room')],
    choices=['Use Object'],
    description_txt=str(Path_room_txt.joinpath('rec_office.txt').resolve()), 
    doors=['the Dock Shop'],
    objects=['Light Switch'])

RecOffice_F = Room(
    quick_desc=['the Receiving Office', p_func.txt_to_str("rec_office_f_quick", 'room')],
    choices=['Use Object'],
    description_txt=str(Path_room_txt.joinpath('rec_office_f.txt').resolve()), 
    doors=['the Dock Shop'],
    objects=["""A large box with a sign that reads- "Today's deliveries. We are under-staffed so please help yourself" """])

WestWing = Room(
    quick_desc=["the West Wing", p_func.txt_to_str("west_wing_quick", 'room')],
    choices=[],
    description_txt=str(Path_room_txt.joinpath('west_wing.txt').resolve()), 
    doors=['the Main Hall']) 

WestWing_E = Room(
    quick_desc=["the West Wing", p_func.txt_to_str("west_wing_quick", 'room')],
    choices=['Look at the rug'], 
    description_txt=str(Path_room_txt.joinpath('west_wing_e.txt').resolve()), 
    doors=['the Main Hall'],
    objects=['Lift up the corner of the rug'])

#*****************************************************************************************************************************************************************************
#*****************************************************************************************************************************************************************************
#! Game Intro - Part 1 of game begins
#*****************************************************************************************************************************************************************************
#*****************************************************************************************************************************************************************************

#*==========================================================
#! Intro Sequence & Start-Up Options
#*==========================================================

game_status = 'Start-Up Options'

while game_status == 'Start-Up Options': #* opening sequence and art
    p_func.animate_txt('dedication_flower(final)', 'art', .001, .007)
    p_func.print_txt('credits', 'misc')
    input('[Enter]')
    p_func.animate_strings(['', '', 'W  E  L  C  O  M  E     T  O  .  .  .  ', '', ''])
    p_func.animate_txt('boot_opening_art_final(60x100)', 'art', .001, .009)
    p_func.animate_strings(['What would you like to do?'])
    print('1: Create a new character\n2: Load a previously created character')

    try:
        start_up_choice = str(input('Enter your choice: '))
        if start_up_choice not in ['1', '2']:
            raise ValueError

    except ValueError:
        print('You must choose 1 or 2.')

    if start_up_choice == '1':
        game_status = 'Intro Options'

    elif start_up_choice == '2':
        load_sequence = 'Active'

        while load_sequence == 'Active':
            p_func.print_txt('load_instructions_pt1', 'misc')
            p_func.print_txt('load_instructions_pt2', 'misc')

            try:
                original_character = input("Enter your character's name: ")
                if os.path.isfile(f'{original_character}_original.txt') == False:
                    raise ValueError

            except ValueError:
                p_func.speech_txt('loading_fail', 'misc')
                load_sequence = 'Failed'
                game_status = 'Start-Up Options'
                
            else:
                with open(f'{original_character}_original.txt', 'r') as player_data:
                    character_sheet = literal_eval(player_data.read())

                    load_sequence = 'Successful'
                    game_status = 'Roaming'
                    room_location = 'Digital Hospital'
                    p_func.animate_strings(['Character Load Successful.', 'Welcome Back!'])   

while game_status == 'Intro Options':
    p_func.animate_strings(['******************', '******************', '******************\n'])
    p_func.animate_strings(['GAME TIP:\n When you see this symbol, hit enter to continue:', ''], .06, .2)
    input('<<<<<<---|--->>>>>>\n')
    p_func.animate_strings(['Would you like to go through the intro sequence (about 5 minutes) or skip to character creation?'])
    game_status = 'Intro Choice'

while game_status == 'Intro Choice':
    print('1) Start at intro\n2) Skip intro and start at character creation')

    try:
        intro_choice = str(input('Enter your choice: '))
        if start_up_choice not in ['1', '2']:
            raise ValueError

    except ValueError:
        print('You must choose 1 or 2.')

    if intro_choice == '1':
        p_func.animate_strings(['', 'Great! Time to B O O T', '', ''], .07, .07)
        input('<<<<<<---|--->>>>>>\n')
        game_status = 'Intro Sequence'

    elif intro_choice == '2':
        p_func.animate_strings(['Got it.', "Let's get right to it...", ''])
        input('<<<<<<---|--->>>>>>\n')
        character_sheet[0]['Name'] = 'empty'
        game_status = 'Character Creation'


#*==========================================================
#! Narrative Intro Sequence Begins
#*==========================================================

while game_status == 'Intro Sequence':

    if character_sheet[0]['Name'] == '': # Long introductory sequence begins only if player name is default empty string
        p_func.rand_char_gen(Path_misc_txt.joinpath('binary').resolve(), 15, .005, .05)
        p_func.detection('Alert', 'Boot sequence initiated', 'Now booting...')
        p_func.rand_char_gen(Path_misc_txt.joinpath('binary').resolve(), 30, .0025, .05)
        p_func.detection('Alert', 'Boot sequence complete', 'Welcome')
        input('<<<<<<---|--->>>>>>\n')
        p_func.detection('Audio Alert', 'Unknown species', 'It begins speaking', 'Translation: SUCCESSFUL')
        p_func.animate_strings(['"Ahhhh, there you are."\n'], scrolling_delay=.1, newline_delay=1)
        p_func.detection('Audio Alert', 'Digital crackling', 'Distorted vocalization', 'Translation: ERROR')
        p_func.animate_strings(['"Oo0opsz, cR@ppp."', '"P@wwzz."', '"I s@1d p@@HHZZZ!!!"\n'], scrolling_delay=.12, newline_delay=.4)
        p_func.rand_char_gen(Path_misc_txt.joinpath('static').resolve(), 8, .01, .07)
        p_func.animate_strings(['"Noo, th@ts N07  &*^%^$#..."\n'], scrolling_delay=.1, newline_delay=.4)
        p_func.rand_char_gen(Path_misc_txt.joinpath('static').resolve(), 6, .01, .07)
        p_func.animate_strings(['"Arg... harmmfffff..."\n'], scrolling_delay=.1)
        p_func.rand_char_gen(Path_misc_txt.joinpath('static').resolve(), 4, .01, .07)
        print('Reactivate sensors:\n') 
        input('<<<<<<---|--->>>>>>\n')
        p_func.detection('Audio Alert', 'Distortion neutralized', 'Speech detection online', 'Translation: SUCCESSFUL')
        p_func.animate_strings(['"I said P A U S E! Damnit. What about that did you not understand!???"\n'], scrolling_delay=.07, newline_delay=.3)
        p_func.detection('Audio & Visual Alert', 'Unknown species', 'Standing before you', 'Looking in your direction', 'It begins to speak')
        p_func.speech_txt('intro_pt1', 'misc')
        input('<<<<<<---|--->>>>>>\n')      
        p_func.speech_txt('intro_pt2', 'misc')
        input('<<<<<<---|--->>>>>>\n')
        p_func.speech_txt('intro_pt3', 'misc')
        p_func.detection('Surface Sensor Alert', 'Fleer places his hand on your shoulder', 'He smiles then continues speaking')
        input('<<<<<<---|--->>>>>>\n')
        p_func.speech_txt('intro_pt4', 'misc')
        input('<<<<<<---|--->>>>>>\n')
        p_func.speech_txt('intro_pt5', 'misc')
        input('<<<<<<---|--->>>>>>\n')
        p_func.speech_txt('intro_pt6', 'misc')       
        p_func.detection('Multi-Sensor Alerts', 'Fleer turns around', 'He picks up a touchscreen device', 'And continues speaking to you')
        character_sheet[0]['Name'] = 'empty' # Prevents intro sequence from replaying again
        game_status = 'Character Creation'

#*==========================================================
#! Character Creation
#*==========================================================

while game_status == 'Character Creation':

    if character_sheet[0]['Name'] == 'empty': #* Player chooses name
        character_sheet[0]['Name'] = input('What is your name?: ')      
        if character_sheet[0]['Name'] == '':
            character_sheet[0]['Name'] = 'empty'
            print('You gotta enter a name')
    else:
        game_status = 'Origin Choice'
        print('')

while game_status == 'Origin Choice': #* Player chooses area of Origin
    p_func.speech_str_list(['Were you from Earth, Mars, Europa, or somewhere else?'])

    origin_decision = 'In Progress'
    while origin_decision == 'In Progress':
    
        try:       
            character_sheet[0]['Origin'] = input('Choose letter-- [e]arth, [m]ars, euro[p]a, or [s]omewhere else?: ')
            if character_sheet[0]['Origin'] not in ['e', 'm', 'p', 's']:
                raise ValueError
                    
        except ValueError:
            print('You must choose a letter from the options.')
    
        else:
            origin_decision = 'Decided'
            
    if character_sheet[0]['Origin'] == 'e':
        character_sheet[0]['Origin'] = 'Earth'
        game_status = 'PC Questions'
        print('')

    elif character_sheet[0]['Origin'] == 'm':
        character_sheet[0]['Origin'] = 'Mars'
        game_status = 'PC Questions'
        print('')
            
    elif character_sheet[0]['Origin'] == 'p':
        character_sheet[0]['Origin'] = 'Europa'
        game_status = 'PC Questions'
        print('')                

    elif character_sheet[0]['Origin'] == 's':
        character_sheet[0]['Origin'] = 'Unknown'
        game_status = 'PC Questions'
        print('')  

while game_status == 'PC Questions': #* PC is asked series of questions, attribute bonuses correspond to choices.

    question_sequence = 'PC Question1'
    p_func.speech_str_list(['Fleer says "Ok, onto some more specific questions..."', '', '"Do you prefer to work inside or outside?"'])
    while question_sequence == 'PC Question1':
        pc_question1 = input('Enter [1] for INSIDE --- or [2] for OUTSIDE: ')
        print('')
        if pc_question1 == '1' or pc_question1 == '2':
            p_func.speech_str_list(['"Alright, got it. Next..."', '', '"Do you prefer to work alone or as part of a team?"'])
            question_sequence = 'PC Question2'
        else:
            question_sequence = 'PC Question1'
        
    while question_sequence == 'PC Question2':            
        pc_question2 = input('Enter [1] for ALONE --- or [2] for TEAM: ')
        print('')
        if pc_question2 == '1' or pc_question2 == '2':
            p_func.speech_str_list(['"Okay."', '"Now-- Would you say you are more likely to trust your outward senses or your internal intuition?"']) 
            question_sequence = 'PC Question3'               
        else:
            question_sequence = 'PC Question2'

    while question_sequence == 'PC Question3':            
        pc_question3 = input('Enter [1] for SENSES --- or [2] for INTUITION: ')
        print('')
        if pc_question3 == '1' or pc_question3 == '2':            
            p_func.speech_str_list(['Fleer spins some knobs on the Revival Computer then says', '"Which scenario happens more often--"',
                                    '"You gain respect from a coworker for coming up with a quick solution to a tough problem?"',
                                    '"Or you gain respect from a coworker for cheering them up on a tough day?"'])
            question_sequence = 'PC Question4'               
        else:
            question_sequence = 'PC Question3'

    while question_sequence == 'PC Question4': 
        pc_question4 = input('Enter [1] for QUICK SOLUTION --- or [2] for CHEER THEM UP: ')
        print('')
        if pc_question4 == '1' or pc_question4 == '2':
            p_func.speech_str_list(['"Onto the final question..."', '"Generally speaking, do you consider yourself to have above average luck?"',
                                    '"Or below average luck?"'])
            question_sequence = 'PC Question5'
        else:
            question_sequence = 'PC Question4'

    while question_sequence == 'PC Question5': 
        pc_question5 = input('Enter [1] for ABOVE AVG LUCK --- or [2] for BELOW AVG LUCK: ')
        print('')
        if pc_question5 == '1' or pc_question5 == '2':
            question_sequence = 'Luck Test'
        else:
            question_sequence = 'PC Question5'

    while question_sequence == 'Luck Test': #* Coin flip Luck test
        p_func.speech_str_list(['"Alright, now we will test your current luck."', '"I will flip this coin..."',
                                '"Do you think it will be heads or tails?"'])
        coin_flip = random.choice(['Heads', 'Tails'])
        pc_coin_flip_answer = input('Enter [1] for Heads --- or [2] for Tails: ')
        print('')
        if pc_coin_flip_answer == '1':
            pc_coin_flip_answer = 'Heads'
            if pc_coin_flip_answer == coin_flip:
                p_func.speech_str_list([f'Fleer flips the coin into the air and it lands {coin_flip} side up.', 
                                '"Ah, you do have some luck I see!"', ''])
                question_sequence = 'Question1 Results'

            else:
                p_func.speech_str_list([f'Fleer flips the coin into the air and it lands {coin_flip} side up.', 
                                '"Hmmm, looks like you guessed wrong."', ''])
                question_sequence = 'Question1 Results'
            
        elif pc_coin_flip_answer == '2':
            pc_coin_flip_answer = 'Tails'
            if pc_coin_flip_answer == coin_flip:
                p_func.speech_str_list([f'Fleer flips the coin into the air and it lands {coin_flip} side up.', 
                                '"Ah, you do have some luck I see!"', ''])
                question_sequence = 'Question1 Results'

            else:
                p_func.speech_str_list([f'Fleer flips the coin into the air and it lands {coin_flip} side up.', 
                                '"Hmmm, looks like you guessed wrong."', ''])
                question_sequence = 'Question1 Results'

        else:
            question_sequence = 'Luck Test'

#* Assigning bonuses to attirbutes based on choices made by player:                   
    while question_sequence == 'Question1 Results':
        if pc_question1 == '1':
            character_sheet[1]['Int'] += 2
            question_sequence = 'Question2 Results'                    
        else:
            character_sheet[1]['Itu'] += 2
            question_sequence = 'Question2 Results'

    while question_sequence == 'Question2 Results':
        if pc_question2 == '1':
            character_sheet[1]['Int'] += 2
            question_sequence = 'Question3 Results'                    
        else:
            character_sheet[1]['Chr'] += 2
            question_sequence = 'Question3 Results'
                    
    while question_sequence == 'Question3 Results':
        if pc_question3 == '1':
            character_sheet[1]['Alt'] += 2
            question_sequence = 'Question4 Results'                    
        else:
            character_sheet[1]['Itu'] += 2
            question_sequence = 'Question4 Results'

    while question_sequence == 'Question4 Results':
        if pc_question4 == '1':
            character_sheet[1]['Alt'] += 2
            question_sequence = 'Question5 Results'                 
        else:
            character_sheet[1]['Chr'] += 2
            question_sequence = 'Question5 Results'
            
    while question_sequence == 'Question5 Results':
        if pc_question5 == '1':
            character_sheet[1]['Lck'] += 2
            question_sequence = 'Coin Flip Results'                    
        else:
            random_attrib = random.choice(['Int', 'Alt', 'Itu', 'Chr'])
            character_sheet[1][random_attrib] += 2
            question_sequence = 'Coin Flip Results'
            
    while question_sequence == 'Coin Flip Results':
        if pc_coin_flip_answer == coin_flip:
            character_sheet[1]['Lck'] += 2
            question_sequence = 'Complete'
            game_status = 'Roll Attributes'
        else:
            random_attrib = random.choice(['Int', 'Alt', 'Itu', 'Chr'])
            character_sheet[1][random_attrib] += 2
            question_sequence = 'Complete'
            game_status = 'Roll Attributes' 

while game_status == 'Roll Attributes': #* PC rolls 1D6 3 times and assigns values to attribute of choice
    p_func.speech_str_list(['Fleer stops to make some final adjustments on the Revival Computer.', 'Then he says--',
                            '"Alright, everything is looking good."', '"Here is what you look like so far..."', ''])
    input('<<<<<<---|--->>>>>>\n') 
    package_player_data()
    p_func.print_attrib() # Displaying current attributes for player to view
    input('\n<<<<<<---|--->>>>>>\n') 
    p_func.speech_txt('intro_pt7', 'misc')
    p_func.detection('Alert', 'System upgrade in progress...')
    input('<<<<<<---|--->>>>>>\n') 
    roll_count = 0
    while roll_count < 3: #* Rolling begins
        input('Hit enter to roll 1d6: ')
        print('')
        d6 = random.randrange(1, 7)
        roll_count += 1
        roll_choice = 'Deciding'
        while roll_choice == 'Deciding':
            p_func.animate_strings([f'You rolled {d6}.', ''], .05, .06)
            attribute_assignment = input('Would you like to assign this to [i]ntelligence, [a]lertness, int[u]ition, [c]harisma, or [l]uck?: ')
            print('')
            if attribute_assignment == 'i':
                character_sheet[1]['Int'] += d6
                roll_choice = 'Decided'

            elif attribute_assignment == 'c':
                character_sheet[1]['Chr'] += d6
                roll_choice = 'Decided'

            elif attribute_assignment == 'a':
                character_sheet[1]['Alt'] += d6
                roll_choice = 'Decided'

            elif attribute_assignment == 'u':
                character_sheet[1]['Itu'] += d6
                roll_choice = 'Decided'

            elif attribute_assignment == 'l':
                character_sheet[1]['Lck'] += d6
                roll_choice = 'Decided'

            else:
                roll_choice == 'Deciding'            

    p_func.animate_strings(["Good, now let's take a look again...", ''])
    input('<<<<<<---|--->>>>>>\n')   
    package_player_data()
    p_func.print_attrib() #* Displaying newly updated attributes for player to view
    input('\n<<<<<<---|--->>>>>>\n')  
    p_func.speech_txt('intro_pt8', 'misc')
    input('<<<<<<---|--->>>>>>\n')
    p_func.print_txt('intro_survival_tips', 'misc')
    input('\n<<<<<<---|--->>>>>>\n')
    p_func.speech_txt('intro_pt9', 'misc')

#* Player chooses password for room door:
    p_func.speech_str_list(['"What would you like your room password to be?"', ''])
    pc_room_password = None
    while pc_room_password == None:  
        try:
            pc_room_password = str(input('Choose whatever you want for your password: '))
            print('')
            if pc_room_password == '':
                raise ValueError
        except ValueError:
            print('You must choose at least one character for your password.')
            pc_room_password = None

        else:
            p_func.speech_str_list(['Fleer says "Okay, got it".', ''])
            p_func.detection('Inventory Alert', 'Fleer hands you the following items:', f'Small notecard that says "{pc_room_password}"', 'Map of The Whisp')
            character_sheet[3]['Inventory']['Items'].append(f'Notecard that says "{pc_room_password}"')
            character_sheet[4]['Internal Notes']['pc_room_password'] = pc_room_password

    p_func.animate_strings([""""Alright, you're all booted up and ready to go!" """, '"Have a look..."', ""])
    input('<<<<<<---|--->>>>>>\n') 
    package_player_data() #! character_sheet now completed. Displaying finished sheet to player:
    p_func.print_bio()
    p_func.print_hpx()
    p_func.print_attrib()
    p_func.print_inv()
    print('')
    input('<<<<<<---|--->>>>>>\n')
    p_func.speech_txt('fleer_send_off', 'npc')
    input('<<<<<<---|--->>>>>>\n')
#* Accepting starting quests:
    accept_quest(quest_name=f"Enter {character_sheet[0]['Name']}'s Room & Use Chest")
    accept_quest(quest_name=f"Use {character_sheet[0]['Name']}'s Hibernation Port")
    accept_quest(quest_name='Recharge Battery At Charging Station')
#* End of intro sequence:
    save_original_character() #* Original character is now complete
    save_player_data() 
    game_status = 'Break Point'


#*****************************************************************************************************************************************************************************
#*****************************************************************************************************************************************************************************
#! BREAK POINT - Part 1 is complete. Player can choose to save and exit or continue on.
#*****************************************************************************************************************************************************************************
#*****************************************************************************************************************************************************************************

while game_status == 'Break Point':
    p_func.print_txt('intro_complete', 'misc')
    print('1: Continue\n2: Save & Exit')

    try:
        start_up_choice = str(input('Enter your choice: '))
        if start_up_choice not in ['1', '2']:
            raise ValueError

    except ValueError:
        print('You must choose 1 or 2.')

    if start_up_choice == '1':
        p_func.animate_strings(["Got it.", 'Back to the game...'])
        game_status = 'Roaming'
        room_location = 'Digital Hospital'

    elif start_up_choice == '2':
        p_func.animate_strings([f'Your save file is called {character_sheet[0]["Name"]}_original.txt'])
        p_func.print_txt('goodbye_breakpoint', 'misc')
        game_status = 'Game Over'

#*****************************************************************************************************************************************************************************
#*****************************************************************************************************************************************************************************
#! MAIN GAME LOOP - Part 2 begins
#! Code is organized alphabetically by room_location
#*****************************************************************************************************************************************************************************
#*****************************************************************************************************************************************************************************

while game_status == 'Roaming': #* main condition of the game until player leaves via holographic transport
    
#!!!!!!!!!!! Begin ChargeStation: !!!!!!!!!!! 
    while room_location == 'Charge Station':
        package_player_data()
        save_player_data()

# Begin ChargeStation QUEST & CONDITION CHECKS:
        if character_sheet[4]['Internal Notes']['Day'] >= 7 and Slympto.available_quest == 'Survive': #*Slympto appears on day 7
            ChargeStation.roomstate = 'inactive' #* causes startup of MicroLodge_F FINAL STATE
            p_func.speech_txt('slympto_surprise', 'npc')
            p_func.detection('Warning', 'Hostility detected', 'Source: Slympto', 'Recommendation: Flee or Neutralize Threat')
            accept_quest(Slympto) #* Slympto Survive quest becomes active
# End ChargeStation QUEST & CONDITION CHECKS

# Begin 1st state ChargeStation:
        elif ChargeStation.roomstate == 'active' and character_sheet[4]['Internal Notes']['Day'] < 7:
            ChargeStation.enter_room()

            if ChargeStation.decisions == [4, 1]: # Door to Commons
                ChargeStation.clear_decisions
                room_location = 'Commons'
                battery_drain()
                
            elif ChargeStation.decisions == [5, 1]: # Use the Charging Station
                ChargeStation.clear_decisions        
                p_func.animate_txt('charging_art2', 'art', .001, .009)
                battery_charge()
                if character_sheet[4]['Internal Notes']['Used Charging Station'] == 'No':
                    character_sheet[4]['Internal Notes']['Used Charging Station'] = 'Yes'
                    complete_quest(xp=100, quest_name='Recharge Battery At Charging Station') #* Reacharge Battery Quest Completion

            else:
                ChargeStation.clear_decisions
# End 1st state ChargeStation

# Begin FINALSTATE ChargeStation:
        elif ChargeStation_F.roomstate == 'active':

            if Slympto.active_quest == ['Survive']:
                p_func.animate_txt('slympto_quest_choice', 'npc')
                attribute_choice = None
                
                while attribute_choice == None:
                
                    try:
                        attribute_choice = input('Enter your choice: ')
                        print('')
                        if attribute_choice not in ['1', '2']:
                            raise ValueError

                    except ValueError:
                        print('You must choose 1 or 2.')
                        attribute_choice = None

                if attribute_choice == '1':
                    attribute_check('Int', 3)

                    if attrib_pass_fail == 'Pass':
                        p_func.speech_txt('slympto_int_pass', 'npc')
                        p_func.detection('Alert', 'Threat neutralized', 'No danger detected')
                        complete_quest(xp=750, NPC_object=Slympto) #* Slympto robbery quest completed FULL XP
                        p_func.animate_strings(['Well that was exciting!', 'Everything seems to be fine now though...'])
                        IGfortytwo.qa_set_one.append((p_func.txt_to_str('ig42_new_question'), p_func.txt_to_str('ig42_new_answer'))) #* New question added for IG-42

                    elif attrib_pass_fail == 'Fail':
                        slympto_fail_sequence()

                elif attribute_choice == '2':
                    attribute_check('Itu', 3)
                    if attrib_pass_fail == 'Pass':
                        p_func.speech_txt('slympto_itu_pass', 'npc')
                        p_func.detection('Alert', 'Threat neutralized', 'No danger detected')
                        complete_quest(xp=750, NPC_object=Slympto) #* Slympto robbery quest completed FULL XP
                        p_func.animate_strings(['Well that was exciting!', 'Everything seems to be fine now though...'])
                        IGfortytwo.qa_set_one.append((p_func.txt_to_str('ig42_new_question'), p_func.txt_to_str('ig42_new_answer'))) #* New question added for IG-42

                    elif attrib_pass_fail == 'Fail':
                        slympto_fail_sequence()

            else:
                ChargeStation_F.enter_room()

                if ChargeStation_F.decisions == [4, 1]: # Door to Commons
                    ChargeStation_F.clear_decisions
                    room_location = 'Commons'
                    battery_drain()
                    
                elif ChargeStation_F.decisions == [5, 1]: # Use Charging Station
                    ChargeStation_F.clear_decisions        
                    p_func.animate_txt('charging_art2', 'art', .001, .009)
                    battery_charge()
                    if character_sheet[4]['Internal Notes']['Used Charging Station'] == 'No':
                        character_sheet[4]['Internal Notes']['Used Charging Station'] = 'Yes'
                        complete_quest(xp=100, quest_name='Recharge Battery At Charging Station') #* Reacharge Battery Quest Completion

                else:
                    ChargeStation_F.clear_decisions
# End FINALSTATE ChargeStation
#******** End ChargeStation *******

#!!!!!!!!!!!! Begin Commons: !!!!!!!!!!!  
    while room_location == 'Commons':
        package_player_data()
        save_player_data()
        
# Begin Commons QUEST & CONDITION CHECKS:
        if 'What are the rules of the game?' in dict(ArtupioAndCeith.asked) and ArtupioAndCeith.available_quest == 'Win all the CAMs':
            accept_quest(ArtupioAndCeith) #* ArtupioAndCeith quest is activated

        elif 'Is there something I can do to show my gratitude?' in dict(Myrum.asked) and Myrum.available_quest == 'Return the Favor':
            character_sheet[3]['Inventory']['Items'].append('Napkin with "982014" written on it')
            accept_quest(Myrum) #* Myrum quest activated
            
        elif "Myrum's Package" in character_sheet[3]['Inventory']['Items'] and MyrumJar.gold >= 5:
            p_func.speech_txt('myrum_quest_fullpass', 'npc')
            character_sheet[3]['Inventory']['Items'].remove("Myrum's Package")
            character_sheet[3]['Inventory']['Items'].append("Tricipian Forged Ring")
            character_sheet[1]['Lck'] += 3
            p_func.detection('Received Item', 'Tricipian Ring +3 Luck (permanent)')
            complete_quest(xp=1000, gold=2, NPC_object=Myrum) #* Myrum quest complete: package returned, no gold stolen, FULL REWARDS
                            
        elif MyrumJar.gold < 5 and "Return the Favor" in Myrum.active_quest:
            p_func.speech_txt('myrum_quest_angry', 'npc')
            if "Myrum's Package" in character_sheet[3]['Inventory']['Items']:
                character_sheet[3]['Inventory']['Items'].remove("Myrum's Package")
            complete_quest(NPC_object=Myrum) #* Myrum quest complete: package returned, STOLEN GOLD is reward, no XP

        elif Nima.active_quest == ['Find Adapter'] and character_sheet[4]['Internal Notes']['Searched Commons'] == 'No' and 'Search Room' not in Commons_GameRoom.choices: 
            Commons_GameRoom.add_or_remove_choice('Search Room', 'add') #* If Nima quest is active Search options are added to the room
            Commons_GameRoom.add_or_remove_object('Check behind the furniture', 'add')
        
        elif character_sheet[4]['Internal Notes']['Searched Commons'] == 'Yes' and 'Search Room' in Commons_GameRoom.choices: 
            Commons_GameRoom.add_or_remove_choice('Search Room', 'remove') #* If player has already searched room options are removed from Commons choices
            Commons_GameRoom.add_or_remove_object('Check behind the furniture', 'remove')                             
# End Commons QUEST & CONDITION CHECKS

# Begin 1st State Commons: 
        elif MainHall.roomstate == 'active': #* Condition for if Ceith is not in the Commons
            Commons.enter_room()

            if Commons.decisions == [4, 1]: # 7 Door options below
                Commons.clear_decisions
                p_func.animate_txt('robo_lodge', 'room', .04, .07)
                input('<<<<<<---|--->>>>>>\n')
                battery_drain()

            elif Commons.decisions == [4, 2]: 
                Commons.clear_decisions
                room_location = 'Digital Hospital'
                battery_drain()

            elif Commons.decisions == [4, 3]: 
                Commons.clear_decisions
                room_location = 'Micro Lodge'
                battery_drain()              

            elif Commons.decisions == [4, 4]: 
                Commons.clear_decisions
                room_location = 'Charge Station'   
                battery_drain()              

            elif Commons.decisions == [4, 5]: 
                Commons.clear_decisions
                p_func.animate_txt('bio_hospital', 'room', .04, .07)
                input('<<<<<<---|--->>>>>>\n')
                battery_drain()

            elif Commons.decisions == [4, 6]: 
                Commons.clear_decisions
                p_func.animate_txt('bio_lodge', 'room', .04, .07)
                input('<<<<<<---|--->>>>>>\n')
                battery_drain()

            elif Commons.decisions == [4, 7]: 
                Commons.clear_decisions
                room_location = 'Main Hall'
                battery_drain()

            elif Commons.decisions == [5, 1]: # NPC Myrum
                Commons.clear_decisions
                
                if 'What do you do here?' in dict(Myrum.asked) and Myrum.available_quest == 'Return the Favor': #Myrum q&a set advance, first step in quest activation
                    Myrum.adv_qa_sets(2)
                    Myrum.player_questions(goodbye_string2='takes a book out of her bag and starts reading. Maybe try back later.')
                    
                else:
                    Myrum.player_questions(goodbye_string1='smiles at you, then turns towards Artupio and asks him a question.')
                
            elif Commons.decisions == [5, 2]: # NPC Artupio
                Commons.clear_decisions
                Artupio.player_questions()

            elif Commons.decisions == [5, 3]: # NPC Slympto
                Commons.clear_decisions
                Slympto.player_questions(goodbye_string2=p_func.txt_to_str("slympto_goodbye2"))

            else:
                Commons.clear_decisions
# End 1st State Commons  

# Begin FINAL STATE Commons_GameRoom:
        elif MainHall.roomstate == 'inactive': #* Condition for if Ceith has left MainHall and is now in Commons
            Commons_GameRoom.enter_room()
            
            if Commons.decisions == [4, 1]: # 7 door options below
                Commons.clear_decisions
                p_func.speech_str(p_func.txt_to_str('robo_lodge', 'room'))
                battery_drain()

            elif Commons.decisions == [4, 2]: 
                Commons.clear_decisions
                room_location = 'Digital Hospital'
                battery_drain()

            elif Commons.decisions == [4, 3]: 
                Commons.clear_decisions
                room_location = 'Micro Lodge'
                battery_drain()              

            elif Commons.decisions == [4, 4]: 
                Commons.clear_decisions
                room_location = 'Charge Station'   
                battery_drain()              

            elif Commons.decisions == [4, 5]: 
                Commons.clear_decisions
                p_func.speech_str(p_func.txt_to_str('bio_hospital', 'room'))
                battery_drain()

            elif Commons.decisions == [4, 6]: 
                Commons.clear_decisions
                p_func.speech_str(p_func.txt_to_str('bio_lodge', 'room'))
                battery_drain()

            elif Commons.decisions == [4, 7]: 
                Commons.clear_decisions
                room_location = 'Main Hall'
                battery_drain()

            elif Commons.decisions == [5, 1]: # NPC Myrum
                Commons.clear_decisions
                
                if 'What do you do here?' in dict(Myrum.asked) and Myrum.available_quest == 'Return the Favor': #Myrum q&a set advance, first step in quest activation
                    Myrum.adv_qa_sets(2)
                    Myrum.player_questions(goodbye_string2='takes a book out of her bag and starts reading. Maybe try back later.')
                    
                else:
                    Myrum.player_questions(goodbye_string1='smiles at you, then turns towards Artupio and asks him a question.')

            elif Commons.decisions == [5, 2]: # NPC ArtupioAndCeith
                Commons.clear_decisions
                
                if 'Win all the CAMs' in ArtupioAndCeith.active_quest: # Condition for if quest is unlocked and active
                    play_slam_cam_choice = None

                    while play_slam_cam_choice == None:

                        try:
                            play_slam_cam_choice = str(input('Artupio says "How about a game of Double Hundo Slam Cam?" [y] or [n]: '))
                            if play_slam_cam_choice not in ['y', 'n']:
                                raise ValueError

                        except ValueError:
                            print('You must choose [y] or [n]')
                            play_slam_cam_choice = None

                    if play_slam_cam_choice == 'y':
                        slamcam()

                    elif play_slam_cam_choice == 'n':
                        p_func.animate_strings(['"Ok, come back and see us when you want to play."'])
                
                elif 'Why are you two looking at me like that?' in dict(ArtupioAndCeith.asked) and 'What are the rules of the game?' not in dict(ArtupioAndCeith.asked): #first step to unlocking quest
                    ArtupioAndCeith.adv_qa_sets(2)
                    ArtupioAndCeith.player_questions('return to what they were doing.', 'start talking about something else, maybe try back later.')
                
                else: # This will catch conditions for if player is talking to ArtupioAndCeith for the first time OR if player has already completed quest
                    if 'Win all the CAMs' in ArtupioAndCeith.compltdquest:
                        ArtupioAndCeith.player_questions(goodbye_string2=p_func.txt_to_str('artupioandceith_goodbye2'))

                    else:
                        p_func.animate_strings(['You approach Artupio and Ceith.', 'They are staring at you with an excited look in their eyes...'])
                        ArtupioAndCeith.player_questions('return to what they were doing.', 'start talking about something else, maybe try back later.')

            elif Commons_GameRoom.decisions == [6, 1]: # Option for Search Room if Nima's quest is active
                Commons.clear_decisions
                character_sheet[4]['Internal Notes']['Searched Commons'] = 'Yes'
                nima_search('Commons', 'Alt') 

            else:
                Commons_GameRoom.clear_decisions           
# End FINAL STATE Commons
#******* End Commons *******

#!!!!!!!!!!!! Begin Digital Hospital: #!!!!!!!!!!!!
    while room_location == 'Digital Hospital': 
        package_player_data()
        save_player_data()
        
# Begin Digital Hospital QUEST & CONDITION CHECKS:
        if 'How can I make some money?' in dict(Fleer.asked) and character_sheet[4]['Internal Notes']['Asked About Money'] == 'No': #unlocking Fleer quest
            Fleer.adv_qa_sets(2)
            accept_quest(Fleer)
            character_sheet[4]['Internal Notes']['Asked About Money'] = 'Yes'
        
        elif "Fleer's Package" in character_sheet[3]['Inventory']['Items'] and 'Get Package' in Fleer.active_quest: #* Fleer quest completion
            character_sheet[3]['Inventory']['Items'].remove("Fleer's Package")
            Fleer.npc_items['CAMs'] -= 10 # removing Fleer's CAMs just for the heck of it
            p_func.speech_txt('fleer_quest_complete', 'npc')
            complete_quest(xp=500, cams=10, NPC_object=Fleer)          
# End Digital Hospital QUEST & CONDITION CHECKS

# Begin 1st State Digital Hospital (UNEXAMINED): 
        elif DigitalHospital.examined == 'No':                        
            DigitalHospital.enter_room()                       
            
            if DigitalHospital.decisions == [4, 1]: # Door to Commons
                DigitalHospital.clear_decisions
                room_location = 'Commons'
                battery_drain()
        
            elif DigitalHospital.decisions == [5, 1]: # NPC Fleer
                DigitalHospital.clear_decisions

                if 'What should I do if I get injured?' in dict(Fleer.asked): #* Fleer healing option
                    fleer_healing()
                    Fleer.player_questions('says "I need to get back to work. Come back and see me soon."', "is busy setting up for an operation.")
                
                else:
                    Fleer.player_questions('says "I need to get back to work. Come back and see me soon."', "is busy setting up for an operation.")
        
            else:
                DigitalHospital.clear_decisions
# End 1st State Digital Hospital

# Begin 2nd State DigitalHospital_E (EXAMINED) where player can talk to IG-42 based on if Slympto quest is not completed:
        elif DigitalHospital.examined == 'Yes' and Slympto.available_quest == 'Survive':
            DigitalHospital.roomstate = 'inactive'
            DigitalHospital_E.enter_room()
            
            if DigitalHospital_E.decisions == [4, 1]: # Door to Commons
                DigitalHospital_E.clear_decisions
                room_location = 'Commons'
                battery_drain()
        
            elif DigitalHospital_E.decisions == [5, 1]: # NPC Fleer
                DigitalHospital_E.clear_decisions

                if 'What should I do if I get injured?' in dict(Fleer.asked): #* Fleer healing option
                    fleer_healing()
                    Fleer.player_questions('says "I need to get back to work. Come back and see me soon."', "is busy setting up for an operation.")
                
                else:
                    Fleer.player_questions('says "I need to get back to work. Come back and see me soon."', "is busy setting up for an operation.")

            elif DigitalHospital_E.decisions == [5, 2]: # NPC IG-42
                DigitalHospital_E.clear_decisions

                if 'Where are you from?' in dict(IGfortytwo.asked) and 'Were you ever a biological creature?' not in dict(IGfortytwo.asked): 
                    IGfortytwo.adv_qa_sets(2)
                    IGfortytwo.player_questions(p_func.txt_to_str('ig42_goodbye'), p_func.txt_to_str('ig42_goodbye'))

                elif 'Were you ever a biological creature?' in dict(IGfortytwo.asked) and 'What do you think about not having choices?' not in dict(IGfortytwo.asked):
                    IGfortytwo.adv_qa_sets(3)
                    IGfortytwo.player_questions(p_func.txt_to_str('ig42_goodbye'), p_func.txt_to_str('ig42_goodbye'))
                
                else:
                    IGfortytwo.player_questions(p_func.txt_to_str('ig42_goodbye'), p_func.txt_to_str('ig42_goodbye'))

        
            else:
                DigitalHospital_E.clear_decisions
# End 2nd State DigitalHospital_E

# Begin FINAL STATE DigitalHospital_F, activated once Slympto quest is complete, IG-42 no longer in room:
        elif Slympto.available_quest == 'None':
            DigitalHospital_E.roomstate = 'inactive'
            DigitalHospital_F.enter_room()
            
            if DigitalHospital_F.decisions == [4, 1]: # Door to Commons
                DigitalHospital_F.clear_decisions
                room_location = 'Commons'
                battery_drain()
        
            elif DigitalHospital_F.decisions == [5, 1]: # NPC Fleer
                DigitalHospital_F.clear_decisions

                if 'What should I do if I get injured?' in dict(Fleer.asked): #* Fleer healing option
                    fleer_healing()
                    Fleer.player_questions('says "I need to get back to work. Come back and see me soon."', "is busy setting up for an operation.")
                
                else:
                    Fleer.player_questions('says "I need to get back to work. Come back and see me soon."', "is busy setting up for an operation.")

            else:
                DigitalHospital_F.clear_decisions
# End FINAL STATE DigitalHospital_F
#******* End Digital Hospital *******

#!!!!!!!!!!!! Begin Dock Shop: !!!!!!!!!!!!
    while room_location == 'Dock Shop':
        package_player_data()
        save_player_data()            

# Begin Dock Shop QUEST & CONDITION CHECKS:   
        if DockShopChest.gold >= 5 and "Myrum's Order Form" in DockShopChest.items and character_sheet[4]['Internal Notes']['Myrum Step One'] == 'No':
            character_sheet[4]['Internal Notes']['Myrum Step One'] = 'Yes'
            character_sheet[4]['Internal Notes']['Myrum Package Tracker'] = character_sheet[4]['Internal Notes']['Day'] + 2 #* setting csheet variable to track Myrum's package

        elif "What kind of work do you need done? Why can't I do it?" in dict(Orix.asked) and Orix.available_quest == 'Five Days of Work':
            accept_quest(Orix) #* Orix quest is activated

        elif character_sheet[4]['Internal Notes']['Days Worked For Orix'] >= 5 and 'Five Days of Work' in Orix.active_quest: # Orix quest check for completion
            p_func.speech_txt('orix_quest_complete_pt1', 'npc')
            input('<<<<<<---|--->>>>>>\n')
            p_func.speech_txt('orix_quest_complete_pt2', 'npc')
            p_func.detection('Alert', 'DLH-15 Hull has been upgraded:', '+2 HP (Permanent)', 'You now have 8 of 8 health')
            character_sheet[2]['HPT'] += 2 #* Player health is increased and refilled
            character_sheet[2]['HPC'] += character_sheet[2]['HPT'] - character_sheet[2]['HPC']
            input('<<<<<<---|--->>>>>>\n')
            complete_quest(xp=600, NPC_object=Orix)

        elif "What do you have for sale?" in dict(Orix.asked) and character_sheet[4]['Internal Notes']['Orix Shop'] == 'Closed' and 'Tricipian Voltage Extender' not in character_sheet[3]['Inventory']['Items']:
            character_sheet[4]['Internal Notes']['Orix Shop'] = 'Open' #* Orix's Shop is activated

        elif Slympto.compltdquest == ['Survive'] and 'IG-42' not in DockShop_E.npcs:
            DockShop_E.add_or_remove_npc('IG-42', 'add') #* Adding IG-42 to Dock Shop if Slympto quest is complete
# End Dock Shop QUEST & CONDITION CHECKS

# Begin 1st State DockShop (UNEXAMINED):
        elif DockShop.examined == 'No':
            DockShop.enter_room()

            if DockShop.decisions == [4, 1]: # Door to Main Hall
                DockShop.clear_decisions
                room_location = 'Main Hall'
                battery_drain()

            elif DockShop.decisions == [4, 2]: # Door to Receiving Office
                DockShop.clear_decisions
                room_location = 'Receiving Office'
                battery_drain()

            elif DockShop.decisions == [4, 3]: # Door to Holographic Transport
                DockShop.clear_decisions
                room_location = 'Holographic Transport'
                battery_drain() 
                
            else:
                DockShop.clear_decisions               
# End 1st State DockShop

# Begin FINAL STATE DockShop_E (EXAMINED):
        elif DockShop.examined == 'Yes':
            DockShop.roomstate = 'inactive' # recording the shut-down of original Room
            DockShop_E.enter_room()
            
            if DockShop_E.decisions == [4, 1]: # Three doors below
                DockShop_E.clear_decisions
                room_location = 'Main Hall'
                battery_drain()

            elif DockShop_E.decisions == [4, 2]:
                DockShop_E.clear_decisions
                room_location = 'Receiving Office'
                battery_drain()

            elif DockShop_E.decisions == [4, 3]:
                DockShop_E.clear_decisions
                room_location = 'Holographic Transport'
                battery_drain() 

            elif DockShop_E.decisions == [5, 1]: # NPC Orix
                DockShop_E.clear_decisions

                if character_sheet[4]['Internal Notes']['Orix Shop'] == 'Open' and Orix.available_quest == 'Five Days of Work': # case for if Orix selling but not employing
                    orix_shop()

                elif Orix.active_quest == ['Five Days of Work'] and character_sheet[4]['Internal Notes']['Orix Shop'] == 'Closed': # case for if Orix employing but not selling
                    orix_work()

                elif Orix.active_quest == ['Five Days of Work'] and character_sheet[4]['Internal Notes']['Orix Shop'] == 'Open': # case for if Orix employing AND selling
                    orix_topic_choice = None

                    while orix_topic_choice == None:

                        try:
                            orix_topic_choice = input('Enter [1] to talk about employment. Enter [2] to see if Orix has anything for sale: ')
                            if orix_topic_choice not in ['1', '2']:
                                raise ValueError

                        except ValueError:
                            print('You must enter [1] or [2].')
                            orix_topic_choice == None

                    if orix_topic_choice == '1':
                        orix_work()

                    elif orix_topic_choice == '2':
                        orix_shop()

                elif 'Do you work here?' in dict(Orix.asked) and Orix.available_quest == 'Five Days of Work': # Checking to see if Player has asked first question
                    Orix.adv_qa_sets(2) # Advancing to next set of questions
                    Orix.player_questions('returns to what he was doing.', 'notices a ship waiting at the dock and starts heading over to help.')
                        
                else:
                    Orix.player_questions('returns to what he was doing.', 'notices a ship waiting at the dock and starts heading over to help.')
                    
            elif DockShop_E.decisions == [5, 2]: #* NPC IG-42 (if Slympto quest is complete)
                DockShop_E.clear_decisions

                p_func.animate_strings(['Thankfully, you see Slympto has been locked up and loaded onto an outbound prisoner transport pod.', 
                                        'IG-42 is standing guard waiting for the pod to launch.', ''])

                if 'Where are you from?' in dict(IGfortytwo.asked) and 'Were you ever a biological creature?' not in dict(IGfortytwo.asked): 
                    IGfortytwo.adv_qa_sets(2)
                    IGfortytwo.player_questions(p_func.txt_to_str('ig42_goodbye'), p_func.txt_to_str('ig42_goodbye'))

                elif 'Were you ever a biological creature?' in dict(IGfortytwo.asked) and 'What do you think about not having choices?' not in dict(IGfortytwo.asked):
                    IGfortytwo.adv_qa_sets(3)
                    IGfortytwo.player_questions(p_func.txt_to_str('ig42_goodbye'), p_func.txt_to_str('ig42_goodbye'))
                
                else:
                    IGfortytwo.player_questions(p_func.txt_to_str('ig42_goodbye'), p_func.txt_to_str('ig42_goodbye'))                
        
            elif DockShop_E.decisions == [6, 1]:
                DockShop_E.clear_decisions
                whisp_chest(DockShopChest)
                
            else:                
                DockShop.clear_decisions
# End FINAL STATE DockShop_E
#******* End Dock Shop *******

#!!!!!!!!!!!! Begin Holographic Transport: !!!!!!!!!!!!  
    while room_location == 'Holographic Transport':
        package_player_data()
        save_player_data()

# Begin Holographic Transport QUEST & CONDITION CHECKS:
        holo_tran_check = character_sheet[4]['Internal Notes']['Gleemon Holo Tran']

        if 'Lost Earring' in character_sheet[3]['Inventory']['Items'] and HoloTran.examined == 'Yes':
            p_func.speech_txt('gleemon_quest_complete', 'npc') 
            character_sheet[3]['Inventory']['Items'].remove('Lost Earring')
            p_func.speech_str_list(['"Here take this..." Gleemon hands you some gold coins.', '"It is the least I can do."', ''])
            complete_quest(xp=1500, gold=3, quest_name='Lost Earring') #* Gleemon quest completed

        elif 'I am ready to leave. Please send me to the Tricipian Merchant Market.' in dict(Gleemon.asked) and holo_tran_check == 'No':
            character_sheet[4]['Internal Notes']['Gleemon Holo Tran'] = 'Yes'
            holographic_transport()           
# End Holographic Transport QUEST & CONDITION CHECKS

# Begin 1st State HoloTran (UNEXAMINED):
        elif HoloTran.examined == 'No':
            HoloTran.enter_room()

            if HoloTran.decisions == [4, 1]:
                HoloTran.clear_decisions
                room_location = 'Dock Shop'
                battery_drain()
                
            elif HoloTran.decisions == [5, 1]: # NPC Gleemon
                HoloTran.clear_decisions

                if 'How should I prepare for transport?' in dict(Gleemon.asked) and "What do you think I should buy while I'm there?" not in dict(Gleemon.asked): 
                    Gleemon.adv_qa_sets(2)
                    Gleemon.player_questions('is interupted by something on her computer...', 'flips two small switches and spins a large knob.')

                elif "What do you think I should buy while I'm there?" in dict(Gleemon.asked) and "Any other advice you have for me out there?" not in dict(Gleemon.asked): 
                    Gleemon.adv_qa_sets(3)
                    Gleemon.player_questions('is interupted by something on her computer...', 'flips two small switches and spins a large knob.')

                else:
                    Gleemon.player_questions('is interupted by something on her computer...', 'flips two small switches and spins a large knob.')

            else:
                HoloTran.clear_decisions
# End 1st State Transport

# Begin FINAL STATE HoloTran_E:
        elif HoloTran.examined == 'Yes':
            HoloTran.roomstate = 'inactive'
            HoloTran_E.enter_room()

            if HoloTran_E.decisions == [4, 1]:
                HoloTran_E.clear_decisions
                room_location = 'Dock Shop'
                battery_drain()
                
            elif HoloTran_E.decisions == [5, 1]: # Gleemon
                HoloTran_E.clear_decisions

                if 'How should I prepare for transport?' in dict(Gleemon.asked) and "What do you think I should buy while I'm there?" not in dict(Gleemon.asked): 
                    Gleemon.adv_qa_sets(2)
                    Gleemon.player_questions('is interupted by something on her computer...', 'flips two small switches and spins a large knob.')

                elif "What do you think I should buy while I'm there?" in dict(Gleemon.asked) and "Any other advice you have for me out there?" not in dict(Gleemon.asked): 
                    Gleemon.adv_qa_sets(3)
                    Gleemon.player_questions('is interupted by something on her computer...', 'flips two small switches and spins a large knob.')

                else:
                    Gleemon.player_questions('is interupted by something on her computer...', 'flips two small switches and spins a large knob.')

            elif HoloTran_E.decisions == [6, 1]: #* Use microbot transporter
                HoloTran_E.clear_decisions
                holographic_transport()
                
            else:
                HoloTran_E.clear_decisions
# End FINAL STATE HoloTran_E
#******* End Holographic Transport *******

#!!!!!!!!!!!! Begin Main Hall: !!!!!!!!!!!!
    while room_location == 'Main Hall':
        package_player_data()
        save_player_data()

# Begin 1st State MainHall, active if player has not completed Ceith quest:
        if 'Power for CAMs' in Ceith.available_quest or 'Power for CAMs' in Ceith.active_quest:
            MainHall.enter_room(player_choices=False)
            p_func.animate_txt('ceith_request', 'npc') #* Ceith requests power for 7 CAMs
            MainHall.player_choices()

            if MainHall.decisions == [4, 1]: # Door to Commons
                MainHall.clear_decisions
                room_location = 'Commons'
                battery_drain()

            elif MainHall.decisions == [5,1]: # NPC Ceith
                if Ceith.available_quest == 'Power for CAMs':
                    accept_quest(Ceith)

                Ceith.player_questions(goodbye_string2='looks at you, awaiting a response...')
                MainHall.clear_decisions

                if Ceith.qa_set_one == []:
                    ceith_help = None
                    while ceith_help == None:

                        try:
                            ceith_help = input('Would you like to give Ceith some battery power in exchange for 7 CAMs? [y] or [n]: ')

                            if ceith_help not in ['y', 'n']:
                                raise ValueError

                        except ValueError:
                            print("You must enter 'y' for yes or 'n' for no.")
                            ceith_help = None

                        else:
                            if ceith_help == 'n':
                                p_func.animate_txt('ceith_miffed', 'npc')
                                MainHall.roomstate = 'inactive' #* Ceith leaves Main Hall. MainHall_NoCeith becomes active, Commons_GameRoom becomes active
                                complete_quest(xp=150, NPC_object=Ceith) #* Ceith Quest is completed

                            elif ceith_help == 'y':
                                p_func.animate_txt('ceith_give_power', 'npc')
                                MainHall.roomstate = 'inactive' #* Ceith leaves Main Hall. MainHall_NoCeith becomes active, Commons_GameRoom becomes active
                                Ceith.npc_items['CAMs'] -= 7                      
                                complete_quest(xp=300, cams=7, NPC_object=Ceith) #* Ceith Quest is completed
                                battery_drain(10) #* all power is drained from battery causing fleer_rescue()

            else:
                MainHall.clear_decisions
                p_func.animate_strings(['"Just help me out, no big deal, and you get seven CAMs."'])

# Begin FINAL STATE MainHall_NoCeith (Ceith quest is complete):
        elif MainHall.roomstate == 'inactive' and 'Power for CAMs' in Ceith.compltdquest:
            MainHall_NoCeith.enter_room()

            if MainHall_NoCeith.decisions == [4, 1]: # Door to Commons
                MainHall_NoCeith.clear_decisions
                room_location = 'Commons'
                battery_drain()

            elif MainHall_NoCeith.decisions == [4, 2]: # Door to Fleer's room, key_pad()
                key_pad("Fleer's room", 'Fleer')              

            elif MainHall_NoCeith.decisions == [4, 3]:
                key_pad("Orix's room", 'Orix')
                    
            elif MainHall_NoCeith.decisions == [4, 4]: # WestWing door entrance
                MainHall_NoCeith.clear_decisions
                p_func.animate_strings(["There is a keypad on the door..."])
                ww_door_code = input('Enter code: ')

                if ww_door_code == '1764':
                    room_location = "West Wing"
                    battery_drain()
                        
                else:
                    p_func.animate_strings(['Hmm...', 'Nothing nothing happens.'])                    

            elif MainHall_NoCeith.decisions == [4, 5]: # Door to MyrumRoom
                MainHall_NoCeith.clear_decisions
                p_func.animate_strings(["There is keypad on Myrum's door..."])
                myrum_door_code = input('Enter code: ')

                if myrum_door_code == '982014':
                    room_location = "Myrum's Room"
                    battery_drain()
                    
                else:
                    p_func.animate_strings(["Hmm...", 'Nothing happens.'])

            elif MainHall_NoCeith.decisions == [4, 6]: # Door to Gleemon's room, key_pad()
                key_pad("Gleemon's room", 'Gleemon')

            elif MainHall_NoCeith.decisions == [4, 7]: # Door to East Wing, key_pad()
                key_pad("the East Wing", 'the Captain of the Whisp')

            elif MainHall_NoCeith.decisions == [4, 8]: # Door to DockShop
                MainHall_NoCeith.clear_decisions
                room_location = 'Dock Shop'
                battery_drain()

            else:
                MainHall_NoCeith.clear_decisions  
# End FINAL STATE MainHall_NoCeith
#******* End Main Hall *******

#!!!!!!!!!!!! Begin Micro Lodge: !!!!!!!!!!!!
    while room_location == 'Micro Lodge':
        package_player_data()
        save_player_data()

# Begin Micro Lodge QUEST & CONDITION CHECKS:
        game_days_passed = character_sheet[4]['Internal Notes']['Day']
        searched_ml = character_sheet[4]['Internal Notes']['Searched Micro Lodge']
        searched_c = character_sheet[4]['Internal Notes']['Searched Commons']

        if PCRoom.objects == ['Book titled "Tips for First Time Bots"']: # adding player name to door, chest, and hibernation port
            PlayerChest.name = f"{character_sheet[0]['Name']}'s Chest" # Setting PlayerChest name based on player name
            MicroLodge_E.add_or_remove_door(f"{character_sheet[0]['Name']}'s Room",  'add')
            PCRoom.add_or_remove_object(f"{character_sheet[0]['Name']}'s Chest",  'add')
            PCRoom.add_or_remove_object(f"{character_sheet[0]['Name']}'s Hibernation Port",  'add')

        #* Nima is added to MicroLodge_E after 5 days have passed and Fleer's Package has been retreived and delivered
        elif game_days_passed >= 6 and MicroLodge_E.npcs == None and Nima.available_quest == 'Find Adapter' and Fleer.compltdquest == ["Get Package"]:
            MicroLodge_E.add_or_remove_npc('Nima', 'add')
            MicroLodge_E.add_or_remove_choice('Talk to NPC', 'add')

        elif "What are you looking for?" in dict(Nima.asked) and Nima.qa_set_two != []: # Step 1 in unlocking Nima quest
            Nima.adv_qa_sets(2)

        elif "I'll help you find the adapter, where should I look?" in dict(Nima.asked) and Nima.available_quest == 'Find Adapter': #* Condition to accept Nima quest
            accept_quest(Nima)

        #* If Nima quest is active Search Room is added to MicroLodge_E options:
        elif Nima.active_quest == ['Find Adapter'] and searched_ml == 'No' and 'Search Room' not in MicroLodge_E.choices: 
            MicroLodge_E.add_or_remove_choice('Search Room', 'add')
            MicroLodge_E.add_or_remove_object('Look under the rugs', 'add')

        #* If player has already searched room the option is removed from available choices:
        elif searched_ml == 'Yes' and 'Search Room' in MicroLodge_E.choices: 
            MicroLodge_E.add_or_remove_choice('Search Room', 'remove')
            MicroLodge_E.add_or_remove_object('Look under the rugs', 'remove')   
# End Micro Lodge QUEST & CONDITION CHECKS
    
# Begin 1st State MicroLodge (UNEXAMINED):
        elif MicroLodge.examined == 'No':
            MicroLodge.enter_room()

            if MicroLodge.decisions == [4, 1]: # Door to Commons
                MicroLodge.clear_decisions
                room_location = 'Commons'
                battery_drain()
                
            else:
                MicroLodge.clear_decisions
# End 1st State MicroLodge   

# Begin FINAL STATE MicroLodge_E (EXAMINED):
        elif MicroLodge.examined == 'Yes':
            MicroLodge.roomstate = 'inactive'
            MicroLodge_E.enter_room()

            if MicroLodge_E.decisions == [4, 1]: # Door to Commons
                MicroLodge_E.clear_decisions
                room_location = 'Commons'
                battery_drain()
                
            elif MicroLodge_E.decisions == [4, 2]: # Door to PCRoom
                MicroLodge_E.clear_decisions
                p_func.animate_strings(["There is keypad on the door..."])
                password_check = input('Enter code: ')
                if password_check == character_sheet[4]['Internal Notes']['pc_room_password']:
                    room_location = "PC Room"
                        
                else:
                    p_func.animate_strings(["Hmm...", 'Seems like you entered the wrong password.', 'Nothing is happening.'])

            elif MicroLodge_E.decisions == [5, 1]: #* NPC Nima is available if conditions are met
                MicroLodge_E.clear_decisions
                p_func.animate_strings(['Nima seems a bit distracted, she appears to be searching for something.'])

                if "Nima's Adapter" in character_sheet[3]['Inventory']['Items']: #* sequence for if player has retrieved Nima's Adapter
                    p_func.animate_txt('nima_quest_complete', 'npc')
                    p_func.detection('Upgrade in progress', 'Nima performs minor surgery on your mainframe', 'Total available power has been increased by one')
                    input('\n<<<<<<---|--->>>>>>\n')
                    character_sheet[3]['Inventory']['Items'].remove("Nima's Adapter")
                    character_sheet[2]['PT'] += 1
                    complete_quest(xp=500, NPC_object=Nima) #* Nima quest is completed
                    p_func.speech_str_list(['Nima says--', 'Alright, that should do it! Check it out...', ''])
                    p_func.print_vitals()
                    input('<<<<<<---|--->>>>>>\n')
                    p_func.animate_txt('nima_leaving_pass', 'npc')
                    MicroLodge_E.add_or_remove_npc('Nima', 'remove')
                    MicroLodge_E.add_or_remove_choice('Talk to NPC', 'remove')

                elif searched_ml == 'Yes' and searched_c == 'Yes' and Nima.active_quest == ['Find Adapter']: #* sequence for if player has failed to find Nima's Adapter
                    p_func.animate_strings(["Oh you're back...", "Thank you for taking the time to try and find it.", "I guess I'll have to order a new one.", ''])                  
                    complete_quest(xp=300, NPC_object=Nima)
                    p_func.animate_txt('nima_leaving_fail', 'npc')
                    MicroLodge_E.add_or_remove_npc('Nima', 'remove')
                    MicroLodge_E.add_or_remove_choice('Talk to NPC', 'remove')
                
                else:
                    Nima.player_questions('continues searching...')

            elif MicroLodge_E.decisions == [6, 1]: #* choice for Search Room if Nima quest is active
                MicroLodge_E.clear_decisions
                character_sheet[4]['Internal Notes']['Searched Micro Lodge'] = 'Yes'
                nima_search('Micro Lodge', 'Lck')               

            else:
                MicroLodge_E.clear_decisions
# End FINAL STATE MicroLodge_E
#******* End Micro Lodge *******

#!!!!!!!!!!!! Begin Myrum's Room: !!!!!!!!!!!!
    while room_location == "Myrum's Room":
        package_player_data()
        save_player_data()

# Begin 1st State MyrumRoom (UNEXAMINED):
        if MyrumRoom.examined == 'No':
            MyrumRoom.enter_room()

            if MyrumRoom.decisions == [4, 1]: # Door to MainHall
                MyrumRoom.clear_decisions
                room_location = 'Main Hall'
                battery_drain()

            elif MyrumRoom.decisions == [5, 1]: # Object Myrum's Cabinet - Myrum's Jar
                MyrumRoom.clear_decisions
                p_func.animate_strings(["You open up the cabinet and see Myrum's Jar on the first shelf. You unscrew the lid..."])
                whisp_chest(MyrumJar)

            else:
                MyrumRoom.clear_decisions           
# End 1st State MyrumRoom

# Begin FINAL STATE MyrumRoom_E (EXAMINED):
        elif MyrumRoom.examined == 'Yes':
            MyrumRoom.roomstate = 'inactive'
            MyrumRoom_E.enter_room()

            if MyrumRoom_E.decisions == [4, 1]: # Door to MainHall
                MyrumRoom_E.clear_decisions
                room_location = 'Main Hall'
                battery_drain()

            elif MyrumRoom_E.decisions == [5, 1]: # Object Myrum's Step-Stool --> Myrum's Cabinet --> Myrum's Jar
                MyrumRoom_E.clear_decisions
                p_func.animate_strings(["You open up the cabinet and see Myrum's Jar on the first shelf. You unscrew the lid..."])
                whisp_chest(MyrumJar)
                
            elif MyrumRoom_E.decisions == [5, 2]: # Object Myrum's Step-Stool --> Myrum's Bulletin Board --> Read Myrum's REMEMBER note
                MyrumRoom_E.clear_decisions
                p_func.animate_txt('myrum_bulletin_board', 'npc', .05, .1) #*Myrum Bulletin Board has code to West Wing
                input('<<<<<<---|--->>>>>>\n')

            else:
                MyrumRoom_E.clear_decisions
# End FINAL STATE MyrumRoom_E
#******* End Myrum's Room *******

#!!!!!!!!!!!! Begin PC Room: !!!!!!!!!!!!  
    while room_location == "PC Room":
        package_player_data()
        save_player_data()

# Begin 1st State PCRoom (Single State):
        if PCRoom.roomstate == 'active':
            PCRoom.enter_room()

            if PCRoom.decisions == [4, 1]: #* No battery drain for entering & exciting PC Room
                PCRoom.clear_decisions
                room_location = 'Micro Lodge'   

            elif PCRoom.decisions == [5, 1]: # Use object book of tips and tricks
                PCRoom.clear_decisions               
                p_func.print_txt('tips_for_bots', 'misc')
                input('<<<<<<---|--->>>>>>\n')

            elif PCRoom.decisions == [5, 2]: # Use object PlayerChest
                PCRoom.clear_decisions               
                whisp_chest(PlayerChest)
                if character_sheet[4]['Internal Notes']['Used MicroLodge Chest'] == 'No':
                    character_sheet[4]['Internal Notes']['Used MicroLodge Chest'] = 'Yes'
                    complete_quest(xp=100, quest_name=f"Enter {character_sheet[0]['Name']}'s Room & Use Chest") #* Use Player Chest Quest Completion

            elif PCRoom.decisions == [5, 3]: # Use object hibernation port
                PCRoom.clear_decisions                
                character_sheet[4]['Internal Notes']['Day'] += 1
                p_func.animate_strings(['Slowly...\nPeacefully...\nAll your sensors go offline.'], .05, .02)
                p_func.rand_char_gen(Path_misc_txt.joinpath('binary').resolve(), 3, .035, .07)           
                p_func.animate_txt('hibernation', 'art', .0015, .009)

                if character_sheet[4]['Internal Notes']['Used Hibernation Port'] == 'No':
                    p_func.rand_char_gen(Path_misc_txt.joinpath('binary').resolve(), 3, .02, .02)
                    p_func.animate_txt('boot_wakeup', 'art', .001, .007)
                    p_func.animate_strings(["Can robots feel well rested? I guess so...", ''])
                    character_sheet[4]['Internal Notes']['Used Hibernation Port'] = 'Yes'
                    complete_quest(xp=100, quest_name=f"Use {character_sheet[0]['Name']}'s Hibernation Port") #* Use Hibernation Port Quest Completion  

                else:
                    p_func.rand_char_gen(Path_misc_txt.joinpath('binary').resolve(), 3, .02, .02)
                    p_func.animate_txt('boot_wakeup', 'art', .001, .007)
                    p_func.animate_strings(["Suddenly all your internal sensors fire back up.\nAnother day, another virtual reality to conquer."], .05, .1)                        

            else:
                PCRoom.clear_decisions           
# End 1st State PCRoom (Single State)   
#******* End PC Room *******

#!!!!!!!!!!!! Receiving Office: !!!!!!!!!!!!  
    while room_location == 'Receiving Office':
        package_player_data()
        save_player_data()
        
# Begin Receiving Office QUEST & CONDITION CHECKS:
        myrum_package_tracker = character_sheet[4]['Internal Notes']['Myrum Package Tracker'] #* Myrum package check begins
        game_days_passed = character_sheet[4]['Internal Notes']['Day']

        if game_days_passed >= myrum_package_tracker and "Myrum's Order Form" in DockShopChest.items and DockShopChest.gold > 4:
            DockShopChest.items.remove("Myrum's Order Form")
            DockShopChest.gold -= 5
            RecOfficeChest.items.append("Myrum's Package")
# End Receiving Office QUEST & CONDITION CHECKS

# Begin 1st State RecOffice (UNEXAMINED, room is dark):
        elif RecOffice.examined == 'No':                        
            RecOffice.enter_room()

            if RecOffice.decisions == [4, 1]: # Door to DockShop
                RecOffice.clear_decisions
                room_location = 'Dock Shop'
                battery_drain()                    

            else:
                RecOffice.clear_decisions
# End 1st State RecOffice

# Begin 2nd State RecOffice_E (EXAMINED, discovered lightswitch)
        elif RecOffice.examined == 'Yes' and RecOffice.roomstate == 'active': #* Case for if player has discovered lightswitch for first time
            RecOffice.roomstate = 'inactive'
            RecOffice_E.enter_room()

            if RecOffice_E.decisions == [4, 1]: # Door to DockShop
                RecOffice_E.clear_decisions
                room_location = 'Dock Shop'
                battery_drain()

            elif RecOffice_E.decisions == [5, 1]: # Use object Lightswitch (CreepySlympto appears)
                RecOffice_E.clear_decisions
                RecOffice_E.roomstate = 'inactive' #* After turning on the light RecOffice_F becomes active
                p_func.speech_txt('slympto_creepy', 'npc') #* Creepy Slympto appears
                SlymptoCreepy.player_questions(goodbye_string2='continues milling around behind the counter, completely ignoring you.')
                p_func.speech_str_list(['He calmly walks past you, then heads out the door...', 'Creepy.'])

            else:
                RecOffice_E.clear_decisions

        elif RecOffice_E.roomstate == 'active' and RecOffice.roomstate == 'inactive': #* Case for if player did not turn on the lightswitch on first visit
            RecOffice_E.enter_room()

            if RecOffice_E.decisions == [4, 1]: # Door to DockShop
                RecOffice_E.clear_decisions
                room_location = 'Dock Shop'
                battery_drain()

            elif RecOffice_E.decisions == [5, 1]: # Use object Lightswitch (CreepySlympto appears)
                RecOffice_E.clear_decisions
                RecOffice_E.roomstate = 'inactive' #* After turning on the light RecOffice_F becomes active
                p_func.animate_txt('slympto_creepy', 'npc') #* Creepy Slympto appears
                SlymptoCreepy.player_questions(goodbye_string2='continues milling around behind the counter, completely ignoring you.')
                p_func.animate_strings(['He calmly walks past you, then heads out the door...', 'Creepy.'])

            else:
                RecOffice.clear_decisions
# End 2nd State RecOffice_E

# Begin FINAL STATE RecOffice_F (Player has already turned on lights and encountered CreepySlympto):
        elif RecOffice_F.roomstate == 'active' and RecOffice_E.roomstate == 'inactive':
            RecOffice_F.enter_room()

            if RecOffice_F.decisions == [4, 1]: # Door to DockShop
                RecOffice_F.clear_decisions
                room_location = 'Dock Shop'
                battery_drain()

            elif RecOffice_F.decisions == [5, 1]: # Use Object RecOfficeChest
                RecOffice_F.clear_decisions
                whisp_chest(RecOfficeChest)

            else:
                RecOffice_F.clear_decisions
# End FINAL STATE RecOffice_F
#******* End Receiving Office: *******

#!!!!!!!!!!!! Begin West Wing: !!!!!!!!!!!!
    while room_location == "West Wing":
        package_player_data()
        save_player_data()

# Begin 1st State WestWing (UNEXAMINED):
        if WestWing.examined == 'No':
            WestWing.enter_room()

            if WestWing.decisions == [4, 1]: # Door to MainHall
                WestWing.clear_decisions
                room_location = 'Main Hall'
                battery_drain()

            else:
                WestWing.clear_decisions
# End 1st State WestWing

# Begin FINAL STATE WestWing_E (EXAMINED):
        elif WestWing.examined == 'Yes':
            WestWing.roomstate = 'inactive'
            WestWing_E.enter_room()

            if WestWing_E.decisions == [4, 1]: # Door to MainHall
                WestWing_E.clear_decisions
                room_location = 'Main Hall'
                battery_drain()
                
            elif WestWing_E.decisions == [5, 1]: # Look at rug --> Lift up the corner of the rug
                WestWing_E.clear_decisions
                
                if 'Lost Earring' in character_sheet[3]['Inventory']['Items']:
                    p_func.animate_strings(["You don't see anything else under the rug."])
                    
                else:               
                    p_func.speech_str_list(['You see a large, hoop-shaped earring.', 'One of the crew must have dropped it.', 'You decide to pick it up and take it with you.', ''])
                    character_sheet[3]['Inventory']['Items'].append('Lost Earring')
                    accept_quest(quest_name='Lost Earring')
                
            else:
                WestWing_E.clear_decisions
# End FINAL STATE West Wing
#******* End West Wing *******
