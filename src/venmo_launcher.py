import sys
from venmo_api import Venmo
from workflow import Workflow

UPDATE_SETTINGS = {'github_slug' : 'azai91/alfred-venmo-workflow'}
HELP_URL = 'https://github.com/azai91/alfred-venmo-workflow/issues'

wf = Workflow(update_settings=UPDATE_SETTINGS, help_url=HELP_URL)

def main(wf):
  url = wf.args[0]
  if url == 'logout':
    Venmo.delete_credentials()
    return sys.stdout.write("logged out")
  elif url == 'login':
    return Venmo.open_auth_page()
  elif url == 'clear':
    Venmo.clear_cache()
    return sys.stdout.write("cache cleared")
  elif url.startswith('set'):
    length = int(url[3:])
    Venmo.set_cache_length(length)
    return sys.stdout.write("cache set to %s seconds" % str(length))

  # Venmo.open_page(url)

if __name__ == '__main__':
  sys.exit(wf.run(main))
