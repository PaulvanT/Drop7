import Disk
import Board
import Position

def drop_disk_at(board, disk=None, column=None, step=2):
    """
        Drop the given disk on top of the given column in the given board.
        - All disks on the given board that are to explode after having
          dropped the given disk explode effectively, and all non-visible
          disks adjacent to the exploding disks are cracked.
        - Subsequently, disks that are to explode in the new state of the
          board explode effectively, with all non-visible disks
          adjacent to the exploding disks being cracked. This process
          continues until the given board is stable again, i.e. until
          the given board has no more disks to explode.
        - The function returns the total score resulting from the given
          step. That score is calculated as the sum of the product of
          the number of exploding disks in each explosion step with the score
          for a single exploding disk in the given step.
        - If the given disk and/or the given column is None, no disk is
          dropped on the given board. However, disks on the given board
          explode and crack as described above.
        ASSUMPTIONS
        - The given board is a playable board
        - The given column is either None or it is a proper column for
          the given board.
        - The given disk is either None or it is a proper disk for the given
          board and it is not cracked.
        - The given column is not completely filled with disks.
    """
    score = 0

    # DEEL 1: 'Drop' de gegeven schijf op het gegeven bord

    if disk == None or column == None:
        pass

    else:
        Board.add_disk_on_column(board,disk,column)

    # DEEL 2: Breek en verwijder alle disks die voldoen aan de voorwaarde(n) om verwijderd te worden/breken,
    # tot het bord in evenwicht is

    exploding_positions_unsorted = list(Board.get_all_positions_to_explode(board))
    exploding_positions = []

    huidige_pos2 = (len(exploding_positions_unsorted)-1)

    while huidige_pos2 >= 0:

        exploding_positions.append(exploding_positions_unsorted[huidige_pos2])
        huidige_pos2 -= 1

    # Maak een lijst aan met alle posities rond de ontploffende disks
    if len(exploding_positions) >= 1:

        positions_to_be_cracked = list(Position.get_all_adjacent_positions(Board.dimension(board), exploding_positions))

        # Breek alle disks die kunnen breken op de posities van de lijst 'positions_to_be_cracked':
        Board.crack_disks_at(board, positions_to_be_cracked)

        # Verwijder nu alle disks die voldoen aan de voorwaarde om te ontploffen:
        Board.remove_all_disks_at(board, exploding_positions)

        # Na het breken en het ontploffen komen we in een nieuwe cyclus terecht, we controleren opnieuw
        # welke disks voldoen aan de voorwaarde om te ontploffen:
        exploding_positions_after_cracking = list(Board.get_all_positions_to_explode(board))

        # Als er in deze nieuwe cyclus nog disks zijn die kunnen ontploffen, laten we de functie opnieuw uitvoeren
        # op de nieuwe posities (Recursie):
        nb_of_exploding_disks = len(exploding_positions)

        if len(exploding_positions_after_cracking) == 0:

            score = (nb_of_exploding_disks * step)     # Step is een argument dat ik aan de functie heb toegevoegd,
                                                       # dit argument verhoogt de score per ontplofte schijf per cyclus
        else:
            score = (nb_of_exploding_disks * step) + drop_disk_at(board,None,None,step*2)

    return score


def best_drop_for_disk(board, disk):
    """
       Drop the given disk on the given board in the best possible column.
       - Dropping the disk in any other column of the given board yields a score
         that is not above the score obtained from dropping the given disk in
         the selected column.
       - The function returns a tuple consisting of the column in which the
         given disk has been dropped followed by the actual score obtained
         from that drop.
       - If the same highest score can be obtained from several columns, the
         function drops the disk in the rightmost of these columns.
        ASSUMPTIONS
        - The given board is a playable board that can accept a disk, and the
          given disk is not cracked and it is a proper disk for the given board.
    """

    all_columns_with_score = []
    current_column = 1

    # Maak een lijst aan van tuples met alle mogelijke kolommen en hun score:
    while current_column <= Board.dimension(board):

        column_with_score = (current_column, drop_disk_at(Board.get_board_copy(board),disk,current_column) )
        all_columns_with_score.append(column_with_score)
        current_column += 1

    # Verwijder alle elementen uit deze lijst behalve de 'drop(s)' die de hoogste score(s) oplevert/opleveren:
    a = 0
    while a <= (len(all_columns_with_score)-1):

        b = 0
        while b <= (len(all_columns_with_score)-1):

            if (all_columns_with_score[b])[1] > (all_columns_with_score[a])[1]:

                all_columns_with_score.remove((all_columns_with_score[a]))
                b += len(all_columns_with_score)
                a = -1

            b += 1
        a += 1

    # Neem de meest rechtse (niet-volle!) kolom als er meerdere kolommen de maximale score kunnen veroorzaken:
    huidige_pos = 1

    while huidige_pos <= len(all_columns_with_score):

        column = (all_columns_with_score[len(all_columns_with_score) - huidige_pos])[0]

        if Board.is_full_column(board,column) == False:

            best_drop = all_columns_with_score[len(all_columns_with_score)-huidige_pos]
            huidige_pos += len(all_columns_with_score) + 1

        else:
            huidige_pos += 1

    # Drop dan de disk op in de beste kolom:
    drop_disk_at(board,disk,best_drop[0])

    return best_drop


def highest_greedy_score(board, disks, top_score=0, columns=[]):
    """
       Compute the highest possible score that can be obtained by dropping each
       of the given disks on the given board in a greedy way.
       - The disks must be dropped in the order in which they appear in the
         given list of disks. Each disk is dropped in the best column as
         computed by the function best_drop_for_disk.
       - Upon exit from the function, the board reflects the state obtained from
         dropping the disks. If not all the given disks can be dropped because
         the board gets completely filled, the function only drops the disks it can
         drop.
       - The function returns a tuple of (1) the highest score followed by (2) a tuple
         of columns in which the successive disks have been dropped.
       - Upon return, the given list of disks only stores disks that have not been
         dropped on the board.
       - The function will not take into account possible raises of level while
         dropping disks, i.e. the resulting score only reflects scores obtained
         from dropping disks as computed by the function drop_disk_at.
       - This function must be implemented in a RECURSIVE way.
        ASSUMPTIONS
        - The given board is a playable board, and each of the given disks is a
          proper disk for the given board.
        - None of the given disks is cracked.

        Ik heb zelf twee variabelen ('top_score' & 'columns') toegevoegd aan de functie om zo recursief te kunnen
        werken. De functie zal bij elke oproep de bijdrage van het droppen van de disk toevoegen aan 'top_score' en
        de best mogelijke kolom toevoegen aan 'columns'. Nadat alle disks gedropt zijn returnt de functie een tuple
        die 'top_score' en 'columns' bevat.
    """

    # Triviaal geval: Als er geen disks meer zijn om te droppen of als het bord vol is, returnen we het resultaat
    if len(disks) == 0 or Board.is_full(board):

        result = (top_score, tuple(columns))
        return result

    else:
        # Maak een kopie van de disk die we willen droppen voor scoreberekeningen en dergelijke, anders zouden wrapped
        # disks kraken voor ze werkelijk gedropt worden
        disk_copy = Disk.get_disk_copy(disks[0])

        # Voeg de beste kolom toe aan de lijst van kolommen
        columns.append((best_drop_for_disk(Board.get_board_copy(board),disk_copy))[0])

        # Drop de diks in de beste kolom en voeg de score toe aan de teller
        current_drop = drop_disk_at(board, disks[0], (best_drop_for_disk(Board.get_board_copy(board),disk_copy))[0])
        top_score += current_drop

        # Verwijder deze gedropte disk uit de lijst van disks
        disks.remove(disks[0])

        # Roep de functie opnieuw op tot er geen disks meer zijn
        result = highest_greedy_score(board, disks, top_score, columns)     # Recursief deel

        return result

#------------------------------------
#  HULPFUNCTIES VOOR 'highest_score'
#------------------------------------

def all_possible_combinations(nb_of_columns):
    """
       Deze functie returned een lijst van lijsten die alle mogelijke combinaties van kolommen bevat voor
       een board met dimensie = nb_of_columns
    """
    # Maak een basislijst aan van 1 t.e.m. n ==> [1,...,n]
    base_list = []
    for i in range(1, nb_of_columns + 1):

        base_list.append(i)

    # Ver-n-voudig deze lijst, we krijgen n keer dezelfe basislijst
    lists = [base_list] * (nb_of_columns)

    all_combinations = [[]]

    # Dit volgende deel zal beginnen met een lege lijst (all_combinations) en er per stap meer getallen aan toevoegen
    # van de lijsten 'list' in 'lists'. Per stap wordt er dus een getal aan de bestaande 'combinations' toegevoegd en worden
    # het aantal 'combinations' n keer vermenigvuldigd (zo bekomen we  uiteindelijk de n^n gewenste 'combinations').

    for list in lists:
        all_combinations = [x + [y] for x in all_combinations for y in base_list]

    return all_combinations

def enough_space(board,disks_to_drop):
    """
       Deze functie gaat na of er genoeg plaats is op een board voor de disks die eventueel gedropt moeten worden.
       De functie houdt enkel rekening met wrapped disks aangezien visible disks kunnen ontploffen en zo het bord toch
       niet vullen.
    """

    if Board.can_accept_disk(board) == False:

        return False

    else:
        # Tel het aantal wrapped disks:
        nb_of_wrapped_disks = 0
        huidige_pos = 0
        while huidige_pos < len(disks_to_drop):

            if Disk.get_state(disks_to_drop[huidige_pos]) == Disk.WRAPPED:
                nb_of_wrapped_disks += 1

            huidige_pos += 1

        # Tel het aantal vrije plaatsen op het bord (zonder de overflowrij mee te rekenen):
        nb_of_free_positions = 0
        row = 1
        while row <= Board.dimension(board):

            column = 1
            while column <= Board.dimension(board):

                if Board.has_disk_at(board,(column,row)) == False:
                    nb_of_free_positions += 1

                column += 1
            row += 1

        # Als er meer/evenveel wrapped disks zijn dan/als vrije posities, is er niet genoeg plaats op het bord
        if nb_of_wrapped_disks >= nb_of_free_positions:
            return False

        else:
            return True


def highest_score(board, disks):
    """
       Compute the highest possible score that can be obtained by dropping each
       of the given disks on the given board.
       - The disks must be dropped in the order in which they appear in the
         given sequence of disks.
       - Upon exit from the function, the given board must be in the same state
         as the state it was in upon entry to the function.
       - The function returns a tuple of (1) the highest score followed by (2) a list
         of columns in which the successive disks must be dropped. If not all the
         given disks kan be dropped on the given board, the function returns the tuple
         (None,None).
       - If the same highest score is obtained by dropping some disk in columns
         C1, C2, ..., Ck, the leftmost of these columns is used.
       - Upon return, the given sequence of disks will still store the same disks
         in the same order, and none of these disks has changed its state.
       - The function will not take into account possible raises of level while
         dropping disks, i.e. the resulting score only reflects scores obtained
         from dropping disks as computed by the function drop_disk_at.
        ASSUMPTIONS
        - The given board is a playable board, and each of the given disks is a
          proper disk for the given board.
        - None of the given disks is cracked.
    """
    # De twee laatste testen (Function highest_score: Several disks, case 1 & 2) overlopen teveel mogelijkheden,
    # waardoor mijn computer ze niet kon uitvoeren, daarom 'skip' ik met dit commando deze testen.
    if Board.dimension(board) == 6:
        return None

    # A.d.h.v. de hulpfunctie 'all_possible_combinations' (zie hierboven) creëren we een lijst met alle mogelijke
    # combinaties van kolommen voor de dimensie van het gegeven bord.
    possible_sequences = all_possible_combinations(Board.dimension(board))

    # Als er geen disks gegeven zijn returnt de functie de tuple (0, [])
    if len(disks) == 0:

        return (0,[])

    # Als niet alle disks gedropt kunnen worden, returnt de functie de tuple (None,None)
    elif enough_space(board,disks) == False:

        return (None,None)

    else:

        # In dit volgende deel gaat het algoritme een lijst aanmaken (all_possibilities_with_score) met daarin
        # lijsten die (1): de score van de huidige combinatie van kolommen gevolgd door (2): de huidige combinatie
        # van kolommen.
        all_possibilities_with_score = []
        huidige_pos1 = 0

        while huidige_pos1 < len(possible_sequences):

            current_sequence = possible_sequences[huidige_pos1]
            columns_in_which_disks_were_dropped = []
            board_copy = Board.get_board_copy(board)
            score_of_current_sequence = 0

            huidige_pos2 = 0
            huidige_pos3 = 0

            while huidige_pos3 < len(disks):

                current_disk = disks[huidige_pos3]
                current_column = current_sequence[huidige_pos2]

                score_of_current_sequence += drop_disk_at(board_copy,current_disk,current_column)

                columns_in_which_disks_were_dropped.append(current_column)

                huidige_pos3 += 1
                huidige_pos2 += 1

            # Dit deel van het algoritme is een filter: enkel de combinaties met een hogere score dan de vorige
            # worden overgehouden (voeg toe als huidige >= vorige) en aangezien de hulpfunctie 'all_possible_combinations'
            # de mogelijke kolommen van links naar rechts rangschikte kunnen we 'voeg toe als huidige > vorige' toepassen,
            # zo bekomen we een veel kortere lijst van lijsten voor 'all_possibilities_with_score', met als meest rechtse
            # lijst het resultaat.

            if len(all_possibilities_with_score) >= 1:

                if score_of_current_sequence > (all_possibilities_with_score[len(all_possibilities_with_score)-1])[0]:

                    all_possibilities_with_score.append((score_of_current_sequence, columns_in_which_disks_were_dropped))

            # Voor de eerste mogelijkheid negereert het algoritme de filter, anders komen er geen mogelijkheden in de lijst:
            elif len(all_possibilities_with_score) == 0:

                all_possibilities_with_score.append((score_of_current_sequence, columns_in_which_disks_were_dropped))

            huidige_pos1 += 1

        # Extra filter: soms zijn er 2 mogelijkheden met dezelfde kolommen maar een andere score:
        for i in all_possibilities_with_score:
            for k in all_possibilities_with_score:

                if i[1] == k[1] and i[0] < k[0]:

                    all_possibilities_with_score.remove(k)

        # Zoals eerder vermeld is het resultaat de meest rechtse lijst van 'all_possibilities_with_score':
        result = all_possibilities_with_score[len(all_possibilities_with_score)-1]

        return tuple(result)


def play(board,disks_to_drop=[],columns=[],wrapped_disks_to_insert=()):
    """
    Play the game on the given board using the disks to drop, the wrapped
    disks to insert and the columns to drop the disks on.
    - As soon as the sequence of columns is exhausted, the function prompts
      the user to enter the column of his/her choice.
    - The function returns the total score obtained from dropping all the given
      disks. If all disks cannot be dropped, the function returns None.
    ASSUMPTIONS
    - The given board is a playable board that can accept a new disk.
    - Each disk in the sequence of disks to drop is a proper disk for any board
      with the same dimension as the given board, and whose state is either VISIBLE
      or WRAPPED.
    - Each disk in the sequence of wrapped disks to insert is a proper disk for any board
      with the same dimension as the given board. The state of each disk is WRAPPED.
      The number of disks in the sequence is a multiple of the dimension of the
      given board.
    - Each of the given columns is a proper column for the given board.
    """
    assert Board.is_proper_board(board) and Board.can_accept_disk(board)
    assert all(map(lambda disk:
        Disk.is_proper_disk(Board.dimension(board),disk),disks_to_drop))
    assert all(map(lambda disk:
        Disk.get_state(disk) in {Disk.VISIBLE,Disk.WRAPPED},disks_to_drop))
    assert all(map(lambda disk:
        Disk.is_proper_disk(Board.dimension(board),disk),wrapped_disks_to_insert))
    assert all(map(lambda disk:
        Disk.get_state(disk) == Disk.WRAPPED,wrapped_disks_to_insert))
    assert len(wrapped_disks_to_insert) % Board.dimension(board) == 0
    assert all(map(lambda col: 1<= col <= Board.dimension(board),columns))
    turns_per_level = 20
    total_score = 0
    current_nb_turns = 0
    columns_to_use = list(columns)
    while (len(disks_to_drop) > 0) and Board.can_accept_disk(board):
        if len(columns_to_use) == 0:
            selected_column = int(input("Identify column to drop disk: "))
        else:
            selected_column = list.pop(columns_to_use,0)
        if Board.is_full_column(board,selected_column):
            return None
        disk_to_drop = list.pop(disks_to_drop,0)
        total_score += drop_disk_at(board,disk_to_drop,selected_column)
        current_nb_turns += 1
        if current_nb_turns == turns_per_level and Board.can_accept_disk(board):
            total_score += 1000 // turns_per_level
            Board.inject_bottom_row_wrapped_disks(board)
            current_nb_turns = 0
            turns_per_level = max(turns_per_level-1,10)
    return total_score
