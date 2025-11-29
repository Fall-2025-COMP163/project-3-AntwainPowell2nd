"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles loading and validating game data from text files.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):
    """
    Load quest data from file
    
    Expected format per quest (separated by blank lines):
    QUEST_ID: unique_quest_name
    TITLE: Quest Display Title
    DESCRIPTION: Quest description text
    REWARD_XP: 100
    REWARD_GOLD: 50
    REQUIRED_LEVEL: 1
    PREREQUISITE: previous_quest_id (or NONE)
    
    Returns: Dictionary of quests {quest_id: quest_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    # TODO: Implement this function
    # Must handle:
    # - FileNotFoundError → raise MissingDataFileError
    # - Invalid format → raise InvalidDataFormatError
    # - Corrupted/unreadable data → raise CorruptedDataError
    quests = {}
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        raise MissingDataFileError
    except OSError:
        raise CorruptedDataError
    quest_blocks = [block.strip() for block in content.split("\n\n") if block.strip()]
    for block in quest_blocks: 
        quest_data = {}
        try:
            for line in block.splitlines():
                if ":" not in line:
                    raise InvalidDataFormatError
                key, value = line.split(":", 1)
                quest_data[key.strip()] = value.strip()
            required_keys = [
                "quest_id", "title", "description",
                "reward_xp", "reward_gold",
                "required_level", "prerequisite"
            ]
            for key in required_keys:
                if key not in quest_data: 
                    raise InvalidDataFormatError
            try:
                quest_data["reward_xp"] = int(quest_data["reward_xp"])
                quest_data["reward_gold"] = int(quest_data["reward_gold"])
                quest_data["required_level"] = int(quest_data["required_level"])
            except ValueError:
                raise InvalidDataFormatError
            quest_id = quest_data["quest_id"]
            quests[quest_id] = quest_data
        except Exception as e:
            if isinstance(e, (InvalidDataFormatError,)):
                raise
            else:
                raise CorruptedDataError
    return quests

    

def load_items(filename="data/items.txt"):
    """
    Load item data from file
    
    Expected format per item (separated by blank lines):
    ITEM_ID: unique_item_name
    NAME: Item Display Name
    TYPE: weapon|armor|consumable
    EFFECT: stat_name:value (e.g., strength:5 or health:20)
    COST: 100
    DESCRIPTION: Item description
    
    Returns: Dictionary of items {item_id: item_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    # TODO: Implement this function
    # Must handle same exceptions as load_quests
    if not os.path.exists(filename):
        raise MissingDataFileError
    try:
        with open(filename, "r") as file:
            data = file.read()
    except (OSError, IOError):
        raise CorruptedDataError
    items = {}
    raw_items = data.strip().split("\n\n")
    for section in raw_items:
        lines = section.strip().split("\n")
        item_content = {}
        try:
            for line in lines:
                key, value = line.split(":", 1)
                key = key.strip().upper()
                value = value.strip()

                if key == "ITEM_ID":
                    item_id = value
                elif key == "EFFECT":
                    stat, val = value.split(":")
                    item_content["EFFECT"] = {stat.strip(): int(val.strip())}
                elif key == "COST":
                    item_content["COST"] = int(value)
                else:
                    item_content[key] = value 
            if not item_id:
                raise InvalidDataFormatError
            items[item_id] = item_content
        except InvalidDataFormatError:
            raise InvalidDataFormatError
    return items

def validate_quest_data(quest_dict):
    """
    Validate that quest dictionary has all required fields
    
    Required fields: quest_id, title, description, reward_xp, 
                    reward_gold, required_level, prerequisite
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields
    """
    # TODO: Implement validation
    # Check that all required keys exist
    # Check that numeric values are actually numbers
    required_fields = [
        "quest_id", "title", "description",
        "reward_xp", "reward_gold",
        "required_level", "prerequisite"
    ]
    for field in required_fields:
        if field not in quest_dict:
            raise InvalidDataFormatError
    numeric_feilds = [
        "reward_xp", "reward_gold", 
        "required_level"
    ]
    for field in numeric_feilds:
        value = quest_dict[field]
        try:
            int(value)
        except (ValueError, TypeError):
            raise InvalidDataFormatError
    return True

def validate_item_data(item_dict):
    """
    Validate that item dictionary has all required fields
    
    Required fields: item_id, name, type, effect, cost, description
    Valid types: weapon, armor, consumable
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields or invalid type
    """
    # TODO: Implement validation
    required_fields = [
        "item_id", "name", "type",
        "effect", "cost", "description"
    ]
    valid_types = {"weapon", "armor", "consumable"}
    for field in required_fields:
        if field not in item_dict:
            raise InvalidDataFormatError
    item_type = item_dict["type"].lower()
    if item_type not in valid_types:
        raise InvalidDataFormatError
    try:
        int(item_dict["cost"])
    except (ValueError, TypeError):
        raise InvalidDataFormatError
    return True

def create_default_data_files():
    """
    Create default data files if they don't exist
    This helps with initial setup and testing
    """
    # TODO: Implement this function
    # Create data/ directory if it doesn't exist
    # Create default quests.txt and items.txt files
    # Handle any file permission errors appropriately
    data_dir = "data"
    quests_file = os.path.join(data_dir, "quests.txt")
    items_file = os.path.join(data_dir, "items.txt")
    try:
        if not os.path.exists(data_dir):
            os.makedirs(data_dir, exist_ok=True)
        if not os.path.exists(quests_file):
            with open(quests_file, "w", encoding="utf-8") as f:
                f.write(
                "QUEST_ID: quest_001\n"
                "TITLE: First Steps\n"
                "DESCRIPTION: Defeat 5 slimes in the forest.\n"
                "REWARD_XP: 100\n"
                "REWARD_GOLD: 50\n"
                "REQUIRED_LEVEL: 1\n"
                "PREREQUISITE: NONE\n\n"
                "QUEST_ID: quest_002\n"
                "TITLE: Goblin Trouble\n"
                "DESCRIPTION: Clear the goblin camp near the river.\n"
                "REWARD_XP: 250\n"
                "REWARD_GOLD: 100\n"
                "REQUIRED_LEVEL: 2\n"
                "PREREQUISITE: quest_001\n"
                )
        if not os.path.exists(items_file):
            with open(items_file, "w", encoding="utf-8") as f:
                f.write(
                "ITEM_ID: sword_001\n"
                "NAME: Iron Sword\n"
                "TYPE: weapon\n"
                "EFFECT: Deals extra damage to slimes\n"
                "COST: 150\n"
                "DESCRIPTION: A sturdy iron sword.\n\n"
                "ITEM_ID: potion_001\n"
                "NAME: Healing Potion\n"
                "TYPE: consumable\n"
                "EFFECT: Restores 50 HP\n"
                "COST: 50\n"
                "DESCRIPTION: A basic potion for adventurers.\n"
                )
    except PermissionError:
        raise PermissionError("Insufficient permissions to create data files.")



# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    """
    Parse a block of lines into a quest dictionary
    
    Args:
        lines: List of strings representing one quest
    
    Returns: Dictionary with quest data
    Raises: InvalidDataFormatError if parsing fails
    """
    # TODO: Implement parsing logic
    # Split each line on ": " to get key-value pairs
    # Convert numeric strings to integers
    # Handle parsing errors gracefully
    quest_data = {}
    for line in lines:
        try:
            if ":" not in line:
                raise InvalidDataFormatError(f"Line missing ':': {line}")
            
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            
            if value.isdigit():
                value = int(value)  
            
            quest_data[key] = value
        
        except ValueError as e:
            raise InvalidDataFormatError(f"Failed to parse line '{line}': {e}")

    return quest_data



def parse_item_block(lines):
    """
    Parse a block of lines into an item dictionary
    
    Args:
        lines: List of strings representing one item
    
    Returns: Dictionary with item data
    Raises: InvalidDataFormatError if parsing fails
    """
    # TODO: Implement parsing logic
    item_data = {}
    for line in lines:
        try:
            if ":" not in line:
                raise InvalidDataFormatError
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            try:
                value = int(value)
            except ValueError:
                pass  
            item_data[key] = value
        except Exception as e:
            raise InvalidDataFormatError(f"{e}")
    return item_data


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===")
    
    # Test creating default files
    create_default_data_files()
    
    # Test loading quests
    try:
        quests = load_quests()
        print(f"Loaded {len(quests)} quests")
    except MissingDataFileError:
        print("Quest file not found")
    except InvalidDataFormatError as e:
        print(f"Invalid quest format: {e}")
    
    # Test loading items
    try:
        items = load_items()
        print(f"Loaded {len(items)} items")
    except MissingDataFileError:
        print("Item file not found")
    except InvalidDataFormatError as e:
        print(f"Invalid item format: {e}")
    
quest = {
    "quest_id": "quest_001",
    "title": "First Steps",
    "description": "Defeat 5 slimes in the forest.",
    "reward_xp": 100,
    "reward_gold": 50,
    "required_level": 1,
    "prerequisite": "NONE"
}

try:
    if validate_quest_data(quest):
        print("Quest data is valid!")
except InvalidDataFormatError as e:
    print("Validation failed:", e)

item = {
    "item_id": "sword_001",
    "name": "Iron Sword",
    "type": "weapon",
    "effect": "Deals extra damage to slimes",
    "cost": 150,
    "description": "A sturdy iron sword."
}

try:
    if validate_item_data(item):
        print("Item data is valid!")
except InvalidDataFormatError as e:
    print("Validation failed:", e)

try:
    create_default_data_files()
    print("Default data files are ready!")
except PermissionError as e:
    print("Setup failed:", e)
lines = [
    "id: 101",
    "name: Rescue the Villager",
    "difficulty: 3",
    "reward: 50"
]

quest = parse_quest_block(lines)
print(quest)





