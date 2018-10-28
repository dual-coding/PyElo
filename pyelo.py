'''
Copyright (C) 2018 PyElo.

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

# Expected score of player A with rating 'rating_a' against player B with
# 'rating_b'.
def expected_score(rating_a, rating_b):
    return 1.0 / (1.0 + 10.0 ** ((rating_b - rating_a) / 400.0))

# Change in rating based on expected and actual score.
def rating_delta(score, expected, k=20):
    if k <= 0:
        raise ValueError("k must be positive.")

    return k * (score - expected)

# Update individual ratings after a 1v1 match. The pair of new ratings is
# returned as a tuple (new rating of player A, new rating of B). K factors may
# be individually set for both players.
def update_rating(rating_a, rating_b, score, k_a=20, k_b=20):
    if k_a <= 0:
        raise ValueError("k_a must be positive.")
    if k_b <= 0:
        raise ValueError("k_b must be positive.")

    expected_a = expected_score(rating_a, rating_b)
    expected_b = 1 - expected_a

    rating_a += rating_delta(score, expected_a, k_a)
    rating_b += rating_delta(1 - score, expected_b, k_b)

    return (rating_a, rating_b)

# Expected score of team A against team B. Teams are a list of player ratings.
def expected_team_score(team_a, team_b):
    if len(team_a) == 0:
        raise ValueError("team_a must have at least one rating.")
    if len(team_b) == 0:
        raise ValueError("team_b must have at least one rating.")

    return expected_score(sum(team_a), sum(team_b))

# Convert Elo ratings to the Bradley-Terry scale.
def elo_to_bt(elo_rating):
    return 10.0 ** (elo_rating / 400.0)

# Update team ratings, where a team is a collection of ratings. The pair of new
# ratings is returned of (new ratings of team A, new ratings of team B) in the
# given order. K factors may be individually set for both teams.
def update_team_rating(team_a, team_b, score, k_a=20, k_b=20):
    if k_a <= 0:
        raise ValueError("k_a must be positive.")
    if k_b <= 0:
        raise ValueError("k_b must be positive.")
    if len(team_a) == 0:
        raise ValueError("team_a must have at least one rating.")
    if len(team_b) == 0:
        raise ValueError("team_b must have at least one rating.")

    expected_a = expected_team_score(team_a, team_b)
    expected_b = 1 - expected_a

    delta_a = rating_delta(score, expected_a, k_a * len(team_a))
    delta_b = rating_delta(1 - score, expected_b, k_b * len(team_b))

    # Teams' ratings converted to the Bradley-Terry scale.
    bt_team_a = [elo_to_bt(rating) for rating in team_a]
    bt_team_b = [elo_to_bt(rating) for rating in team_b]

    # Calculate normalization quotient.
    norm_bt_team_a = sum(bt_team_a)
    norm_bt_team_b = sum(bt_team_b)

    # Normalize Bradley-Terry team ratings.
    bt_team_a = [rating / norm_bt_team_a for rating in bt_team_a]
    bt_team_b = [rating / norm_bt_team_b for rating in bt_team_b]

    # Apply deltas in terms of normalized ratings.
    team_a_delta = [delta_a * rating for rating in bt_team_a]
    team_b_delta = [delta_b * rating for rating in bt_team_b]

    # Return updated ratings.
    return ([rating + delta for rating, delta in zip(team_a, team_a_delta)], [rating + delta for rating, delta in zip(team_b, team_b_delta)])

# Expected score in a match with multiple ranks.
def expected_rank_score(ranks):
    if len(ranks) <= 1:
        raise ValueError("The length of ranks must be 2 or greater.")

    return [sum(expected_score(ranks[i], opp_rating) for j, opp_rating in enumerate(ranks) if i != j) for i, rating in enumerate(ranks)]

# Expected placing in a match with multiple ranks.  Return values are not
# rounded to the nearest integer.
def expected_place(rating, opponent_ratings):
    if len(opponent_ratings) == 0:
        raise ValueError("opponent_ratings must have at least one rating.")

    return 1 + len(opponent_ratings) - sum(expected_score(rating, opp_rating) for opp_rating in opponent_ratings)

# Update the rating of a ranking of players, where ranks is a list of ratings
# sorted by results: the first element of the list is 1st place, the second is
# 2nd place, and so on. Ratings are returned in the same order, and K factors
# may either be set for all players or individually for each player.
def update_rank_rating(ranks, k=20):
    if len(ranks) <= 1:
        raise ValueError("The length of ranks must have two ratings or greater.")
    if type(k) is list:
        if len(k) != len(ranks):
            raise ValueError("The length of ranks must be the same as the length of k, or a single k factor should be given.")
        # Check if all k are positive.
        if sum(1 for individual_k in k if individual_k <= 0) > 0:
            raise ValueError("All k factors must be positive.")
    else:
        if k <= 0:
            raise ValueError("k must be positive.")
        # Add len(ranks) - 1 elements to k.
        k = [k] * len(ranks)

    expected = expected_rank_score(ranks)

    # Calculate k normalization quotient.
    k_norm = len(ranks) - 1
    scores = list(range(k_norm, -1, -1))

    return [rating + rating_delta(score, individual_expected, individual_k / k_norm) for rating, score, individual_expected, individual_k in zip(ranks, scores, expected, k)]
