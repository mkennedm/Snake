![snake-full](https://github.com/mkennedm/Snake/assets/8769212/a1d2b337-3b80-449d-ae5c-7cf849c1fdf3)

If you haven't played snake before, then you're at least familiar with how the game works. I'll spare you an explanation of its simple and ubiquitous design. Instead I'll use this page to explain why I chose to make it and what's different about my version.

This was built the summer after completing one of my favorite college courses, CS 235 Algebraic Algorithms with Professor Lapets. My enjoyment lied not just in the content, but also how the material was covered. All of the assignments were in Python, a language I had never used before. I think our professor recognized early on that I wasn't the only person in that unfortunate position. Lectures were taught with a Python interpreter running on the projector and he graciously fielded basic questions about how the language performed in addition to more specific queries about the course material. Python may be one of the more beginner friendly programming languages out there, but I found it intimidating to pick up in a short time frame. By the end of the semester I was beyond comfortable with the language and today it's my first choice for projects I know won't require much horsepower.

After building [Minesweeper](https://github.com/mkennedm/Minesweeper) that summer, I was itching to do something on a similar scale in Python. The result was snake.py. For this project, I used the popular [Pygame](https://www.pygame.org/) library. All I had to focus on was Snake's logic. Pygame handles things like reading input from the mouse and keyboard, generating the window, and other low-level subroutines needed for any game to run.

As I reached the end of development, I found myself playing the game as much as I was programming in order to test it. Compared to the other games I've made Snake has the distiction of being the only one that isn't turn based. It requires a degree of manual dexterity that I just don't have. I tried to mitigate this challenge by reducing the snake's movement speed (one of the reasons the game has three difficulty settings), but it wasn't enough. Eventually, I got the idea to just teach the game how to play against itself.

Having witnessed the success of a game tree in Connect 4, I tried using one for Snake's artificial intelligence. The results were disastrous for the same reason I kept losing. Game trees make decisions too slowly even when they're pruned efficiently. The final version of the AI uses a much simpler algorithm that compares the snake's body and direction to the location of the food. It still dies eventually (the game is designed so even a perfect player will lose in the end) and takes some odd routes, but the AI performs much better than I can. The [best score I've ever seen the AI attain](https://github.com/mkennedm/Snake/blob/master/ai_comparison.txt) is 960. It gets 10 points for every piece of food it eats which means it got 96 pieces in that run. The AI can be triggered by selecting the "Demo" option in the main menu underneath the three difficulty settings. In Demo mode, the snake's speed is fixed to the same rate that it would move on the player controlled Hard difficulty.

After multiple failed efferts at converting my Python code into a single executable file, I've decided to make the [raw files downloadable here](https://github.com/mkennedm/Snake/blob/master/snake.zip).  That zip file contains the most recent version of snake.py which I updated to run on the 32 bit Python 3.6. You'll also need Pygame for the version of Python installed. I've also uploaded my entire Python folder in case of any issues getting the necessary libraries to install. If you don't want to go through the trouble of preparing the environment (which I won't blame you for at all), there's video of the game linked below. The AI demo starts at [0:53](https://youtu.be/aZHz5M4_hz4?t=53).

https://youtu.be/aZHz5M4_hz4
