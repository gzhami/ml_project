
# File: Texas Holdem Hand Strength Simulation Using Monte Carlo Techniques
# Author: Zihan 


import eventBasedAnimation 
import random

def royalFlush(ranks,suits):
    counter = 0 
    check = [10,11,12,13,14]
    card_num = 5
    for i in xrange(card_num):
        if suits.count(suits[i]) >= card_num: counter += 1
    for x in check: 
        if ranks.count(x) >= 1: counter += 1
    return counter >= card_num * 2

def five_sequence(ranks,i = 4):
    if i == len(ranks): return False
    a = ranks[i-4:i+1]
    for char in xrange(len(a)-1):
        if a[char] != a[char+1]-1:
            return five_sequence(ranks,i+1)
    return True

def straightFlush(ranks,suits):
    check_num = 3 
    flush = 5
    for i in xrange(check_num):
        if suits.count(suits[i]) >= flush and five_sequence(ranks):
            return True
    return False

def FourOfAKind(ranks,i = 3):
    check = 3
    if i == len(ranks): return False
    a = ranks[i-check:i+1]
    for char in xrange(len(a)-1):
        if a[char] != a[char+1]:
            return FourOfAKind(ranks, i+1)
    return True

def FullHouse(ranks):
    check = 0
    counter = 3
    compare = 5 # Full House!
    for rank in ranks:
        if ranks.count(rank) >= counter: check += 1
        elif ranks.count(rank) >= 2: check += 1
    return check >= compare

def Flush(suits):
    check = 3
    counter = 5
    for i in xrange(check):
        if suits.count(suits[i]) >= counter:
            return True
    return False

def Straight(ranks):
    if five_sequence(ranks):
        return True
    return False

def ThreeOfAKind(ranks):
    deck = 7
    threeOfKind = 3
    for i in xrange(deck - threeOfKind):
        if ranks.count(ranks[i]) >= threeOfKind:
            return True
    return False

def TwoPair(ranks):
    twopair = 4
    check = 0
    pair = 2
    deck = 7
    for i in xrange(deck):
        if ranks.count(ranks[i]) >= pair:
            check += 1
    return check >= twopair

def OnePair(ranks):
    check = 0
    deck = 7
    for i in xrange(deck):
        if ranks.count(ranks[i]) > 1:
            check += 1
    return check >= 2

def convert(hand):
    # This function converts hand that has letter values into integer value
    # for example T is 10, K is 13. This is designed for simplification of 
    # calculation!
    len_hand = 14
    for i in xrange(len_hand):
        if hand[i] == 'T': hand[i] = '10'
        if hand[i] == 'J': hand[i] = '11'
        if hand[i] == 'Q': hand[i] = '12'
        if hand[i] == 'K': hand[i] = '13'
        if hand[i] == 'A': hand[i] = '14'
    return hand

# We check all possible hands, from the most powerful ones
# to the less power ones. Notice, we assigned a value to each of these
# hands, in order to further compare their strength!
# Notice, if we have failed all the combinations, we then just return the 
# largest value in the hands!
def strength(h):
    # Strength takes one parameter, hand and evaluate the strength!
    h = convert(h)
    ranks = []
    suits = []
    two_hands = 14
    for i in xrange(two_hands):
        if i % 2 == 0:
            ranks += [eval(h[i])] # seven integers!
        else: suits += h[i]
    strength = None
    ranks = sorted(ranks) 
    if royalFlush(ranks,suits): strength = 100
    elif straightFlush(ranks,suits): strength = 90
    elif FourOfAKind(ranks): strength = 80
    elif FullHouse(ranks): strength = 70
    elif Flush(suits): strength = 60
    elif Straight(ranks): strength = 50
    elif ThreeOfAKind(ranks): strength = 40
    elif TwoPair(ranks): strength = 30
    elif OnePair(ranks): strength = 20
    else:
         strength = max(ranks)
    return strength

def randomSettings(hand):
    # The set contains all the possible combination! 52 in total. This is 
    # basically just the deck!
    Set = [['2', 's'], ['2', 'h'], ['2', 'd'], ['2', 'c'], ['3', 's'], 
    ['3', 'h'], ['3', 'd'], ['3', 'c'], ['4', 's'], ['4', 'h'], ['4', 'd'], 
    ['4', 'c'], ['5', 's'], ['5', 'h'], ['5', 'd'], ['5', 'c'], ['6', 's'], 
    ['6', 'h'], ['6', 'd'], ['6', 'c'], ['7', 's'], ['7', 'h'], ['7', 'd'], 
    ['7', 'c'], ['8', 's'], ['8', 'h'], ['8', 'd'], ['8', 'c'], ['9', 's'], 
    ['9', 'h'], ['9', 'd'], ['9', 'c'], ['T', 's'], ['T', 'h'], ['T', 'd'], 
    ['T', 'c'], ['J', 's'], ['J', 'h'], ['J', 'd'], ['J', 'c'], ['Q', 's'], 
    ['Q', 'h'], ['Q', 'd'], ['Q', 'c'], ['K', 's'], ['K', 'h'], ['K', 'd'], 
    ['K', 'c'], ['A', 's'], ['A', 'h'], ['A', 'd'], ['A', 'c']]
    Set.remove(hand[:2])
    try: Set.remove(hand[2:])
    except: pass 
    community = []
    num_community = 5
    for i in xrange(num_community):
        card = random.choice(Set)
        Set.remove(card)
        community += card
    player2 = []
    num_players = 2
    for i in xrange(num_players):
        card = random.choice(Set)
        Set.remove(card)
        player2 += card
    return community, player2

def player_one_win(hand,player2,community):
    combinationOne = hand + community
    combinationTwo = player2 + community
    strengthOne = strength(combinationOne)
    strengthTwo = strength(combinationTwo)
    if strengthOne > strengthTwo:
        return True
    return False

def strengthSimulation(trials,hand):
    # Finally, we use Carlo Monte Method to calculate the chance of winning!
    win = 0
    loss = 0 
    hand = hand
    for trial in xrange(trials):
        player2 = randomSettings(hand)[1]
        community = randomSettings(hand)[0]
        if player_one_win(hand,player2,community):
            win += 1
        else:
            loss += 1
    return (float(win)/trials) * 100 

def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)

class Board(object):
    def __init__(self,w,h,unit):
        self.w = w
        self.h = h
        self.u = unit
        self.deck = 52
        self.num_deck = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
        self.suit = ['s','h','d','c']
        self.grid = [[('n1','suit1','n2','suit2')] * self.deck] * self.deck

    def draw(self,canvas):
        w,h,u = self.w,self.h,self.u
        canvas.create_rectangle(0,0,w,h,fill = "pink")
        num_card = 52
        margin = 90
        d = self.num_deck
        s = self.suit
        for row in xrange(num_card):
            for col in xrange(num_card):
                (x0,y0) = (margin+u*row,margin+u*col)
                (x1,y1) = (x0 + u, y0 + u)
                canvas.create_rectangle((x0,y0),(x1,y1),
                                    fill = rgbString(row*20/4,col*20/4,128))

class Axis(object):
    def __init__(self,w,h):
        self.w = w
        self.h = h
    def draw(self,canvas):
        w,h = self.w,self.h
        suit,unit = 4,10
        margin = 90
        # let's draw the rows first!
        num_deck = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
        x0,y0 = (margin+unit*2,h-margin+2*unit)
        for i in xrange(len(num_deck)):
            canvas.create_text(x0 + i * suit * unit, y0,
                    text=str(num_deck[i]),fill="black", font='Arial 15 bold')
        # Now, let's draw the colums!
        x1,y1 = (margin-2*unit,margin+unit*2)
        for i in xrange(len(num_deck)):
            canvas.create_text(x1, y1 + i * suit * unit,
                    text=str(num_deck[len(num_deck)-i-1]),fill="black", 
                                                    font='Arial 15 bold')

class bonusTexasHoldEmVisualizer_Main(eventBasedAnimation.Animation):
    def onInit(self):
        self.unit = 10 
        # the size of the grid!
        self.board = Board(self.width,self.height,self.unit)
        self.axis = Axis(self.width,self.height)
        self.deck = 52
        self.num_deck = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
        self.suit = ['s','h','d','c']
        deck = 52
        self.grid = [['','','',''] * deck] * deck
        self.temp = 0
        self.Board = []
        for value in xrange(len(self.num_deck)):
            for suit in xrange(len(self.suit)):
                self.Board += [[self.num_deck[value],self.suit[suit]]]
        for row in xrange(deck):
            for col in xrange(deck):
                self.grid[row][col] = self.Board[row]+self.Board[col]
        self.strength = "Try Click the Graph! Be Patient! Python is slow"

    def onDraw(self,canvas):
        margin = 50
        self.board.draw(canvas)
        self.axis.draw(canvas)
        canvas.create_text(self.width/2,margin,
                    text=str(self.strength),fill="black", font='Arial 15 bold')

    def onMouse(self,event):
        strength = self.checkLocation(event.x, event.y)
        self.strength = (str(strength[1]) + '\n' + 'Average Win % = ' +
                        str(strength[0]))

    def checkLocation(self,x, y):
        margin = 90
        cellWidth = 10
        cols,rows = 52,52
        board = self.grid 
        # 52*52 grids!
        strength = "Try Click the Graph! Be Patient! Python is slow! "
        hand = None
        for row in xrange(rows):
            for col in xrange(cols):
                left = margin + cellWidth * col
                top = margin + cellWidth * row
                if ((x > left and x < left + cellWidth) and
                    (y > top and y < top+ cellWidth)): 
                    hand =  self.Board[cols-1-row]+self.Board[col]
                    strength = strengthSimulation(1000,hand)
        return [strength,hand]

def bonusTexasHoldEmVisualizer():
    bonusTexasHoldEmVisualizer_Main(width =700,height=700,timerDelay=30).run()

bonusTexasHoldEmVisualizer()


