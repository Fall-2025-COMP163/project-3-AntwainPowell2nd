"""
COMP 163 - Project 3: Quest Chronicles
Custom Exception Definitions

This module defines all custom exceptions used throughout the game.
"""

# ============================================================================
# BASE GAME EXCEPTIONS
# ============================================================================

class GameError(Exception): # the base exception for all game-related errors
    """Base exception for all game-related errors"""
    pass

class DataError(GameError): # the base exception for data-related errors
    """Base exception for data-related errors"""
    pass

class CharacterError(GameError): # the base exception for character-related errors
    """Base exception for character-related errors"""
    pass

class CombatError(GameError): # the base exception for combat-related errors
    """Base exception for combat-related errors"""
    pass

class QuestError(GameError): # the base exception for quest-related errors
    """Base exception for quest-related errors"""
    pass

class InventoryError(GameError): # the base exception for inventory-related errors
    """Base exception for inventory-related errors"""
    pass

# ============================================================================
# SPECIFIC EXCEPTIONS
# ============================================================================

# Data Loading Exceptions
class InvalidDataFormatError(DataError):
    """Raised when data file has incorrect format"""
    def __init__(self):
        super().__init__("data file has incorrect format")

class MissingDataFileError(DataError):
    """Raised when required data file is not found"""
    def __init__(self):
        super().__init__("required data file is not found")

class CorruptedDataError(DataError):
    """Raised when data file is corrupted or unreadable"""
    def __init__(self):
        super().__init__("data file is corrupted or unreadable")

# Character Exceptions
class InvalidCharacterClassError(CharacterError):
    """Raised when an invalid character class is specified"""
    def __init__(self):
        super().__init__("invalid character class is specified")

class CharacterNotFoundError(CharacterError):
    """Raised when trying to load a character that doesn't exist"""
    def __init__(self):
        super().__init__("character doesn't exist")

class CharacterDeadError(CharacterError):
    """Raised when trying to perform actions with a dead character"""
    def __init__(self):
        super().__init__("Cannot perform actions, character is dead")

class InsufficientLevelError(CharacterError):
    """Raised when character level is too low for an action"""
    def __init__(self):
        super().__init__("Character level is too low to perform action")

# Combat Exceptions
class InvalidTargetError(CombatError):
    """Raised when trying to target an invalid enemy"""
    def __init__(self):
        super().__init__("Cannot target, invalid enemy")

class CombatNotActiveError(CombatError):
    """Raised when trying to perform combat actions outside of battle"""
    def __init__(self):
        super().__init__("Not in an active battle")

class AbilityOnCooldownError(CombatError):
    """Raised when trying to use an ability that's on cooldown"""
    def __init__(self):
        super().__init__("Cannot use ability right now")

# Quest Exceptions
class QuestNotFoundError(QuestError):
    """Raised when trying to access a quest that doesn't exist"""
    def __init__(self):
        super().__init__("Quest does not exist")

class QuestRequirementsNotMetError(QuestError):
    """Raised when trying to start a quest without meeting requirements"""
    def __init__(self):
        super().__init__("Cannot Start quest you do not meet the requirements")

class QuestAlreadyCompletedError(QuestError):
    """Raised when trying to accept an already completed quest"""
    def __init__(self):
        super().__init__("Quest already complete")

class QuestNotActiveError(QuestError):
    """Raised when trying to complete a quest that isn't active"""
    def __init__(self):
        super().__init__("Quest isn't active")

# Inventory Exceptions
class InventoryFullError(InventoryError):
    """Raised when trying to add items to a full inventory"""
    def __init__(self):
        super().__init__("Inventory is full")

class ItemNotFoundError(InventoryError):
    """Raised when trying to use an item that doesn't exist"""
    def __init__(self):
        super().__init__("Item does not exist")  

class InsufficientResourcesError(InventoryError):
    """Raised when player doesn't have enough gold or items"""
    def __init__(self):
        super().__init__("You do not have enough gold")

class InvalidItemTypeError(InventoryError):
    """Raised when item type is not recognized"""
    def __init__(self):
        super().__init__("Item not recognized")

# Save/Load Exceptions
class SaveFileCorruptedError(GameError):
    """Raised when save file cannot be loaded due to corruption"""
    def __init__(self):
        super().__init__("Save File cannot be loaded due to corruption")

class InvalidSaveDataError(GameError):
    """Raised when save file contains invalid data"""
    def __init__(self):
        super().__init__("File contains invalid data")

