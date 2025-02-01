"""
Pygame Chess
Friday, June 17, 2022
Peter Ton

Assignment: Create a game with images and sounds using the pygame library
"""

# Import python libraries
import pygame
import math
import random
import copy

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Declare the surface
bg = pygame.display.set_mode((360, 360))
bg.fill((255, 255, 255))

# Declare game images
menuImage = pygame.image.load('sprites/menuImage.jpg')
titleText = pygame.image.load('sprites/titleText.png')
buttonImage1 = pygame.image.load('sprites/button1.jpg')
playerText1 = pygame.image.load('sprites/1player.png')
playerHoverText1 = pygame.image.load('sprites/1playerHover.png')
playerText2 = pygame.image.load('sprites/2player.png')
playerHoverText2 = pygame.image.load('sprites/2playerHover.png')

gameOverImage = pygame.image.load('sprites/gameOverBackground.jpg')
whiteWinText = pygame.image.load('sprites/whiteWins.png')
blackWinText = pygame.image.load('sprites/blackWins.png')
stalemateText = pygame.image.load('sprites/stalemate.png')
menuText = pygame.image.load('sprites/menu.png')
menuHoverText = pygame.image.load('sprites/menuHover.png')
rematchText = pygame.image.load('sprites/rematch.png')
rematchHoverText = pygame.image.load('sprites/rematchHover.png')

# Load chess piece images
wKingImage = pygame.image.load('sprites/Chess_klt45.svg.png')
bKingImage = pygame.image.load('sprites/Chess_kdt45.svg.png')
wQueenImage = pygame.image.load('sprites/Chess_qlt45.svg.png')
bQueenImage = pygame.image.load('sprites/Chess_qdt45.svg.png')
wRookImage = pygame.image.load('sprites/Chess_rlt45.svg.png')
bRookImage = pygame.image.load('sprites/Chess_rdt45.svg.png')
wBishopImage = pygame.image.load('sprites/Chess_blt45.svg.png')
bBishopImage = pygame.image.load('sprites/Chess_bdt45.svg.png')
wKnightImage = pygame.image.load('sprites/Chess_nlt45.svg.png')
bKnightImage = pygame.image.load('sprites/Chess_ndt45.svg.png')
wPawnImage = pygame.image.load('sprites/Chess_plt45.svg.png')
bPawnImage = pygame.image.load('sprites/Chess_pdt45.svg.png')

# Declare game sounds
moveSound = pygame.mixer.Sound('sounds/moveSound.mp3')
captureSound = pygame.mixer.Sound('sounds/captureSound.mp3')
errorSound = pygame.mixer.Sound('sounds/errorSound.mp3')

# Declare other variables
scene = "Menu"
transition = False
transitionVal = 0
currentScene = True
nextScene = ""

buttonGlow1 = False
buttonGlow2 = False

selectPos = [-1, -1]
pieceDrag = False
secondDrag = False
mousePos = []
prevMove = []
inCheck = False
boardPossibleMoves = []
allPossibleMoves = []
enPassant = False
enPassantPos = []

aiOpponent = False
timer = 0
inCheckTimer = 0
aiDepth = 3
aiTimer = 0
aiTurn = False
aiColour = "B"


board = []

# Piece Movement
rookPath = [
  [[0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7]],
  [[1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0]],
  [[0, -1], [0, -2], [0, -3], [0, -4], [0, -5], [0, -6], [0, -7]],
  [[-1, 0], [-2, 0], [-3, 0], [-4, 0], [-5, 0], [-6, 0], [-7, 0]],
];
knightPath = [
  [[1, 2]],
  [[2, 1]],
  [[2, -1]],
  [[1, -2]],
  [[-1, -2]],
  [[-2, -1]],
  [[-2, 1]],
  [[-1, 2]],
];
bishopPath = [
  [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7]],
  [[1, -1], [2, -2], [3, -3], [4, -4], [5, -5], [6, -6], [7, -7]],
  [[-1, 1], [-2, 2], [-3, 3], [-4, 4], [-5, 5], [-6, 6], [-7, 7]],
  [[-1, -1], [-2, -2], [-3, -3], [-4, -4], [-5, -5], [-6, -6], [-7, -7]],
];
queenPath = [
  [[0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7]],
  [[1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0]],
  [[0, -1], [0, -2], [0, -3], [0, -4], [0, -5], [0, -6], [0, -7]],
  [[-1, 0], [-2, 0], [-3, 0], [-4, 0], [-5, 0], [-6, 0], [-7, 0]],
  [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7]],
  [[1, -1], [2, -2], [3, -3], [4, -4], [5, -5], [6, -6], [7, -7]],
  [[-1, 1], [-2, 2], [-3, 3], [-4, 4], [-5, 5], [-6, 6], [-7, 7]],
  [[-1, -1], [-2, -2], [-3, -3], [-4, -4], [-5, -5], [-6, -6], [-7, -7]],
];
kingPath = [
  [[0, 1]],
  [[1, 1]],
  [[1, 0], [2, 0]],
  [[1, -1]],
  [[0, -1]],
  [[-1, -1]],
  [[-1, 0], [-2, 0]],
  [[-1, 1]],
];
pawnPath1 = [
  [[0, -1], [0, -2]],
  [[-1, -1]],
  [[1, -1]],
];
pawnPath2 = [
  [[0, 1], [0, 2]],
  [[-1, 1]],
  [[1, 1]],
];
pawnCheckPath1 = [
  [[-1, -1]],
  [[1, -1]],
]
pawnCheckPath2 = [
  [[-1, 1]],
  [[1, 1]],
]
kingCheckPath = [
  [[0, 1]],
  [[1, 1]],
  [[1, 0]],
  [[1, -1]],
  [[0, -1]],
  [[-1, -1]],
  [[-1, 0]],
  [[-1, 1]],
];


pieceValues = {"K": 1000, "Q": 9, "R": 5, "B": 3, "N": 3, "P": 1, " ": 0}
piecePaths = {"WK": kingPath, "WQ": queenPath, "WR": rookPath, "WB": bishopPath, "WN": knightPath, "WP": pawnPath1, "BK": kingPath, "BQ": queenPath, "BR": rookPath, "BB": bishopPath, "BN": knightPath, "BP": pawnPath2, "  ": []}


# Start a scene transition
def transitionScene(futureScene):
  global transition, transitionVal, currentScene, nextScene
  transition = True
  transitionVal = 0
  currentScene = True
  nextScene = futureScene

# Find if a player is in check
def findCheck(turn, currentBoard):
  x = -1
  y = -1
  # Look for the kings' positions
  for i in range(len(currentBoard)):
    for j in range(len(currentBoard[i])):
      if currentBoard[i][j] == turn + "K":
        x = j
        y = i
  
  checkPaths = [kingCheckPath, rookPath, bishopPath, knightPath]
  if turn == "W":
    checkPaths.append(pawnCheckPath1)
  elif turn == "B":
    checkPaths.append(pawnCheckPath2)
  
  # Loop through piece movements and find checks
  for currentPath in checkPaths:
    for i in range(len(currentPath)):
      blocked = False
      for j in range(len(currentPath[i])):
        currentX = x + currentPath[i][j][0]
        currentY = y + currentPath[i][j][1]
        
        if currentX >= 8 or currentX < 0 or currentY >= 8 or currentY < 0:
          break
        
        currentPiece = currentBoard[currentY][currentX]
        
        if currentPiece != "  ":
          blocked = True
        
        if currentPiece[0] != turn and currentPiece[0] != "  ":
          if currentPath == kingCheckPath:
            if currentPiece[1] == "K":
              return(True)
          elif currentPath == rookPath:
            if currentPiece[1] == "R" or currentPiece[1] == "Q":
              return(True)
          elif currentPath == bishopPath:
            if currentPiece[1] == "B" or currentPiece[1] == "Q":
              return(True)
          elif currentPath == knightPath:
            if currentPiece[1] == "N":
              return(True)
          elif currentPath == pawnCheckPath1 or currentPath == pawnCheckPath2:
            if currentPiece[1] == "P":
              return(True)
        if blocked == True:
          break
  return(False)


# Find the possible moves for a given piece
def findPossibleMoves(x, y, currentBoard, currentTurn):
  possibleMoves = []
  piece = currentBoard[y][x]
  currentPath = piecePaths[piece]
  blocked = False

  # Loop through the piece's movement
  for i in range(len(currentPath)):
    blocked = False
    for j in range(len(currentPath[i])):
      currentX = x + currentPath[i][j][0]
      currentY = y + currentPath[i][j][1]
      
      if currentX >= 8 or currentX < 0 or currentY >= 8 or currentY < 0:
        break

      currentPiece = currentBoard[currentY][currentX]
      
      if currentPiece != "  ":
        blocked = True

      if currentPiece[0] != currentTurn:
        if currentBoard[y][x][1] == "P":
          if i == 0:
            if currentPiece != "  ":
              break
          else:
            if currentPiece == "  ":
              if aiOpponent and currentTurn == aiColour:
                break
              if not enPassant:
                break
              else:
                if not (enPassantPos[1] == y and enPassantPos[0] == currentX):
                  break
              
          if j == 1:
            if currentTurn == "W" and y != 6:
              break
            elif currentTurn == "B" and y != 1:
              break
        if currentBoard[y][x][1] == "K":
          if j == 1:
            if currentPiece != "  ":
              break
            if findCheck(currentTurn, currentBoard):
              break
            if i == 2:
              if canCastle[1] == False and currentTurn == "W" or canCastle[3] == False and currentTurn == "B":
                break
            if i == 6:
              if canCastle[0] == False and currentTurn == "W" or canCastle[2] == False and currentTurn == "B":
                break

        # Look for checks
        checked = False
        futureBoard = copy.deepcopy(currentBoard)
        futureBoard[currentY][currentX] = futureBoard[y][x]
        futureBoard[y][x] = "  "
        if findCheck(currentTurn, futureBoard):
          checked = True
        else:
          if currentBoard[y][x][1] == "K" and abs(currentX - x) == 2:
            halfStep = int((currentX - x) / 2)
            
            futureBoard = copy.deepcopy(currentBoard)
            futureBoard[currentY][x + halfStep] = futureBoard[y][x]
            futureBoard[y][x] = "  "
            if findCheck(currentTurn, futureBoard):
              checked = True
        if checked == False:
          possibleMoves.append([currentX, currentY])

      # If the movement is blocked, break the loop
      if blocked == True:
        break
      
  return possibleMoves


# Find all possible moves given a board state
def findAllPossibleMoves(currentBoard, currentTurn):
  global allPossibleMoves
  allPossibleMoves = []
  for i in range(len(currentBoard)):
    for j in range(len(currentBoard[i])):
      if currentBoard[i][j][0] == currentTurn:
        possibleMoves = findPossibleMoves(j, i, currentBoard, currentTurn)
        if len(possibleMoves) > 0:
          for k in range(len(possibleMoves)):
            allPossibleMoves.append([j, i, possibleMoves[k][0], possibleMoves[k][1]])  
def findBoardPossibleMoves(currentBoard, currentTurn):
  global boardPossibleMoves
  boardPossibleMoves = []
  for i in range(len(currentBoard)):
    boardPossibleMoves.append([])
    for j in range(len(currentBoard[i])):
      boardPossibleMoves[i].append([])
      if currentBoard[i][j][0] == currentTurn:
        possibleMoves = findPossibleMoves(j, i, currentBoard, currentTurn)
        if len(possibleMoves) > 0:
          boardPossibleMoves[i][j] = possibleMoves 


# Move a piece
def movePiece(x1, y1, x2, y2):
  global board, gameTurn, turnNum, boardPossibleMoves, allPossibleMoves, prevMove, inCheck, inCheckTimer, enPassant, enPassantPos
  findBoardPossibleMoves(board, gameTurn)
  findAllPossibleMoves(board, gameTurn)
  halfStep = int((x2 - x1) / 2)
  
  if [x2, y2] in boardPossibleMoves[y1][x1]:
    if board[y2][x2] == "  ":
      moveSound.play()    
    else:
      captureSound.play()
    
    memBoard = board[y2][x2]
    board[y2][x2] = board[y1][x1]
    board[y1][x1] = "  "
    if memBoard[1] == "R":
      if x2 == 0 and y2 == 7:
        canCastle[0] = False
      elif x2 == 7 and y2 == 7:
        canCastle[1] = False
      elif x2 == 0 and y2 == 0:
        canCastle[2] = False
      elif x2 == 7 and y2 == 0:
        canCastle[3] = False
    
    if board[y2][x2][1] == "R":
      if x1 == 0 and y1 == 7:
        canCastle[0] = False
      elif x1 == 7 and y1 == 7:
        canCastle[1] = False
      elif x1 == 0 and y1 == 0:
        canCastle[2] = False
      elif x1 == 7 and y1 == 0:
        canCastle[3] = False
    elif board[y2][x2][1] == "K":
      if gameTurn == "W":
        canCastle[0:2] = [False, False]
        if abs(x2 - x1) == 2:
          board[y2][x1 + halfStep] = "WR"
          if x2 == 6:
            board[7][7] = "  "
          elif x2 == 2:
            board[7][0] = "  "
      elif gameTurn == "B":
        canCastle[2:4] = [False, False]
        if abs(x2 - x1) == 2:
          board[y2][x1 + halfStep] = "BR"
          if x2 == 6:
            board[0][7] = "  "
          elif x2 == 2:
            board[0][0] = "  "
    elif board[y2][x2][1] == "P":
      if gameTurn == "W" and y2 == 0:
        board[y2][x2] = "WQ"
      elif gameTurn == "B" and y2 == 7:
        board[y2][x2] = "BQ"

      if enPassant and x2 != x1:
        if enPassantPos[1] == y1 and enPassantPos[0] == x2:
          if gameTurn == "W":
            board[y2 + 1][x2] = "  "
          else:
            board[y2 - 1][x2] = "  "
      
      enPassant = False
      if abs(y2 - y1) == 2:
        enPassant = True
        enPassantPos = [x2, y2]
        
    
    if gameTurn == "W":
      gameTurn = "B"
    else:
      gameTurn = "W"
    
    turnNum += 0.5
    findAllPossibleMoves(board, gameTurn)
    findBoardPossibleMoves(board, gameTurn)
    prevMove = [x1, y1, x2, y2]
  else: # Illegal move
    errorSound.play()
    if findCheck(gameTurn, board):
      inCheck = True
      inCheckTimer = timer
    

# Evaluate the current board state
def evaluateBoard(currentBoard):
  score = 0
  for i in range(len(currentBoard)):
    for j in range(len(currentBoard[i])):
      piece = currentBoard[i][j]
      val = pieceValues[piece[1]]
      if piece[1] == "Q" and turnNum < 10:
        if piece[0] == "W" and i < 7:
          val -= 1
        elif piece[0] == "B" and i > 0:
          val -= 1
      if piece[0] == "W":
        score += val
      elif piece[0] == "B":
        score -= val
  if gameTurn == "B":
    return -score
  elif gameTurn == "W":
    return score

# Find the "best" move in a given position
def minimax(currentBoard, currentTurn, iteration, alpha, beta):
  bestMove = -1
  if gameTurn == "W":
    futureTurn = "B"
  else:
    futureTurn = "W"  
  
  currentAllPossibleMoves = []
  
  if iteration >= aiDepth:
    
    findAllPossibleMoves(currentBoard, currentTurn)
    currentAllPossibleMoves = allPossibleMoves
    if len(currentAllPossibleMoves) == 0:
      if findCheck(currentTurn, currentBoard):
        if currentTurn == gameTurn:
          return [-1, -1000 + iteration]
        else:
          return [-1, 1000 - iteration]
      else:
        return [-1, 0]
    currentScore = evaluateBoard(currentBoard)
    
    if currentTurn == gameTurn:
      currentScore += len(currentAllPossibleMoves) * 0.00001
    else:
      currentScore -= len(currentAllPossibleMoves) * 0.00001
    
    return [-1, currentScore]
    
  else:
    
    findAllPossibleMoves(currentBoard, currentTurn)
    currentAllPossibleMoves = allPossibleMoves
    if len(currentAllPossibleMoves) == 0:
      if findCheck(currentTurn, currentBoard):
        if currentTurn == gameTurn:
          return [-1, -1000 + iteration]
        else:
          return [-1, 1000 - iteration]
      else:
        return [-1, 0]

    
    if currentTurn == gameTurn:
      bestScore = -100000
      
      for i in range(len(currentAllPossibleMoves)):
        futureBoard = copy.deepcopy(currentBoard)
        
        currentMove = currentAllPossibleMoves[i]
        futureBoard[currentMove[3]][currentMove[2]] = futureBoard[currentMove[1]][currentMove[0]]
        futureBoard[currentMove[1]][currentMove[0]] = "  "
        if futureBoard[currentMove[3]][currentMove[2]][1] == "P":
          if currentTurn == "W" and currentMove[3] == 0:
            futureBoard[currentMove[3]][currentMove[2]] = "WQ"
          elif currentTurn == "B" and currentMove[3] == 7:
            futureBoard[currentMove[3]][currentMove[2]] = "BQ"          
        
        minimaxVal = minimax(futureBoard, futureTurn, iteration + 1, alpha, beta)
        currentScore = minimaxVal[1]
        currentScore += random.randrange(-1, 1) * 0.0001 / (turnNum + 2)
      
        if currentScore > bestScore:
          bestMove = i
          bestScore = currentScore

        alpha = max(alpha, bestScore)
        if beta <= alpha:
          break
    else:
      bestScore = 100000
      
      for i in range(len(currentAllPossibleMoves)):
        futureBoard = copy.deepcopy(currentBoard)
        
        currentMove = currentAllPossibleMoves[i]
        futureBoard[currentMove[3]][currentMove[2]] = futureBoard[currentMove[1]][currentMove[0]]
        futureBoard[currentMove[1]][currentMove[0]] = "  "
        if futureBoard[currentMove[3]][currentMove[2]][1] == "P":
          if currentTurn == "W" and currentMove[3] == 0:
            futureBoard[currentMove[3]][currentMove[2]] = "WQ"
          elif currentTurn == "B" and currentMove[3] == 7:
            futureBoard[currentMove[3]][currentMove[2]] = "BQ"          
      
        minimaxVal = minimax(futureBoard, gameTurn, iteration + 1, alpha, beta)
        currentScore = minimaxVal[1]
        currentScore += random.randrange(-1, 1) * 0.0001 / (turnNum + 2)
        
        if currentScore < bestScore:
          bestMove = i
          bestScore = currentScore
          
        beta = min(beta, bestScore)
        if beta <= alpha:
          break
  return [bestMove, bestScore]

# Draw the board graphics
def drawBoard():
  global inCheck
  
  # Display board and chess pieces
  for i in range(8):
    for j in range(8):
      if (i + j) % 2 == 0:
        colour = (255, 255, 230)
      else:
        colour = (100, 150, 70)  
      pygame.draw.rect(bg, colour, (j * 45, i * 45, 45, 45))

      # If a piece is currently selected
      if pieceDrag or selectPos != [-1, -1]:
        # Display the possible moves
        for k in boardPossibleMoves[selectPos[1]][selectPos[0]]:
          if k[0] == j and k[1] == i:
            highLight = pygame.Surface((45, 45))
            highLight.set_alpha(70)
            highLight.fill((255, 255, 0))
            bg.blit(highLight, (j * 45, i * 45)) 
        if j == selectPos[0] and i == selectPos[1]:
          highLight = pygame.Surface((45, 45))
          highLight.set_alpha(100)
          highLight.fill((255, 255, 0))
          bg.blit(highLight, (j * 45, i * 45))
      if prevMove != []:
        if prevMove[0] == j and prevMove[1] == i or prevMove[2] == j and prevMove[3] == i:
          highLight = pygame.Surface((45, 45))
          highLight.set_alpha(100)
          highLight.fill((255, 255, 0))
          bg.blit(highLight, (j * 45, i * 45))
      if inCheck and board[i][j] == gameTurn + "K":
        checkTime = (timer - inCheckTimer)
        if math.floor(checkTime / 20) % 2 == 0:
          highLight = pygame.Surface((45, 45))
          highLight.set_alpha(150)
          highLight.fill((255, 0, 0))
          bg.blit(highLight, (j * 45, i * 45))
        if checkTime > 120:
          inCheck = False
      
      if board[i][j] == "WK":
        image = wKingImage
      elif board[i][j] == "BK":
        image = bKingImage
      elif board[i][j] == "WQ":
        image = wQueenImage
      elif board[i][j] == "BQ":
        image = bQueenImage
      elif board[i][j] == "WR":
        image = wRookImage
      elif board[i][j] == "BR":
        image = bRookImage
      elif board[i][j] == "WB":
        image = wBishopImage
      elif board[i][j] == "BB":
        image = bBishopImage
      elif board[i][j] == "WN":
        image = wKnightImage
      elif board[i][j] == "BN":
        image = bKnightImage
      elif board[i][j] == "WP":
        image = wPawnImage
      elif board[i][j] == "BP":
        image = bPawnImage
      
      if board[i][j] != "  ":
        if not ((pieceDrag or secondDrag) and selectPos[0] == j and selectPos[1] == i and selectPos != [-1, -1]):
          bg.blit(image, (j * 45, i * 45))

  # Draw the selected piece on top of the board
  if selectPos != [-1, -1] and (pieceDrag or secondDrag):
    i = selectPos[1]
    j = selectPos[0]
    if board[i][j] == "WK":
      image = wKingImage
    elif board[i][j] == "BK":
      image = bKingImage
    elif board[i][j] == "WQ":
      image = wQueenImage
    elif board[i][j] == "BQ":
      image = bQueenImage
    elif board[i][j] == "WR":
      image = wRookImage
    elif board[i][j] == "BR":
      image = bRookImage
    elif board[i][j] == "WB":
      image = wBishopImage
    elif board[i][j] == "BB":
      image = bBishopImage
    elif board[i][j] == "WN":
      image = wKnightImage
    elif board[i][j] == "BN":
      image = bKnightImage
    elif board[i][j] == "WP":
      image = wPawnImage
    elif board[i][j] == "BP":
      image = bPawnImage
  
    
    bg.blit(image, (mousePos[0] - 45 / 2, mousePos[1] - 45 / 2))

# Initialize the chess game
def gameInit ():
  # Reset the board, turn number, and other variables
  global board, turnNum, gameTurn, canCastle, timer, gameOver
  board = [
    ["BR", "BN", "BB", "BQ", "BK", "BB", "BN", "BR"],
    ["BP", "BP", "BP", "BP", "BP", "BP", "BP", "BP"],
    ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "], 
    ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "], 
    ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "], 
    ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "], 
    ["WP", "WP", "WP", "WP", "WP", "WP", "WP", "WP"],
    ["WR", "WN", "WB", "WQ", "WK", "WB", "WN", "WR"]
  ]
  turnNum = 0
  gameTurn = "W"
  canCastle = [True, True, True, True]
  timer = 0
  gameOver = False

  # Find the possible moves and draw the board
  findAllPossibleMoves(board, gameTurn)
  findBoardPossibleMoves(board, gameTurn)
  drawBoard()  


# Main loop
while True:
  # Code is organized based on current scene
  if scene == "Menu":
    # Display the menu and buttons
    bg.blit(menuImage, (-310, -20))
    bg.blit(titleText, (145, 20))
    bg.blit(buttonImage1, (175, 120))
    bg.blit(buttonImage1, (175, 170))
    
    eventList = pygame.event.get()
    mousePos = pygame.mouse.get_pos()

    # Display button text and button functionalities
    if mousePos[0] >= 175 and mousePos[0] < 305 and mousePos[1] >= 120 and mousePos[1] < 165:
      for i in eventList:
        if i.type == pygame.MOUSEBUTTONDOWN:
          if transition == False:
            transitionScene("Game")
            aiOpponent = True
      
      bg.blit(playerHoverText1, (180, 125))
    else: 
      bg.blit(playerText1, (180, 125))
    
    if mousePos[0] >= 175 and mousePos[0] < 305 and mousePos[1] >= 170 and mousePos[1] < 215:
      for i in eventList:
        if i.type == pygame.MOUSEBUTTONDOWN:
          if transition == False:
            transitionScene("Game")
            aiOpponent = False
      
      bg.blit(playerHoverText2, (180, 175))
    else: 
      bg.blit(playerText2, (180, 175))
    
  elif scene == "GameOver":
    # Display game over screen and buttons
    
    bg.blit(gameOverImage, (0, 0))
    if gameOver == "W":
      bg.blit(whiteWinText, (6, 50))
    elif gameOver == "B":
      bg.blit(blackWinText, (10, 50))
    else:
      bg.blit(stalemateText, (30, 50))
    
    bg.blit(buttonImage1, (115, 160))
    bg.blit(buttonImage1, (115, 210))
    
    eventList = pygame.event.get()
    mousePos = pygame.mouse.get_pos()    

    # Display button text and button functionalities
    if mousePos[0] >= 115 and mousePos[0] < 245 and mousePos[1] >= 160 and mousePos[1] < 205:
      for i in eventList:
        if i.type == pygame.MOUSEBUTTONDOWN:
          if transition == False:
            transitionScene("Game")
      
      bg.blit(rematchHoverText, (117, 165))
    else: 
      bg.blit(rematchText, (117, 165))
    
    if mousePos[0] >= 115 and mousePos[0] < 245 and mousePos[1] >= 210 and mousePos[1] < 255:
      for i in eventList:
        if i.type == pygame.MOUSEBUTTONDOWN:
          if transition == False:
            transitionScene("Menu")
            
      bg.blit(menuHoverText, (140, 215))
    else: 
      bg.blit(menuText, (140, 215))
    
    
  elif scene == "Game":
    timer += 1

    # Look for checkmate
    if len(allPossibleMoves) == 0:
      if findCheck(gameTurn, board):
        if gameTurn == "W" and gameOver == False:
          gameOver = "B"
          gameOverTimer = timer
        elif gameTurn == "B" and gameOver == False:
          gameOver = "W"
          gameOverTimer = timer
      elif gameOver == False:
        gameOver = " "
        gameOverTimer = timer
      
      if timer - gameOverTimer > 250 and transition == False:
        transitionScene("GameOver")

    # Run opponent AI
    elif aiOpponent:
      if gameTurn == aiColour:
        if aiTurn == False:
          aiTurn = True
          aiTimer = timer
  
          findAllPossibleMoves(board, gameTurn)
          minimaxVal = minimax(board, gameTurn, 0, -100000, 100000)
          bestMove = minimaxVal[0]
          
          findAllPossibleMoves(board, gameTurn)
          rMove = allPossibleMoves[bestMove]
          
      if aiTurn and timer - aiTimer > 0:
        movePiece(rMove[0], rMove[1], rMove[2], rMove[3])
        aiTurn = False  
        
    
    eventList = pygame.event.get()
    mousePos = pygame.mouse.get_pos()
    
    # User input
    for i in eventList:
      if i.type == pygame.MOUSEBUTTONDOWN:
        squarePos = [math.floor(mousePos[0] / 45), math.floor(mousePos[1] / 45)]
  
        if selectPos == [-1, -1]:
          if board[squarePos[1]][squarePos[0]][0] == gameTurn:
            pieceDrag = True
            selectPos = squarePos
        else:
          if selectPos == squarePos:
            secondDrag = True
          elif board[squarePos[1]][squarePos[0]][0] == gameTurn:
            pieceDrag = True
            selectPos = squarePos
        
      elif i.type == pygame.MOUSEBUTTONUP:
        squarePos = [math.floor(mousePos[0] / 45), math.floor(mousePos[1] / 45)]
        
        if secondDrag == True and selectPos == squarePos:
          selectPos = [-1, -1]        
        
        if pieceDrag:
          pieceDrag = False
          
          if selectPos != squarePos:
            if board[squarePos[1]][squarePos[0]][0] != gameTurn:
              movePiece(selectPos[0], selectPos[1], squarePos[0], squarePos[1])
            selectPos = [-1, -1]
        else:
          if selectPos != [-1, -1]:
            if board[squarePos[1]][squarePos[0]][0] == gameTurn:
              selectPos = squarePos
            else:
              movePiece(selectPos[0], selectPos[1], squarePos[0], squarePos[1])
              selectPos = [-1, -1]
        secondDrag = False
    
    drawBoard()
    

  # Scene fade transitions
  if transition:
    if currentScene:
      transitionVal += (257 - transitionVal) * 0.01
      if transitionVal > 255:
        currentScene = False
        scene = nextScene
        if scene == "Game":
          gameInit()
    else:
      transitionVal += (-2 - transitionVal) * 0.01
      if transitionVal < 0:
        transition = False
    
    fade = pygame.Surface((360, 360))
    fade.set_alpha(transitionVal)
    fade.fill((0, 0, 0))
    bg.blit(fade, (0, 0))
    
  pygame.display.flip()
      
