# Boards are square areas of N rows and N columns.
#     - Rows and columns in boards are numbered starting from 1.

import Disk
import Position

def is_proper_board(board):
    """
        Check whether the given board is a proper board. The function
        returns true if all the conditions below are satisfied:
        - The given board may not be None, and its dimension
          must be a natural number.
        - Each cell of the given board either stores nothing (None),
          or it stores a proper disk for the given board.
        ASSUMPTIONS
        - None
    """
    # Deze hulpfunctie wordt iets verder in de code gebruik om te kijken
    # of alle kolommen 'proper disks' bevatten of None's:
    def all_columns_are_proper(board):

        dimension = board[0]
        huidige_pos = 0

        while huidige_pos <= (dimension-1):

            for i in range(dimension):

                #Elke cel moet ofwel een 'proper disk' bevatten of None zijn:
                if Disk.is_proper_disk(dimension, ((board[1])[huidige_pos])[i]) == True \
                        or ((board[1])[huidige_pos])[i] == None:

                    return True
                else:
                    return False

            huidige_pos += 1

    # Voorwaarde 1 (Deel 1): Onmiddellijk False als board == None:
    if board == None or board == str(board):

        return False

    # Voorwaarde 2: Elke cel bevat ofwel een 'proper disk' of een 'None' (= lege cel):
    dimension = board[0]

    for i in range(dimension-1):

        # Voorwaarde 1 (Deel 2): Dimensie moet een natuurlijk getal zijn:
        if dimension != int(dimension) or dimension <= 0:

            return False

        # Het bord moet vol kolommen zijn:
        elif len(board[1]) != dimension:

            return False

        # Deze kolommen moeten op hun beurt vol met disks zijn of None's bevatten (zie boven voor functie):
        elif all_columns_are_proper(board) == False:

            return False

        else:
            return True


def is_playable_board(board):
    """
        Check whether the given board is a playable board. The function
        returns true if all the conditions below are satisfied:
        - The given board is a proper board.
        - If a cell stores a disk, all cells below also store
          a disk (i.e. there are no gaps in columns).
        - The same disk is not stored at several positions on the given board.
        ASSUMPTIONS
        - None
    """
    dimension = board[0]
    result = True

    # Voorwaarde 1: Het gegeven bord moet een 'proper' bord zijn:
    if is_proper_board(board) == False:

        result = False

    else:

        current_column = 0

        # Voorwaarde 2: Dit stuk zal nagaan of er ergens op het bord een disk bestaat met daaronder een 'None',
        # als dit waar is returned de functie False, anders True
        while current_column <= (dimension - 1):

            current_row = 1

            while current_row <= dimension:         #Overflowrij meerekenen (dus '<= dimension' i.p.v. '<= (dimension - 1)')

                if ((board[1])[current_column])[current_row] != None:

                    if ((board[1])[current_column])[current_row-1] == None:

                        current_row += dimension
                        current_column += dimension
                        result = False

                    else:
                        result = True

                current_row += 1

            current_column += 1

        # Voorwaarde 3: Dit stuk zal nagaan of het bord twee (of meerdere keren) dezelfde disk bevat
        column = 0

        while column <= (dimension - 1):

            for i in range(dimension):

                for j in range(dimension):

                    # We gebruiken 'is' en niet '==' omdat gelijke disks mogen, maar niet 1 disk op meerdere posities

                    if ((board[1])[column])[i] is ((board[1])[column])[j] and i != j \
                            and ((board[1])[column])[i] != None and ((board[1])[column])[j] != None:

                        result = False
                        break
            column += 1

    return result


def init_board(dimension, given_disks=()):
    """
        Return a new board with given dimension and filled with the given disks.

        - The collection of given disks is a sequence. The element at position I
          in that sequence specifies the disks to be loaded on column I+1 of the
          new board.
        - If there is no matching element for a column, no disks are loaded on
          that column.
        ASSUMPTIONS
        - The given dimension is a positive integer number.
        - The number of elements in the sequence of given disks is between 0
          and the given dimension.
        - Each element of the given sequence of disks is a sequence of
          disks for the new board. The length of each sequence of disks
          is less than or equal to the given dimension incremented with 1.
          Each disk must be a proper disk for the given board.
        NOTE
        - Notice that the resulting board will be a proper board, but not
          necessarily a playable board. Notice also that some disks on the board
          might satisfy the conditions to explode.
    """
    huidige_pos = 0
    board = []

    # De bedoeling is om de gegeven disks op het bord te plaatsen en daarna alle lege cellen
    # te vullen met 'None' om zo een 'proper' bord te verkrijgen:

    # Gegeven kolommen aanvullen met lege disks tot als de kolommen vol zijn (Overflowrij meegerekend).
    while huidige_pos <= len(given_disks)-1:

        current_column = list(given_disks[huidige_pos])

        while len(current_column) <= dimension:

            current_column.append(None)

        board.append(current_column)
        huidige_pos += 1

    # Als er te weinig kolommen gegeven zijn ==> voeg lege kolommen toe tot het bord vol is:
    if len(board) < dimension:

        while len(board) != dimension:

            new_empty_column = []

            while len(new_empty_column) < (dimension+1):

                new_empty_column.append(None)

            board.append(new_empty_column)

    return [dimension,board]


def get_board_copy(board):
    """
      Return a full copy of the given board.
      - The resulting copy contains copies of the disks stored
         on the original board.
      ASSUMPTIONS
      - The given board is a proper board.
    """
    board_copy = []
    current_column = 0

    while current_column <= (dimension(board)-1):

        column_copy = []
        current_row = 0

        while current_row <= dimension(board):

            # Als de huidige positie (= (current_column+1,current_row+1) 'None' bevat, voegen we None toe aan de huidige kolom
            if ((board[1])[current_column])[current_row] == None:

                column_copy.append(None)

            # Als de huidige positie een disk bevat, creëren we een kopie van deze disk m.b.v. de append-functie
            else:
                disk_copy = []

                # State toevoegen aan kopie van huidige disk
                disk_copy.append((((board[1])[current_column])[current_row])[0])

                # Value toevoegen aan kopie van huidige disk
                disk_copy.append((((board[1])[current_column])[current_row])[1])

                # Kopie van huidige disk toevoegen aan kopie van huidige kolom
                column_copy.append(disk_copy)

            current_row += 1

        # Kopie van de huidige kolom toevoegen aan kopie van het bord
        board_copy.append(column_copy)

        current_column += 1

    # Kopie van het bord returnen zonder de dimensie te vergeten!
    return [dimension(board),board_copy]


def dimension(board):
    """
        Return the dimension of the given board.
        - The dimension of a square board is its number of rows or equivalently
          its number of columns.
        - The function returns None if no dimension can be obtained from the given
          board. This is for instance the case if a string, a number, ... is passed
          instead of a board.
        ASSUMPTIONS
        - None (we must be able to use this function at times the thing that
          is given to us is not necessarily a proper board, e.g. in the function
          is_proper_board itself)
    """
    if board == str(board):

        dimension = None

    # Dit kon ook met dimension = board[0], maar de uitleg van de functie specifieert dat de dimensie de lengte van
    # het aantal kolommen of rijen moet zijn:
    else:
        dimension = len(board[1])

    return dimension


def get_disk_at(board, position):
    """
        Return the disk at the given position on the given board.
        - None is returned if there is no disk at the given position.
        - The function also returns None if no disk can be obtained from the given
          board at the given position. This is for instance the case if a string,
          a number, ... is passed instead of a board or a position, if the given
          position is outside the boundaries of the given board, ...
        ASSUMPTIONS
        - None (same remark as for the function dimension)
     """

    # Gegeven bord moet tenminste uit een leesbaar formaat bestaan voor schijven:
    if board == str(board) or board == None:

        disk = None

    elif position == None or len(position) == 1:

        disk = None

    # Gegeven positie moet getallen bevatten:
    elif position[0] == str(position[0]):

        disk = None

    elif position[1] == str(position[1]):

        disk = None

    # Element in given_disks op positie I behoort tot kolom I+1 enzovoort:
    else:
        disk = ((board[1])[(position[0]-1)])[(position[1]-1)]

    return disk


def set_disk_at(board, position, disk):
    """
        Fill the cell at the given position on the given board with the given disk.
        - The disk nor any other disk will yet explode, even if the conditions
          for having an explosion are satisfied.
        - The given disk may be None, in which case the disk, if any, at the given
          position is removed from the given board, WITHOUT disks at higher positions
          in the column dropping down one position.
        ASSUMPTIONS
        - The given board is a proper board, the given position is a proper
          proper position for the given board and the given disk is a proper
          disk for the given board.
    """

    # Aangezien borden 'mutable lists' zijn, kunnen we gewoonweg
    # de disk op de gegeven positie vervangen door de nieuwe disk
    ((board[1])[position[0]-1])[position[1]-1] = disk

    return board


def has_disk_at(board, position):
    """
        Check whether a disk is stored at the given position on the given board.
        - The function returns false if no disk can be obtained from the given
          board at the given position.
        ASSUMPTIONS
        - The given board is a proper board and the given position is a
          proper position for that board.
    """

    # Aangezien het bord een proper bord is, kan een cel enkel 'None' of een 'proper disk' bevatten,
    # ==> Als een cel 'None' bevat op de gegeven positie: return False, anders is het sowieso een 'proper disk' (return True)
    if get_disk_at(board,position) == None:

        return False

    else:
        return True


def is_full_column(board, column):
    """
       Check whether the non-overflow part of the given column on the given board
       is completely filled with disks.
       - The overflow cell of a full column may also contain a disk, but it may
         also be empty.
        ASSUMPTIONS
        - The given board is a proper board, and the given column is a proper column
          for that board.
    """
    huidige_pos = 1
    column = int(column)

    # Elke positie van de gegeven kolom wordt gecontroleerd met de functie 'has_disk_at':
    while huidige_pos <= dimension(board):                              # Overflowrij moeten we niet controleren

        if has_disk_at(board,(column,huidige_pos)) == True:

            huidige_pos += 1
            result = True

        else:
            result = False
            break

    return result

def is_full(board):                                                                                                                                                                                                                                                                                                                                                                                                                                                     
    """
       Check whether the non-overflow part of the  given board is completely
       filled with disks.
        ASSUMPTIONS
        - The given board is a proper board.
    """
    huidige_pos = 1

    # Elke kolom van het gegeven bord wordt gecontroleerd met de functie'is_full_column':
    while huidige_pos <= dimension(board):

        if is_full_column(board,huidige_pos) == True:

            huidige_pos += 1
            result = True

        else:
            huidige_pos += dimension(board)
            result = False

    return result

def can_accept_disk(board):
    """
        Check whether the given board can accept an additional disk.
        - True if and only if (1) all overflow cells of the given board are free,
          and (2) at least one of the cells in the non-overflow portion of the
          given board is free.
        ASSUMPTIONS
        - The given board is a proper board.

    """
    # Hulpfunctie om voorwaarde (1) te controleren:
    def is_overflow_row_empty(board):

        for i in range(0,(dimension(board)-1)):

            if ((board[1])[i])[dimension(board)] == None:

                return True
            else:
                return False

    # Hulpfunctie om voorwaarde (2) te controleren:
    # ==> deze hebben we eerder al geschreven, nl. 'is_full(board)'.

    # Als beide voorwaarden zijn voldaan ==> return True
    if is_overflow_row_empty(board) == True and is_full(board) == False:

        return True
    else:
        return False


def add_disk_on_column(board, disk, column):
    """
        Add the given disk on top of the given column of the given board.
        - The disk is registered at the lowest free position in the given column.
          Nothing happens if the given column is completely filled, including the
          overflow cell of that column.
        - The disk nor any other disk will yet explode, even if the conditions for
          having an explosion are satisfied.
        ASSUMPTIONS
        - The given board is a proper board, the given column is a proper column
          for the given board, and the given disk is a proper disk for the given board.
    """
    # We beginnen vanaf beneden in de gegeven kolom: Als een cel 'None' bevat voegen we de gegeven disk toe,
    # anders gebeurt er niets.

    current_row = 1

    while current_row <= (dimension(board)+1):                  # Rekening houden met de overflowrij

        if get_disk_at(board,(column,current_row)) == None:

            set_disk_at(board,(column,current_row), disk)
            current_row += (dimension(board)+1)

        else:
            current_row += 1


def inject_disk_in_column(board, disk, column):
    """
        Inject the given disk at the bottom of the given column of the given board.
        - The disk is registered in the bottom cell of the given column, i.e., in the
          cell at row 1.
        - All disks already in the given column are shifted up one position.
        ASSUMPTIONS
        - The given board is a proper board, the given column is a proper column
          for that board whose overflow cell is free, and the given disk is a
          proper disk for the given board.
    """

    # We beginnen vanboven en gaan naar beneden in de gegeven kolom
    current_row = dimension(board)

    while current_row > 0:

        # Zolang de kolom leeg is (van boven naar beneden) verplaatsen we geen disks
        if get_disk_at(board,(column,current_row)) == None:

            current_row -= 1

        else:
            # We vervangen de disk boven de huidige disk met de huidige disk en zetten er een 'None' in de plaats
            ((board[1])[column - 1])[current_row] = ((board[1])[column-1])[current_row - 1]
            ((board[1])[column - 1])[current_row - 1] = None

    # Eens alle disks 1 positie naar boven zijn verplaatst kunnen we vanonder de gegeven disk toevoegen

    add_disk_on_column(board,disk,column)   # In deze functie beginnen we van beneden ==> als de onderste cel leeg is (None)
                                            # zal de disk daar geplaatst worden


def inject_bottom_row_wrapped_disks(board):
    """
        Insert a bottom row of wrapped disks in the given board.
        - All disks already in the board are shifted up one position.
        - No disk on the given board will explode yet, even if the conditions
          for having an explosion are satisfied.
        ASSUMPTIONS
        - The given board is a playable board that can accept a disk.
    """
    column = 1

    # We gaan van links naar rechts op vlak van kolommen en bewegen in elke kolom elke disk 1 positie naar boven
    # en voegen vanonder een 'wrapped disk' toe met willekeurige 'value':
    while column <= dimension(board):

        inject_disk_in_column(board, Disk.get_random_disk(dimension(board), (Disk.WRAPPED, )), column)
        column += 1

def remove_disk_at(board, position):
    """
        Remove the disk at the given position from the given board.
        - All disks above the removed disk drop one position down.
        - Nothing happens if no disk is stored at the given position.
        - No disk will explode yet, even if the conditions for having an
          explosion are satisfied.
        ASSUMPTIONS
        - The given board is a proper board, and the given position is
          a proper position for that board.
        NOTE
        - This function must be implemented in a RECURSIVE way.
    """
    # Er gebeurt niets als de cel op gegeven positie leeg is
    if get_disk_at(board,position) == None:

        return

    else:

        # Definieer positie boven de huidige bekeken positie
        position_above = Position.up(dimension(board), position)

        # Als er geen disks meer zijn om te laten vallen voegen we 'None' (lege cel) toe aan
        # de bovenkant van de kolom schijven, waar vroeger de bovenste schijf was
        if get_disk_at(board,position_above) == None :

            set_disk_at(board, position, None)

        # Als er nog schijven zijn om te laten vallen, laten we ze 'vallen' door telkens de huidig bekeken schijf te
        # vervangen met de schijf daar juist boven
        else:
            set_disk_at(board,position,get_disk_at(board,position_above))
            remove_disk_at(board,position_above)                            #Recursief deel

# _______________________________________________________________________________________________________

# RECURSIEVE HULPFUNCTIES voor de functies 'get_length_vertical_chain' en 'get_length_horizontal_chain':
# _______________________________________________________________________________________________________

def count_disks_above(board,position):
    """
       Telt het aantal schijven boven de gegeven positie op een recursieve manier
    """

    if get_disk_at(board,position) == None or Position.is_proper_position(dimension(board),position) == False:

        return 0

    else:
        position_above = Position.up(dimension(board),position)
        result = 1 + count_disks_above(board,position_above)
        return result


def count_disks_below(board,position):
    """
       Telt het aantal schijven onder de gegeven positie op een recursieve manier
    """

    if get_disk_at(board, position) == None or Position.is_proper_position(dimension(board),position) == False:

        return 0

    else:
        position_below = Position.down(dimension(board), position)
        result = 1 + count_disks_below(board, position_below)
        return result


def count_disks_left(board,position):
    """
       Telt het aantal schijven links van de gegeven positie op een recursieve manier
    """

    if get_disk_at(board, position) == None or Position.is_proper_position(dimension(board),position) == False:

        return 0

    else:
        position_left = Position.left(dimension(board), position)
        result = 1 + count_disks_left(board, position_left)
        return result


def count_disks_right(board,position):
    """
       Telt het aantal schijven rechts van de gegeven positie op een recursieve manier
    """

    if get_disk_at(board, position) == None or Position.is_proper_position(dimension(board),position) == False:

        return 0

    else:
        position_right = Position.right(dimension(board), position)
        result = 1 + count_disks_right(board, position_right)
        return result

# _______________________________________________________________________________

def get_length_vertical_chain(board, position):
    """
        Return the length of the vertical chain of disks involving the given
        position. Zero is returned if no disk is stored at the given position.
        ASSUMPTIONS
        - The given board is a playable board and the given position is a
          proper position for the given
          board.
        NOTE
        - This function must be implemented in a RECURSIVE way.
    """
    # Zie uitleg bij hulpfuncties hierboven
    # De voorwaarde dat de lengte 0 is als er geen disks is op de gegeven positie wordt al gecontroleerd door
    # de hulpfuncties.

    if count_disks_below(board,position) == 0 and count_disks_above(board,position) == 0:

        vertical_length = 0

    else:
        # Hier is de verticale lengte = (som - 1) want beide hulpfuncties tellen de disk op de gegeven positie mee
        # (Hierdoor is er hierboven een if functie, anders zou de lengte -1 zijn op een lege positie)

        vertical_length = count_disks_above(board,position) + count_disks_below(board,position) - 1

    return vertical_length


def get_length_horizontal_chain(board, position):
    """
        Return the length of the horizontal chain of disks involving the given
        position. Zero is returned if no disk is stored at the given position.
        ASSUMPTIONS
        - The given board is a proper board and the given position is a
          proper position for the given board.
    """
    # Zie uitleg bij hulpfuncties boven de functie 'get_lenght_vertical_chain'
    # De voorwaarde dat de lengte 0 is als er geen disks is op de gegeven positie wordt al gecontroleerd door
    # de hulpfuncties.

    if count_disks_left(board, position) == 0 and count_disks_right(board, position) == 0:

        horizontal_length = 0

    else:
        # Hier is de horizontale lengte = (som - 1) want beide hulpfuncties tellen de disk op de gegeven positie mee
        # (Hierdoor is er hierboven een if functie, anders zou de lengte -1 zijn op een lege positie)

        horizontal_length = count_disks_left(board,position) + count_disks_right(board,position) - 1

    return horizontal_length


def is_to_explode(board, position):
    """
        Return a boolean indicating whether the disk, if any, at the given
        position on the given board satisfies the conditions to explode.
        - True if and only if (1) the disk at the given position is visible, and
          (2) the number of the disk is equal to the length of the horizontal chain
          and/or the vertical chain involving that position.
        ASSUMPTIONS
        - The given board is a proper board and the given position is a
          proper position for the given board.
    """

    if get_disk_at(board,position) == None:

      return False

    # Voorwaarde 1: De schijf op gegeven positie is VISIBLE:
    elif Disk.get_state(get_disk_at(board,position)) == Disk.VISIBLE:

        # Voorwaarde 2: De horizontale en/of verticale lengte van de ketting van schijven is evengroot als
        # de waarde van de schijf

        if get_length_horizontal_chain(board,position) == Disk.get_value(get_disk_at(board,position)) or \
            get_length_vertical_chain(board,position) == Disk.get_value(get_disk_at(board,position)):

            return True

    else:
        return False


def get_all_positions_to_explode(board,start_pos=(1,1)):
    """
        Return a frozen set of all positions on the given board that
        have a disk that satisfies the conditions to explode, starting
        from the given position and proceeding to the top of the board
        using the next function.
        - The function returns the empty set if the given start position
          is None.
        ASSUMPTIONS
        - The given board is a proper board.
        - The given start position is either None or it is a proper position
          for the given board.
        NOTE
        - The second parameter should not be included in the code that
          is given to the students. They must learn to extend functions
          with extra parameters with a default value. The documentation
          of the function must be changed in view of that.
    """

    # Hulpfunctie:
    def explode(board,start_column=1):
        """
        Deze hulpfunctie returnt een lijst met alle posities die moeten ontploffen. Daarna zal de
        functie 'get_all_positions_to_explode' deze lijst omvormen in een set.

        """
        result = []
        positions_fit_to_explode = []

        if start_column > dimension(board):

            return result

        else:
            current_row = 1

            # Overloop het hele bord op een recursieve manier met 'is_to_explode' en voeg de disks die gaan ontploffen
            # toe aan de resulterende lijst:
            while current_row <= dimension(board) + 1:  # Rekening houden met de Overflowrij

                current_position = (start_column, current_row)

                if is_to_explode(board, current_position) == True:
                    positions_fit_to_explode.append(current_position)

                current_row += 1

            result = positions_fit_to_explode
            result.extend(explode(board, start_column + 1))     # Recursief deel

        return result

    if start_pos == None:
        return set()

    else:
        return frozenset(explode(board,start_pos[0]))


def crack_disks_at(board, positions):
    """
        Crack all disks at the given positions on the given board.
        - Wrapped disks will become cracked, and cracked disks will become
          visible.
        - Some positions may not contain any disk, or may contain non-crackable
          disks.
        ASSUMPTIONS
        - The given board is a proper board, and each of the given positions
          is a proper position for the given board.
    """
    huidige_pos = 0
    positions = list(positions)

    while huidige_pos <= (len(positions)-1):

        position = list(positions[huidige_pos])

        if Disk.get_state(get_disk_at(board,position)) == Disk.WRAPPED:

            Disk.set_state(get_disk_at(board,position),Disk.CRACKED)

        elif Disk.get_state(get_disk_at(board,position)) == Disk.CRACKED:

            Disk.set_state(get_disk_at(board,position),Disk.VISIBLE)

        huidige_pos += 1

def remove_all_disks_at(board, positions):
    """
        Remove all disks at the given positions on the given board.
        - All disks on top of disks that are removed drop down.
        - Positions in the given collection of positions at which no disk
          is stored, are ignored.
        ASSUMPTIONS
        - The given board is a proper board, and each of the given positions
          is a proper position for the given board.
    """

    #De tweede voorwaarde is al geïntegreerd in de functie 'remove_disk_at'

    # We sorteren de gegeven posities van 'groot' naar 'klein' op vlak van rij, zodat, als een disk verwijderd wordt,
    # dit de diks die nog moeten ontploffen in dezelfde kolom niet van plaats veranderen:
    huidige_pos = 0
    positions = list(positions)
    completly_sorted = False

    while completly_sorted == False:

        completly_sorted = True

        for i in range(len(positions) - 1):
            # De functie blijft sorteren zolang de lijst niet helemaal gesorteerd is
            if positions[i] < positions[i+1]:
                positions[i], positions[i+1] = positions[i+1], positions[i]
                completly_sorted = False

    # Verwijder deze gesorteerde disks dan elk om de beurt:
    while huidige_pos <= (len(positions)-1):

        position = list(positions[huidige_pos])
        remove_disk_at(board,position)
        huidige_pos += 1


### BOARD HELPER FUNCTIONS ###

def print_board(board):
    """
        Print the given board.
        ASSUMPTIONS
        - The given board must be a proper board.
    """
    assert is_proper_board(board)
    # Formatting could be used to improve the layout.
    for row in range(dimension(board)+1, 0, -1):
        print(end="|")
        for col in range(1, dimension(board) + 1):
            disk = get_disk_at(board, (col, row))
            if disk == None:
                print('   ', end=" |", )
            else:
                status = Disk.get_state(disk)
                value = Disk.get_value(disk)
                if status == Disk.WRAPPED:
                    print('%2s' % '\u2B24', end=" |")
                elif status == Disk.CRACKED:
                    print('%4s' % '\u20DD', end=" |")
                else:  # numbered disk
                    print('%3s' % value, end=" |", )
        print()
        if row == dimension(board)+1:
            print("|"+"----|"*dimension(board))
    print()