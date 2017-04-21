## Heuristic Analysis

I tried 3 custom heuristics for get the game have a better performance compare with ID_Improved agent, and I use _legal moves and forecasted new legal moves_ as the ultimate heuristic according to the score it get.

### h(1) moves and blanks' ratio

compare the differential of legal_moves with total blank spaces, game with high ratio leads better outcomes.

**Implementation**:
$$
h(1) = \frac{(player1Moves * 3 - player2Moves * 2)}{blank Space }
$$
**results**:

ID_Improved         62.86%
Student            67.14%

### h(2) legal moves and forecasted new legal moves

Based on the differential of player's legal moves and opponent's legal moves, add the check of how many new legal moves it leads to with forecast every legal moves, compare the sum of new legal moves between the player and it's opponent.

**Implementation**:
$$
h(2) = (player1Moves + player2ForecastMove) - (player2Moves + player1ForescastMove)
$$
**results**:

ID_Improved         65.71%
Student             76.43%

### h(3) moves and centor moves

Based on the differential of player's legal moves and opponent's legal moves, give addional score if moves results in center.

**Implementation**:
$$
h(3) = (player1Moves + player1CentorMove) - (player2Moves + player2CentorMove)
$$
**results**:

ID_Improved         60.00%
Student             66.43% 

### conclusion

Based on the three heuristic results, h(1) and h(3) both invite the idea of blank spaces, centor moves and add weight to current moves, it seems doesn't gives a much better performance. 

h(1) and h(3) both improved the student agent's score little bit but not very much, h(2) gives a much better performance.

I think the main reason for this is h(2) invites the idea that goes one branch deeper to compare the results of what the current move leads to, then choose the one that gives a better 'future'. 



