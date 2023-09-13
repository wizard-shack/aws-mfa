import yaml
import curses
from helpers.validate_config import get_valid_config

def _accounts_menu(stdscr):
    '''Returns the selected account from the menu'''
    curses.curs_set(0)
    current_row = 0

    config = get_valid_config()

    while True:
        stdscr.clear()
        for i, account in enumerate(config['accounts']):
            if i == current_row:
                stdscr.addstr(i, 0, account['name'], curses.A_REVERSE)
            else:
                stdscr.addstr(i, 0, account['name'])
        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(config['accounts']) - 1:
            current_row += 1
        elif key in [10, 13]:
            selection = config['accounts'][current_row]
            break
        stdscr.refresh()
    
    return selection

def _user_menu(stdscr, account):
    '''Returns the selected user from the menu'''
    curses.curs_set(0)
    current_row = 0

    while True:
        stdscr.clear()
        for i, user in enumerate(account['users']):
            if i == current_row:
                stdscr.addstr(i, 0, user['name'], curses.A_REVERSE)
            else:
                stdscr.addstr(i, 0, user['name'])
        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(account['users']) - 1:
            current_row += 1
        elif key in [10, 13]:
            selection = account['users'][current_row]
            break
        stdscr.refresh()
    
    return selection

def get_account():
    return curses.wrapper(_accounts_menu)

def get_user(account):
    return curses.wrapper(_user_menu, account)