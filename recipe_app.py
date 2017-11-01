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
import webbrowser   # For printing on a web-browser

class CookBook(object):
    '''Class holds recipe_app database routines.'''

    def __init__(self):
        '''Initialization function.
        Sets up attributes and global variables
        '''
        global connection   # Accessible from anywhere within the class
        global cursor       # Accessible from anywhere within the class
        
        self.totalcount = 0     # Count the number of recipes
        # Connection and cursor to the Database
        connection = apsw.Connection('recipe_app.db')
        cursor = connection.cursor()
    
    def database_menu():
        '''A loop that displays a list of options that the user 
        can perform'''
        cbk = CookBook() # Init
        loop = True # Controls program temination
        
        while loop == True:
            print(format(' RECIPE DATABASE ', '=^80'))
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
                cbk.search_for_recipe()
            
            elif menu_selection == '3': # Show a Single Recipe
                cbk.print_all_recipes() # list the recipes by pkid
                try:
                    recipe_selection = int(input('Enter recipe number or 0 to go back : '))
                    if recipe_selection <= cbk.totalcount: 
                        cbk.print_single_recipe(recipe_selection) # call with pkid
                    elif recipe_selection == 0:
                        print('Back to main menu')
                    else:
                        print('Unrecognized Command...Returnnig to menu')
                except ValueError:
                    print('Sorry.... NOT a valid recipe NUMBER..')

            elif menu_selection == '4': # Delete
                cbk.print_all_recipes() # Display items by pkid
                print('0 - Return To Menu')
                try:
                    record_to_del = int(input(
                        'Enter Recipe No. to DELETE or 0 to EXIT -> '))
                    if record_to_del != 0:
                        cbk.delete_recipe(record_to_del) # call with pkid
                    elif record_to_del == '0':
                        print('Back to main menu.....')
                    else:
                        print('Unrecognized Command. Returning to Menu')
                except ValueError:
                    print('Not a number...back to menu..')
            
            elif menu_selection == '5': # Add
                cbk.add_new_recipe()
            
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
        '''
        Prints all Recipes in the recipe_app database.
        Displays all the information out of the Recipes data table
        in the  database.
        '''
        # "pretty-print" Header for recipe list. 
        print('~' * 80 )
        print('{0:5s} {1:35s} {2:10s} {3:20s}'.format('Item', 'Name', 'Serves', \
                'Source')) 
        print('~' * 80 )
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
        inkey = input('press any key to continue >>') # pause

    def search_for_recipe(self):         
        '''Allows a database search for a recipe'''
        # Print the search menu
        print('-' * 80)
        print(format(' Search Type ', '-^70'))
        print('-' * 80)
        print('\t 1 - Recipe Name - a word in the recipe name')
        print('\t 2 - Recipe Source - a word in the recipe source')
        print('\t 3 - Ingredients - a word in the ingredients list')
        print('\t 0 - Return to main menu')
        print('-' * 80)
        print('Enter [1 - 3] to select search Type')

        search_type =  input('Enter Search Type -> ')

        if search_type in ['1', '2', '3']:

            if search_type == '1':
                search_in = 'Recipe Name'
            
            elif search_type == '2':
                search_in = 'Recipe Source'
            
            elif search_type == '3':
                search_in = 'Ingredients'
            
            search = search_type
            search_item = input('Search for what in {} (blank to exit) -> '
                .format(search_in))
            
            if search == '1': # Recipe Name
                sql = "SELECT pkid,name,source,servings FROM Recipes WHERE name like \
                    '%%{0}%%'".format(search_item)
            
            elif search == '2': # Recipe Source
                sql = "SELECT pkid,name,source,servings FROM Recipes WHERE source like \
                    '%%{0}%%'".format(search_item)
            
            elif search == '3': # Ingredients
                sql = "SELECT r.pkid,r.name,r.servings,r.source,\
                    i.ingredients FROM Recipes r Left Join ingredients i on \
                    (r.pkid = i.recipeID) WHERE i.ingredients like '%%{0}%%' \
                    GROUP BY r.pkid".format(search_item)
            try:
                if search == '3':
                    print('{0:5s} {1:35s} {2:10s} {3:15s} {4:55s}'.format(
                        'Item', 'Name', 'Serves', 'Source', 'Ingredients'))
                    print('-' * 120)

                else:
                    print('{0:5s} {1:35s} {2:10s} {3:20}'.format('Item', 
                        'Name', 'Serves', 'Source'))
                    print('-' * 80)
            

                for record in cursor.execute(sql):
                    if search == '3':
                        print('{0:5s} {1:35s} {2:10s} {3:15s} {4:55s}'.format(
                            str(record[0]), str(record[1]), str(record[2]), 
                            str(record[3]), str(record[4])))
                        print('-' * 80)
                        # inkey = input('press any key to continue') # Pause
                    elif search == '2' or search == '1':
                        print('{0:5s} {1:35s} {2:10s} {3:20s} '.format(
                            str(record[0]), str(record[1]), str(record[3]), 
                            str(record[2])))
                        print('-' * 80)
                        # inkey = input('press any key to continue') # Pause

            except NameError:
                print('A Search Error occured')
                print('-' * 80)
                inkey = input('press any key to continue') # Pause
        elif search_type == '0':
            print('Retruning to Menu')
        else:
            print('INVALID entry -> {0} ....... Returning to main menu'.format(search_type))

    def print_single_recipe(self, which):
        '''
        Takes one argument which (the recipe by pkid).
        Displays the data for a single recipe from all three tables in 
        the database (|Recipes|Ingredients|Instructions|)
        '''
        sql = 'SELECT * FROM Recipes WHERE pkid={0}'.format(which) 
        print('*' * 80)
        for record in cursor.execute(sql):# Query for gross recipe info by pkid
            recipeID = record[0]
            print("Title: {0} ".format(record[1]))
            print('~' * 6)
            print("Serves: {0} ".format(record[2]))
            print('~' * 7)
            print("Source: {0} ".format(record[3]))
            print('~' * 7)

        sql = 'SELECT * FROM Ingredients WHERE recipeID={0}'.format(recipeID) 
        print('\nIngredients List:')
        print('~' * 18)
        for record in cursor.execute(sql):# Query for Ingredients info by pkid
            print(record[2])
        
        print('\nInstructions:')
        print('~' * 14)
        sql = 'SELECT * FROM Instructions WHERE recipeID={0}'.format(recipeID)
       
        for record in cursor.execute(sql): # Query for Instructions info by pkid
            print(record[2])
        print('~' * 120)
        inkey = input('press any key to continue >>') # pause

    def delete_recipe(self, which):
        '''
        Takes one argument which (the recipe).
        Deletes the recipe and all it's info from the database
        '''
        resp = input('Are you sure you want to delete this record? (Y/n) -> ')
        if resp.upper() == 'Y': 
            # Delete Recipe records
            sql = 'DELETE FROM Recipes WHERE pkID = {}'.format(str(which))
            cursor.execute(sql)
            sql = 'DELETE FROM Instructions WHERE recipeID = {}'.format(str(which))
            cursor.execute(sql)
            sql = 'DELETE FROM Ingredients WHERE recipeID = {}'.format(str(which))
            cursor.execute(sql)
            print("\nRecipe information DELETED...")
            print('~' * 80)
            inkey = input('Press Enter to return to Main menu -> ')
        else:
            print('~' * 80)
            print('Delete Aborted.. - Returning to Menu')
            print('~' * 80)
    
    def add_new_recipe(self):
        '''
        Adds a new recipe entry into the recipe_app database
        '''
        # Init vars
        ingredients_list = [] 
        recipe_name = ''
        recipe_source = ''
        recipe_serves = ''
        instructions = ''
        last_pkid = 0
        # Prompt user for Recipe Title, Source & Servings. Escape apstrophes in user input
        resp = input('Enter Recipe Title (Leave Blank to exit) -> ')
        if resp != '':
            
            if "'" in resp: 
                recipe_name = resp.replace("'", "\'")
            else:
                recipe_name = resp
            print("RecipeName will be {}.".format(recipe_name))

            resp = input('Enter Recipe Source -> ')              
            if "'" in resp:
                recipe_source = resp.replace("'", "\'")
            else:
                recipe_source = resp

            resp = input('Enter Number of Servings -> ')
            if "'" in resp:
                recipe_serves = resp.replace("'", "\'")
            else:
                recipe_serves = resp
            
            print('Enter Ingredients List')

            ingredients_loop = True # Controls input of ingredients
            # ask for each ingredient, appending to ingredients_list while escaping apostrophes
            while ingredients_loop == True: # enter loop
                list_item = input('Enter an Ingredient. (0 to finish) -> ')
                if list_item != '0':
                    if "'" in list_item:
                        ingredients_list.append(list_item.replace("'", "\'"))
                    else:
                        ingredients_list.append(list_item)
                else:
                    ingredients_loop = False # exit the loop when finished
            
            # Prompt user for Instructions
            resp = input('Enter Instructions -> ')
            if "'" in resp:
                instructions = resp.replace("'", "\'")
            else:
                instructions = resp
            # Display progress before promting SAVE
            print('~' * 80)
            print("Here's what we have so far..")
            print("Title: {}".format(recipe_name))
            print("Source: {}".format(recipe_source))
            print("Servings: {}".format(recipe_serves))
            print("Ingredients")
            for item in ingredients_list:
                print(item)
            print("Instrcutions: {}".format(instructions))
            print('~' * 70)

            # Prompt SAVE option
            resp = input("OK to save? (Y/n) -> ")
            
            if resp.upper() != 'N': # Connect to Database
                connection=apsw.Connection('recipe_app.db')
                cursor=connection.cursor()
            
                # Write the Recipe record to the Database
                sql = 'INSERT INTO Recipes (name,servings,source) \
                        VALUES ("{0}","{1}","{2}")'.format(
                        recipe_name, recipe_serves, recipe_source)
                cursor.execute(sql)

                # Query for Recipe pkid
                sql = "SELECT last_insert_rowid()"
                cursor.execute(sql)

                for item in cursor.execute(sql):
                    last_pkid = item[0] # update pkid for linking other tables as foreign key
                    print("Last Primary Key = {}".format(last_pkid))
                
                # Write the Ingredients Record with appropriate foreign key
                for list_item in ingredients_list:
                    sql = 'INSERT INTO Ingredients (recipeID, ingredients) \
                            VALUES ({0}, "{1}")'.format(last_pkid, list_item)
                    cursor.execute(sql)

                # Write the Instructions record
                sql = 'INSERT INTO Instructions (recipeID, instructions) \
                            VALUES ({0}, "{1}")'.format(last_pkid, instructions)
                cursor.execute(sql)
                # Prompt User that we are DONE..
                print('Done.....SAVE Successful......')


            else:
                print('Saving ABORTED.....Entries DISCARDED')

        else:
            print('Returning to Main Menu')

    
    def print_out_recipe(self, which):
        '''
        Takes one argument which (the recipe).
        Prints out the recipe to default printer.
        '''
        pass

if __name__ == '__main__':
    CookBook.database_menu()