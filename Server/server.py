import pygame

from PodSixNet.Channel import Channel
from PodSixNet.Server import Server

import uuid

import os
import sys

# This is needed so that the file can import Screen and Camera from the main project directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from Orbs.orbs import SmallOrb
from Players.player import StandardClass

class ClientChannel(Channel):
    
    def Network(self, data):
        #print(f"Received from {self.id}: {data}")
        pass

    def Network_myaction(self, data):
        # Process action, update game state
        response = {"action": "update", "data": data}
        self._server.send_to_all(response)

    def Close(self):
        self._server.remove_player(self.id)

    def Network_move_player(self, data):
        player = self._server.players.get(self.id)
        if player:
            # Calculate new position based on movement data
            dx = -player.speed if data['data']['left'] else player.speed if data['data']['right'] else 0
            dy = -player.speed if data['data']['up'] else player.speed if data['data']['down'] else 0
            player.position[0] = max(0, min(self._server.world_width - player.width, player.position[0] + dx))
            player.position[1] = max(0, min(self._server.world_height - player.height, player.position[1] + dy))
        
    def Network_shoot_bullet(self, data):
        player = self._server.players.get(self.id)
        if player:
            player.shooting(data['data'])

class GameServer(Server):
    channelClass = ClientChannel

    def __init__(self):
        super().__init__(localaddr=("localhost", 31425))
        self.world_width = 2400
        self.world_height = 1800
        self.players = {}
        self.orbs = [SmallOrb() for _ in range(30)]
        self.player_id_counter = 0

    def Connected(self, channel, addr):
        # Initialize a new player and send the player ID to the client
        player_id = str(uuid.uuid4())
        channel.id = player_id
        new_player = StandardClass("PlayerName", self.world_width, self.world_height)
        self.players[player_id] = new_player
        channel.Send({"action": "initialize_player", "player_id": player_id, "position": new_player.position})
        print(f"New connection: {player_id} from {addr}")
        self.broadcast_player_states()

        # Send the orbs to the client
        self.send_orbs_to_client()

    def broadcast_player_states(self):
        player_states = []
        for player_id, player in self.players.items():
            player_states.append({
                'player_id': player_id,
                'position': player.position,
                'level': player.level,
                'xp': player.xp,
            })
        self.SendToAll({"action": "update_players", "players": player_states})
    
    def broadcast_bullet_states(self):
        bullet_states = []
        for player_id, player in self.players.items():
            # Convert the bullets to a serializable format, so that we can send it to the client with the SendToAll method
            # (doesn't support sending objects that are not serializable, like the Bullet class)
            bullet_data = [{
                'position': bullet.position,
                'direction': bullet.direction
            } for bullet in player.bullets]
            bullet_states.append({
                'player_id': player_id,
                'bullet_data': bullet_data
            })
        self.SendToAll({"action": "update_bullets", "bullets": bullet_states})
    
    def update_bullets(self):
        for player in self.players.values():
            player.update_bullets()

        self.broadcast_bullet_states()

    def send_orbs_to_client(self):
        orb_data = [{
            "id": id(orb),
            "position": orb.position,
            "health": orb.health,
        } for orb in self.orbs]
        self.SendToAll({"action": "initialize_orbs", "orbs": orb_data})

    def check_collisions(self):
        for player_id, player in self.players.items():
            for orb in self.orbs[:]:
                if orb.collide_with_player(player):
                    player.add_xp(orb.xp_value)
                    # Remove the orb that was collected and send a message to all clients
                    self.orbs.remove(orb)
                    self.SendToAll({"action": "remove_orb", "id": id(orb)})
                    # Add a new orb to the game and send the updated list to all clients
                    self.orbs.append(SmallOrb())
                    self.send_orbs_to_client()

    def SendToAll(self, data):
        # Broadcast data to all connected clients
        for channel in self.channels:
            channel.Send(data)
    
    def remove_player(self, player_id):
        if player_id in self.players:
            del self.players[player_id]
            print(f"Player {player_id} has been removed")

if __name__ == "__main__":
    game_server = GameServer()
    while True:
        game_server.Pump()
        game_server.check_collisions()
        game_server.update_bullets()
        game_server.broadcast_bullet_states()
        game_server.broadcast_player_states()
        pygame.time.wait(1000 // 60)  # Maintain a Loop at 60 FPS