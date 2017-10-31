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
        pass
    
    def database_menu():
        '''A loop that displays a list of options that the user 
        can perform'''
        cbk = CookBook() # Initialize the class

    

if __name__ == '__main__':
    CookBook.database_menu()