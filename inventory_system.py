"""
COMP 163 - Project 3: Quest Chronicles
Inventory System Module - Starter Code

Name: [Aj]

AI Usage: [Document any AI assistance used]

This module handles inventory management, item usage, and equipment.
"""

from custom_exceptions import (
    InventoryFullError,
    ItemNotFoundError,
    InsufficientResourcesError,
    InvalidItemTypeError
)
from collections import Counter

# Maximum inventory size
MAX_INVENTORY_SIZE = 20

# ============================================================================
# INVENTORY MANAGEMENT
# ============================================================================
def get_numeric_value(file_path, target_key):#put in comment about AI help
    try:
        with open(file_path, "r") as file:
            for line in file:
                if line.startswith(target_key + ":"):
                    value = line.strip().split(":", 1)[1].strip()
                    if ":" in value:
                        return value.split(":", 1).strip()
                    else:
                        return value
    except FileNotFoundError:
        print(f"File not found {file_path}")
    return None
def get_name(file_path, target_key):
    try:
        with open(file_path, "r") as file:
            for line in file:
                if line.startswith(target_key + ":"):
                    value = line.strip().split(":", 1)[1].strip()
                    return value
    except FileNotFoundError:
        print(f"File not found {file_path}")
    return None

def add_item_to_inventory(character, item_id):
    """
    Add an item to character's inventory
    
    Args:
        character: Character dictionary
        item_id: Unique item identifier
    
    Returns: True if added successfully
    Raises: InventoryFullError if inventory is at max capacity
    """
    # TODO: Implement adding items
    # Check if inventory is full (>= MAX_INVENTORY_SIZE)
    # Add item_id to character['inventory'] list
    if len(character['inventory']) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError
    else:
        character['inventory'].append(item_id)
        return True

def remove_item_from_inventory(character, item_id):
    """
    Remove an item from character's inventory
    
    Args:
        character: Character dictionary
        item_id: Item to remove
    
    Returns: True if removed successfully
    Raises: ItemNotFoundError if item not in inventory
    """
    # TODO: Implement item removal
    # Check if item exists in inventory
    # Remove item from list
    if item_id in character['inventory']:
        character['inventory'].remove(item_id)
        return True
    else:
        raise ItemNotFoundError

def has_item(character, item_id):
    """
    Check if character has a specific item
    
    Returns: True if item in inventory, False otherwise
    """
    # TODO: Implement item check
    if item_id in character['inventory']:
        return True
    else:
        return False

def count_item(character, item_id):
    """
    Count how many of a specific item the character has
    
    Returns: Integer count of item
    """
    # TODO: Implement item counting
    # Use list.count() method
    return character['inventory'].count(item_id)

def get_inventory_space_remaining(character):
    """
    Calculate how many more items can fit in inventory
    
    Returns: Integer representing available slots
    """
    # TODO: Implement space calculation
    if len(character['inventory']) < MAX_INVENTORY_SIZE:
        return MAX_INVENTORY_SIZE - len(character['inventory']) 
    else:
        return 0 

def clear_inventory(character):
    """
    Remove all items from inventory
    
    Returns: List of removed items
    """
    # TODO: Implement inventory clearing
    # Save current inventory before clearing
    # Clear character's inventory list
    removed_items = character['inventory'][:]
    character['inventory'].clear()
    return removed_items

# ============================================================================
# ITEM USAGE
# ============================================================================

def use_item(character, item_id, item_data):
    """
    Use a consumable item from inventory
    
    Args:
        character: Character dictionary
        item_id: Item to use
        item_data: Item information dictionary from game_data
    
    Item types and effects:
    - consumable: Apply effect and remove from inventory
    - weapon/armor: Cannot be "used", only equipped
    
    Returns: String describing what happened
    Raises: 
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'consumable'
    """
    # TODO: Implement item usage
    # Check if character has the item
    # Check if item type is 'consumable'
    # Parse effect (format: "stat_name:value" e.g., "health:20")
    # Apply effect to character
    # Remove item from inventory
    if not has_item(character, item_id):
        raise ItemNotFoundError
    if item_data is None:
        raise ItemNotFoundError
    if item_data['type'] != "consumable": 
        raise InvalidItemTypeError
    stat_name, value = parse_item_effect(item_data["effect"])
    apply_stat_effect(character, stat_name, value)
    character['inventory'].remove(item_id)
    return f"{item_id} used to increase {stat_name} by {value}"

def equip_weapon(character, item_id, item_data):
    """
    Equip a weapon
    
    Args:
        character: Character dictionary
        item_id: Weapon to equip
        item_data: Item information dictionary
    
    Weapon effect format: "strength:5" (adds 5 to strength)
    
    If character already has weapon equipped:
    - Unequip current weapon (remove bonus)
    - Add old weapon back to inventory
    
    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'weapon'
    """
    # TODO: Implement weapon equipping
    # Check item exists and is type 'weapon'
    # Handle unequipping current weapon if exists
    # Parse effect and apply to character stats
    # Store equipped_weapon in character dictionary
    # Remove item from inventory
    if not has_item(character, item_id):
        raise ItemNotFoundError
    if item_data is None or item_data.get("type") != "weapon":
        raise InvalidItemTypeError
    old_weapon_id = unequip_weapon(character)
    stat, value = parse_item_effect(item_data["effect"])
    apply_stat_effect(character, stat, value)
    character["equipped_weapon"] = item_id
    character["equipped_weapon_effect"] = (stat, value)
    character["inventory"].remove(item_id)
def equip_armor(character, item_id, item_data):
    """
    Equip armor
    
    Args:
        character: Character dictionary
        item_id: Armor to equip
        item_data: Item information dictionary
    
    Armor effect format: "max_health:10" (adds 10 to max_health)
    
    If character already has armor equipped:
    - Unequip current armor (remove bonus)
    - Add old armor back to inventory
    
    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'armor'
    """
    # TODO: Implement armor equipping
    # Similar to equip_weapon but for armor
    inventory = character.get("inventory", [])

    if item_id not in inventory:
        raise ItemNotFoundError
    
    if item_data.get("type") != "armor":
        raise InvalidItemTypeError
    
    if character.get("equipped_armor"):
        old_armor = unequip_armor(character)

        old_itme_data = item_data.get("effects_removed", {})

        if "effect" in item_data:
            stat, value = item_data["effect"].split(":")
            character[stat] = character.get(stat, 0) - int(value)
    inventory.remove(item_id)
    character["equipped_armor"] = item_id

    effect = item_data.get("effect")
    if effect:
        try:
            stat, value = effect.split(":")
            character[stat] = character.get(stat, 0) + int(value)
        except ValueError:
            pass

    return f"Equipped {item_data.get("name", item_data)} as armor"

def unequip_weapon(character):
    """
    Remove equipped weapon and return it to inventory
    
    Returns: Item ID that was unequipped, or None if no weapon equipped
    Raises: InventoryFullError if inventory is full
    """
    # TODO: Implement weapon unequipping
    # Check if weapon is equipped
    # Remove stat bonuses
    # Add weapon back to inventory
    # Clear equipped_weapon from character
    weapon_id = character.get("equipped_weapon")
    if not weapon_id:
        return None
    if get_inventory_space_remaining(character) == 0:
        raise InventoryFullError
    effect = character.get("equipped_weapon_effect")
    if effect:
        stat, value = effect
        apply_stat_effect(character, stat, -value)
    character["inventory"].append(weapon_id)
    character["equipped_weapon"] = None
    character["equipped_weapon_effect"] = None
    return weapon_id

def unequip_armor(character):
    """
    Remove equipped armor and return it to inventory
    
    Returns: Item ID that was unequipped, or None if no armor equipped
    Raises: InventoryFullError if inventory is full
    """
    # TODO: Implement armor unequipping
    equipped_armor = character.get("equiped_armor")
    inventory = character.get("inventory", [])

    if not equip_armor:
        return None
    
    if len(inventory) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError
    
    inventory.append(equipped_armor)
    character["inventory"] = inventory
    character["equip_armor"] = None

    return equipped_armor

# ============================================================================
# SHOP SYSTEM
# ============================================================================

def purchase_item(character, item_id, item_data):
    """
    Purchase an item from a shop
    
    Args:
        character: Character dictionary
        item_id: Item to purchase
        item_data: Item information with 'cost' field
    
    Returns: True if purchased successfully
    Raises:
        InsufficientResourcesError if not enough gold
        InventoryFullError if inventory is full
    """
    # TODO: Implement purchasing
    # Check if character has enough gold
    # Check if inventory has space
    # Subtract gold from character
    # Add item to inventory
    gold = int(character.get("gold", 0))
    inventory = character.get("inventory", [])
    cost = int(item_data.get("cost", 0))

    if gold < cost:
        raise InsufficientResourcesError
    if len(inventory) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError
    
    character["gold"] -= cost
    inventory.append(item_id)
    character["inventory"] = inventory
    
    return True

def sell_item(character, item_id, item_data):
    """
    Sell an item for half its purchase cost
    
    Args:
        character: Character dictionary
        item_id: Item to sell
        item_data: Item information with 'cost' field
    
    Returns: Amount of gold received
    Raises: ItemNotFoundError if item not in inventory
    """
    # TODO: Implement selling
    # Check if character has item
    # Calculate sell price (cost // 2)
    # Remove item from inventory
    # Add gold to character
    inventory = character.get("inventory", [])
    gold = int(character.get("gold", 0))

    if item_id not in inventory:
        raise ItemNotFoundError
    
    cost = item_data.get("cost", 0)
    sell_price = cost // 2

    inventory.remove(item_id)
    character["inventory"] = inventory
    character["gold"] = gold + sell_price

    return sell_price
# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_item_effect(effect_string):
    """
    Parse item effect string into stat name and value
    
    Args:
        effect_string: String in format "stat_name:value"
    
    Returns: Tuple of (stat_name, value)
    Example: "health:20" → ("health", 20)
    """
    # TODO: Implement effect parsing
    # Split on ":"
    # Convert value to integer
    try:
        stat, val = effect_string.split(":")
        stat = stat.strip()
        val = int(val.strip())
        return stat, val
    except (ValueError, AttributeError):
        raise ValueError(f"Invalid Effect Format: {effect_string}")

    

def apply_stat_effect(character, stat_name, value):
    """
    Apply a stat modification to character
    
    Valid stats: health, max_health, strength, magic
    
    Note: health cannot exceed max_health
    """
    # TODO: Implement stat application
    # Add value to character[stat_name]
    # If stat is health, ensure it doesn't exceed max_health
    if stat_name not in ["health", "max_health", "strength", "magic"]:
        raise ValueError(f"Invalid stat name {stat_name}")
    character[stat_name] = character.get(stat_name, 0) + value
    if stat_name == "max_health":
        max_hp = character.get("max_health", 0)
        if character["health"] > max_hp:
            character["health"] = max_hp

def display_inventory(character, item_data_dict):
    """
    Display character's inventory in formatted way
    
    Args:
        character: Character dictionary
        item_data_dict: Dictionary of all item data
    
    Shows item names, types, and quantities
    """
    # TODO: Implement inventory display
    # Count items (some may appear multiple times)
    # Display with item names from item_data_dict
    inventory = character.get("inventory", [])
    if not inventory:
        print("Inventory is empty.")
        return
    item_counts = Counter(inventory)
    print("=== INVENTORY ===")
    for item_id, count in item_counts.items():
        item_info = item_data_dict.get(item_id, {})
        name = item_info.get("name", str(item_id))
        item_type = item_info.get("type", "Unknown")
        print(f"{name} ({item_type}) x{count}")
# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== INVENTORY SYSTEM TEST ===")
    
    # Test adding items
    test_char = {'inventory': [], 'gold': 100, 'health': 80, 'max_health': 80}
    # 
    try:
        add_item_to_inventory(test_char, "health_potion")
        print(f"Inventory: {test_char['inventory']}")
    except InventoryFullError:
        print("Inventory is full!")
    
    # Test using items
    test_item = {
        'item_id': 'health_potion',
        'type': 'consumable',
        'effect': 'health:20'
    }
    # 
    try:
        result = use_item(test_char, "health_potion", test_item)
        print(result)
    except ItemNotFoundError:
        print("Item not found")

