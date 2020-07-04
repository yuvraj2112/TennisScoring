import sys

class Match:
    def __init__(self, plyr1, plyr2):
        self.scoreMap = {
            plyr1: 0,
            plyr2: 0
        }
        self.gameMap = {
            plyr1: 0,
            plyr2: 0
        }
        self.draw = False

    """
        Method to update a point scored by a player
    """
    def pointWonBy(self, plyr):
        # raises exception attempt made to score after set over
        if self.isSet():
            raise Exception('Match Over')
        self.scoreMap[plyr] += 1
        if self.isGame():
            self.nextGame()

    """
        Method to check if current game is over after a point is scored
    """
    def isGame(self):
        for k1, v1 in self.scoreMap.items():
            for k2, v2 in self.scoreMap.items():
                if (k1 != k2 and v1 > (3 if not self.draw else 6) and (v1 - v2) > 1):
                    return k1
        return None

    """
        Method to check if the set is complete
    """
    def isSet(self):
        for k1, v1 in self.gameMap.items():
            for k2, v2 in self.gameMap.items():
                if (k1 != k2) and ((not self.draw and v1 > 6 and (v1 - v2) > 1) or (self.draw and v1 > v2)):
                    return k1
        return None

    """
        Method to check if the set has a tie
    """
    def isTie(self):
        for k1, v1 in self.gameMap.items():
            for k2, v2 in self.gameMap.items():
                if k1 != k2:
                    return v1 == v2 and v1 == 6

    """
        Method for when a game is over
        Used to reset current game score, check if the set is complete or change game mode to 'tied'
    """
    def nextGame(self):
        gameWonBy = self.isGame()
        self.gameMap[gameWonBy] += 1
        if self.isSet():
            print ('Set won by ' + self.isSet())
            return
        if self.isTie() or self.draw:
            self.draw = True
        for key in self.scoreMap:
            self.scoreMap[key] = 0

    """
        Method to generate tennis scoring lingo in case of normal/untied game
    """
    def getScoreString(self):
        scoringScheme = [0, 15, 30, 40]
        for k1, v1 in self.scoreMap.items():
            for k2, v2 in self.scoreMap.items():
                if k1 != k2 and v1 == v2 and v1 > 2 and v2 > 2:
                    return 'Deuce'
                elif k1 != k2 and v1 - v2 == 1 and v1 > 2 and v2 > 2:
                    return f'Advantage {k1}'
                elif k1 != k2:
                    return f'{v1 if v1 > len(scoringScheme) - 1 else scoringScheme[v1]} - {v2 if v2 > len(scoringScheme) - 1 else scoringScheme[v2]}'

    """
        Method to return score
    """
    def score(self):
        setScore = ' - '.join([str(k) for k in self.gameMap.values()])
        if self.draw:
            return setScore + ', ' + ' - '.join([str(k) for k in self.scoreMap.values()])
        else:
            return setScore + ', ' + self.getScoreString()

start = False
p1, p2 = None, None
match = None
while (True):
    m = None
    if not start:
        p1 = input("Player 1: ")
        p2 = input("Player 2: ")
        if p1 == None or p2 == None or p1 == p2:
            print ('Invalid input')
            continue
        match = Match(p1, p2)
        start = True
    else:
        choice = input(f"Press 1 for point won by {p1} and 2 for point won by {p2}, 3 for score, 4 to exit: ")
        if choice == '1':
            match.pointWonBy(p1)
        elif choice == '2':
            match.pointWonBy(p2)
        elif choice == '3':
            print(match.score())
        elif choice == '4':
            sys.exit()
        else:
            print ("Wrong input")
