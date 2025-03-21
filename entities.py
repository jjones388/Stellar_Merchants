import pygame
import math
import random

class Entity:
    """Base class for all game entities"""
    def __init__(self, x, y, size, entity_type):
        self.x = x
        self.y = y
        self.size = size
        self.entity_type = entity_type
        self.rotation = 0  # In radians
        self.rotation_speed = 0  # Rotation speed in radians per second
    
    def update(self, delta_time, player=None):
        """Update entity state"""
        # Rotate the entity
        self.rotation += self.rotation_speed * delta_time
        
        # Keep rotation within 0 to 2π
        self.rotation %= 2 * math.pi
    
    def render(self, screen, player_x, player_y):
        """Render the entity relative to player position"""
        # Calculate screen position relative to player
        screen_x = screen.get_width() // 2 + (self.x - player_x)
        screen_y = screen.get_height() // 2 + (self.y - player_y)
        
        # Check if entity is on screen (with some margin)
        if -100 <= screen_x <= screen.get_width() + 100 and -100 <= screen_y <= screen.get_height() + 100:
            # Draw a simple circle for now
            pygame.draw.circle(screen, (200, 200, 200), (int(screen_x), int(screen_y)), self.size)
    
    def check_collision(self, other):
        """Check if this entity collides with another entity"""
        distance = math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
        return distance < self.size + other.hit_radius

class Planet(Entity):
    """A planet that can be traded with"""
    def __init__(self, x, y, size, planet_type, name, tech_level):
        super().__init__(x, y, size, "Planet")
        self.planet_type = planet_type
        self.name = name
        self.tech_level = tech_level
        self.rotation_speed = random.uniform(0.05, 0.2)  # Slow rotation
        
        # Generate planet color based on type
        if planet_type == "Terrestrial":
            self.color = (0, 128, 0)  # Green
        elif planet_type == "Gas Giant":
            self.color = (200, 150, 50)  # Orange-ish
        elif planet_type == "Ice World":
            self.color = (200, 200, 255)  # Light blue
        elif planet_type == "Desert":
            self.color = (210, 180, 140)  # Tan
        elif planet_type == "Jungle":
            self.color = (0, 100, 0)  # Dark green
        elif planet_type == "Ocean":
            self.color = (0, 0, 150)  # Dark blue
        else:
            self.color = (150, 150, 150)  # Gray default
        
        # Trading properties
        self.can_trade = True
        
        # Create surface for better performance
        self.surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.surface, self.color, (size, size), size)
        
        # Add some details based on planet type
        if planet_type == "Terrestrial" or planet_type == "Jungle":
            # Add landmasses
            for _ in range(5):
                land_x = random.randint(size//3, size*5//3)
                land_y = random.randint(size//3, size*5//3)
                land_size = random.randint(size//5, size//2)
                land_color = (0, random.randint(90, 160), 0)
                pygame.draw.circle(self.surface, land_color, (land_x, land_y), land_size)
        
        elif planet_type == "Gas Giant":
            # Add bands
            for i in range(3):
                band_y = size // 2 + (i - 1) * size // 3
                band_height = size // 5
                band_color = (random.randint(180, 220), random.randint(130, 170), random.randint(30, 70))
                pygame.draw.rect(self.surface, band_color, (0, band_y, size * 2, band_height))
        
        elif planet_type == "Ice World":
            # Add ice caps
            cap_color = (255, 255, 255)
            pygame.draw.circle(self.surface, cap_color, (size, size//3), size//2)
            pygame.draw.circle(self.surface, cap_color, (size, size*5//3), size//2)
        
        elif planet_type == "Desert":
            # Add craters
            for _ in range(3):
                crater_x = random.randint(size//3, size*5//3)
                crater_y = random.randint(size//3, size*5//3)
                crater_size = random.randint(size//6, size//3)
                crater_color = (180, 150, 120)
                pygame.draw.circle(self.surface, crater_color, (crater_x, crater_y), crater_size)
        
        elif planet_type == "Ocean":
            # Add small islands
            for _ in range(3):
                island_x = random.randint(size//3, size*5//3)
                island_y = random.randint(size//3, size*5//3)
                island_size = random.randint(size//8, size//4)
                island_color = (0, 150, 0)
                pygame.draw.circle(self.surface, island_color, (island_x, island_y), island_size)
    
    def render(self, screen, player_x, player_y):
        """Render the planet"""
        # Calculate screen position relative to player
        screen_x = screen.get_width() // 2 + (self.x - player_x)
        screen_y = screen.get_height() // 2 + (self.y - player_y)
        
        # Check if planet is on screen (with some margin)
        if -100 <= screen_x <= screen.get_width() + 100 and -100 <= screen_y <= screen.get_height() + 100:
            # Get the rect for positioning
            planet_rect = self.surface.get_rect(center=(screen_x, screen_y))
            
            # Draw the planet
            screen.blit(self.surface, planet_rect)
            
            # Draw name above planet
            font = pygame.font.SysFont(None, 20)
            name_text = font.render(f"{self.name} ({self.planet_type})", True, (200, 200, 255))
            screen.blit(name_text, (screen_x - name_text.get_width() // 2, screen_y - self.size - 25))

class SpaceStation(Entity):
    """A space station that can be traded with"""
    def __init__(self, x, y, size, station_type, name, tech_level):
        super().__init__(x, y, size, "SpaceStation")
        self.station_type = station_type
        self.name = name
        self.tech_level = tech_level
        self.rotation_speed = random.uniform(0.1, 0.3)  # Rotate slowly
        
        # Trading properties
        self.can_trade = True
        
        # Generate station appearance based on type
        if station_type == "Trading Post":
            self.color = (0, 150, 150)  # Teal
        elif station_type == "Military Base":
            self.color = (150, 0, 0)  # Red
        elif station_type == "Research Facility":
            self.color = (150, 0, 150)  # Purple
        elif station_type == "Mining Outpost":
            self.color = (150, 150, 0)  # Yellow
        else:
            self.color = (150, 150, 150)  # Gray default
        
        # Create surface for better performance
        self.surface = pygame.Surface((size * 3, size * 3), pygame.SRCALPHA)
        
        # Draw station - varies by type
        if station_type == "Trading Post":
            # Central hub with extending arms
            pygame.draw.circle(self.surface, self.color, (size * 3 // 2, size * 3 // 2), size // 2)
            
            # Draw extending arms
            arm_width = size // 3
            for i in range(4):
                angle = i * math.pi / 2
                arm_x = size * 3 // 2 + math.cos(angle) * size
                arm_y = size * 3 // 2 + math.sin(angle) * size
                
                pygame.draw.line(self.surface, self.color, 
                               (size * 3 // 2, size * 3 // 2),
                               (int(arm_x), int(arm_y)), arm_width)
                
                # Add a "pod" at the end of each arm
                pygame.draw.circle(self.surface, self.color, (int(arm_x), int(arm_y)), size // 3)
        
        elif station_type == "Military Base":
            # Central structure with defensive emplacements
            pygame.draw.rect(self.surface, self.color, 
                           (size * 3 // 2 - size // 2, size * 3 // 2 - size // 2, 
                            size, size))
            
            # Add defensive turrets
            for i in range(4):
                angle = i * math.pi / 2 + math.pi / 4
                turret_x = size * 3 // 2 + math.cos(angle) * size * 0.8
                turret_y = size * 3 // 2 + math.sin(angle) * size * 0.8
                
                pygame.draw.circle(self.surface, (200, 50, 50), 
                                 (int(turret_x), int(turret_y)), size // 5)
        
        elif station_type == "Research Facility":
            # Ring structure with central lab
            pygame.draw.circle(self.surface, self.color, (size * 3 // 2, size * 3 // 2), size, 4)
            pygame.draw.circle(self.surface, self.color, (size * 3 // 2, size * 3 // 2), size // 3)
            
            # Add sensor dishes
            for i in range(3):
                angle = i * 2 * math.pi / 3
                sensor_x = size * 3 // 2 + math.cos(angle) * size
                sensor_y = size * 3 // 2 + math.sin(angle) * size
                
                pygame.draw.circle(self.surface, (200, 100, 200), 
                                 (int(sensor_x), int(sensor_y)), size // 4)
        
        elif station_type == "Mining Outpost":
            # Asymmetric structure with mining arms
            pygame.draw.rect(self.surface, self.color, 
                           (size * 3 // 2 - size // 3, size * 3 // 2 - size // 3, 
                            size * 2 // 3, size * 2 // 3))
            
            # Add mining arms
            for i in range(2):
                angle = i * math.pi
                arm_length = size * 1.2
                arm_x = size * 3 // 2 + math.cos(angle) * arm_length
                arm_y = size * 3 // 2 + math.sin(angle) * arm_length
                
                pygame.draw.line(self.surface, self.color, 
                               (size * 3 // 2, size * 3 // 2),
                               (int(arm_x), int(arm_y)), size // 4)
                
                # Add drill
                pygame.draw.polygon(self.surface, (100, 100, 50), 
                                  [(int(arm_x), int(arm_y)),
                                   (int(arm_x + size//4), int(arm_y + size//4)),
                                   (int(arm_x - size//4), int(arm_y + size//4))])
    
    def render(self, screen, player_x, player_y):
        """Render the space station"""
        # Calculate screen position relative to player
        screen_x = screen.get_width() // 2 + (self.x - player_x)
        screen_y = screen.get_height() // 2 + (self.y - player_y)
        
        # Check if station is on screen (with some margin)
        if -100 <= screen_x <= screen.get_width() + 100 and -100 <= screen_y <= screen.get_height() + 100:
            # Create a rotated copy of the station surface
            angle_degrees = math.degrees(self.rotation)
            rotated_station = pygame.transform.rotate(self.surface, -angle_degrees)
            
            # Get the rect for positioning
            station_rect = rotated_station.get_rect(center=(screen_x, screen_y))
            
            # Draw the station
            screen.blit(rotated_station, station_rect)
            
            # Draw name above station
            font = pygame.font.SysFont(None, 20)
            name_text = font.render(f"{self.name} ({self.station_type})", True, (200, 200, 255))
            screen.blit(name_text, (screen_x - name_text.get_width() // 2, screen_y - self.size - 25))

class WarpGate(Entity):
    """A warp gate that connects star systems"""
    def __init__(self, x, y, direction, destination):
        super().__init__(x, y, 30, "WarpGate")
        self.direction = direction  # N, E, S, W
        self.destination = destination  # Target StarSystem
        self.active = True
        self.pulse_time = 0
        self.pulse_max = 2.0  # Seconds per pulse
        
        # Set rotation based on direction
        if direction == "North":
            self.rotation = 0
        elif direction == "East":
            self.rotation = math.pi / 2
        elif direction == "South":
            self.rotation = math.pi
        elif direction == "West":
            self.rotation = 3 * math.pi / 2
        
        # Create surface for better performance
        self.surface = pygame.Surface((100, 100), pygame.SRCALPHA)
        
        # Draw gate structure
        pygame.draw.circle(self.surface, (50, 100, 200), (50, 50), 30, 5)
        
        # Add some details
        # Struts
        for i in range(4):
            angle = i * math.pi / 2
            x1 = 50 + math.cos(angle) * 15
            y1 = 50 + math.sin(angle) * 15
            x2 = 50 + math.cos(angle) * 30
            y2 = 50 + math.sin(angle) * 30
            
            pygame.draw.line(self.surface, (100, 150, 200), (x1, y1), (x2, y2), 3)
        
        # Energy core
        pygame.draw.circle(self.surface, (150, 200, 255), (50, 50), 15)
    
    def update(self, delta_time, player=None):
        """Update gate state"""
        super().update(delta_time)
        
        # Update pulse time
        self.pulse_time += delta_time
        if self.pulse_time > self.pulse_max:
            self.pulse_time = 0
    
    def render(self, screen, player_x, player_y):
        """Render the warp gate"""
        # Calculate screen position relative to player
        screen_x = screen.get_width() // 2 + (self.x - player_x)
        screen_y = screen.get_height() // 2 + (self.y - player_y)
        
        # Check if gate is on screen (with some margin)
        if -100 <= screen_x <= screen.get_width() + 100 and -100 <= screen_y <= screen.get_height() + 100:
            # Create a copy of the gate surface with pulsing effect
            gate_surface = self.surface.copy()
            
            # Calculate pulse effect (energy core pulsates)
            pulse_factor = abs(math.sin(self.pulse_time * math.pi / self.pulse_max))
            pulse_color = (
                int(100 + 155 * pulse_factor),
                int(150 + 105 * pulse_factor),
                255
            )
            
            # Draw pulsing energy core
            pygame.draw.circle(gate_surface, pulse_color, (50, 50), 15)
            
            # Get the rect for positioning
            gate_rect = gate_surface.get_rect(center=(screen_x, screen_y))
            
            # Draw the gate
            screen.blit(gate_surface, gate_rect)
            
            # Draw direction text
            font = pygame.font.SysFont(None, 20)
            text = font.render(f"{self.direction} Gate", True, (200, 200, 255))
            screen.blit(text, (screen_x - text.get_width() // 2, screen_y - self.size - 15))
            
            # If destination is known, show it
            if self.destination:
                dest_text = font.render(f"To: {self.destination.name}", True, (200, 200, 255))
                screen.blit(dest_text, (screen_x - dest_text.get_width() // 2, screen_y - self.size - 35))
    
    def check_collision(self, player):
        """Check if player has entered the gate"""
        distance = math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2)
        return distance < 20  # Smaller than visual size to require deliberate entry

class Asteroid(Entity):
    """An asteroid that can be mined or is an obstacle"""
    def __init__(self, x, y, size, rotation, asteroid_type):
        super().__init__(x, y, size, "Asteroid")
        self.rotation = rotation
        self.rotation_speed = random.uniform(-0.5, 0.5)
        self.vx = random.uniform(-5, 5)
        self.vy = random.uniform(-5, 5)
        self.asteroid_type = asteroid_type
        
        # Determine color based on type
        if asteroid_type == "Iron":
            self.color = (150, 100, 50)
        elif asteroid_type == "Ice":
            self.color = (200, 200, 255)
        elif asteroid_type == "Carbon":
            self.color = (50, 50, 50)
        elif asteroid_type == "Precious":
            self.color = (212, 175, 55)  # Gold-ish
        else:
            self.color = (150, 150, 150)
        
        # Create asteroid shape (irregular polygon)
        self.points = []
        num_points = random.randint(6, 10)
        for i in range(num_points):
            angle = i * 2 * math.pi / num_points
            # Random distance from center
            dist = size * random.uniform(0.7, 1.3)
            x = math.cos(angle) * dist
            y = math.sin(angle) * dist
            self.points.append((x, y))
        
        # Create surface
        self.surface = pygame.Surface((size * 3, size * 3), pygame.SRCALPHA)
        
        # Convert points to surface coordinates
        surface_points = [(size * 3 // 2 + pt[0], size * 3 // 2 + pt[1]) for pt in self.points]
        
        # Draw asteroid
        pygame.draw.polygon(self.surface, self.color, surface_points)
        
        # Add some craters or details
        for _ in range(random.randint(2, 5)):
            crater_x = random.randint(size * 3 // 4, size * 9 // 4)
            crater_y = random.randint(size * 3 // 4, size * 9 // 4)
            crater_size = random.randint(size // 6, size // 3)
            
            # Slightly darker color for craters
            crater_color = (
                max(0, self.color[0] - 30),
                max(0, self.color[1] - 30),
                max(0, self.color[2] - 30)
            )
            
            pygame.draw.circle(self.surface, crater_color, (crater_x, crater_y), crater_size)
    
    def update(self, delta_time, player=None):
        """Update asteroid state"""
        super().update(delta_time)
        
        # Move asteroid
        self.x += self.vx * delta_time
        self.y += self.vy * delta_time
        
        # Wrap around edges of system (crude method, would use better in full implementation)
        if self.x < -500:
            self.x = 1500
        elif self.x > 1500:
            self.x = -500
            
        if self.y < -500:
            self.y = 1500
        elif self.y > 1500:
            self.y = -500
    
    def render(self, screen, player_x, player_y):
        """Render the asteroid"""
        # Calculate screen position relative to player
        screen_x = screen.get_width() // 2 + (self.x - player_x)
        screen_y = screen.get_height() // 2 + (self.y - player_y)
        
        # Check if asteroid is on screen (with some margin)
        if -100 <= screen_x <= screen.get_width() + 100 and -100 <= screen_y <= screen.get_height() + 100:
            # Create a rotated copy of the asteroid surface
            angle_degrees = math.degrees(self.rotation)
            rotated_asteroid = pygame.transform.rotate(self.surface, -angle_degrees)
            
            # Get the rect for positioning
            asteroid_rect = rotated_asteroid.get_rect(center=(screen_x, screen_y))
            
            # Draw the asteroid
            screen.blit(rotated_asteroid, asteroid_rect)

class EnemyShip(Entity):
    """An enemy ship that can attack or trade with the player"""
    def __init__(self, x, y, ship_type, level):
        size = 10 + level * 2  # Bigger ships for higher levels
        super().__init__(x, y, size, "EnemyShip")
        self.ship_type = ship_type
        self.level = level
        
        # Movement properties
        self.vx = 0
        self.vy = 0
        self.max_speed = 50 + level * 10
        self.thrust = 30 + level * 5
        
        # Combat properties
        self.health = 20 + level * 10
        self.max_health = self.health
        self.damage = 5 + level * 2
        self.fire_rate = 1 + level * 0.2  # Shots per second
        self.fire_timer = 0
        self.aggression = 0  # 0: neutral, negative: friendly, positive: hostile
        
        # AI properties
        self.state = "PATROL"  # PATROL, CHASE, ATTACK, FLEE
        self.target_x = x
        self.target_y = y
        self.waypoint_timer = 0
        self.detection_range = 200 + level * 20
        
        # Visual appearance based on type
        if ship_type == "Pirate":
            self.color = (200, 0, 0)  # Red for pirates
            self.aggression = random.randint(5, 10)  # Very aggressive
        elif ship_type == "Trader":
            self.color = (0, 200, 0)  # Green for traders
            self.aggression = random.randint(-5, 0)  # Non-aggressive unless provoked
        elif ship_type == "Police":
            self.color = (0, 0, 200)  # Blue for police
            self.aggression = 0  # Neutral unless player is wanted
        elif ship_type == "Military":
            self.color = (200, 200, 0)  # Yellow for military
            self.aggression = random.randint(0, 5)  # Somewhat aggressive
        else:
            self.color = (150, 150, 150)
            self.aggression = 0
        
        # Create ship surface
        self.create_ship_surface()
    
    def create_ship_surface(self):
        """Create the ship's visual appearance"""
        self.surface = pygame.Surface((self.size * 3, self.size * 3), pygame.SRCALPHA)
        
        # Ship shape varies by type
        if self.ship_type == "Pirate":
            # Sleek, asymmetric design
            points = [
                (self.size * 3 // 2, self.size * 3 // 2 - self.size),  # Front
                (self.size * 3 // 2 + self.size * 0.7, self.size * 3 // 2 + self.size * 0.5),  # Right
                (self.size * 3 // 2, self.size * 3 // 2 + self.size * 0.3),  # Back middle
                (self.size * 3 // 2 - self.size * 0.7, self.size * 3 // 2 + self.size * 0.5)   # Left
            ]
            pygame.draw.polygon(self.surface, self.color, points)
            
            # Add details (engine glow, etc)
            pygame.draw.circle(self.surface, (255, 150, 0), 
                             (self.size * 3 // 2, self.size * 3 // 2 + self.size * 0.3), self.size // 3)
        
        elif self.ship_type == "Trader":
            # Bulky, symmetric design
            pygame.draw.rect(self.surface, self.color, 
                           (self.size * 3 // 2 - self.size * 0.5, self.size * 3 // 2 - self.size * 0.8, 
                            self.size, self.size * 1.6))
            
            # Cargo containers on sides
            pygame.draw.rect(self.surface, (self.color[0], self.color[1], max(0, self.color[2] - 50)), 
                           (self.size * 3 // 2 - self.size * 1.2, self.size * 3 // 2 - self.size * 0.5, 
                            self.size * 0.6, self.size))
            pygame.draw.rect(self.surface, (self.color[0], self.color[1], max(0, self.color[2] - 50)), 
                           (self.size * 3 // 2 + self.size * 0.6, self.size * 3 // 2 - self.size * 0.5, 
                            self.size * 0.6, self.size))
            
            # Engine
            pygame.draw.rect(self.surface, (100, 100, 150), 
                           (self.size * 3 // 2 - self.size * 0.3, self.size * 3 // 2 + self.size * 0.8, 
                            self.size * 0.6, self.size * 0.3))
        
        elif self.ship_type == "Police" or self.ship_type == "Military":
            # Angular, symmetric design
            points = [
                (self.size * 3 // 2, self.size * 3 // 2 - self.size),  # Front
                (self.size * 3 // 2 + self.size, self.size * 3 // 2),  # Right
                (self.size * 3 // 2 + self.size * 0.5, self.size * 3 // 2 + self.size),  # Right back
                (self.size * 3 // 2 - self.size * 0.5, self.size * 3 // 2 + self.size),  # Left back
                (self.size * 3 // 2 - self.size, self.size * 3 // 2)   # Left
            ]
            pygame.draw.polygon(self.surface, self.color, points)
            
            # Add details
            if self.ship_type == "Police":
                # Police lights
                pygame.draw.circle(self.surface, (255, 0, 0), 
                                 (self.size * 3 // 2 - self.size * 0.3, self.size * 3 // 2 - self.size * 0.3), 
                                 self.size * 0.2)
                pygame.draw.circle(self.surface, (0, 0, 255), 
                                 (self.size * 3 // 2 + self.size * 0.3, self.size * 3 // 2 - self.size * 0.3), 
                                 self.size * 0.2)
            else:  # Military
                # Weapon hardpoints
                pygame.draw.rect(self.surface, (100, 100, 100), 
                               (int(self.size * 3 // 2 - self.size * 0.7), int(self.size * 3 // 2 - self.size * 0.3), 
                                int(self.size * 0.3), int(self.size * 0.6)))
                pygame.draw.rect(self.surface, (100, 100, 100), 
                               (int(self.size * 3 // 2 + self.size * 0.4), int(self.size * 3 // 2 - self.size * 0.3), 
                                int(self.size * 0.3), int(self.size * 0.6)))
    
    def update(self, delta_time, player=None):
        """Update enemy ship state"""
        super().update(delta_time)
        
        # AI behavior
        if player:
            # Check if player is within detection range
            distance_to_player = math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2)
            
            if distance_to_player < self.detection_range:
                # Check aggression to determine behavior
                if self.aggression > 5:  # Hostile
                    self.state = "ATTACK"
                    self.target_x = player.x
                    self.target_y = player.y
                elif self.aggression < -5:  # Friendly
                    # Could help player if implemented
                    self.state = "PATROL"
                else:  # Neutral
                    # Just continue current behavior
                    pass
            
            # If in attack state, update target position to player position
            if self.state == "ATTACK":
                self.target_x = player.x
                self.target_y = player.y
                
                # If close enough, fire at player
                if distance_to_player < 150:
                    self.fire_timer += delta_time
                    if self.fire_timer >= 1.0 / self.fire_rate:
                        self.fire_timer = 0
                        # Would fire a projectile here in full implementation
        
        # Patrol behavior
        if self.state == "PATROL":
            self.waypoint_timer += delta_time
            if self.waypoint_timer >= 5:  # New waypoint every 5 seconds
                self.waypoint_timer = 0
                # Pick a new random waypoint
                self.target_x = self.x + random.uniform(-200, 200)
                self.target_y = self.y + random.uniform(-200, 200)
        
        # Move toward target
        angle_to_target = math.atan2(self.target_y - self.y, self.target_x - self.x)
        
        # Gradually rotate toward target angle
        angle_diff = ((angle_to_target - self.rotation + math.pi) % (2 * math.pi)) - math.pi
        self.rotation += angle_diff * 2 * delta_time  # Adjust rotation speed as needed
        
        # Apply thrust in current direction
        thrust_factor = min(1.0, distance_to_player / 100) if self.state == "ATTACK" else 1.0
        self.vx += math.cos(self.rotation) * self.thrust * thrust_factor * delta_time
        self.vy += math.sin(self.rotation) * self.thrust * thrust_factor * delta_time
        
        # Apply drag (more when close to target to avoid overshooting)
        distance_to_target = math.sqrt((self.x - self.target_x)**2 + (self.y - self.target_y)**2)
        drag_factor = 0.1 + 0.9 * max(0, 1 - distance_to_target / 100)
        self.vx *= (1 - drag_factor * delta_time)
        self.vy *= (1 - drag_factor * delta_time)
        
        # Apply movement
        self.x += self.vx * delta_time
        self.y += self.vy * delta_time
    
    def render(self, screen, player_x, player_y):
        """Render the enemy ship"""
        # Calculate screen position relative to player
        screen_x = screen.get_width() // 2 + (self.x - player_x)
        screen_y = screen.get_height() // 2 + (self.y - player_y)
        
        # Check if ship is on screen (with some margin)
        if -100 <= screen_x <= screen.get_width() + 100 and -100 <= screen_y <= screen.get_height() + 100:
            # Create a rotated copy of the ship surface
            angle_degrees = math.degrees(self.rotation)
            rotated_ship = pygame.transform.rotate(self.surface, -angle_degrees)
            
            # Get the rect for positioning
            ship_rect = rotated_ship.get_rect(center=(screen_x, screen_y))
            
            # Draw the ship
            screen.blit(rotated_ship, ship_rect)
            
            # Draw engine glow if moving
            if abs(self.vx) > 5 or abs(self.vy) > 5:
                # Calculate engine position
                engine_x = screen_x - math.cos(self.rotation) * self.size
                engine_y = screen_y - math.sin(self.rotation) * self.size
                
                # Draw engine glow
                pygame.draw.circle(screen, (255, 165, 0), 
                                 (int(engine_x), int(engine_y)), self.size // 3)
            
            # Draw health bar if damaged
            if self.health < self.max_health:
                bar_width = self.size * 2
                health_percentage = self.health / self.max_health
                
                # Background bar (red)
                pygame.draw.rect(screen, (200, 0, 0), 
                               (screen_x - bar_width // 2, screen_y - self.size - 10, 
                                bar_width, 5))
                
                # Health bar (green)
                pygame.draw.rect(screen, (0, 200, 0), 
                               (screen_x - bar_width // 2, screen_y - self.size - 10, 
                                int(bar_width * health_percentage), 5))
