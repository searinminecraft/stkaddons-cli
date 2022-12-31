#!/usr/bin/env python3

debug = False

def debuglog(text: str, int: int):
    if debug == False: return

    if int == 0:
        print(f'[INFO] {text}')
    if int == 1:
        print(f'[WARN] {text}')
    if int == 2:
        print(f'[ERROR] {text}')

import configparser
import os
import shutil
import subprocess
import sys
import xml.etree.ElementTree as et
from getpass import getpass
from glob import glob
from pathlib import Path
from urllib import request

# =============================================================
# =============================================================

try:
    from pick import pick
except ImportError as e:
    print('To use this, install pick (pip install pick) first.')
    debuglog(f'Unable to execute script: {str(e)}', 2)
    sys.exit(1)

# =============================================================
# =============================================================

api = 'https://online.supertuxkart.net/api/v2/user/'
useragent = 'Mozilla/5.0 (compatible; STKAddonsCLI/1.0; https://github.com/searinminecraft)'

config = configparser.ConfigParser()

def clear():
    if debug == True: return

    os.system('clear' if os.name == 'posix' else 'cls')

# ================================================
# =               BEGIN API CALLS                =
# ================================================

def poll(userid: int, token: str) -> bool:


    try:
        payload = f'userid={userid}&token={token}'

        debuglog(f'Sending \'{payload}\' to \'{api}poll\''.replace(token, '**************'), 0)

        proc = subprocess.run([
                            'curl',
                            '-fsSL',
                            '--request',
                            'POST',
                            api + 'poll',
                            '--data',
                            payload,
                            '--user-agent',
                            '\'' + useragent + '\''
                            ], stdout=subprocess.PIPE)

        with open('poll.xml', 'w') as f:
            f.write(proc.stdout.decode('utf-8'))

        item = et.parse(os.getcwd() + '/poll.xml')
        res = item.getroot()

        success = res.get('success')
        info = res.get('info')

        if success == 'no':
            debuglog(f'Error polling user. The server returned an error: {info}',2)
            return False
        else:
            return True

    except Exception as e:
        debuglog(f'An error occured while polling user: {str(e)}', 2)
        return False

def savedsession(userid: int, token: str) -> bool:

    try:
        payload = f'userid={userid}&token={token}'

        debuglog(f'Sending \'{payload}\' to \'{api}saved-session\''.replace(token, '**************'), 0)

        proc = subprocess.run([
                            'curl',
                            '-fsSL',
                            '--request',
                            'POST',
                            api + 'saved-session',
                            '--data',
                            payload,
                            '--user-agent',
                            '\'' + useragent + '\''
                            ], stdout=subprocess.PIPE)

        with open('session.xml', 'w') as f:
            f.write(proc.stdout.decode('utf-8'))

        item = et.parse(os.getcwd() + '/session.xml')
        res = item.getroot()

        success = res.get('success')
        info = res.get('info')

        if success == 'no':
            debuglog(f'Couldn\'t save session. The server returned an error: {info}',2)
            return False
        else:
            return True

    except Exception as e:
        debuglog(f'An error occured while saving the session: {str(e)}', 2)
        return False

def client_quit(userid: int, token: str) -> bool:

    try:
        payload = f'userid={userid}&token={token}'

        debuglog(f'Sending \'{payload}\' to \'{api}client-quit\''.replace(token, '**************'), 0)

        proc = subprocess.run([
                            'curl',
                            '-fsSL',
                            '--request',
                            'POST',
                            api + 'client-quit',
                            '--data',
                            payload,
                            '--user-agent',
                            '\'' + useragent + '\''
                            ], stdout=subprocess.PIPE)

        with open('session.xml', 'w') as f:
            f.write(proc.stdout.decode('utf-8'))

        item = et.parse(os.getcwd() + '/session.xml')
        res = item.getroot()

        success = res.get('success')
        info = res.get('info')

        if success == 'no':
            debuglog(f'Couldn\'t send client-quit request. The server returned an error: {info}',2)
            return False
        else:
            return True

    except Exception as e:
        debuglog(f'An error occured: {str(e)}', 2)
        return False

def get_friends_list(userid: int, token: str, visitingid: int) -> dict:

    try:
        payload = f'userid={userid}&token={token}&visitingid={visitingid}'

        debuglog(f'Sending \'{payload}\' to \'{api}get-friends-list\''.replace(token, '**************'), 0)
        proc = subprocess.run([
                            'curl',
                            '-fsSL',
                            '--request',
                            'POST',
                            api + 'get-friends-list',
                            '--data',
                            payload,
                            '--user-agent',
                            '\'' + useragent + '\''
                            ], stdout=subprocess.PIPE)

        with open('friends.xml', 'w') as f:
            f.write(proc.stdout.decode('utf-8'))
    except Exception:
        return []

    list = []

    item = et.parse(os.getcwd() + '/friends.xml')
    res = item.getroot()

    info = res.get('info')

    if res.get('success') == 'no':
        debuglog(f'[FriendManager]: Unable to get friends: The server returned an error: {info}', 2)
        print(f'Error getting friends: {info}')

    else:
        pass



    for i in res.findall('friends'):
        for friend in i.findall('friend'):
            for user in friend.findall('user'):
                list.append([user.get('user_name'), user.get('id'),
                friend.get('online'), friend.get('date'), friend.get('is_pending'), friend.get('is_asker')])

    return list

def user_search(userid: int, token: str, search_string: str) -> dict:
    try:
        payload = f'userid={userid}&token={token}&search-string={search_string}'

        debuglog(f'Sending \'{payload}\' to \'{api}user-search\''.replace(token, '**************'), 0)
        proc = subprocess.run([
                            'curl',
                            '-fsSL',
                            '--request',
                            'POST',
                            api + 'user-search',
                            '--data',
                            payload,
                            '--user-agent',
                            '\'' + useragent + '\''
                            ], stdout=subprocess.PIPE)

        with open('users.xml', 'w') as f:
            f.write(proc.stdout.decode('utf-8'))
    except Exception:
        return []

    list = []

    item = et.parse(os.getcwd() + '/users.xml')
    res = item.getroot()

    info = res.get('info')

    if res.get('success') == 'no':
        debuglog(f'[UserSearch]: Error getting search results: The server returned an error: {info}', 2)
        print(f'Error getting search results: {info}')
        return
    else:
        pass

    for i in res.findall('users'):
        for user in i.findall('user'):
            list.append([user.get('user_name'), user.get('id')])

    return list

def getranking(userid: int, token: str, username: str, id: int):
    try:
        payload = f'userid={userid}&token={token}&id={id}'

        debuglog(f'Sending \'{payload}\' to \'{api}get-ranking\''.replace(token, '**************'), 0)

        proc = subprocess.run([
                            'curl',
                            '-fsSL',
                            '--request',
                            'POST',
                            api + 'get-ranking',
                            '--data',
                            payload,
                            '--user-agent',
                            '\'' + useragent + '\''
                            ], stdout=subprocess.PIPE)

        with open('ranking.xml', 'w') as f:
            f.write(proc.stdout.decode('utf-8'))
    except Exception:
        pass

    item = et.parse(os.getcwd() + '/ranking.xml')
    res = item.getroot()

    info = res.get('info')

    if res.get('success') == 'no':
        print(f'Error getting ranking: {info}')
        return
    else:
        scores = res.get('scores')
        max_scores = res.get('max-scores')
        num_races_done = res.get('num-races-done')
        raw_scores = res.get('raw-scores')
        rating_deviation = res.get('rating_deviation')
        disconnects = res.get('disconnects')
        rank = res.get('rank')

        if int(rank) < 0:
            print(f'{username} has no ranking yet!')
            return

        print(f'{username} is at rank {rank} with a score of {scores}.')
        print('Detailed ranked information:')
        print(f'Number of races done: {num_races_done}')
        print(f'Highest score: {max_scores}')
        print(f'Raw Score: {raw_scores}')
        print(f'Rating Deviation: {rating_deviation}')
        print(f'Disconnects: {disconnects}')

def top_players(userid: int, token: str) -> dict:
    try:
        payload = f'userid={userid}&token={token}'

        debuglog(f'Sending \'{payload}\' to \'{api}top-players\''.replace(token, '**************'), 0)

        proc = subprocess.run([
                            'curl',
                            '-fsSL',
                            '--request',
                            'POST',
                            api + 'top-players',
                            '--data',
                            payload,
                            '--user-agent',
                            '\'' + useragent + '\''
                            ], stdout=subprocess.PIPE)

        with open('top.xml', 'w') as f:
            f.write(proc.stdout.decode('utf-8'))
    except Exception:
        return []

    list = []

    item = et.parse(os.getcwd() + '/top.xml')
    res = item.getroot()

    info = res.get('info')

    if res.get('success') == 'no':
        debuglog(f'[RankedTopPlayers]: Couldn\'t get top players: The server returned an error: {info}', 2)
        print(f'Error getting top players: {info}')
        return
    else:
        pass

    for i in res.findall('players'):
        for player in i.findall('player'):
            list.append([player.get('username'),
                        int(float(player.get('scores'))),
                        int(float(player.get('max-scores'))),
                        player.get('num-races-done'),
                        int(float(player.get('raw-scores'))),
                        int(float(player.get('rating-deviation'))),
                        player.get('disconnects')])

    return list

def friend_request(userid: int, token: str, friendid: int):
    try:
        payload = f'userid={userid}&token={token}&friendid={friendid}'

        debuglog(f'Sending \'{payload}\' to \'{api}friend-request\''.replace(token, '**************'), 2)

        proc = subprocess.run([
                            'curl',
                            '-fsSL',
                            '--request',
                            'POST',
                            api + 'friend-request',
                            '--data',
                            payload,
                            '--user-agent',
                            '\'' + useragent + '\''
                            ], stdout=subprocess.PIPE)

        with open('friendrequest.xml', 'w') as f:
            f.write(proc.stdout.decode('utf-8'))
    except Exception:
        pass

    item = et.parse(os.getcwd() + '/friendrequest.xml')
    res = item.getroot()

    info = res.get('info')

    if res.get('success') == 'no':
        debuglog(f'[FriendService]: Error sending friend request: The server returned an error: {info}', 2)
        print(f'Error sending friend request: {info}')
        return
    else:
        print(f'Successfully sent friend request to ID {friendid}!')

def accept_friend_request(userid: int, token: str, friendid: int):
    try:
        payload = f'userid={userid}&token={token}&friendid={friendid}'

        debuglog(f'Sending \'{payload}\' to \'{api}accept-friend-request\''.replace(token, '**************'), 0)

        proc = subprocess.run([
                            'curl',
                            '-fsSL',
                            '--request',
                            'POST',
                            api + 'accept-friend-request',
                            '--data',
                            payload,
                            '--user-agent',
                            '\'' + useragent + '\''
                            ], stdout=subprocess.PIPE)

        with open('friendrequest.xml', 'w') as f:
            f.write(proc.stdout.decode('utf-8'))
    except Exception:
        pass

    item = et.parse(os.getcwd() + '/friendrequest.xml')
    res = item.getroot()

    info = res.get('info')

    if res.get('success') == 'no':
        print(f'Error accepting friend request: {info}')
        return
    else:
        print(f'Successfully accepted friend request! You\'re now friends!')

def cancel_friend_request(userid: int, token: str, friendid: int):
    try:
        payload = f'userid={userid}&token={token}&friendid={friendid}'

        debuglog(f'Sending \'{payload}\' to \'{api}cancel-friend-request\''.replace(token, '**************'), 0)

        proc = subprocess.run([
                            'curl',
                            '-fsSL',
                            '--request',
                            'POST',
                            api + 'cancel-friend-request',
                            '--data',
                            payload,
                            '--user-agent',
                            '\'' + useragent + '\''
                            ], stdout=subprocess.PIPE)

        with open('friendrequest.xml', 'w') as f:
            f.write(proc.stdout.decode('utf-8'))
    except Exception:
        pass

    item = et.parse(os.getcwd() + '/friendrequest.xml')
    res = item.getroot()

    info = res.get('info')

    if res.get('success') == 'no':
        debuglog(f'[FriendService]: Error cancelling friend request: The server returned an error: {info}', 2)
        print(f'Error cancelling friend request: {info}')
        return
    else:
        print(f'Successfully cancelled friend request of ID {friendid}!')

def remove_friend(userid: int, token: str, friendid: int):
    try:
        payload = f'userid={userid}&token={token}&friendid={friendid}'

        debuglog(f'Sending \'{payload}\' to \'{api}remove-friend\''.replace(token, '**************'), 0)

        proc = subprocess.run([
                            'curl',
                            '-fsSL',
                            '--request',
                            'POST',
                            api + 'remove-friend',
                            '--data',
                            payload,
                            '--user-agent',
                            '\'' + useragent + '\''
                            ], stdout=subprocess.PIPE)

        with open('friendrequest.xml', 'w') as f:
            f.write(proc.stdout.decode('utf-8'))
    except Exception:
        pass

    item = et.parse(os.getcwd() + '/friendrequest.xml')
    res = item.getroot()

    info = res.get('info')

    if res.get('success') == 'no':
        debuglog(f'[FriendService]: Error removing friend: The server returned an error: {info}', 2)
        print(f'Error removing: {info}')
        return
    else:
        print(f'Successfully removed {friendid}!')

def decline_friend_request(userid: int, token: str, friendid: int):
    try:
        payload = f'userid={userid}&token={token}&friendid={friendid}'

        debuglog(f'Sending \'{payload}\' to \'{api}decline-friend-request\''.replace(token, '**************'), 0)

        proc = subprocess.run([
                            'curl',
                            '-fsSL',
                            '--request',
                            'POST',
                            api + 'decline-friend-request',
                            '--data',
                            payload,
                            '--user-agent',
                            '\'' + useragent + '\''
                            ], stdout=subprocess.PIPE)

        with open('friendrequest.xml', 'w') as f:
            f.write(proc.stdout.decode('utf-8'))
    except Exception:
        pass

    item = et.parse(os.getcwd() + '/friendrequest.xml')
    res = item.getroot()

    info = res.get('info')

    if res.get('success') == 'no':
        debuglog(f'[FriendService]: Error declining friend request: The server returned an error: {info}', 2)
        print(f'Error declining friend request: {info}')
        return
    else:
        print(f'Successfully declined friend request of ID {friendid}!')

def register(username: str, password: str, password_confirm: str, realname: str, email: str, terms: str):

    try:
        payload = f'username={username}&password={password}&password_confirm={password_confirm}&realname={realname}&email={email}&terms={terms}'

        debuglog(f'Sending \'{payload}\' to \'{api}register\''.replace(password, '**************').replace(password_confirm, '**************'), 0)

        proc = subprocess.run([
                            'curl',
                            '-fsSL',
                            '--request',
                            'POST',
                            api + 'register',
                            '--data',
                            payload,
                            '--user-agent',
                            '\'' + useragent + '\''
                            ], stdout=subprocess.PIPE)

        with open('registration.xml', 'w') as f:
            f.write(proc.stdout.decode('utf-8'))
    except Exception:
        pass

    item = et.parse(os.getcwd() + '/registration.xml')
    res = item.getroot()

    info = res.get('info')

    if res.get('success') == 'no':
        debuglog(f'[Registrar]: Couldn\'t register user {username}: The server returned an error: {info}', 0)
        print(f'Unable to register: {info}')
    else:
        print(f'You will receive an email with further instructions regarding account activation. Please be patient and be sure to check your spam folder.')

def reset_password(userid: int, current: str, new1: str, new2: str):
    try:
        payload = f'userid={userid}&current={current}&new1={new1}&new2={new2}'

        debuglog(f'Sending \'{payload}\' to \'{api}change-password\''.replace(current, '**************').replace(new1, '**************').replace(new2, '**************'), 0)

        proc = subprocess.run([
                            'curl',
                            '-fsSL',
                            '--request',
                            'POST',
                            api + 'change-password',
                            '--data',
                            payload,
                            '--user-agent',
                            '\'' + useragent + '\''
                            ], stdout=subprocess.PIPE)

        with open('reset_password.xml', 'w') as f:
            f.write(proc.stdout.decode('utf-8'))
    except Exception:
        pass

    item = et.parse(os.getcwd() + '/reset_password.xml')
    res = item.getroot()

    info = res.get('info')

    if res.get('success') == 'no':
        debuglog(f'[PasswordReset]: Password reset failed: The server returned an error: {info}', 2)
        print(f'Can\'t reset password: {info}')
        return
    else:
        print('Successfully reset password!')

def account_recovery(username: str, email: str):
    try:
        payload = f'username={username}&email={email}'

        debuglog(f'Sending \'{payload}\' to \'{api}recover\'', 0)

        proc = subprocess.run([
                            'curl',
                            '-fsSL',
                            '--request',
                            'POST',
                            api + 'recover',
                            '--data',
                            payload,
                            '--user-agent',
                            '\'' + useragent + '\''
                            ], stdout=subprocess.PIPE)

        with open('recovery.xml', 'w') as f:
            f.write(proc.stdout.decode('utf-8'))
    except Exception:
        pass

    item = et.parse(os.getcwd() + '/recovery.xml')
    res = item.getroot()

    info = res.get('info')

    if res.get('success') == 'no':
        debuglog(f'[Recovery]: Couldn\'t process recovery: The server returned an error: {info}', 2)
        print(f'Can\'t recover account: {info}')
        return
    else:
        print('You will receive an email with further instructions on how to reset your password. Please be patient and be sure to check your spam folder.')

def change_email(userid: int, token: str, new_email: str):
    try:
        payload = f'userid={userid}&token={token}&new-email={new_email}'

        debuglog(f'Sending \'{payload}\' to \'{api}change-email\''.replace(token, '**************'), 0)

        proc = subprocess.run([
                            'curl',
                            '-fsSL',
                            '--request',
                            'POST',
                            api + 'change-email',
                            '--data',
                            payload,
                            '--user-agent',
                            '\'' + useragent + '\''
                            ], stdout=subprocess.PIPE)

        with open('change_email.xml', 'w') as f:
            f.write(proc.stdout.decode('utf-8'))
    except Exception:
        pass

    item = et.parse(os.getcwd() + '/change_email.xml')
    res = item.getroot()

    info = res.get('info')

    if res.get('success') == 'no':
        print(f'Can\'t change email: {info}')
        return
    else:
        print(f'You will recieve an email to the new email for instructions on how to change the email of your STK account. Please be patient and be sure to check your spam folder.')

def getaddonvote(userid: int, token: str, addonid: str) -> dict:

    try:
        payload = f'userid={userid}&token={token}&addonid={addonid}'

        debuglog(f'Sending \'{payload}\' to \'{api}get-addon-vote\''.replace(token, '**************'), 0)
        proc = subprocess.run([
                           'curl',
                           '-fsSL',
                           '--request',
                           'POST',
                           api + 'get-addon-vote',
                           '--data',
                           payload,
                           '--user-agent',
                           '\'' + useragent + '\''
                           ], stdout=subprocess.PIPE)

        with open('addon_vote.xml', 'w') as f:
            f.write(proc.stdout.decode('utf-8'))

    except Exception:
       pass

    item = et.parse(os.getcwd() + '/addon_vote.xml')
    res = item.getroot()

    info = res.get('info')

    if res.get('success') == 'no':
        print(f'Can\'t get addon vote: {info}')
        return
    else:
        return [res.get('voted'), res.get('rating')]

def setaddonvote(userid: int, token: str, addonid: str, rating: int) -> dict:

    if int(rating) > 3:
        print('Your rating is above 3. It will automatically be set to 3.')
        rating = 3

    try:
        payload = f'userid={userid}&token={token}&addonid={addonid}&rating={rating}'

        debuglog(f'Sending \'{payload}\' to \'{api}set-addon-vote\''.replace(token, '**************'), 0)
        proc = subprocess.run([
                           'curl',
                           '-fsSL',
                           '--request',
                           'POST',
                           api + 'set-addon-vote',
                           '--data',
                           payload,
                           '--user-agent',
                           '\'' + useragent + '\''
                           ], stdout=subprocess.PIPE)

        with open('addon_vote.xml', 'w') as f:
            f.write(proc.stdout.decode('utf-8'))

    except Exception:
       pass

    item = et.parse(os.getcwd() + '/addon_vote.xml')
    res = item.getroot()

    info = res.get('info')

    if res.get('success') == 'no':
        print(f'Can\'t set addon vote: {info}')
        return
    else:
        return [res.get('new-average'), res.get('new-number'), res.get('addon-id')]

# ================================================
# =               END OF API CALLS               =
# ================================================

# =============================================================
# =============================================================

def authenticate(username: str, password: str, save_session: str = None) -> dict:
    try:

        if save_session is None:
            save_session = 'true'


        payload = f'username={username}&password={password}&save_session={save_session}'

        debuglog(f'Sending \'{payload}\' to \'{api}connect\''.replace(password, '**************'), 0)

        proc = subprocess.run([
                            'curl',
                            '-fsSL',
                            '--request',
                            'POST',
                            api + 'connect',
                            '--data',
                            payload,
                            '--user-agent',
                            '\'' + useragent + '\''
                            ], stdout=subprocess.PIPE)

        with open('connect.xml', 'w') as f:
            f.write(proc.stdout.decode('utf-8'))


        res = et.parse(os.getcwd() + '/connect.xml').getroot()

        if res.get('success') == 'no':
            print('Authentication failure: ' + res.get('info'))
            return
        else:
            os.remove('connect.xml')
            return [res.get('userid'), res.get('token'), res.get('username')]

    except Exception as e:
        print(str(e))

def login_prompt(username: str = None):


    if username is None:
        name = input('Username: ')

        if name == '':
            print('Username cannot be blank.')
            login_prompt()
    else:
        name = username

    password = getpass('Password: ')

    if password == '':
        print('Password cannot be blank.')
        login_prompt()

    clear()

    print(f'Logging in {name}...')

    data = authenticate(name, password)

    config.set('Config', 'token', data[1])
    config.set('Config', 'userid', data[0])
    config.set('Config', 'username', data[2])

    with open(os.path.expanduser('~')+"/.config/searinminecraft/stk_api_playground/config.ini", 'w') as configfile:
            config.write(configfile)

    config.read(os.path.expanduser('~') + "/.config/searinminecraft/stk_api_playground/config.ini")

    savedsession(config.get('Config', 'userid'), config.get('Config', 'token'))
    poll(config.get('Config', 'userid'), config.get('Config', 'token'))

    with open(os.path.expanduser('~') + '/.config/searinminecraft/stk_api_playground/config.ini', 'w') as f:
       config.write(f)

    main()

def loggedoutenv():

    choices = ['Login to STKAddons', 'Sign Up for an account', 'Reset password', 'Exit']

    opt, ind = pick(choices, 'Welcome to STKAddons CLI!')

    if ind == 0:
        login_prompt()
    if ind == 1:
        registration()
    if ind == 2:
        recovery()
    if ind == 3:
        sys.exit(0)

# =============================================================
# =============================================================

def get_addons(want: int) -> dict:

    try:
        proc = subprocess.run([
                            'curl',
                            '-fsSL',
                            'https://online.supertuxkart.net/downloads/xml/online_assets.xml',
                            '--user-agent',
                            '\'' + useragent + '\''
                            ], stdout=subprocess.PIPE)

        with open('online_assets.xml', 'w') as f:
            f.write(proc.stdout.decode('utf-8'))

        list_kart = []
        list_track = []
        list_arena = []

        item = et.parse(os.getcwd() + '/online_assets.xml')
        root = item.getroot()

        for kart in root.findall('kart'):
            list_kart.append([kart.get('name'), kart.get('id'), kart.get('file'), kart.get('uploader'), kart.get('designer'), kart.get('description'), int(kart.get('status')), int(len(kart.get('rating'))), int(kart.get('revision'))])

        for track in root.findall('track'):
            list_track.append([track.get('name'), track.get('id'), track.get('file'), track.get('uploader'), track.get('designer'), track.get('description'), int(track.get('status')), int(len(track.get('rating'))), int(track.get('revision'))])

        for arena in root.findall('arena'):
            list_arena.append([arena.get('name'), arena.get('id'), arena.get('file'), arena.get('uploader'), arena.get('designer'), arena.get('description'), int(arena.get('status')), int(len(arena.get('rating'))), int(arena.get('revision'))])


        if want == 0:
            return list_kart
        if want == 1:
            return list_track
        if want == 2:
            return list_arena

    except:
        return []

def get_addon_details(item: dict, type: int):

    dir_win = os.path.expanduser('~') + '/AppData/Roaming/supertuxkart/addons/'
    dir_linux = os.path.expanduser('~') + '/.local/share/supertuxkart/addons/'

    dir = dir_linux if os.name == 'posix' else dir_win

    name = item[0]
    id = item[1]
    file = item[2]
    uploader = item[3]
    designer = item[4]
    description = item[5]
    status = item[6]
    rating = item[7]
    revision = item[8]

    choices = ['Install Addon', 'Rate', 'Exit']

    title = f'Addon Name: {name}\nID: {id}\nUploader: {uploader}\nDesigner: {designer}\n\nDescription: {description}\nStatus: 0x{status}\nRating: {rating}\nRevision: {revision}\n\n\nWhat do you want to do to this item?'

    opt, ind = pick(choices, title)

    if ind == 0:
        try:

            debuglog(f'[AddonManager]: retrieving file \'{file}\'', 0)
            request.urlretrieve(file, os.getcwd() + f'/{id}.zip')


            debuglog('Unpacking file ' + os.getcwd() + f'/{id}.zip', 0)
            if type == 0:
                shutil.unpack_archive(os.getcwd() + f'/{id}.zip', f'{dir}karts/{id}')
            if type == 1 or type == 2:
                shutil.unpack_archive(os.getcwd() + f'/{id}.zip', f'{dir}tracks/{id}')

            os.remove(os.getcwd() + f'/{id}.zip')

        except Exception as e:
            debuglog(f'[AddonManager]: An error occured: {str(e)}', 2)
            print(f'Failed to install: {str(e)}')
        else:
            print(f'Successfully downloaded {name}!')
            input('Press Enter to continue.')

            addonexplorer()
    if ind == 1:
        clear()
        print(f'Please wait while I get your vote for {name}...')

        res = getaddonvote(config.get('Config', 'userid'), config.get('Config', 'token'), id)

        if res[0] == 'no':
            print('You have not voted for the addon yet. Input your rating from 0-3 to cast a vote:')
        else:
            print(f'You\'ve voted for the addon {name} already with a rating of {res[1]}. But you can change the rating by inputting a rating from 0-3:')

        rating = input('>')

        print('Please wait...')

        res = setaddonvote(config.get('Config', 'userid'), config.get('Config', 'token'), id, int(rating))

        print(f'Successfully voted for addon {name}! New average rating: {res[0]}')
        input('Press enter to continue.')

        addonexplorer()
    if ind == 2:
        return

def addonexplorer():

    choices = ['<-- Go Back', 'Karts', 'Tracks', 'Arenas']

    opt, ind = pick(choices, 'What type of addon do you want to explore?', '>')

    if ind == 1:
        karts = get_addons(0)

        choices = []

        for key in karts:
            choices.append(f'{key[0]} (revision {key[8]}) by {key[4]}')


        opt, ind = pick(choices, 'Pick a kart to get details or install: ', '>')

        get_addon_details(karts[ind], 0)

    if ind == 2:
        tracks = get_addons(1)

        choices = []

        for key in tracks:
            choices.append(f'{key[0]} (revision {key[8]}) by {key[4]}')


        opt, ind = pick(choices, 'Pick a track to get details or install: ', '>')

        get_addon_details(tracks[ind], 1)

    if ind == 3:
        arenas = get_addons(2)

        choices = []

        for key in arenas:
            choices.append(f'{key[0]} (revision {key[8]}) by {key[4]}')


        opt, ind = pick(choices, 'Pick an arena to get details or install: ', '>')

        get_addon_details(arenas[ind], 2)

    if ind == 0:
        return

# =============================================================
# =============================================================

def process_friends_list():

    id = input('ID of user to get friends list (leave blank to get your friends list): ')

    if id == '':
        id = config.get('Config', 'userid')
    else:
        print('Note: you are visiting someone else\'s friends list. Information will be limited.')

    print('<Name> <ID> <Online> <Since> <Pending?> <Recieving Request?>')

    for friend in get_friends_list(config.get('Config', 'userid'), config.get('Config', 'token'), id):

        if id == config.get('Config', 'userid'):
            print(f'{friend[0]}  {friend[1]}  {friend[2]}  [{friend[3]}]  {friend[4]}  {friend[5]}')
        else:
            print(f'{friend[0]}  {friend[1]}')

def getuserranking():

    id = input('ID of user to get ranking info (leave blank for your ranking information): ')

    username = config.get('Config', 'username')

    if id == '':
        id = config.get('Config', 'userid')
        print(f'Getting ranking information for {username}')
        getranking(config.get('Config', 'userid'), config.get('Config', 'token'), config.get('Config', 'username'), config.get('Config', 'userid'))
    else:
        print(f'Getting ranking information from ID {id}')
        getranking(config.get('Config', 'userid'), config.get('Config', 'token'), id, id)

def search():

    user = input('Enter the string you want to search: ')

    if user == '':
        print('Search query can\'t be empty.')
        return

    print('<Name> <ID>')

    query = user_search(config.get('Config', 'userid'), config.get('Config', 'token'), user)

    if query == []:
        print('No Results :/')
        return

    for user in query:
        print(f'{user[0]} {user[1]}')

def getldb():

    print('Top 10 Ranked Players')

    print('<#> <Name> <Score> <Highest Score> <Races Done> <Raw Score> <Rating Deviation> <Disconnects>')

    rank = 1

    for player in top_players(config.get('Config', 'userid'), config.get('Config', 'token')):


        print(f'{rank}. {player[0]} {player[1]} {player[2]} {player[3]} {player[4]} {player[5]} {player[6]}')

        rank +=1

def friend(action: int):
    id = input('Enter the ID of the user: ')

    if id == '':
        print('ID must not be empty!')
        return
    if action == 0:
        friend_request(config.get('Config', 'userid'), config.get('Config', 'token'), id)
    elif action == 1:
        accept_friend_request(config.get('Config', 'userid'), config.get('Config', 'token'), id)
    elif action == 2:
        decline_friend_request(config.get('Config', 'userid'), config.get('Config', 'token'), id)
    elif action == 3:
        cancel_friend_request(config.get('Config', 'userid'), config.get('Config', 'token'), id)

def registration():
    clear()

    username = input('Please enter a username: ')

    if username == '':
        print('Username cannot be blank.')
        registration()

    password = getpass('Enter a password: ')

    if password == '':
        print('Password cannot be blank.')
        registration()

    confirm = getpass('Confirm password: ')

    if confirm != password:
        print('Passwords don\'t match!')
        registration()

    email = input('Enter your email: ')

    if email == '':
        print('Email cannot be blank.')
        registration()

    realname = input(f'Enter your real name [{username}]: ')

    if realname == '':
        realname = username

    clear()
    print('Please read the terms and conditions for SuperTuxKart at \'https://terms.supertuxkart.net\'. You must agree to these terms in order to register an account for STK. If you have any questions or comments regarding these terms, please contact searinminecraft or the SuperTuxKart team.')
    input('\nI agree to the above terms and am 13 years or older.')

    clear()
    print('Please Wait...')
    register(username, password, confirm, realname, email.replace('@', '%40'), 'on')

def passwordreset():

    current = getpass('Current password: ')

    new = getpass('New password:')

    if new == '':
        print('New password cannot be blank.')
        passwordreset()

    confirm = getpass('Confirm new password: ')

    if confirm != new:
        print('Passwords don\'t match!')
        passwordreset()

    reset_password(config.get('Config', 'userid'), current, new, confirm)

def recovery():

    print('Enter the username and email you supplied in registration:')

    username = input('Username: ')

    if username == '':
        print('Username cannot be blank.')
        recovery()

    email = input('Email: ')

    if email == '':
        print('Email cannot be blank.')
        recovery()

    account_recovery(username, email.replace('@', '%40'))

def email_change():
    print('Enter the new email below:')

    email = input('> ')

    if email == '':
        print('Email cannot be blank.')
        email_change()

    change_email(config.get('Config', 'userid'), config.get('Config', 'token'), email.replace('@', '%40'))

# =============================================================
# =============================================================


def init():
    debuglog("Creating Config...", 0)

    Path(os.path.expanduser('~') + '/.config/searinminecraft/stk_api_playground').mkdir(parents=True, exist_ok=True)

    f = open(os.path.expanduser('~') + "/.config/searinminecraft/stk_api_playground/config.ini", 'w')
    f.close()
    config.read(os.path.expanduser('~') + "/.config/searinminecraft/stk_api_playground/config.ini")
    config.add_section('Config')
    config.set('Config', 'token', '')
    config.set('Config', 'userid', '')
    config.set('Config', 'username', '')

# =============================================================
# =============================================================

def cleanup():
    for file in glob('*.xml'):
        os.remove(os.getcwd() + '/' + file)

def main():

    choices = ['Log Out',
            'Switch Account',
            'Poll User',
            'Get Friends List',
            'Search for a user',
            'Get ranking',
            'Get Top 10 Ranked Players',
            'Send a Friend Request',
            'Accept a Friend Request',
            'Decline a Friend Request',
            'Cancel a Friend Request',
            'Change email',
            'Get Addons',
            'Exit (Will save session)',]

    opt, ind = pick(choices, 'Hi ' + config.get('Config', 'username') + '! What do you want to do today?')


    if ind == 0:
        print('Goodbye!')
        cleanup()
        config.set('Config', 'token', '')
        config.set('Config', 'userid', '')
        config.set('Config', 'username', '')

        with open(os.path.expanduser('~')+"/.config/searinminecraft/stk_api_playground/config.ini", 'w') as configfile:
            config.write(configfile)

        client_quit(config.get('Config', 'userid'), config.get('Config', 'token'))

        loggedoutenv()
    elif ind == 1:
        login_prompt()
        main()
    elif ind == 2:
        if poll(config.get('Config', 'userid'), config.get('Config', 'token')) == True:
            print('Success!')
            input('\nPress enter to continue.')
        else:
            print('User poll failed.')
            input('\nPress enter to continue.')
    elif ind == 3:
        process_friends_list()
        input('\nPress enter to continue.')
    elif ind == 4:
        search()
        input('\nPress enter to continue.')
    elif ind == 5:
        getuserranking()
        input('\nPress enter to continue.')
    elif ind == 6:
        getldb()
        input('\nPress enter to continue.')
    elif ind == 7:
        friend(0)
        input('\nPress enter to continue.')
    elif ind == 8:
        friend(1)
        input('\nPress enter to continue.')
    elif ind == 9:
        friend(2)
        input('\nPress enter to continue.')
    elif ind == 10:
        friend(3)
        input('\nPress enter to continue.')
    elif ind == 11:
        email_change()
    elif ind == 12:
        addonexplorer()
    elif ind == 13:
        print("Goodbye!")
        client_quit(config.get('Config', 'userid'), config.get('Config', 'token'))
        cleanup()
        sys.exit(0)

    clear()
    main()

# =============================================================
# =============================================================

if __name__ == '__main__':
    clear()

    debuglog("Checking for config...", 0)
    if (not(os.path.exists(os.path.expanduser('~')+"/.config/searinminecraft/stk_api_playground/config.ini")) or os.stat(os.path.expanduser('~')+"/.config/searinminecraft/stk_api_playground/config.ini").st_size == 0):
        init()

    config.read(os.path.expanduser('~') + "/.config/searinminecraft/stk_api_playground/config.ini")

    debuglog("Checking for token...", 0)
    if config.get('Config', 'token') == '':
        clear()
        loggedoutenv()

    debuglog("Authenticating user...", 0)
    pollstat = savedsession(config.get('Config', 'userid'), config.get('Config', 'token'))

    if pollstat == False:
        print("Session is invalid (token may be tempoary, expired, or renewed). Please log in again.")

        print("Logging in as " + config.get('Config', 'username') +".")
        login_prompt(config.get('Config', 'username'))
    clear()
    poll(config.get('Config', 'userid'), config.get('Config', 'token'))
    main()

