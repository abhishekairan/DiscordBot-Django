from django.test import TestCase
import os
# Create your tests here.

try:
    os.remove('E:\CODES\discord\Keni_V2\discordBot\migrations\\0001_initial.py')
except:
    pass
try:
    os.remove('E:\CODES\discord\Keni_V2\db.sqlite3')
except:
    pass