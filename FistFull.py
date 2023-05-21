#!/usr/bin/python3
import curses
import threading
import time
import requests
import pyfiglet
import argparse
import sys
import os
import queue

# Define the URLs for bulk requests
url = ""
last_word = ""
loot = 0

def setup_arg_parser():
    parser = argparse.ArgumentParser(description='CLI arguments')
    parser.add_argument('--url', metavar='u', type=str, required=True, help='Target URL')
    parser.add_argument('-X', choices=['GET', 'POST'], help='HTTP method')
    parser.add_argument('-H', '--header', action='append', nargs=2, metavar=('key','value'), help='HTTP header (key-value pair)')
    parser.add_argument('-w', '--wordlist', help='Custom wordlist', default='linux.txt')
    parser.add_argument('-O', '--os', choices=['windows', 'linux'], default='linux', help='Operating system (default: linux)')
    parser.add_argument('-fs', '--filter-size', type=int, help='Filter response size')
    parser.add_argument('-d', '--data', action='append', metavar='value', help='Data for POST request (can be repeated)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose mode')

    
    # Parse the args.
    args = parser.parse_args()

    if args.X == 'POST' and args.data is None:
        parser.error("When using POST method, --data parameter is required.")

    return args

# Function to update the global loot variable
def update_variable_loot():
    global loot
    loot += 1


    # Read the wordlist from the file
def read_wordlist(file):
    with open(file, 'r') as f:
        return [line.strip() for line in f]


# Function to make URL requests
def make_requests():
    update_variable_loot()
    global last_word
    print("sdklfjkasld;fkl;jdsfj")
    headers = {}
    modified_data = []
    modified_url = ""


    if args.header:
        for header in args.H:
            key, value = header
            headers[key] = value

        
    if args.X == 'GET':
        for word in wordlist:
            last_word = word
            update_variable_loot()
            time.sleep(1)
            modified_url = args.url.replace('LOOT', word)

    elif args.X == 'POST':
        if args.data:
            for word in wordlist:
                time.sleep(1)           
                update_variable_loot()
                last_word = word

    else:
        raise ValueError('Unsupported method specified.')

    pass

def main(stdscr):
    # Set up the terminal
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(1)  # Non-blocking input
    stdscr.timeout(100)  # Delay between animation frames (in milliseconds)

    # Define the ASCII art frames
    frames = [
        r'''
        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠉⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣻⣿⣭⡀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣽⣿⣿⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡿⠟⢛⣹⣷⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠉⠳⠀⠈⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⠟⣹⢟⡽⠋⠁⠀⠐⠉⣹⣿⣯⡉⠛⠀⠿⠟⠻⠋⠙⠉⠉⠈⠏⠁⠀⠀⠀⠀⠀⠐⠿⣮⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⠟⠁⠀⠁⡉⠀⠀⠀⡀⠄⠀⠈⠙⠻⠱⡀⠀⠀⠀⢠⣠⣀⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⠿⣿⣿⣿⣿⣿⣿⣿⣿
        ⣿⣿⡿⠁⠀⠀⠀⠀⣃⣠⣤⠶⠖⢫⣭⠀⠀⠀⠈⠁⠀⠀⢠⣾⣿⣟⠟⢷⣾⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿
        ⣿⣿⠡⠀⠀⠀⠀⣈⠋⢁⡠⠔⢊⣽⣿⣇⡀⠀⠀⠉⠁⣀⣹⣿⣶⣾⣿⣶⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣿⣿⣿⣿⣿
        ⣿⠃⠀⠀⠀⠀⢸⣿⡷⢀⣴⣾⡋⣁⣾⣿⠁⠀⣠⣤⣶⣿⣿⣿⣿⣿⣿⡿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣹⣿⣿⣿⣿
        ⠇⡀⠀⠀⠀⠀⠀⠉⠁⠈⠀⠹⣿⣿⣭⣽⡈⠀⣿⣿⣿⣿⣿⣦⣍⡁⠁⠀⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿
        ⣸⠁⠀⠀⠀⠀⠀⠀⡔⠀⠀⠨⠏⣿⣗⢀⣀⠨⣿⣿⣿⣿⣿⣟⣿⣿⣿⣷⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⣿⣿
        ⡟⠀⠀⠀⠀⠀⠀⠀⣰⢀⠀⠀⠀⠘⠟⠀⢀⣠⣿⣿⣿⣿⣿⣿⣿⡟⣿⣿⣿⣿⣿⣷⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⢻⣿⣿⣿⣿
        ⡇⠀⠀⠀⠀⠀⠀⠀⡹⢸⣦⡀⠀⠀⠀⠀⢀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⣿⢿⣿
        ⣷⡄⠀⠀⠀⠀⠀⢀⢷⡈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⡂⠸⠯⠿⢿⣼⣿
        ''',
        r'''
        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣻⣯⣥⡀⠛⠛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡾⠿⢿⣿⣷⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠙⠳⠀⠀⠉⠙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⠟⣹⢟⡽⠋⠁⠀⠐⠉⣹⣿⣯⡉⠛⠀⠻⠟⠻⠋⠙⠉⠉⠈⠏⠁⠀⠀⠀⠀⠀⠐⠺⣮⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⠟⠀⠀⠁⡉⠀⠀⠀⡀⠄⠀⠈⠙⠻⠱⡀⠀⠀⠀⢠⣠⣀⠤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⠿⣿⣿⣿⣿⣿⣿⣿⣿
        ⣿⣿⡿⠁⠀⠀⠀⢀⣃⣠⣤⠶⠖⢢⣬⠀⠀⠀⠀⠀⠀⡀⢀⣾⣿⣿⠿⢿⣾⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿
        ⣿⣿⠡⠀⠀⠀⠀⢈⠋⢁⣠⠔⢊⣽⣿⣇⡄⠀⠀⠉⠅⣀⣹⣿⣶⣾⣿⣶⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣿⣿⣿⣿⣿
        ⠿⠃⠀⠀⠀⣀⣸⠿⡿⣀⣴⣾⣏⣡⣼⣻⣇⣀⣤⣤⣴⣿⣿⣿⣿⣿⠿⠿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣹⣿⣿⣿⣿
        ⠆⡀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠹⣿⣿⣽⣶⡈⠉⢿⣿⣿⣿⣿⣶⣄⣀⠀⠀⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⢻⣿⣿⣿⣿
        ⣠⠀⠁⠀⠀⠀⠀⠀⡀⠀⠃⠠⠤⣿⣿⣏⠉⡀⠀⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣤⣿⣿⣿
        ⡟⠀⠀⠀⠀⠀⠀⠀⣰⢀⠀⠀⠀⠘⠏⠀⢀⣠⣿⣿⣿⣿⣿⣿⣿⡟⢿⣿⣿⣿⣿⣷⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⢻⣿⣿⣿⣿
        ⡇⠀⠀⠀⠀⠀⠀⠀⡸⢸⣦⡀⠀⠀⠀⠀⢀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⣿⢿⣿
        ⣿⡄⠀⠀⠀⠀⠀⢀⢷⡈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⡀⠸⠯⠿⢿⣼⣿
        ''',
        r'''
        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣻⣯⣥⡀⠛⠛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡾⠿⠿⣻⣷⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠉⠳⠀⠈⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⠟⣹⢟⡽⠋⠁⠀⠐⠉⣹⣿⣯⡉⠛⠀⠿⠟⠻⠋⠙⠉⠉⠈⠏⠁⠀⠀⠀⠀⠀⠐⠿⣮⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⠟⠁⠀⠁⡉⠀⠀⠀⡀⠄⠀⠈⠙⠻⠱⡀⠀⠀⠀⢠⣠⣀⠤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⠿⣿⣿⣿⣿⣿⣿⣿⣿
        ⣿⣿⡿⠁⠀⠀⠀⢀⣃⣠⣤⠶⠖⢫⣭⠀⠀⠀⠈⠁⠀⡀⢀⣶⣿⣟⠿⢷⣾⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿
        ⣿⣿⠡⠀⠀⠀⠀⢈⠋⢁⣠⠔⢊⣽⣿⣇⡄⠀⠀⠩⠅⣀⣹⣿⣶⣾⣿⣶⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣿⣿⣿⣿⣿
        ⠿⠃⠀⠀⠀⣀⣸⠿⡿⣀⣴⣾⣏⣡⡺⠿⢃⣀⣠⣤⣶⡿⣿⣿⣿⡿⠿⠿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣹⣿⣿⣿⣿
        ⠆⡀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠹⣿⣿⣵⣶⡈⠉⣿⣿⣿⣿⢶⣦⣄⡀⠀⠀⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⢻⣿⣿⣿⣿
        ⣠⠀⠁⠀⠀⠀⠀⠀⡀⠀⠃⠠⠄⣾⣏⢻⣁⠀⣤⣼⣿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣏⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣤⣿⣿⣿
        ⡟⠀⠀⠀⠀⠀⠀⠀⣰⢀⠀⠀⠀⠘⠟⠀⢀⣠⣿⣿⣿⣿⣿⣷⣿⡟⣿⣿⣿⣿⣿⣷⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⢻⣿⣿⣿⣿
        ⡇⠀⠀⠀⠀⠀⠀⠀⡹⢸⣦⡀⠀⠀⠀⠀⢀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⣿⢿⣿
        ⣿⡄⠀⠀⠀⠀⠀⢀⢷⡈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⡀⠸⠯⠿⢿⣼⣿
        '''
    ]

    banner = r'''
    ███████╗██╗███████╗████████╗███████╗██╗   ██╗██╗     ██╗        ██████╗ ██╗   ██╗
    ██╔════╝██║██╔════╝╚══██╔══╝██╔════╝██║   ██║██║     ██║        ██╔══██╗╚██╗ ██╔╝
    █████╗  ██║███████╗   ██║   █████╗  ██║   ██║██║     ██║        ██████╔╝ ╚████╔╝ 
    ██╔══╝  ██║╚════██║   ██║   ██╔══╝  ██║   ██║██║     ██║        ██╔═══╝   ╚██╔╝  
    ██║     ██║███████║   ██║   ██║     ╚██████╔╝███████╗███████╗██╗██║        ██║   
    ╚═╝     ╚═╝╚══════╝   ╚═╝   ╚═╝      ╚═════╝ ╚══════╝╚══════╝╚═╝╚═╝        ╚═╝   LFI
                                                                                 
    '''
    # Create a thread for making URL requests
    request_thread = threading.Thread(target=make_requests)
    request_thread.daemon = True
    request_thread.start()
    global loot
    global last_word

    # Run the animation
    frame_index = 0

    while True:
        # Clear the screen
        stdscr.clear()
        i = 0


        # Print the current frame

        stdscr.addstr(0, 0, banner)
        stdscr.addstr(9,10, "DancingEmus")
        stdscr.addstr(10, 0, frames[frame_index])
        stdscr.addstr(27, 10, f"Loot: {loot}")
        stdscr.addstr(28, 10, f"Target: {args.url}")
        stdscr.addstr(29, 10, f"Request Type: {args.X}")
        stdscr.addstr(29, 40, f"OS: {args.os}")
        stdscr.addstr(30, 10, f"WordList: {args.wordlist}")
        

        if args.header:
            stdscr.addstr(31, 10, 'Request Headers:')
            for i, header in enumerate(args.header):
                key, value = header
                stdscr.addstr(32 + i, 12, f'{key}: {value}')


        if args.verbose:
            if args.X == 'GET':
                stdscr.addstr(33 + i, 10, f'url payload: {args.url.replace("LOOT", last_word)}')
            elif args.X == 'POST':
                stdscr.addstr(33 + i, 10, 'Data: ')
                for j, data in enumerate(args.data):
                    stdscr.addstr(34 + j, 12, f'{data.replace("LOOT", last_word)}')


        # Update the frame index
        frame_index = (frame_index + 1) % len(frames)

        # Refresh the screen
        stdscr.refresh()

        # Delay between frames
        time.sleep(0.1)

    # Wait for the request thread to finish.
    request_thread.join()

# Acess the parsed arguments globally.
args = setup_arg_parser()


# Define the wordlist as an array from the file
wordlist = read_wordlist(args.wordlist) if args.wordlist else []

# Run the script
if __name__ == '__main__':
    curses.wrapper(main)