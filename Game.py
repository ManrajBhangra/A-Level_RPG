import json
import random
import socket
import threading
import time

import pygame
from pygame import mixer

from OOP import Enemy
from OOP import Mage
from OOP import Knight
from Stack import stack

HOST = "127.0.0.1"
PORT = 12789

pygame.init()

mixer.init()

width = 800
height = 800
Background = pygame.image.load("cave_background.jpg")
Background = pygame.transform.scale(Background, (width, height))
Scroll = pygame.image.load("Scroll-PNG-Image.png")
Scroll = pygame.transform.scale(Scroll, (850, 200))
Scroll2 = pygame.image.load("Scroll-PNG-Image.png")
Scroll2 = pygame.transform.scale(Scroll2, (850, 800))
Scroll2 = pygame.transform.rotate(Scroll2, 90)

GameType = 0

White = (255, 255, 254)
Black = (0, 0, 0)
DGreen = (51, 121, 52)

screen = pygame.display.set_mode([width, height])
carry_on = True
wait = False
Turn = 0
Wave = 1
Enemies = stack()
end = True
MM = False
GO = False
Back = True

clock = pygame.time.Clock()

P1 = Knight(1, screen, "Knight", "H")
P1.rect.x = 51
P1.rect.y = 500

P2 = Mage(1, screen, "Mage", "H")
P2.rect.x = 80
P2.rect.y = 500

Players = {1: P1, 2: P2}

Player_Sprite_list = pygame.sprite.Group()
Player_Sprite_list.add(P1)
Player_Sprite_list.add(P2)

Enemy_Sprite_list = pygame.sprite.Group()

Font = pygame.font.SysFont("Kristen ITC", 18)
Font2 = pygame.font.SysFont("Kristen ITC", 14)
Font3 = pygame.font.SysFont("Kristen ITC", 65)


def Text(Message, screen, centre):
    ##### Text #######
    # Parameters :- Message:String, screen:pygame screen, centre: array of numbers
    # Return Type :- None
    # Purpose :- Display text onto the screen for player to read
    ###########################

    text = Font.render(Message, True, White)
    textRect = text.get_rect()
    textRect.center = centre
    screen.blit(text, textRect)
    pygame.display.flip()


def MainMenu():
    ##### MainMenu #######
    # Parameters :- None
    # Return Type :- None
    # Purpose :- Creates and displays the main menu on the screen
    ###########################
    screen.blit(Background, (0, 0))
    screen.blit(Scroll2, (0, -25))
    Text("Welcome, Press 1 for One Player and 2 for Two Player", screen, (400, 400))
    Text("Press I for Instructions", screen, (400, 500))
    Text("Press S for a story synopsis", screen, (400, 600))
    Line1 = Font3.render("Hunt of", True, White)
    Line1Rect = Line1.get_rect()
    Line1Rect.center = (400, 150)
    screen.blit(Line1, Line1Rect)
    Line2 = Font3.render("the Demon!", True, White)
    Line2Rect = Line2.get_rect()
    Line2Rect.center = (400, 250)
    screen.blit(Line2, Line2Rect)
    pygame.display.flip()


def Instructions():
    ##### Instructions #######
    # Parameters :- None
    # Return Type :- None
    # Purpose :- Creates and displays the instructions on the screen when needed
    ###########################
    screen.blit(Background, (0, 0))
    screen.blit(Scroll2, (0, -25))
    Text("Instructions", screen, (400, 100))
    Text("You will have control of a knight and mage throughout the game", screen, (400, 150))
    Text("In single player you will take control over both characters", screen, (400, 175))
    Text("In multiplayer, player one will take control of the knight", screen, (400, 200))
    Text("player two will have control over the mage", screen, (400, 225))
    Text("Both characters have a certain amount of Health points", screen, (400, 250))
    Text("and Special points which are abbreviated to HP and Sp", screen, (400, 275))
    Text("When it is your turn you will be presented with 3 actions", screen, (400, 325))
    Text("The first of these actions is Attack.", screen, (400, 375))
    Text("This is a very simple action where you attack one your enemies", screen, (400, 400))
    Text("The second action is your Special attacks", screen, (400, 450))
    Text("You will start the game with 1 Special attack and ", screen, (400, 475))
    Text("obtain up to 3 more for each character throughout the game", screen, (400, 500))
    Text("The final action is Blocking", screen, (400, 550))
    Text("Blocking will regain your SP and make you take", screen, (400, 575))
    Text("less damage from one Attack", screen, (400, 600))
    Text("Your goal is to defeat all waves of enemies and the Final Boss", screen, (400, 650))
    Text("Enemies will have the same arsenal of moves as you to select from", screen, (400, 675))
    Text("Press 5 to return to the previous Menu", screen, (400, 725))


def Story():
    ##### Story #######
    # Parameters :- none
    # Return Type :- None
    # Purpose :- Creates and displays the screen for the story synopsis
    ###########################
    screen.blit(Background, (0, 0))
    screen.blit(Scroll2, (0, -25))
    Text("Story", screen, (400, 100))
    Text("Two brothers, a knight and a mage, venture through a cave to", screen, (400, 200))
    Text("the underworld in hope to find a demon that lurks in its deepest", screen, (400, 250))
    Text("depth for revenge after their father went through this same cave", screen, (400, 300))
    Text("25 years ago. Together they must battle through hordes of", screen, (400, 350))
    Text("enemies to grow strong enough to defeat the demon, learning", screen, (400, 400))
    Text("new attacks along the way. They know that killing the demon", screen, (400, 450))
    Text("will not bring back their father, but the satisfaction of", screen, (400, 500))
    Text("vengeance is reason enough for them to both risk their lives...", screen, (400, 550))
    Text("Press 5 to return to the previous Menu", screen, (400, 650))


def background(TY):
    ##### Background #######
    # Parameters :- TY: integer
    # Return Type :- none
    # Purpose :- Creates the multiple backgrounds needed throughout the game and displays them
    # the TY integer refers to type and signifies which background needs to be made
    ###########################
    screen.blit(Background, (0, 0))
    screen.blit(Scroll, (-25, 0))
    for i in range(1, 3):
        if not Players.get(i).Dead:  # This 'if' statement checks if one of characters is dead and therefore display
            # the correct sprite
            if Players.get(i).type == "Knight":
                pygame.draw.rect(screen, (255, 0, 0),
                                 [91, 546, 120 * Players.get(i).health / Players.get(i).healthMax * 4 / 3, 7 * 2])
                pygame.draw.rect(screen, (255, 215, 0),
                                 [91, 560, 120 * Players.get(i).SpGauge / Players.get(i).SpGaugeMax * 4 / 3, 7 * 2])

            elif Players.get(i).type == "Mage":
                pygame.draw.rect(screen, (255, 0, 0),
                                 [187.5, 754, 120 * Players.get(i).health / Players.get(i).healthMax * 4 / 3, 7 * 2])
                pygame.draw.rect(screen, (255, 215, 0),
                                 [187.5, 768, 120 * Players.get(i).SpGauge / Players.get(i).SpGaugeMax * 4 / 3, 7 * 2])

    Player_Sprite_list.draw(screen)
    Enemy_Sprite_list.draw(screen)
    if TY == 1:  # This 'if' statement checks the TY variable to display the correct background needed with the correct
        # text
        Text(("It is your " + Players.get((Turn + 1)).type + "'s turn"), screen, (400, 50))
        Text("1 : Attack                2 : Special Attack              3 : Block", screen, (400, 100))
    elif TY == 3:
        Text("Select the special move you would like to use", screen, (400, 50))
        if Turn == 0:
            if len(P1.SpMoves) >= 4:
                Text("1 : Sword Strike 2 : Protect 3 : Empower 4 : Excalibur's Revenge 5 : Back", screen, (400, 100))
            elif len(P1.SpMoves) >= 3:
                Text("1 : Sword Strike 2 : Protect 3 : Empower 5 : Back", screen, (400, 100))
            elif len(P1.SpMoves) >= 2:
                Text("1 : Sword Strike 2 : Protect 5 : Back", screen, (400, 100))
            elif len(P1.SpMoves) >= 1:
                Text("1 : Sword Strike 5 : Back", screen, (400, 100))

        elif Turn == 1:
            if len(P2.SpMoves) >= 4:
                Text("1 : Heal 2 : Fireball 3 : Thunder 4 : Meteor Storm 5 : Back", screen, (400, 100))
            elif len(P2.SpMoves) >= 3:
                Text("1 : Heal 2 : Fireball 3 : Thunder 5 : Back", screen, (400, 100))
            elif len(P2.SpMoves) >= 2:
                Text("1 : Heal 2 : Fireball 5 : Back", screen, (400, 100))
            elif len(P2.SpMoves) >= 1:
                Text("1 : Heal 5 : Back", screen, (400, 100))

    elif TY == 4:
        Text(("You must wait " + str(P1.protectCooldown) + " more turns to use this move again"), screen, (400, 75))

    elif TY == 5:
        Text("It is the other player's turn", screen, (400, 75))

    elif TY == 6:
        Text("Congratulations, you leveled up", screen, (400, 50))
        Text("Your stats have increased", screen, (400, 100))

    pygame.display.flip()


def GiveXP(En):
    ##### GiveXP #######
    # Parameters :- En: An enemy
    # Return Type :- None
    # Purpose :- Gives the XP yield of the enemy just defeated to the knight and mage
    ###########################
    P1.adjust_XP(En)
    P2.adjust_XP(En)


def LowSP():
    ##### LowSP #######
    # Parameters :- None
    # Return Type :- None
    # Purpose :- Displays text on the screen saying that a character doesn't have enough XP to complete
    # a special attack
    ###########################
    background(2)
    Text("You don't have enough SP to complete this move", screen, (400, 50))
    time.sleep(1.5)


def Empower_check(P1):
    ##### Empower_check #######
    # Parameters :- P1: The knight
    # Return Type :- none
    # Purpose :- Increases the amount of turns the empower effect until it reaches 4 turns and is deactivated
    ###########################
    if 0 < P1.EmpowerTurns < 4:
        P1.EmpowerTurns += 1
    if P1.EmpowerTurns == 4:
        P1.Depower(P2)
        P1.EmpowerTurns = 5
        background(2)
        Text("Your empower has worn off", screen, (400, 50))
        time.sleep(1.5)


def receive_message(s, Self, P):
    ##### receive_message #######
    # Parameters :- s:server, self:Knight or Mage, P:other character
    # Return Type :- none
    # Purpose :- Allows the server to interact with the clients and has the client receive messages
    # from the server. These messages change variables within the knight and mage class which allows
    # the game to produce the actions completed from the other client. It also allows the second client
    # to know the enemy moves that were calculated on player one's client.
    ###########################
    while True:
        data = s.recv(1024)
        if not data:
            continue
        else:
            msg = json.loads(data.decode())

        if msg["Data"]["Move"] == "Attack":  # This 'if' statement reads the message from the server and updates
            # variables to allow for the moves to happen on the client
            P.Att = True

        elif msg["Data"]["Move"] == "En":
            if msg["Data"]["Target"] == 1:
                Self.En_Tar = 1
            elif msg["Data"]["Target"] == 2:
                Self.En_Tar = 2

            if msg["Data"]["Attack"] == "Attack":
                Self.En_Atts = 1
            elif msg["Data"]["Attack"] == "Special":
                Self.En_Atts = 2
            elif msg["Data"]["Attack"] == "Block":
                Self.En_Atts = 3

        elif msg["Data"]["Move"] == "SP":
            if msg["Data"]["SP"] == 1:
                P.SP1 = True
            elif msg["Data"]["SP"] == 2:
                P.SP2 = True
            elif msg["Data"]["SP"] == 3:
                P.SP3 = True
            elif msg["Data"]["SP"] == 4:
                P.SP4 = True

        elif msg["Data"]["Move"] == "Block":
            P.Bl = True

        elif msg["Data"]["Move"] == "Close":
            P.S_Cl = True


def wave1():
    ##### wave1 #######
    # Parameters :- None
    # Return Type :- None
    # Purpose :- Creates the enemies for the first wave
    ###########################
    Gob1 = Enemy(screen, "Goblin", 1, "E")
    Gob1.rect.x = 500
    Gob1.rect.y = 575
    Enemy_Sprite_list.add(Gob1)
    Enemies.push(Gob1)
    Gob2 = Enemy(screen, "Goblin", 1, "E")
    Gob2.rect.x = 450
    Gob2.rect.y = 500
    Enemy_Sprite_list.add(Gob2)
    Enemies.push(Gob2)
    Gob3 = Enemy(screen, "Goblin", 1, "E")
    Gob3.rect.x = 350
    Gob3.rect.y = 575
    Enemy_Sprite_list.add(Gob3)
    Enemies.push(Gob3)
    Gob4 = Enemy(screen, "Goblin", 1, "E")
    Gob4.rect.x = 300
    Gob4.rect.y = 500
    Enemy_Sprite_list.add(Gob4)
    Enemies.push(Gob4)


def wave2():
    ##### wave2 #######
    # Parameters :- None
    # Return Type :- None
    # Purpose :- Creates the enemies for the second wave
    ###########################
    Gob1 = Enemy(screen, "Goblin", 1, "E")
    Gob1.rect.x = 425
    Gob1.rect.y = 537.5
    Enemy_Sprite_list.add(Gob1)
    Enemies.push(Gob1)
    Skele1 = Enemy(screen, "Skeleton Warrior", 1, "E")
    Skele1.rect.x = 350
    Skele1.rect.y = 575
    Enemy_Sprite_list.add(Skele1)
    Enemies.push(Skele1)
    Skele2 = Enemy(screen, "Skeleton Warrior", 1, "E")
    Skele2.rect.x = 300
    Skele2.rect.y = 500
    Enemy_Sprite_list.add(Skele2)
    Enemies.push(Skele2)


def wave3():
    ##### wave3 #######
    # Parameters :- None
    # Return Type :- None
    # Purpose :- Creates the enemies for the third wave
    ###########################
    Mush1 = Enemy(screen, "Mushroom", 1, "E")
    Mush1.rect.x = 500
    Mush1.rect.y = 600
    Enemy_Sprite_list.add(Mush1)
    Enemies.push(Mush1)
    Mush2 = Enemy(screen, "Mushroom", 1, "E")
    Mush2.rect.x = 400
    Mush2.rect.y = 575
    Enemy_Sprite_list.add(Mush2)
    Enemies.push(Mush2)
    Mush3 = Enemy(screen, "Mushroom", 1, "E")
    Mush3.rect.x = 460
    Mush3.rect.y = 520
    Enemy_Sprite_list.add(Mush3)
    Enemies.push(Mush3)
    Mush4 = Enemy(screen, "Mushroom", 1, "E")
    Mush4.rect.x = 275
    Mush4.rect.y = 600
    Enemy_Sprite_list.add(Mush4)
    Enemies.push(Mush4)
    Mush5 = Enemy(screen, "Mushroom", 1, "E")
    Mush5.rect.x = 330
    Mush5.rect.y = 575
    Enemy_Sprite_list.add(Mush5)
    Enemies.push(Mush5)
    Mush6 = Enemy(screen, "Mushroom", 1, "E")
    Mush6.rect.x = 300
    Mush6.rect.y = 520
    Enemy_Sprite_list.add(Mush6)
    Enemies.push(Mush6)


def wave4():
    ##### wave4 #######
    # Parameters :- None
    # Return Type :- None
    # Purpose :- Creates the enemies for the fourth wave
    ###########################
    Ninja1 = Enemy(screen, "Ninja", 1, "E")
    Ninja1.rect.x = 400
    Ninja1.rect.y = 512.5
    Enemy_Sprite_list.add(Ninja1)
    Enemies.push(Ninja1)
    Ninja2 = Enemy(screen, "Ninja", 1, "E")
    Ninja2.rect.x = 300
    Ninja2.rect.y = 475
    Enemy_Sprite_list.add(Ninja2)
    Enemies.push(Ninja2)


def FinalBoss():
    ##### FinalBoss #######
    # Parameters :- None
    # Return Type :- None
    # Purpose :- Creates the final boss for the final battle
    ###########################
    Demon = Enemy(screen, "Demon", 1, "E")
    Demon.rect.x = -200
    Demon.rect.y = -25
    Enemy_Sprite_list.add(Demon)
    Enemies.push(Demon)
    mixer.music.stop()
    mixer.music.load("Final boss.mp3")  # Music from https://www.youtube.com/watch?v=BUqQtcij7Jc
    mixer.music.set_volume(0.7)
    mixer.music.play(-1)


def Win():
    ##### Win #######
    # Parameters :- none
    # Return Type :- none
    # Purpose :- Creates and displays the win screen for finishing the game
    ###########################
    screen.blit(Background, (0, 0))
    text = Font3.render("CONGRATULATIONS!", True, White)
    textRect = text.get_rect()
    textRect.center = (400, 200)
    screen.blit(text, textRect)
    text = Font3.render("YOU WIN!", True, White)
    textRect = text.get_rect()
    textRect.center = (400, 350)
    screen.blit(text, textRect)
    P1.image = pygame.transform.scale(P1.image, (120 * 5, 80 * 5))
    P2.image = pygame.transform.scale(P2.image, (250 * 3.5, 250 * 3.5))
    P2.image = pygame.transform.flip(P2.image, True, False)
    P1.rect.x = -50
    P1.rect.y = 350
    P2.rect.x = 150
    P2.rect.y = 160
    Player_Sprite_list.draw(screen)
    pygame.display.flip()
    mixer.music.stop()
    mixer.music.load("Win music.mp3")  # Music from https://www.youtube.com/watch?v=3zqNr0Qjo_M
    mixer.music.set_volume(0.7)
    mixer.music.play(-1)


def GameOver():
    ##### GameOver #######
    # Parameters :- none
    # Return Type :- none
    # Purpose :- Creates and displays the game over screen if the user loses the game
    ###########################
    screen.blit(Background, (0, 0))
    text = Font3.render("GAME OVER!", True, White)
    textRect = text.get_rect()
    textRect.center = (400, 200)
    screen.blit(text, textRect)
    text = Font3.render("Press 1 to try again", True, White)
    textRect = text.get_rect()
    textRect.center = (400, 350)
    screen.blit(text, textRect)
    text = Font3.render("or 2 to quit", True, White)
    textRect = text.get_rect()
    textRect.center = (400, 500)
    screen.blit(text, textRect)
    pygame.display.flip()


def Attack(Attacker, Target):
    ##### Attack #######
    # Parameters :- Attacker: Character being attacked, Target: Character about to be attacked
    # Return Type :- none
    # Purpose :- Makes the character move towards the opposing faction and attack them followed by
    # them moving back into position
    ###########################
    if Attacker.team == "E":
        Attacker.move_left()
    elif Attacker.team == "H":
        Attacker.move_right()
    background(2)
    if Attacker.team == "E":
        Text(("Enemy " + Attacker.type + " attacks your " + Target.type + " for " + str(int(
            Attacker.attack * 100 // (100 + Target.defense))) + " Damage"), screen, (400, 50))
    elif Attacker.team == "H":
        Text(("Your " + Attacker.type + " attacks enemy " + Target.type + " for " + str(int(
            Attacker.attack * 100 // (100 + Target.defense))) + " Damage"), screen, (400, 50))
    Attacker.attacking(Target)
    if Attacker.team == "E":
        Attacker.move_right()
    elif Attacker.team == "H":
        Attacker.move_left()


def SpAttack(Attacker, Target):
    ##### SpAttack #######
    # Parameters :- Attacker: Enemy that is attacking, Target: Knight or mage being attacked
    # Return Type :- none
    # Purpose :- Allows for enemies to attack use their special attack to attack the enemy.
    # The enemy moves left, attacks then moves right
    ###########################
    if Attacker.team == "E":
        Attacker.move_left()
    background(2)
    Text(("Enemy " + Attacker.type + " attacks your " + Target.type + " for " + str(
        int((Attacker.SpMoves.get("Damage") // 5) *
            Attacker.attack * 100 // (
                    100 + Target.defense))) + " Damage using its " + Attacker.SpMoves.get(
        "Move")) + "!", screen, (400, 50))
    if Attacker.team == "E":
        Attacker.move_right()
    Attacker.SpMove(Target)


def playerSpAttack(Attacker, Target, SpMove):
    ##### playerSpAttack #######
    # Parameters :- Attacker: Knight or Mage, Target: Enemy, SpMove: Integer
    # Return Type :- none
    # Purpose :- Allows for a knight or mage to complete one of their attacking special attack
    # on an enemy by moving right, attacking then moving left
    ###########################
    Attacker.move_right()
    background(2)
    damage = int(((Attacker.SpMoves.get(SpMove).get("Damage")) // 5) * Attacker.attack * 100 // (100 + Target.defense))
    Text((Attacker.type + " uses " + Attacker.SpMoves.get(SpMove).get(
        "Move") + " on " + Target.type) + " for " + str(damage) + " Damage!",
         screen, (400, 50))
    time.sleep(1.5)
    Attacker.move_left()
    Attacker.SpecialMove(SpMove, Target)
    if Attacker.type == "Knight":
        Empower_check(Attacker)


def player2Heal(Healer, Target):
    ##### player2Heal #######
    # Parameters :- Healer:Mage, Target: Knight
    # Return Type :- none
    # Purpose :- Allows the mage to use their heal special attack and heal the knight.
    ###########################
    Healed = (Target.healthMax * 0.1)
    if Target.health + Healed > Target.healthMax:
        Healed = Healed - (Target.health + Healed - Target.healthMax)
    Healer.SpecialMove(1, Target)
    Healer.move_right()
    background(2)
    Text(("Your " + Healer.type + " heals " + Target.type + " by " + str(int(Healed))),
         screen, (400, 50))
    time.sleep(1.5)
    Healer.move_left()


def player1Protect(Protector, Target):
    ##### player1Protect #######
    # Parameters :- Protector: Knight, Target: Mage
    # Return Type :- none
    # Purpose :- Allows the knight to use its protect special attack and not have either character take
    # damage from the next set of attacks from the enemy
    ###########################
    Protector.SpecialMove(2, Target)
    Protector.move_right()
    background(2)
    Text(("Your " + Protector.type + " protects your whole team"), screen, (400, 50))
    time.sleep(1.5)
    Protector.move_left()


def player1Empower(Empowerer, Target):
    ##### player1Empower #######
    # Parameters :- Empowerer: Knight, Target: Mage
    # Return Type :- none
    # Purpose :- Allows Knight to use empower special move and increase attack of both
    # characters move
    ###########################
    Empowerer.SpecialMove(3, Target)
    Empowerer.move_right()
    background(2)
    Text(("Your " + Empowerer.type + " uses " + Empowerer.SpMoves.get(3).get(
        "Move") + " to increase the power of your attacks!"), screen, (400, 50))
    time.sleep(1.5)
    Empowerer.move_left()


def playerSpAtt4(Attacker, Target):
    ##### playerSpAtt4 #######
    # Parameters :- Attacker: Knight or Mage, Target: Enemy
    # Return Type :- none
    # Purpose :- Allows knight and mage to use their fourth special attack which targets all
    # enemies
    ###########################
    for i in Target:
        Attacker.SpecialMove(4, i)
    Attacker.move_right()
    background(2)
    Text(("Your " + Attacker.type + " uses " + Attacker.SpMoves.get(4).get(
        "Move") + " on all enemies!"), screen, (400, 50))
    time.sleep(1.5)
    Attacker.move_left()


def playerBlock(Blocker):
    ##### playerBlock #######
    # Parameters :- Blocker: Knight or Mage
    # Return Type :- none
    # Purpose :- Increases players defence for a turn and increases their current SP
    ###########################
    if Players.get(Blocker + 1).SpGauge == Players.get(Blocker + 1).SpGaugeMax:
        Players.get(Blocker + 1).block()
        Players.get(Blocker + 1).move_right()
        Blocker += 1
        background(2)
        Text(("Your " + Players.get(Blocker).type + " is blocking but your SP is full"), screen, (400, 50))
        time.sleep(1.5)
        Players.get(Blocker).move_left()

    else:
        Players.get(Blocker + 1).block()
        Blocker += 1
        Players.get(Blocker).move_right()
        background(2)
        Text(("Your " + Players.get(Blocker).type + " is blocking and regained some SP"), screen, (400, 50))
        time.sleep(1.5)
        Players.get(Blocker).move_left()


def AI_Attack(HP, Enemies, index, Target, Attacker):
    ##### AI_Attack #######
    # Parameters :- HP: integer, Enemies: list of enemies, index: integer, Target: Knight or Mage, Attacker: Enemy
    # Return Type :- Boolean
    # Purpose :- More complex part of the enemy AI which will discover if one of your characters can be killed
    # this turn and returns True if not but False if not meaning the function is only run once and can be called
    # upon by itself
    ###########################
    if len(Enemies.Enemies) - index - 1 >= 1:  # Creates a stopping condition for the recursive function
        for i in (0, len(Enemies.Enemies) - index - 1):
            Attacky = Enemies.Enemies[i]
            if HP - (Attacky.attack * 100 // (100 + Players.get(Target).defense)) <= 0:
                # 'if' and 'elif' check to see if character is killable
                Attack(Attacker, Players.get(Target))
                if GameType == "Multi":
                    P1.Server_En(s, playerNum, Target, "Attack")
                return True
            elif Attacky.SpGauge - Attacky.SpMoves.get("Cost") >= 0:
                if HP - int((Attacky.SpMoves.get("Damage") // 5) * Attacky.attack * 100 // (
                        100 + Players.get(Target).defense)) <= 0:
                    Attack(Attacker, Players.get(Target))
                    if GameType == "Multi":
                        P1.Server_En(s, playerNum, Target, "Attack")
                return True
            else:
                # 'else' happens if not killable with current amount of characters and will check if one more killable
                HP -= Attacky.attack * 100 // (100 + Players.get(Target).defense)
                index -= 1
                AI_Attack(HP, Enemies, index, Target, Attacker)
    else:
        return False


def Demon_death(Demon, Frame):
    ##### Demon_death #######
    # Parameters :- Demon: Demon enemy type, Frame: Integer
    # Return Type :- none
    # Purpose :- Continuously changes the sprite of the demon to create the animation of the demon dying
    ###########################
    while Frame < 23:
        background(2)
        Demon.Death(Frame)
        time.sleep(0.1)
        Frame += 1


def check_dead(Target):
    ##### check_dead #######
    # Parameters :- Target: Knight or Mage
    # Return Type :- none
    # Purpose :- Checks if one of your characters has died and updates the variables and sprite of the
    # character if they have
    ###########################
    if Players.get(Target).Dead:
        background(2)
        Text(("Your " + Players.get(Target).type + " has Died"), screen, (400, 50))
        time.sleep(1.5)
        Players.get(Target).Death()
        if Players.get(Target).type == "Knight" and Players.get(Target).EmpowerTurns != 0:
            Players.get(Target).Depower(Players.get(Target + 1))


mixer.music.load(
    "Main Music.mp3")  # Loads the main music theme for the game and plays it, music from https://www.youtube.com/watch?v=fxWqzJ2GxhI
mixer.music.set_volume(0.7)
mixer.music.play(-1)

while GameType == 0:  # Stays in loop until a game type has been selected
    if not MM:  # Displays Main Menu screen when false, so it doesn't keep doing it uselessly
        MainMenu()
        MM = True
    for event in pygame.event.get():  # Collects event that happen on the screen or the key board

        if event.type == pygame.QUIT:  # Closes game if X button in top right pressed
            GameType = "Single"
            carry_on = False
            end = False

        if event.type == pygame.KEYDOWN:  # Goes through checks if event was with the keyboard
            if event.key == pygame.K_1:
                GameType = "Single"

            if event.key == pygame.K_2:
                GameType = "Multi"

            if event.key == pygame.K_i:
                Instructions()
                MM = False
                Ins = True
                while Ins:  # Keeps open instruction until returned to previous screen
                    for press in pygame.event.get():
                        if press.type == pygame.QUIT:
                            GameType = "Single"
                            carry_on = False
                            end = False
                            Ins = False

                        if press.type == pygame.KEYDOWN:
                            if press.key == pygame.K_5:
                                Ins = False

            if event.key == pygame.K_s:
                Story()
                MM = False
                Stor = True
                while Stor:  # Keeps open story synopsis until returned to previous screen
                    for press in pygame.event.get():
                        if press.type == pygame.QUIT:
                            GameType = "Single"
                            carry_on = False
                            end = False
                            Stor = False

                        if press.type == pygame.KEYDOWN:
                            if press.key == pygame.K_5:
                                Stor = False

if GameType == "Multi":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Connects to server if 2-player selected
    s.connect((HOST, PORT))

    msg = json.loads(s.recv(1024).decode())
    if msg["Command"] == "WAIT":
        print("Waiting for connections")  # Waits for both clients to connect to server
    while msg["Command"] == "WAIT":
        print("Still waiting")
        data = s.recv(1024)
        if data:
            msg = json.loads(data.decode())

        time.sleep(1.5)
    playerNum = msg["Data"]["PlayerNum"]

    if playerNum == 1:  # Begins threading changing the variables depending on the player number
        threading.Thread(target=receive_message, args=(s, P1, P2)).start()

    elif playerNum == 2:
        threading.Thread(target=receive_message, args=(s, P2, P1)).start()

while carry_on:  # Creates main loop for the game to go through
    if Wave == 1:
        wave1()
        Wave += 0.5
    elif Wave == 2:
        wave2()
        Wave += 0.5
    elif Wave == 3:
        wave3()
        Wave += 0.5
    elif Wave == 4:
        wave4()
        Wave += 0.5
    elif Wave == 5:
        FinalBoss()
        Wave += 0.5

    elif Wave == 6:
        carry_on = False

    if Turn <= 1 and Back:  # Refreshes background
        if GameType != "Multi":
            background(1)
            Back = False
        elif GameType == "Multi":
            if playerNum == 1 and Turn == 0:
                background(1)
                Back = False

            elif playerNum == 2 and Turn == 1:
                background(1)
                Back = False
            else:
                background(5)
                Back = False

    for event in pygame.event.get():  # Retrieves all the events obtained during the game

        if event.type == pygame.QUIT:
            carry_on = False
            end = False
            if GameType == "Multi":  # Closes server if game is 2-player
                Players.get(playerNum).Server_Close(s, playerNum)

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_1:  # Allows player to attack
                if Turn == 0:
                    if GameType == "Single":
                        Turn += 1
                        Attack(P1, Enemies.peek())
                        time.sleep(1.5)
                        Empower_check(P1)
                        Back = True
                    elif GameType == "Multi" and playerNum == 1:  # Sends to server the action that just happened
                        Turn += 1
                        Attack(P1, Enemies.peek())
                        time.sleep(1.5)
                        Empower_check(P1)
                        P1.Server_att(s, playerNum)
                        Back = True

                elif Turn == 1:
                    if GameType == "Single":
                        Turn += 1
                        Attack(P2, Enemies.peek())
                        time.sleep(1.5)
                        Back = True

                    elif GameType == "Multi" and playerNum == 2:
                        Turn += 1
                        Attack(P2, Enemies.peek())
                        time.sleep(1.5)
                        P2.Server_att(s, playerNum)
                        Back = True

            if event.key == pygame.K_2:  # Allows player to open up special moves menu and select one
                if GameType == "Single" or GameType == "Multi" and (playerNum - 1) == Turn:
                    background(3)
                    wait = True
                    Back = True
                    while wait:
                        for action in pygame.event.get():
                            if action.type == pygame.QUIT:
                                carry_on = False
                                wait = False
                                end = False

                            if action.type == pygame.KEYDOWN:  # Allows player to press a key which corresponds to a
                                # special move

                                if action.key == pygame.K_1:
                                    if Turn == 0:
                                        if GameType == "Single":
                                            if P1.SpMoves.get(1).get("Cost") <= P1.SpGauge:
                                                playerSpAttack(P1, Enemies.peek(), 1)
                                                Turn += 1
                                                wait = False

                                            else:
                                                LowSP()  # Tells player that they don't have enough SP for a
                                                # special move
                                                wait = False

                                        elif GameType == "Multi":
                                            if P1.SpMoves.get(1).get("Cost") <= P1.SpGauge:
                                                playerSpAttack(P1, Enemies.peek(), 1)
                                                P1.Server_SP(s, playerNum, 1)
                                                Turn += 1
                                                wait = False

                                            else:
                                                LowSP()
                                                wait = False

                                    elif Turn == 1:
                                        if P2.SpMoves.get(1).get("Cost") <= P2.SpGauge:
                                            if GameType == "Single":
                                                player2Heal(P2, P1)
                                                Turn += 1
                                                wait = False

                                            elif GameType == "Multi":
                                                player2Heal(P2, P1)
                                                P2.Server_SP(s, playerNum, 1)
                                                Turn += 1
                                                wait = False

                                        else:
                                            LowSP()
                                            wait = False

                                if action.key == pygame.K_2:
                                    if len(P1.SpMoves) >= 2 and Turn == 0 and P1.protectCooldown <= 0:
                                        if P1.SpMoves.get(2).get("Cost") <= P1.SpGauge:
                                            if GameType == "Single":
                                                player1Protect(P1, P2)
                                                Turn += 1
                                                wait = False
                                            elif GameType == "Multi":
                                                player1Protect(P1, P2)
                                                P1.Server_SP(s, playerNum, 2)
                                                Turn += 1
                                                wait = False

                                        else:
                                            LowSP()
                                            wait = False

                                    elif len(P1.SpMoves) >= 2 and Turn == 0 and P1.protectCooldown > 0:
                                        background(4)
                                        time.sleep(1.5)
                                        wait = False

                                    elif len(P2.SpMoves) >= 2 and Turn == 1:
                                        if P2.SpMoves.get(2).get("Cost") <= P2.SpGauge:
                                            if GameType == "Single":
                                                playerSpAttack(P2, Enemies.peek(), 2)
                                                Turn += 1
                                                wait = False
                                            elif GameType == "Multi":
                                                playerSpAttack(P2, Enemies.peek(), 2)
                                                P2.Server_SP(s, playerNum, 2)
                                                Turn += 1
                                                wait = False

                                        else:
                                            LowSP()
                                            wait = False

                                if action.key == pygame.K_3:

                                    if len(P1.SpMoves) >= 3 and Turn == 0 and P1.EmpowerCooldown <= 0:
                                        if P1.SpMoves.get(3).get("Cost") <= P1.SpGauge:
                                            if GameType == "Single":
                                                player1Empower(P1, P2)
                                                Turn += 1
                                                wait = False
                                            elif GameType == "Multi":
                                                player1Empower(P1, P2)
                                                P1.Server_SP(s, playerNum, 3)
                                                Turn += 1
                                                wait = False

                                        else:
                                            LowSP()
                                            wait = False

                                    elif P1.EmpowerCooldown > 0 and Turn == 0:
                                        background(2)
                                        Text(("You must wait " + str(
                                            P1.EmpowerCooldown) + " more turns to use this attack again"), screen,
                                             (400, 50))
                                        time.sleep(1.5)
                                        wait = False

                                    elif len(P2.SpMoves) >= 3 and Turn == 1:
                                        if P2.SpMoves.get(3).get("Cost") <= P2.SpGauge:
                                            if GameType == "Single":
                                                playerSpAttack(P2, Enemies.peek(), 3)
                                                Turn += 1
                                                wait = False
                                            elif GameType == "Multi":
                                                playerSpAttack(P2, Enemies.peek(), 3)
                                                P2.Server_SP(s, playerNum, 3)
                                                Turn += 1
                                                wait = False

                                        else:
                                            LowSP()
                                            wait = False

                                if action.key == pygame.K_4:
                                    if len(P1.SpMoves) == 4 and Turn == 0:
                                        if P1.SpMoves.get(4).get("Cost") <= P1.SpGauge:
                                            if GameType == "Single":
                                                playerSpAtt4(P1, Enemies.Enemies)
                                                Turn += 1
                                                wait = False
                                                Empower_check(P1)
                                            elif GameType == "Multi":
                                                playerSpAtt4(P1, Enemies.Enemies)
                                                P1.Server_SP(s, playerNum, 4)
                                                Turn += 1
                                                wait = False
                                                Empower_check(P1)

                                        else:
                                            LowSP()
                                            wait = False

                                    elif len(P2.SpMoves) == 4 and Turn == 1:
                                        if P2.SpMoves.get(4).get("Cost") <= P1.SpGauge:
                                            if GameType == "Single":
                                                playerSpAtt4(P2, Enemies.Enemies)
                                                Turn += 1
                                                wait = False
                                            elif GameType == "Multi":
                                                playerSpAtt4(P2, Enemies.Enemies)
                                                P2.Server_SP(s, playerNum, 4)
                                                Turn += 1
                                                wait = False

                                        else:
                                            LowSP()
                                            wait = False

                                if action.key == pygame.K_5:
                                    wait = False

                                pygame.event.clear()

            if event.key == pygame.K_3:  # Allows player to block a move during their turn
                if GameType == "Single" or GameType == "Multi" and Turn + 1 == playerNum:
                    playerBlock(Turn)
                    Turn += 1
                    Back = True
                    if Players.get(Turn).type == "Knight":
                        Empower_check(P1)
                    if GameType == "Multi":
                        if playerNum == 1:
                            P1.Server_Blo(s, playerNum)
                        elif playerNum == 2:
                            P2.Server_Blo(s, playerNum)

            pygame.event.clear()

    if GameType == "Multi":  # Has the client complete the move that happened on the other client if in multiplayer
        if playerNum == 1 and P2.Att:
            Turn += 1
            Attack(P2, Enemies.peek())
            time.sleep(1.5)
            P2.Att = False
            Back = True
        elif playerNum == 2 and P1.Att:
            Turn += 1
            Attack(P1, Enemies.peek())
            time.sleep(1.5)
            Empower_check(P1)
            P1.Att = False
            Back = True
        elif playerNum == 1 and P2.SP1:
            player2Heal(P2, P1)
            Turn += 1
            P2.SP1 = False
            Back = True
        elif playerNum == 1 and P2.SP2:
            playerSpAttack(P2, Enemies.peek(), 2)
            Turn += 1
            P2.SP2 = False
            Back = True
        elif playerNum == 1 and P2.SP3:
            playerSpAttack(P2, Enemies.peek(), 3)
            Turn += 1
            P2.SP3 = False
            Back = True
        elif playerNum == 1 and P2.SP4:
            playerSpAtt4(P2, Enemies.Enemies)
            Turn += 1
            P2.SP4 = False
            Back = True
        elif playerNum == 2 and P1.SP1:
            playerSpAttack(P1, Enemies.peek(), 1)
            Turn += 1
            P1.SP1 = False
            Back = True
        elif playerNum == 2 and P1.SP2:
            player1Protect(P1, P2)
            Turn += 1
            P1.SP2 = False
            Back = True
        elif playerNum == 2 and P1.SP3:
            player1Empower(P1, P2)
            Turn += 1
            P1.SP3 = False
            Back = True
        elif playerNum == 2 and P1.SP4:
            playerSpAtt4(P1, Enemies.Enemies)
            Turn += 1
            Empower_check(P1)
            P1.SP4 = False
            Back = True
        elif playerNum == 1 and P2.Bl:
            playerBlock(Turn)
            Turn += 1
            P2.Bl = False
            Back = True
        elif playerNum == 2 and P1.Bl:
            Empower_check(P1)
            playerBlock(Turn)
            Turn += 1
            P1.Bl = False
            Back = True

    if P1.Dead is True and Turn == 0:  # Skips turn if character is dead
        Turn = 1
        Back = True

    if P2.Dead is True and Turn == 1:
        Turn = 2
        Back = True

    while not Enemies.Enemies == [] and Enemies.peek().Dead is True:  # Checks if next enemy is dead but not if enemies
        # list is empty and adds the XP gained as well as removing them from the stack
        if Wave != 5.5:  # Makes sure it isn't the final boss that was just deafeated
            GiveXP(Enemies.peek())
            background(2)
            Text(Enemies.peek().type + " has been defeated", screen, (400, 50))
            pygame.display.flip()
            time.sleep(0.75)
            Enemy_Sprite_list.remove(Enemies.peek())
            background(2)
            Text(Enemies.peek().type + " has been defeated", screen, (400, 50))
            pygame.display.flip()
            time.sleep(0.75)
            Enemies.pop()
        else:  # Does special animation for the Demon's death
            Demon_death(Enemies.peek(), 1)
            Enemy_Sprite_list.remove(Enemies.peek())
            Enemies.pop()
        Back = True

    if Turn == 2:  # Goes through enemies turn
        if Players.get(1).protect:  # Skips enemy turn if protect was activated
            background(2)
            Text("Your team was protected from the enemy", screen, (400, 50))
            Turn = 0
            time.sleep(1.5)
        elif (Wave < 3 and GameType == "Single") or (Wave < 3 and GameType == "Multi" and playerNum == 1):
            # Checks the wave is before 3 and game is single player or multiplayer and the playerNum is 1
            Enemies.Enemies.reverse()
            for i in Enemies.Enemies:  # Has all enemies attack
                if P1.Dead is False or P2.Dead is False:
                    Target = random.randint(1, 2)  # Has enemy attack completely randomly
                    Attack_Type = random.randint(1, 10)
                    if Players.get(Target).Dead:
                        if Target == 1:
                            Target = 2
                        elif Target == 2:
                            Target = 1
                    if Attack_Type <= 3:
                        if i.SpGauge - i.SpMoves.get("Cost") >= 0:  # Makes sure enemy can afford special move
                            SpAttack(i, Players.get(Target))
                            if GameType == "Multi":  # Sends to server the character that was attacked and what
                                # attack was used
                                P1.Server_En(s, playerNum, Target, "Special")
                        else:
                            Attack_Type = random.randint(4, 10)  # Rerolls if enemy can't afford to do attack

                    if 4 <= Attack_Type <= 8:
                        Attack(i, Players.get(Target))
                        if GameType == "Multi":
                            P1.Server_En(s, playerNum, Target, "Attack")
                    elif Attack_Type >= 9:
                        i.move_left()
                        background(2)
                        Text(("Enemy " + i.type + " begins to block!"), screen, (400, 50))
                        pygame.display.flip()
                        i.move_right()
                        i.block()
                        if GameType == "Multi":
                            P1.Server_En(s, playerNum, Target, "Block")
                    if Wave != 3:
                        time.sleep(0.85)
                    else:
                        time.sleep(1)
                    check_dead(Target)
            Enemies.Enemies.reverse()
            Turn = 0
            P1.protectCooldown -= 1
            P1.EmpowerCooldown -= 1
            for i in Players:  # Stops Mage and/or blocking if they currently are
                if Players.get(i).blocking:
                    Players.get(i).Stop_Block()

            Back = True

        elif (Turn == 2 and GameType == "Single") or (Turn == 2 and GameType == "Multi" and playerNum == 1):
            # Does more complex and smarter enemy attacks if wave is 3 or later
            killable = True
            Enemies.Enemies.reverse()
            for i in Enemies.Enemies:
                if P1.Dead is False or P2.Dead is False:
                    if Players.get(1).blocking and Players.get(2).blocking:  # Selects to attack the character that
                        # isn't blocking or less health unless they are dead
                        Target = 2
                    elif Players.get(2).blocking:
                        Target = 1
                    elif Players.get(1).blocking:
                        Target = 2

                    elif Players.get(1).health < Players.get(2).health:
                        Target = 1

                    else:
                        Target = 2

                    if Players.get(Target).Dead:
                        if Target == 1:
                            Target = 2
                        elif Target == 2:
                            Target = 1

                    if Players.get(Target).health - (i.attack * 100 // (100 + Players.get(Target).defense)) <= 0:
                        Attack(i, Players.get(Target))  # Has enemy attack if the opponent is killable
                        if GameType == "Multi":
                            P1.Server_En(s, playerNum, Target, "Attack")  # Sends to server the enemies attack details
                    elif i.SpGauge - i.SpMoves.get("Cost") >= 0:  # Has enemy use the strongest attack if it
                        # can be afforded
                        SpAttack(i, Players.get(Target))
                        if GameType == "Multi":
                            P1.Server_En(s, playerNum, Target, "Special")
                    elif killable:  # Checks if one of characters can be killed this turn
                        killable = AI_Attack((i.attack * 100 // (100 + Players.get(Target).defense)),
                                             Enemies, Enemies.Enemies.index(i), Target, i)

                    if not killable:  # If neither character can be killed the enemy will just block
                        i.move_left()
                        background(2)
                        Text(("Enemy " + i.type + " begins to block!"), screen, (400, 50))
                        i.block()
                        i.move_right()
                        if GameType == "Multi":
                            P1.Server_En(s, playerNum, Target, "Block")

                    time.sleep(1)
                    check_dead(Target)  # Checks if player is dead
            Enemies.Enemies.reverse()
            Turn = 0
            P1.protectCooldown -= 1
            P1.EmpowerCooldown -= 1
            for i in Players:
                if Players.get(i).blocking:
                    Players.get(i).Stop_Block()
            Back = True

        elif Turn == 2 and GameType == "Multi" and playerNum == 2:
            # Completes turn 2 on playerNum 2's side by variables that were given by the other client
            if P2.En_Atts == 1:
                Enemies.Enemies.reverse()
                Attack(Enemies.Enemies[P2.En_Am], Players.get(P2.En_Tar))
                if Wave != 3:
                    time.sleep(0.5)
                else:
                    time.sleep(1)
                P2.En_Am += 1
                Enemies.Enemies.reverse()
                check_dead(P2.En_Tar)
            elif P2.En_Atts == 2:
                Enemies.Enemies.reverse()
                SpAttack(Enemies.Enemies[P2.En_Am], Players.get(P2.En_Tar))
                if Wave != 3:
                    time.sleep(0.5)
                else:
                    time.sleep(1)
                P2.En_Am += 1
                Enemies.Enemies.reverse()
                check_dead(P2.En_Tar)
            elif P2.En_Atts == 3:
                Enemies.Enemies.reverse()
                Enemies.Enemies[P2.En_Am].move_left()
                background(2)
                Text(("Enemy " + Enemies.Enemies[P2.En_Am].type + " begins to block!"), screen, (400, 50))
                if Wave != 3:
                    time.sleep(0.5)
                else:
                    time.sleep(1)
                Enemies.Enemies[P2.En_Am].move_right()
                Enemies.Enemies[P2.En_Am].block()
                P2.En_Am += 1
                Enemies.Enemies.reverse()

            P2.En_Atts = 0

            if P2.En_Am == len(Enemies.Enemies):
                P2.En_Am = 0
                Turn = 0
                P1.protectCooldown -= 1
                P1.EmpowerCooldown -= 1
                for i in Players:
                    if Players.get(i).blocking:
                        Players.get(i).Stop_Block()
                Back = True

        if P1.protect:
            P1.StopProtect(P2)

    if not Enemies.Enemies:  # If all enemies are dead game checks if a level has been earned and increase the hp
        # and sp back to max. Also, all cool-downs are reset and sprites are returned to normal if dead.
        Wave += 0.5
        Turn = 0
        for player in Players:
            if Players.get(player).Dead:
                Players.get(player).Alive()
                Players.get(player).Dead = False
            Players.get(player).check_xp()
            Players.get(player).health = Players.get(player).healthMax
            Players.get(player).SpGauge = Players.get(player).SpGaugeMax
        if P1.EmpowerTurns <= 4:
            P1.Depower(P2)
            P1.EmpowerTurns = 5
        if P1.EmpowerCooldown != 0:
            P1.EmpowerCooldown = 0
        if P1.protectCooldown != 0:
            P1.protectCooldown = 0
        if P1.protect:
            P1.StopProtect(P2)

    if P1.Dead and P2.Dead:  # Creates game over if both knight and mage die
        GO = True
        GameOver()
        while GO:
            for act in pygame.event.get():
                if act.type == pygame.QUIT:
                    GO = False
                    carry_on = False
                    end = False

                elif act.type == pygame.KEYDOWN:
                    if act.key == pygame.K_1:
                        GO = False
                        Back = True

                    elif act.key == pygame.K_2:
                        GO = False
                        carry_on = False
                        end = False

            pygame.event.clear()
        if carry_on:  # Checks if a level up was earned and health and SP reset to max as well as the sprites reset to
            # normal
            Enemies.erase()
            Enemy_Sprite_list.empty()
            Turn = 0
            for player in Players:
                Players.get(player).Alive()
                Players.get(player).check_xp()
                Players.get(player).health = Players.get(player).healthMax
                Players.get(player).SpGauge = Players.get(player).SpGaugeMax
                Players.get(player).Dead = False
            if P1.EmpowerCooldown != 0:
                if 0 < P1.EmpowerCooldown < 4:
                    P1.Depower(P2)
                P1.EmpowerCooldown = 0
            if P1.protectCooldown != 0:
                P1.protectCooldown = 0
            if P1.protect:
                P1.StopProtect(P2)
            Wave -= 0.5

    if P1.levelUp:  # Shows that a level up has happened
        background(6)
        P1.levelUp = False
        P2.levelUp = False
        time.sleep(1)
        Back = True

    clock.tick(30)  # Limits at 30 FPS

    if P1.S_Cl or P2.S_Cl:  # Closes game on both sides in multiplayer
        end = False
        carry_on = False

if end:  # Creates win screen if game not quit
    Win()

while end:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            end = False

if GameType == "Multi":  # Disconnects clients form server
    Players.get(playerNum).Server_Close(s, playerNum)
    s.close()

mixer.music.stop()  # Stops music
