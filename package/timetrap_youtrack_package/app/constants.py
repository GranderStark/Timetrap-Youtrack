from os.path import expanduser

TYRC_EXAMPLE = """
db:
  url: 'sqlite:////PATH_TO_TIMETRAP_DB/timetrap.db'

track_auth:
  url: ''
  login: 'xxx'
  password: 'yyy'
  
tasks_name_masks: ['prj1-', 'prj2-']
"""

HOME = expanduser("~")
