assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s + t for s in A for t in B]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
"""
Add diagonal_units into units, this will add diagnal constraints
units and peers are used in all functions except in naked_twins
naked_twins function will still constraints without diagmal constrains, renamed to peers2
"""
diagonal_units1 = [[a + b for a, b in (zip(rows, cols))]]
diagonal_units2 = [[a + b for a, b in (zip(rows, cols[::-1]))]]
unitlist = row_units + column_units + square_units +diagonal_units1 + diagonal_units2
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

unitlist2 = row_units + column_units + square_units
units2 = dict((s, [u for u in unitlist2 if s in u]) for s in boxes)
peers2 = dict((s, set(sum(units2[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

    """
    1. Find the labels of sudoko box which has two digits values
    2. Group the labels which have same value
    3. Group out the peers of two same value label
    4. Delete the same value from the grouped out peers
    """
    labels = [label for label in values.keys() if len(values[label]) == 2]
    for test_label in labels:
        labels_of_same_value = [label for label in labels if values[label] == values[test_label]]
        for i in range(len(labels_of_same_value) - 1):
            for j in range(i + 1, len(labels_of_same_value)):
                # check if two labels at same peers
                intersection_labels = peers2[labels_of_same_value[i]].intersection(peers2[labels_of_same_value[j]])
                if len(intersection_labels) >= 7:
                    for label in intersection_labels:
                        for digit in values[labels_of_same_value[i]]:
                            values[label] = values[label].replace(digit, '')
        [labels.remove(label) for label in labels_of_same_value] #remove the onces which has finished naked_twins check

    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    assert len(grid) == 81, "Input grid must be a string of length 81 (9x9)"

    values = []
    all_digits = '123456789'
    for c in grid:
        if c == '.':
            values.append(all_digits)
        else:
            values.append(c)

    return dict(zip(cross(rows, cols), values))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in cross(rows, cols))
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """
    Elimite the already solved boxes's values from peers
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for label in solved_values:
        digit = values[label]
        for peer in peers[label]:
            values[peer] = values[peer].replace(digit, '')

    return values

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in unitlist:
        for digit in '123456789':
            box_arr = [box for box in unit if digit in values[box]]
            if len(box_arr) == 1:
                values[box_arr[0]] = digit
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    # [assign_value(sudoko, label, sudoko[label]) for label in sudoko.keys()]
    return search(grid_values(grid))


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
