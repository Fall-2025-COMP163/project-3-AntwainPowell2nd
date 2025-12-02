"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles character creation, loading, and saving.
"""

import os
from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    InvalidSaveDataError,
    CharacterDeadError
)

# ============================================================================
# CHARACTER MANAGEMENT FUNCTIONS
# ============================================================================

def create_character(name, character_class): # creates a new character and validates classes 
    """
    Create a new character with stats based on class
    
    Valid classes: Warrior, Mage, Rogue, Cleric
    
    Returns: Dictionary with character data including:
            - name, class, level, health, max_health, strength, magic
            - experience, gold, inventory, active_quests, completed_quests
    
    Raises: InvalidCharacterClassError if class is not valid
    """
    # TODO: Implement character creation
    # Validate character_class first
    # Example base stats:
    # Warrior: health=120, strength=15, magic=5
    # Mage: health=80, strength=8, magic=20
    # Rogue: health=90, strength=12, magic=10
    # Cleric: health=100, strength=10, magic=15
    
    # All characters start with:
    # - level=1, experience=0, gold=100
    # - inventory=[], active_quests=[], completed_quests=[]
    
    # Raise InvalidCharacterClassError if class not in valid list
    character_class = character_class.capitalize()
    valid_classes = {
        "Warrior": {"health": 120, "strength": 15, "magic": 5},
        "Mage": {"health": 80, "strength": 8, "magic": 20},
        "Rogue": {"health": 90, "strength": 12, "magic": 10},
        "Cleric": {"health": 100, "strength": 10, "magic": 15}
    }

    if character_class not in valid_classes:
        raise InvalidCharacterClassError

    stats = valid_classes[character_class]
    return {
        "name": name,
        "class": character_class,
        "level": 1,
        "health": stats["health"],
        "max_health": stats["health"],
        "strength": stats["strength"],
        "magic": stats["magic"],
        "experience": 0,
        "gold": 100,
        "inventory": [],
        "active_quests": [],
        "completed_quests": []
    }



def save_character(character, save_directory="data/save_games"): # saves character data to a file
    """
    Save character to file
    
    Filename format: {character_name}_save.txt
    
    File format:
    NAME: character_name
    CLASS: class_name
    LEVEL: 1
    HEALTH: 120
    MAX_HEALTH: 120
    STRENGTH: 15
    MAGIC: 5
    EXPERIENCE: 0
    GOLD: 100
    INVENTORY: item1,item2,item3
    ACTIVE_QUESTS: quest1,quest2
    COMPLETED_QUESTS: quest1,quest2
    
    Returns: True if successful
    Raises: PermissionError, IOError (let them propagate or handle)
    """
    # TODO: Implement save functionality
    # Create save_directory if it doesn't exist
    # Handle any file I/O errors appropriately
    # Lists should be saved as comma-separated values
    os.makedirs(save_directory, exist_ok=True)
    filename = f"{character['name']}_save.txt"
    filepath = os.path.join(save_directory, filename)

    try:
        lines = [
            f"NAME: {character['name']}",
            f"CLASS: {character['class']}",
            f"LEVEL: {character['level']}",
            f"HEALTH: {character['health']}",
            f"MAX_HEALTH: {character['max_health']}",
            f"STRENGTH: {character['strength']}",
            f"MAGIC: {character['magic']}",
            f"EXPERIENCE: {character['experience']}",
            f"GOLD: {character['gold']}",
            f"INVENTORY: {','.join(character.get('inventory', []))}",
            f"ACTIVE_QUESTS: {','.join(character.get('active_quests', []))}",
            f"COMPLETED_QUESTS: {','.join(character.get('completed_quests', []))}"
        ]
        with open(filepath, "w") as file:
            file.write('\n'.join(lines))
        return True
    except (PermissionError, IOError):
        raise

 

def load_character(character_name, save_directory="data/save_games"): # loads character data from a file
    """
    Load character from save file
    
    Args:
        character_name: Name of character to load
        save_directory: Directory containing save files
    
    Returns: Character dictionary
    Raises: 
        CharacterNotFoundError if save file doesn't exist
        SaveFileCorruptedError if file exists but can't be read
        InvalidSaveDataError if data format is wrong
    """
    # TODO: Implement load functionality
    # Check if file exists → CharacterNotFoundError
    # Try to read file → SaveFileCorruptedError
    # Validate data format → InvalidSaveDataError
    # Parse comma-separated lists back into Python lists
    filename = f"{character_name}_save.txt"
    filepath = os.path.join(save_directory, filename)
    if not os.path.exists(filepath):
        raise CharacterNotFoundError
    try:
        with open(filepath, "r") as file:
            lines = file.readlines()
    except:
        raise SaveFileCorruptedError 
    character = {}
    try:
        for line in lines:
            key, value = line.strip().split(":", 1)
            key = key.strip().lower()
            value = value.strip()

            if "," in value:
                character[key] = value.strip().split(",")
            else:
                character[key] = value
    except:
        raise InvalidSaveDataError
    return character

def list_saved_characters(save_directory="data/save_games"): # lists all saved character names in the save directory
    """
    Get list of all saved character names
    
    Returns: List of character names (without _save.txt extension)
    """
    # TODO: Implement this function
    # Return empty list if directory doesn't exist
    # Extract character names from filenames
    if not os.path.isdir(save_directory):
        return []
    character_names = []
    for filename in os.listdir(save_directory):
        if filename.endswith("_save.txt"):
            name = filename[:-9]
            character_names.append(name)
    return character_names

def delete_character(character_name, save_directory="data/save_games"): # deletes a character's save file
    """
    Delete a character's save file
    
    Returns: True if deleted successfully
    Raises: CharacterNotFoundError if character doesn't exist
    """
    # TODO: Implement character deletion
    # Verify file exists before attempting deletion
    filename = f"{character_name}_save.txt"
    filepath = os.path.join(save_directory, filename)
    if not os.path.exists(filepath):
        raise CharacterNotFoundError
    os.remove(filepath)
    return True

# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount): # adds experience and handles level ups
    """
    Add experience to character and handle level ups
    
    Level up formula: level_up_xp = current_level * 100
    Example when leveling up:
    - Increase level by 1
    - Increase max_health by 10
    - Increase strength by 2
    - Increase magic by 2
    - Restore health to max_health
    
    Raises: CharacterDeadError if character health is 0
    """
    # TODO: Implement experience gain and leveling
    # Check if character is dead first
    # Add experience
    # Check for level up (can level up multiple times)
    # Update stats on level up
    if is_character_dead(character):
        raise CharacterDeadError
    character["experience"] += xp_amount

    while character["experience"] >= character["level"] * 100:
        character["experience"] -= character["level"] * 100
        character["level"] += 1
        character["max_health"] += 10
        character["strength"] += 2
        character["magic"] += 2
        character["health"] = character["max_health"]
    return character

def add_gold(character, amount): # this adds gold to the character's inventory
    """
    Add gold to character's inventory
    
    Args:
        character: Character dictionary
        amount: Amount of gold to add (can be negative for spending)
    
    Returns: New gold total
    Raises: ValueError if result would be negative
    """
    # TODO: Implement gold management
    # Check that result won't be negative
    # Update character's gold
    current_gold = character.get("gold", 0)
    new_gold = current_gold + amount
    if new_gold < 0:
        raise ValueError("Gold amount canot be negative")
    character["gold"] = new_gold
    return new_gold
    

def heal_character(character, amount): # heals the character by a specified amount
    """
    Heal character by specified amount
    
    Health cannot exceed max_health
    
    Returns: Actual amount healed
    """
    # TODO: Implement healing
    # Calculate actual healing (don't exceed max_health)
    # Update character health
    current_health = character.get("health", 0)
    max_health = character.get("max_health")
    healable_amount = max_health - current_health
    actual_healing = min(amount, healable_amount)

    character["health"] = current_health + actual_healing
    return actual_healing

def is_character_dead(character): # checks if the character is dead meaning health is 0 or below
    """
    Check if character's health is 0 or below
    
    Returns: True if dead, False if alive
    """
    # TODO: Implement death check
    return character.get("health", 0) <= 0

def revive_character(character): # revives a dead character with 50% health
    """
    Revive a dead character with 50% health
    
    Returns: True if revived
    """
    # TODO: Implement revival
    # Restore health to half of max_health
    if character.get("health", 1) > 0:
        return True
    max_health = character.get("max_health")
    if max_health is None:
        raise ValueError("charcater is missing 'max_health' attribute")
    character["health"] = max(1, max_health // 2)
    return True


# ============================================================================
# VALIDATION
# ============================================================================

def validate_character_data(character): # validates that the character data has all required fields and correct types
    """
    Validate that character dictionary has all required fields
    
    Required fields: name, class, level, health, max_health, 
                    strength, magic, experience, gold, inventory,
                    active_quests, completed_quests
    
    Returns: True if valid
    Raises: InvalidSaveDataError if missing fields or invalid types
    """
    # TODO: Implement validation
    # Check all required keys exist
    # Check that numeric values are numbers
    # Check that lists are actually lists
    required_feilds = {
        "name" : str,
        "class" : str,
        "level" : int,
        "health" : int,
        "max_health" : int,
        "strength" : int,
        "magic" : int,
        "experience" : int,
        "gold" : int,
        "inventory" : list,
        "active_quests" : list,
        "completed_quests" : list
    }
    for feild, expected_types in required_feilds.items():
        if feild not in character:
            raise InvalidSaveDataError
        if not isinstance(character[feild], expected_types):
            raise InvalidSaveDataError
    return True

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== CHARACTER MANAGER TEST ===")
    
    #Test character creation
    try:
         char = create_character("TestHero", "Warrior")
         print(f"Created: {char['name']} the {char['class']}")
         print(f"Stats: HP={char['health']}, STR={char['strength']}, MAG={char['magic']}")
    except InvalidCharacterClassError as e:
         print(f"Invalid class: {e}")
    
    # Test saving
    try:
        save_character(char)
        print("Character saved successfully")
    except Exception as e:
        print(f"Save error: {e}")
    
    # Test loading
    try:
        loaded = load_character("TestHero")
        print(f"Loaded: {loaded['name']}")
    except CharacterNotFoundError:
        print("Character not found")
    except SaveFileCorruptedError:
        print("Save file corrupted")

