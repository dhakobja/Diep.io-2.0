import pygame
from PodSixNet.Connection import ConnectionListener, connection

import os
import sys

# This is needed so that the file can import Screen and Camera from the main project directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from Screen.screen import Screen
from Camera.camera import Camera
from Players.player import StandardClass
from Orbs.orbs import SmallOrb, MediumOrb, LargeOrb
from Bullets.bullets import Bullet

class GameClient(ConnectionListener):
    def __init__(self, host, port):
        self.Connect((host, port))
        pygame.init()

        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.screen = Screen(800, 600)
        self.camera = None
        self.player = None
        self.players = {}
        self.orbs = []
        self.run = True
    
    def Loop(self):
        connection.Pump()
        self.Pump()

    def Network_initialize_player(self, data):
        self.player = StandardClass(data["player_id"], self.screen.width, self.screen.height)
        self.player.position = data["position"]
        self.camera = Camera(self.player, self.screen.width, self.screen.height)
        self.camera.update()
    
    def Network_connected(self, data):
        print("You are now connected to the server")
    
    def Network_myresponse(self, data):
        print("Server response: ", data)
    
    def Network_update_players(self, data):
        for player_data in data['players']:
            player_id = player_data['player_id']
            if player_id not in self.players:
                self.players[player_id] = StandardClass(player_data['player_id'])

            # Update player properties
            self.players[player_id].position = player_data['position']
            self.players[player_id].level = player_data['level']
            self.players[player_id].xp = player_data['xp']

            # If the updated player is the main player this client controls, update the camera
            if self.player and player_id == self.player.name:
                self.camera.target = self.players[player_id]  # Ensure camera's target is correctly set
                self.camera.update()
    
    def Network_update_bullets(self, data):
        bullet_states = data['bullets']
        for bullet_state in bullet_states:
            player_id = bullet_state['player_id']
            if player_id in self.players:
                self.players[player_id].bullets = [
                    Bullet(position=bullet['position'], direction=bullet['direction'])
                    for bullet in bullet_state['bullet_data']
                ]
        
    def Network_initialize_orbs(self, data):
        temp_orbs = {orb.id: orb for orb in self.orbs}  # Existing orbs by id
        new_orbs = []
        for orb_data in data['orbs']:
            orb = temp_orbs.get(orb_data['id'])
            if orb:
                orb.position = orb_data['position']
                orb.health = orb_data['health']
            else:
                # Create new orb based on type
                if orb_data['type'] == 'SmallOrb':
                    orb = SmallOrb(position=orb_data['position'], health=orb_data['health'])
                elif orb_data['type'] == 'MediumOrb':
                    orb = MediumOrb(position=orb_data['position'], health=orb_data['health'])
                elif orb_data['type'] == 'LargeOrb':
                    orb = LargeOrb(position=orb_data['position'], health=orb_data['health'])
                orb.id = orb_data['id']  # Make sure to assign the ID from the data
            new_orbs.append(orb)
        self.orbs = new_orbs
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
        
        self.send_movement()
        self.send_shoot_bullet()

    def send_movement(self):
        keys = pygame.key.get_pressed()
        movement_data = {
            'left': keys[pygame.K_a],
            'right': keys[pygame.K_d],
            'up': keys[pygame.K_w],
            'down': keys[pygame.K_s]
        }

        self.Send({"action": "move_player", "data": movement_data})
    
    def send_shoot_bullet(self):
        keys = pygame.key.get_pressed()
        direction_data = {
            'left': keys[pygame.K_LEFT],
            'right': keys[pygame.K_RIGHT],
            'up': keys[pygame.K_UP],
            'down': keys[pygame.K_DOWN]
        }

        self.Send({"action": "shoot_bullet", "data": direction_data})

    def draw(self):
        if not self.camera:
            return
        self.screen.clear_screen()
        
        # Draw the players
        for player in self.players.values():
            player.draw(self.screen.get_surface(), self.camera)
            for bullet in player.bullets:
                bullet.draw(self.screen.get_surface(), self.camera.apply(bullet.position))

        # Draw the orbs
        for orb in self.orbs:
            orb.draw(self.screen.get_surface(), self.camera)
        self.screen.update_display()
    
    def run_game(self):
        while self.run:
            self.Loop()
            self.handle_events()
            if self.camera:
                self.camera.update()
            self.draw()
            self.clock.tick(self.FPS)
        pygame.quit()

if __name__ == "__main__":
    client = GameClient("localhost", 31425)
    client.run_game()
