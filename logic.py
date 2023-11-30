import copy

# TODO
# make a function to display the board nicely
# make a draw counter

player = "whiMin"


#clear game.txt
gameFile = open("game.txt", "w")
gameFile.write("")
gameFile.close()


class State:
    def __init__(self, board):
        self.board = board


def createBoardArray():
    with open("testingState.txt") as startingBoardtxt:
        startingBoardArray = []
        for row in startingBoardtxt.readlines():
            tempArray = []
            for square in row.rstrip():
                tempArray.append(square)
            startingBoardArray.append(tempArray)
    return startingBoardArray


def checkForwardsLeftSquare(
    currentStateBoard: list, currentPlayer: str, rowNum: int, columnNum: int
):  # return empty, blocked, or opponent
    if currentPlayer == "redMax":
        if rowNum == 7 or columnNum == 7:  # against edges of board
            return "r"
        return currentStateBoard[rowNum + 1][columnNum + 1]
    elif currentPlayer == "whiMin":
        if rowNum == 0 or columnNum == 0:
            return "w"
        return currentStateBoard[rowNum - 1][columnNum - 1]


def checkForwardsRightSquare(
    currentStateBoard: list, currentPlayer: str, rowNum: int, columnNum: int
):  # return empty, blocked, or opponent
    if currentPlayer == "redMax":
        if rowNum == 7 or columnNum == 0:  # against edges of board
            return "r"
        return currentStateBoard[rowNum + 1][columnNum - 1]
    elif currentPlayer == "whiMin":
        if rowNum == 0 or columnNum == 7:
            return "w"
        return currentStateBoard[rowNum - 1][columnNum + 1]


def checkBackwardsLeftSquare(
    currentStateBoard: list, currentPlayer: str, rowNum: int, columnNum: int
):  # return empty, blocked, or opponent
    if currentPlayer == "redMax":
        if rowNum == 0 or columnNum == 7:  # against edges of board
            return "r"
        return currentStateBoard[rowNum - 1][columnNum + 1]
    elif currentPlayer == "whiMin":
        if rowNum == 7 or columnNum == 0:
            return "w"
        return currentStateBoard[rowNum + 1][columnNum - 1]


def checkBackwardsRightSquare(
    currentStateBoard: list, currentPlayer: str, rowNum: int, columnNum: int
):  # return empty, blocked, or opponent
    if currentPlayer == "redMax":
        if rowNum == 0 or columnNum == 0:  # against edges of board
            return "r"
        return currentStateBoard[rowNum - 1][columnNum - 1]
    elif currentPlayer == "whiMin":
        if rowNum == 7 or columnNum == 7:
            return "w"
        return currentStateBoard[rowNum + 1][columnNum + 1]


def checkForwardsLeftJump(
    currentStateBoard: list, currentPlayer: str, rowNum: int, columnNum: int
):
    if currentPlayer == "redMax":
        if rowNum >= 6 or columnNum >= 6:  # against edges of board
            return "r"
        return currentStateBoard[rowNum + 2][columnNum + 2]
    elif currentPlayer == "whiMin":
        if rowNum <= 1 or columnNum <= 1:
            return "w"
        return currentStateBoard[rowNum - 2][columnNum - 2]


def checkForwardsRightJump(
    currentStateBoard: list, currentPlayer: str, rowNum: int, columnNum: int
):
    if currentPlayer == "redMax":
        if rowNum >= 6 or columnNum <= 1:  # against edges of board
            return "r"
        return currentStateBoard[rowNum + 2][columnNum - 2]
    elif currentPlayer == "whiMin":
        if rowNum <= 1 or columnNum >= 6:
            return "w"
        return currentStateBoard[rowNum - 2][columnNum + 2]


def checkBackwardsLeftJump(
    currentStateBoard: list, currentPlayer: str, rowNum: int, columnNum: int
):  # based on red/white's forward facing left
    if currentPlayer == "redMax":
        if rowNum <= 1 or columnNum >= 6:  # against edges of board
            return "r"
        return currentStateBoard[rowNum - 2][columnNum + 2]
    elif currentPlayer == "whiMin":
        if rowNum >= 6 or columnNum <= 1:
            return "w"
        return currentStateBoard[rowNum + 2][columnNum - 2]


def checkBackwardsRightJump(
    currentStateBoard: list, currentPlayer: str, rowNum: int, columnNum: int
):  # based on red/white's forward facing left
    if currentPlayer == "redMax":
        if rowNum <= 1 or columnNum <= 1:  # against edges of board
            return "r"
        return currentStateBoard[rowNum - 2][columnNum - 2]
    elif currentPlayer == "whiMin":
        if rowNum >= 6 or columnNum >= 6:
            return "w"
        return currentStateBoard[rowNum + 2][columnNum + 2]


def getJumps(
    currentStateBoard: list,
    currentPlayer: str,
    rowNum: int,
    columnNum: int,
    isQueen: bool,
    jumpingStates: list,
    hasRun: bool,
):
    possibleJumps = []

    # possibleJumps is a 2D array in the form [a new state, the new rowNum, the new columnNum]

    # given a space, find all possible jumps/routes
    # start by looking at squares in front and if they are opponents, check if the next square is free
    # if it is free, create the altered board and add it to a list
    # loop through each possible position and call getJumps, when there are no more positions left, create a successor and return

    if currentPlayer == "redMax":
        if (
            checkForwardsLeftSquare(
                currentStateBoard, currentPlayer, rowNum, columnNum
            ).lower()
            == "w"
            and checkForwardsLeftJump(
                currentStateBoard, currentPlayer, rowNum, columnNum
            )
            == "."
        ):
            possibleJumps.append(
                [
                    createSuccessor(
                        currentStateBoard,
                        currentPlayer,
                        rowNum,
                        columnNum,
                        rowNum + 2,
                        columnNum + 2,
                        True,
                    ),
                    rowNum + 2,
                    columnNum + 2,
                ]
            )

        if (
            checkForwardsRightSquare(
                currentStateBoard, currentPlayer, rowNum, columnNum
            ).lower()
            == "w"
            and checkForwardsRightJump(
                currentStateBoard, currentPlayer, rowNum, columnNum
            )
            == "."
        ):
            possibleJumps.append(
                [
                    createSuccessor(
                        currentStateBoard,
                        currentPlayer,
                        rowNum,
                        columnNum,
                        rowNum + 2,
                        columnNum - 2,
                        True,
                    ),
                    rowNum + 2,
                    columnNum - 2,
                ]
            )

        if isQueen:
            if (
                checkBackwardsLeftSquare(
                    currentStateBoard, currentPlayer, rowNum, columnNum
                ).lower()
                == "w"
                and checkBackwardsLeftJump(
                    currentStateBoard, currentPlayer, rowNum, columnNum
                )
                == "."
            ):
                possibleJumps.append(
                    [
                        createSuccessor(
                            currentStateBoard,
                            currentPlayer,
                            rowNum,
                            columnNum,
                            rowNum - 2,
                            columnNum + 2,
                            True,
                        ),
                        rowNum - 2,
                        columnNum + 2,
                    ]
                )

            if (
                checkBackwardsRightSquare(
                    currentStateBoard, currentPlayer, rowNum, columnNum
                ).lower()
                == "w"
                and checkBackwardsRightJump(
                    currentStateBoard, currentPlayer, rowNum, columnNum
                )
                == "."
            ):
                possibleJumps.append(
                    [
                        createSuccessor(
                            currentStateBoard,
                            currentPlayer,
                            rowNum,
                            columnNum,
                            rowNum - 2,
                            columnNum - 2,
                            True,
                        ),
                        rowNum - 2,
                        columnNum - 2,
                    ]
                )

    if currentPlayer == "whiMin":
        if (
            checkForwardsLeftSquare(
                currentStateBoard, currentPlayer, rowNum, columnNum
            ).lower()
            == "r"
            and checkForwardsLeftJump(
                currentStateBoard, currentPlayer, rowNum, columnNum
            )
            == "."
        ):
            possibleJumps.append(
                [
                    createSuccessor(
                        currentStateBoard,
                        currentPlayer,
                        rowNum,
                        columnNum,
                        rowNum - 2,
                        columnNum - 2,
                        True,
                    ),
                    rowNum - 2,
                    columnNum - 2,
                ]
            )

        if (
            checkForwardsRightSquare(
                currentStateBoard, currentPlayer, rowNum, columnNum
            ).lower()
            == "r"
            and checkForwardsRightJump(
                currentStateBoard, currentPlayer, rowNum, columnNum
            )
            == "."
        ):
            possibleJumps.append(
                [
                    createSuccessor(
                        currentStateBoard,
                        currentPlayer,
                        rowNum,
                        columnNum,
                        rowNum - 2,
                        columnNum + 2,
                        True,
                    ),
                    rowNum - 2,
                    columnNum + 2,
                ]
            )

        if isQueen:
            if (
                checkBackwardsLeftSquare(
                    currentStateBoard, currentPlayer, rowNum, columnNum
                ).lower()
                == "r"
                and checkBackwardsLeftJump(
                    currentStateBoard, currentPlayer, rowNum, columnNum
                )
                == "."
            ):
                possibleJumps.append(
                    [
                        createSuccessor(
                            currentStateBoard,
                            currentPlayer,
                            rowNum,
                            columnNum,
                            rowNum + 2,
                            columnNum - 2,
                            True,
                        ),
                        rowNum + 2,
                        columnNum - 2,
                    ]
                )

            if (
                checkBackwardsRightSquare(
                    currentStateBoard, currentPlayer, rowNum, columnNum
                ).lower()
                == "r"
                and checkBackwardsRightJump(
                    currentStateBoard, currentPlayer, rowNum, columnNum
                )
                == "."
            ):
                possibleJumps.append(
                    [
                        createSuccessor(
                            currentStateBoard,
                            currentPlayer,
                            rowNum,
                            columnNum,
                            rowNum + 2,
                            columnNum + 2,
                            True,
                        ),
                        rowNum + 2,
                        columnNum + 2,
                    ]
                )

    for possibleJump in possibleJumps:
        hasRun = True
        getJumps(
            possibleJump[0],
            currentPlayer,
            possibleJump[1],
            possibleJump[2],
            isQueen,
            jumpingStates,
            hasRun,
        )

    if len(possibleJumps) == 0 and hasRun:
        jumpingStates.append(currentStateBoard)
        return


def createSuccessor(
    currentStateBoard: list,
    currentPlayer: str,
    rowNum: int,
    columnNum: int,
    newRowNum: int,
    newColumnNum: int,
    isJumping: bool,
):
    # copy the current board and then alter it according to parameters
    newStateBoard = copy.deepcopy(currentStateBoard)

    if not (isJumping):
        # copy the piece and move it to new location
        tempPiece = newStateBoard[rowNum][columnNum]
        newStateBoard[rowNum][columnNum] = "."
        newStateBoard[newRowNum][newColumnNum] = tempPiece
        if currentPlayer == "redMax" and newRowNum == 7:
            newStateBoard[newRowNum][newColumnNum] = tempPiece.upper()
        elif currentPlayer == "whiMin" and newRowNum == 0:
            newStateBoard[newRowNum][newColumnNum] = tempPiece.upper()
    elif isJumping:
        # copy the piece and move it to new location
        tempPiece = newStateBoard[rowNum][columnNum]
        newStateBoard[rowNum][columnNum] = "."
        newStateBoard[int((rowNum + newRowNum) / 2)][
            int((columnNum + newColumnNum) / 2)
        ] = "."
        newStateBoard[newRowNum][newColumnNum] = tempPiece
        if currentPlayer == "redMax" and newRowNum == 7:
            newStateBoard[newRowNum][newColumnNum] = tempPiece.upper()
        elif currentPlayer == "whiMin" and newRowNum == 0:
            newStateBoard[newRowNum][newColumnNum] = tempPiece.upper()

    return newStateBoard


# return a list of all possible future states (depth:1)
def getSuccessors(currentStateBoard, currentPlayer: str):
    nonJumpingStates = []
    jumpingStates = []

    for rowNum in range(8):
        for columnNum in range(8):
            # depending on player, call functions on pieces to get moves
            if (
                currentPlayer == "redMax"
                and currentStateBoard[rowNum][columnNum] == "r"
            ):  # red singles
                forwardsLeftStatus = checkForwardsLeftSquare(
                    currentStateBoard, currentPlayer, rowNum, columnNum
                )
                forwardsRightStatus = checkForwardsRightSquare(
                    currentStateBoard, currentPlayer, rowNum, columnNum
                )
                if (
                    forwardsLeftStatus == "."
                ):  # check the square that is forwards and left of the piece, the using this particular player's left (board is flipped for red)
                    nonJumpingStates.append(
                        createSuccessor(
                            currentStateBoard,
                            currentPlayer,
                            rowNum,
                            columnNum,
                            rowNum + 1,
                            columnNum + 1,
                            False,
                        )
                    )

                if (
                    forwardsRightStatus == "."
                ):  # check the square that is forwards and right of the piece, the using this particular player's right (board is flipped for red)
                    nonJumpingStates.append(
                        createSuccessor(
                            currentStateBoard,
                            currentPlayer,
                            rowNum,
                            columnNum,
                            rowNum + 1,
                            columnNum - 1,
                            False,
                        )
                    )

                if (
                    forwardsLeftStatus.lower() == "w"
                    or forwardsRightStatus.lower() == "w"
                ):
                    getJumps(
                        currentStateBoard,
                        currentPlayer,
                        rowNum,
                        columnNum,
                        False,
                        jumpingStates,
                        False,
                    )

            elif (
                currentPlayer == "redMax"
                and currentStateBoard[rowNum][columnNum] == "R"
            ):  # red queens
                forwardsLeftStatus = checkForwardsLeftSquare(
                    currentStateBoard, currentPlayer, rowNum, columnNum
                )
                forwardsRightStatus = checkForwardsRightSquare(
                    currentStateBoard, currentPlayer, rowNum, columnNum
                )
                backwardsLeftStatus = checkBackwardsLeftSquare(
                    currentStateBoard, currentPlayer, rowNum, columnNum
                )
                backwardsRightStatus = checkBackwardsRightSquare(
                    currentStateBoard, currentPlayer, rowNum, columnNum
                )
                if (
                    forwardsLeftStatus == "."
                ):  # check the square that is forwards and left of the piece, the using this particular player's left (board is flipped for red)
                    nonJumpingStates.append(
                        createSuccessor(
                            currentStateBoard,
                            currentPlayer,
                            rowNum,
                            columnNum,
                            rowNum + 1,
                            columnNum + 1,
                            False,
                        )
                    )

                if (
                    forwardsRightStatus == "."
                ):  # check the square that is forwards and right of the piece, the using this particular player's right (board is flipped for red)
                    nonJumpingStates.append(
                        createSuccessor(
                            currentStateBoard,
                            currentPlayer,
                            rowNum,
                            columnNum,
                            rowNum + 1,
                            columnNum - 1,
                            False,
                        )
                    )

                if (
                    backwardsLeftStatus == "."
                ):  # check the square that is backwards and left of the piece, the using this particular player's left (board is flipped for red)
                    nonJumpingStates.append(
                        createSuccessor(
                            currentStateBoard,
                            currentPlayer,
                            rowNum,
                            columnNum,
                            rowNum - 1,
                            columnNum + 1,
                            False,
                        )
                    )

                if (
                    backwardsRightStatus == "."
                ):  # check the square that is backwards and right of the piece, the using this particular player's right (board is flipped for red)
                    nonJumpingStates.append(
                        createSuccessor(
                            currentStateBoard,
                            currentPlayer,
                            rowNum,
                            columnNum,
                            rowNum - 1,
                            columnNum - 1,
                            False,
                        )
                    )

                if (
                    forwardsLeftStatus.lower() == "w"
                    or forwardsRightStatus.lower() == "w"
                    or backwardsLeftStatus.lower() == "w"
                    or backwardsRightStatus.lower() == "w"
                ):
                    getJumps(
                        currentStateBoard,
                        currentPlayer,
                        rowNum,
                        columnNum,
                        True,
                        jumpingStates,
                        False,
                    )

            elif (
                currentPlayer == "whiMin"
                and currentStateBoard[rowNum][columnNum] == "w"
            ):  # white singles
                forwardsLeftStatus = checkForwardsLeftSquare(
                    currentStateBoard, currentPlayer, rowNum, columnNum
                )
                forwardsRightStatus = checkForwardsRightSquare(
                    currentStateBoard, currentPlayer, rowNum, columnNum
                )
                if (
                    forwardsLeftStatus == "."
                ):  # check the square that is forwards and left of the piece, the using this particular player's left (board is flipped for red)
                    nonJumpingStates.append(
                        createSuccessor(
                            currentStateBoard,
                            currentPlayer,
                            rowNum,
                            columnNum,
                            rowNum - 1,
                            columnNum - 1,
                            False,
                        )
                    )

                if (
                    forwardsRightStatus == "."
                ):  # check the square that is forwards and right of the piece, the using this particular player's right (board is flipped for red)
                    nonJumpingStates.append(
                        createSuccessor(
                            currentStateBoard,
                            currentPlayer,
                            rowNum,
                            columnNum,
                            rowNum - 1,
                            columnNum + 1,
                            False,
                        )
                    )

                if (
                    forwardsLeftStatus.lower() == "r"
                    or forwardsRightStatus.lower() == "r"
                ):
                    getJumps(
                        currentStateBoard,
                        currentPlayer,
                        rowNum,
                        columnNum,
                        False,
                        jumpingStates,
                        False,
                    )

            elif (
                currentPlayer == "whiMin"
                and currentStateBoard[rowNum][columnNum] == "W"
            ):  # white queens
                forwardsLeftStatus = checkForwardsLeftSquare(
                    currentStateBoard, currentPlayer, rowNum, columnNum
                )
                forwardsRightStatus = checkForwardsRightSquare(
                    currentStateBoard, currentPlayer, rowNum, columnNum
                )
                backwardsLeftStatus = checkBackwardsLeftSquare(
                    currentStateBoard, currentPlayer, rowNum, columnNum
                )
                backwardsRightStatus = checkBackwardsRightSquare(
                    currentStateBoard, currentPlayer, rowNum, columnNum
                )
                if (
                    forwardsLeftStatus == "."
                ):  # check the square that is forwards and left of the piece, the using this particular player's left (board is flipped for red)
                    nonJumpingStates.append(
                        createSuccessor(
                            currentStateBoard,
                            currentPlayer,
                            rowNum,
                            columnNum,
                            rowNum - 1,
                            columnNum - 1,
                            False,
                        )
                    )

                if (
                    forwardsRightStatus == "."
                ):  # check the square that is forwards and right of the piece, the using this particular player's right (board is flipped for red)
                    nonJumpingStates.append(
                        createSuccessor(
                            currentStateBoard,
                            currentPlayer,
                            rowNum,
                            columnNum,
                            rowNum - 1,
                            columnNum + 1,
                            False,
                        )
                    )

                if (
                    backwardsLeftStatus == "."
                ):  # check the square that is backwards and left of the piece, the using this particular player's left (board is flipped for red)
                    nonJumpingStates.append(
                        createSuccessor(
                            currentStateBoard,
                            currentPlayer,
                            rowNum,
                            columnNum,
                            rowNum + 1,
                            columnNum - 1,
                            False,
                        )
                    )

                if (
                    backwardsRightStatus == "."
                ):  # check the square that is backwards and right of the piece, the using this particular player's right (board is flipped for red)
                    nonJumpingStates.append(
                        createSuccessor(
                            currentStateBoard,
                            currentPlayer,
                            rowNum,
                            columnNum,
                            rowNum + 1,
                            columnNum + 1,
                            False,
                        )
                    )

                if (
                    forwardsLeftStatus.lower() == "r"
                    or forwardsRightStatus.lower() == "r"
                    or backwardsLeftStatus.lower() == "r"
                    or backwardsRightStatus.lower() == "r"
                ):
                    getJumps(
                        currentStateBoard,
                        currentPlayer,
                        rowNum,
                        columnNum,
                        True,
                        jumpingStates,
                        False,
                    )


    if len(jumpingStates) == 0:
        return nonJumpingStates
    else:
        return jumpingStates


def evaluateState(state: list, currentPlayer: str):
    # evaluate state criteria
    # win or loss criteria
    # run out of pieces
    # run out of moves
    # number of queens, number of pieces vs. opponent, number of center controlling pieces
    # how many squares of the back rank are controlled/number of home-row pieces
    # number of safe pieces eg. defended pieces

    evalNum = 0  # net
    redPieceValue = 0  # weighted piece value
    whiPieceValue = 0
    redInCenter = 0  # speical areas
    whiInCenter = 0
    redBackRank = 0
    whiBackRank = 0
    redProtected = 0  # if protected
    whiProtected = 0
    redEndangered = 0  # if about to be jumped
    whiEndangered = 0

    for rowNum in range(8):
        for columnNum in range(8):  # main loop through all pieces
            # tally pieces and add piece to row number function
            # pawns gain value as they approach the back rank up to a maximum of 1.75 ish, the value of a queen
            # check behind a piece to see if its protected, if not then check jumps

            redBackwardsLeft = checkBackwardsLeftSquare(
                state, "redMax", rowNum, columnNum
            )
            redBackwardsRight = checkBackwardsRightSquare(
                state, "redMax", rowNum, columnNum
            )
            redForwardsLeft = checkForwardsLeftSquare(
                state, "redMax", rowNum, columnNum
            )
            redForwardsRight = checkForwardsRightSquare(
                state, "redMax", rowNum, columnNum
            )

            whiBackwardsLeft = checkBackwardsLeftSquare(
                state, "whiMin", rowNum, columnNum
            )
            whiBackwardsRight = checkBackwardsRightSquare(
                state, "whiMin", rowNum, columnNum
            )
            whiForwardsLeft = checkForwardsLeftSquare(
                state, "whiMin", rowNum, columnNum
            )
            whiForwardsRight = checkForwardsRightSquare(
                state, "whiMin", rowNum, columnNum
            )


            if state[rowNum][columnNum] == "r":
                redPieceValue += 1 + (rowNum / 10)

                if redBackwardsLeft.lower() == "r" and redBackwardsRight.lower() == "r":
                    redProtected += 0.25
                elif (
                    (
                        redBackwardsLeft.lower() == "."
                        and redForwardsRight.lower() == "w"
                    )
                    or (
                        redBackwardsRight.lower() == "."
                        and redForwardsLeft.lower() == "w"
                    )
                    or (
                        redBackwardsLeft == "W"
                        and redForwardsRight.lower() == "."
                    )
                    or (
                        redBackwardsRight == "W"
                        and redForwardsLeft.lower() == "."
                    ) and currentPlayer=="whiMin"
                ):
                    redEndangered += 1

            elif state[rowNum][columnNum] == "R":
                redPieceValue += 1.75

                if redBackwardsLeft.lower() == "r" and redBackwardsRight.lower() == "r":
                    redProtected += 0.25
                elif (
                    (
                        redBackwardsLeft.lower() == "."
                        and redForwardsRight.lower() == "w"
                    )
                    or (
                        redBackwardsRight.lower() == "."
                        and redForwardsLeft.lower() == "w"
                    )
                    or (
                        redBackwardsLeft == "W"
                        and redForwardsRight.lower() == "."
                    )
                    or (
                        redBackwardsRight == "W"
                        and redForwardsLeft.lower() == "."
                    ) and currentPlayer=="whiMin"
                ):
                    redEndangered += 1

            elif state[rowNum][columnNum] == "w":
                whiPieceValue += 1 + ((7 - rowNum) / 10)

                if whiBackwardsLeft.lower() == "w" and whiBackwardsRight.lower() == "w":
                    whiProtected += 0.25
                elif (
                    (
                        whiBackwardsLeft.lower() == "."
                        and whiForwardsRight.lower() == "r"
                    )
                    or (
                        whiBackwardsRight.lower() == "."
                        and whiForwardsLeft.lower() == "r"
                    )
                    or (
                        whiBackwardsLeft == "R"
                        and whiForwardsRight.lower() == "."
                    )
                    or (
                        whiBackwardsRight == "R"
                        and whiForwardsLeft.lower() == "."
                    ) and currentPlayer=="redMax"
                ):
                    whiEndangered += 1

            elif state[rowNum][columnNum] == "W":
                whiPieceValue += 1.75

                if whiBackwardsLeft.lower() == "w" and whiBackwardsRight.lower() == "w":
                    whiProtected += 0.25
                elif (
                    (
                        whiBackwardsLeft.lower() == "."
                        and whiForwardsRight.lower() == "r"
                    )
                    or (
                        whiBackwardsRight.lower() == "."
                        and whiForwardsLeft.lower() == "r"
                    )
                    or (
                        whiBackwardsLeft== "R"
                        and whiForwardsRight.lower() == "."
                    )
                    or (
                        whiBackwardsRight == "R"
                        and whiForwardsLeft.lower() == "."
                    ) and currentPlayer=="redMax"
                ):
                    whiEndangered += 1

            # center pieces
            if (rowNum == 3 or rowNum == 4) and (columnNum >= 2 or columnNum <= 5):
                if state[rowNum][columnNum].lower() == "r":
                    redInCenter += 1
                elif state[rowNum][columnNum].lower() == "w":
                    whiInCenter += 1

            # back rank
            if rowNum == 0 and state[rowNum][columnNum].lower() == "r":
                redBackRank += 1
            if rowNum == 7 and state[rowNum][columnNum].lower() == "w":
                whiBackRank += 1

    # sum for evalNum
    evalNum = (
        redPieceValue * 10
        + redInCenter * 0.5
        + redBackRank * 3
        + redProtected * 2
        + whiEndangered * 1
    ) - (
        whiPieceValue * 10
        + whiInCenter * 0.5
        + whiBackRank * 3
        + whiProtected * 2
        + redEndangered * 1
    )
    # check for win
    winner = checkForWin(state, currentPlayer)

    if winner != -1:
        evalNum = winner

    return evalNum


def checkForWin(state: list, currentPlayer: str):
    whiMoves = len(getSuccessors(state, "whiMin"))
    redMoves = len(getSuccessors(state, "redMax"))

    # print(whiMoves, redMoves)

    numrR = 0
    numwW = 0

    for row in state:
        for piece in row:
            if piece.lower() == "r":
                numrR += 1
            elif piece.lower() == "w":
                numwW += 1

    if numrR == 0 or (currentPlayer == "redMax" and redMoves == 0):
        return float("-inf")
    elif numwW == 0 or (currentPlayer == "whiMin" and whiMoves == 0):
        return float("inf")
    return -1


def minimax(state: list, depth: int, currentPlayer: str, alpha:float, beta: float):

    # print("")
    # i=0
    # for line in state:
    #     collectedLine=""
    #     for square in line:
    #         collectedLine+=square
    #     print(collectedLine,i)
    #     i+=1

    if depth == 0 or checkForWin(state, currentPlayer) != -1:
        return evaluateState(state, currentPlayer), state

    if currentPlayer == "redMax":
        bestVal = float("-inf")
        bestMove = None
        for move in getSuccessors(state, currentPlayer):
            evalNum = minimax(move, depth - 1, "whiMin", alpha, beta)[0]

            
            bestVal = max(bestVal, evalNum)
            alpha = max(bestVal, evalNum)
            if bestVal == evalNum:
                bestMove = move
            if beta<=alpha:
                break

        return bestVal, bestMove


    if currentPlayer == "whiMin":
        bestVal = float("inf")
        bestMove = None
        for move in getSuccessors(state, currentPlayer):
            evalNum = minimax(move, depth - 1, "redMax", alpha, beta)[0]
            
            bestVal = min(bestVal, evalNum)
            beta = min(beta, evalNum)
            if bestVal == evalNum:
                bestMove = move
            if beta<=alpha:
                break

        return bestVal, bestMove



def gameLoop(state: list, currentPlayer: str):
    counter = 150
    
    updatedState = state
    while counter > 0 and checkForWin(updatedState, currentPlayer) == -1:
        evalNum, updatedState = minimax(
            updatedState, 6, currentPlayer, float("-inf"), float("inf")
        )
        print(checkForWin(updatedState, currentPlayer))

        if currentPlayer == "redMax":
            currentPlayer = "whiMin"
        else:
            currentPlayer = "redMax"


        counter -= 1

        gameFile = open("game.txt", "a")
        i = 0
        for row in updatedState:
            collectedRow = ""
            for piece in row:
                collectedRow += piece
            gameFile.write(collectedRow+"\n")
            i += 1

        gameFile.write("\n")
        gameFile.close()

        # display game in the console
        print(counter, currentPlayer, evalNum)

        i = 0
        for row in updatedState:
            collectedRow = ""
            for piece in row:
                collectedRow += piece
            print(collectedRow, i)
            i += 1

        print("")


createBoardArray()  # make testing file into board
testingState = State(createBoardArray())


# print("current state evaluation is:")
# evaluateState(testingState.board, player)

# for state in getSuccessors(testingState.board, player):

#     evaluateState(state, player)



#THIS LINE OF CODE WILL RUN THE AI AGAINST THE AI

# gameLoop(testingState.board, player)
