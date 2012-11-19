from distutils.core import setup
import os

here = os.path.dirname(os.path.abspath(__file__))
try:
    description = file(os.path.join(here, 'README.md')).read()
except (OSError, IOError):
    description = ''

setup(name = "PassTools",
    version = '1.0.1',
    description = 'Python SDK for PassTools API',
    author = 'Tello, Inc.',
    author_email = 'help@tello.com',
    packages = ['passtools'],
    data_files = [('Example_Scripts/', ['Example_Scripts/Ex1_Templates.py', 
                                'Example_Scripts/Ex2_Passes.py', 
                                'Example_Scripts/Ex3_User_Specific_Passes.py', 
                                'Example_Scripts/Ex4_Updating_Pass_Data.py',
                                'Example_Scripts/Ex5_List_Variations.py',
                                'Example_Scripts/Ex6_Push_Update.py'])]
    )