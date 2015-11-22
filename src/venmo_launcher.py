import sys
import util
from venmo_api import Venmo
from workflow import Workflow

UPDATE_SETTINGS = {'github_slug' : 'azai91/alfred-venmo-workflow'}
HELP_URL = 'https://github.com/azai91/alfred-venmo-workflow/issues'

wf = Workflow(update_settings=UPDATE_SETTINGS, help_url=HELP_URL)

def main(wf):
    command = wf.args[0]
    if command == 'logout':
        Venmo.delete_credentials()
        return sys.stdout.write("logged out")
    elif command == 'login':
        return Venmo.open_auth_page()
    elif command == 'clear':
        Venmo.clear_cache()
        return sys.stdout.write("cache cleared")
    elif command.startswith('set'):
        length = int(command[3:])
        Venmo.set_cache_length(length)
        return sys.stdout.write("cache set to %s seconds" % str(length))

    try:
        Venmo.complete_transaction(command)
        sys.stdout.write(util.create_post_message(command))
    except:
        sys.stdout.write("Payment failed")


if __name__ == '__main__':
    sys.exit(wf.run(main))
