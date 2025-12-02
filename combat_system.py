"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

Handles combat mechanics
"""

from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError
)

# ============================================================================
# ENEMY DEFINITIONS
# ============================================================================

def create_enemy(enemy_type): # creates enemy based on type meaning goblin, orc, dragon
    """
    Create an enemy based on type
    
    Example enemy types and stats:
    - goblin: health=50, strength=8, magic=2, xp_reward=25, gold_reward=10
    - orc: health=80, strength=12, magic=5, xp_reward=50, gold_reward=25
    - dragon: health=200, strength=25, magic=15, xp_reward=200, gold_reward=100
    
    Returns: Enemy dictionary
    Raises: InvalidTargetError if enemy_type not recognized
    """
    # TODO: Implement enemy creation
    # Return dictionary with: name, health, max_health, strength, magic, xp_reward, gold_reward
    enemy_type = enemy_type.capitalize()
    if enemy_type == "Goblin":
        return {
            'name': 'Goblin',
            'health': 50,
            'max_health': 50,
            'strength': 8,
            'magic': 2,
            'xp_reward': 25,
            'gold_reward': 10
        }
    elif enemy_type == "Orc":
        return {
            'name': 'Orc',
            'health': 80,
            'max_health': 80,
            'strength': 12,
            'magic': 5,
            'xp_reward': 50,
            'gold_reward': 25
        }
    elif enemy_type == "Dragon":
        return {
            'name': 'Dragon',
            'health': 200,
            'max_health': 200,
            'strength': 25,
            'magic': 15,
            'xp_reward': 200,
            'gold_reward': 100
        }
    else:
        raise InvalidTargetError()

def get_random_enemy_for_level(character_level): # creates enemy based on character level
    """
    Get an appropriate enemy for character's level
    
    Level 1-2: Goblins
    Level 3-5: Orcs
    Level 6+: Dragons
    
    Returns: Enemy dictionary
    """
    # TODO: Implement level-appropriate enemy selection
    # Use if/elif/else to select enemy type
    # Call create_enemy with appropriate type
    if int(character_level) <= 2:
        return create_enemy("Goblin")
    elif 3 <= int(character_level) <= 5:
        return create_enemy("Orc")
    else:
        return create_enemy("Dragon")

# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle: # simple turn-based combat system
    """
    Simple turn-based combat system
    
    Manages combat between character and enemy
    """
    
    def __init__(self, character, enemy):
        """Initialize battle with character and enemy"""
        # TODO: Implement initialization
        # Store character and enemy
        # Set combat_active flag
        # Initialize turn counter
        self.character = character
        self.enemy = enemy
        self.combat_active = True
        self.turn_counter = 1
    
    def start_battle(self): # starts the battle loop
        """
        Start the combat loop
        
        Returns: Dictionary with battle results:
                {'winner': 'player'|'enemy', 'xp_gained': int, 'gold_gained': int}
        
        Raises: CharacterDeadError if character is already dead
        """
        # TODO: Implement battle loop
        # Check character isn't dead
        # Loop until someone dies
        # Award XP and gold if player wins
        if int(self.character['health']) <= 0:
            raise CharacterDeadError()
        while self.combat_active:
            self.player_turn()
            if not self.combat_active:
                break
            self.enemy_turn()
            result = self.check_battle_end()
            if result == 'player':
                self.combat_active = False
                xp = self.enemy['xp_reward']
                gold = self.enemy['gold_reward']
                return {'winner': 'player', 'xp_gained': xp, 'gold_gained': gold}
            elif result == 'enemy':
                self.combat_active = False
                raise CharacterDeadError()
            self.turn_counter += 1 
    
    def player_turn(self): # handles player's turn
        """
        Handle player's turn
        
        Displays options:
        1. Basic Attack
        2. Special Ability (if available)
        3. Try to Run
        
        Raises: CombatNotActiveError if called outside of battle
        """
        # TODO: Implement player turn
        # Check combat is active
        # Display options
        # Get player choice
        # Execute chosen action
        if self.combat_active:
            print("\nPlayer's Turn:")
            print("1. Basic Attack")
            print("2. Special Ability")
            print("3. Try to Run")
            choice = input("Choose an action (1-3): ")
            if choice == '1':
                damage = self.calculate_damage(self.character, self.enemy)
                self.apply_damage(self.enemy, damage)
                display_battle_log(f"You attack the {self.enemy['name']} for {damage} damage!")
            elif choice == '2':
                try:
                    result = use_special_ability(self.character, self.enemy)
                    display_battle_log(result)
                except AbilityOnCooldownError as e:
                    display_battle_log(str(e))
            elif choice == '3':
                escaped = self.attempt_escape()
                if escaped:
                    display_battle_log("You successfully escaped the battle!")
                    self.combat_active = False
                else:
                    display_battle_log("Escape failed! The battle continues.")
            else:
                display_battle_log("Invalid choice! You lose your turn.")
        else:
            raise CombatNotActiveError()
    
    def enemy_turn(self): # creates simple enemy AI for its turn
        """
        Handle enemy's turn - simple AI
        
        Enemy always attacks
        
        Raises: CombatNotActiveError if called outside of battle
        """
        # TODO: Implement enemy turn
        # Check combat is active
        # Calculate damage
        # Apply to character
        if not self.combat_active:
            raise CombatNotActiveError()
        if not self.check_battle_end():
            damage = self.calculate_damage(self.enemy, self.character)
            self.apply_damage(self.character, damage)
            display_battle_log(f"The {self.enemy['name']} attacks you for {damage} damage!")
    
    def calculate_damage(self, attacker, defender): # calculates damage from attacker to defender
        """
        Calculate damage from attack
        
        Damage formula: attacker['strength'] - (defender['strength'] // 4)
        Minimum damage: 1
        
        Returns: Integer damage amount
        """
        # TODO: Implement damage calculation
        base_damage = int(attacker['strength']) - (int(defender['strength']) // 4)
        return max(1, base_damage)
    
    def apply_damage(self, target, damage): # applies damage to target
        """
        Apply damage to a character or enemy
        
        Reduces health, prevents negative health
        """
        # TODO: Implement damage application
        target['health'] = max(0, int(target['health']) - int(damage))
    
    def check_battle_end(self): # checks if battle is over
        """
        Check if battle is over
        
        Returns: 'player' if enemy dead, 'enemy' if character dead, None if ongoing
        """
        # TODO: Implement battle end check
        if int(self.enemy['health']) <= 0:
            return 'player'
        elif int(self.character['health']) <= 0:
            return 'enemy'
        else:
            return None
    
    def attempt_escape(self): # handels if players attempts to escape from battle
        """
        Try to escape from battle
        
        50% success chance
        
        Returns: True if escaped, False if failed
        """
        # TODO: Implement escape attempt
        # Use random number or simple calculation
        # If successful, set combat_active to False
        import random
        return random.choice([True, False])


# ============================================================================
# SPECIAL ABILITIES
# ============================================================================

def use_special_ability(character, enemy): # uses character's special ability based on class
    """
    Use character's class-specific special ability
    
    Example abilities by class:
    - Warrior: Power Strike (2x strength damage)
    - Mage: Fireball (2x magic damage)
    - Rogue: Critical Strike (3x strength damage, 50% chance)
    - Cleric: Heal (restore 30 health)
    
    Returns: String describing what happened
    Raises: AbilityOnCooldownError if ability was used recently
    """
    # TODO: Implement special abilities
    # Check character class
    # Execute appropriate ability
    # Track cooldowns (optional advanced feature)
    char_class = character.get('class', '').lower()
    if char_class == 'warrior':
        warrior_power_strike(character, enemy)
        return "You used Power Strike!"
    elif char_class == 'mage':
        mage_fireball(character, enemy)
        return "You cast Fireball!"
    elif char_class == 'rogue':
        rogue_critical_strike(character, enemy)
        return "You performed Critical Strike!"
    elif char_class == 'cleric':
        cleric_heal(character)
        return "You cast Heal!"
    else:
        raise AbilityOnCooldownError()
def warrior_power_strike(character, enemy): # warrior special ability
    """Warrior special ability"""
    # TODO: Implement power strike
    # Double strength damage
    damage = int(character['strength']) * 2 - (int(enemy['strength']) // 4)
    damage = max(1, damage)
    enemy['health'] = max(0, int(enemy['health']) - int(damage))


def mage_fireball(character, enemy): # mage special ability
    """Mage special ability"""
    # TODO: Implement fireball
    # Double magic damage
    damage = int(character['magic']) * 2 - (int(enemy['strength']) // 4)
    damage = max(1, damage)
    enemy['health'] = max(0, int(enemy['health']) - int(damage))


def rogue_critical_strike(character, enemy): # rogue special ability
    """Rogue special ability"""
    # TODO: Implement critical strike
    # 50% chance for triple damage
    import random
    if random.random() < 0.5:
        damage = int(character['strength']) * 3 - (int(enemy['strength']) // 4)
    else:
        damage = int(character['strength']) - (int(enemy['strength']) // 4)
    damage = max(1, damage)
    enemy['health'] = max(0, int(enemy['health']) - int(damage))

def cleric_heal(character): # cleric special ability
    """Cleric special ability"""
    # TODO: Implement healing
    # Restore 30 HP (not exceeding max_health)
    heal_amount = 30
    character['health'] = min(int(character['max_health']), int(character['health']) + int(heal_amount))


# ============================================================================
# COMBAT UTILITIES
# ============================================================================

def can_character_fight(character): # checks if character can fight (based on health)
    """
    Check if character is in condition to fight
    
    Returns: True if health > 0 and not in battle
    """
    # TODO: Implement fight check
    return character['health'] > 0

def get_victory_rewards(enemy): # calculates rewards for defeating enemy
    """
    Calculate rewards for defeating enemy
    
    Returns: Dictionary with 'xp' and 'gold'
    """
    # TODO: Implement reward calculation
    return {
        'xp': enemy['xp_reward'],
        'gold': enemy['gold_reward']
    }


def display_combat_stats(character, enemy): # displays current combat stats
    """
    Display current combat status
    
    Shows both character and enemy health/stats
    """
    # TODO: Implement status display
    print(f"\n{character['name']}: HP={character['health']}/{character['max_health']}")
    print(f"{enemy['name']}: HP={enemy['health']}/{enemy['max_health']}")

def display_battle_log(message): # displays battle messages to keep player informed of the damage theve delt and and reciving and if they won or not
    """
    Display a formatted battle message
    """
    # TODO: Implement battle log display
    print(f">>> {message}")

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== COMBAT SYSTEM TEST ===")
    
    #Test enemy creation
    try:
        goblin = create_enemy("goblin")
        print(f"Created {goblin['name']}")
    except InvalidTargetError as e:
        print(f"Invalid enemy: {e}")
    
    # Test battle
    test_char = {
        'name': 'Hero',
        'class': 'Warrior',
        'health': 120,
        'max_health': 120,
        'strength': 15,
        'magic': 5
    }
    #
    battle = SimpleBattle(test_char, goblin)
    try:
        result = battle.start_battle()
        print(f"Battle result: {result}")
    except CharacterDeadError:
        print("Character is dead!")

