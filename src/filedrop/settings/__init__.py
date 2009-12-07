import platform

if platform.node() == "staff.penny-arcade.com":
    from filedrop.settings.production import *
else:
    from filedrop.settings.development import *
