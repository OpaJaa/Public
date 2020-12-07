"""
COMP.CS.100 GUI Accesscard.
By: OpaJaa

A project for the basic programming course at Tampere University. No prior
programming experience.

A program to manage access cards. The access cards are read from a file
containing their information in CSV-format and the doors are stored in a global
dictionary. The available doors and access cards are shown to the user in the
GUI window.

User can:
    - Check information from access cards.
        - First the user clicks the checkboxes of those cardholders whose
          information the user wants to get.
        - After that the user clicks the button "Kortin Tiedot".
        - Information is printed in the text box.
        - And if only ONE access card is chosen, the door and area codes where
          that card has access are checked.
    - Check who has access to a door.
        - First the user chooses ONE door and clicks its checkbutton.
        - Then the user clicks "Pääsy ovelle".
        - The information is printed to the text box and those access cards
          checkboxes are checked who have access to that door.
    - Add new doors to access cards.
        - First the user clicks the checkboxes of those cardholders whose
          cards the user wants to add more access rights.
        - The user can choose multiple cards.
        - Then the user clicks the checkboxes of the doors which the user
          wants to be added to chosen cards.
        - The user can choose multiple doors
        - Then the user clicks the button "Lisää kulkuoikeuksia".
        - The doors are added to those access cards.
    - Merge access cards.
        - First the user chooses TWO access cards to be merged.
        - Then the user clicks the button "Yhdistä kortteja".
        - Both of the cards are merged, so both cards get every access right
          the other card has.
    - Remove access codes from access cards
        - First the user chooses access cards to remove access codes from
        - Then the user chooses which door and/or area to remove.
        - After that the user clicks "Poista kulkuoikeuksia".
        - The selected codes are removed from the selected access cards.
    - Add a new access card.
        - First the user has to write the name and id of the card to be added
          in the entry fields provided.
        - Then the user clicks the button "Lisää kortti".
        - The card appears in the end of the list of cards and now the user
          can choose that card and add doors to it using the "Lisää
          kulkuoikeuksia" -button.
    - Remove a access card.
        - First the user has to choose the cards to be removed using the
          checkboxes.
        - Then the user clicks "Poista kortti".
        - The card(s) are removed.
    - Clear text from the text box.
        - The user can clear the text box by clicking the button "Tyhjennä"
            under the text box.
    - Clear selections
        - The user can clear selections from the doors and cards by clicking
        the button "Poista valinnat". The button next to the doors clears
        selected doors and the button under the cards clears selected cards.
    - Start from scratch
        - To start without any access cards the user can click "Tiedosto"
          from the menubar and then click "Uusi".
        - The access cards are removed and the user can add new cards using
          the methods described above.
    - Load a file containing access card info.
        - To open a file containing access card info the user clicks "Tiedosto"
          from the menubar and then "Avaa korttitiedosto".
        - A window will open where the user can choose a .txt -file.
        - The file must be in csv -format: id_number;name;access_codes
          where access codes are separated using ",".
        - If the file is in correct format, the access cards are added to the
          main window and all previus cards are removed.
    - Save the access cards in a .txt -file.
        - To save the user can click "Tiedosto" from the menubar and then
          "Tallenna korttitiedosto".
        - A window will open where the user is asked to name the file to be
          saved.
        - If the name allready exists there will be a popup asking if the user
          wants to replace the file.
        - The file is saved in the same csv -format and can be opened later.
    - Exit the programme.
        - To exit the programme the user can click the menubar "Tiedosto" and
        then from the menu click "Lopeta Ohjelma".
    - Read the user manual.
        - To read the manual, the user clicks "Apua" from the menubar and
          then "Käyttöohjeet".
        - A popup with very short user manual is shown.

    - If the user does something wrong, there will be a popup window telling
      what went wrong and what to do.

"""

# Import the GUI -library
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from tkinter.filedialog import askopenfile
from tkinter.filedialog import asksaveasfile

# A global dictionary containing all the door codes as keys and area codes as
# values. All doors don't have area codes.
DOORCODES = {'TC114': ['TIE'], 'TC203': ['TIE'], 'TC210': ['TIE', 'TST'],
             'TD201': ['TST'], 'TE111': [], 'TE113': [], 'TE115': [],
             'TE117': [], 'TE102': ['TIE'], 'TD203': ['TST'], 'TA666': ['X'],
             'TC103': ['TIE', 'OPET', 'SGN'], 'TC205': ['TIE', 'OPET', 'ELT'],
             'TB109': ['OPET', 'TST'], 'TB111': ['OPET', 'TST'],
             'TB103': ['OPET'], 'TB104': ['OPET'], 'TB205': ['G'],
             'SM111': [], 'SM112': [], 'SM113': [], 'SM114': [],
             'S1': ['OPET'], 'S2': ['OPET'], 'S3': ['OPET'], 'S4': ['OPET'],
             'K1705': ['OPET'], 'SB100': ['G'], 'SB202': ['G'],
             'SM220': ['ELT'], 'SM221': ['ELT'], 'SM222': ['ELT'],
             'TA': ['G'], 'TB': ['G'], 'SA': ['G'], 'KA': ['G']}


class Userinterface:
    """
    A class for the GUI part
    """

    def __init__(self):
        """
        The constructor
        """
        # The Tk() parent window is named as mainwindow
        self.__mainwindow = Tk()

        # The menubar is created
        menubar = Menu(self.__mainwindow)
        # The filemenu is created
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Uusi",
                             command=self.new_table)
        filemenu.add_command(label="Avaa korttitiedosto",
                             command=self.open_file)
        filemenu.add_command(label="Tallenna korttitiedosto",
                             command=self.save_file)
        # A separator in the menubar to separate the exiting of the program
        filemenu.add_separator()
        filemenu.add_command(label="Lopeta Ohjelma",
                             command=self.__mainwindow.quit)
        menubar.add_cascade(label="Tiedosto",
                            menu=filemenu)
        # The helpmenu is created in the menubar
        helpmenu = Menu(menubar,
                        tearoff=0)
        helpmenu.add_command(label="Käyttöohjeet",
                             command=self.read_me)
        menubar.add_cascade(label="Apua",
                            menu=helpmenu)
        self.__mainwindow.config(menu=menubar)

        # The main label is created
        self.__main_label = Label(self.__mainwindow,
                                  text="AVAINKORTTIENHALLINTAOHJELMA",
                                  font="Verdana 20 bold")

        # Label for the doors is created
        self.__door_label = Label(self.__mainwindow,
                                  text="Ovikoodit",
                                  font="Verdana 14 bold")
        # A dictionary that is used to store the values of the checkbuttons
        self.__selected_doors = {}
        # Two variables for placing the checkbuttons in right places
        d_row_counter = 3
        d_column_counter = 1
        # A loop to create the checkbuttons for the doors
        for door in DOORCODES:
            # The variable that tells if the button is checked. 1=check, 0=not
            d_var = IntVar()
            # The checkbutton is created using the doorcode and variable
            self.__doors = Checkbutton(self.__mainwindow,
                                       text=f"{door}",
                                       variable=d_var)
            # And the checkbutton is placed using grid. The variables are used
            # to place the button in the right place
            self.__doors.grid(row=d_row_counter,
                              column=d_column_counter,
                              sticky=W)
            # The checkbutton and its status are stored in the dictionary
            self.__selected_doors[door] = d_var
            # The counter raises by one
            d_row_counter += 1
            # And the column is changed if there are 7 doors in the column
            if d_row_counter == 10:
                d_column_counter += 1
                d_row_counter = 3

        self.__area_label = Label(self.__mainwindow,
                                  text="Aluekoodit",
                                  font="Verdana 14 bold")

        self.__selected_areacodes = {}
        a_row_counter = 12
        a_column_counter = 1
        self.__areacodes = []
        for door in DOORCODES:
            for area in DOORCODES[door]:
                self.__areacodes.append(area)
        self.__areacodes = set(self.__areacodes)
        for areacode in self.__areacodes:
            # The variable that tells if the button is checked. 1=check, 0=not
            a_var = IntVar()
            # The checkbutton is created using the doorcode and variable
            self.__areas = Checkbutton(self.__mainwindow,
                                       text=f"{areacode}",
                                       variable=a_var)
            # And the checkbutton is placed using grid. The variables are used
            # to place the button in the right place
            self.__areas.grid(row=a_row_counter,
                              column=a_column_counter,
                              sticky=W)
            # The checkbutton and its status are stored in the dictionary
            self.__selected_areacodes[areacode] = a_var
            # The counter raises by one
            a_row_counter += 1
            # And the column is changed if there are 7 doors in the column
            if a_row_counter == 14:
                a_column_counter += 1
                a_row_counter = 12

        # Label for the cards is created
        self.__card_label = Label(self.__mainwindow,
                                  text="Avainkortit",
                                  font="Verdana 14 bold")

        # Buttons are created for the different methods the user can use
        self.__button_labels = Label(self.__mainwindow,
                                     text="Toiminnot",
                                     font="Verdana 14 bold")
        self.__access_button = Button(self.__mainwindow,
                                      text="Kortin Tiedot",
                                      command=self.access_info)
        self.__has_access_button = Button(self.__mainwindow,
                                          text="Pääsy ovelle",
                                          command=self.who_has_access)
        self.__add_button = Button(self.__mainwindow,
                                   text="Lisää kulkuoikeuksia",
                                   command=self.add_doors)
        self.__clear_text_button = Button(self.__mainwindow,
                                          text="Tyhjennä",
                                          command=self.clear_text)
        self.__clear_selected_cards = Button(self.__mainwindow,
                                             text="Tyhjennä valinnat",
                                             command=self.clear_selected_cards)
        self.__clear_selected_doors = Button(self.__mainwindow,
                                             text="Tyhjennä valinnat",
                                             command=self.clear_selected_doors)
        self.__remove_doors_button = Button(self.__mainwindow,
                                            text="Poista kulkuoikeuksia",
                                            command=self.remove_doors)
        self.__merge_cards_button = Button(self.__mainwindow,
                                           text="Yhdistä kortteja",
                                           command=self.merge_cards)
        self.__add_new_card_button = Button(self.__mainwindow,
                                            text="Lisää kortti",
                                            command=self.add_card)
        self.__remove_card_button = Button(self.__mainwindow,
                                           text="Poista kortti",
                                           command=self.remove_card)

        # A text field where the information of chosen cards is printed
        self.__text_field = Text(self.__mainwindow, bd=2, relief=SUNKEN)

        # A label for entry box for the new users name
        self.__new_user_name_label = Label(self.__mainwindow,
                                           text="Uuden käyttäjän nimi")
        # A label for the entry box for the new users id
        self.__new_user_id_label = Label(self.__mainwindow,
                                         text="Uuden käyttäjän id-tunnus")
        # Entry box for the new users name
        self.__new_user_name_entry = Entry(self.__mainwindow)
        # Entry box for the new users id
        self.__new_user_id_entry = Entry(self.__mainwindow)

        # The elements of the userinterface are placed in the window using grid
        self.__main_label.grid(row=1, column=0, columnspan=5)
        self.__door_label.grid(row=2, column=1, sticky=W)
        self.__area_label.grid(row=11, column=1, sticky=W)
        self.__card_label.grid(row=15, sticky=W)
        self.__new_user_name_label.grid(row=17, sticky=W)
        self.__new_user_name_entry.grid(row=18, sticky=W)
        self.__new_user_id_label.grid(row=19, sticky=W)
        self.__new_user_id_entry.grid(row=20, sticky=W)
        self.__button_labels.grid(row=2, column=0, sticky=W)
        self.__access_button.grid(row=3, column=0, sticky=W)
        self.__has_access_button.grid(row=4, column=0, sticky=W)
        self.__add_button.grid(row=5, column=0, sticky=W)
        self.__merge_cards_button.grid(row=6, column=0, sticky=W)
        self.__remove_doors_button.grid(row=7, column=0, sticky=W)
        self.__add_new_card_button.grid(row=8, column=0, sticky=W)
        self.__remove_card_button.grid(row=9, column=0, sticky=W)
        self.__text_field.grid(row=15, column=1, rowspan=10, columnspan=4)
        self.__clear_text_button.grid(row=25, column=4)
        self.__clear_selected_cards.grid(row=16, column=0, sticky=W)
        self.__clear_selected_doors.grid(row=2, column=2, sticky=W)

        # Declaring the dictionary of access cards as global
        global ACCESSCARDS
        # Function call to read the file containing the access information and
        # storing the returned dictionary in a variable
        ACCESSCARDS = read_file("accessinfo.txt")

        # A list of the card checkbuttons
        self.__card_checkbox_list = []
        # A dictionary that is used to store the values of the checkbuttons
        self.__selected_cards = {}
        if ACCESSCARDS:
            # A method is called to loop through the access cards
            self.loop_for_cards()
        else:
            information = "Tiedostoa ei voitu lukea!"
            self.__text_field.insert(END, information)

    def start(self):
        """
        Starts the mainloop.
        """
        self.__mainwindow.mainloop()

    def quit(self):
        """
        Destroys the mainwindow so the program ends
        """
        self.__mainwindow.destroy()

    def loop_for_cards(self):
        """
        A method to create the checkbuttons for the access cards
        """

        # The text field is cleared
        self.clear_text()
        # First the list containing the checkbuttons is cleared
        for card in self.__card_checkbox_list:
            card.destroy()

        # A variable for the placement of the checkbuttons
        c_row_counter = 21

        # A loop to iterate through the dictionary containing the access cards
        for card in ACCESSCARDS:
            # The variable that tells if the button is checked. 1=check, 0=not
            c_var = IntVar()
            # The checkbutton is created using name from the card and variable
            self.__cards = Checkbutton(self.__mainwindow,
                                       text=f"{ACCESSCARDS[card].get_name()}",
                                       variable=c_var)
            # The checkbutton is placed in the window using counter variable
            self.__cards.grid(row=c_row_counter,
                              column=0,
                              sticky=W)
            # The checkbutton and its status are stored in a dictionary
            self.__selected_cards[card] = c_var
            # The checkbuttons are stored in a list
            self.__card_checkbox_list.append(self.__cards)
            # The counter value is raised by 1
            c_row_counter += 1

    def clear_text(self):
        """
        A method for clearing the text field
        """

        self.__text_field.delete(1.0, END)

    def clear_selected_cards(self):
        """
        A method for clearing checkbutton selections from access cards
        """
        # A loop to iterate through all the checkbuttons and their state
        for card in self.__selected_cards:
            # If the button is checked, the value is changed to 0 (unchecked)
            if self.__selected_cards[card].get() != 0:
                self.__selected_cards[card].set(0)

    def clear_selected_doors(self):
        """
        A method for clearing checkbutton selections from doors and areas
        """
        # A loop to iterate through all the door checkbuttons and their states
        for door in self.__selected_doors:
            # If the button is checked, the value is changed to 0 (unchecked)
            if self.__selected_doors[door].get() != 0:
                self.__selected_doors[door].set(0)
        # And a loop to do the same for the area checkbuttons
        for area in self.__selected_areacodes:
            # If the button is checked, the value is changed to 0 (unchecked)
            if self.__selected_areacodes[area].get() != 0:
                self.__selected_areacodes[area].set(0)

    def get_checked_cards(self):
        """
        A method to gather all checked cards from the dictionary
        """
        # A dictionary for storing the checked cards
        checked_cards = {}

        # A loop to iterate through all the checkbuttons
        for card in self.__selected_cards:
            # If the button is checked, it is added to the dictionary
            if self.__selected_cards[card].get() == 1:
                checked_cards[card] = 1

        # The dictionary containing all the checked buttons is returned
        return checked_cards

    def get_checked_doors(self):
        """
        A method to gather all checkded doors from the dictionary
        """
        # A dictionary for storing the checked doors
        checkded_doors = {}

        # A loop to iterate through all the checkbuttons
        for door in self.__selected_doors:
            # If the button is checked, it is added to the dictionary
            if self.__selected_doors[door].get() == 1:
                checkded_doors[door] = 1

        # The dictionary containing all the checked buttons is returned
        return checkded_doors

    def get_checked_areas(self):
        """
        A method to gather all checked area codes from the dictionary
        """
        # A dictionary for storing the checked doors
        checkded_areacodes = {}

        # A loop to iterate through all the checkbuttons
        for area in self.__selected_areacodes:
            # If the button is checked, it is added to the dictionary
            if self.__selected_areacodes[area].get() == 1:
                checkded_areacodes[area] = 1

        # The dictionary containing all the checked buttons is returned
        return checkded_areacodes

    def access_info(self):
        """
        A method for printing the information of chosen access cards to the
        text field. If only one card is chosen, the doors where the card has
        access will get their checkbuttons checked.
        """

        # The text field is cleared of any previous texts
        self.clear_text()

        # The door selections are cleared
        self.clear_selected_doors()

        # The method is called to get the chosen cards
        card_dict = self.get_checked_cards()

        # A variable to help the printing of the information
        info_list = []

        # A variable for error popup headline
        headline = "Virhe"
        # A variable for error popup information
        information1 = "Valitse vähintään yksi kortti!"

        # If there are no cards chosen, a method for error popup is called
        if len(card_dict) == 0:
            self.error_popup(headline, information1)

        # A loop for gathering the cards information from the card object dict
        else:
            for card in card_dict:
                if card in ACCESSCARDS:
                    # The card object is named
                    card_info = ACCESSCARDS[card]
                    # And the information is stored using a method from the
                    # Accesscard class
                    info_list.append(card_info.info())

            # A loop to join the information in the list to a string
            for info in info_list:
                output = ", ".join(info)
                # And the string is printed to the text field with two empty
                # lines after the text
                self.__text_field.insert(END, output)
                self.__text_field.insert(END, "\n")
                self.__text_field.insert(END, "\n")

        # And if only ONE card is chosen
        if len(card_dict) == 1:
            # The door selections are cleared
            self.clear_selected_doors()
            # And loops are used to activate the checkbuttons of the door and
            # area codes that the card has
            for card in card_dict:
                for door in self.__selected_doors:
                    if ACCESSCARDS[card].check_access(door):
                        self.__selected_doors[door].set(1)
                for area in self.__selected_areacodes:
                    if ACCESSCARDS[card].check_access(area):
                        self.__selected_areacodes[area].set(1)


    def add_doors(self):
        """
        A method to add access codes to access cards
        """
        # Two dictionaries to store the chosen doors and cards
        door_dict = self.get_checked_doors()
        area_dict = self.get_checked_areas()
        card_dict = self.get_checked_cards()

        # A variable for error popup headline
        headline = "Virhe"
        # Two variables for different information in the error popup
        information1 = "Valitse vähintään yksi kortti!"
        information2 = "Valitse vähintään yksi lisättävä ovi tai alue!"

        # If there are no chose cards, the error popup method is called
        if len(card_dict) == 0:
            self.error_popup(headline, information1)
            return
        # And the same for doors, with corresponding information
        elif len(door_dict) == 0:
            if len(area_dict) != 0:
                # A loop to iterate through the chosen cards
                for card in card_dict:
                    # And the corresponding card object is mined from the dict
                    card = ACCESSCARDS[card]
                    for area in area_dict:
                        card.add_access(area)
            else:
                self.error_popup(headline, information2)
                return

        else:
            # A loop to iterate through the chosen cards
            for card in card_dict:
                # And the corresponding card object is mined from the dict
                card = ACCESSCARDS[card]
                # A loop to add the chosen doors using a method
                if len(door_dict) != 0:
                    for door in door_dict:
                        card.add_access(door)
                    if len(area_dict) != 0:
                        for area in area_dict:
                            card.add_access(area)
                else:
                    for area in area_dict:
                        card.add_access(area)
        # Information in the text field is updated
        self.access_info()

    def remove_doors(self):
        """
        A method to remove access codes from access cards
        """

        # Two dictionaries to store the chosen doors and cards using methods
        door_dict = self.get_checked_doors()
        area_dict = self.get_checked_areas()
        card_dict = self.get_checked_cards()

        # A variable for error popup headline
        headline = "Virhe"
        # Two variables for different information in the error popup
        information1 = "Valitse vähintään yksi kortti!"
        information2 = "Valitse vähintään yksi poistettava ovi!"

        # If there are no chose cards, the error popup method is called
        if len(card_dict) == 0:
            self.error_popup(headline, information1)
            return
        # And the same for doors, with corresponding information
        elif len(door_dict) == 0:
            if len(area_dict) != 0:
                # A loop to iterate through the chosen cards
                for card in card_dict:
                    # And the corresponding card object is mined from the dict
                    card = ACCESSCARDS[card]
                    # A loop to remove the chosen areas using a method
                    for area in area_dict:
                        card.remove_access(area)
            else:
                self.error_popup(headline, information2)
                return

        else:
            # A loop to iterate through the chosen cards
            for card in card_dict:
                # And the corresponding card object is mined from the dict
                card = ACCESSCARDS[card]
                # A loop to remove the chosen doors using a method
                for door in door_dict:
                    card.remove_access(door)
                if len(area_dict) != 0:
                    for area in area_dict:
                        card.remove_access(area)

        # Information in the text field is updated
        self.access_info()

    def merge_cards(self):
        """
        A method to merge two access cards access codes together. Both cards
        will get every code from the other
        """

        # A dictionary to store the chosen cards using a method
        card_dict = self.get_checked_cards()
        # A list for the cards
        card_list = []

        # A variable for error popup headline
        headline = "Virhe"
        # A variable containing information to the error popup
        information = "Valitse KAKSI yhdistettävää korttia!"

        # A loop to store the cards to a list
        for key in card_dict:
            card_list.append(key)

        # If there are more or less cards than 2, error popup method is called
        if len(card_dict) != 2:
            self.error_popup(headline, information)
            return

        else:
            # The two cards in the list are assigned to variables
            card1 = card_list[0]
            card2 = card_list[1]
            # And the corresponding card objects are mined from the dict
            card1 = ACCESSCARDS[card1]
            card2 = ACCESSCARDS[card2]

            # And the cards are merged together using their methods
            card1.merge(card2)
            card2.merge(card1)

        # Information in the text field is updated
        self.access_info()

    def add_card(self):
        """
        A method to create a new access card with no access rights
        """

        # A variable for the error popup headline
        headline = "Virhe"
        # Two variables for different error information for the popup
        information1 = "Syötä nimi!"
        information2 = "Syötä id-numero!"

        # The entries from the entry boxes is stored in variables
        name = self.__new_user_name_entry.get()
        id_num = self.__new_user_id_entry.get()

        # If the name is empty, corresponding error popup is called
        if len(name) == 0:
            self.error_popup(headline, information1)
        # And the same for the id
        elif len(id_num) == 0:
            self.error_popup(headline, information2)

        else:
            # The new Accesscard object is created
            name = Accesscard(id_num, name)
            # And stored to the dict
            ACCESSCARDS[id_num] = name

            # The method for creating the card checkbuttons is used to refresh
            # the list of cards
            self.loop_for_cards()

            # And the entry fields are cleared
            self.__new_user_id_entry.delete(0, END)
            self.__new_user_name_entry.delete(0, END)

    def remove_card(self):
        """
        A method to remove access cards
        """

        # A dictionary to store the chosen cards using a method
        card_dict = self.get_checked_cards()

        # A variable for the error popup headline
        headline = "Virhe"
        # A variable for the information to the error popup
        information1 = "Valitse vähintään yksi poistettava kortti!"

        # there are no chosen cards, the error popup method is called
        if len(card_dict) == 0:
            self.error_popup(headline, information1)

        else:
            # A loop to go through the cards to be removed
            for card in card_dict:
                # If the card is in the dict of card objects, it is removed
                if card in ACCESSCARDS:
                    del ACCESSCARDS[card]
                    # And the method is called to refresh the card checkbuttons
                    self.loop_for_cards()

                # And the selections are cleared so they won't "haunt"
                self.clear_selected_cards()
                
    def who_has_access(self):
        """
        A method to print those cards to the text box who have access to
        selected door. The cards checkbuttons will also get checked.
        """
        # The text field is cleared of any previous texts
        self.clear_text()

        # The card checkbuttons are cleared
        self.clear_selected_cards()

        # A variable for the doors that are checked
        door_dict = self.get_checked_doors()

        # A variable to help the printing of the information
        info_list = []

        # A variable for error popup headline
        headline = "Virhe"
        # A variable for error popup information
        information1 = "Valitse YKSI ovikoodi!"

        # A variable to use, if there are no cards with access to the door
        no_cards = "Kenelläkään ei ole pääsyä tälle ovelle."

        # If there are no doors chosen, a method for error popup is called
        if len(door_dict) != 1:
            self.error_popup(headline, information1)
        else:
            # A loop to gather the cards information who have access
            for door in door_dict:
                for card in ACCESSCARDS:
                    if ACCESSCARDS[card].check_access(door):
                        card_info = ACCESSCARDS[card]
                        # And the information is stored using a method from the
                        # Accesscard class
                        info_list.append(card_info.info())
                        # And the checkbuttons of those cards are activated
                        self.__selected_cards[card].set(1)
            # If no one has access, a text is shown
            if not info_list:
                self.__text_field.insert(END, no_cards)
            # And if someone has access, all this happens
            else:
                # A loop to join the information in the list to a string
                for info in info_list:
                    output = ", ".join(info)
                    # And the string is printed to the text field with two
                    # empty lines after the text
                    self.__text_field.insert(END, output)
                    self.__text_field.insert(END, "\n")
                    self.__text_field.insert(END, "\n")

    def error_popup(self, headline, information):
        """
        A method to display error popup windows
        :param headline: str, the headline of the popup
        :param information: str, the information about the error. Used to guide
        the user to correct the thing that caused the error
        """

        # A popup command is used to create the popup with the information
        messagebox.showwarning(headline, information)

    def open_file(self):
        """
        A method for opening and reading a text file containing access card
        information.
        """

        # A variable for the file. Uses askopenfile to create a window
        # where the user chooses which file is to be opened. Only .txt
        # files are allowed
        file = askopenfile(mode="r", filetypes=[("Text files", "*.txt")])

        # If the file is opened (user does not click "Cancel")
        if file is not None:
            # File contents are read using the function and stored in a
            # variable
            content = read_file(file.name)
            # The previous dict containing all the access card objects is
            # cleared
            ACCESSCARDS.clear()

            # And the new cards are stored in the dict
            for card in content:
                ACCESSCARDS[card] = content[card]

        # And the card checkbuttons are looped
        self.loop_for_cards()

    def save_file(self):
        """
        A method to save the access cards to a .txt file in csv -format
        """

        # A variable for the file. Uses asksaveasfile to create a window
        # where the user can choose the location and name for the file
        saved_file = asksaveasfile(mode="w",
                                   filetypes=[("Text files", "*.txt")])

        # Variables for the information to be saved
        id_number = ""
        name = ""
        access = []

        # If the user does not click cancel
        if saved_file is not None:
            # A loop is used to iterate through the dict of access card objects
            for card in ACCESSCARDS:
                # The information is stored to variables
                id_number = str(card)
                name = ACCESSCARDS[card].get_name()
                access = ACCESSCARDS[card].get_access_list()
                # The access list is joined together with "," separating
                # different access codes
                access_string = ",".join(access)

                # And the information is written to the saved file in correct
                # manner and order
                saved_file.write(f"{id_number};{name};{access_string}\n")

            # When everything is saved, the file is closed
            saved_file.close()

    def new_table(self):
        """
        A method to clear the dict of access card objects to allow the user
        to create their own access cards from scratch
        """

        # The dictionary is cleared completely using clear() method
        ACCESSCARDS.clear()
        # The access card loop is called to refresh the list so that the
        # removed cards are removed from the window
        self.loop_for_cards()

    def read_me(self):
        """
        A method to show the user manual in a popup window
        :return:
        """
        try:
            # A variable where all the information from the file is stored
            read_me_file = open("readme.txt", "r")
            # The information is then read as a string to a file
            information = read_me_file.read()
            # And everything is printed to a popup window
            messagebox.showinfo("Käyttöohjeet", information)

        # If there is an error in reading the file, the error popup method is
        # used to tell about it
        except Exception:
            Headline = "Virhe"
            Information = "Tiedostoa ei voitu lukea!"
            self.error_popup(Headline, Information)


class Accesscard:
    """
    This class models an access card
    """

    def __init__(self, id, name, access=[]):
        """
        Constructor, creates a new card object that has no access rights.

        :param id: str, card holders personal id
        :param name: str, card holders name
        :param access: list, list of access rights. Empty by default
        """

        self.__id = id
        self.__name = name
        self.__access = access

    def info(self):
        """
        Method for storing the information of the access card to a list
        for printing
        """

        # A list to help in printing
        printlist = []

        # A loop for iterating through all the access rights of the object
        # and adding them in a list
        for code in self.__access:
            printlist.append(code)

        # The list is sorted
        printlist.sort()
        printlist.insert(0, self.__name)
        printlist.insert(0, self.__id)
        # And joined together as a string
        printstring = ", ".join(printlist)
        printlist = printstring.split(",")

        # And the returned to be used
        return printlist

    def get_name(self):
        """
        Method to get the objects name for use outside the object.
        :return: Returns the name of the access card holder.
        """

        return self.__name

    def add_access(self, new_access_code):
        """
        Method to add a new access code into the card.

        :param new_access_code: str, the access code to be added in the card.
        """

        # First a list to help managing all the access codes
        combined_list = []

        # A loop to add all the access codes already in the card to the list
        for key in self.__access:
            combined_list.append(key)
        # And then the new access code id added
        combined_list.append(new_access_code)
        # The list is made to a set to remove duplicates easily
        combined_list = set(combined_list)

        # A list for codes to be removed
        remove_list = []
        # A loop to iterate through the combined list
        for value in combined_list:
            # If the code is a door code
            if value in DOORCODES:
                # Then a loop to check all the area codes for that door
                for area_codes in DOORCODES[value]:
                    # And if there is a area code for that door in the list,
                    # the door code is added to the remove list
                    if area_codes in combined_list:
                        remove_list.append(value)

        # And a loop to remove all the values in the remove list from
        # the combined list
        for value in remove_list:
            if value in combined_list:
                combined_list.remove(value)

        # And finally the cards access codes are updated with the new codes
        self.__access = combined_list

    def check_access(self, door):
        """
        Method to check if the access card has a access to a provided door.
        Returns a boolean value accordingly.

        :param door: str, the door code of the door that is being accessed.
        :return: True: The door opens for this access card.
                 False: The door does not open for this access card.
        """

        # A list to store area codes
        area = []

        # DOORCODES[door] contains the area codes, so if there are any, they
        # are stored to the list
        if door in DOORCODES:
            area = DOORCODES[door]

        # Checks if the door is in the access rights of the card
        if door in self.__access:
            return True
        # Checks if the area code of the door is in the access rights
        for code in area:
            if code in self.__access:
                return True
        # And if there are no access rights for the door, returns False
        else:
            return False

    def merge(self, card):
        """
        Method for merging the access codes from another card to this card.

        :param card: Accesscard, the card object whose access rights are added
        to this card.
        """

        # A loop to iterate through the access rights in the card whose
        # rights are to be added to this card
        for card_key in card.__access:
            # The rights are added through the add_access -method
            self.add_access(card_key)

    def remove_access(self, door):
        """
        Method for removing access code from the card.

        :param door: the access code to be removed
        """

        # First a list to help managing all the access codes
        combined_list = []

        # A loop to add all the access codes already in the card to the list
        for key in self.__access:
            combined_list.append(key)

        # If the door to be removed is in the list, it is removed
        if door in combined_list:
            combined_list.remove(door)

        # And finally the cards access codes are updated
        self.__access = combined_list

    def get_access_list(self):
        """

        :return:
        """

        access_list = []

        for key in self.__access:
            access_list.append(key)

        return access_list


def print_list(obj_dict):
    """
    Method to print out all the access cards in a neat and tidy manner
    """

    # A loop to iterate through a sorted dictionary of the access card objects
    for key in sorted(obj_dict):
        # And a method is called to print the information
        obj_dict[key].info()


def read_file(filename):
    """
    Reads the file containing information about access cards and their
    information. Creates objects of class Accesscard containing that
    information and stores those objects in a dictionary.
    :return: dict, a dictionary of card objects
    """

    # "Helper" variables are created here before assigning stuff into them
    # They are placed here so they are empty for every round of the loops
    access = ""
    access_list = []
    obj_dict = {}

    # Exception for the opening of the file containing all the information
    try:
        # A variable where the information from the file is stored
        access_file = open(filename, "r")
        # A variable for a single line from the file
        file_line = access_file.readline()
        # A loop to manage the data in the line, if the line is empty,
        # the loop ends
        while file_line != "":

            # Remove the "\n" from the end of the line
            file_line = file_line.rstrip()

            # The information is separated to different elements and added to
            # a list
            info_list = file_line.split(";")

            # The different elements are assigned into variables named after
            # the information they are containing
            id_num = info_list[0]
            name = info_list[1]
            access = info_list[2]

            # The access -variable is split into a list (there may be numerous
            # access codes in it)
            access_list = access.split(",")

            # The information is used to create a new Accescard -object
            name = Accesscard(id_num, name)
            # Then the access codes are stored using a method
            for code in access_list:
                name.add_access(code)
            # And the object is stored in a dictionary
            obj_dict[id_num] = name

            # The next line is read and the loop continues
            file_line = access_file.readline()

        # The file is closed after all the information is stored
        access_file.close()

    # If there is any kind of problems reading the file, an error is raised
    except Exception:
        return {}
    # The created dictionary is returned
    return obj_dict


def main():

    # Create an object of the class Userinterface
    ui = Userinterface()
    # Starts the GUI
    ui.start()


if __name__ == "__main__":
    main()
