"""
Displays settings
"""

from workflow import Workflow
from venmo_api import Venmo
import util

UPDATE_SETTINGS = {'github_slug' : 'azai91/alfred-venmo-workflow'}
HELP_URL = 'https://github.com/azai91/alfred-venmo-workflow/issues'

wf = Workflow(update_settings=UPDATE_SETTINGS, help_url=HELP_URL)

def main(_):
    user_input = ""
    options = True if wf.args[0][0] == '>' else False

    if wf.update_available:
        Venmo.add_update()

    try:
        user_input = wf.args[0][1::].strip() if options else wf.args[0]
    except:
        user_input = wf.args[0]

    if options:
        Venmo.show_options(user_input)
    elif len(user_input) and Venmo.findFriend(user_input):
        Venmo.show_formatting(user_input)
    elif len(user_input):
        try:
            Venmo.show_friends(user_input)
        except:
            Venmo.show_options('login')

    return 0

if __name__ == '__main__':
    wf.run(main)