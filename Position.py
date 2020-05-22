# Positions identify individual cells on game boards.

def is_proper_position(dimension, position):
    """
        Check whether the given position is a proper position for any board
        with the given dimension.
        - The given position must be a tuple of length 2 whose elements are both
          natural numbers.
        - The first element identifies the column. It may not exceed the given
          dimension.
        - The second element identifies the row. It may not exceed the given
          dimension incremented with 1 (taking into account the overflow position)
        ASSUMPTIONS
        - None
    """
    # Controle van de voorwaarden voor position
    if len(position) != 2 or position != tuple(position):
        return False

    # Definieer de plaats van column en row in position
    column = position[0]
    row = position[1]

    # Controle van de voorwaarden voor column
    if column <= 0 or column > dimension or column != int(column):
        return False

    # Controle van de voorwaarden voor row
    elif row <= 0 or row > (dimension+1) or row != int(row):
        return False

    # Als alle voorwaarden zijn voldaan ==> return True
    else:
        return True


def is_overflow_position(dimension,position):
    """
        Check whether the given position is an overflow position for any board
        with the given dimension.
        - True if and only if the position is in the overflow row of the given board.
        ASSUMPTIONS
        - The given position is a proper position for any board with the
          given dimension.
    """
    if position == None:
        return False

    # Als het nummer van de rij gelijk is aan de  dimensie + 1 zit de positie in de overflowrij
    if position[1] == (dimension+1):
        return True
    else:
        return False


def left(dimension, position):
    """
        Return the position on any board with the given dimension immediately to
        the left of the given position.
        - None is returned if the generated position is outside the boundaries of
          a board with the given dimension.
        ASSUMPTIONS
        - The given position is a proper position for any board with the
          given dimension.
    """
    # Definieer de variabelen
    column = position[0]
    row = position[1]

    # Controle om te weten of de linkse positie mogelijk is
    if column >= 2:
        left_position = ((column-1),row)

    # Linkse positie is None als de linkse positie buiten het bord valt
    else:
        left_position = None

    return left_position

def right(dimension, position):
    """
       Return the position on any board with the given dimension immediately to
       the right of the given position.
       - None is returned if the generated position is outside the boundaries of
         a board with the given dimension.
       ASSUMPTIONS
       - The given position is a proper position for any board with the
         given dimension.
     """
    # Definieer de variabelen
    column = position[0]
    row = position[1]

    # Controle om te weten of de rechtse positie mogelijk is
    if column <= (dimension-1):
        right_position = ((column + 1), row)

    # Rechtse positie is None als de rechtse positie buiten het bord valt
    else:
        right_position = None

    return right_position


def up(dimension, position):
    """
        Return the position on any board with the given dimension immediately
        above the given position.
        - None is returned if the generated position is outside the boundaries of
          a board with the given dimension.
        ASSUMPTIONS
        - The given position is a proper position for any board with the
          given dimension.
     """
    # Definieer de variabelen
    column = position[0]
    row = position[1]

    # Controle om te weten of de bovenste positie mogelijk is
    if row <= (dimension):                                      # ==> Overflowrij moet ook kunnen
        up_position = (column, (row+1))

    # Bovenste positie is None als de bovenste positie buiten het bord valt
    else:
        up_position = None

    return up_position


def down(dimension, position):
    """
        Return the position on any board with the given dimension immediately
        below the given position.
        - None is returned if the generated position is outside the boundaries of
          a board with the given dimension.
        ASSUMPTIONS
        - The given position is a proper position for any board with the
          given dimension.
     """
    # Definieer de variabelen
    column = position[0]
    row = position[1]

    # Controle om te weten of de onderste positie mogelijk is
    if row >= 2:
        down_position = (column,(row-1))

    # Onderste positie is None als de onderste positie buiten het bord valt
    else:
        down_position = None

    return down_position


def next(dimension, position):
    """
        Return the position on any board with the given dimension next to the
        given position.
        - If the given position is not at the end of a row, the resulting position
          is immediately to the right of the given position.
        - If the given position is at the end of a row, the resulting position is
          the leftmost position of the row above. If that next row does not exist,
          None is returned.
        ASSUMPTIONS
        - The given position is a proper position for any board with the
          given dimension.
     """
    column = position[0]
    row = position[1]

    # next_position is rechts van de gegeven positie als dat binnen de grenzen van het bord valt:
    if column <= (dimension-1):
        next_position = right(dimension,position)

    else:
        # Als we verticaal gezien nog binnen de grenzen van het bord zijn is de volgende positie de meest linkse
        # op de volgende rij
        if row <= (dimension-1):
            next_position = (1,row+1)

        # Anders bestaat 'next_position' niet
        else:
            next_position = None

    return next_position


def get_all_adjacent_positions(dimension, positions):
    """
        Return a mutable set of all positions adjacent to at least one of the positions
        in the given collection of positions and within the boundaries of any board
        with the given dimension.
        ASSUMPTIONS
        - Each position in the given collection of positions is a proper position
          for any board with the given dimension.
    """

    # I.p.v. voorwaarden op te stellen voor bepaalde positities en welke 'adjacent' posities kunnen binnen de grenzen
    # van het bord, kunnen we gewoon alle posities toevoegen en dan verder alle 'None'-posities verwijderen uit de lijst
    huidige_pos = 0
    result_list = []

    while huidige_pos <= (len(positions) - 1):

        result_list.append(up(dimension, positions[huidige_pos]))
        result_list.append(down(dimension, positions[huidige_pos]))
        result_list.append(right(dimension, positions[huidige_pos]))
        result_list.append(left(dimension, positions[huidige_pos]))

        huidige_pos += 1

    # Verwijder de onmogelijke adjacent posities uit de resulterende lijst
    all_nones_gone = False

    while all_nones_gone == False:

        all_nones_gone = True

        for adjacent_positions in result_list:

            if adjacent_positions == None:

                result_list.remove(adjacent_positions)
                all_nones_gone = False

    # Verander de resulterende lijst in een 'mutable set'
    result_set = set(result_list)

    # Het resultaat is de resulterende, mutable set
    return result_set