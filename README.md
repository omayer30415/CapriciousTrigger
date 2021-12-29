# Capstone

## Introduction

Capstone is a single-player shooters (TPS) game though it is a web game. Killing gangs and threats of country to ensure peace is the main purpose in this game. 


Main features of this game is:

- Choosing team
- Winning battles 
- Earning experience and money
- Buying wonderful equipments
- Promoting soldiers to general
- Leveling up
- Increasing power of generals and soldiers
- Saving progress

With all of these, this game can be played in all sizes of devices (computer, tablet or even in mobiles!)


## Distinctiveness and Complexity
 No doubt about that, this project is unique and complex than any other projects of not only cs50's projects but also projects that I have done in my life. 

 ### Comparison in general
  This project is unique because of:

   - More functionality 
   - More style
   - More creative
   - Animation
   - Testing
   - Security
   - Interactivity
   - Interesting
   - Mobile-responsive

 ### Comparison in each project
 This project is undoubtedly distinct from project 0 bacause it is **Full stack application** where project 0 is fully *front-end*. project 1 cannot stand with this, bacause it has database and has more complexity than that. Project 2 is little bit complex but that has no javascript, only a few, which is got from bootstrap. But this project has more interactivity in one page without reloading the entire page. Project 3 is a single-page application, but it is not that kind of application. In this project, only in the main game page, it has more functionality and interactivity than the whole project 3. Project 4 is a social website, but this project is a web-game application. Project 4 has some complexity in that, but that cannot be compare with this project bacause it has more API routes and in this projects lots of data are exchanged through API from client-side to sever-side or vice-versa. 

 With all of these, it is proved that this project is unique and complex than any other projects of the previous projects.


## Contents of files

 ### Outside the project

 #### Files created by Django by default
 1. `manage.py` provides the commnad-line utility for this project


 #### Created by me
 1. `requirement.txt` file stores python package related data which is essential to run this web-game application.
 
 ### Inside the project folder
   
 > `asgi.py` and `wsgi.py` are not changed, they are created by Django by default. `settings.py` sets the game options and `urls.py` has the main route connections of the project.     

### Inside my application

There are only one app in the project: **singlePlayer**. In that app:
 
 #### Files created by Django by default
 1. In `views.py`, there are functions for each of the view of the game.

 2. In `urls.py`, all routes related to the web-game are included.

 3. In `tests.py`, several tests are done to ensure that the game application bahaves as the way it is expected to.
 
 4. `models.py` stores all the models of the game.

 5. `apps.py` has only the *AppConfig* class created by Django by default.

 6. `admin.py` registers the models in the administration panel to simplify data-entry.

 #### Created by me
 1. In `serializers.py`, classess inherited from *Django rest framework*'s *ModelSerializer* class, are created, which serialize the models created in the `models.py` module to back-and-forth API data from client-side to server-side or vice-versa.

 2. The `source.py` module is the source of some utility functions, which is used to simplify game functions.

 3. **templates** folder stores all `Html` files. There are two sub-folders in this folder. One is **game**, another is **singlePlayer** folder.
 
    In **singlePlayer** folder, there are 5 `Html` files, `layout.html`, `index.html`, `choose.html`, `login.html`, `register.html`.

    i. `layout.html` structures the layout of the other three `Html` files.

    ii. `index.html` structures the view of the index page of the game.

    iii. `choose.html` structures the view of the choosing team page.

    iv. `login.html` structures the login page.

    v. `register.html` structures the registration page of the game

    In **game** folder, there are four `Html` files: `layout.html`, `cabinet.html`, `game.html`, `shop.html`.
    
    i. `layout.html` designs the layout of the other three `Html` files.

    ii. `cabinet.html` file is the view of the general's room and promotion room of the game. 

    iii. `game.html` file structures the main view of the game.

    iv. `shop.html` file is the shop of the game by which gamers are able to buy equipments for the generals and the soldiers.

    

 4. **static** folder stores all `css` and `javascript` files, which is used to style those `Html` files and adds interactivity to that. There are two sub-folders in this folder. One is **css** and the other is **JSbundle**.
    In **css** folder:

     i. `styles.css` file styles the index page and the choosing team page.

     ii. `cabinet.css` file styles the cabinet room of the generals and soldiers.

     iii. `game.css` file styles the main game page.
     
     
     In **JSbundle** folder:    

     i. `choose.js` file adds interactivity to the choosing team page.

     ii. `cabinet.js` file adds interactivity to the cabinet room.

     iii. `game.js` file adds interactivity the main game.
        
## Run my application
 **Steps to follow:**

 1. Create a superuser.
 2. Run the server
 3. Go to the admin panel.
 4. Create **Teams** and some **Generals** associated with that team. Also add some equipments in the **Products** table. But Remember, your *product* **category** must be **Cap** or **Helmet**.
 5. Come back to the index page.
 6. Click **New Game**
 7. Click **See the Generals** to see the generals, then click **Take Team** to take that team as your team
 8. Then you will be in the cabinet. Here you can click on a **general's name** to see the attributes of the general.
 9. Click **Start Game** to start main game.

 10.Your army will be on the top-side of the screen. On the other side, enemy generals and soldiers will take their place. Click any of your **general** or **soldier** to select him and then click an opponent **general** or **soldier** to kill him.

 11. If you missed the shot, you will see a small animation which messages you **Miss**, to ensure that you miss the shot. If you successfully hit your enemy, the message will say **-1**. And if your targeted enemy's all life are lost, then the message will say **Killed** and you will see that general or soldier disappears.Killing soldiers or generals will automatically update the score count of your team or the opponent team. 

 12. You do not have to select your army every time you shot an enemy, once you select a general or soldier, the general or soldier will be selected until you select another general or soldier.

 13. If you successfully kill most of your enemy's soldier or general, you will **WON** the match and in between you and your enemy, a big message will be shown that you have won the match. Then you see a button called **next**, click that button, if you do so, your gaming progress will be save and your **experience** and **money** will increase, and you will be redirected to the cabinet.

 14. You can buy additional equipments in the shop by your money. To buy any cap or helmet, click **Buy** to buy any cap or helmet. If you buy a cap, all of your generals will have that cap and the multiplication of the number of your generals and the price of the product will be the final price of the product and your money will cut based on the fianl price of the product. Helmet can also be bought by the same process as the cap buying process does. 

 15. The **power** of the **Cap** or **Helmet** will increase the defense of your generals or soldiers.

 As may times you wish to, you can play the game and enjoy!

 ## Additional Information Stuff Should Know

 *Dear grading stuff*,
 
 - When you are creating **Teams**, I recommend you to create four teams. **Star**,**Patriot**,**Jungle Warriors**,**Gangstars**. You can add additional teams, if you want to, but without these teams, I think the game will less interesting to you. 
 - If you stuck at getting free images, I recommend you to get images from [clipart-library](http://clipart-library.com/free/army-helmet-png.html) . 
 - If you find bugs in my code, please message me so that I can fix that problem and can learn more. 
 
## Conclusion

When you run the application, you will see yourself, how it is. Everything should not be said, something must need to hide to surprise.
