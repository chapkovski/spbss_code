from os import environ

SESSION_CONFIGS = [
    dict(
        name='dice',
        display_name='Dice game (Fischbacher and Föllmi-Heusi 2013)',
        app_sequence=['dice'],
        num_demo_participants=1,
        beliefs=False
    ),
    dict(
        name='dice_beliefs',
        display_name='Dice game  with beliefs',
        app_sequence=['dice'],
        num_demo_participants=1,
        beliefs=True
    ),
    dict(
        name='dg',
        display_name='Dictator game',
        app_sequence=['dg'],
        num_demo_participants=2,
    ),
    dict(
        name='ug',
        display_name='Ultimatum game',
        app_sequence=['ug'],
        num_demo_participants=2,
        strategy=False
    ),
    dict(
        name='ug_strategy',
        display_name='Ultimatum game  - strategy method',
        app_sequence=['ug'],
        num_demo_participants=2,
        strategy=True
    ),
    dict(
        name='tg',
        display_name='Trust game',
        app_sequence=['tg'],
        num_demo_participants=2,
    ),
    dict(
        name='pgg',
        display_name='Public good game',
        app_sequence=['pgg'],
        num_demo_participants=3,
    ),
    dict(
        name='ret',
        display_name='RET',
        app_sequence=['ret'],
        num_demo_participants=1,
    ),

]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00,
    participation_fee=0.00,
    doc="",
    use_browser_bots=False,
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '6286421661163'
