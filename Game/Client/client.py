import pygame
from pygame.sprite import LayeredUpdates
from PodSixNet.Connection import ConnectionListener, connection

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
        self.screen = Screen(1200, 700)
        self.camera = None
        self.player = None
        self.players = {}
        self.orbs = []
        self.group = LayeredUpdates()
        self.run = True
    
    def Loop(self):
        connection.Pump()
        self.Pump()

    def Network_initialize_player(self, data):
        player_id = data["player_id"]
        self.player = StandardClass(player_id, self.group)
        self.player.position = data["position"]

        # Add the player to the players dictionary
        if player_id not in self.players:
            self.players[player_id] = self.player

        self.camera = Camera(self.player, self.screen.width, self.screen.height)
        self.camera.update()
        print("Player initialized")
    
    def Network_connected(self, data):
        print("You are now connected to the server")
    
    def Network_myresponse(self, data):
        print("Server response: ", data)
    
    def Network_update_players(self, data):
        for player_data in data['players']:
            # Remove players that are no longer in the game
            for player_id in self.players.copy():
                if player_id not in [player['player_id'] for player in data['players']]:
                    self.players.pop(player_id)

            # Add players that are new to the game
            player_id = player_data['player_id']

            # Update player properties
            self.players[player_id].position = player_data['position']
            self.players[player_id].level = player_data['level']
            self.players[player_id].xp = player_data['xp']
            self.players[player_id].max_xp = player_data['max_xp']
            self.players[player_id].health = player_data['health']

            # If the updated player is the main player this client controls, update the player and camera
            if self.player and player_id == self.player.name:
                self.player = self.players[player_id]  # Ensure player is correctly set
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
                    orb = SmallOrb(orb_data['position'], orb_data['health'], self.group)
                elif orb_data['type'] == 'MediumOrb':
                    orb = MediumOrb(orb_data['position'], orb_data['health'], self.group)
                elif orb_data['type'] == 'LargeOrb':
                    orb = LargeOrb(orb_data['position'], orb_data['health'], self.group)
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
        # for player in self.players.values():
        #     player.draw(self.screen.get_surface(), self.camera)
        #     for bullet in player.bullets:
        #         bullet.draw(self.screen.get_surface(), self.camera.apply(bullet.position))
        self.group.draw(self.screen.get_surface())

        # Draw the orbs
        for orb in self.orbs:
            orb.draw(self.screen.get_surface(), self.camera)
        
        # Draw the player's specific information
        self.draw_player_specifics()

        self.screen.update_display()
    
    def draw_player_specifics(self):
        # Draw the player's current and max XP
        if self.player:
            self.player.draw_player_specifics(self.screen.get_surface())
    
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
