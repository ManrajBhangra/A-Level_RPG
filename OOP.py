import pygame
import json


class characters(pygame.sprite.Sprite):
    #  Creates Character class
    def __init__(self, colour, screen, type, team):
        super().__init__()

        self.colour = colour
        self.type = type
        self.Dead = False
        self.team = team

        self.image = pygame.Surface([800, 800])
        self.image.set_colorkey((0, 0, 0))
        self.attack = 10
        self.defense = 10
        self.SpGauge = 20
        self.SpGaugeMax = 20
        self.blocking = False

        self.width = 30
        self.height = 30

        pygame.draw.rect(self.image, self.colour, [self.width, self.height, 10, 60], 0)

        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 100

    def move_left(self):
        ##### move_left #######
        # Parameters :- self
        # Return Type :- none
        # Purpose :- moves sprite left
        ###########################
        self.rect.x -= 25

    def move_right(self):
        ##### move_right #######
        # Parameters :- self
        # Return Type :- none
        # Purpose :- moves sprite right
        ###########################
        self.rect.x += 25

    def Stop_Block(self):
        ##### Stop_Block #######
        # Parameters :- self
        # Return Type :- none
        # Purpose :- Stops a character that is blocking
        ###########################
        self.blocking = False
        self.defense = self.defense / 2.5

    def attacking(self, target):
        ##### attacking #######
        # Parameters :- self, target
        # Return Type :- none
        # Purpose :- Allows a character to attack another character
        ###########################
        target.health -= self.attack * 100 // (100 + target.defense)
        if target.health < 0:  # Sets target as dead if hp is below 0
            target.health = 0
            target.Dead = True
        if target.blocking:
            target.Stop_Block()

    def block(self):
        ##### block #######
        # Parameters :- self
        # Return Type :- none
        # Purpose :- allows a character to block during their turn and increase their defence and sp
        ###########################
        self.defense = self.defense * 2.5
        if self.SpGauge + (self.SpGauge // 20) == self.SpGauge:
            self.SpGauge += 2

        else:
            self.SpGauge += (self.SpGauge // 20)

        if self.SpGauge > self.SpGaugeMax:
            self.SpGauge = self.SpGaugeMax
        self.blocking = True


class Player(characters, pygame.sprite.Sprite):
    # Creates Player class which inherits from characters

    def __init__(self, colour, screen, type, team):
        super().__init__(colour, screen, type, team)  # inherits variables from character

        self.XP = 0
        self.blocking = False
        self.protect = False
        self.Att = False
        self.SP1 = False
        self.SP2 = False
        self.SP3 = False
        self.SP4 = False
        self.Bl = False
        self.S_Cl = False
        self.levelUp = False
        self.SpMoves = []

        self.width = 50
        self.height = 200

    def adjust_XP(self, target):
        ##### adjust_XP #######
        # Parameters :- self, target
        # Return Type :- none
        # Purpose :- Increase the XP of a player
        ###########################
        self.XP += target.XPYield

    def learn_move(self):
        ##### learn_move #######
        # Parameters :- self
        # Return Type :- none
        # Purpose :- Allows a player to learn a new move depending on their type
        ###########################

        if self.type == "Mage":  # Teaches correct move depending on type
            if len(self.SpMoves) == 1:
                self.SpMoves[2] = {"Move": "Fireball", "Cost": 10, "Damage": 15, "Targets": "1", "Type": "Fire"}
            elif len(self.SpMoves) == 2:
                self.SpMoves[3] = {"Move": "Thunder", "Cost": 15, "Damage": 20, "Targets": "3", "Type": "Lightning"}
            elif len(self.SpMoves) == 3:
                self.SpMoves[4] = {"Move": "Meteor Storm", "Cost": 18, "Damage": 50, "Targets": "All", "Type": "Ground"}

        elif self.type == "Knight":
            if len(self.SpMoves) == 1:
                self.SpMoves[2] = {"Move": "Protect", "Cost": 10}
            elif len(self.SpMoves) == 2:
                self.SpMoves[3] = {"Move": "Empower", "Cost": 10}
            elif len(self.SpMoves) == 3:
                self.SpMoves[4] = {"Move": "Excalibur's Revenge", "Cost": 18, "Damage": 50, "Targets": "All",
                                   "Type": "Light"}

    def Empower(self, duo):
        ##### Empower #######
        # Parameters :- self, duo: other player
        # Return Type :- none
        # Purpose :- Increases the power of both characters for a set amount of time
        ###########################
        self.EmpowerCooldown = 5
        self.EmpowerTurns = 1
        self.attack = self.attack * 1.5
        duo.attack = duo.attack * 1.5

    def Depower(self, duo):
        ##### Depower #######
        # Parameters :- self, duo: other player
        # Return Type :- none
        # Purpose :- Reverse effects of empower after a set amount of time
        ###########################
        self.attack = self.attack * 2 / 3
        duo.attack = duo.attack * 2 / 3

    def StopProtect(self, duo):
        ##### StopProtect #######
        # Parameters :- self, duo: other player
        # Return Type :- none
        # Purpose :- Stop a player's protect after the turn is up
        ###########################
        self.protect = False
        duo.protect = False

    def SpecialMove(self, move, target):
        ##### Special #######
        # Parameters :- Self, move: integer, target: enemy
        # Return Type :- none
        # Purpose :- Allows for players to use special move depending on the player's type and move number
        ###########################
        if self.type == "Knight":  # Checks the character type to select the correct pool of special moves
            if move == 1:  # Checks the move number to enact the correct action
                target.health -= ((self.SpMoves.get(move).get("Damage")) // 5) * self.attack * 100 // (
                        100 + target.defense)
                self.SpGauge -= self.SpMoves.get(move).get("Cost")
                if target.health < 0:  # Kills enemy if health less than 0
                    target.health = 0
                    target.Dead = True
                if target.blocking:  # Makes enemy stop blocking if they are blocking
                    target.Stop_Block()

            elif move == 2:
                self.protect = True
                target.protect = True
                self.protectCooldown = 5
                self.SpGauge -= self.SpMoves.get(move).get("Cost")

            elif move == 3:
                self.Empower(target)
                self.SpGauge -= self.SpMoves.get(move).get("Cost")

            elif move == 4:
                target.health -= ((self.SpMoves.get(move).get("Damage")) // 5) * self.attack * 100 // (
                        100 + target.defense)
                self.SpGauge -= self.SpMoves.get(move).get("Cost")
                if target.health < 0:
                    target.health = 0
                    target.Dead = True
                if target.blocking:
                    target.Stop_Block()

        elif self.type == "Mage":
            if move == 1:
                target.health += (target.healthMax // 10)
                if target.health > target.healthMax:
                    target.health = target.healthMax
                self.SpGauge -= self.SpMoves.get(move).get("Cost")

            elif move == 2:
                target.health -= ((self.SpMoves.get(move).get("Damage")) // 5) * self.attack * 100 // (
                        100 + target.defense)
                self.SpGauge -= self.SpMoves.get(move).get("Cost")
                if target.health < 0:
                    target.health = 0
                    target.Dead = True
                if target.blocking:
                    target.Stop_Block()

            elif move == 3:
                target.health -= ((self.SpMoves.get(move).get("Damage")) // 5) * self.attack * 100 // (
                        100 + target.defense)
                self.SpGauge -= self.SpMoves.get(move).get("Cost")
                if target.health < 0:
                    target.health = 0
                    target.Dead = True
                if target.blocking:
                    target.Stop_Block()

            elif move == 4:
                target.health -= ((self.SpMoves.get(move).get("Damage")) // 5) * self.attack * 100 // (
                        100 + target.defense)
                self.SpGauge -= self.SpMoves.get(move).get("Cost")
                if target.health < 0:
                    target.health = 0
                    target.Dead = True
                if target.blocking:
                    target.Stop_Block()

    def check_xp(self):
        ##### check_XP #######
        # Parameters :- self
        # Return Type :- none
        # Purpose :- Checks to see if a level up has been earned
        ###########################
        if self.XP >= 200 and len(self.SpMoves) < 2:  # Only lets the player level up one time per battle
            self.learn_move()
            self.attack += 10
            self.defense += 10
            self.SpGaugeMax += 3
            self.healthMax += 10
            self.levelUp = True
        elif self.XP >= 550 and len(self.SpMoves) < 3:
            self.learn_move()
            self.attack += 10
            self.defense += 10
            self.SpGaugeMax += 3
            self.healthMax += 10
            self.levelUp = True
        elif self.XP >= 670 and self.attack != 80:  # Allows the player to keep leveling up to prevent getting stuck
            # on one battle due to not knowing the perfect way to win
            self.attack += 10
            self.defense += 10
            self.SpGaugeMax += 3
            self.healthMax += 10
            self.levelUp = True
        if self.XP >= 1000 and len(self.SpMoves) < 4:
            self.learn_move()
            self.levelUp = True

    def Death(self):
        ##### Death #######
        # Parameters :- self
        # Return Type :- none
        # Purpose :- Changes a player's sprite to dead
        ###########################
        if self.type == "Knight":
            self.image = pygame.Surface([120, 80])
            self.image.set_colorkey((0, 0, 0))
            if self.colour == 1:
                Dead_Knight = pygame.image.load("Knight_Dead1.png")
                # Sprite from https://aamatniekss.itch.io/fantasy-knight-free-pixelart-animated-character
                self.image.blit(Dead_Knight, (0, 0), (1080, 0, 1200, 80))
                self.image = pygame.transform.scale(self.image, (120 * 2, 80 * 2))
        elif self.type == "Mage":
            self.image = pygame.Surface([250, 250])
            self.image.set_colorkey((0, 0, 0))
            if self.colour == 1:
                Dead_Mage = pygame.image.load("Mage_Dead1.png")
                # Sprite from https://luizmelo.itch.io/evil-wizard-2
                self.image.blit(Dead_Mage, (0, 0), (1500, 0, 1750, 250))
                self.image = pygame.transform.scale(self.image, (250 * 1.5, 250 * 1.5))

    def Alive(self):
        ##### ALive #######
        # Parameters :- self
        # Return Type :- none
        # Purpose :- Changes a player's sprite back to normal
        ###########################
        if self.type == "Knight":
            self.image = pygame.Surface([120, 80])
            self.image.set_colorkey((0, 0, 0))
            if self.colour == 1:
                Idle_Knight = pygame.image.load("Knight_Idle1.png")
                # Sprite from https://aamatniekss.itch.io/fantasy-knight-free-pixelart-animated-character
                self.image.blit(Idle_Knight, (0, 0), (0, 0, 120, 80))
                self.image = pygame.transform.scale(self.image, (120 * 2, 80 * 2))

        elif self.type == "Mage":
            self.image = pygame.Surface([250, 250])
            self.image.set_colorkey((0, 0, 0))
            if self.colour == 1:
                Idle_Mage = pygame.image.load("Mage_Idle1.png")
                # Sprite from https://luizmelo.itch.io/evil-wizard-2
                self.image.blit(Idle_Mage, (0, 0), (0, 0, 250, 250))
                self.image = pygame.transform.scale(self.image, (250 * 1.5, 250 * 1.5))

    def Server_att(self, server, playerNum):
        ##### Server_att #######
        # Parameters :- self, server, playerNum: integer
        # Return Type :- none
        # Purpose :- Sends to server that an attack has happened
        ###########################
        msg = {"Command": "SETUP", "Data": {"playerNum": playerNum, "Move": "Attack"}}
        server.sendall(json.dumps(msg).encode())

    def Server_En(self, server, playerNum, Target, Move):
        ##### Server_ #En######
        # Parameters :- self, server, playerNum: integer, Target: integer, Move: integer
        # Return Type :- none
        # Purpose :- Sends to server that an enemy has made an action and what the action was
        ###########################
        msg = {"Command": "SETUP", "Data": {"playerNum": playerNum, "Move": "En", "Target": Target, "Attack": Move}}
        server.sendall(json.dumps(msg).encode())

    def Server_SP(self, server, playerNum, SP):
        ##### Server_Sp #######
        # Parameters :- self, server, playerNum: integer, SP: integer
        # Return Type :- none
        # Purpose :- Sends to server that a special attack has happened and which one
        ###########################
        msg = {"Command": "SETUP", "Data": {"playerNum": playerNum, "Move": "SP", "SP": SP}}
        server.sendall(json.dumps(msg).encode())

    def Server_Blo(self, server, playerNum):
        ##### Server_Blo #######
        # Parameters :- self, server, playerNum: integer
        # Return Type :- none
        # Purpose :- Sends to server that a block has happened
        ###########################
        msg = {"Command": "SETUP", "Data": {"playerNum": playerNum, "Move": "Block"}}
        server.sendall(json.dumps(msg).encode())

    def Server_Close(self, server, playerNum):
        ##### Server_Close #######
        # Parameters :- self, server, playerNum: integer
        # Return Type :- none
        # Purpose :- Sends to server that one client wishes to disconnect
        ###########################
        msg = {"Command": "SETUP", "Data": {"playerNum": playerNum, "Move": "Close"}}
        server.sendall(json.dumps(msg).encode())


class Knight(Player, pygame.sprite.Sprite):
    # Creates class for knight which inherits from Player

    def __init__(self, colour, screen, type, team):
        super().__init__(colour, screen, type, team)

        self.image = pygame.Surface([120, 80])
        self.image.set_colorkey((0, 0, 0))
        if self.colour == 1:
            Idle_Knight = pygame.image.load("Knight_Idle1.png")
            # https://www.youtube.com/watch?v=M6e3_8LHc7A, learnt how to do
            # Sprite from https://aamatniekss.itch.io/fantasy-knight-free-pixelart-animated-character
            self.image.blit(Idle_Knight, (0, 0), (0, 0, 120, 80))
            self.image = pygame.transform.scale(self.image, (120 * 2, 80 * 2))
        self.SpGauge = 30
        self.SpGaugeMax = 30
        self.defense = 20
        self.attack = 50
        self.health = 400
        self.healthMax = 400
        self.SpMoves = {1: {"Move": "Sword Strike", "Cost": 15, "Damage": 15, "Targets": 1, "Type": "Light"}}
        self.protectCooldown = 0
        self.EmpowerTurns = 5
        self.EmpowerCooldown = 0


class Mage(Player, pygame.sprite.Sprite):
    # Creates class for mage which inherits from Player

    def __init__(self, colour, screen, type, team):
        super().__init__(colour, screen, type, team)

        self.image = pygame.Surface([250, 250])
        self.image.set_colorkey((0, 0, 0))
        if self.colour == 1:
            Idle_Mage = pygame.image.load("Mage_Idle1.png")
            # Sprite from https://luizmelo.itch.io/evil-wizard-2
            self.image.blit(Idle_Mage, (0, 0), (0, 0, 250, 250))
            self.image = pygame.transform.scale(self.image, (250 * 1.5, 250 * 1.5))
        self.SpGauge = 20
        self.SpGaugeMax = 20
        self.defense = 10
        self.attack = 40
        self.health = 350
        self.healthMax = 350
        self.SpMoves = {1: {"Move": "Heal", "Cost": 5}}
        self.En_Tar = ""
        self.En_Atts = ""
        self.En_Am = 0


class Enemy(characters, pygame.sprite.Sprite):
    # Creates class for Enemy which inherits from characters

    def __init__(self, screen, type, colour, team):

        super().__init__(colour, screen, type, team)

        if self.type == "Goblin":  # Has different variables depending on the type of enemy
            self.image = pygame.Surface([150, 150])
            self.image.fill((255, 255, 255))
            self.image.set_colorkey((255, 255, 255))
            self.attack = 30
            self.defense = 10
            self.health = 100
            self.SpGauge = 7
            self.SpGaugeMax = 7
            self.blocking = False
            self.SpMoves = {"Move": "Club Whack", "Cost": 3, "Damage": 15}
            self.XPYield = 50

            if self.colour == 1:
                Goblin = pygame.image.load("Goblin.png")
                # Sprite from https://luizmelo.itch.io/monsters-creatures-fantasy
                self.image.blit(Goblin, (0, 0), (0, 0, 150, 150))
                self.image = pygame.transform.scale(self.image, (150 * 1.9, 150 * 1.9))
                self.image = pygame.transform.flip(self.image, True, False)

        if self.type == "Ninja":
            self.image = pygame.Surface([200, 200])
            self.image.fill((255, 255, 255))
            self.image.set_colorkey((255, 255, 255))
            self.attack = 40
            self.defense = 50
            self.health = 400
            self.SpGauge = 9
            self.SpGaugeMax = 9
            self.blocking = False
            self.SpMoves = {"Move": "Stealth Strike", "Cost": 5, "Damage": 30}
            self.XPYield = 200

            if self.colour == 1:
                Idle_Ninja = pygame.image.load("Ninja_Idle1.png")
                # Sprite from https://luizmelo.itch.io/martial-hero
                self.image.blit(Idle_Ninja, (0, 0), (0, 0, 200, 200))
                self.image = pygame.transform.scale(self.image, (200 * 2, 200 * 2))
                self.image = pygame.transform.flip(self.image, True, False)

        if self.type == "Skeleton Warrior":
            self.image = pygame.Surface([150, 150])
            self.image.fill((255, 255, 255))
            self.image.set_colorkey((255, 255, 255))
            self.attack = 40
            self.defense = 60
            self.health = 300
            self.SpGauge = 15
            self.SpGaugeMax = 15
            self.blocking = False
            self.SpMoves = {"Move": "Undead Slash", "Cost": 5, "Damage": 10}
            self.XPYield = 150

            if self.colour == 1:
                Idle_Skele = pygame.image.load("Skeleton.png")
                # Sprite from https://luizmelo.itch.io/monsters-creatures-fantasy
                self.image.blit(Idle_Skele, (0, 0), (450, 0, 600, 200))
                self.image = pygame.transform.scale(self.image, (150 * 2, 150 * 2))
                self.image = pygame.transform.flip(self.image, True, False)

        if self.type == "Mushroom":
            self.image = pygame.Surface([150, 150])
            self.image.fill((255, 255, 255))
            self.image.set_colorkey((255, 255, 255))
            self.attack = 15
            self.defense = 20
            self.health = 75
            self.SpGauge = 9
            self.SpGaugeMax = 9
            self.blocking = False
            self.SpMoves = {"Move": "Spore Storm", "Cost": 4, "Damage": 20}
            self.XPYield = 20

            if self.colour == 1:
                Idle_Mush = pygame.image.load("Mush.png")
                # Sprite from https://luizmelo.itch.io/monsters-creatures-fantasy
                self.image.blit(Idle_Mush, (0, 0), (0, 0, 150, 150))
                self.image = pygame.transform.scale(self.image, (150 * 1.5, 150 * 1.5))
                self.image = pygame.transform.flip(self.image, True, False)

        if self.type == "Demon":
            self.image = pygame.Surface([288, 160])
            self.image.fill((255, 255, 255))
            self.image.set_colorkey((255, 255, 255))
            self.attack = 100
            self.defense = 110
            self.health = 1500
            self.SpGauge = 9
            self.SpGaugeMax = 9
            self.blocking = False
            self.SpMoves = {"Move": "Hellfire", "Cost": 8, "Damage": 25}
            self.XPYield = 0

            if self.colour == 1:
                Idle_Demon = pygame.image.load("Demon_Idle.png")
                # Sprite from https://chierit.itch.io/boss-demon-slime
                self.image.blit(Idle_Demon, (0, 0), (0, 0, 288, 160))
                self.image = pygame.transform.scale(self.image, (288 * 5, 160 * 5))

    def SpMove(self, target):
        ##### SpMove #######
        # Parameters :- Self, Target: Player
        # Return Type :- none
        # Purpose :- Allows for an enemy to use their special attack
        ###########################
        target.health -= ((self.SpMoves.get("Damage")) // 5) * self.attack * 100 // (
                100 + target.defense)
        self.SpGauge -= self.SpMoves.get("Cost")
        if target.health < 0:
            target.health = 0
            target.Dead = True
        if target.blocking:
            target.Stop_Block()

    def Death(self, frame):
        ##### Death #######
        # Parameters :- self, frame: integer
        # Return Type :- none
        # Purpose :- Changes demon sprite during death animation
        ###########################
        if self.type == "Demon":
            self.image = pygame.Surface([288, 160])
            self.image.fill((255, 255, 255))
            self.image.set_colorkey((255, 255, 255))

            if self.colour == 1:
                if frame == 1:  # Updates the sprite frame by frame slowly
                    Dead_Demon = pygame.image.load("demon_death_1.png")
                    # Sprite from https://chierit.itch.io/boss-demon-slime
                    self.image.blit(Dead_Demon, (0, 0), (0, 0, 288, 160))
                    self.image = pygame.transform.scale(self.image, (288 * 5, 160 * 5))

                elif frame == 2:
                    Dead_Demon = pygame.image.load("demon_death_2.png")
                    # Sprite from https://chierit.itch.io/boss-demon-slime
                    self.image.blit(Dead_Demon, (0, 0), (0, 0, 288, 160))
                    self.image = pygame.transform.scale(self.image, (288 * 5, 160 * 5))

                elif frame == 3:
                    Dead_Demon = pygame.image.load("demon_death_3.png")
                    # Sprite from https://chierit.itch.io/boss-demon-slime
                    self.image.blit(Dead_Demon, (0, 0), (0, 0, 288, 160))
                    self.image = pygame.transform.scale(self.image, (288 * 5, 160 * 5))

                elif frame == 4:
                    Dead_Demon = pygame.image.load("demon_death_4.png")
                    # Sprite from https://chierit.itch.io/boss-demon-slime
                    self.image.blit(Dead_Demon, (0, 0), (0, 0, 288, 160))
                    self.image = pygame.transform.scale(self.image, (288 * 5, 160 * 5))

                elif frame == 5:
                    Dead_Demon = pygame.image.load("demon_death_5.png")
                    # Sprite from https://chierit.itch.io/boss-demon-slime
                    self.image.blit(Dead_Demon, (0, 0), (0, 0, 288, 160))
                    self.image = pygame.transform.scale(self.image, (288 * 5, 160 * 5))

                elif frame == 6:
                    Dead_Demon = pygame.image.load("demon_death_6.png")
                    # Sprite from https://chierit.itch.io/boss-demon-slime
                    self.image.blit(Dead_Demon, (0, 0), (0, 0, 288, 160))
                    self.image = pygame.transform.scale(self.image, (288 * 5, 160 * 5))

                elif frame == 7:
                    Dead_Demon = pygame.image.load("demon_death_7.png")
                    # Sprite from https://chierit.itch.io/boss-demon-slime
                    self.image.blit(Dead_Demon, (0, 0), (0, 0, 288, 160))
                    self.image = pygame.transform.scale(self.image, (288 * 5, 160 * 5))

                elif frame == 8:
                    Dead_Demon = pygame.image.load("demon_death_8.png")
                    # Sprite from https://chierit.itch.io/boss-demon-slime
                    self.image.blit(Dead_Demon, (0, 0), (0, 0, 288, 160))
                    self.image = pygame.transform.scale(self.image, (288 * 5, 160 * 5))

                elif frame == 9:
                    Dead_Demon = pygame.image.load("demon_death_9.png")
                    # Sprite from https://chierit.itch.io/boss-demon-slime
                    self.image.blit(Dead_Demon, (0, 0), (0, 0, 288, 160))
                    self.image = pygame.transform.scale(self.image, (288 * 5, 160 * 5))

                elif frame == 10:
                    Dead_Demon = pygame.image.load("demon_death_10.png")
                    # Sprite from https://chierit.itch.io/boss-demon-slime
                    self.image.blit(Dead_Demon, (0, 0), (0, 0, 288, 160))
                    self.image = pygame.transform.scale(self.image, (288 * 5, 160 * 5))

                elif frame == 11:
                    Dead_Demon = pygame.image.load("demon_death_11.png")
                    # Sprite from https://chierit.itch.io/boss-demon-slime
                    self.image.blit(Dead_Demon, (0, 0), (0, 0, 288, 160))
                    self.image = pygame.transform.scale(self.image, (288 * 5, 160 * 5))

                elif frame == 12:
                    Dead_Demon = pygame.image.load("demon_death_12.png")
                    # Sprite from https://chierit.itch.io/boss-demon-slime
                    self.image.blit(Dead_Demon, (0, 0), (0, 0, 288, 160))
                    self.image = pygame.transform.scale(self.image, (288 * 5, 160 * 5))

                elif frame == 13:
                    Dead_Demon = pygame.image.load("demon_death_13.png")
                    # Sprite from https://chierit.itch.io/boss-demon-slime
                    self.image.blit(Dead_Demon, (0, 0), (0, 0, 288, 160))
                    self.image = pygame.transform.scale(self.image, (288 * 5, 160 * 5))

                elif frame == 14:
                    Dead_Demon = pygame.image.load("demon_death_14.png")
                    # Sprite from https://chierit.itch.io/boss-demon-slime
                    self.image.blit(Dead_Demon, (0, 0), (0, 0, 288, 160))
                    self.image = pygame.transform.scale(self.image, (288 * 5, 160 * 5))

                elif frame == 15:
                    Dead_Demon = pygame.image.load("demon_death_15.png")
                    # Sprite from https://chierit.itch.io/boss-demon-slime
                    self.image.blit(Dead_Demon, (0, 0), (0, 0, 288, 160))
                    self.image = pygame.transform.scale(self.image, (288 * 5, 160 * 5))

                elif frame == 16:
                    Dead_Demon = pygame.image.load("demon_death_16.png")
                    # Sprite from https://chierit.itch.io/boss-demon-slime
                    self.image.blit(Dead_Demon, (0, 0), (0, 0, 288, 160))
                    self.image = pygame.transform.scale(self.image, (288 * 5, 160 * 5))

                elif frame == 17:
                    Dead_Demon = pygame.image.load("demon_death_17.png")
                    # Sprite from https://chierit.itch.io/boss-demon-slime
                    self.image.blit(Dead_Demon, (0, 0), (0, 0, 288, 160))
                    self.image = pygame.transform.scale(self.image, (288 * 5, 160 * 5))

                elif frame == 18:
                    Dead_Demon = pygame.image.load("demon_death_18.png")
                    # Sprite from https://chierit.itch.io/boss-demon-slime
                    self.image.blit(Dead_Demon, (0, 0), (0, 0, 288, 160))
                    self.image = pygame.transform.scale(self.image, (288 * 5, 160 * 5))

                elif frame == 19:
                    Dead_Demon = pygame.image.load("demon_death_19.png")
                    # Sprite from https://chierit.itch.io/boss-demon-slime
                    self.image.blit(Dead_Demon, (0, 0), (0, 0, 288, 160))
                    self.image = pygame.transform.scale(self.image, (288 * 5, 160 * 5))

                elif frame == 20:
                    Dead_Demon = pygame.image.load("demon_death_20.png")
                    # Sprite from https://chierit.itch.io/boss-demon-slime
                    self.image.blit(Dead_Demon, (0, 0), (0, 0, 288, 160))
                    self.image = pygame.transform.scale(self.image, (288 * 5, 160 * 5))

                elif frame == 21:
                    Dead_Demon = pygame.image.load("demon_death_21.png")
                    # Sprite from https://chierit.itch.io/boss-demon-slime
                    self.image.blit(Dead_Demon, (0, 0), (0, 0, 288, 160))
                    self.image = pygame.transform.scale(self.image, (288 * 5, 160 * 5))

                elif frame == 22:
                    Dead_Demon = pygame.image.load("demon_death_22.png")
                    # Sprite from https://chierit.itch.io/boss-demon-slime
                    self.image.blit(Dead_Demon, (0, 0), (0, 0, 288, 160))
                    self.image = pygame.transform.scale(self.image, (288 * 5, 160 * 5))
