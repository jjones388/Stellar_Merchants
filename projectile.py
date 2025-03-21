import pygame
import math

class Projectile:
    """Base class for all projectiles"""
    def __init__(self, x, y, angle, damage):
        self.x = x
        self.y = y
        self.angle = angle
        self.damage = damage
        self.speed = 0
        self.lifetime = 0
        self.max_lifetime = 0
        self.color = (255, 255, 255)
        self.size = 2
    
    def update(self, delta_time):
        """Update projectile position"""
        # Move in the direction of angle
        self.x += math.cos(self.angle) * self.speed * delta_time
        self.y += math.sin(self.angle) * self.speed * delta_time
        
        # Decrease lifetime
        self.lifetime -= delta_time
    
    def render(self, screen):
        """Render the projectile"""
        # Draw projectile
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
    
    def render_at(self, screen, screen_x, screen_y):
        """Render the projectile at the specified screen coordinates"""
        # Draw projectile at the given position
        pygame.draw.circle(screen, self.color, (int(screen_x), int(screen_y)), self.size)
    
    def check_collision(self, entity):
        """Check if projectile collides with an entity"""
        if hasattr(entity, 'hit_radius'):
            radius = entity.hit_radius
        else:
            radius = entity.size
            
        distance = math.sqrt((self.x - entity.x)**2 + (self.y - entity.y)**2)
        return distance < radius + self.size

class Laser(Projectile):
    """A basic laser projectile"""
    def __init__(self, x, y, angle, damage):
        super().__init__(x, y, angle, damage)
        self.speed = 600  # Pixels per second
        self.lifetime = 1.0  # Seconds
        self.max_lifetime = 1.0
        self.color = (255, 0, 0)  # Red laser
        self.length = 20  # Laser length
        self.width = 2    # Laser width
    
    def render_at(self, screen, screen_x, screen_y):
        """Render the laser at the specified screen coordinates"""
        # Calculate end position
        end_x = screen_x - math.cos(self.angle) * self.length
        end_y = screen_y - math.sin(self.angle) * self.length
        
        # Draw laser trail
        pygame.draw.line(screen, self.color, (screen_x, screen_y), (end_x, end_y), self.width)
        
        # Draw bright core
        pygame.draw.line(screen, (255, 255, 255), (screen_x, screen_y), 
                        (screen_x - math.cos(self.angle) * 5, screen_y - math.sin(self.angle) * 5), 1)

class Missile(Projectile):
    """A guided missile projectile"""
    def __init__(self, x, y, angle, damage, target=None):
        super().__init__(x, y, angle, damage)
        self.speed = 200  # Slower than laser but tracks target
        self.lifetime = 5.0  # Longer lifetime
        self.max_lifetime = 5.0
        self.color = (255, 200, 0)  # Yellow/orange
        self.size = 3
        self.target = target  # Entity to track
        self.turn_rate = 3.0  # Radians per second
        self.smoke_trail = []  # List of smoke particles
    
    def update(self, delta_time):
        """Update missile position and tracking"""
        # If we have a target, adjust angle to track it
        if self.target and hasattr(self.target, 'x') and hasattr(self.target, 'y'):
            # Calculate angle to target
            target_angle = math.atan2(self.target.y - self.y, self.target.x - self.x)
            
            # Calculate angle difference
            angle_diff = ((target_angle - self.angle + math.pi) % (2 * math.pi)) - math.pi
            
            # Adjust angle (limited by turn rate)
            max_turn = self.turn_rate * delta_time
            if abs(angle_diff) > max_turn:
                angle_diff = max_turn if angle_diff > 0 else -max_turn
            
            self.angle += angle_diff
        
        # Call parent update for movement
        super().update(delta_time)
        
        # Add smoke trail particle
        if self.lifetime < self.max_lifetime - 0.1:  # Don't create smoke for the first 0.1s
            self.smoke_trail.append({
                'x': self.x,
                'y': self.y,
                'lifetime': 0.5,  # Smoke lifetime in seconds
                'size': self.size * 0.8
            })
        
        # Update smoke trail
        for particle in self.smoke_trail[:]:
            particle['lifetime'] -= delta_time
            if particle['lifetime'] <= 0:
                self.smoke_trail.remove(particle)
    
    def render(self, screen):
        """Render the missile and its smoke trail"""
        # Render smoke trail first (so missile appears on top)
        for particle in self.smoke_trail:
            # Calculate alpha based on remaining lifetime
            alpha = min(255, int(255 * particle['lifetime'] / 0.5))
            
            # Calculate color with alpha
            smoke_color = (200, 200, 200, alpha)
            
            # Create a temporary surface for the smoke with alpha
            smoke_surface = pygame.Surface((int(particle['size'] * 2), int(particle['size'] * 2)), 
                                          pygame.SRCALPHA)
            
            # Draw the smoke particle
            pygame.draw.circle(smoke_surface, smoke_color, 
                             (int(particle['size']), int(particle['size'])), 
                             int(particle['size']))
            
            # Blit the smoke surface to the screen
            screen.blit(smoke_surface, 
                      (int(particle['x'] - particle['size']), int(particle['y'] - particle['size'])))
        
        # Render missile itself
        # Missile body
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        
        # Engine glow
        engine_x = self.x - math.cos(self.angle) * self.size * 1.5
        engine_y = self.y - math.sin(self.angle) * self.size * 1.5
        pygame.draw.circle(screen, (255, 100, 0), (int(engine_x), int(engine_y)), self.size * 0.8)

class Mine(Projectile):
    """A stationary mine that explodes on contact"""
    def __init__(self, x, y, damage):
        super().__init__(x, y, 0, damage)
        self.speed = 0  # Doesn't move
        self.lifetime = 20.0  # Long lifetime
        self.max_lifetime = 20.0
        self.color = (255, 0, 0)
        self.size = 6
        self.pulse_time = 0
        self.pulse_period = 1.0  # Seconds per pulse
        self.armed = False
        self.arm_time = 1.0  # Time before mine is armed
    
    def update(self, delta_time):
        """Update mine state"""
        # Decrease lifetime
        super().update(delta_time)
        
        # Update pulse time
        self.pulse_time += delta_time
        if self.pulse_time > self.pulse_period:
            self.pulse_time = 0
        
        # Arm the mine after a delay
        if not self.armed and self.max_lifetime - self.lifetime >= self.arm_time:
            self.armed = True
    
    def render(self, screen):
        """Render the mine with pulsing effect"""
        # Calculate pulse value (0 to 1)
        pulse_value = abs(math.sin(self.pulse_time * math.pi / self.pulse_period))
        
        # Mine body
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        
        # Pulsing core
        core_size = self.size * 0.5 * (0.5 + 0.5 * pulse_value)
        
        # Different color based on armed status
        if self.armed:
            core_color = (255, 255, 0)  # Yellow when armed
        else:
            core_color = (100, 100, 100)  # Gray when not armed
            
        pygame.draw.circle(screen, core_color, (int(self.x), int(self.y)), int(core_size))
        
        # Spikes
        for i in range(8):
            angle = i * math.pi / 4
            spike_x = self.x + math.cos(angle) * self.size
            spike_y = self.y + math.sin(angle) * self.size
            spike_length = self.size * 0.5
            
            # Draw spike
            pygame.draw.line(screen, self.color,
                           (spike_x, spike_y),
                           (spike_x + math.cos(angle) * spike_length,
                            spike_y + math.sin(angle) * spike_length),
                           2)
