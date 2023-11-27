
"""
IN ORDER TO RUN THIS PROJECT:
    GO TO TERMINAL and type the following:
 -> $ cd downloads
 -> $ cd SahilKakkad_BrandonPizano_FinalProject
 -> $ python3 FlappyBird.py
 """

"""USE SPACEBAR TO MOVE BIRD"""

import pygame, sys, random
pygame.init()

def draw_floor():
    screen.blit(floor_surface,(floor_x_pos,680)) # adds the top left of floor_surface at (0,680)
    screen.blit(floor_surface,(floor_x_pos + 500,680)) #adds another floor_surface to the right of it

def create_pipe():
    """ First sets the pipe position to a random height for
    the list of potential pipe heights. The function then
    returns the two rectangles it creates, one for the top
    pipe and one for the bottom. """
    random_pipe_pos = random.choice(pipe_heights)
    bottom_pipe = pipe_surface.get_rect(midtop = (610,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (610, random_pipe_pos - 230))
    return bottom_pipe,top_pipe

def move_pipes(pipes):
    """ In order to simulate the bird's movement, the pipes will be
    moving from right to left (opposite of the way the bird would
    be going). Each pipe is moved 5 pixels and a list with each
    adjusted pipe is returned to show the pipes after "moving". """
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    """ Displays the pipes on the screen. If the pipe is
    located below the base, it is a bottom pipe and does
    not need to be flipped. If it is a top pipe it needs
    to be flipped as the pipe would face the wrong way. """
    for pipe in pipes:
        if pipe.bottom >= 780:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe,pipe)

def check_collision(pipes):
    """ This function utilizes the collide method for rectangles to check
    if the bird rectangle hit the pipe rectangle. If there is a
    collision the function returns false and leads to the game ending.
    To check whether the bird rectangle is still on the screen, both
    the top and bottom bounds are tested in the if statement - this
    would once again lead the game to end. If the bird is in the display
    and does not collide with the pipe, the game continues running. """
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= 680:
        death_sound.play()
        return False
    return True

def rotate_bird(bird):
    """ Rotates the bird and returns the new rotated bird. """
    new_bird = pygame.transform.rotozoom(bird,-bird_movement*3,1)
    return new_bird

def bird_animation():
    """ Picks the bird from the two different frames
    and creates a rectangle at the previous bird's
    center so the position is not updated. The
    function returns the new bird and its rectangle. """
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    """ This function checks between two game states and displays the
    score accordingly. If the game is still running, the score is
    rendered in a white font at the top of the screen. If the game
    is over, the same current score is displayed but the high score
    is also added in the same color at the bottom of the display. """
    if game_state == "main_game":
        score_surface = game_font.render(str(int(score)),True,(255,255,255)) #RGB tuple
        score_rect = score_surface.get_rect(center = (250, 75))
        screen.blit(score_surface,score_rect)

    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}',True,(255,255,255)) #RGB tuple
        score_rect = score_surface.get_rect(center = (250, 75))
        screen.blit(score_surface,score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}',True,(255,255,255)) #RGB tuple
        high_score_rect = high_score_surface.get_rect(center = (250, 630))
        screen.blit(high_score_surface,high_score_rect)

def update_score(score, high_score):
    """ This function simply updates the high score if
    there is a score higher than the previous record. """
    if score > high_score:
        high_score = score
    return high_score

#--SCREEN--
screen = pygame.display.set_mode((500,780)) # creates the screen that is displayed
#--TIMER--
clock = pygame.time.Clock() # creates a clock object that tracks time
#--WRITING--
game_font = pygame.font.Font('04B_19.ttf',45) # sets the font for all test displayed


#-GAME VARIABLES-
gravity = 0.25 # constant falling motion of the bird
bird_movement = 0 # gravity and space bar clicks alter the movement --> rectangle is moved accordingly
game_active = True # condition to continue running game loop
score = 0 # initial score
high_score = 0 # initial high score


#-BACKGROUND-
"""loads the background image and fits it in the display"""
bg_surface = pygame.image.load('FlappyBirdImages/background-night.png')
bg_surface = pygame.transform.scale(bg_surface, (500,780))
#-FLOOR-
"""loads the base image and fits it in the display"""
floor_surface = pygame.image.load('FlappyBirdImages/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0


#BIRD-
""" Incorporates the animations for both the up and down flap and
    creates a list with those two frames. The index chooses the frame
    from the list and a rectangle is created from the chosen frame.
    The timer is set to perform BIRDFLAP every 200 milliseconds. """
bird_downflap = pygame.transform.scale2x(pygame.image.load('FlappyBirdImages/greenbird-downflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('FlappyBirdImages/greenbird-upflap.png').convert_alpha())
bird_frames = [bird_downflap, bird_upflap]
bird_index = 0 # picks specific surface from bird_frames
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100,390))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)
#---------------


#PIPES----------
""" Similar to bird, the pipe images are loaded and scaled to fit
    the display, an empty list of pipes is initialized  and the
    timer is set to perform SPAWNPIPE every 1.2 seconds. The three
    different height cases are initialized in a list at this stage. """
pipe_surface = pygame.image.load('FlappyBirdImages/pipe-blend.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = [] # list that holds rectangles with pipes
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200) #takes in the event that will be triggered every 1200 milliseconds
pipe_heights = [305,455,610]
#---------------


#GAMEOVER-------
""" Loads and scales the game over image and creates a
    rectangle to place it in the center of the display. """
game_over_surface = pygame.transform.scale(pygame.image.load('FlappyBirdImages/message.png').convert_alpha(),(300,480))
game_over_rect = game_over_surface.get_rect(center = (250, 350))
#---------------

#AUDIO-------
""" Loads each sound used in the game and sets
    the countdown for the sound made when a point
    is scored to ensure it plays every full second. """
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100
#------------


#--GAME LOOP--
while True:
    for event in pygame.event.get(): #keeps track of all events (keystrokes)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit() #shuts down the game completely

        if event.type == pygame.KEYDOWN: #if a key is pressed run the following
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 8
                flap_sound.play()
            """ When the space bar is pressed and the game is still active, the
                bird's movement is reset to 0 and moved "down" 8 pixels to make
                the bird jump and as a result play the wing flapping sound. """

            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100,390)
                bird_movement = 0
                score = 0
            """ When the space bar is pressed but the game is over, a new
                game is prepared by setting the score and movement to 0,
                while restarting the game with a new set of pipes and
                replacing the bird at the starting position. """

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
        """ When the type of event is SPAWNPIPE, the list of pipes is extended
            and has a pipe added to it to continue the motion of the game. """

        if event.type == BIRDFLAP:
            if bird_index < 1:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface,bird_rect = bird_animation()
        """ When the type of event is BIRDFLAP, the index is updated to
            continue alternating the up and down flapping bird frames. """

    screen.blit(bg_surface,(0,0)) #puts the background surface on the screen

    if game_active:

        #---Bird[game loop]---#
        """ When the game is active, gravity is constantly acting on the bird
            and it is updating the movement each frame. The bird is rotated in
            the game and the movement is added to the center of the rectangle.
            The rotated bird is added to the screen and check_collision is
            called to ensure the player did not make contact with the pipes. """
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)
        #----------#

        #---Pipes[game loop]---#
        """ The pipe list is updated by calling the move_pipes function
            and is then drawn on the screen to simulate the bird moving. """
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        #------------------------#

        #---Score[game loop]---#
        """ Updates the score by 0.01 every milliscond and calls score_display
            with the game currently running. The countdown for the sound is
            used to time the sound with each point earned. """
        score += 0.01
        score_display('main_game')

        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
        #----------------------#

    else:
        """ If the game is over, the screen is updated. The
            current and high score are displayed when the score_display
            function is called with the inactive game state. """
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')


    #---Floor in game loop---#
    """ The floor is redrawn with the updated position to make it seem
        as though the animation is moving. If the floor is entirely past
        the left boundry of the x-axis the x-pos is reset to 0"""
    floor_x_pos -= 1 #redraws the floor position so that it is updating and "moving"
    draw_floor()
    if floor_x_pos <= -500:
        floor_x_pos = 0
    #------------------------#

    pygame.display.update() # updates the display
    clock.tick(120) # Keeps framerate below 120 frames per second
