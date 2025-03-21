import pygame
import random
import math
import names
from entities import Planet, SpaceStation, WarpGate, Asteroid, EnemyShip

# Constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SYSTEM_TYPES = ["Agricultural", "Industrial", "Mining", "High-Tech", "Tourist", "Frontier"]
FACTION_TYPES = ["Federation", "Empire", "Independent", "Rebel", "Corporate"]

class StarSystem:
    def __init__(self, x, y, grid_x, grid_y, universe):
        # Grid position in galaxy
        self.grid_x = grid_x
        self.grid_y = grid_y
        
        # Center position of the system (for rendering on galaxy map)
        self.map_x = x
        self.map_y = y
        
        # System properties
        self.name = self.generate_name()
        self.system_type = random.choice(SYSTEM_TYPES)
        self.faction = random.choice(FACTION_TYPES)
        self.tech_level = random.randint(1, 10)
        self.danger_level = random.randint(1, 10)
        self.explored = False  # Start as unexplored
        
        # Reference to parent universe
        self.universe = universe
        
        # Entities in this system
        self.entities = []
        self.warp_gates = []
        
        # The main celestial body (planet or station)
        self.main_entity = None
        
        # Generate system contents
        self.generate_system()
    
    def generate_name(self):
        """Generate a random star system name"""
        prefixes = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Eta", "Theta", 
                   "Iota", "Kappa", "Lambda", "Mu", "Nu", "Xi", "Omicron", "Pi", "Rho", 
                   "Sigma", "Tau", "Upsilon", "Phi", "Chi", "Psi", "Omega"]
        
        suffixes = ["Prime", "Major", "Minor", "Secundus", "Tertius", "Quartus", "Quintus",
                   "A", "B", "C", "I", "II", "III", "IV", "V"]
        
        # Generate a name
        name = f"{random.choice(prefixes)} {names.get_last_name()}"
        
        # 50% chance to add a suffix
        if random.random() < 0.5:
            name += f" {random.choice(suffixes)}"
            
        return name
    
    def generate_system(self):
        """Generate the contents of this star system"""
        # Create central entity (planet or station)
        if random.random() < 0.7:  # 70% chance for a planet
            planet_type = random.choice(["Terrestrial", "Gas Giant", "Ice World", "Desert", "Jungle", "Ocean"])
            
            # Create planet at center of screen
            self.main_entity = Planet(
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2,
                random.randint(40, 80),  # Size
                planet_type,
                self.name,
                self.tech_level
            )
        else:  # 30% chance for a space station
            station_type = random.choice(["Trading Post", "Military Base", "Research Facility", "Mining Outpost"])
            
            self.main_entity = SpaceStation(
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2,
                random.randint(30, 60),  # Size
                station_type,
                self.name,
                self.tech_level
            )
        
        # Add main entity to the system
        self.entities.append(self.main_entity)
        
        # Create warp gates at cardinal directions (N,E,S,W) only if we have a neighboring system
        gate_distance = 1200  # Distance from center to warp gates
        
        # Only create gates where there will be connections to other systems
        # North gate (only if not at top edge)
        if self.grid_y > 0:
            north_gate = WarpGate(
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 - gate_distance,
                "North",
                None  # Will set the destination later once all systems are created
            )
            self.warp_gates.append(north_gate)
            self.entities.append(north_gate)
        
        # East gate (only if not at right edge)
        if self.grid_x < self.universe.width - 1:
            east_gate = WarpGate(
                SCREEN_WIDTH // 2 + gate_distance,
                SCREEN_HEIGHT // 2,
                "East",
                None
            )
            self.warp_gates.append(east_gate)
            self.entities.append(east_gate)
        
        # South gate (only if not at bottom edge)
        if self.grid_y < self.universe.height - 1:
            south_gate = WarpGate(
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 + gate_distance,
                "South",
                None
            )
            self.warp_gates.append(south_gate)
            self.entities.append(south_gate)
        
        # West gate (only if not at left edge)
        if self.grid_x > 0:
            west_gate = WarpGate(
                SCREEN_WIDTH // 2 - gate_distance,
                SCREEN_HEIGHT // 2,
                "West",
                None
            )
            self.warp_gates.append(west_gate)
            self.entities.append(west_gate)
        
        # Add asteroids
        num_asteroids = random.randint(5, 20)
        for _ in range(num_asteroids):
            # Random position (avoiding center and gate paths)
            while True:
                # Random angle and distance from center
                angle = random.uniform(0, 2 * math.pi)
                distance = random.uniform(100, 350)
                
                # Calculate position
                x = SCREEN_WIDTH // 2 + math.cos(angle) * distance
                y = SCREEN_HEIGHT // 2 + math.sin(angle) * distance
                
                # Check if position is too close to gates (avoid main paths)
                too_close = False
                for gate in self.warp_gates:
                    gate_angle = math.atan2(gate.y - SCREEN_HEIGHT // 2, gate.x - SCREEN_WIDTH // 2)
                    angle_diff = abs((angle - gate_angle + math.pi) % (2 * math.pi) - math.pi)
                    if angle_diff < 0.5:  # Within ~30 degrees of gate path
                        too_close = True
                        break
                
                if not too_close:
                    break
            
            # Create asteroid
            asteroid = Asteroid(
                x, y,
                random.randint(5, 20),  # Size
                random.uniform(0, 2 * math.pi),  # Rotation
                random.choice(["Iron", "Ice", "Carbon", "Precious"])  # Type
            )
            self.entities.append(asteroid)
        
        # Add enemy ships based on danger level
        num_enemies = random.randint(0, self.danger_level // 2)
        for _ in range(num_enemies):
            # Random position (avoiding center)
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(150, 350)
            
            x = SCREEN_WIDTH // 2 + math.cos(angle) * distance
            y = SCREEN_HEIGHT // 2 + math.sin(angle) * distance
            
            # Create enemy ship
            enemy = EnemyShip(
                x, y,
                random.choice(["Pirate", "Trader", "Police", "Military"]),  # Type
                random.randint(1, self.danger_level)  # Level
            )
            self.entities.append(enemy)
    
    def connect_warp_gates(self):
        """Connect warp gates to neighboring systems"""
        # This is called after all systems are created
        # Since we only create gates where there are neighboring systems,
        # we can connect each gate to its corresponding neighbor
        
        # North gate connects to system with grid_y - 1
        if self.grid_y > 0:
            # Find the North gate
            for gate in self.warp_gates:
                if gate.direction == "North":
                    north_system = self.universe.get_system(self.grid_x, self.grid_y - 1)
                    gate.destination = north_system
                    break
        
        # East gate connects to system with grid_x + 1
        if self.grid_x < self.universe.width - 1:
            # Find the East gate
            for gate in self.warp_gates:
                if gate.direction == "East":
                    east_system = self.universe.get_system(self.grid_x + 1, self.grid_y)
                    gate.destination = east_system
                    break
        
        # South gate connects to system with grid_y + 1
        if self.grid_y < self.universe.height - 1:
            # Find the South gate
            for gate in self.warp_gates:
                if gate.direction == "South":
                    south_system = self.universe.get_system(self.grid_x, self.grid_y + 1)
                    gate.destination = south_system
                    break
        
        # West gate connects to system with grid_x - 1
        if self.grid_x > 0:
            # Find the West gate
            for gate in self.warp_gates:
                if gate.direction == "West":
                    west_system = self.universe.get_system(self.grid_x - 1, self.grid_y)
                    gate.destination = west_system
                    break
    
    def update(self, delta_time, player=None):
        """Update all entities in this system"""
        for entity in self.entities:
            if hasattr(entity, 'update'):
                entity.update(delta_time, player)
    
    def render(self, screen, player):
        """Render all entities in this system"""
        for entity in self.entities:
            if hasattr(entity, 'render'):
                entity.render(screen, player.x, player.y)
        
        # Render system name
        font = pygame.font.SysFont(None, 24)
        name_text = font.render(self.name, True, (200, 200, 200))
        screen.blit(name_text, (10, 10))
        
        # Render system info
        #info_text = font.render(f"Type: {self.system_type} | Faction: {self.faction} | Tech: {self.tech_level}", 
        #                      True, (200, 200, 200))
        #screen.blit(info_text, (10, 35))

class Universe:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.systems = {}  # Dictionary to store systems by coordinates
        
        # Create systems grid
        self.generate_systems()
        
        # Connect all systems
        self.connect_systems()
    
    def generate_systems(self):
        """Generate all star systems in the universe"""
        for x in range(self.width):
            for y in range(self.height):
                # Create a system at this grid position
                # Calculate position on galaxy map
                map_x = 100 + x * 80
                map_y = 100 + y * 80
                
                # Create system
                system = StarSystem(map_x, map_y, x, y, self)
                
                # Store in systems dictionary
                self.systems[(x, y)] = system
    
    def connect_systems(self):
        """Connect all systems with warp gates"""
        for coords, system in self.systems.items():
            system.connect_warp_gates()
    
    def get_system(self, x, y):
        """Get a system by its grid coordinates"""
        # Check if coordinates are valid
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.systems.get((x, y))
        return None
    
    def update_current_system(self, current_system, delta_time):
        """Update only the current system the player is in"""
        if current_system:
            current_system.update(delta_time)
    
    def render_current_system(self, screen, player):
        """Render only the current system the player is in"""
        if player.current_system:
            player.current_system.render(screen, player)
    
    def render_galaxy_map(self, screen, current_system):
        """Render the galaxy map showing all systems"""
        # Draw connections between systems
        for coords, system in self.systems.items():
            x, y = coords
            
            # Only draw connections for explored systems
            if system.explored:
                # Draw lines to adjacent systems if they are explored
                if x > 0 and self.systems[(x-1, y)].explored:
                    pygame.draw.line(screen, (100, 100, 100), 
                                   (system.map_x, system.map_y),
                                   (self.systems[(x-1, y)].map_x, self.systems[(x-1, y)].map_y), 2)
                
                if x < self.width - 1 and self.systems[(x+1, y)].explored:
                    pygame.draw.line(screen, (100, 100, 100), 
                                   (system.map_x, system.map_y),
                                   (self.systems[(x+1, y)].map_x, self.systems[(x+1, y)].map_y), 2)
                
                if y > 0 and self.systems[(x, y-1)].explored:
                    pygame.draw.line(screen, (100, 100, 100), 
                                   (system.map_x, system.map_y),
                                   (self.systems[(x, y-1)].map_x, self.systems[(x, y-1)].map_y), 2)
                
                if y < self.height - 1 and self.systems[(x, y+1)].explored:
                    pygame.draw.line(screen, (100, 100, 100), 
                                   (system.map_x, system.map_y),
                                   (self.systems[(x, y+1)].map_x, self.systems[(x, y+1)].map_y), 2)
        
        # Draw systems
        for coords, system in self.systems.items():
            # Only show explored systems
            if system.explored:
                # Different colors based on system type
                if system.system_type == "Agricultural":
                    color = (0, 200, 0)  # Green
                elif system.system_type == "Industrial":
                    color = (200, 100, 0)  # Orange
                elif system.system_type == "Mining":
                    color = (150, 150, 150)  # Gray
                elif system.system_type == "High-Tech":
                    color = (0, 150, 200)  # Blue
                elif system.system_type == "Tourist":
                    color = (200, 0, 200)  # Purple
                else:  # Frontier
                    color = (200, 200, 0)  # Yellow
                
                # Draw system dot
                pygame.draw.circle(screen, color, (system.map_x, system.map_y), 6)
                
                # Highlight current system
                if system == current_system:
                    pygame.draw.circle(screen, (255, 255, 255), (system.map_x, system.map_y), 10, 2)
                
                # Draw system name
                font = pygame.font.SysFont(None, 16)
                name_text = font.render(system.name, True, (200, 200, 200))
                screen.blit(name_text, (system.map_x - name_text.get_width() // 2, system.map_y + 10))
