import pygame
import math
import random
from pygame.locals import *

class UI:
    """Manages all game user interface elements"""
    def __init__(self, screen, player, universe, economy):
        self.screen = screen
        self.player = player
        self.universe = universe
        self.economy = economy
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (100, 100, 100)
        self.LIGHT_GRAY = (200, 200, 200)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        self.CYAN = (0, 255, 255)
        self.PURPLE = (150, 0, 150)
        
        # Fonts
        self.title_font = pygame.font.SysFont(None, 48)
        self.header_font = pygame.font.SysFont(None, 32)
        self.normal_font = pygame.font.SysFont(None, 24)
        self.small_font = pygame.font.SysFont(None, 18)
        
        # UI state
        self.selected_menu_item = 0
        self.selected_commodity = 0
        self.trading_scroll_offset = 0
        self.map_scroll_offset = (0, 0)
        self.show_trade_details = False
        self.show_help = False
        self.notification_text = ""
        self.notification_timer = 0
        self.selected_upgrade = 0
        
        # Menu items
        self.main_menu_items = ["New Game", "Load Game", "Options", "Exit"]
        self.pause_menu_items = ["Resume", "Save Game", "Options", "Quit to Menu"]
        
        # Buttons and UI elements
        self.buttons = []
        self.initialize_ui_elements()
    
    def initialize_ui_elements(self):
        """Create UI elements like buttons"""
        # Trading interface buttons
        self.buttons.append({
            'id': 'buy',
            'rect': pygame.Rect(self.screen.get_width() - 220, self.screen.get_height() - 100, 100, 40),
            'text': "Buy",
            'action': 'buy_commodity',
            'state': 'trading'
        })
        
        self.buttons.append({
            'id': 'sell',
            'rect': pygame.Rect(self.screen.get_width() - 110, self.screen.get_height() - 100, 100, 40),
            'text': "Sell",
            'action': 'sell_commodity',
            'state': 'trading'
        })
        
        self.buttons.append({
            'id': 'close_trading',
            'rect': pygame.Rect(self.screen.get_width() - 110, self.screen.get_height() - 50, 100, 40),
            'text': "Close",
            'action': 'close_trading',
            'state': 'trading'
        })
        
        # Upgrade buttons
        self.buttons.append({
            'id': 'upgrade_engine',
            'rect': pygame.Rect(self.screen.get_width() - 220, 200, 200, 40),
            'text': "Upgrade Engine",
            'action': 'upgrade_engine',
            'state': 'upgrade'
        })
        
        self.buttons.append({
            'id': 'upgrade_weapons',
            'rect': pygame.Rect(self.screen.get_width() - 220, 250, 200, 40),
            'text': "Upgrade Weapons",
            'action': 'upgrade_weapons',
            'state': 'upgrade'
        })
        
        self.buttons.append({
            'id': 'upgrade_shields',
            'rect': pygame.Rect(self.screen.get_width() - 220, 300, 200, 40),
            'text': "Upgrade Shields",
            'action': 'upgrade_shields',
            'state': 'upgrade'
        })
        
        self.buttons.append({
            'id': 'upgrade_cargo',
            'rect': pygame.Rect(self.screen.get_width() - 220, 350, 200, 40),
            'text': "Upgrade Cargo",
            'action': 'upgrade_cargo',
            'state': 'upgrade'
        })
        
        self.buttons.append({
            'id': 'upgrade_sensors',
            'rect': pygame.Rect(self.screen.get_width() - 220, 400, 200, 40),
            'text': "Upgrade Sensors",
            'action': 'upgrade_sensors',
            'state': 'upgrade'
        })
        
        self.buttons.append({
            'id': 'close_upgrade',
            'rect': pygame.Rect(self.screen.get_width() - 220, 450, 200, 40),
            'text': "Close",
            'action': 'close_upgrade',
            'state': 'upgrade'
        })
    
    def handle_event(self, event, game_state):
        """Process UI-related events"""
        if event.type == MOUSEBUTTONDOWN:
            # Check for button clicks
            mouse_pos = pygame.mouse.get_pos()
            
            for button in self.buttons:
                if button['state'] == game_state.lower() and button['rect'].collidepoint(mouse_pos):
                    self.handle_button_action(button['action'])
                    return True
            
            # Trading item selection
            if game_state == "TRADING":
                # Check if clicking on commodity list
                trading_area = pygame.Rect(50, 150, self.screen.get_width() - 100, self.screen.get_height() - 300)
                if trading_area.collidepoint(mouse_pos):
                    # Calculate which item was clicked based on position
                    item_height = 30
                    item_index = (mouse_pos[1] - 150 + self.trading_scroll_offset) // item_height
                    
                    # Get market data
                    market = self.economy.get_system_market(self.player.current_system)
                    
                    # Check if valid index
                    if 0 <= item_index < len(market):
                        self.selected_commodity = item_index
                        self.show_trade_details = True
                        return True
            
            # Map system selection
            elif game_state == "MAP":
                # Check for system clicks on galaxy map
                explored_systems = [system for coords, system in self.universe.systems.items() if system.explored]
                
                for system in explored_systems:
                    # Calculate screen position with scroll offset
                    screen_x = system.map_x - self.map_scroll_offset[0]
                    screen_y = system.map_y - self.map_scroll_offset[1]
                    
                    # Check if clicking near system
                    if math.sqrt((mouse_pos[0] - screen_x)**2 + (mouse_pos[1] - screen_y)**2) < 15:
                        # Select this system
                        self.show_system_details(system)
                        return True
        
        elif event.type == MOUSEBUTTONUP:
            # Handle scrolling
            if event.button == 4:  # Scroll up
                if game_state == "TRADING":
                    self.trading_scroll_offset = max(0, self.trading_scroll_offset - 30)
                elif game_state == "MAP":
                    self.map_scroll_offset = (self.map_scroll_offset[0], max(0, self.map_scroll_offset[1] - 30))
            
            elif event.button == 5:  # Scroll down
                if game_state == "TRADING":
                    # Get maximum scroll (based on number of items)
                    market = self.economy.get_system_market(self.player.current_system)
                    max_scroll = max(0, len(market) * 30 - (self.screen.get_height() - 300))
                    self.trading_scroll_offset = min(max_scroll, self.trading_scroll_offset + 30)
                elif game_state == "MAP":
                    # Maximum map scroll would depend on galaxy size
                    max_x = max(0, self.universe.width * 80 - self.screen.get_width())
                    max_y = max(0, self.universe.height * 80 - self.screen.get_height())
                    new_y = min(max_y, self.map_scroll_offset[1] + 30)
                    self.map_scroll_offset = (self.map_scroll_offset[0], new_y)
        
        elif event.type == KEYDOWN:
            # Menu navigation
            if game_state == "MENU":
                if event.key == K_UP:
                    self.selected_menu_item = (self.selected_menu_item - 1) % len(self.main_menu_items)
                elif event.key == K_DOWN:
                    self.selected_menu_item = (self.selected_menu_item + 1) % len(self.main_menu_items)
                elif event.key == K_RETURN:
                    self.handle_menu_selection(self.main_menu_items[self.selected_menu_item])
            
            # Trading interface
            elif game_state == "TRADING":
                if event.key == K_UP:
                    # Move selection up
                    self.selected_commodity = max(0, self.selected_commodity - 1)
                    # Scroll if needed
                    if self.selected_commodity * 30 < self.trading_scroll_offset:
                        self.trading_scroll_offset = self.selected_commodity * 30
                elif event.key == K_DOWN:
                    # Get market data
                    market = self.economy.get_system_market(self.player.current_system)
                    # Move selection down
                    self.selected_commodity = min(len(market) - 1, self.selected_commodity + 1)
                    # Scroll if needed
                    if (self.selected_commodity + 1) * 30 > self.trading_scroll_offset + (self.screen.get_height() - 300):
                        self.trading_scroll_offset = (self.selected_commodity + 1) * 30 - (self.screen.get_height() - 300)
                elif event.key == K_b:
                    # Buy selected commodity
                    self.buy_selected_commodity()
                elif event.key == K_s:
                    # Sell selected commodity
                    self.sell_selected_commodity()
            
            # Help toggle
            if event.key == K_h:
                self.show_help = not self.show_help
        
        return False
    
    def handle_button_action(self, action):
        """Process button actions"""
        if action == 'buy_commodity':
            self.buy_selected_commodity()
        elif action == 'sell_commodity':
            self.sell_selected_commodity()
        elif action == 'close_trading':
            # Return to playing state (would be handled by game)
            pass
        elif action == 'upgrade_engine':
            self.upgrade_ship('engine')
        elif action == 'upgrade_weapons':
            self.upgrade_ship('weapons')
        elif action == 'upgrade_shields':
            self.upgrade_ship('shields')
        elif action == 'upgrade_cargo':
            self.upgrade_ship('cargo')
        elif action == 'upgrade_sensors':
            self.upgrade_ship('sensors')
        elif action == 'close_upgrade':
            # Return to playing state (would be handled by game)
            pass
    
    def handle_menu_selection(self, menu_item):
        """Process menu selections"""
        # This method just passes the selection to the game's handle_menu_selection method
        # The game class actually changes game states
        if menu_item in self.main_menu_items:
            print(f"Selected menu item: {menu_item}")
            return menu_item
        return None
    
    def buy_selected_commodity(self):
        """Buy the currently selected commodity"""
        # Get market data
        market = self.economy.get_system_market(self.player.current_system)
        
        # Check if valid selection
        if 0 <= self.selected_commodity < len(market):
            item = market[self.selected_commodity]
            
            # Default to buying 1 unit
            quantity = 1
            
            # In a full implementation, would show a quantity input dialog
            # For now, hardcode to 1 unit
            
            # Try to buy
            success, message = self.economy.buy_commodity(
                self.player, 
                self.player.current_system, 
                item['commodity'].name, 
                quantity
            )
            
            # Show notification
            self.show_notification(message)
    
    def sell_selected_commodity(self):
        """Sell the currently selected commodity"""
        # Get market data
        market = self.economy.get_system_market(self.player.current_system)
        
        # Check if valid selection
        if 0 <= self.selected_commodity < len(market):
            item = market[self.selected_commodity]
            
            # Check if player has any of this commodity
            if item['commodity'].name in self.player.cargo and self.player.cargo[item['commodity'].name] > 0:
                # Default to selling 1 unit
                quantity = 1
                
                # In a full implementation, would show a quantity input dialog
                # For now, hardcode to 1 unit
                
                # Try to sell
                success, message = self.economy.sell_commodity(
                    self.player, 
                    self.player.current_system, 
                    item['commodity'].name, 
                    quantity
                )
                
                # Show notification
                self.show_notification(message)
            else:
                self.show_notification("You don't have any of this commodity to sell")
    
    def upgrade_ship(self, upgrade_type):
        """Upgrade a ship component"""
        # Ensure attribute name matches player's attribute
        attribute_name = upgrade_type
        if upgrade_type == "weapons":
            attribute_name = "weapon"
        elif upgrade_type == "shields":
            attribute_name = "shield"
        elif upgrade_type == "sensors":
            attribute_name = "sensor"
            
        # Upgrade costs (increasing with level)
        upgrade_costs = {
            'engine': [1000, 2500, 5000, 10000, 20000],
            'weapon': [1500, 3000, 6000, 12000, 24000],
            'shield': [2000, 4000, 8000, 16000, 32000],
            'cargo': [1000, 2000, 4000, 8000, 16000],
            'sensor': [800, 1600, 3200, 6400, 12800]
        }
        
        # Get current level and check if max level
        current_level = getattr(self.player, f"{attribute_name}_level")
        if current_level >= 5:  # Max level is 5
            self.show_notification(f"{upgrade_type.capitalize()} already at maximum level")
            return
        
        # Get upgrade cost
        cost = upgrade_costs[attribute_name][current_level - 1]
        
        # Check if player has enough credits
        if self.player.credits >= cost:
            # Deduct credits
            self.player.credits -= cost
            
            # Apply upgrade
            if attribute_name == 'engine':
                self.player.upgrade_engine()
            elif attribute_name == 'weapon':
                self.player.upgrade_weapon()
            elif attribute_name == 'shield':
                self.player.upgrade_shield()
            elif attribute_name == 'cargo':
                self.player.upgrade_cargo()
            elif attribute_name == 'sensor':
                self.player.upgrade_sensors()
            
            self.show_notification(f"{upgrade_type.capitalize()} upgraded to level {current_level + 1}")
        else:
            self.show_notification(f"Not enough credits for upgrade (need {cost})")
    
    def show_notification(self, text):
        """Display a notification message"""
        self.notification_text = text
        self.notification_timer = 3.0  # Show for 3 seconds
    
    def show_system_details(self, system):
        """Show details about a selected system on the map"""
        # In a full implementation, would show a dialog with system details
        # For now, just print to console
        print(f"System: {system.name}")
        print(f"Type: {system.system_type}")
        print(f"Faction: {system.faction}")
        print(f"Tech Level: {system.tech_level}")
        print(f"Danger Level: {system.danger_level}")
    
    def update(self, game_state):
        """Update UI state"""
        # Update notification timer
        if self.notification_timer > 0:
            self.notification_timer -= 1/60  # Assuming 60 FPS
            if self.notification_timer <= 0:
                self.notification_text = ""
    
    def render_menu(self):
        """Render the main menu"""
        # Clear screen with space background
        self.screen.fill(self.BLACK)
        
        # Create stable starfield if not already created
        if not hasattr(self, 'menu_stars'):
            self.menu_stars = []
            for _ in range(300):  # Increased number of stars
                self.menu_stars.append({
                    'x': random.randint(0, self.screen.get_width()),
                    'y': random.randint(0, self.screen.get_height()),
                    'radius': random.uniform(0.5, 2.0),
                    'brightness': random.randint(100, 255),
                    'speed': random.uniform(0.1, 0.3)  # Slow movement speed
                })
        
        # Update and draw stars
        for star in self.menu_stars:
            # Slowly move stars from top to bottom
            star['y'] += star['speed']
            
            # Wrap stars that go off screen
            if star['y'] > self.screen.get_height():
                star['y'] = 0
                star['x'] = random.randint(0, self.screen.get_width())
            
            # Draw the star
            brightness = star['brightness']
            color = (brightness, brightness, brightness)
            pygame.draw.circle(self.screen, color, (int(star['x']), int(star['y'])), star['radius'])
        
        # Draw title
        title = self.title_font.render("STELLAR MERCHANTS", True, self.YELLOW)
        self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 100))
        
        # Draw menu items with background rectangles for better visibility and clicking
        for i, item in enumerate(self.main_menu_items):
            item_rect = pygame.Rect(self.screen.get_width() // 2 - 100, 200 + i * 50, 200, 40)
            
            # Draw background for better visibility
            if i == self.selected_menu_item:
                pygame.draw.rect(self.screen, (40, 40, 80), item_rect, border_radius=5)
                color = self.YELLOW
                # Draw selection arrow
                arrow = self.normal_font.render("> ", True, self.YELLOW)
                self.screen.blit(arrow, (self.screen.get_width() // 2 - 120, 200 + i * 50 + 5))
            else:
                pygame.draw.rect(self.screen, (20, 20, 40), item_rect, border_radius=5)
                color = self.WHITE
            
            # Draw border around button
            pygame.draw.rect(self.screen, self.GRAY, item_rect, 1, border_radius=5)
            
            text = self.normal_font.render(item, True, color)
            self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, 205 + i * 50))
        
        # Draw instructions
        instructions = self.small_font.render("Use arrow keys to select, Enter to confirm", True, self.LIGHT_GRAY)
        self.screen.blit(instructions, (self.screen.get_width() // 2 - instructions.get_width() // 2, 
                                       self.screen.get_height() - 60))
        
        # Draw version and credits
        version = self.small_font.render("Version 0.1", True, self.GRAY)
        self.screen.blit(version, (10, self.screen.get_height() - 30))
        
        credits = self.small_font.render("© 2025 Your Game Studio", True, self.GRAY)
        self.screen.blit(credits, (self.screen.get_width() - credits.get_width() - 10, self.screen.get_height() - 30))
    
    def render_hud(self):
        """Render the heads-up display during gameplay"""
        # Player status panel (top-left)
        panel_rect = pygame.Rect(10, 10, 200, 120)
        pygame.draw.rect(self.screen, (0, 0, 0, 150), panel_rect)
        pygame.draw.rect(self.screen, self.GRAY, panel_rect, 1)
        
        # Credits
        credits_text = self.normal_font.render(f"Credits: {self.player.credits}", True, self.WHITE)
        self.screen.blit(credits_text, (20, 20))
        
        # Health bar
        health_text = self.small_font.render(f"Hull: {self.player.health}/{self.player.max_health}", True, self.WHITE)
        self.screen.blit(health_text, (20, 45))
        
        # Health bar background
        pygame.draw.rect(self.screen, self.GRAY, (100, 45, 100, 15))
        
        # Health bar fill
        health_percentage = self.player.health / self.player.max_health
        health_width = int(100 * health_percentage)
        health_color = (
            int(255 * (1 - health_percentage)),
            int(255 * health_percentage),
            0
        )
        pygame.draw.rect(self.screen, health_color, (100, 45, health_width, 15))
        
        # Shield bar
        shield_text = self.small_font.render(f"Shield: {self.player.shield}/{self.player.max_shield}", True, self.WHITE)
        self.screen.blit(shield_text, (20, 65))
        
        # Shield bar background
        pygame.draw.rect(self.screen, self.GRAY, (100, 65, 100, 15))
        
        # Shield bar fill
        shield_percentage = self.player.shield / self.player.max_shield
        shield_width = int(100 * shield_percentage)
        pygame.draw.rect(self.screen, self.BLUE, (100, 65, shield_width, 15))
        
        # Cargo space
        cargo_used = sum(self.player.cargo.values())
        cargo_text = self.small_font.render(f"Cargo: {cargo_used}/{self.player.cargo_capacity}", True, self.WHITE)
        self.screen.blit(cargo_text, (20, 85))
        
        # Cargo bar background
        pygame.draw.rect(self.screen, self.GRAY, (100, 85, 100, 15))
        
        # Cargo bar fill
        cargo_percentage = cargo_used / self.player.cargo_capacity
        cargo_width = int(100 * cargo_percentage)
        pygame.draw.rect(self.screen, self.YELLOW, (100, 85, cargo_width, 15))
        
        # System info panel (top-right)
        if self.player.current_system:
            system = self.player.current_system
            panel_rect = pygame.Rect(self.screen.get_width() - 250, 10, 240, 80)
            pygame.draw.rect(self.screen, (0, 0, 0, 150), panel_rect)
            pygame.draw.rect(self.screen, self.GRAY, panel_rect, 1)
            
            # System name
            name_text = self.normal_font.render(system.name, True, self.WHITE)
            self.screen.blit(name_text, (self.screen.get_width() - 240, 20))
            
            # System info
            info_text = self.small_font.render(f"Type: {system.system_type} | Tech: {system.tech_level}", True, self.WHITE)
            self.screen.blit(info_text, (self.screen.get_width() - 240, 45))
            
            faction_text = self.small_font.render(f"Faction: {system.faction}", True, self.WHITE)
            self.screen.blit(faction_text, (self.screen.get_width() - 240, 65))
        
        # Controls help (bottom-right)
        if self.show_help:
            help_rect = pygame.Rect(self.screen.get_width() - 250, self.screen.get_height() - 180, 240, 170)
            pygame.draw.rect(self.screen, (0, 0, 0, 200), help_rect)
            pygame.draw.rect(self.screen, self.GRAY, help_rect, 1)
            
            help_title = self.small_font.render("Controls:", True, self.YELLOW)
            self.screen.blit(help_title, (self.screen.get_width() - 240, self.screen.get_height() - 175))
            
            controls = [
                "Arrows: Steer ship",
                "Space: Fire weapon",
                "T: Trading interface",
                "U: Upgrade ship (at stations)",
                "M: Galaxy map",
                "H: Toggle help",
                "Esc: Menu"
            ]
            
            for i, control in enumerate(controls):
                text = self.small_font.render(control, True, self.WHITE)
                self.screen.blit(text, (self.screen.get_width() - 240, self.screen.get_height() - 155 + i * 20))
        else:
            # Just show help hint
            help_hint = self.small_font.render("Press H for controls", True, self.GRAY)
            self.screen.blit(help_hint, (self.screen.get_width() - help_hint.get_width() - 10, self.screen.get_height() - 30))
        
        # Notification area (bottom-center)
        if self.notification_text:
            # Calculate alpha based on remaining time
            alpha = min(255, int(255 * self.notification_timer / 3.0))
            
            # Create notification background
            notif_text = self.normal_font.render(self.notification_text, True, self.WHITE)
            notif_width = notif_text.get_width() + 20
            notif_rect = pygame.Rect(self.screen.get_width() // 2 - notif_width // 2, 
                                   self.screen.get_height() - 50, notif_width, 30)
            
            # Create a surface with alpha for the background
            bg_surface = pygame.Surface((notif_width, 30))
            bg_surface.fill((0, 0, 0))
            bg_surface.set_alpha(alpha * 0.8)
            self.screen.blit(bg_surface, (notif_rect.x, notif_rect.y))
            
            # Create a surface with alpha for the text
            text_surface = pygame.Surface(notif_text.get_size(), pygame.SRCALPHA)
            text_surface.fill((0, 0, 0, 0))
            text_surface.blit(notif_text, (0, 0))
            text_surface.set_alpha(alpha)
            
            # Draw notification
            pygame.draw.rect(self.screen, self.GRAY, notif_rect, 1)
            self.screen.blit(text_surface, (notif_rect.x + 10, notif_rect.y + 5))
        
        # Trading/Upgrade prompts if near station
        if self.player.can_trade():
            trade_text = self.normal_font.render("Press T to trade", True, self.GREEN)
            self.screen.blit(trade_text, (self.screen.get_width() // 2 - trade_text.get_width() // 2, 
                                       self.screen.get_height() - 80))
            
            upgrade_text = self.normal_font.render("Press U to upgrade ship", True, self.CYAN)
            self.screen.blit(upgrade_text, (self.screen.get_width() // 2 - upgrade_text.get_width() // 2, 
                                       self.screen.get_height() - 110))
    
    def render_minimap(self):
        """Render the minimap showing local system"""
        # Minimap panel (bottom-left)
        map_size = 150
        panel_rect = pygame.Rect(10, self.screen.get_height() - map_size - 10, map_size, map_size)
        pygame.draw.rect(self.screen, (0, 0, 0, 150), panel_rect)
        pygame.draw.rect(self.screen, self.GRAY, panel_rect, 1)
        
        # Minimap title
        map_title = self.small_font.render("Local Area", True, self.WHITE)
        self.screen.blit(map_title, (15, self.screen.get_height() - map_size - 5))
        
        # Calculate minimap center
        map_center_x = 10 + map_size // 2
        map_center_y = self.screen.get_height() - map_size // 2 - 10
        
        # Calculate minimap scale (how much area to show) - higher values = more zoomed out
        map_scale = 12.0  # Increased from 5.0 for a more zoomed out view
        
        # Draw entities on minimap
        if self.player.current_system:
            for entity in self.player.current_system.entities:
                # Calculate position relative to player
                rel_x = entity.x - self.player.x
                rel_y = entity.y - self.player.y
                
                # Scale and position on minimap
                map_x = map_center_x + rel_x / map_scale
                map_y = map_center_y + rel_y / map_scale
                
                # Check if within minimap bounds
                if (10 <= map_x < 10 + map_size and 
                    self.screen.get_height() - map_size - 10 <= map_y < self.screen.get_height() - 10):
                    
                    # Draw different colored dots based on entity type
                    if entity.entity_type == "Planet":
                        color = entity.color
                        size = 5
                    elif entity.entity_type == "SpaceStation":
                        color = entity.color
                        size = 4
                    elif entity.entity_type == "WarpGate":
                        color = (100, 150, 255)
                        size = 3
                    elif entity.entity_type == "Asteroid":
                        color = (150, 150, 150)
                        size = 1
                    elif entity.entity_type == "EnemyShip":
                        color = entity.color
                        size = 2
                    else:
                        color = self.WHITE
                        size = 1
                    
                    pygame.draw.circle(self.screen, color, (int(map_x), int(map_y)), size)
            
            # Draw player (always in center)
            pygame.draw.circle(self.screen, self.GREEN, (map_center_x, map_center_y), 3)
    
    def render_trading_interface(self):
        """Render the trading interface"""
        # Background overlay
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(200)
        self.screen.blit(overlay, (0, 0))
        
        # Trading panel
        panel_rect = pygame.Rect(50, 50, self.screen.get_width() - 100, self.screen.get_height() - 100)
        pygame.draw.rect(self.screen, (20, 20, 40), panel_rect)
        pygame.draw.rect(self.screen, self.GRAY, panel_rect, 2)
        
        # Trading title
        if self.player.nearest_trade_entity:
            entity_name = self.player.nearest_trade_entity.name
            entity_type = self.player.nearest_trade_entity.entity_type
            title_text = f"Trading with {entity_name} ({entity_type})"
        else:
            title_text = "Trading"
        
        title = self.header_font.render(title_text, True, self.WHITE)
        self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 70))
        
        # Player info
        credits_text = self.normal_font.render(f"Credits: {self.player.credits}", True, self.WHITE)
        self.screen.blit(credits_text, (70, 110))
        
        cargo_text = self.normal_font.render(f"Cargo Space: {self.player.get_cargo_space_remaining()} / {self.player.cargo_capacity} units", True, self.WHITE)
        self.screen.blit(cargo_text, (300, 110))
        
        # Column headers
        pygame.draw.line(self.screen, self.GRAY, (70, 145), (self.screen.get_width() - 70, 145), 1)
        
        headers = ["Commodity", "Buy Price", "Sell Price", "Available", "In Cargo", "Trend"]
        header_widths = [0.35, 0.15, 0.15, 0.15, 0.1, 0.1]  # Proportions of total width
        total_width = self.screen.get_width() - 140
        
        for i, header in enumerate(headers):
            pos_x = 70 + sum(header_widths[:i]) * total_width
            width = header_widths[i] * total_width
            
            header_text = self.small_font.render(header, True, self.YELLOW)
            self.screen.blit(header_text, (pos_x, 125))
        
        # Commodities list
        market = self.economy.get_system_market(self.player.current_system)
        
        # Create clipping rect for scrollable area
        clip_rect = pygame.Rect(50, 150, self.screen.get_width() - 100, self.screen.get_height() - 300)
        pygame.draw.rect(self.screen, (20, 20, 40), clip_rect)
        
        # Apply clipping
        original_clip = self.screen.get_clip()
        self.screen.set_clip(clip_rect)
        
        # Draw items
        for i, item in enumerate(market):
            y_pos = 150 + i * 30 - self.trading_scroll_offset
            
            # Skip if off-screen
            if y_pos < 150 - 30 or y_pos > self.screen.get_height() - 300 + 30:
                continue
            
            # Highlight selected item
            if i == self.selected_commodity:
                pygame.draw.rect(self.screen, (40, 40, 80), 
                               (70, y_pos, self.screen.get_width() - 140, 25))
            
            # Item details
            commodity = item['commodity']
            
            # Get quantity in player's cargo
            in_cargo = self.player.cargo.get(commodity.name, 0)
            
            # Get price trend
            trend = self.economy.get_price_trend(commodity.name)
            
            # Columns
            columns = [
                commodity.name,
                f"{item['buy_price']}",
                f"{item['sell_price']}",
                f"{item['quantity']}",
                f"{in_cargo}",
                trend
            ]
            
            # Draw each column
            for j, column in enumerate(columns):
                pos_x = 70 + sum(header_widths[:j]) * total_width
                width = header_widths[j] * total_width
                
                # Color based on content
                if j == 0:  # Commodity name
                    if commodity.illegal:
                        color = self.RED  # Red for illegal goods
                    else:
                        color = self.WHITE
                elif j == 1:  # Buy price
                    color = self.YELLOW
                elif j == 2:  # Sell price
                    color = self.GREEN
                elif j == 5:  # Trend
                    if trend == "↑":
                        color = self.GREEN
                    elif trend == "↓":
                        color = self.RED
                    else:
                        color = self.WHITE
                else:
                    color = self.WHITE
                
                text = self.small_font.render(column, True, color)
                self.screen.blit(text, (pos_x, y_pos + 5))
        
        # Reset clipping
        self.screen.set_clip(original_clip)
        
        # Draw buttons
        for button in self.buttons:
            if button['state'] == 'trading':
                pygame.draw.rect(self.screen, (40, 40, 80), button['rect'])
                pygame.draw.rect(self.screen, self.GRAY, button['rect'], 1)
                
                text = self.normal_font.render(button['text'], True, self.WHITE)
                text_x = button['rect'].x + (button['rect'].width - text.get_width()) // 2
                text_y = button['rect'].y + (button['rect'].height - text.get_height()) // 2
                self.screen.blit(text, (text_x, text_y))
        
        # Commodity details
        if self.show_trade_details and 0 <= self.selected_commodity < len(market):
            item = market[self.selected_commodity]
            commodity = item['commodity']
            
            details_rect = pygame.Rect(70, self.screen.get_height() - 130, self.screen.get_width() - 140, 60)
            pygame.draw.rect(self.screen, (30, 30, 50), details_rect)
            pygame.draw.rect(self.screen, self.GRAY, details_rect, 1)
            
            # Commodity information
            name_text = self.normal_font.render(commodity.name, True, self.WHITE)
            self.screen.blit(name_text, (80, self.screen.get_height() - 125))
            
            category_text = self.small_font.render(f"Category: {commodity.category}", True, self.LIGHT_GRAY)
            self.screen.blit(category_text, (80, self.screen.get_height() - 100))
            
            if commodity.illegal:
                illegal_text = self.small_font.render("ILLEGAL GOOD", True, self.RED)
                self.screen.blit(illegal_text, (300, self.screen.get_height() - 100))
    
    def render_upgrade_interface(self):
        """Render the ship upgrade interface"""
        # Background overlay
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(200)
        self.screen.blit(overlay, (0, 0))
        
        # Upgrade panel
        panel_rect = pygame.Rect(50, 50, self.screen.get_width() - 100, self.screen.get_height() - 100)
        pygame.draw.rect(self.screen, (20, 20, 40), panel_rect)
        pygame.draw.rect(self.screen, self.GRAY, panel_rect, 2)
        
        # Title
        title = self.header_font.render("Ship Upgrades", True, self.WHITE)
        self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 70))
        
        # Credits display
        credits_text = self.normal_font.render(f"Available Credits: {self.player.credits}", True, self.WHITE)
        self.screen.blit(credits_text, (70, 110))
        
        # Current ship stats
        stats_title = self.normal_font.render("Current Ship Statistics:", True, self.YELLOW)
        self.screen.blit(stats_title, (70, 150))
        
        # Engine
        engine_level = self.normal_font.render(f"Engine Level: {self.player.engine_level}", True, self.WHITE)
        self.screen.blit(engine_level, (70, 180))
        engine_stats = self.small_font.render(f"Thrust: {self.player.thrust:.1f} | Max Speed: {self.player.max_speed:.1f}", True, self.LIGHT_GRAY)
        self.screen.blit(engine_stats, (70, 205))
        
        # Weapons
        weapon_level = self.normal_font.render(f"Weapon Level: {self.player.weapon_level}", True, self.WHITE)
        self.screen.blit(weapon_level, (70, 235))
        weapon_stats = self.small_font.render(f"Damage: {self.player.weapon_damage:.1f} | Cooldown: {self.player.weapon_cooldown_max:.2f}s", True, self.LIGHT_GRAY)
        self.screen.blit(weapon_stats, (70, 260))
        
        # Shields
        shield_level = self.normal_font.render(f"Shield Level: {self.player.shield_level}", True, self.WHITE)
        self.screen.blit(shield_level, (70, 290))
        shield_stats = self.small_font.render(f"Capacity: {self.player.max_shield}", True, self.LIGHT_GRAY)
        self.screen.blit(shield_stats, (70, 315))
        
        # Cargo
        cargo_level = self.normal_font.render(f"Cargo Level: {self.player.cargo_level}", True, self.WHITE)
        self.screen.blit(cargo_level, (70, 345))
        cargo_stats = self.small_font.render(f"Capacity: {self.player.cargo_capacity} units", True, self.LIGHT_GRAY)
        self.screen.blit(cargo_stats, (70, 370))
        
        # Sensors
        sensor_level = self.normal_font.render(f"Sensor Level: {self.player.sensor_level}", True, self.WHITE)
        self.screen.blit(sensor_level, (70, 400))
        sensor_stats = self.small_font.render(f"Range: {self.player.trade_range:.1f}", True, self.LIGHT_GRAY)
        self.screen.blit(sensor_stats, (70, 425))
        
        # Upgrade costs
        upgrade_title = self.normal_font.render("Available Upgrades:", True, self.YELLOW)
        self.screen.blit(upgrade_title, (self.screen.get_width() - 400, 150))
        
        # Upgrade costs based on current level
        upgrade_costs = {
            'engine': [1000, 2500, 5000, 10000, 20000],
            'weapons': [1500, 3000, 6000, 12000, 24000],
            'shields': [2000, 4000, 8000, 16000, 32000],
            'cargo': [1000, 2000, 4000, 8000, 16000],
            'sensors': [800, 1600, 3200, 6400, 12800]
        }
        
        # Draw upgrade buttons
        y_offset = 180
        for button in self.buttons:
            if button['state'] == 'upgrade':
                # Skip close button for now
                if button['id'] == 'close_upgrade':
                    continue
                
                pygame.draw.rect(self.screen, (40, 40, 80), button['rect'])
                
                # Gray out if max level or can't afford
                upgrade_type = button['id'].split('_')[1]
                
                # Fix attribute name mismatches (plural to singular)
                attribute_name = upgrade_type
                if upgrade_type == "weapons":
                    attribute_name = "weapon"
                elif upgrade_type == "shields":
                    attribute_name = "shield"
                elif upgrade_type == "sensors":
                    attribute_name = "sensor"
                
                current_level = getattr(self.player, f"{attribute_name}_level")
                
                # Check if max level
                if current_level >= 5:  # Max level is 5
                    text = self.normal_font.render(f"{button['text']} (MAX)", True, self.GRAY)
                    pygame.draw.rect(self.screen, (60, 60, 80), button['rect'])
                else:
                    # Get cost for next level
                    cost = upgrade_costs[upgrade_type][current_level - 1]
                    
                    # Check if can afford
                    if self.player.credits >= cost:
                        text = self.normal_font.render(f"{button['text']} ({cost} cr)", True, self.WHITE)
                        pygame.draw.rect(self.screen, (60, 60, 100), button['rect'])
                    else:
                        text = self.normal_font.render(f"{button['text']} ({cost} cr)", True, self.GRAY)
                        pygame.draw.rect(self.screen, (60, 60, 80), button['rect'])
                
                pygame.draw.rect(self.screen, self.GRAY, button['rect'], 1)
                
                text_x = button['rect'].x + (button['rect'].width - text.get_width()) // 2
                text_y = button['rect'].y + (button['rect'].height - text.get_height()) // 2
                self.screen.blit(text, (text_x, text_y))
                
                y_offset += 50
        
        # Draw close button
        for button in self.buttons:
            if button['id'] == 'close_upgrade':
                pygame.draw.rect(self.screen, (60, 30, 30), button['rect'])
                pygame.draw.rect(self.screen, self.GRAY, button['rect'], 1)
                
                text = self.normal_font.render(button['text'], True, self.WHITE)
                text_x = button['rect'].x + (button['rect'].width - text.get_width()) // 2
                text_y = button['rect'].y + (button['rect'].height - text.get_height()) // 2
                self.screen.blit(text, (text_x, text_y))
                
        # Upgrade benefits explanation
        benefits_title = self.normal_font.render("Upgrade Benefits:", True, self.YELLOW)
        self.screen.blit(benefits_title, (70, 470))
        
        benefits = [
            "Engine: Increases thrust, speed, and turning rate",
            "Weapons: Increases damage and reduces firing cooldown",
            "Shields: Increases maximum shield capacity",
            "Cargo: Increases cargo capacity for trading",
            "Sensors: Increases trading and detection range"
        ]
        
        for i, benefit in enumerate(benefits):
            text = self.small_font.render(benefit, True, self.LIGHT_GRAY)
            self.screen.blit(text, (70, 500 + i * 25))
    
    def render_galaxy_map(self):
        """Render the galaxy map"""
        # Background
        self.screen.fill((5, 10, 20))
        
        # Draw grid lines
        for x in range(0, self.screen.get_width(), 50):
            pygame.draw.line(self.screen, (20, 30, 40), (x, 0), (x, self.screen.get_height()))
        
        for y in range(0, self.screen.get_height(), 50):
            pygame.draw.line(self.screen, (20, 30, 40), (0, y), (self.screen.get_width(), y))
        
        # Title
        title = self.header_font.render("Galaxy Map", True, self.WHITE)
        self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 20))
        
        # Get all explored systems
        explored_systems = [system for coords, system in self.universe.systems.items() if system.explored]
        
        # Draw the map
        self.universe.render_galaxy_map(self.screen, self.player.current_system)
        
        # Legend
        legend_rect = pygame.Rect(20, self.screen.get_height() - 200, 150, 180)
        pygame.draw.rect(self.screen, (0, 0, 0, 150), legend_rect)
        pygame.draw.rect(self.screen, self.GRAY, legend_rect, 1)
        
        legend_title = self.small_font.render("Legend", True, self.WHITE)
        self.screen.blit(legend_title, (25, self.screen.get_height() - 195))
        
        # System types
        system_types = {
            "Agricultural": (0, 200, 0),
            "Industrial": (200, 100, 0),
            "Mining": (150, 150, 150),
            "High-Tech": (0, 150, 200),
            "Tourist": (200, 0, 200),
            "Frontier": (200, 200, 0)
        }
        
        y_offset = self.screen.get_height() - 175
        for system_type, color in system_types.items():
            pygame.draw.circle(self.screen, color, (35, y_offset), 5)
            type_text = self.small_font.render(system_type, True, self.WHITE)
            self.screen.blit(type_text, (50, y_offset - 8))
            y_offset += 20
        
        # Instructions
        instructions = self.small_font.render("Click on a system for details", True, self.LIGHT_GRAY)
        self.screen.blit(instructions, (20, self.screen.get_height() - 25))
        
        # Current system highlight
        if self.player.current_system and self.player.current_system.explored:
            current_text = self.normal_font.render(f"Current System: {self.player.current_system.name}", True, self.WHITE)
            self.screen.blit(current_text, (self.screen.get_width() // 2 - current_text.get_width() // 2, 60))
        
        # Close button
        close_rect = pygame.Rect(self.screen.get_width() - 100, 20, 80, 30)
        pygame.draw.rect(self.screen, (40, 40, 80), close_rect)
        pygame.draw.rect(self.screen, self.GRAY, close_rect, 1)
        
        close_text = self.normal_font.render("Close", True, self.WHITE)
        self.screen.blit(close_text, (self.screen.get_width() - 60 - close_text.get_width() // 2, 25))
    
    def render_game_over(self):
        """Render game over screen"""
        # Background overlay
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(220)
        self.screen.blit(overlay, (0, 0))
        
        # Game over message
        game_over = self.title_font.render("GAME OVER", True, self.RED)
        self.screen.blit(game_over, (self.screen.get_width() // 2 - game_over.get_width() // 2, 
                                   self.screen.get_height() // 2 - 100))
        
        # Score display (would be calculated based on game progress)
        score = 10000  # Example score
        score_text = self.header_font.render(f"Final Score: {score}", True, self.WHITE)
        self.screen.blit(score_text, (self.screen.get_width() // 2 - score_text.get_width() // 2, 
                                   self.screen.get_height() // 2 - 40))
        
        # Restart button
        restart_rect = pygame.Rect(self.screen.get_width() // 2 - 100, self.screen.get_height() // 2 + 20, 200, 40)
        pygame.draw.rect(self.screen, (40, 40, 80), restart_rect)
        pygame.draw.rect(self.screen, self.GRAY, restart_rect, 2)
        
        restart_text = self.normal_font.render("Restart Game", True, self.WHITE)
        self.screen.blit(restart_text, (self.screen.get_width() // 2 - restart_text.get_width() // 2, 
                                      self.screen.get_height() // 2 + 30))
        
        # Quit button
        quit_rect = pygame.Rect(self.screen.get_width() // 2 - 100, self.screen.get_height() // 2 + 80, 200, 40)
        pygame.draw.rect(self.screen, (40, 40, 80), quit_rect)
        pygame.draw.rect(self.screen, self.GRAY, quit_rect, 2)
        
        quit_text = self.normal_font.render("Quit to Menu", True, self.WHITE)
        self.screen.blit(quit_text, (self.screen.get_width() // 2 - quit_text.get_width() // 2, 
                                   self.screen.get_height() // 2 + 90))
