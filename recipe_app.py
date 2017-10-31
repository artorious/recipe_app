#!/usr/bin/env python3
'''A simple menu-driven recipe database program

Program features:
    * Store recipes for later retrival.
    * Search function allowing users to search by;
        + Recipe title,
        + Author,
        + Ingredients.
    * Create new recipe entries.
    * Delete recipes
    * Print out recipes

NOTE:
    Data stored in Database File: recipe_app.db

'''

__AUTHOR__ = 'Arthur Ngondo'

import apsw         # SQLite3 Wrapper
import string       # 
import webbrowser   # For printing on a web-browser

class CookBook(object):
    '''Class holds recipe_app database routines.'''
    
    def __init__(self):
        '''Initialization function.
        Sets up attributes and global variables'''
        
        global connection   # Accessible from anywhere within the class
        global cursor       # Accessible from anywhere within the class
        
        self.totalcount = 0     # Count the number of recipes
        # Connection and cursor to the Database
        connection = apsw.Connection('recipe_app.db')
        cursor = connection.cursor()
    
    def database_menu():
        '''A loop that displays a list of options that the user 
        can perform'''
        
        cbk = CookBook() # Initialize the class

        loop = True # Controls program temination
        
        while loop == True:
            print('=' * 80)
            print(format(' RECIPE DATABASE ', '=^80'))
            print('=' * 80)
            # prompts that the user can perform
            print('\t 1 - Show all recipes')
            print('\t 2 - Search for a recipe')
            print('\t 3 - Show a recipe')
            print('\t 4 - Delete a recipe')
            print('\t 5 - Add a recipe')
            print('\t 6 - Print a recipe')
            print('\t 0 - Exit')
            print('=' * 80)
            # Wait for user input
            menu_selection = input('Enter a selection [0-6]: ')

            # Handle user's option
            if menu_selection == '1': # Show all
                cbk.print_all_recipes() 
            
            elif menu_selection == '2': # Search
                pass
            
            elif menu_selection == '3': # Show a Single Recipe
                cbk.print_all_recipes()
            
            elif menu_selection == '4': # Delete
                pass
            
            elif menu_selection == '5': # Add
                pass
            
            elif menu_selection == '6': # Print
                cbk.print_all_recipes()
            
            elif menu_selection == '0': # Exit
                print(format(' Good-Bye ', '*^80'))
                loop = False # Terminate program
            
            else:
                print(format(' UNRECOGNIZED COMMAND ', '*^80'))
                print('{0} is NOT a valid menu selection.'.format(menu_selection))
                print(format(' Try Again ', '-^80'))


    def print_all_recipes(self):
        '''Prints all Recipes in the recipe_app database.
        
        Displays all the information out of the Recipes data table
        in the  database.
        '''
        # "pretty-print" Header for recipe list. 
        print('{0:5s} {1:35s} {2:10s} {3:20s}'.format('Item', 'Name', 'Serves', \
                'Source'))  
        # query database and display results from tuple returned by APSW
        sql = 'SELECT * FROM Recipes' 
        cntr = 0 # counts the number of recipes we display to the user
        for table_row in cursor.execute(sql):
            cntr += 1
            # Use pkid  as Item to allow for correct recipe selection from Recipe Table.      
            print('{0:5s} {1:35s} {2:10s} {3:20s}'.format(str(table_row[0]), \
                str(table_row[1]) , str(table_row[2]), str(table_row[3])))

            print('-' * 80)
            self.totalcount = cntr
        print('=' * 80)   
        print('Total Recipes - {0}'.format(self.totalcount))
        print('=' * 80)
        inkey = input('press any key to continue')

    def search_for_recipe(self):
        '''Allows a database search for a recipe'''
        pass
    
    def print_single_recipe(self, which):
        '''Takes one argument which (the recipe).

        Displays the data for a single recipe from all three tables in 
        the database (|Recipes|Ingredients|Instructions|)
        '''
        pass

    def delete_recipe(self, which):
        '''Takes one argument which (the recipe).

        Deletes the recipe and all it's info from the database
        '''
        pass
    
    def add_new_recipe(self):
        '''Adds a new recipe entry into the recipe_app database'''
        pass
    
    def print_out_recipe(self, which):
        '''Takes one argument which (the recipe).

        Prints out the recipe to default printer.
        '''
        pass

if __name__ == '__main__':
    CookBook.database_menu()