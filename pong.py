# Implementation of classic arcade game Pong

# To play, copy and paste code into Codeskulptor http://www.codeskulptor.org/ or visit http://www.codeskulptor.org/#user38_YnAr1o7lQ6ro2ON.py
# Player 1 controls paddles with W & S; Player 2 uses Up and Down arrows

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

paddle1_pos = HEIGHT / 2 - PAD_HEIGHT /2
paddle2_pos = HEIGHT / 2 - PAD_HEIGHT /2

paddle1_vel = 0.0
paddle2_vel = 0.0
paddle_acc = 3.0

p1_score = 0
p2_score = 0

def spawn_ball(direction):
    # initialize ball_pos and ball_vel for new bal in middle of table
    # if direction is RIGHT, the ball's velocity is upper right, else upper left
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    global RIGHT, LEFT
    
    # Add randomization to ball velocity
    if RIGHT == True:
        ball_vel = [random.randrange(2, 4), -random.randrange(1, 3)]
        RIGHT = False
    else:
        ball_vel = [-random.randrange(2, 4), -random.randrange(1, 3)]
        RIGHT = True
        
# define event handlers
def new_game():
    
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel
    global score1, score2  # these are ints
    global ball_pos
    global p1_score, p2_score
    
    paddle1_pos = HEIGHT / 2 - PAD_HEIGHT /2
    paddle2_pos = HEIGHT / 2 - PAD_HEIGHT /2
    
    paddle1_vel = 0.0
    paddle2_vel = 0.0
    paddle_acc = 2.5
    
    p1_score = 0
    p2_score = 0 
    
    spawn_ball(RIGHT)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    global paddle1_vel, paddle2_vel
    global p1_score, p2_score

    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # Bounce off the top and bottom walls
    if ball_pos[1] >= (HEIGHT - 1) - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    elif ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]

    # collides on left wall
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        # check if ball collides with paddle, else score
        if ball_pos[1] < paddle1_pos :
            p2_score += 1
            spawn_ball(LEFT)         
        elif ball_pos[1] > paddle1_pos + PAD_HEIGHT :
            p2_score += 1
            spawn_ball(LEFT)                    
        else:
            ball_vel[0] = -1.1 * ball_vel[0] 
            ball_vel[1] =  1.1 * ball_vel[1]
            
    # collides on right wall
    if ball_pos[0] >= (WIDTH - 1) - BALL_RADIUS - PAD_WIDTH :
        # check if ball collides with paddle, else score  
        if ball_pos[1] < paddle2_pos:
            p1_score += 1
            spawn_ball(RIGHT)
        elif ball_pos[1] > paddle2_pos + PAD_HEIGHT :  
            p1_score += 1
            spawn_ball(RIGHT) 
        else :
            ball_vel[0] = -1.1 * ball_vel[0]
            ball_vel[1] =  1.1 * ball_vel[1]

    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Yellow", "White")

    # update paddle's vertical position, keep paddle on the screen
    # paddle right
    paddle1_pos += paddle1_vel
    # Check if paddle 1 is moving off the screen
    if paddle1_pos <= 0.0  :	
        paddle1_pos = 0.0
    elif paddle1_pos >= HEIGHT - PAD_HEIGHT :
        paddle1_pos = HEIGHT - PAD_HEIGHT

    # paddle left
    paddle2_pos += paddle2_vel
    # Check if paddle is moving off the screen
    if paddle2_pos <= 0.0 :
        paddle2_pos = 0.0
    elif paddle2_pos >= HEIGHT - PAD_HEIGHT :
        paddle2_pos = HEIGHT - PAD_HEIGHT    

    # draw paddles
    # left
    canvas.draw_line((0 + HALF_PAD_WIDTH - 1, paddle1_pos), (0 + HALF_PAD_WIDTH -1, paddle1_pos + PAD_HEIGHT), PAD_WIDTH, 'Red')
    # right
    canvas.draw_line((WIDTH - HALF_PAD_WIDTH + 1, paddle2_pos), (WIDTH - HALF_PAD_WIDTH + 1, paddle2_pos + PAD_HEIGHT), PAD_WIDTH, 'Blue')

    # draw scores
    canvas.draw_text(str(p1_score), (WIDTH / 4, 100), 100, "Red")
    canvas.draw_text(str(p2_score), (WIDTH / 1.5, 100), 100, "Blue")

def keydown(key):
    global paddle1_vel, paddle2_vel
    
    # while key is down, keep moving
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel -= paddle_acc
    elif key==simplegui.KEY_MAP["s"]:
        paddle1_vel += paddle_acc 
        
    if key==simplegui.KEY_MAP["down"]:
        paddle2_vel += paddle_acc
    elif key==simplegui.KEY_MAP["up"]:
        paddle2_vel -= paddle_acc 

def keyup(key):
    global paddle1_vel, paddle2_vel
    
    # when keyup, don't move
    paddle1_vel = 0.0
    paddle2_vel = 0.0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", new_game)

# start frame
new_game()
frame.start()
