import pygame
import sys
import math
import random
from pygame.locals import *

# Import game modules
from player import Player
from universe import Universe
from economy import Economy
from ui import UI
from combat import CombatManager
from entities import Entity, Planet, SpaceStation, WarpGate, Asteroid, EnemyShip

# Initialize pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Game constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60
GAME_TITLE = "Stellar Merchants"
VERSION = "0.1"

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

class Game:
    def __init__(self):
        # Set up display
        # Use fullscreen mode
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # Get the actual screen dimensions
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        pygame.display.set_caption(f"{GAME_TITLE} v{VERSION}")
        self.clock = pygame.time.Clock()
        
        # Initialize game components
        self.running = True
        self.game_state = "MENU"  # MENU, PLAYING, TRADING, MAP, GAME_OVER, UPGRADE
        
        # Game universe
        self.universe = Universe(10, 10)  # 10x10 grid of star systems
        starting_system = self.universe.get_system(5, 5)  # Start in the middle
        
        # Mark starting system as explored
        starting_system.explored = True
        
        # Player
        self.player = Player(self.screen_width // 2, self.screen_height // 2, starting_system)
        
        # Economy
        self.economy = Economy(self.universe)
        
        # UI
        self.ui = UI(self.screen, self.player, self.universe, self.economy)
        
        # Combat
        self.combat_manager = CombatManager(self.player, self.universe)
        
        # Time tracking
        self.last_time = pygame.time.get_ticks()
        self.delta_time = 0
        
        # Load resources
        self.load_resources()
    
    def load_resources(self):
        """Load all game resources (images, sounds, etc)"""
        # In a full implementation, load sprites, sounds, etc.
        # For now, we'll use simple shapes
        
        # You could add sounds like:
        # self.laser_sound = pygame.mixer.Sound('assets/sounds/laser.wav')
        pass
    
    def handle_events(self):
        """Process game events"""
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
                
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if self.game_state in ["PLAYING", "TRADING", "MAP", "UPGRADE"]:
                        self.game_state = "MENU"
                    elif self.game_state == "MENU":
                        self.running = False
                
                elif event.key == K_m:
                    # Toggle map view
                    if self.game_state == "PLAYING":
                        self.game_state = "MAP"
                    elif self.game_state == "MAP":
                        self.game_state = "PLAYING"
                
                elif event.key == K_t and self.player.can_trade():
                    # Toggle trading interface
                    if self.game_state == "PLAYING":
                        self.game_state = "TRADING"
                    elif self.game_state == "TRADING":
                        self.game_state = "PLAYING"
                
                elif event.key == K_u and self.player.can_trade():
                    # Toggle upgrade interface (only at stations)
                    if self.game_state == "PLAYING":
                        self.game_state = "UPGRADE"
                    elif self.game_state == "UPGRADE":
                        self.game_state = "PLAYING"
                
                elif event.key == K_SPACE:
                    # Fire weapon
                    if self.game_state == "PLAYING":
                        self.player.fire_weapon()
                
                elif event.key == K_RETURN and self.game_state == "MENU":
                    # Handle menu selection with Enter key
                    selection = self.ui.main_menu_items[self.ui.selected_menu_item]
                    self.handle_menu_selection(selection)
            
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:  # Left click
                # Handle menu clicks
                if self.game_state == "MENU":
                    mouse_pos = pygame.mouse.get_pos()
                    # Check if click is on a menu item
                    for i, item in enumerate(self.ui.main_menu_items):
                        item_rect = pygame.Rect(
                            self.screen.get_width() // 2 - 100, 
                            200 + i * 50, 
                            200, 40
                        )
                        if item_rect.collidepoint(mouse_pos):
                            self.handle_menu_selection(item)
                            break
                
                            # Handle upgrade button clicks
                elif self.game_state == "UPGRADE":
                    mouse_pos = pygame.mouse.get_pos()
                    for button in self.ui.buttons:
                        if button['state'] == 'upgrade' and button['rect'].collidepoint(mouse_pos):
                            action = button['action']
                            # We'll pass the actual button ID string directly to upgrade_ship
                            # which will handle the conversion to the right attribute name
                            if action in ['upgrade_engine', 'upgrade_weapons', 'upgrade_shields', 
                                         'upgrade_cargo', 'upgrade_sensors']:
                                self.ui.upgrade_ship(action.split('_')[1])
                            elif action == 'close_upgrade':
                                self.game_state = "PLAYING"
            
            # Handle UI events
            self.ui.handle_event(event, self.game_state)
    
    def update(self):
        """Update game state"""
        # Calculate delta time
        current_time = pygame.time.get_ticks()
        self.delta_time = (current_time - self.last_time) / 1000.0  # Convert to seconds
        self.last_time = current_time
        
        if self.game_state == "PLAYING":
            # Update player
            self.player.update(self.delta_time)
            
            # Check for warp gate interactions
            for gate in self.player.current_system.warp_gates:
                if gate.check_collision(self.player) and gate.destination:
                    # Capture the player's current angle before warping
                    entry_angle = self.player.angle
                    self.warp_to_new_system(gate.destination, gate.direction, entry_angle)
            
            # Update entities in current system
            self.universe.update_current_system(self.player.current_system, self.delta_time)
            
            # Update combat
            self.combat_manager.update(self.delta_time)
            
            # Check for trading opportunities
            self.player.update_trade_status()
            
            # Economy updates (slower frequency)
            if current_time % 5000 < self.delta_time * 1000:  # Every 5 seconds
                self.economy.update()
        
        # Update UI regardless of state
        self.ui.update(self.game_state)
    
    def render(self):
        """Render the game"""
        # Clear screen
        self.screen.fill(BLACK)
        
        if self.game_state == "MENU":
            self.ui.render_menu()
            
        elif self.game_state == "PLAYING":
            # Render space background
            self.render_space_background()
            
            # Render all entities in the current system
            self.universe.render_current_system(self.screen, self.player)
            
            # Render player
            self.player.render(self.screen)
            
            # Render combat effects
            self.combat_manager.render(self.screen)
            
            # Render UI elements
            self.ui.render_hud()
            self.ui.render_minimap()
            
        elif self.game_state == "TRADING":
            self.ui.render_trading_interface()
            
        elif self.game_state == "UPGRADE":
            self.ui.render_upgrade_interface()
            
        elif self.game_state == "MAP":
            self.ui.render_galaxy_map()
            
        elif self.game_state == "GAME_OVER":
            self.ui.render_game_over()
        
        # Update display
        pygame.display.flip()
    
    def render_space_background(self):
        """Render a starfield background"""
        # Create a more stable starfield
        if not hasattr(self, 'stars'):
            # Initialize stars when first called
            self.stars = []
            for _ in range(300):  # Increased number of stars
                self.stars.append({
                    'x': random.randint(0, self.screen_width),
                    'y': random.randint(0, self.screen_height),
                    'radius': random.uniform(0.5, 2.0),
                    'brightness': random.randint(100, 255),
                    'speed': random.uniform(0.1, 0.5)  # Slow movement speed
                })
        
        # Update and draw stars
        for star in self.stars:
            # Slowly move stars from top to bottom to create parallax effect
            star['y'] += star['speed']
            
            # Wrap stars that go off screen
            if star['y'] > self.screen_height:
                star['y'] = 0
                star['x'] = random.randint(0, self.screen_width)
            
            # Draw the star
            brightness = star['brightness']
            color = (brightness, brightness, brightness)
            pygame.draw.circle(self.screen, color, (int(star['x']), int(star['y'])), star['radius'])
    
    def warp_to_new_system(self, destination_system, entry_direction, entry_angle):
        """Handle warping to a new star system"""
        self.player.current_system = destination_system
        
        # Determine exit gate based on entry direction
        opposite_direction = {
            "North": "South",
            "South": "North",
            "East": "West",
            "West": "East"
        }
        
        exit_direction = opposite_direction[entry_direction]
        
        # Find the exit gate in the destination system
        exit_gate = None
        for gate in destination_system.warp_gates:
            if gate.direction == exit_direction:
                exit_gate = gate
                break
        
        # Position player at the exit gate
        if exit_gate:
            # Position just outside the gate, so we don't immediately trigger it again
            offset_distance = 50  # Distance to offset from gate center
            
            # Set player position at the exit gate
            self.player.x = exit_gate.x
            self.player.y = exit_gate.y
            
            # Apply a small offset based on the player's angle to prevent re-triggering
            self.player.x += math.cos(entry_angle) * offset_distance
            self.player.y += math.sin(entry_angle) * offset_distance
            
            # Maintain the player's original angle
            self.player.angle = entry_angle
            
            # Set a consistent exit velocity in the direction the player is facing
            exit_speed = 50  # Consistent, moderate exit speed
            self.player.vx = math.cos(entry_angle) * exit_speed
            self.player.vy = math.sin(entry_angle) * exit_speed
        else:
            # Fallback if no matching gate is found
            self.player.x = self.screen_width // 2
            self.player.y = self.screen_height // 2
            self.player.vx = 0
            self.player.vy = 0
        
        # If the system was unexplored, mark it as explored
        destination_system.explored = True
        
        # Play warp sound effect (would be implemented in full game)
        # pygame.mixer.Sound('assets/sounds/warp.wav').play()
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
        
    def handle_menu_selection(self, menu_item):
        """Handle menu selections"""
        if menu_item == "New Game":
            print("Starting new game...")
            self.game_state = "PLAYING"
        elif menu_item == "Load Game":
            # In a full implementation, this would load a saved game
            print("Load game not implemented yet")
        elif menu_item == "Options":
            # In a full implementation, this would show an options screen
            print("Options not implemented yet")
        elif menu_item == "Exit":
            self.running = False
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
