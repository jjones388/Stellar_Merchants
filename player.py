import pygame
import math
from pygame.locals import *
from projectile import Laser

class Player:
    def __init__(self, x, y, starting_system):
        # Position
        self.x = x
        self.y = y
        self.angle = 0  # Angle in radians
        
        # Movement
        self.vx = 0
        self.vy = 0
        self.thrust = 200  # Acceleration per second
        self.max_speed = 300
        self.rotation_speed = 3  # Radians per second
        self.drag = 0.2  # Slow down over time
        
        # Ship properties
        self.size = 15  # Ship size
        self.color = (0, 255, 0)  # Green ship
        self.shape = [(-self.size, -self.size/2), (self.size, 0), (-self.size, self.size/2)]
        self.hit_radius = self.size  # Collision detection
        
        # Combat
        self.health = 100
        self.max_health = 100
        self.shield = 50
        self.max_shield = 50
        self.weapon_cooldown = 0
        self.weapon_cooldown_max = 0.3  # Seconds between shots
        self.weapon_damage = 10
        self.projectiles = []  # List of active projectiles
        
        # Economy
        self.credits = 1000
        self.cargo = {}  # Dictionary of goods and quantities
        self.cargo_capacity = 10  # Units of cargo
        
        # Navigation
        self.current_system = starting_system
        self.is_near_station = False
        self.nearest_trade_entity = None
        self.trade_range = 100  # Distance at which trading is possible
        
        # Upgrades
        self.engine_level = 1
        self.weapon_level = 1
        self.shield_level = 1
        self.cargo_level = 1
        self.sensor_level = 1
        
        # Create ship surface for better performance
        self.update_ship_surface()
    
    def update_ship_surface(self):
        """Update the ship's surface based on current properties"""
        # Create a surface for the ship
        self.ship_surface = pygame.Surface((self.size * 3, self.size * 3), pygame.SRCALPHA)
        
        # Draw triangle ship on the surface
        pygame.draw.polygon(self.ship_surface, self.color, 
                          [(self.size * 3 // 2 + pt[0], self.size * 3 // 2 + pt[1]) for pt in self.shape])
        
        # Add engine glow when thrusting (would be more sophisticated in full implementation)
        engine_points = [(-self.size - 5, 0), (-self.size, -self.size/4), (-self.size, self.size/4)]
        pygame.draw.polygon(self.ship_surface, (255, 165, 0), 
                          [(self.size * 3 // 2 + pt[0], self.size * 3 // 2 + pt[1]) for pt in engine_points])
    
    def handle_input(self):
        """Process keyboard input for the player ship"""
        keys = pygame.key.get_pressed()
        
        # Rotation
        if keys[K_LEFT]:
            self.angle -= self.rotation_speed * (1/60)  # Assuming 60 FPS
        if keys[K_RIGHT]:
            self.angle += self.rotation_speed * (1/60)
        
        # Thrust
        if keys[K_UP]:
            # Calculate thrust vector based on angle
            thrust_x = self.thrust * math.cos(self.angle) * (1/60)
            thrust_y = self.thrust * math.sin(self.angle) * (1/60)
            
            # Apply thrust
            self.vx += thrust_x
            self.vy += thrust_y
            
            # Limit speed
            speed = math.sqrt(self.vx**2 + self.vy**2)
            if speed > self.max_speed:
                self.vx = (self.vx / speed) * self.max_speed
                self.vy = (self.vy / speed) * self.max_speed
    
    def update(self, delta_time):
        """Update player state"""
        # Handle keyboard input
        self.handle_input()
        
        # Apply drag
        self.vx *= (1 - self.drag * delta_time)
        self.vy *= (1 - self.drag * delta_time)
        
        # Update position
        self.x += self.vx * delta_time
        self.y += self.vy * delta_time
        
        # No screen wrapping - view is centered on ship
        # Instead, we'll let the ship move freely in the system
        
        # Update weapon cooldown
        if self.weapon_cooldown > 0:
            self.weapon_cooldown -= delta_time
        
        # Update projectiles
        for projectile in self.projectiles[:]:
            projectile.update(delta_time)
            # Remove projectiles that have expired
            if projectile.lifetime <= 0:
                self.projectiles.remove(projectile)
        
        # Check distance to trade entities
        self.update_trade_status()
    
    def render(self, screen):
        """Render the player ship"""
        # Get screen dimensions
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        
        # Position the ship at the center of the screen
        screen_center_x = screen_width // 2
        screen_center_y = screen_height // 2
        
        # Create a rotated copy of the ship surface
        angle_degrees = math.degrees(self.angle)
        rotated_ship = pygame.transform.rotate(self.ship_surface, -angle_degrees)
        
        # Get the rect for positioning
        ship_rect = rotated_ship.get_rect(center=(screen_center_x, screen_center_y))
        
        # Draw the ship
        screen.blit(rotated_ship, ship_rect)
        
        # Draw engine glow when thrusting (would be more sophisticated)
        keys = pygame.key.get_pressed()
        if keys[K_UP]:
            # Calculate engine position
            engine_x = screen_center_x - math.cos(self.angle) * self.size
            engine_y = screen_center_y - math.sin(self.angle) * self.size
            
            # Draw engine glow
            pygame.draw.circle(screen, (255, 165, 0), (int(engine_x), int(engine_y)), 5)
        
        # Render all projectiles
        for projectile in self.projectiles:
            # Calculate projectile position relative to player
            screen_x = screen_center_x + (projectile.x - self.x)
            screen_y = screen_center_y + (projectile.y - self.y)
            
            # We need to modify the projectile's render method to accept custom coordinates
            projectile.render_at(screen, screen_x, screen_y)
        
        # Debug: draw hit radius
        # pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)), self.hit_radius, 1)
    
    def fire_weapon(self):
        """Fire the ship's weapon if cooldown allows"""
        if self.weapon_cooldown <= 0:
            # Reset cooldown
            self.weapon_cooldown = self.weapon_cooldown_max
            
            # Calculate projectile spawn position (front of ship)
            spawn_x = self.x + math.cos(self.angle) * self.size
            spawn_y = self.y + math.sin(self.angle) * self.size
            
            # Create new projectile
            new_laser = Laser(spawn_x, spawn_y, self.angle, self.weapon_damage)
            self.projectiles.append(new_laser)
            
            # Play sound (would be implemented in full game)
            # self.laser_sound.play()
            
            return True
        return False
    
    def take_damage(self, amount):
        """Apply damage to shields first, then hull"""
        if self.shield > 0:
            # Shield absorbs damage
            if self.shield >= amount:
                self.shield -= amount
                amount = 0
            else:
                # Shield is depleted, remaining damage goes to hull
                amount -= self.shield
                self.shield = 0
        
        # Apply remaining damage to hull
        if amount > 0:
            self.health -= amount
            
            # Check if destroyed
            if self.health <= 0:
                self.health = 0
                return True  # Ship destroyed
        
        return False  # Ship still alive
    
    def heal(self, amount):
        """Repair the ship's hull"""
        self.health = min(self.max_health, self.health + amount)
    
    def recharge_shield(self, amount):
        """Recharge the ship's shield"""
        self.shield = min(self.max_shield, self.shield + amount)
    
    def add_cargo(self, item, quantity):
        """Add items to cargo hold if there's space"""
        # Calculate current cargo usage
        current_cargo = sum(self.cargo.values())
        
        if current_cargo + quantity <= self.cargo_capacity:
            # There's enough space
            if item in self.cargo:
                self.cargo[item] += quantity
            else:
                self.cargo[item] = quantity
            return True
        return False  # Not enough space
    
    def remove_cargo(self, item, quantity):
        """Remove items from cargo"""
        if item in self.cargo and self.cargo[item] >= quantity:
            self.cargo[item] -= quantity
            
            # Remove item completely if quantity is 0
            if self.cargo[item] == 0:
                del self.cargo[item]
            
            return True
        return False  # Not enough of this item
    
    def get_cargo_space_remaining(self):
        """Calculate remaining cargo space"""
        current_cargo = sum(self.cargo.values())
        return self.cargo_capacity - current_cargo
    
    def upgrade_engine(self):
        """Upgrade the ship's engine"""
        self.engine_level += 1
        self.thrust *= 1.2
        self.max_speed *= 1.1
        self.rotation_speed *= 1.1
    
    def upgrade_weapon(self):
        """Upgrade the ship's weapons"""
        self.weapon_level += 1
        self.weapon_damage *= 1.2
        self.weapon_cooldown_max *= 0.9  # Faster fire rate
    
    def upgrade_shield(self):
        """Upgrade the ship's shields"""
        self.shield_level += 1
        self.max_shield *= 1.3
        self.shield = self.max_shield  # Refill shield with upgrade
    
    def upgrade_cargo(self):
        """Upgrade the ship's cargo capacity"""
        self.cargo_level += 1
        self.cargo_capacity += 5  # Add 5 units per upgrade
    
    def upgrade_sensors(self):
        """Upgrade the ship's sensors"""
        self.sensor_level += 1
        self.trade_range *= 1.2
    
    def update_trade_status(self):
        """Check if player is near a planet or station for trading"""
        self.is_near_station = False
        self.nearest_trade_entity = None
        
        # Check distance to all trade entities in current system
        for entity in self.current_system.entities:
            if hasattr(entity, 'can_trade') and entity.can_trade:
                distance = math.sqrt((self.x - entity.x)**2 + (self.y - entity.y)**2)
                if distance <= self.trade_range:
                    self.is_near_station = True
                    self.nearest_trade_entity = entity
                    break
    
    def can_trade(self):
        """Check if player can trade now"""
        return self.is_near_station
