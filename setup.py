from distutils.core import setup

setup(name = "PassTools",
        version = '1.0.0',
        description = 'Python SDK for PassTools API',
        author = 'Tello, Inc.',
        author_email = 'help@tello.com',
        packages = ['passtools'],
        data_files = [('Example_Scripts/', ['Example_Scripts/Ex1_Templates.py', 
                                    'Example_Scripts/Ex2_Passes.py', 
                                    'Example_Scripts/Ex3_User_Specific_Passes.py', 
                                    'Example_Scripts/Ex4_Updating_Pass_Data.py'])]
    )