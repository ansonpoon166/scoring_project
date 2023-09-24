CS50 scoring app
#### Video Demo:
#### Description:
My project is a scoring for the Chinese board games Mah Jong and Landlord.

'app.py' is the file where the application was written in Flask. It is a stateful app that can remember the players. Paths were defined using decorators. Every page can be accessed with both 'GET' and 'POST' requests except the homepage. When a page is redirected or returned using 'POST' request, information is passed in by users in a form. Under the 'mah_jong' and 'landlord' functions, the scores are calcuted based on users' inputs which are then used to update the SQL database. Under the 'mah_jong' and 'landlord' functions, there are also options for users to remove rows if a mistake is made.

The 'static' folder contains the 'style.css' where all the codes were written in to format the web app. This changes the format of tables, containers and background. This was modified from the css file from CS50 Finance.

The 'templates' folder contains all the html templates for the web app.

The 'layout.html' is the template where other templates were built on. This was taken from CS50 Finance with some modification.

The 'login.html' is the template of the homepage. This contains the description of the game and web app.

The 'landlord_player.html' is the template where the users can log the Landlord players' names. This just contains a form with three input fields and one submit button. The names are then remembered by the web app by session. However, the name does not exist in the table, the names would be added to table. This was done by linking the form to a sqlite3 database. There also exists a form that allow users to deregister from the table to delete a chosen row from the SQL database.

The 'landlord.html' is the template where the users can input the result of each round. There also exists a table where the data is taken form the sql database, giving the scores from each round. There is also another table that gives the total scores of the game so far. There also exists a form that allow users to deregister from the table to delete a chosen row from the SQL database.


The 'mah_jong_player.html' is the template where the users can log the Mah Jong players' names. This just contains a form with four input fields and one submit button. The names are then remembered by the web app by session. However, the name does not exist in the table, the names would be added to table This was done by linking the form to a sqlite3 database. There also exists a table where the data is taken form the sql database. This was done by linking the form to a sqlite3 database.

The 'mah_jong.html' is the template where the users can input the result of each round. There also exists a table where the data is taken form the sql database, giving the scores from each round. There is also another table that gives the total scores of the game so far. There also exists a form that allow users to deregister from the table to delete a chosen row from the SQL database.

'helpers.py' contain the library of functions which are later used in 'app.py'.

'score.db' is the sqlite3 database that stores all the score data. There are two tables in the database which are the score table for Mah Jong and the Landlord game.


