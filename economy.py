import random
import math

class Commodity:
    """A tradable commodity in the game"""
    def __init__(self, name, category, base_price, tech_level_min, illegal=False):
        self.name = name
        self.category = category  # Raw, Manufactured, Luxury, Contraband
        self.base_price = base_price
        self.tech_level_min = tech_level_min  # Minimum tech level to produce
        self.illegal = illegal
        
        # Price fluctuation parameters
        self.volatility = random.uniform(0.05, 0.3)  # How much price changes
        self.price_state = random.uniform(-1.0, 1.0)  # Current price state
        
        # System specific price modifiers
        self.system_modifiers = {
            "Agricultural": {"Raw": 0.7, "Manufactured": 1.2, "Luxury": 1.1, "Contraband": 1.0},
            "Industrial": {"Raw": 1.2, "Manufactured": 0.8, "Luxury": 1.0, "Contraband": 1.0},
            "Mining": {"Raw": 0.6, "Manufactured": 1.1, "Luxury": 1.2, "Contraband": 1.0},
            "High-Tech": {"Raw": 1.3, "Manufactured": 0.7, "Luxury": 0.9, "Contraband": 1.1},
            "Tourist": {"Raw": 1.2, "Manufactured": 1.1, "Luxury": 0.6, "Contraband": 0.8},
            "Frontier": {"Raw": 1.1, "Manufactured": 1.3, "Luxury": 1.3, "Contraband": 0.6}
        }
        
        # Faction specific price modifiers
        self.faction_modifiers = {
            "Federation": {"Raw": 1.0, "Manufactured": 0.9, "Luxury": 1.1, "Contraband": 1.5},
            "Empire": {"Raw": 1.1, "Manufactured": 1.0, "Luxury": 0.8, "Contraband": 1.3},
            "Independent": {"Raw": 0.9, "Manufactured": 1.1, "Luxury": 1.0, "Contraband": 0.9},
            "Rebel": {"Raw": 1.2, "Manufactured": 1.2, "Luxury": 1.2, "Contraband": 0.7},
            "Corporate": {"Raw": 0.8, "Manufactured": 0.8, "Luxury": 0.9, "Contraband": 1.2}
        }
        
        # System type supply/demand modifiers (positive means high supply, negative means high demand)
        self.supply_modifiers = {
            "Agricultural": {"Raw": 0.5, "Manufactured": -0.3, "Luxury": -0.1, "Contraband": 0.0},
            "Industrial": {"Raw": -0.3, "Manufactured": 0.5, "Luxury": 0.0, "Contraband": 0.0},
            "Mining": {"Raw": 0.7, "Manufactured": -0.2, "Luxury": -0.3, "Contraband": 0.0},
            "High-Tech": {"Raw": -0.4, "Manufactured": 0.4, "Luxury": 0.2, "Contraband": -0.1},
            "Tourist": {"Raw": -0.2, "Manufactured": -0.1, "Luxury": 0.5, "Contraband": 0.3},
            "Frontier": {"Raw": 0.3, "Manufactured": -0.5, "Luxury": -0.4, "Contraband": 0.5}
        }
    
    def get_system_price(self, system):
        """Calculate the price of this commodity in a specific system"""
        # Base modifiers from system type and faction
        system_mod = self.system_modifiers.get(system.system_type, {}).get(self.category, 1.0)
        faction_mod = self.faction_modifiers.get(system.faction, {}).get(self.category, 1.0)
        
        # Tech level modifier (higher tech level means better prices for low-tech goods)
        tech_diff = system.tech_level - self.tech_level_min
        tech_mod = 1.0 - (0.05 * max(0, tech_diff))  # 5% less per tech level above minimum
        tech_mod = max(0.7, tech_mod)  # Cap at 30% discount
        
        # Price state fluctuation
        fluctuation = 1.0 + (self.price_state * self.volatility)
        
        # Calculate final price
        price = self.base_price * system_mod * faction_mod * tech_mod * fluctuation
        
        # Round to nearest integer
        return round(price)
    
    def get_system_quantity(self, system):
        """Calculate the available quantity of this commodity in a specific system"""
        # Base quantity (higher for higher tech systems)
        base_quantity = 10 + system.tech_level * 5
        
        # Adjust based on supply/demand modifiers
        supply_mod = self.supply_modifiers.get(system.system_type, {}).get(self.category, 0.0)
        
        # Apply modifier (positive means more supply, negative means less)
        quantity_mod = 1.0 + supply_mod
        quantity = base_quantity * quantity_mod
        
        # Illegal goods are less available
        if self.illegal:
            quantity *= 0.5
        
        # Random variation
        variation = random.uniform(0.7, 1.3)
        
        # Calculate final quantity
        final_quantity = max(0, round(quantity * variation))
        
        # If tech level is too low, no quantity available
        if system.tech_level < self.tech_level_min:
            final_quantity = 0
        
        return final_quantity
    
    def update_price_state(self):
        """Update the price state for this commodity"""
        # Randomly walk the price up or down
        self.price_state += random.uniform(-0.2, 0.2)
        
        # Clamp to range [-1, 1]
        self.price_state = max(-1.0, min(1.0, self.price_state))
        
        # Tendency to revert to mean
        self.price_state *= 0.95

class Economy:
    """Manages the game's economy and trading"""
    def __init__(self, universe):
        self.universe = universe
        self.commodities = []
        self.system_markets = {}  # Cache of market data by system
        self.market_update_time = 300  # Seconds between market updates
        self.last_update = 0
        
        # Initialize commodities
        self.initialize_commodities()
    
    def initialize_commodities(self):
        """Create all tradable commodities"""
        # Raw materials (low tech level requirement)
        self.commodities.extend([
            Commodity("Food", "Raw", 50, 1),
            Commodity("Water", "Raw", 30, 1),
            Commodity("Minerals", "Raw", 80, 1),
            Commodity("Ore", "Raw", 100, 2),
            Commodity("Crystals", "Raw", 150, 3),
            Commodity("Metals", "Raw", 120, 2),
            Commodity("Fuel", "Raw", 90, 2),
            Commodity("Gases", "Raw", 70, 3)
        ])
        
        # Manufactured goods (medium tech level requirement)
        self.commodities.extend([
            Commodity("Electronics", "Manufactured", 200, 5),
            Commodity("Weapons", "Manufactured", 350, 4),
            Commodity("Medicine", "Manufactured", 300, 5),
            Commodity("Machinery", "Manufactured", 250, 3),
            Commodity("Tools", "Manufactured", 180, 3),
            Commodity("Construction Materials", "Manufactured", 150, 2),
            Commodity("Clothing", "Manufactured", 120, 2),
            Commodity("Robots", "Manufactured", 400, 7)
        ])
        
        # Luxury goods (higher tech level requirement)
        self.commodities.extend([
            Commodity("Art", "Luxury", 500, 4),
            Commodity("Jewelry", "Luxury", 600, 5),
            Commodity("Exotic Foods", "Luxury", 400, 4),
            Commodity("Antiques", "Luxury", 700, 3),
            Commodity("Entertainment Systems", "Luxury", 450, 6),
            Commodity("Designer Clothes", "Luxury", 350, 5),
            Commodity("Luxury Vehicles", "Luxury", 800, 7),
            Commodity("Virtual Reality Equipment", "Luxury", 650, 8)
        ])
        
        # Contraband (illegal goods)
        self.commodities.extend([
            Commodity("Narcotics", "Contraband", 900, 3, True),
            Commodity("Stolen Goods", "Contraband", 500, 2, True),
            Commodity("Illegal Weapons", "Contraband", 1200, 5, True),
            Commodity("Slaves", "Contraband", 2000, 4, True),
            Commodity("Forbidden Technology", "Contraband", 1500, 8, True)
        ])
    
    def update(self):
        """Update commodity prices and stock levels"""
        # Update price states for all commodities
        for commodity in self.commodities:
            commodity.update_price_state()
        
        # Clear market cache to force recalculation
        self.system_markets = {}
    
    def get_system_market(self, system):
        """Get market data for a specific system"""
        # Check if we have cached data
        if system in self.system_markets:
            return self.system_markets[system]
        
        # Calculate market data for this system
        market_data = []
        
        for commodity in self.commodities:
            price = commodity.get_system_price(system)
            quantity = commodity.get_system_quantity(system)
            
            market_data.append({
                'commodity': commodity,
                'buy_price': price,
                'sell_price': int(price * 0.8),  # 20% less when selling to station
                'quantity': quantity
            })
        
        # Sort by category then name
        market_data.sort(key=lambda x: (x['commodity'].category, x['commodity'].name))
        
        # Cache the result
        self.system_markets[system] = market_data
        
        return market_data
    
    def buy_commodity(self, player, system, commodity_name, quantity):
        """Player buys a commodity from the system"""
        # Get market data
        market = self.get_system_market(system)
        
        # Find the commodity
        for item in market:
            if item['commodity'].name == commodity_name:
                # Check if enough in stock
                if item['quantity'] >= quantity:
                    # Calculate total cost
                    total_cost = item['buy_price'] * quantity
                    
                    # Check if player has enough credits
                    if player.credits >= total_cost:
                        # Check if player has enough cargo space
                        if player.get_cargo_space_remaining() >= quantity:
                            # Deduct credits
                            player.credits -= total_cost
                            
                            # Add to player's cargo
                            player.add_cargo(commodity_name, quantity)
                            
                            # Reduce quantity in market
                            item['quantity'] -= quantity
                            
                            return True, "Purchase successful"
                        else:
                            return False, "Not enough cargo space"
                    else:
                        return False, "Not enough credits"
                else:
                    return False, "Not enough stock available"
        
        return False, "Commodity not found"
    
    def sell_commodity(self, player, system, commodity_name, quantity):
        """Player sells a commodity to the system"""
        # Get market data
        market = self.get_system_market(system)
        
        # Find the commodity
        for item in market:
            if item['commodity'].name == commodity_name:
                # Check if player has enough in cargo
                if commodity_name in player.cargo and player.cargo[commodity_name] >= quantity:
                    # Calculate total value
                    total_value = item['sell_price'] * quantity
                    
                    # Add credits to player
                    player.credits += total_value
                    
                    # Remove from player's cargo
                    player.remove_cargo(commodity_name, quantity)
                    
                    # Increase quantity in market
                    item['quantity'] += quantity
                    
                    return True, "Sale successful"
                else:
                    return False, "Not enough in cargo"
        
        return False, "Commodity not found"
    
    def get_price_trend(self, commodity_name):
        """Get price trend indicator for a commodity"""
        for commodity in self.commodities:
            if commodity.name == commodity_name:
                # Use price_state to determine trend
                if commodity.price_state > 0.2:
                    return "↑"  # Rising
                elif commodity.price_state < -0.2:
                    return "↓"  # Falling
                else:
                    return "→"  # Stable
        
        return "?"  # Unknown
    
    def get_best_deals(self, current_system, known_systems, top_n=5):
        """Find the best trading opportunities from current system to known systems"""
        deals = []
        
        # Get market data for current system
        current_market = self.get_system_market(current_system)
        
        # Check each commodity in current system
        for current_item in current_market:
            # Skip if no stock available to buy
            if current_item['quantity'] <= 0:
                continue
            
            commodity = current_item['commodity']
            buy_price = current_item['buy_price']
            
            # Check each known system for selling opportunities
            for dest_system in known_systems:
                # Skip current system
                if dest_system == current_system:
                    continue
                
                # Get market data for destination system
                dest_market = self.get_system_market(dest_system)
                
                # Find same commodity in destination market
                for dest_item in dest_market:
                    if dest_item['commodity'].name == commodity.name:
                        sell_price = dest_item['sell_price']
                        
                        # Calculate profit per unit
                        profit_per_unit = sell_price - buy_price
                        
                        # Only include profitable trades
                        if profit_per_unit > 0:
                            deals.append({
                                'commodity': commodity.name,
                                'from_system': current_system.name,
                                'to_system': dest_system.name,
                                'buy_price': buy_price,
                                'sell_price': sell_price,
                                'profit_per_unit': profit_per_unit,
                                'quantity_available': current_item['quantity']
                            })
        
        # Sort by profit per unit (descending)
        deals.sort(key=lambda x: x['profit_per_unit'], reverse=True)
        
        # Return top N deals
        return deals[:top_n]
    
    def create_market_event(self, system):
        """Create a special market event in a system"""
        event_types = [
            "Shortage",
            "Surplus",
            "Price Crash",
            "Price Spike",
            "Trade Festival",
            "Blockade",
            "Plague",
            "Luxury Boom"
        ]
        
        # Select random event
        event_type = random.choice(event_types)
        
        # Duration in days
        duration = random.randint(3, 10)
        
        # Affected commodities (1-3 random commodities)
        num_commodities = random.randint(1, 3)
        affected_commodities = random.sample(self.commodities, num_commodities)
        
        # Create event
        event = {
            'type': event_type,
            'system': system,
            'duration': duration,
            'commodities': affected_commodities,
            'description': self.generate_event_description(event_type, system, affected_commodities)
        }
        
        # Apply event effects
        self.apply_event_effects(event)
        
        return event
    
    def generate_event_description(self, event_type, system, commodities):
        """Generate a description for a market event"""
        commodity_names = [c.name for c in commodities]
        
        if len(commodity_names) == 1:
            commodity_str = commodity_names[0]
        elif len(commodity_names) == 2:
            commodity_str = f"{commodity_names[0]} and {commodity_names[1]}"
        else:
            commodity_str = ", ".join(commodity_names[:-1]) + f", and {commodity_names[-1]}"
        
        if event_type == "Shortage":
            return f"A shortage of {commodity_str} has struck {system.name} due to production issues."
        elif event_type == "Surplus":
            return f"An unexpected surplus of {commodity_str} has flooded the market in {system.name}."
        elif event_type == "Price Crash":
            return f"Prices for {commodity_str} have crashed in {system.name} due to market panic."
        elif event_type == "Price Spike":
            return f"Prices for {commodity_str} have spiked in {system.name} due to high demand."
        elif event_type == "Trade Festival":
            return f"A trade festival in {system.name} has increased commerce in {commodity_str}."
        elif event_type == "Blockade":
            return f"A blockade in {system.name} has restricted trade in {commodity_str}."
        elif event_type == "Plague":
            return f"A plague in {system.name} has affected demand for {commodity_str}."
        elif event_type == "Luxury Boom":
            return f"A luxury boom in {system.name} has increased demand for {commodity_str}."
        else:
            return f"An unknown event is affecting {commodity_str} in {system.name}."
    
    def apply_event_effects(self, event):
        """Apply effects of a market event"""
        # Price modifiers based on event type
        price_modifiers = {
            "Shortage": 1.5,      # 50% price increase
            "Surplus": 0.7,       # 30% price decrease
            "Price Crash": 0.5,   # 50% price decrease
            "Price Spike": 2.0,   # 100% price increase
            "Trade Festival": 1.2, # 20% price increase
            "Blockade": 1.8,      # 80% price increase
            "Plague": 0.8,        # 20% price decrease
            "Luxury Boom": 1.5    # 50% price increase
        }
        
        # Quantity modifiers based on event type
        quantity_modifiers = {
            "Shortage": 0.3,      # 70% less available
            "Surplus": 2.0,       # 100% more available
            "Price Crash": 1.5,   # 50% more available
            "Price Spike": 0.5,   # 50% less available
            "Trade Festival": 1.5, # 50% more available
            "Blockade": 0.2,      # 80% less available
            "Plague": 0.7,        # 30% less available
            "Luxury Boom": 0.8    # 20% less available
        }
        
        # Get modifiers for this event
        price_mod = price_modifiers.get(event['type'], 1.0)
        quantity_mod = quantity_modifiers.get(event['type'], 1.0)
        
        # Apply modifiers to each affected commodity
        for commodity in event['commodities']:
            commodity.price_state = (price_mod - 1.0) * 2  # Adjust price state
            
            # Clear cached market data for the system
            if event['system'] in self.system_markets:
                del self.system_markets[event['system']]
        
        # In a full implementation, would need to persist these effects for the event duration
