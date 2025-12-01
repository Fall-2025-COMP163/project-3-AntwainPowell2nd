"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This is the main game file that ties all modules together.
Demonstrates module integration and complete game flow.
"""

# Import all our custom modules
import character_manager
import inventory_system
import quest_handler
import combat_system
import game_data
from custom_exceptions import *

# ============================================================================
# GAME STATE
# ============================================================================

# Global variables for game data
current_character = None
all_quests = {}
all_items = {}
game_running = False

# ============================================================================
# MAIN MENU
# ============================================================================

def main_menu():
    """
    Display main menu and get player choice
    
    Options:
    1. New Game
    2. Load Game
    3. Exit
    
    Returns: Integer choice (1-3)
    """
    # TODO: Implement main menu display
    # Show options
    # Get user input
    # Validate input (1-3)
    # Return choice
    print("Options:\n1. New Game\n2. Load Game\n3. Exit")
    user_input = input("Enter your choice (1-3): ")
    try:
        choice = int(user_input)
        if choice in [1, 2, 3]:
            return choice
        else:
            print("Invalid choice. Please select 1-3.")
            return main_menu()
    except ValueError:
        print("Invalid input. Please enter a number (1-3).")
        return main_menu()

def new_game():
    """
    Start a new game
    
    Prompts for:
    - Character name
    - Character class
    
    Creates character and starts game loop
    """
    global current_character
    
    # TODO: Implement new game creation
    # Get character name from user
    # Get character class from user
    # Try to create character with character_manager.create_character()
    # Handle InvalidCharacterClassError
    # Save character
    # Start game loop
    print("\nStarting a New Game...")
    name = input("Enter your character's name: ")
    print("Choose your character class:")
    print("1. Warrior\n2. Mage\n3. Rogue\n4. Cleric")
    class_choice = input("Enter the number of your choice: ")
    try:
        current_character = character_manager.create_character(name, class_choice)
        character_manager.save_character(current_character)
        print(f"Character '{name}' the {current_character['class']} created successfully!")
        game_loop(current_character)
    except InvalidCharacterClassError as e:
        print(f"Error: {e}")
        print("Please try creating your character again.")
        new_game()
    


def load_game():
    """
    Load an existing saved game
    
    Shows list of saved characters
    Prompts user to select one
    """
    global current_character
    
    # TODO: Implement game loading
    # Get list of saved characters
    # Display them to user
    # Get user choice
    # Try to load character with character_manager.load_character()
    # Handle CharacterNotFoundError and SaveFileCorruptedError
    # Start game loop
    print("\nLoading a Saved Game...")
    try:
        saved_characters = character_manager.list_saved_characters()
        if not saved_characters:
            print("No saved characters found. Please start a new game.")
            return

        while True:
            print("\nSaved Characters:")
            for idx, char_name in enumerate(saved_characters, start=1):
                print(f"{idx}. {char_name}")

            choice = input("Enter the number of the character to load: ").strip()

            try:
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(saved_characters):
                    char_name = saved_characters[choice_idx]
                    current_character = character_manager.load_character(char_name)
                    print(f"Character '{char_name}' loaded successfully!")
                    game_loop(current_character)
                    break 
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a valid number.")

    except (CharacterNotFoundError, SaveFileCorruptedError) as e:
        print(f"Error: {e}")
        print("Please try loading your character again.")
        load_game()  



# ============================================================================
# GAME LOOP
# ============================================================================

def game_loop():
    """
    Main game loop - shows game menu and processes actions
    """
    global game_running, current_character
    
    game_running = True
    
    # TODO: Implement game loop
    # While game_running:
    #   Display game menu
    #   Get player choice
    #   Execute chosen action
    #   Save game after each action
    while game_running:
        choice = game_menu()
        
        if choice == 1:
            view_character_stats()
        elif choice == 2:
            view_inventory()
        elif choice == 3:
            quest_menu()
        elif choice == 4:
            explore()
        elif choice == 5:
            shop()
        elif choice == 6:
            save_game()
            print("Game saved. Exiting to main menu.")
            game_running = False
        else:
            print("Invalid choice. Please select a valid option.")



def game_menu():
    """
    Display game menu and get player choice
    
    Options:
    1. View Character Stats
    2. View Inventory
    3. Quest Menu
    4. Explore (Find Battles)
    5. Shop
    6. Save and Quit
    
    Returns: Integer choice (1-6)
    """
    # TODO: Implement game menu
    print("\nGame Menu:")
    print("1. View Character Stats")
    print("2. View Inventory")
    print("3. Quest Menu")
    print("4. Explore (Find Battles)")
    print("5. Shop")
    print("6. Save and Quit")
    user_input = input("Enter your choice (1-6): ")
    try:
        choice = int(user_input)
        if choice in [1, 2, 3, 4, 5, 6]:
            return choice
        else:
            print("Invalid choice. Please select 1-6.")
            return game_menu()
    except ValueError:
        print("Invalid input. Please enter a number (1-6).")
        return game_menu()

# ============================================================================
# GAME ACTIONS
# ============================================================================

def view_character_stats():
    """Display character information"""
    global current_character
    
    # TODO: Implement stats display
    # Show: name, class, level, health, stats, gold, etc.
    # Use character_manager functions
    # Show quest progress using quest_handler
    if not current_character:
        print("No character loaded.")
        return
    
    print("\nCharacter Stats:")
    print(f"Name: {current_character.get('name', 'Unknown')}")
    print(f"Class: {current_character.get('class', 'Unknown')}")
    print(f"Level: {current_character.get('level', 1)}")
    print(f"Health: {current_character.get('health', 0)}/{current_character.get('max_health', 0)}")
    print(f"Gold: {current_character.get('gold', 0)}")
    print("Stats:")
    for stat, value in current_character.get('stats', {}).items():
        print(f"  {stat.capitalize()}: {value}")
    print("Active Quests:")
    try:
        active_quests = quest_handler.get_active_quests(current_character, all_quests)
        if active_quests:
            for quest in active_quests:
                name = quest.get('name', 'Unknown Quest')
                desc = quest.get('description', '')
                print(f"  - {name}: {desc}")
        else:
            print("  None")
    except Exception as e:
        print(f"  Error retrieving quests: {e}")


def view_inventory():
    """Display and manage inventory"""
    global current_character, all_items
    
    # TODO: Implement inventory menu
    # Show current inventory
    # Options: Use item, Equip weapon/armor, Drop item
    # Handle exceptions from inventory_system
    
    while True:
        print("\n=== Inventory Menu ===")
        
        if not current_character["inventory"]:
            print("Your inventory is empty.")
        else:
            for idx, item_id in enumerate(current_character["inventory"], start=1):
                item = all_items.get(item_id, {"name": "Unknown"})
                print(f"{idx}. {item['name']} ({item.get('type', 'unknown')})")

        print("\nOptions:")
        print("1. Use item")
        print("2. Equip weapon")
        print("3. Equip armor")
        print("4. Drop item")
        print("5. Exit inventory")
        
        choice = input("Select an option: ").strip()
        
        try:
            if choice == "1":  
                idx = int(input("Enter item number to use: ")) - 1
                item_id = current_character["inventory"][idx]
                item_data = all_items.get(item_id)
                
                result = inventory_system.use_item(current_character, item_id, item_data)
                print(result)
            
            elif choice == "2":  # Equip weapon
                idx = int(input("Enter item number to equip as weapon: ")) - 1
                item_id = current_character["inventory"][idx]
                item_data = all_items.get(item_id)
                
                result = inventory_system.equip_weapon(current_character, item_id, item_data)
                print(result if result else f"Equipped {item_data['name']} as weapon.")
            
            elif choice == "3":  # Equip armor
                idx = int(input("Enter item number to equip as armor: ")) - 1
                item_id = current_character["inventory"][idx]
                item_data = all_items.get(item_id)
                
                result = inventory_system.equip_armor(current_character, item_id, item_data)
                print(result)
            
            elif choice == "4":  # Drop item
                idx = int(input("Enter item number to drop: ")) - 1
                item_id = current_character["inventory"][idx]
                
                result = inventory_system.remove_item_from_inventory(current_character, item_id)
                print(result)
            
            elif choice == "5":
                print("Exiting inventory...")
                break
            
            else:
                print("Invalid choice. Try again.")
        
        except (ValueError, IndexError):
            print("Invalid item selection.")
        except Exception as e:
            print(f"Error: {e}")


def quest_menu():
    """Quest management menu"""
    global current_character, all_quests
    
    # TODO: Implement quest menu
    # Show:
    #   1. View Active Quests
    #   2. View Available Quests
    #   3. View Completed Quests
    #   4. Accept Quest
    #   5. Abandon Quest
    #   6. Complete Quest (for testing)
    #   7. Back
    # Handle exceptions from quest_handler
    while True:
        print("\n=== Quest Menu ===")
        print("1. View Active Quests")
        print("2. View Available Quests")
        print("3. View Completed Quests")
        print("4. Accept Quest")
        print("5. Abandon Quest")
        print("6. Complete Quest (for testing)")
        print("7. Back")
        
        choice = input("Select an option: ").strip()
        
        try:
            if choice == "1":
                active_quests = quest_handler.get_active_quests(current_character, all_quests)
                if active_quests:
                    print("\nActive Quests:")
                    for quest in active_quests:
                        print(f"- {quest['name']}: {quest['description']}")
                else:
                    print("No active quests.")
            
            elif choice == "2":
                available_quests = quest_handler.get_available_quests(current_character, all_quests)
                if available_quests:
                    print("\nAvailable Quests:")
                    for quest in available_quests:
                        print(f"- {quest['name']}: {quest['description']}")
                else:
                    print("No available quests.")
            
            elif choice == "3":
                completed_quests = quest_handler.get_completed_quests(current_character, all_quests)
                if completed_quests:
                    print("\nCompleted Quests:")
                    for quest in completed_quests:
                        print(f"- {quest['name']}: {quest['description']}")
                else:
                    print("No completed quests.")
            
            elif choice == "4":
                quest_name = input("Enter the name of the quest to accept: ").strip()
                result = quest_handler.accept_quest(current_character, quest_name, all_quests)
                print(result)
            
            elif choice == "5":
                quest_name = input("Enter the name of the quest to abandon: ").strip()
                result = quest_handler.abandon_quest(current_character, quest_name)
                print(result)
            
            elif choice == "6":
                quest_name = input("Enter the name of the quest to complete: ").strip()
                result = quest_handler.complete_quest(current_character, quest_name, all_quests)
                print(result)
            
            elif choice == "7":
                print("Exiting quest menu...")
                break
            
            else:
                print("Invalid choice. Try again.")
        
        except Exception as e:
            print(f"Error: {e}")

def explore():
    """Find and fight random enemies"""
    global current_character
    
    # TODO: Implement exploration
    # Generate random enemy based on character level
    # Start combat with combat_system.SimpleBattle
    # Handle combat results (XP, gold, death)
    # Handle exceptions
    try:
        print("\nExploring the world...")
        enemy = combat_system.generate_random_enemy(current_character['level'])
        print(f"You encountered a {enemy['name']}!")
        battle = combat_system.simple_battle(current_character, enemy)
        battle_result = battle.start_battle()
        if battle_result["winner"] == "player":
            rewards = combat_system.get_victory_rewards(enemy) 
            current_character["xp"] = current_character.get("xp", 0) + rewards["xp"]
            current_character["gold"] = current_character.get("gold", 0) + rewards["gold"]
            
            print(f"You defeated {enemy['name']}! "
                  f"Gained {rewards['xp']} XP and {rewards['gold']} gold.")
        
        elif battle_result["winner"] == "enemy":
            print(f"You were defeated by {enemy['name']}...")
            handle_character_death(current_character)

    except Exception as e:
        print(f"Error during exploration: {e}")
    

def shop():
    """Shop menu for buying/selling items"""
    global current_character, all_items
    
    # TODO: Implement shop
    # Show available items for purchase
    # Show current gold
    # Options: Buy item, Sell item, Back
    # Handle exceptions from inventory_system
    while True:
        print("\n=== Shop Menu ===")
        print(f"Your Gold: {current_character.get('gold', 0)}")
        
        print("\nItems for Sale:")
        for item_id, item in all_items.items():
            cost = item.get("cost", 0)
            print(f"- {item_id}: {item.get('name', 'Unknown')} ({item.get('type', 'unknown')}) - {cost} gold")
        
        print("\nOptions:")
        print("1. Buy item")
        print("2. Sell item")
        print("3. Back")
        
        choice = input("Select an option: ").strip()
        
        try:
            if choice == "1": 
                item_id = input("Enter item ID to buy: ").strip()
                item_data = all_items.get(item_id)
                
                if not item_data:
                    print("Item not found in shop.")
                    continue
                
                result = inventory_system.purchase_item(current_character, item_id, item_data)
                print(result)
            
            elif choice == "2":  
                result = inventory_system.sell_item(current_character, all_items)
                print(result)
            
            elif choice == "3":  # Back
                print("Leaving the shop...")
                break 
            
            else:
                print("Invalid choice. Try again.")
        
        # --- Exception Handling ---
        except ItemNotFoundError as e:
            print(f"Item not found: {e}")
        except InventoryFullError as e:
            print(f"Inventory full: {e}")
        except ValueError:
            print("Invalid input.")
        except Exception as e:
            print(f"Unexpected error: {e}")    

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def save_game():
    """Save current game state"""
    global current_character
    
    # TODO: Implement save
    # Use character_manager.save_character()
    # Handle any file I/O exceptions
    pass

def load_game_data():
    """Load all quest and item data from files"""
    global all_quests, all_items
    
    # TODO: Implement data loading
    # Try to load quests with game_data.load_quests()
    # Try to load items with game_data.load_items()
    # Handle MissingDataFileError, InvalidDataFormatError
    # If files missing, create defaults with game_data.create_default_data_files()
    pass

def handle_character_death():
    """Handle character death"""
    global current_character, game_running
    
    # TODO: Implement death handling
    # Display death message
    # Offer: Revive (costs gold) or Quit
    # If revive: use character_manager.revive_character()
    # If quit: set game_running = False
    pass

def display_welcome():
    """Display welcome message"""
    print("=" * 50)
    print("     QUEST CHRONICLES - A MODULAR RPG ADVENTURE")
    print("=" * 50)
    print("\nWelcome to Quest Chronicles!")
    print("Build your character, complete quests, and become a legend!")
    print()

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main game execution function"""
    
    # Display welcome message
    display_welcome()
    
    # Load game data
    try:
        load_game_data()
        print("Game data loaded successfully!")
    except MissingDataFileError:
        print("Creating default game data...")
        game_data.create_default_data_files()
        load_game_data()
    except InvalidDataFormatError as e:
        print(f"Error loading game data: {e}")
        print("Please check data files for errors.")
        return
    
    # Main menu loop
    while True:
        choice = main_menu()
        
        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            print("\nThanks for playing Quest Chronicles!")
            break
        else:
            print("Invalid choice. Please select 1-3.")

if __name__ == "__main__":
    main()

