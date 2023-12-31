import pygame
from UI import UIManager
import projectiles
from Weapons import Weapon
from Weapons import FlamingDeco
from Weapons import FrostyDeco
from Weapons import ShroomDeco
from pygame.math import Vector2
from map.map import *
from Entities.Entity import *
import os.path 
from Inventory import getIndexToReplace
from Inventory import InventoryManager
from random import randint

DEBUG = 0

# weapons that user starts game with
defaultWeapons = {
    "pistol": "The Blickey",
    "shotgun": None,
    "machineGun": None
}

# default Items
defaultItems = {
    "healthPotions": None,
    "manaPotions": None
}

# default stats
defaultStats = {
    "Attack": 0,
    "Defense": 0,
    "Speed": 0,
    "HP": 100,
    "Mana": 50
}


class Game:
    def __init__(self):
        """
        Start up Pygame and instantiate all
        relevant actors.
        @width : sets width of the screen
        @height : sets height of the screen
        """
        # https://www.mygreatlearning.com/blog/global-variables-in-python/#:~:text=However%2C%20if%20you%20want%20to,would%20in%20a%20regular%20function.&text=Access%20across%20modules%3A%20Global%20variables,modules%20within%20the%20same%20program.
        global pistol 
        pistol = Weapon(self, 1.0, 2.0, 10, 1.5 , .3, 5)
        global shotgun
        shotgun = Weapon(self, .65, 10, 4, 15, .7, 3) 
        global machineGun
        machineGun = Weapon(self, 15, 5, 45, 7, .25, 10)

        self.projectiles = []
        self.FPS = 120
        self.TILESIZE = 40
        self.MAPWIDTH = 45
        self.MAPHEIGHT = 24
        pygame.init()
        self.clock = pygame.time.Clock()
        self.inventory = InventoryManager()
        self.inventory.addItem(pistol)
        self.inventory.addItem(shotgun)
        self.inventory.addItem(machineGun)
        self.screen = pygame.display.set_mode((self.MAPWIDTH * self.TILESIZE, self.MAPHEIGHT * self.TILESIZE))
        self.UI = UIManager(defaultStats, self.inventory, self.screen)
        self.player = Player(23*self.TILESIZE,12*self.TILESIZE,50,50)
        self.map = Map(self.player,self.screen)
        self.shooting = False
        # this allows us to filter the event queue
        # for faster event processing
        pygame.event.set_allowed([
            pygame.QUIT,
            pygame.KEYDOWN
        ])
        try: # Attempt to delete the angle debug file so new data is shown each run
            os.remove('angledbg.log')
        except OSError:
            pass
        


    def loop(self):
        
        """
        Primary game loop. This should be
        run perpetually until the game is
        over or is closed.
        """
        self.currentWeapon = pistol
        self.screen.fill("black")
        while True:
            #print(self.clock.get_fps())
            keys = pygame.key.get_pressed()
            if(self.UI.pMenu.isActive()): 
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                self.UI.update(keys, defaultStats)
                pygame.display.flip()
                # pygame.display.update()
                self.clock.tick(self.FPS)
            else: 
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    if(keys[pygame.K_x]): 
                        defaultStats["Attack"] += randint(0, 10)
                        defaultStats["Defense"] += randint(0, 10)
                        defaultStats["Speed"] += randint(0, 10) 
                        defaultStats["HP"] += randint(0, 10)
                        defaultStats["Mana"] += randint(0, 10)
                    if(keys[pygame.K_z]):      
                        self.inventory.addItem(100)
                    if(keys[pygame.K_q]): 
                        self.inventory.useItem("healthPot")
                    if(keys[pygame.K_e]): 
                        self.inventory.useItem("manaPot")
                    if(keys[pygame.K_8]): 
                        if(not isinstance(self.inventory.getItem(Weapon, 0), FlamingDeco)): 
                           flamingPistol = FlamingDeco(self.screen, pistol)
                           self.inventory.addItem(flamingPistol)

                    if(keys[pygame.K_9]): 
                        if(not isinstance(self.inventory.getItem(Weapon, 1), FrostyDeco)): 
                            frostyShotgun = FrostyDeco(self.screen, shotgun)
                            self.inventory.addItem(frostyShotgun)

                    if(keys[pygame.K_0]): 
                        if(not isinstance(self.inventory.getItem(Weapon, 2), ShroomDeco)): 
                            shroomMachineGun = ShroomDeco(self.screen, machineGun)
                            self.inventory.addItem(shroomMachineGun)

                    if(keys[pygame.K_1]): 
                        self.currentWeapon = self.inventory.getItem(Weapon, 0)
                    elif(keys[pygame.K_2]): 
                        if(len(self.inventory.getItem(Weapon)) > 1):
                            self.currentWeapon = self.inventory.getItem(Weapon, 1)
                    elif(keys[pygame.K_3]): 
                        if(len(self.inventory.getItem(Weapon)) > 2): 
                            self.currentWeapon = self.inventory.getItem(Weapon, 2)

                    if((event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1)): 
                        self.shooting = True

                    if((event.type == pygame.MOUSEBUTTONUP) and (event.button == 1)): 
                        self.shooting = False

                    if(self.shooting): 
                        player_rect = self.player.rect
                        player_center = Vector2(self.player.rect.centerx, self.player.rect.centery)
                        mouse_pos = pygame.mouse.get_pos()
                        direction = self.player.player_dir                
                        new_projectiles = self.inventory.useItem(self.currentWeapon, player_center, self.player.player_dir)
                        if new_projectiles is not None:
                            self.projectiles.extend(new_projectiles)

                self.screen.fill("black")
                self.map.update(self.screen)
                # Update projectiles
                for p in self.projectiles:
                    p.update()
                    p.draw(self.screen)
                self.UI.update(keys, defaultStats)
                pygame.display.flip()
                # pygame.display.update()
                self.clock.tick(self.FPS)


if __name__ == "__main__":
    game = Game()
    game.loop()
    
