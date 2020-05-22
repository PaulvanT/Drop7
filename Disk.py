# Disks can be stored on the game board. They have a state
# and a number.
#  - Disks are mutable things. More in particular, it must be
#    possible to change the state of a disk.

# Enumeration of the possible states of a disk.
VISIBLE = 10
CRACKED = 20
WRAPPED = 30

import random


def is_proper_disk(dimension, disk):
    """
       Check whether the given disk is a proper disk for any board with
       the given dimension.
       - The state of the given disk must be one of the values VISIBLE,
         WRAPPED, CRACKED or some additional self-defined state.
       - The value of the given disk must be a positive integer number
         that does not exceed the dimension of the given board.
       ASSUMPTIONS
       - None
    """
    # Helpt voor lege posities in het deel 'Board.py':
    if disk == None or disk == str(disk):
        return False

# Deze functie moet 2 dingen controleren, deze twee controles verdelen we in twee subfuncties:

    # Controleer of de 'state' van de gegeven disk één van de 3 mogelijke 'states' is (voeg in deze lijst extra
    # waarden toe voor de 'self defined states':
    def is_proper_state(state):

        possible_states = (10,20,30)

        huidige_pos = 0
        while huidige_pos < len(possible_states):

            if state == possible_states[huidige_pos]:
                huidige_pos += len(possible_states)
                return True

            huidige_pos += 1

        return False

    # Controleer of de 'value' van de gegeven disk geldig is t.o.v. de gegeven dimensie
    def is_proper_value(dimension,value):

        if value > dimension:
            return False

        elif value <= 0:
            return False

        else:
            return True

    # Als beide functies 'True' zijn ==> is_proper_disk is ook True, anders niet:
    if is_proper_state(disk[0]) == True and is_proper_value(dimension,disk[1]) == True:
        return True

    else:
        return False


def init_disk(state, value):
    """
       Return a new disk with given state and given value.
       ASSUMPTIONS
       - None
    """
    disk = [state,value]

    return disk


def get_random_disk(dimension,possible_states):
    """
       Return a random disk for a board with the given dimension with
       a state that belongs to the collection of possible states.
       ASSUMPTIONS
       - The given dimension is positive.
       - The given collection of possible states is not empty and contains
         only elements VISIBLE, WRAPPED and/or CRACKED
    """

    # Maak een lege disk aan
    disk = []

    # Maak lijsten van de mogelijkheden zodat random.choice gebruikt kan worden (werkt niet met sets)
    possible_states = list(possible_states)
    possible_values = list(range(1,dimension))

    # Voeg op de eerste positie een random state toe en op de tweede positie een random value
    # (voor het random kiezen werd 'random' geïmporteerd (zie boven functie))
    disk.append(random.choice(possible_states))
    disk.append(random.choice(possible_values))
    return disk


def set_state(disk, state):
    """
        Set the state of the given disk to the given state.
        ASSUMPTIONS
        - The given disk is a proper disk for any board with a dimension at
          least equal to the value of the given disk.
    """
    disk[0] = state
    return disk


def get_state(disk):
    """
        Return the state of the given disk.
        ASSUMPTIONS
        - The given disk is a proper disk for any board with a dimension at
          least equal to the value of the given disk.
    """
    # Helpt bij de functie crack_disks_at in Board.py
    if disk == None:

        return None

    else:
        return disk[0]


def set_value(disk, value):
    """
        Set the value of the given disk to the given value.
        ASSUMPTIONS
        - The given disk is a proper disk for any board with a dimension at
          least equal to the value of the given disk.
    """
    disk[1] = value
    return disk


def get_value(disk):
    """
        Return the value of the given disk.
        ASSUMPTIONS
        - The given disk is a proper disk for any board with a dimension at
          least equal to the value of the given disk.
    """
    return disk[1]


def get_disk_copy(disk):
    """
        Return a new disk whose state and value are identical to the
        state and value of the given disk.
        ASSUMPTIONS
        - The given disk is a proper disk for any board with a dimension at
          least equal to the value of the given disk.
    """
    # Gebruik append om zo een nieuwe disk te maken i.p.v. 2 disks gelijk te stellen:
    disk_copy = []
    disk_copy.append(disk[0])
    disk_copy.append(disk[1])
    return disk_copy