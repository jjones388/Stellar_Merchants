import pygame
import math
import random
from projectile import Laser, Missile, Mine

class CombatManager:
    """Manages combat interactions between player and enemies"""
    def __init__(self, player, universe):
        self.player = player
        self.universe = universe
        self.enemy_projectiles = []  # List of projectiles fired by enemies
        self.explosion_particles = []  # List of explosion particles
        self.damage_numbers = []  # List of damage number displays
    
    def update(self, delta_time):
        """Update combat state"""
        # Skip if no current system
        if not self.player.current_system:
            return
        
        # Update enemy projectiles
        for projectile in self.enemy_projectiles[:]:
            projectile.update(delta_time)
            
            # Check if projectile has expired
            if projectile.lifetime <= 0:
                self.enemy_projectiles.remove(projectile)
                continue
            
            # Check for collision with player
            if projectile.check_collision(self.player):
                # Apply damage to player
                player_destroyed = self.player.take_damage(projectile.damage)
                
                # Create damage number
                self.create_damage_number(self.player.x, self.player.y, projectile.damage)
                
                # Create explosion
                self.create_explosion(projectile.x, projectile.y, 10)
                
                # Remove projectile
                self.enemy_projectiles.remove(projectile)
                
                # Handle player destruction
                if player_destroyed:
                    # In a full implementation, would trigger game over
                    pass
        
        # Check player projectiles against enemies
        for projectile in self.player.projectiles[:]:
            for entity in self.player.current_system.entities:
                # Only check enemy ships
                if entity.entity_type == "EnemyShip":
                    if projectile.check_collision(entity):
                        # Apply damage to enemy
                        entity.health -= projectile.damage
                        
                        # Create damage number
                        self.create_damage_number(entity.x, entity.y, projectile.damage)
                        
                        # Create explosion
                        self.create_explosion(projectile.x, projectile.y, 10)
                        
                        # Remove projectile
                        if projectile in self.player.projectiles:
                            self.player.projectiles.remove(projectile)
                        
                        # Check if enemy is destroyed
                        if entity.health <= 0:
                            # Create larger explosion
                            self.create_explosion(entity.x, entity.y, 20)
                            
                            # Remove enemy from system
                            self.player.current_system.entities.remove(entity)
                            
                            # In a full implementation, would add rewards, etc.
                            break
        
        # Update explosions
        for particle in self.explosion_particles[:]:
            particle['lifetime'] -= delta_time
            if particle['lifetime'] <= 0:
                self.explosion_particles.remove(particle)
            else:
                # Move particle
                particle['x'] += particle['vx'] * delta_time
                particle['y'] += particle['vy'] * delta_time
        
        # Update damage numbers
        for damage in self.damage_numbers[:]:
            damage['lifetime'] -= delta_time
            if damage['lifetime'] <= 0:
                self.damage_numbers.remove(damage)
            else:
                # Float upward
                damage['y'] -= 30 * delta_time
    
    def render(self, screen):
        """Render combat effects"""
        # Render enemy projectiles
        for projectile in self.enemy_projectiles:
            projectile.render(screen)
        
        # Render explosions
        for particle in self.explosion_particles:
            # Calculate alpha based on remaining lifetime
            alpha = min(255, int(255 * particle['lifetime'] / particle['max_lifetime']))
            
            # Calculate color with alpha
            if particle['type'] == 'fire':
                color = (255, 100 + int(155 * particle['lifetime'] / particle['max_lifetime']), 0, alpha)
            else:  # smoke
                gray = 150 + int(105 * particle['lifetime'] / particle['max_lifetime'])
                color = (gray, gray, gray, alpha)
            
            # Create a temporary surface for the particle with alpha
            particle_surface = pygame.Surface((int(particle['size'] * 2), int(particle['size'] * 2)), 
                                            pygame.SRCALPHA)
            
            # Draw the particle
            pygame.draw.circle(particle_surface, color, 
                             (int(particle['size']), int(particle['size'])), 
                             int(particle['size'] * (0.5 + 0.5 * particle['lifetime'] / particle['max_lifetime'])))
            
            # Calculate screen position relative to player
            screen_x = screen.get_width() // 2 + (particle['x'] - self.player.x)
            screen_y = screen.get_height() // 2 + (particle['y'] - self.player.y)
            
            # Blit the particle surface to the screen
            screen.blit(particle_surface, 
                      (int(screen_x - particle['size']), int(screen_y - particle['size'])))
        
        # Render damage numbers
        for damage in self.damage_numbers:
            # Calculate alpha based on remaining lifetime
            alpha = min(255, int(255 * damage['lifetime'] / damage['max_lifetime']))
            
            # Calculate screen position relative to player
            screen_x = screen.get_width() // 2 + (damage['x'] - self.player.x)
            screen_y = screen.get_height() // 2 + (damage['y'] - self.player.y)
            
            # Render text with alpha
            font = pygame.font.SysFont(None, 20)
            
            # Different colors based on damage amount
            if damage['amount'] >= 20:
                color = (255, 0, 0)  # Red for high damage
            elif damage['amount'] >= 10:
                color = (255, 150, 0)  # Orange for medium damage
            else:
                color = (255, 255, 0)  # Yellow for low damage
            
            text = font.render(str(int(damage['amount'])), True, color)
            
            # Create a surface with alpha for the text
            text_surface = pygame.Surface(text.get_size(), pygame.SRCALPHA)
            text_surface.fill((0, 0, 0, 0))  # Fill with transparent
            text_surface.blit(text, (0, 0))
            
            # Apply alpha to the entire surface
            text_surface.set_alpha(alpha)
            
            # Draw the text
            screen.blit(text_surface, 
                      (screen_x - text.get_width() // 2, screen_y - text.get_height() // 2))
    
    def enemy_fire_laser(self, enemy, target_x, target_y):
        """Create a laser projectile fired by an enemy"""
        # Calculate angle to target
        angle = math.atan2(target_y - enemy.y, target_x - enemy.x)
        
        # Calculate spawn position (front of enemy ship)
        spawn_x = enemy.x + math.cos(angle) * enemy.size
        spawn_y = enemy.y + math.sin(angle) * enemy.size
        
        # Create laser
        laser = Laser(spawn_x, spawn_y, angle, enemy.damage)
        
        # Add to enemy projectiles list
        self.enemy_projectiles.append(laser)
        
        # In full implementation, would play sound
    
    def enemy_fire_missile(self, enemy, target):
        """Create a missile projectile fired by an enemy"""
        # Calculate spawn position (front of enemy ship)
        spawn_x = enemy.x + math.cos(enemy.rotation) * enemy.size
        spawn_y = enemy.y + math.sin(enemy.rotation) * enemy.size
        
        # Create missile
        missile = Missile(spawn_x, spawn_y, enemy.rotation, enemy.damage * 1.5, target)
        
        # Add to enemy projectiles list
        self.enemy_projectiles.append(missile)
        
        # In full implementation, would play sound
    
    def enemy_deploy_mine(self, enemy):
        """Deploy a mine at an enemy's position"""
        # Create mine
        mine = Mine(enemy.x, enemy.y, enemy.damage * 2)
        
        # Add to enemy projectiles list
        self.enemy_projectiles.append(mine)
        
        # In full implementation, would play sound
    
    def create_explosion(self, x, y, size):
        """Create an explosion effect at the given position"""
        # Number of particles based on size
        num_particles = size * 2
        
        # Create explosion particles
        for _ in range(num_particles):
            # Random velocity
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(50, 150)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
            # Random size
            particle_size = random.uniform(size * 0.2, size * 0.6)
            
            # Random lifetime
            lifetime = random.uniform(0.3, 0.8)
            
            # Determine particle type (fire or smoke)
            particle_type = 'fire' if random.random() < 0.7 else 'smoke'
            
            # Create particle
            particle = {
                'x': x + random.uniform(-size * 0.2, size * 0.2),
                'y': y + random.uniform(-size * 0.2, size * 0.2),
                'vx': vx,
                'vy': vy,
                'size': particle_size,
                'lifetime': lifetime,
                'max_lifetime': lifetime,
                'type': particle_type
            }
            
            # Add to explosion particles list
            self.explosion_particles.append(particle)
        
        # In full implementation, would play sound
    
    def create_damage_number(self, x, y, amount):
        """Create a floating damage number at the given position"""
        # Create damage number
        damage = {
            'x': x + random.uniform(-10, 10),
            'y': y - 10,
            'amount': amount,
            'lifetime': 1.0,
            'max_lifetime': 1.0
        }
        
        # Add to damage numbers list
        self.damage_numbers.append(damage)
