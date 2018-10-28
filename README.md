# PyElo
**PyElo** is a Python implementation of the Elo rating system. PyElo supports rating **1v1 matches** and **team versus team** matches. PyElo also supports rating **ranked matches** where players place in ordered positions (e.g., 1st place, 2nd place, 3rd place, and so on).

## 1v1 matches
In the Elo rating system, a win is worth **1 point**, a draw is worth **0.5 points**, and a loss is worth **0 points**. Consider a match between two players A and B with ratings `rating_a` and `rating_b`. To get the expected score of player A, use the `expected_score` function. To get the expected score of player B, reverse the arguments (`expected_score(rating_b, rating_a)`), or do `1 - expected_score(rating_a, rating_b)`.

```Python
# All arguments are ints or floats.
def expected_score(rating_a, rating_b)
```

Suppose that player A and player B have played a match, and player A scores `score` points. Use the `update_rating` function, which returns a tuple with the new ratings of both players:

```Python
# All arguments are ints or floats.
def update_rating(rating_a, rating_b, score, k_a=20, k_b=20):
```

`update_rating` allows you to set the *K* factor of player A and player B (`k_a` and `k_b`). The *K* factor is the maximum change in rating after a match. Higher values of *K* make ratings change more drastically per game.

```Python
>>> rating_a = 1500 # Rating of player A.
>>> rating_b = 1500 # Rating of player B.
>>> expected_score(rating_a, rating_b)
0.5
>>> score = 1 # Score of player A.
>>> update_rating(rating_a, rating_b, score)
(1510.0, 1490.0)
```

## Team versus team matches
A *team* is a group of players. Consider a match between two teams A and B. `team_a` and `team_b` are the list of each players' ratings in each team. To get the expected score of team A, use the `expected_team_score` function. To get the expected score of player B, reverse the arguments (`expected_team_score(team_b, team_b)`), or do `1 - expected_team_score(team_a, team_b)`.

```Python
# All arguments are lists of ints or floats.
def expected_team_score(team_a, team_b)
```

Suppose that team A and team B have played a match, and team A scores `score` points. Use the `update_rating` function, which returns a tuple with the new ratings of both teams in the given order:

```Python
# team_a and team_b are lists of ints or floats. score, k_a, and k_b are ints or floats.
def update_team_rating(team_a, team_b, score, k_a=20, k_b=20)
```

`update_team_rating` allows you to set the *K* factor of team A and team B (`k_a` and `k_b`).

```Python
>>> team_a = [1500, 1200] # Ratings of team A.
>>> team_b = [1300, 1400] # Rating of player B.
>>> expected_team_score(team_a, team_b)
0.5
>>> score = 1 # Score of team A.
>>> update_team_rating(team_a, team_b, score)
([1516.9804088557735, 1203.0195911442265], [1292.8012999960577, 1387.1987000039423])
```

## Ranked matches
A ranked match is where each player places in a specific position after the match, like 1st place, 2nd place, 3rd place, and so on. Consider a ranked match between two or more players. To get the expected placing of a player A against the opposing players, use the `expected_place` function.

```Python
# rating is an int or float, opponent_ratings is a list of ints or floats.
def expected_place(rating, opponent_ratings)
```

For example,
```Python
>>> rating = 1500 # Player rating.
>>> opponent_ratings = [1300, 1600, 1400]
>>> expected_place(rating, opponent_ratings) # Around 2nd or 3rd place.
2.240253073352042
```

Suppose that two or more players have played a ranked match, and their ratings are ordered in the `ranks` list. Use the `update_rank_rating` function, which returns a list of all updated ratings in the given order:

```Python
# ranks is a list of ints or floats, k is either an int or float or a list of ints or floats.
def update_rank_rating(ranks, k=20)
```

`update_rank_rating` allows you to set either a single *K* factor for all players, or a list of *K* factors for each player.

```Python
>>> ranks = [1500, 1400, 1450, 1300, 1400, 1600]
>>> update_rank_rating(ranks)
[1508.114899824563, 1407.3248401762253, 1451.7141475303665, 1302.3691294900568, 1395.3248401762253, 1585.1521428025628]
```
