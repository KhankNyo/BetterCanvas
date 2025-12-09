# M2 - Set Up
Run the command "git clone https://github.com/KhankNyo/BetterCanvas" in your terminal
then cd into BetterCanvas directory. 
Run the file run.py using python3 run.py in your terminal. Put in the link "http://127.0.0.1:5000/logout" in your browser. 
### IMPORTANT: Make sure you are logged out on our website! Changes to the database were made.
Then, to access different parts of the website, please log in or register an account. Teacher and student accounts see different things on the website. 

If you do not wish to register, input "tester" into the username and "password123" for the password (without the quotes). This logs you into a premade teacher account. The rest of the accounts found in the /people tab also have the password "password123" as well. 

> Here is a screenshot from an example runtime after logging in as a teacher:
![teacher's runtime view](images/runtimess.png "BetterCanvas")

> Here is a screenshot after logging in as a student:
![student's runtime view](images/runtime_student_ss.png)


# Test Instructions: 
From the BetterCanvas directory, cd to the test directory in the terminal using "cd app/tests" (without the quotes). 
### IMPORTANT: run each test separately in the terminal. 
Ex. input (without the quotes) "pytest test_routes_home.py" and do the same for each test. Here are all the tests that should be run. Feel free to copy and paste:  
- pytest test_forms.py
- pytest test_routes_home.py 
- pytest test_routes_login.py
- pytest test_routes_redirect.py
- pytest test_routes_error.py


# Team Roles
- Bryan: Made models, forms and routes + most of the html 
- Khanh: Created and organized files, decorated + formatted
- Janet: Implemented login/logout with database. Wrote use cases and test cases.  
