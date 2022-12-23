# STKAddons CLI

A command line tool that lets you manage your SuperTuxKart Account and download addons, in the command line!

## Dependencies:

* At least Python 3 or later
* `pick`

## What works?

* Everything

# FAQ

* Does this steal my SuperTuxKart credentials?
    
    * No! This Python script does not send any of your credentials to any server except the SuperTuxKart servers.

    If you don't trust this script, you can always view at the source code :) (disclaimer: it's a mess so don't judge my code)

* I get errors! What do I do?

    * If it says something like 'Session not valid. Please sign in.' or anything related to sessions, go to the main menu of this script, select 'Log out' (don't log out of your desktop, though!), then try to log in again.

    If you get code related errors, you can always create an issue.

* Why does this exist?

    * At first I planned to make this a python script that messes with the SuperTuxKart API. But when I added more and more stuff to it, it seemed like a CLI frontend for STKAddons. So thats why I decided to make this the CLI frontend for STKAddons.

    * And also, this can be useful for people who use a tty on linux.