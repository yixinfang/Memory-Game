'''
    CS5001
    Fall 2020
    Project
    Yixin Fang
    12122020



'''


from turtle import TK, TurtleScreen, Turtle, Shape, _Screen, ScrolledCanvas, _Root, Screen
import random
import time
import math 
import copy
import turtle
import os

gameTitle = "Memory_Matching_Game"

nrows = 3  # number of rows in grid
ncols = 4  # number of cols in grid

MAIN_BLOCK_LEFT = -350
MAIN_BLOCK_RIGHT = 100
MAIN_BLOCK_TOP = 300
MAIN_BLOCK_BOTTOM = -200
CANVAS_SIZE_X = 810
CANVAS_SIZE_Y = 800
CARD_WIDTH = 100
CARD_HEIGHT = 175
CARD_PADDING = 10

my_turtle = turtle.Turtle()
score_turtle = turtle.Turtle()
screen = turtle.Screen()
screen.title(gameTitle)
    
class CardClick:
    card_stamp = -1
    back_stamp = -1
    def __init__(self, x=-1, y=-1, img_id=-1, filename=""):
        self.x = x
        self.y = y
        self.img_id = img_id
        self.filename = filename
        if y > MAIN_BLOCK_TOP or y < MAIN_BLOCK_BOTTOM or \
            x > MAIN_BLOCK_RIGHT or x < MAIN_BLOCK_LEFT:
            raise ValueError

    def __eq__(self, other):
        return self.filename == other.filename

    def __str__(self):
        return str(self.img_id) + " " + self.filename      

    def displayCard(self):
        self.card_stamp = displaySingleCard(str(self.img_id), self.x, self.y)

    def displayBack(self):
        self.back_stamp = displaySingleCard("back_" + str(self.img_id), self.x, self.y)

    def deleteStamps(self):
        my_turtle.clearstamp(self.card_stamp)
        my_turtle.clearstamp(self.back_stamp)


class Players:
    def __init__(self):
        self.name = ""
        self.total_image = 0
        self.guess = 0
        self.is_quitted = False
        self.total_guess = 0
        self.right_guess = 0
        self.global_dictionary = {}
        self.back_card_stamps = [0] * self.total_image
        self.last_click = CardClick() # last_click is an object
        self.second_last_click = CardClick() #second_last_click is another object
    def bad_init(self):
        if total_image < 8 or total_image == 9 or total_image == 11 or total_image > 12:
            raise ValueError
    def __eq__(self, other):
        if self.total_image == other.total_image and \
           self.guess == other.guess and self.is_quitted == other.is_quitted:
            return True
        return False
    def __str__(self):
        return self.name + ' ' + str(self.right_guess)+' '+ str(self.total_guess)
    def score(self):
        return int(100*float(self.right_guess) / float(self.total_guess)) ### compare the ratio of correctness between different players 

current_player = Players()

def on_click(x, y):
    
    if y > MAIN_BLOCK_TOP or (-265< y < MAIN_BLOCK_TOP and x > MAIN_BLOCK_RIGHT) or \
       (MAIN_BLOCK_RIGHT < x < 205 and y < MAIN_BLOCK_BOTTOM) or x < MAIN_BLOCK_LEFT \
       or x > 265 or (205 < x < 265 and y < -305): 
        print("out of main block", x, y)
        return
    
    to_top = MAIN_BLOCK_TOP - y
    to_left = x - MAIN_BLOCK_LEFT
    if to_top % (CARD_HEIGHT+CARD_PADDING) < CARD_PADDING or \
       to_left % (CARD_WIDTH+CARD_PADDING) < CARD_PADDING:
       print("click on padding", x, y)
       return

    if 205 < x < 265 and -305 < y < -265:
        is_quitted = True
        screen.addshape("quitmsg.gif")
        my_turtle.penup()
        my_turtle.setposition(0,0)
        my_turtle.shape("quitmsg.gif")
        my_turtle.stamp()
        time.sleep(10)
        #screen.bye()
        return is_quitted
        

    row_grid = to_top // (CARD_HEIGHT+CARD_PADDING) 
    col_grid = to_left // (CARD_WIDTH+CARD_PADDING)
       
    x_face = MAIN_BLOCK_LEFT + CARD_PADDING*(col_grid+1) + CARD_WIDTH*col_grid + (CARD_WIDTH/2)
    y_face = MAIN_BLOCK_TOP - (CARD_PADDING*(row_grid+1) + CARD_HEIGHT*row_grid + (CARD_HEIGHT/2))
    a = int(row_grid)
    b = int(col_grid)
    id = a * ncols + b
    img_id = str(id)
    
    global current_player

    if current_player.global_dictionary.get(img_id):
        # this position has card

        current_player.second_last_click = current_player.last_click
        current_player.last_click = CardClick(x_face, y_face, id, current_player.global_dictionary.get(img_id))
        # display just clicked card
        current_player.last_click.displayCard()

        print("clicked on", row_grid, col_grid)
        print("last_click", current_player.last_click.__str__())
        print("second_last_click", current_player.second_last_click.__str__())
        # call update function    
        update(current_player)

        
def record_leader_board(player):
    write_list = [player.name, str(player.score()), str(player.total_guess)]
    with open("leader_board.txt", 'a') as fout:
        fout.write(" ".join(write_list) + "\n")
        
        
def update(current_player):

    if current_player.last_click.img_id != -1 and current_player.second_last_click.img_id != -1:

        # clicked 2 cards, this is one guess
        current_player.total_guess = current_player.total_guess + 1
        
        # we have 2 clicks, now do the check
        if  current_player.last_click == current_player.second_last_click:
            
            time.sleep(0.5)
            
            # Remove images from global_dictionary
            current_player.global_dictionary.pop(str(current_player.last_click.img_id))
            current_player.global_dictionary.pop(str(current_player.second_last_click.img_id))
            # Remove the backs
            my_turtle.clearstamp(current_player.back_card_stamps[current_player.last_click.img_id])
            my_turtle.clearstamp(current_player.back_card_stamps[current_player.second_last_click.img_id])
            
            #lst_score.append(score)
            #status_board("Score", scores)
            # A right guess
            current_player.right_guess = current_player.right_guess + 1
            if current_player.right_guess == current_player.total_image / 2:
                # Win
                win_msg()
                record_leader_board(current_player)
        else:
            # no match, reset to the card back
            time.sleep(0.5)
            current_player.last_click.displayBack()
            time.sleep(1)
            current_player.second_last_click.displayBack()

        current_player.last_click.deleteStamps()
        current_player.second_last_click.deleteStamps()
        # reset the clicks since this round match is done
        current_player.last_click = CardClick()
        current_player.second_last_click = CardClick()

        
        print("current player status: ", current_player.__str__())

        status_board(current_player.total_guess, current_player.right_guess)

def win_msg():         
    screen.addshape("winner.gif")
    my_turtle.penup()
    my_turtle.setposition(0,0)
    my_turtle.shape("winner.gif")
    my_turtle.stamp()  

def initial_player():

    answer_name = screen.textinput("CS5001 Memory", "Your Name: ")
    total_image = screen.textinput("Set Up", "# of Cards to Play: (8, 10 or 12)")
    if int(total_image) == 9 or int(total_image) == 11:
        total_image = screen.textinput("Set Up", "Neareast Even Number, Please")
    elif int(total_image) < 8 or int(total_image) > 12:
        total_image = screen.textinput("Set Up", "# of Cards to Play: (8, 10 or 12)")

    player = Players()
    player.name = answer_name
    player.total_image = int(total_image)
    player.back_card_stamps = [0] * int(total_image)
    return player
    
        
def initial_setup(): ## set up the playboard
    #t = turtle.Turtle()
    my_turtle.up()
    my_turtle.goto(-350,285)
    my_turtle.down()
    my_turtle.pensize(5)
    my_turtle.color("black")
    for i in range(4):
        if i % 2 == 0:
            my_turtle.forward(450)
        else:
            my_turtle.forward(535)
        my_turtle.right(90)

    my_turtle.hideturtle()
    my_turtle.up()
    my_turtle.goto(-350,-265)
    my_turtle.down()
    for i in range(4):
        if i % 2 == 0:
            my_turtle.forward(450)
        else:
            my_turtle.forward(40)
        my_turtle.right(90)

    my_turtle.hideturtle()
    my_turtle.up()
    my_turtle.goto(175,285)
    my_turtle.down()
    my_turtle.color("blue")
    for i in range(4):
        if i % 2 == 0:
            my_turtle.forward(140)
        else:
            my_turtle.forward(535)
        my_turtle.right(90)

    my_turtle.hideturtle()
    my_turtle.penup()
    my_turtle.setposition(-325,-295)
    my_turtle.write("Guess: ", font = ("Arial", 10, "bold", "normal"))
    my_turtle.setposition(-105,-295)
    my_turtle.write("Score: ", font = ("Arial", 11, "bold", "normal"))
    my_turtle.setposition(195,260)
    my_turtle.write("Leader: ", font = ("Arial", 14, "bold", "normal"))

    screen.addshape("quitbutton.gif")
    my_turtle.penup()
    my_turtle.setposition(235,-285)
    my_turtle.shape("quitbutton.gif")
    my_turtle.stamp()



def initAllImages(total_image = 12):

    ## loads card back images
    # the images are loaded as shapes to the screen, the number depends on players' input.

    cur_img_cnt = 0
    row_break_flag = False
    for row_ind in range(3):
        for col_ind in range(4):
            x = MAIN_BLOCK_LEFT + CARD_PADDING*(col_ind+1) + CARD_WIDTH*col_ind + (CARD_WIDTH/2)
            y = MAIN_BLOCK_TOP - (CARD_PADDING*(row_ind+1) + CARD_HEIGHT*row_ind + (CARD_HEIGHT/2))
            s = Shape("image", "card_back.gif")

            img_id = "back_" + str(cur_img_cnt)
            print ("img_id", img_id, s)
            screen.addshape(img_id, s)
            current_player.back_card_stamps[cur_img_cnt] = displaySingleCard(img_id, x, y)
            cur_img_cnt += 1
            if cur_img_cnt == total_image:
                row_break_flag = True
                break
        if row_break_flag:
            break
    
# small function, display image
def displaySingleCard(id, x, y):
    my_turtle.penup()
    my_turtle.setposition(x,y)
    my_turtle.shape(id)
    return my_turtle.stamp() #stamp is required to fix img

def shuffle(cards):
    shuffle_cards = cards.copy()
    random.shuffle(shuffle_cards)
    return shuffle_cards

def storeCards(total_image, card_list):
    my_turtle.hideturtle()
    shape_list_for_playing = (card_list[:(int(total_image/2))]) * 2
    shuffle_cards_for_playing = shuffle(shape_list_for_playing)
    print(shuffle_cards_for_playing)
    card_id_lst = []
    cur_img_cnt = 0
    row_break_flag = False
    for row_ind in range(3):
        for col_ind in range(4):
            x = MAIN_BLOCK_LEFT + CARD_PADDING*(col_ind+1) + CARD_WIDTH*col_ind + (CARD_WIDTH/2)
            y = MAIN_BLOCK_TOP - (CARD_PADDING*(row_ind+1) + CARD_HEIGHT*row_ind + (CARD_HEIGHT/2))
            s = Shape("image", shuffle_cards_for_playing[cur_img_cnt])
            img_id = str(cur_img_cnt)
            card_id_lst.append(img_id)
            screen.addshape(img_id, s)
            cur_img_cnt += 1
            if cur_img_cnt == total_image:
                row_break_flag = True
                break
        if row_break_flag:
            break
    dictionary = {}
    for i in range(len(card_id_lst)):
        dictionary[card_id_lst[i]] = shuffle_cards_for_playing[i]
    return dictionary

    
def status_board(total_guess, right_guess):
    score_turtle.clearstamps()
    score_turtle.penup()
    score_turtle.setposition(-270,-295)
    score_turtle.write(total_guess, font = ("Arial", 10, "bold", "normal"))
    
    score_turtle.setposition(-50,-295)
    score_turtle.write(right_guess, font = ("Arial", 10, "bold", "normal"))
    score_turtle.stamp()
          
def globalSetup(total_image):
    #initial_player()
    initial_setup()
    screen.setup(CANVAS_SIZE_X, CANVAS_SIZE_Y)
    initAllImages(total_image)


def printLeaderBoard(): ## print on leader board with 2 scores: correctness & correct guess
    lines = None
    if not os.path.exists("leader_board.txt"):
        return

    with open("leader_board.txt", 'r') as f:
        lines = f.readlines()
    
    lines = [line.split(" ") for line in lines]
    lines.sort(reverse=True, key=lambda x:float(x[1]))
    t1 = turtle.Turtle()    
    t1.hideturtle()
    
    line_start = 200
    for i in range(min(len(lines), 6)):
        line = lines[i]
        t1.penup()
        t1.setposition(200,200-i*30)
        write_str = " ".join(line)
        t1.write(write_str, font = ("Arial", 10, "bold", "normal"))
        
##  read card images specified by a configuration file,
##  allowing the program to use different sets of cards
def load_configuration_file(filename):
    with open(filename, mode = 'r') as infile:
        shape_list_from_file = []
        for each_file in infile:
            shape_list_from_file.append(each_file)
        return shape_list_from_file
            

    
def main():

    #ORIGIN_SHAPE_LIST = load_configuration_file('dog.txt') 
   
    ORIGIN_SHAPE_LIST = ["ace_of_diamonds.gif", "2_of_clubs.gif","2_of_diamonds.gif","3_of_hearts.gif", "jack_of_spades.gif", "queen_of_hearts.gif","jack_of_spades.gif"]
    card_list = copy.deepcopy(ORIGIN_SHAPE_LIST)

    #screen.bgcolor("lightgreen")
    #screen.tracer(False)
    players = []
    # Add latest palyer
    players.append(initial_player())
    global current_player
    current_player = players[-1]

    speed = 0
    globalSetup(current_player.total_image)
    printLeaderBoard()
    screen.update()
    current_player.global_dictionary = storeCards(current_player.total_image, card_list) ## store the imgs into the screen(not show yet)
    print(current_player.global_dictionary)

    print("all shapess", screen.getshapes())

    #initFrontImages()
    turtle.onscreenclick(on_click)
    #game = Game()
    #game.show_start_screen()

  
    turtle.mainloop()
    # my_turtle.hideturtle()
    
    


if __name__ == "__main__":
    main()

