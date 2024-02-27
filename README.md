# Simple Minigames - Python Project

## Short Description
Simple Minigames is a collection of straightforward and entertaining 
mini-games designed for users seeking a quick gaming experience. 
The minimal functionality includes a main menu where users can choose 
from a selection of games. The project aims to implement a scoring system 
to encourage competition among users, resembling a simpler version of Friv. 
The application is written in Python, utilizing technologies such as Pygame 
for the frontend and SQL for data storage.

## Technologies Used
- Python
- Pygame
- Tkinter
- Natural Language Toolkit
- Python Imaging Library

## How to Run / Use

1. Install required dependencies.

   ```bash
   sudo apt install python3-pip
   pip install pygame
   python -m pip install --upgrade Pillow
   pip install tk
   sudo apt-get install python3-tk
   pip install nltk
   python
   >>> import nltk
   >>> nltk.download('words')
   ```

2. Run the application.
   ```bash
   make
   ```
3. Navigate through the main menu and enjoy playing the simple minigames.

## Team Members
Our team was composed of: 
1. Andreescu Andrei Valerian
2. Andronache Mădălina-Georgiana
3. Mihai Bianca-Ioana
4. Tarău Alexandru-Bogdan

### 1. Andreescu Andrei Valerian
   - **Contributions:**
     - Implemented the Wordle Game.
     - Designed and implemented the scoring system of the Wordle Game.
     - Integrated Tkinter for the frontend of the Wordle Game.
     - Implemented the Minesweeper Challenge.
     - Integrated Pygame for the frontend of the Minesweeper Challenge.
   - **Difficulties faced:**
     - Wordle-like game that adhered to the original Wordle's rules and mechanics   
     - Implementing a system to handle a vast dictionary of words
     - arranging the components on the  game board, particularly in terms of layout 
design and gameplay mechanics.
     
### 2. Andronache Mădălina-Georgiana
   - **Contributions:**
     - Implemented the main menu and game selection functionality.
     - Used Pygame for the frontend of the main menu.
     - Created the design of the main menu page.
     - Implemented the Football Pong Game.
     - Designed and implemented the scoring system of the Football Pong Game.
     - Integrated Pygame for the frontend of the Football Pong Game.
   - **Difficulties faced:**
     - Moving the paddles at the same time in different directions.
     - Changing the angle of the ball after each restart of the game.
     - Having a scoring system.
     
### 3. Mihai Bianca-Ioana
   - **Contributions:**
     - Implemented the Capture the Cat Game.
     - Designed and implemented the scoring system of the Capture the Cat Game.
     - Integrated Pygame for the frontend of the Capture the Cat Game.
     - Designed and implemented the scoring system of the Minesweeper Challenge.
   - **Difficulties faced:**
     - Aligning the game's requirements with the dimensions of the application window   
     - Conceptualizing the application's operational mode
     - Establishing seamless connections between the individual games and the main menu
     
### 4. Tarău Alexandru-Bogdan
   - **Contributions:**
     - Implemented the Turtle Warrior Game.
     - Designed and implemented the scoring system of the Turtle Warrior Game.
     - Integrated Pygame for the frontend of the Turtle Warrior Game.
     - Created all the sprites of the game.
   - **Difficulties faced:**
     - Implementing precise collision detection mechanisms.
     - Designing an intuitive and responsive menu system
     - Ensuring consistent frame rates via manual deltaTime implementation

## App description

### 1. Main Page
   - **Description:**
     - Navigate through the main menu of our Simple Minigames App, choose your
favorite mini-game, and start playing!
   - **Features:**
     - Players can enter their names for a personalized experience.
     - You can click on the logo of the game and the game will start.

### 2. Football Pong
   - **Description:**
     - Dive into the exciting world of Football Pong, a reimagined take on 
the classic 2-player Ping-Pong game infused with a football-themed twist. 
Get ready for a fast-paced and dynamic gaming experience that combines the thrill 
of sports with the simplicity of arcade fun.


   - **Gameplay Features:**

        #### 1. Football-Themed Action
        - Immerse yourself in the world of football with a game that combines 
the skills of Ping-Pong with the excitement of the soccer field.
        
        #### 2. 2-Player Competition
        - Engage in thrilling head-to-head matches. The right player can use 
the arrow keys, and the left player can use the WASD keys to control their 
paddles. The up and down keys (right player) and W and S keys (left player) 
are used to move the paddles.

        #### 3. Gadgets
        - **Speed Boost Gadget:**
             - Activate with the right arrow key (right player) or the D key 
(left player). This gadget changes the ball's speed upon contact with the 
player's paddle, adding an element of surprise to the game.

        - **Position Change Gadget:**
             - Activate with the left arrow key (right player) or the A key 
(left player). This gadget changes the y-coordinate of the player's paddle based
on the ball's position. Use strategic positioning to gain an advantage, even in 
the final seconds.
     
        #### 4. Score Tracking
        - When a player reaches the goal of 10 points, the game will stop, 
and the final screen will appear. Then, you can choose if you want to play 
again or return to the main page.
     
### 3. Turtle Warrior
   - **Description:**
     - The Turtle Warrior Defense Game is an action-packed adventure where you,
as a warrior with a massive shield on your back, defend against incoming spider
enemies from the NORTH, EAST, WEST, and SOUTH directions.
Using your shield to block ranged attacks and a trusty bow to fend off enemies,
the game intensifies over time, challenging you to survive against increasingly
difficult waves of enemies.


   - **Gameplay Features:**

        #### 1. Dynamic Gameplay
        - **Combat:**
             - Utilize a large shield on your back to block ranged attacks from
incoming spiders.
             - Employ a bow to attack enemies approaching from various
directions.

        - **Progressive Difficulty:**
             - Experience escalating challenges as the game advances.

        #### 2. Abilities
        - **Shield Power:**
             - Grants immunity to ranged attacks for a short duration, available
every 4 successful blocks.

        - **Piercing Arrow:**
             - Obliterates a whole line of enemies, obtainable every 10 kills.

        #### 3. Controls
        - Entirely keyboard-based gameplay. Use WASD or arrow keys to change
facing direction. Press SPACE to shoot.

        #### 4. Game End
        - The game concludes upon receiving 3 hits.

        #### 5. Menu
        - The game is paused.
        - **Options:**
             - Return to main menu.
             - Restart the game.
             - Adjust music and sound volume.
             For changing volume: Move to the sound/music icons, select them,
use A/D or left/right arrow keys to adjust volume, confirm with SPACE.
        - Icons receive a black outline when focused.
        - Navigate using WASD/arrow keys, select options with SPACE.

### 4. Capture the Cat Game

   - **Description:**
     - Dive into the captivating world of "Capture the Cat", an intriguing
and dynamic game where strategy meets fun. With two engaging game modes,
players are either pitted against a clever enemy or challenge each other
in a race to capture the elusive cat. Navigate through obstacles and
outsmart your opponents in this fast-paced game. Whether you prefer a 
solo challenge or the excitement of a 2-player showdown, this game
promises minutes of fun and strategic thinking.


   - **Gameplay Features:**

        #### 1.  One-Player Mode: The Strategic Chase
        - Navigate through a maze of bricks, each acting as an obstacle, making strategic moves to corner and capture the cat.
Stay alert! An intelligent enemy will try to catch you. Outmaneuver the enemy while keeping your focus on the cat.
   
        #### 2. Two-Player Mode: The Competitive Race
        - Each player controls a character in a shared maze, racing to be the first to trap the cat.
Both players face the same challenges, making it a fair and exciting competition.
Points are awarded to the player who captures the cat first. The game keeps track of each player's wins, adding a competitive edge.
   
        #### 3. Dynamic Game Environment
        - Each game generates a new maze layout, ensuring a unique experience every time.
Bricks and obstacles add complexity to the game, requiring tactical movement and planning.

        #### 4. Win Conditions and Score Tracking
        - Catch the cat to score points. In the two-player mode, the first player to catch the cat wins the round.
Keep track of your wins and progress throughout the game, adding motivation to improve and compete.

### 5. Minesweeper Challenge
   - **Description:**
     - Embark on a strategic journey with Minesweeper Challenge, a classic puzzle game
reimagined for modern gameplay. Test your logic and concentration as you
navigate a minefield, uncovering safe cells and marking dangerous ones to
clear the board without detonating any mines.


   - **Gameplay Features:**

        #### 1.  Classic Minesweeper Gameplay
        - Experience the timeless puzzle game with a familiar grid-based layout.
Each cell may hide a mine, and it's your task to uncover all safe cells
without triggering any hidden mines.
        
        #### 2. Customizable Grid Size
        - Adapt the challenge to your skill level by choosing from different grid sizes.
The larger the grid, the more mines you'll have to navigate, offering a more
complex and engaging experience.

        #### 3.  Flag Mode
        - Toggle the flag mode to mark suspected mines. Use this feature to keep track 
of dangerous cells. Activate flag mode by clicking on the designated button or by 
pressing the spacebar.

### 6. Wordle-like Game
   - **Description:**
     - Experience the classic word-guessing thrill with this Wordle-like game.
A perfect blend of challenge and fun, it is designed to test your vocabulary 
and strategic thinking. Each guess requires you to deduce the hidden word 
through a process of elimination and clever guesswork.

       
   - **Gameplay Features:**

        #### 1.  Intuitive Word Guessing
        - Each guess must be a valid 5-letter word. After each guess, the color of 
the tiles will change to show how close your guess was to the word.

        #### 2. Interactive Feedback
        - **Color-Coded Hints:**
          - Green Tile: The letter is in the word and in the correct spot.
          - Yellow Tile: The letter is in the word but in the wrong spot.
          - Grey Tile: The letter is not in the word.
        
        ### 3. Reset Functionality
        - The ability to reset the game at any point, giving a fresh start whenever needed.
        
        ### 4. End Game Options

        - Once a game concludes, either by guessing the word or running out of 
attempts, options to play again or return to the main menu are provided.
