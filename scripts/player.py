import pygame
from scripts.utils import load_sprite
from scripts.bezier import Bezier

class Player:
    def __init__(self, game, name, pos, sprite, size):
        self.game = game
        self.name = name
        self.sprite = load_sprite(game,sprite,size)
        self.size = size
        self.pos = list(pos)
        self.velocity = [0,0]

        self.speed = 2
        self.rotation = 0
        self.collisions = {'down' : False, 'right': False, 'up': False, 'left': False}
        self.frame_movement = [0,0]
        self.legs = []


        self.jump_frame = False
        self.jump_height = 2
        self.allowed_jumps = 1

    def rect(self):
        return pygame.Rect(*self.pos, *self.size)


    def update(self, movement):
        self.collisions = {'down' : False, 'right': False, 'up': False, 'left': False}
        
        self.frame_movement = (self.speed*(movement[0] + self.velocity[0]), self.speed*(movement[1] + self.velocity[1]))
        
        # Horizontal Movement
        self.pos[0] += self.frame_movement[0]
        current_rect = self.rect()
        for tile in self.game.get_close_tiles(self.pos):
            if tile.interactable is True:
                if self.rect().colliderect(tile.rect()):
                    if self.frame_movement[0] > 0:
                        current_rect.right = tile.rect().left
                        self.collisions['right'] = True
                    elif self.frame_movement[0] < 0:
                        current_rect.left = tile.rect().right
                        self.collisions['left'] = True
                    self.pos[0] = current_rect.x

        if self.collisions['right'] or self.collisions['left']:
            self.velocity[0] = 0

        # Vertical Movement       
        self.pos[1] += self.frame_movement[1]
        current_rect = self.rect()
        for tile in self.game.get_close_tiles(self.pos):
            if tile.interactable is True:
                if self.rect().colliderect(tile.rect()):
                    if self.frame_movement[1] > 0:
                        current_rect.bottom = tile.rect().top
                        self.collisions['down'] = True
                        self.allowed_jumps = 1
                    elif self.frame_movement[1] < 0:
                        current_rect.top = tile.rect().bottom
                        self.collisions['up'] = True

                    self.pos[1] = current_rect.y


        # Gravity
        self.velocity[1] = min(3,self.velocity[1]+0)

        if self.collisions['up'] or self.collisions['down']:
            self.velocity[1] = 0
        

        # Legs
        for leg in self.legs:
            leg.update()


        self.render(self.game.display)

    def jump(self):
        if self.allowed_jumps:
            self.allowed_jumps -= 1
            self.velocity[1] = -2

    def render(self, display):
        frame_rotation = 0

        if self.collisions['down']:
            if self.frame_movement[0] > 0:
                frame_rotation -= 10
            if self.frame_movement[0] < 0:
                frame_rotation += 10
        self.rotation += frame_rotation

        
        #self.sprite = pygame.transform.rotate(self.sprite, frame_rotation)
        #self.sprite = pygame.transform.rotate(self.sprite, 10)
        #rotated_sprite = pygame.transform.rotate(self.sprite,self.rotation)
        
        display.blit(self.sprite, self.pos)


