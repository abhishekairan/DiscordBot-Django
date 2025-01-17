# Discord Bot Dashboard
This is a project i tried to build during my learning phase of django. The main purpose of this project is to server a discordbot with its own dashboard where user can configure every part of the project, however due to my incomplete kknowledge that time and lack of asyn and sync understanding i was unable to continue this project and scrap it.
### Things i learned from this project
- How to work with sync and async task.
- Importance of env variables
- Working with APIs and importance of creating API instead of hard coding everying or using classes and functions
- Authentication using Oauth2 (i used discord api for authenticating)
- Template engines like jinja which help me understanding templates and helping me alot till now
- Understating some cloud security messures like CSRF token, SQL Injections and how to protect your app from it
- Serving static files on web
- Deploying the app is real challenge
- Version control. I opened different branches to organize and log my progress (Deleted all the branches as of now)
- Dynamic routing, parsing url, web scrabing, and alot more 
Although i no longer plan to complete this project since i started working on other project but if you are intreseted in developing this type app i hope my code may help you a little, feel free to connect if you have queries
### Features
- User authentication using discord
- Server listing (Dashboard will show all the server in which he/she can add the bot)
- Embed Sender
- Discord Bot
- Join & Leave greeting
### How to run this project?
- Download or clone the repo
- run ```pip install requirements.txt -r```
- run ```py manage.py runserver```
- run ```py manage.py runbot``` (on a seprate terminal)
