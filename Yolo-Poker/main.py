from ultralytics import YOLO
import cv2
import cvzone
import math


def findPokerHand(hand):

    ranks = []
    suits = []
    possibleRanks = []
    sortedRanks = []

    # Seperate into list of suits and ranks
    for card in hand:
        if len(card) == 2:
            rank = card[0]
        else:
            rank = card[0:2]

        if len(card) == 2:
            suit = card[1]
        else:
            suit = card[2]

        # Convert High Ranks to Numbers
        if rank == "A":
            rank = 14
        if rank == "K":
            rank = 13
        if rank == "Q":
            rank = 12
        if rank == "J":
            rank = 11

        suits.append(suit)
        ranks.append(int(rank))

    sortedRanks = sorted(ranks)

    # Find Poker Hand

    pokerHandRanks = {
        10: "Royal Flush",
        9: "Straight Flush",
        8: "Four of a Kind",
        7: "Full House",
        6: "Straight",
        5: "Flush",
        4: "Three of a kind ",
        3: "Two Pair",
        2: "One Pair",
        1: "High Card"
    }

    # Check for Flush
    if suits.count(suits[0]) == 5:
        if 14 in sortedRanks \
                and 13 in sortedRanks \
                and 12 in sortedRanks \
                and 11 in sortedRanks \
                and 10 in sortedRanks:
            possibleRanks.append(10)  # Add Royal Flush to Possible Ranks
        elif all(sortedRanks[i] == sortedRanks[i - 1] + 1 for i in range(1, len(sortedRanks))):
            possibleRanks.append(9)  # Add Straight Flush to Possible Ranks
        else:
            # If not Straight or Royal Flush then add Flush to Possible Ranks
            possibleRanks.append(5)

    # Check for Straight
    if all(sortedRanks[i] == sortedRanks[i - 1] + 1 for i in range(1, len(sortedRanks))):
        possibleRanks.append(6)  # Add Straight to possible Ranks

    # Finds Unique Ranks : e.g [ A , A , A , K , K] -> [A , K]
    handUniqueRanks = list(set(sortedRanks))

    # Find Either Four of a Kind or Full House
    if len(handUniqueRanks) == 2:
        for currentRank in handUniqueRanks:
            # If One of the two numbers occurs 4 times then Four for a Kind
            if sortedRanks.count(currentRank) == 4:
                possibleRanks.append(8)  # Four of a Kind
            # If One of the two numbers occurs 3 times and the set is only 2 then full house
            if sortedRanks.count(currentRank) == 3:
                possibleRanks.append(7)  # Full House

    # Check for Three of a Kind or Two pair
    if len(handUniqueRanks) == 3:
        for currentRank in handUniqueRanks:
            # If One of the two numbers occurs 3 times then Three for a Kind
            if sortedRanks.count(currentRank) == 3:
                possibleRanks.append(4)  # Three of a Kind
            else:  # Otherwise it must be two pair
                possibleRanks.append(3)  # Two Pair

    # Check for Pair
    if len(handUniqueRanks) == 4:
        for currentRank in handUniqueRanks:
            # If One of the two numbers occurs 2 times then one pair
            if sortedRanks.count(currentRank) == 2:
                possibleRanks.append(2)

    # if no other hands were found then it has a high card
    if not possibleRanks:
        possibleRanks.append(1)

    output = pokerHandRanks[max(possibleRanks)]
    print(hand, output)

    return output


if __name__ == "__main__":
    findPokerHand(["AH", "KH", "QH", "JH", "10H"])  # Royal Flush
    findPokerHand(["KH", "QH", "JH", "10H", "9H"])  # Straight Flush
    findPokerHand(["5H", "5S", "5D", "5C", "9H"])  # Four of a Kind
    findPokerHand(["5H", "5S", "5D", "9D", "9H"])  # Full House
    findPokerHand(["KD", "QH", "JC", "10H", "9S"])  # Straight
    findPokerHand(["KH", "8H", "3H", "9H", "2H"])  # Flush
    findPokerHand(["5H", "5S", "5D", "8D", "9H"])  # Three of a kind
    findPokerHand(["5H", "5S", "2D", "8D", "8H"])  # Two Pair
    findPokerHand(["5H", "5S", "2D", "8D", "9H"])  # One Pair
    findPokerHand(["4H", "5S", "2D", "8D", "9H"])  # High Card 
