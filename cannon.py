import turtle as t
import random

# Global variables
score = 0
lives = 3  # Number of lives
shuffles_left = 3  # Number of shuffles available
game_over = False

# Store initial cannon position and heading
initial_position = (-200, 10)
initial_heading = 20

# Create a turtle for messages
message_turtle = t.Turtle()
message_turtle.hideturtle()
message_turtle.penup()

# Score display
def update_scoreboard():
    scoreboard.clear()
    scoreboard.write(f"Score: {score}   Lives: {lives}   Shuffles Left: {shuffles_left}", 
                     align="center", font=("Arial", 16, "normal"))

def move_left():
    if not game_over:
        x = t.xcor()
        x -= 20  # Move left by 20 units
        if x < -300:  # Prevent moving out of bounds
            x = -300
        t.setx(x)

def move_right():
    if not game_over:
        x = t.xcor()
        x += 20  # Move right by 20 units
        if x > 300:  # Prevent moving out of bounds
            x = 300
        t.setx(x)

def turn_up():
    if not game_over:
        t.left(2)

def turn_down():
    if not game_over:
        t.right(2)

def move_blocks():
    for block in blocks:
        # Set block to a new random position within bounds
        block.goto(random.randint(-250, 250), random.randint(0, 200))

def create_new_block():
    block = t.Turtle()
    block.shape("square")
    block.color("brown")
    block.penup()
    block.goto(random.randint(-250, 250), random.randint(0, 200))
    blocks.append(block)

def reset_cannon():
    t.goto(initial_position)  # Reset to initial position
    t.setheading(initial_heading)  # Reset to initial heading

def fire():
    global score, lives, game_over
    if game_over:
        return  # Do nothing if the game is over
    
    ang = t.heading()
    t.setheading(ang)  # Ensure the cannon maintains its angle
    
    # Start firing
    while t.ycor() > 0:
        t.forward(15)
        t.right(5)

        # Check for collision with blocks
        for block in blocks:
            if t.distance(block) < 20:
                lives -= 1  # Decrease lives
                if lives <= 0:
                    game_over = True  # Set game over
                    t.color("red")
                    message_turtle.goto(0, 0)
                    message_turtle.write("Game Over! Press Esc to restart.", align="center", font=("Arial", 24, "normal"))
                else:
                    reset_cannon()  # Reset the cannon
                update_scoreboard()  # Update scoreboard
                return  # End firing and game

    d = t.distance(target, 0)
    t.sety(random.randint(10, 100))
    
    if d < 25:
        t.color("blue")
        message_turtle.goto(0, 0)
        message_turtle.write("Good!", align="center", font=("Arial", 15, "normal"))
        score += 1  # Increment score
        
        # Create a new block upon a successful hit
        create_new_block()

        move_blocks()  # Move existing blocks to new positions if hit is good
    else:
        t.color("red")
        message_turtle.goto(0, 0)
        message_turtle.write("Bad!", align="center", font=("Arial", 15, "normal"))
        score = 0  # Reset score on failure
    
    update_scoreboard()  # Update the scoreboard
    t.color("black")
    t.goto(initial_position)  # Return to starting position
    t.setheading(initial_heading)

def shuffle_blocks():
    global shuffles_left
    if shuffles_left > 0:
        move_blocks()  # Shuffle block positions
        shuffles_left -= 1  # Decrement the shuffles left
        update_scoreboard()  # Update scoreboard to reflect remaining shuffles

def restart_game():
    global score, lives, shuffles_left, game_over, blocks
    score = 0
    lives = 3
    shuffles_left = 3  # Reset shuffles
    game_over = False
    scoreboard.clear()
    update_scoreboard()
    reset_cannon()
    message_turtle.clear()  # Clear any previous messages
    
    # Reset blocks
    for block in blocks:
        block.hideturtle()  # Hide the old blocks
    blocks.clear()  # Clear the list of blocks

    # Recreate initial blocks
    for _ in range(5):
        create_new_block()

# Initial setup
t.speed(0)  # Fastest drawing
t.goto(-300, 0)
t.down()
t.goto(300, 0)

target = random.randint(50, 150)

t.pensize(3)
t.color("green")
t.up()
t.goto(target - 25, 2)
t.down()
t.goto(target + 25, 2)

# Create initial blocks
blocks = []
for _ in range(5):
    create_new_block()

# Scoreboard setup
scoreboard = t.Turtle()
scoreboard.hideturtle()
scoreboard.penup()
scoreboard.goto(0, 250)
update_scoreboard()  # Initialize scoreboard

t.color("black")
t.up()
t.goto(initial_position)  # Set to initial position
t.setheading(initial_heading)  # Set to initial heading

# Bind keys to functions
t.onkeypress(turn_up, "Up")
t.onkeypress(turn_down, "Down")
t.onkeypress(fire, "space")
t.onkeypress(shuffle_blocks, "r")  # Shuffle blocks when 'R' is pressed
t.onkeypress(restart_game, "Escape")  # Restart the game when 'Escape' is pressed

t.listen()
t.mainloop()
