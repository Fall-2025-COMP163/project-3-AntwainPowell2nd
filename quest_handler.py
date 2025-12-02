"""
COMP 163 - Project 3: Quest Chronicles
Quest Handler Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles quest management, dependencies, and completion.
"""

from custom_exceptions import (
    QuestNotFoundError,
    QuestRequirementsNotMetError,
    QuestAlreadyCompletedError,
    QuestNotActiveError,
    InsufficientLevelError

)
import character_manager

# ============================================================================
# QUEST MANAGEMENT
# ============================================================================

def accept_quest(character, quest_id, quest_data_dict):
    """
    Accept a new quest
    
    Args:
        character: Character dictionary
        quest_id: Quest to accept
        quest_data_dict: Dictionary of all quest data
    
    Requirements to accept quest:
    - Character level >= quest required_level
    - Prerequisite quest completed (if any)
    - Quest not already completed
    - Quest not already active
    
    Returns: True if quest accepted
    Raises:
        QuestNotFoundError if quest_id not in quest_data_dict
        InsufficientLevelError if character level too low
        QuestRequirementsNotMetError if prerequisite not completed
        QuestAlreadyCompletedError if quest already done
    """
    # TODO: Implement quest acceptance
    # Check quest exists
    # Check level requirement
    # Check prerequisite (if not "NONE")
    # Check not already completed
    # Check not already active
    # Add to character['active_quests']
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError

    if quest_id in character.get("completed_quests", []):
        raise QuestAlreadyCompletedError

    if quest_id in character.get("active_quests", []):
        raise QuestNotActiveError

    quest = quest_data_dict[quest_id]
    level = int(character.get("level", 0))
    required_level = int(quest.get("required_level", 0))

    if level < required_level:
        raise InsufficientLevelError

    prereq = quest.get("prerequisite")
    if prereq and prereq != "NONE" and prereq not in character.get("completed_quests", []):
        raise QuestRequirementsNotMetError

    if not isinstance(character.get("active_quests"), list):
        character["active_quests"] = []
    character["active_quests"].append(quest_id)


    return True




 

    


def complete_quest(character, quest_id, quest_data_dict):
    """
    Complete an active quest and grant rewards
    
    Args:
        character: Character dictionary
        quest_id: Quest to complete
        quest_data_dict: Dictionary of all quest data
    
    Rewards:
    - Experience points (reward_xp)
    - Gold (reward_gold)
    
    Returns: Dictionary with reward information
    Raises:
        QuestNotFoundError if quest_id not in quest_data_dict
        QuestNotActiveError if quest not in active_quests
    """
    # TODO: Implement quest completion
    # Check quest exists
    # Check quest is active
    # Remove from active_quests
    # Add to completed_quests
    # Grant rewards (use character_manager.gain_experience and add_gold)
    # Return reward summary
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError
    if not is_quest_active(character, quest_id):
        raise QuestNotActiveError
    quest = quest_data_dict[quest_id]
    if not quest:
        raise QuestNotFoundError
    character["active_quests"].remove(quest_id)
    character.setdefault("completed_quests", []).append(quest_id)
    reward_xp = quest.get("reward_xp", 0)
    reward_gold = quest.get("reward_gold", 0)
    character_manager.gain_experience(character, reward_xp)
    character_manager.add_gold(character, reward_gold)
    totals = get_total_quest_rewards_earned(character, quest_data_dict)
    return totals


def abandon_quest(character, quest_id):
    """
    Remove a quest from active quests without completing it
    
    Returns: True if abandoned
    Raises: QuestNotActiveError if quest not active
    """
    # TODO: Implement quest abandonment
    active_quests = character.get("active_quests", [])
    if quest_id not in active_quests:
        raise QuestNotActiveError
    active_quests.remove(quest_id)
    character["active_quests"] = active_quests
    return True

def get_active_quests(character, quest_data_dict):
    """
    Get full data for all active quests
    
    Returns: List of quest dictionaries for active quests
    """
    # TODO: Implement active quest retrieval
    # Look up each quest_id in character['active_quests']
    # Return list of full quest data dictionaries
    active_quests = character.get("active_quests", [])
    result = []
    for quest_id in active_quests:
        quest = quest_data_dict.get(quest_id)
        if quest:
            result.append(quest)
    return result

def get_completed_quests(character, quest_data_dict):
    """
    Get full data for all completed quests
    
    Returns: List of quest dictionaries for completed quests
    """
    # TODO: Implement completed quest retrieval
    completed_quest = character.get("completed_quests", [])
    result = []
    for quest_id in completed_quest:
        quest = quest_data_dict.get(quest_id)
        if quest:
            result.append(quest)
    return result


def get_available_quests(character, quest_data_dict):
    """
    Get quests that character can currently accept
    
    Available = meets level req + prerequisite done + not completed + not active
    
    Returns: List of quest dictionaries
    """
    # TODO: Implement available quest search
    # Filter all quests by requirements
    avaliable_quests = []
    level = int(character.get("level", 0))
    active = set(character.get("active_quests", []))
    completed = set(character.get("completed_quests", []))
    for quest_id, quest in quest_data_dict.items():
        try:
            required_level = int(quest.get("required_level", 0))
            if level < required_level:
                continue

            if quest_id in active or quest_id in completed:
                continue

            prerequisite = quest.get("prerequisite", "NONE")
            if prerequisite and prerequisite != "NONE":
                if prerequisite not in completed:
                    continue
            
            avaliable_quests.append(quest)

        except (ValueError, TypeError):
            continue
    return avaliable_quests

# ============================================================================
# QUEST TRACKING
# ============================================================================

def is_quest_completed(character, quest_id):
    """
    Check if a specific quest has been completed
    
    Returns: True if completed, False otherwise
    """
    # TODO: Implement completion check
    return quest_id in character.get("completed_quests", [])


def is_quest_active(character, quest_id):
    """
    Check if a specific quest is currently active
    
    Returns: True if active, False otherwise
    """
    # TODO: Implement active check
    if quest_id not in character["active_quests"]:
        return False
    return True

def can_accept_quest(character, quest_id, quest_data_dict):
    """
    Check if character meets all requirements to accept quest
    
    Returns: True if can accept, False otherwise
    Does NOT raise exceptions - just returns boolean
    """
    # TODO: Implement requirement checking
    quest = quest_data_dict.get(quest_id)
    if not quest:
        return False

    try:
        required_level = int(quest.get("required_level", 0))
    except (TypeError, ValueError):
        return False

    if int(character.get("level", 0)) < required_level:
        return False

    prerequisite = quest.get("prerequisite")
    if prerequisite and prerequisite != "NONE":
        completed = character.get("completed_quests", [])
        if prerequisite not in completed:
            return False

    return True


def get_quest_prerequisite_chain(quest_id, quest_data_dict):
    """
    Get the full chain of prerequisites for a quest
    
    Returns: List of quest IDs in order [earliest_prereq, ..., quest_id]
    Example: If Quest C requires Quest B, which requires Quest A:
             Returns ["quest_a", "quest_b", "quest_c"]
    
    Raises: QuestNotFoundError if quest doesn't exist
    """
    # TODO: Implement prerequisite chain tracing
    # Follow prerequisite links backwards
    # Build list in reverse order
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError
    chain = []
    visited = ()
    current_id = quest_id
    while current_id:
        if current_id in visited:
            raise ValueError
        visited.add(current_id)
        quest = quest_data_dict.get(current_id)
        if not quest:
            raise QuestNotFoundError
        prerequisite = quest_data_dict.get("PREREQUISITE")
        if prerequisite:
            chain.insert(0, prerequisite)
        current_id = prerequisite
    chain.append(current_id)
    return chain


# ============================================================================
# QUEST STATISTICS
# ============================================================================

def get_quest_completion_percentage(character, quest_data_dict):
    """
    Calculate what percentage of all quests have been completed
    
    Returns: Float between 0 and 100
    """
    # TODO: Implement percentage calculation
    # total_quests = len(quest_data_dict)
    # completed_quests = len(character['completed_quests'])
    # percentage = (completed / total) * 100
    total_quests = len(quest_data_dict)
    complete_quests = len(character["completed_quests"])
    percentage = (complete_quests / total_quests) * 100
    return percentage

def get_total_quest_rewards_earned(character, quest_data_dict):
    """
    Calculate total XP and gold earned from completed quests
    
    Returns: Dictionary with 'total_xp' and 'total_gold'
    """
    # TODO: Implement reward calculation
    # Sum up reward_xp and reward_gold for all completed quests
    total_xp = 0
    total_gold = 0
    for quest_id in character.get("completed_quests", []):
        quest = quest_data_dict.get(quest_id)
        if quest:
            total_xp += quest.get("reward_xp")
            total_gold += quest.get("reward_gold")

    return {
        "total_xp" : total_xp,
        "total_gold" : total_gold
    }

    

def get_quests_by_level(quest_data_dict, min_level, max_level):
    """
    Get all quests within a level range
    
    Returns: List of quest dictionaries
    """
    # TODO: Implement level filtering
    return [
        quest for quest in quest_data_dict.values()
        if min_level <= quest.get("required_level", quest.get("REQUIRED_LEVEL", 0)) <= max_level
    ]


# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def display_quest_info(quest_data):
    """
    Display formatted quest information
    
    Shows: Title, Description, Rewards, Requirements
    """
    # TODO: Implement quest display
    print(f"\n=== {quest_data['title']} ===")
    print(f"Description: {quest_data['description']}")
    print(f"Rewards: {quest_data['rewards']}")
    print(f"Requirements: {quest_data['requirements']}")
    

def display_quest_list(quest_list):
    """
    Display a list of quests in summary format
    
    Shows: Title, Required Level, Rewards
    """
    # TODO: Implement quest list display
    if not quest_list:
        print("No quests avaliable")
        return
    print(f"{'Title':<30} {'Level':<10} {'Rewards'}")
    print("-" * 60)

    for quest in quest_list:
        title = quest.get("title", "unknown")
        level = quest.get("level", "N/A")
        rewards = ",".join(quest.get("rewards", []))
        print(f"{title:<30} {level:<10} {rewards}")
    

def display_character_quest_progress(character, quest_data_dict):
    """
    Display character's quest statistics and progress
    
    Shows:
    - Active quests count
    - Completed quests count
    - Completion percentage
    - Total rewards earned
    """
    # TODO: Implement progress display
    total_active_quests = len(character["active_quests"])
    total_completed_quests = len(character["completed_quests"])
    completion_percentage = get_quest_completion_percentage(character, quest_data_dict)
    total_rewards = []
    for quest_id in character["completed_quests"]:
        quest = quest_data_dict.get(quest_id)
        if quest and "rewards" in quest:
            total_rewards.extend(quest["rewards"])
    print("=== Quest Progress Summary ===")
    print(f"Active Quests: {total_active_quests}")
    print(f"Completed Quests: {total_completed_quests}")
    print(f"Completion: {completion_percentage:.2f}%")
    print(f"Total Rewards Earned: {', '.join(total_rewards) if total_rewards else 'None'}")





# ============================================================================
# VALIDATION
# ============================================================================

def validate_quest_prerequisites(quest_data_dict):
    """
    Validate that all quest prerequisites exist
    
    Checks that every prerequisite (that's not "NONE") refers to a real quest
    
    Returns: True if all valid
    Raises: QuestNotFoundError if invalid prerequisite found
    """
    # TODO: Implement prerequisite validation
    # Check each quest's prerequisite
    # Ensure prerequisite exists in quest_data_dict
    for quest_id, quest_data in quest_data_dict.items():
        prerequisite = quest_data.get("PREREQUISITE")
        if prerequisite and prerequisite != "None":
            if prerequisite not in quest_data_dict:
                raise QuestNotFoundError
    return True


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== QUEST HANDLER TEST ===")
    
    # Test data
    test_char = {
        'level': 1,
        'active_quests': [],
        'completed_quests': [],
        'experience': 0,
        'gold': 100
    }
    #
    test_quests = {
        'first_quest': {
            'quest_id': 'first_quest',
            'title': 'First Steps',
            'description': 'Complete your first quest',
            'reward_xp': 50,
            'reward_gold': 25,
            'required_level': 1,
            'prerequisite': 'NONE'
        }
    }
    #
    try:
        accept_quest(test_char, 'first_quest', test_quests)
        print("Quest accepted!")
    except QuestRequirementsNotMetError as e:
        print(f"Cannot accept: {e}")

