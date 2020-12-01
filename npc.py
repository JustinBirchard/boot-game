# npc.py
"""Class NPC for player interactions with NPCs"""

from ast import literal_eval
from room import Room
import p_func

class NPC:
    """Class NPC for player interactions with NPCs"""

    def __init__(self, name, quick_desc, qa_set_one, qa_set_two=[], 
                qa_set_three=[], avlbl_quest=None, npc_items=None, 
                actvquest=[], compltdquest=[], asked=[]):
        self.name = name
        self.quick_desc = quick_desc
        self.qa_set_one = qa_set_one
        self.qa_set_two = qa_set_two if qa_set_two is not [] else []
        self.qa_set_three = qa_set_three if qa_set_three is not [] else []
        self.avlbl_quest = avlbl_quest if avlbl_quest is not None else None
        self.npc_items = npc_items if npc_items is not None else None
        self._actvquest = actvquest if actvquest is [] else []
        self._compltdquest = compltdquest if compltdquest is [] else []
        self._asked = asked if asked is [] else []

## NEW __str__ def 8-30-20:
    def __str__(self):                
        return (f'You approach {self.name}, a {self.quick_desc[0]}\n{self.quick_desc[1]}\n') 

    @property
    def asked(self):
        """return contents of the self._asked list"""
        return self._asked

    @property
    def available_quest(self):
        """Returns NPC's available quests"""
        return self.avlbl_quest

    @property
    def accept_quest(self):
        """Cuts contents of self.avlbl_quest and pastes into self._actvquest"""
        accepted = self.avlbl_quest
        self._actvquest.append(accepted)
        self.avlbl_quest='None'

    @property
    def active_quest(self):
        """Returns player's currently active quest for this NPC"""
        return self._actvquest

    @property
    def complete_quest(self):
        """Cuts contents of self.actvquest & pastes into self._compltdquest"""
        completed = self._actvquest
        self._compltdquest[:] = completed
        self._actvquest=[]

    @property
    def compltdquest(self):
        """Returns completed quest"""
        return self._compltdquest

## 9-8-20 Added else clause to help in my quest for better NPC interactions
    def adv_qa_sets(self, qa_set):
        """Enables the next set of NPC Q&A.
        qa_set should be 2 to advance qa_set_two into qa_set_one
        qa_set should be 3 to advance qa_set_three into qa_set_one
        """
        if qa_set == 2:
            self.qa_set_one += self.qa_set_two
            self.qa_set_two=[]

        elif qa_set == 3:
            self.qa_set_one += self.qa_set_three
            self.qa_set_three=[]

        else:
            print('Looks like they have nothing left to say to you.')

## Massive updates 9/8 & 9/9, finally working they way I want! (I think)
    def player_questions(self, goodbye_string1='returns to what it was doing.', 
                         goodbye_string2="is focused on something else at the moment, maybe try later."):
                         
        """Presents player with questions to ask NPCs. Note that function can only handle 5 total questions at a time.
           If more than 5 questions are available the function will stall and program will break.

        Args:
            goodbye_string1 (str, optional): Dialouge for when NPC has run out of questions in set one. 
            Defaults to 'returns to what it was doing.'.
            goodbye_string2 (str, option): Dialouge for when NPC has run out of dialouge in all qa sets.
            Defaults to "is focused on something else at the moment, maybe try later".
        """

        function_status = 'Active'
        choice_loop = 'Detecting Status'

        while function_status == 'Active':
            choice_loop = 'Detecting Status'

            while choice_loop == 'Detecting Status': # Resets questions & answers lists and checks for current conditions.
                questions = [] # questions from qa_set_one will be added to this list when player asks
                answers = [] # answers from qa_set_one will be added to this list when NPC replies

                if self.qa_set_one == [] and self.qa_set_two == [] and self.qa_set_three == []: # if all 3 q&a sets are empty player is sent back to main Room options
                    p_func.speech_str(f"{self.name} {goodbye_string2}")
                    choice_loop = 'Completed'
                    function_status = 'Completed'

                elif self.qa_set_one == []: #* when qa_set_one is empty the player is sent back to main Room options. 
                                            #* Note: to reload qa_set_one use adv_qa_sets() in boot.py
                    p_func.speech_str(f'{self.name} {goodbye_string1}')
                    choice_loop = 'Completed'
                    function_status = 'Completed'

                else:
                    choice_loop = 'Print Options'

            while choice_loop == 'Print Options': # Heart of the function where player chooses from dialogue options
                print('What do you want to do?')
                print('0: Go back to room options')
                print(f'1: Look at {self.name}')
                for question, answer in self.qa_set_one: # unpacking the tuples in qa_set_one
                    questions.append(question) # appending unpacked question to questions list
                    answers.append(answer) # appending unpacked answer to answers list
                for i, question in zip([i for i in range(len(questions))], questions): # Printing indexed list of questions that player can ask     
                    print(f'{i + 2}: Say- {question}')
                print('')
                choice_loop = 'Player Input'

            while choice_loop == 'Player Input':

                try: # Player chooses from indexed list of questions. Error handling in place.
                    player_choice = int(input('Enter your choice: '))
                    print('')
                    if player_choice == '':
                        raise ValueError

                    elif player_choice > len(self.qa_set_one) + 1:
                        raise ValueError

                except ValueError:
                    print('You must choose from the options above.')

                else:
                    choice_loop = 'Results'

            while choice_loop == 'Results': # Providing player with printed answers, adjusting NPC data, and setting while loop variables accordingly

                if player_choice == 0: # option to go back to Room options
                    function_status = 'Completed'
                    choice_loop = 'Completed'
                    print('')

                elif player_choice == 1: # option to look at NPC
                    for string in self.quick_desc:
                        p_func.animate_strings([string])
                    choice_loop = 'Detecting Status' # Sends back up to 'Detecting Status' While loop
                    print('') 
                    
                elif player_choice == 2:
                    p_func.speech_str(f'{answers[0]}') # printing NPC answer for player
                    self._asked += self.qa_set_one[0:1] # adding tuple of strings to the NPC._asked attribute so that it can be referenced later in boot.py
                    self.qa_set_one[0:1] = [] # deleting appropriate tuple of strings from qa_set_one
                    choice_loop = 'Detecting Status' # Sends back up to 'Detecting Status' While loop

                elif player_choice == 3:
                    p_func.speech_str(f'{answers[1]}')
                    self._asked += self.qa_set_one[1:2]
                    self.qa_set_one[1:2] = []
                    choice_loop = 'Detecting Status'

                elif player_choice == 4:
                    p_func.speech_str(f'{answers[2]}')
                    self._asked += self.qa_set_one[2:3]
                    self.qa_set_one[2:3] = []
                    choice_loop = 'Detecting Status'

                elif player_choice == 5:
                    p_func.speech_str(f'{answers[3]}')
                    self._asked += self.qa_set_one[3:4]
                    self.qa_set_one[3:4] = []
                    choice_loop = 'Detecting Status'

                elif player_choice == 6:
                    p_func.speech_str(f'{answers[4]}')
                    self._asked += self.qa_set_one[4:5]
                    self.qa_set_one[4:5] = []
                    choice_loop = 'Detecting Status'