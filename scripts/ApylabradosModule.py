def startGame():
    """
    Inicializa todas las variables para comenzar una nueva partida
    """
    # Creamos las variables booleana end, show_help y show_help_plus
    global end
    end = False
    global show_help
    show_help = True
    global show_help_plus
    show_help_plus = True
    
    # Creamos la bolsa de fichas del juego
    global bag_of_pawns
    bag_of_pawns = Pawns()
    bag_of_pawns.createBag()

    # Creamos las fichas del jugador
    global player_pawns
    player_pawns = Pawns()

    # Creamos el tablero de juego
    global board
    board = Board()
    Board.score = 0
    board.setUpMultiplier()

    # Mensaje de bienvenida e instrucciones
    welcome()
    instructions()
    deal7Pawns()
    board.showBoard()
    legend()
    
    
    
def welcome():
    """
    Muestra el mensaje de bienvenida para la primera vez que empezamos a jugar
    """
    filepath = "/content/drive/MyDrive/Colab Notebooks/Proyecto Final Udemy/scripts/welcome_message.txt"
    with open(filepath, "r") as f:
        print(f.read())
        
        
        
def instructions():
    """
    Muestra las instrucciones de la partida de Apylabrados
    """
    filepath = "/content/drive/MyDrive/Colab Notebooks/Proyecto Final Udemy/scripts/instructions_message.txt"
    with open(filepath, "r") as f:
        print(f.read())
        


def deal7Pawns():
    """
    Reparte fichas al jugador hasta completar las 7 de su mano actual
    """
    while(player_pawns.getTotalPawns() < 7):
        player_pawns.addPawn(bag_of_pawns.takeRandomPawn())
    
    
    
def showOptions():
    """
    Muestra las opciones en caso de que todavía no haya palabra introducida
    """
    global show_help
    filepath = "/content/drive/MyDrive/Colab Notebooks/Proyecto Final Udemy/scripts/options_message.txt"
    print("\n¿Qué deseas hacer? {}".format("" if show_help else "(Introduce SHOWHELP para ver las diferentes opciones)"))
    if show_help:
        with open(filepath, "r") as f:
            print(f.read())
        show_help = False
    ans = input().upper()
    if ans == "SHOWHELP":
        show_help = True
        showOptions()
    elif ans == "ENTERWORD":
        introduceNewWord()
    elif ans == "MYPAWNS":
        print("Estas son tus fichas:")
        player_pawns.showPawns()
        showOptions()
    elif ans == "MYSCORE":
        print("Puntos: {}".format(Board.score))
        showOptions()
    elif ans == "PAWNSPOINTS":
        Pawns.showPawnsPoints()
        showOptions()
    elif ans == "HELPWORD":
        helpWithWords()
        showOptions()
    elif ans == "HELPLEGEND":
        legend()
        showOptions()
    elif ans == "QUITGAME":
        endGame()
    else:
        showOptions()
        
        
        
def showOptionsPlus():
    """
    Muestra las opciones en caso de que haya palabra introducida para colocar en el tablero
    """
    global show_help_plus
    filepath = "/content/drive/MyDrive/Colab Notebooks/Proyecto Final Udemy/scripts/options_plus_message.txt"
    print("\n¿Qué deseas hacer? {}".format("" if show_help_plus else "(Introduce SHOWHELP para ver las diferentes opciones)"))
    if show_help_plus:
        with open(filepath, "r") as f:
            print(f.read())
        show_help_plus = False
    ans = input().upper()
    if ans == "SHOWHELP":
        show_help_plus = True
        showOptionsPlus()
    elif ans == "ENTERPOSITION":
        introduceCoordinatesAndDirection()
    elif ans == "ENTERWORD":
        introduceNewWord()
    elif ans == "MYPAWNS":
        print("Estas son tus fichas:")
        player_pawns.showPawns()
        showOptionsPlus()
    elif ans == "MYSCORE":
        print("Puntos: {}".format(Board.score))
        showOptionsPlus()
    elif ans == "PAWNSPOINTS":
        Pawns.showPawnsPoints()
        showOptionsPlus()
    elif ans == "HELPWORD":
        helpWithWords()
        showOptionsPlus()
    elif ans == "HELPPOS":
        helpWithPosition()
        showOptionsPlus()
    elif ans == "HELPLEGEND":
        legend()
        showOptionsPlus()
    elif ans == "QUITGAME":
        endGame()
    else:
        showOptionsPlus()
        
        
        
def helpWithWords():
    """
    Muestra las posibles palabras que se pueden formar con las fichas disponibles del jugador
    y las que ya hay colocadas en el tablero
    """
    print("Estas son las posibles palabras a formar:")
    if board.totalWords == 0:
        Dictionary.showWords(player_pawns)
    else:
        board_letters = []
        for i in range(15):
            for j in range(15):
                if board.board[i][j] != " " and board.board[i][j] not in board_letters:
                    board_letters.append(board.board[i][j])
                    Dictionary.showWordsPlus(player_pawns, board.board[i][j])



def helpWithPosition():
    """
    Muestra las posibles colocaciones en el tablero de la palabra introducida
    """
    print("Estas son las posibles colocaciones")
    board.showWordPlacement(player_pawns, new_word)
    
    
    
def introduceNewWord():
    """
    Permite que el usuario introduzca una nueva palabra por consola
    y comprueba que existe en el diccionario, y que puede formarse con las 
    fichas de que dispone el jugador y las ubicadas sobre el tablero. 
    """
    print("Introduce tu palabra:")
    global new_word
    new_word = Word.readWord()
    new_word_ft = new_word.getFrequency()
    player_pawns_ft = player_pawns.getFrequency()
    isInDictionary = Dictionary.validateWord(new_word)
    
    if board.totalWords == 0:
        newWordIsSubset = FrequencyTable.isSubset(new_word_ft, player_pawns_ft)
    else:
        board_letters = []
        forcedBreak = False
    
        for i in range(15):
            if forcedBreak:
                break
            for j in range(15):
                if board.board[i][j] != " " and board.board[i][j] not in board_letters:
                    board_letters.append(board.board[i][j])
                    player_pawns_plus = player_pawns_ft
                    player_pawns_plus.update(board.board[i][j])
                    newWordIsSubset = FrequencyTable.isSubset(new_word_ft, player_pawns_plus)
                    player_pawns_plus.delete(board.board[i][j])
                    
                    if newWordIsSubset:
                        forcedBreak = True
                        break
    
    if not isInDictionary or not newWordIsSubset:
        if not newWordIsSubset:
            print("No puedes formar esa palabra con tus fichas")
        showOptions()
    else:
        showOptionsPlus()
        
        
        
def introduceCoordinatesAndDirection():
    """
    Permite al jugador introducir por consola la posición y orientación de una palabra.
    Comprueba si la palabra se puede colocar en dicha ubicación.
    """
    print("Introduce coordenada de la fila: ", end = " ")
    x = int(input())
    print("Introduce coordenada de la columna: ", end = " ")
    y = int(input())
    print("Introduce dirección: ", end = " ")
    direction = input().upper()
    
    if direction != "V" and direction != "H":
        print("Recuerda: solamente hay dos posibles direcciones para colocar las palabras: V (vertical) y H (horizontal)")
        showOptionsPlus()

    possible, message = board.isPossible(new_word, x, y, direction)
    if not possible:
        print(message)
        showOptionsPlus()
    else:
        needed_pawns = board.getPawns(new_word, x, y, direction)
        if FrequencyTable.isSubset(needed_pawns.getFrequency(), player_pawns.getFrequency()):
            board.placeWord(player_pawns, new_word, x, y, direction)
            board.showBoard()
        else:
            print("Las fichas de que dispones no son suficientes")
            showOptionsPlus()
            
  
      
def legend():
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
      
    def generate_vertex(center_x, center_y):
        vertex = np.array([[center_x - 0.5, center_y - 0.5], [center_x - 0.5, center_y + 0.5],
                        [center_x + 0.5, center_y + 0.5], [center_x + 0.5, center_y - 0.5]])
        return vertex

    def transformationX(x):
        return x / 16

    def transformationY(x):
        return (x + 1) / 3

    fig = plt.figure(figsize = [10, 2])
    ax = fig.add_subplot(111)

    ax.set_xlim(0, 16)
    ax.set_ylim(-1, 2)

    # Escalamos para que la parrilla ocupe toda la figura
    ax.set_position([0, 0, 1, 1])

    # Nos deshacemos de los ejes
    ax.set_axis_off()

    colors = ["#FFCCCC", "#B2FFCD", "#CCCEFF", "#CCF9FF"]
    texts = ["x3\nPalabra", "x2\nPalabra", "x3\nLetra", "x2\nLetra"]
    for i in range(4):
        polygon = plt.Polygon(generate_vertex(1.5 + 4 * i, 0.5), color = colors[i])
        ax.add_artist(polygon)
        ax.text(transformationX(3.5 + 4 * i), transformationY(.5), texts[i],
            verticalalignment = "center", horizontalalignment = "center",
            fontsize = 25, fontfamily = "fantasy", fontweight = "bold",
            transform = ax.transAxes)

    plt.show()
    


      
def endGame():
    """
    Finaliza la partida actual
    """
    print("Fin del juego")
    global end
    end = True
    
    
    
class Pawns():
    points = {"A": 1, "B": 3, "C": 3, "D": 2, "E": 1, "F": 4, "G": 2, "H": 4, "I": 1,
          "J": 8, "K": 5, "L": 1, "M": 3, "N": 1, "O": 1, "P": 3, "Q": 10, "R": 1,
          "S": 1, "T": 1, "U": 1, "V": 4, "W": 4, "X": 8, "Y": 4, "Z": 10
          }
          
    def __init__(self):
        self.letters = []
        
    def addPawn(self,c):
        self.letters.append(c)
        
    def addPawns(self,c,n):
        for i in range(n):
            self.addPawn(c)
            
    def createBag(self):
        import pandas as pd
        
        filepath = "/content/drive/MyDrive/Colab Notebooks/Proyecto Final Udemy/scripts/bag_of_pawns.csv"
        bag = pd.read_csv(filepath)
        
        for i in bag.itertuples():
            self.addPawns(i[1], i[2])
            
    def showPawns(self):
        """
        Muestra las fichas que contiene la bolsa y el número de veces que está repetida cada ficha
        """
        ft_pawns = self.getFrequency()
        ft_pawns.showFrequency()
    
                
    def takeRandomPawn(self):
        from numpy import random
        
        idx = random.randint(0, len(self.letters) - 1)
        letter = self.letters[idx]
        self.letters.remove(letter)
        return letter
        
    def takePawn(self, c):
        """
        Toma la ficha c de la bolsa y la elimina de ella
        """
        self.letters.remove(c)
        
    def getTotalPawns(self):
        """
        Total fichas del saco
        """
        return len(self.letters)
        
    def getFrequency(self):
        """
        Muestra frecuencia de aparación de cada ficha
        """
        ft = FrequencyTable()
        for c in self.letters:
            ft.update(c)
        return ft
        
    @staticmethod
    def getPoints(c):
        """
        Devuelve los puntos de la ficha c
        """
        return Pawns.points[c]
        
    @staticmethod
    def showPawnsPoints():
        """
        Muestra por pantalla la puntuación de cada ficha
        """
        
        print("Puntos de cada ficha:")
        count = 0
        end = "   "
        
        for key in Pawns.points:
            print("{}:{}{}".format(key, " " if Pawns.getPoints(key) < 9 else "", Pawns.getPoints(key)), end = end)
            count += 1
            end = "\n" if count % 3 == 2 else "   "
    
      
        
class Word():
    def __init__(self):
        self.word = []
    
    def __str__(self):
        """
        Imprimimos la palabra en formato string
        """
        string = ""
        for i in range(len(self.word)):
            string += self.word[i]
        return string

    def areEqual(self, w):
        """
        Comprueba si dos palabras son iguales
        """
        return self.word == w.word
      
    def isEmpty(self):
        """ 
        Comprueba si una palabra es vacía
        """
        return len(self.word) == 0
          
    @classmethod
    def readWord(cls):
        """
        Lee una palabra por teclado y la devuelve como un objeto de la clase Word
        """
        input_word = input().strip()
        w = Word()
        for c in input_word.upper():
            w.word.append(c)
        return w
        
    @staticmethod
    def readWordFromFile(f):
        """
        Lee una palabra del fichero y la devuelve como un objeto dela clase Word
        """
        w = Word()
        file_word = f.readline()
        # Tenemos en cuenta toda la línea, excepto el salto de línea final -- Sólo tenemos en cuenta la palabra
        for i in file_word[:-1]:
            w.word.append(i)
        return w
    
    def getFrequency(self):
        """
        Muestra frecuencia de aparación de cada letra en una palabra
        """
        ft = FrequencyTable()
        for c in self.word:
            ft.update(c)
        return ft
    
    def getLengthWord(self):
        """
        Devuelve la longitud de la palabra
        """
        return len(self.word)
    
   
    
class Dictionary():
    
    filepath = "/content/drive/MyDrive/Colab Notebooks/Proyecto Final Udemy/scripts/dictionary.txt"
        
    @staticmethod
    def validateWord(word):
        """
        Comprueba si la palabra se encuentra dentro del diccionario
        """
        with open(Dictionary.filepath, "r") as f:
            w = Word.readWordFromFile(f)
            while(not w.isEmpty() and not word.areEqual(w)):
                w = Word.readWordFromFile(f)
                
        if w.isEmpty() and not word.areEqual(w):
            print("La palabra no se encuentra en el diccionario")
            return False
            
        else:
            return True
            
    @staticmethod
    def showWords(pawns):
        """
        Muestra todas las posibles palabras que se pueden formar con las fichas de pawns
        """
        tf_pawns = pawns.getFrequency()
        count = 0
        end = " "
        with open(Dictionary.filepath, "r") as f:
            word = Word.readWordFromFile(f)
            while (not word.isEmpty()):
                n = word.getLengthWord()
                tf_word = word.getFrequency()
                if FrequencyTable.isSubset(tf_word, tf_pawns):
                    print(word, end = end * (10 - n) if end == " " else end)
                    count += 1
                    end = "\n" if count % 5 == 4 else " "
                word = Word.readWordFromFile(f)
            
    
    @staticmethod
    def showWordsPlus(pawns, c):
        """
        Muestra todas las posibles palabras que contienen el caracter c y que se pueden formar con las fichas de pawns
        """
        tf_pawns = pawns.getFrequency()
        tf_pawns.update(c)
        count = 0
        end = " "
        with open(Dictionary.filepath, "r") as f:
            word = Word.readWordFromFile(f)
            while (not word.isEmpty()):
                n = word.getLengthWord()
                if c in word.word:
                    tf_word = word.getFrequency()
                    if FrequencyTable.isSubset(tf_word, tf_pawns):
                        print(word, end = end * (10 - n) if end == " " else end)
                        count += 1
                        end = "\n" if count % 5 == 4 else " "
                word = Word.readWordFromFile(f)
        print("")
        
        
        
class FrequencyTable():
    def __init__(self):
        self.letters = [chr(x) for x in range(ord("A"), ord("Z") + 1)]
        self.frequencies = [0 for _ in range(len(self.letters))]

    def showFrequency(self):
        """
        Muestre la frecuencia de aquellas letras con frecuencia distinta de 0.
        """
        for i in range(len(self.letters)):
            if self.frequencies[i] !=0:
                print("{}:{}".format(self.letters[i], self.frequencies[i]))
                
    @staticmethod
    def isSubset(ft1, ft2):
        """
        Comprueba si ft1 es subconjunto de ft2
        """
        for i in range(len(ft1.frequencies)):
            if ft1.frequencies[i] > ft2.frequencies[i]:
                return False
        return True
        
    def update(self, c):
        """
        Actualiza frequencia de la letra que pasamos por parámetro,c
        """
        idx = self.letters.index(c)
        self.frequencies[idx] +=1
        
        
    def delete(self, c):
        """
        Actualiza la frecuencia de la letra c que pasemos por parámetro (resta 1)
        """
        idx = self.letters.index(c)
        self.frequencies[idx] -= 1



class Board():
    score = 0
    
    def __init__(self):
        self.board = [[" " for j in range(15)] for i in range(15)]
        self.totalWords = 0
        self.totalPawns = 0
        self.multiplier = [[(1, "") for j in range(15)] for i in range(15)]
        
    def setUpMultiplier(self):
        """
        Configura el multiplicador de cada casilla
        """
        import pandas as pd
        filepath = "/content/drive/MyDrive/Colab Notebooks/Proyecto Final Udemy/scripts/multiplier_board.csv"
        multipliers = pd.read_csv(filepath)
        for row in multipliers.itertuples():
            self.multiplier[row[1]][row[2]] = (row[3], row[4])
        
    def showBoard(self):
        # Cargamos las librerías que nos harán falta
        import matplotlib.pyplot as plt
        import numpy as np
        import pandas as pd
        
        def generate_vertex(center_x, center_y):
            vertex = np.array([[center_x - 0.5, center_y - 0.5], [center_x - 0.5, center_y + 0.5],
                       [center_x + 0.5, center_y + 0.5], [center_x + 0.5, center_y - 0.5]])
            return vertex
    
        # Función que pasa del intervalo [-1, 16] al intervalo [0, 1]
        def transformation(x):
            return (x + 1)/17
            
        filepath = "/content/drive/MyDrive/Colab Notebooks/Proyecto Final Udemy/scripts/xycolor_board.csv"
        xycolors = pd.read_csv(filepath)

        # Creamos la figura de plt que guardará el tablero
        fig = plt.figure(figsize = [10, 10])
        ax = fig.add_subplot(111)

        # Dibujamos las rectas verticales y horizontales
        for x in range(16):
            ax.plot([x, x], [0, 15], 'k')
        for y in range(16):
            ax.plot([0, 15], [y, y], 'k')

        # Redefinimos los límites de los ejes
        ax.set_xlim(-1, 16)
        ax.set_ylim(-1, 16)

        # Escalamos para que la parrilla ocupe toda la figura
        ax.set_position([0, 0, 1, 1])

        # Nos deshacemos de los ejes
        ax.set_axis_off()
        
        for row in xycolors.itertuples():
            polygon = plt.Polygon(generate_vertex(row[1], row[2]), color = row[3])
            ax.add_artist(polygon)


        for i in range(len(self.board)):
            # números de arriba
            ax.text(transformation(i + 0.5), transformation(15.5), str(i),
              verticalalignment = "center", horizontalalignment = "center",
              fontsize = 20, fontfamily = "fantasy", fontweight = "bold",
              transform = ax.transAxes)
            # números de la derecha
            ax.text(transformation(15.5), transformation(i + 0.5), str(14 - i),
              verticalalignment = "center", horizontalalignment = "center",
              fontsize = 20, fontfamily = "fantasy", fontweight = "bold",
              transform = ax.transAxes)
            # letras
            for j in range(len(self.board)):
                ax.text(transformation(j + 0.5), transformation(14 - i + 0.5), self.board[i][j],
                  verticalalignment = "center", horizontalalignment = "center",
                  transform = ax.transAxes, fontsize = 15)
                  
        ax.text(transformation(0), transformation(-0.5), "Score: {}".format(Board.score),
          verticalalignment = "center", horizontalalignment = "left",
          fontsize = 25, fontfamily = "fantasy", fontweight = "bold",
          transform = ax.transAxes)
          
        deal7Pawns()
          
        pawn_pos = 4
        for pawn in player_pawns.letters:
            polygon = plt.Polygon(generate_vertex(pawn_pos, -0.6), color = "#FFF68F")
            ax.add_artist(polygon)
            ax.text(transformation(pawn_pos), transformation(-0.6), pawn,
            verticalalignment = "center", horizontalalignment = "center",
            transform = ax.transAxes, fontsize = 15)
            pawn_pos += 1.5

        plt.show()

    def placeWord(self, player_pawns, word, x, y, direction):
        """
        Colocamos la palabra word sobre el tablero y eliminamos las fichas usadas de la bolsa del jugador
        """
        word_points = 0
        word_multiplier = 1
        
        for letter in word.word:
            if letter != self.board[x][y]:
                player_pawns.takePawn(letter)
                self.totalPawns += 1
                self.board[x][y] = letter
                if self.multiplier[x][y][1] != "w":# multiplicador de pawn o nada
                    word_points += Pawns.getPoints(letter) * self.multiplier[x][y][0]
                else:# multiplicador de word
                    word_points += Pawns.getPoints(letter)
                    word_multiplier *= self.multiplier[x][y][0]
                
            if direction == "V":
                x += 1
            if direction == "H":
                y += 1
        
        
        Board.score += word_points * word_multiplier        
        self.totalWords += 1
     
    def isPossible(self, word, x, y, direction):
        """
        Comprueba si es posible colocar la palabra word en la posición y dirección proporcionadas
        """
        message = ""
        x0 = x
        y0 = y

        # Si es el primer turno, comprobamos si alguna ficha se sitúa sobre la casilla central
        
        if self.totalWords == 0:
            message = "Ninguna ficha pasa por la casilla central"
            if direction == "V":
                if y0 != 7:
                    return (False, message)
                elif x0 + word.getLengthWord() - 1 < 7 or x0 > 7:
                    return (False, message)
            
            if direction == "H":
                if x0 != 7:
                    return (False, message)
                elif y0 + word.getLengthWord() - 1 < 7 or y0 > 7:
                    return (False, message)

        else:
            # Comprobamos si la palabra se sale del tablero
            message = "La palabra se sale de los límites del tablero"
            if (x0 < 0 or x0 >= 15 or y0 < 0 or y0 >= 15):
                return (False, message)
            if direction == "V" and x0 + word.getLengthWord() - 1 >= 15:
                return (False, message)
            if direction == "H" and y0 + word.getLengthWord() - 1 >= 15:
                return (False, message)
        
            # Comprobamos si se utiliza alguna ficha del tablero para formar la palabra
            x = x0
            y = y0
            blanks = []
            for c in word.word:
                if self.board[x][y] == " ":
                    blanks.append(c)
          
                if direction == "V":
                    x += 1
                if direction == "H":
                    y += 1
    
            if len(blanks) == word.getLengthWord():
                message = "No se está utilizando ninguna ficha del tablero"
                return (False, message)

            # Comprobamos si la casilla está libre u ocupada por la misma letra
            x = x0
            y = y0
            for c in word.word:
                if self.board[x][y] != " " and self.board[x][y] != c:
                    message = "Hay una ficha diferente ocupando una posición"
                    return (False, message)
                if direction == "V":
                    x += 1
                if direction == "H":
                    y += 1
            
            # Comprobamos si se coloca una nueva ficha en el tablero
            x = x0
            y = y0
            matching = []
            for c in word.word:
                if self.board[x][y] == c:
                    matching.append(c)
                if direction == "V":
                    x += 1
                if direction == "H":
                    y += 1
    
            if len(matching) == word.getLengthWord():
                message = "No se está colocando ninguna ficha nueva en el tablero"
                return (False, message)
    
        
            # Comprobamos que no hay fichas adicionales a principio y final de palabra
            message = "Hay fichas adicionales a principio o final de palabra"
            x = x0
            y = y0
            if direction == "V" and ((x != 0 and self.board[x - 1][y] != " ") or (x + word.getLengthWord() != 14 and self.board[x + word.getLengthWord()][y] != " ")):
                return (False, message)
            if direction == "H" and ((y != 0 and self.board[x][y - 1] != " ") or (y + word.getLengthWord() != 14 and self.board[x][y + word.getLengthWord()] != " ")):
                return (False, message)
  
        message = "La palabra se puede situar en el tablero"
        return (True, message)           
        
        
    def getPawns(self,word, x, y, direction):
        """
        Dada una palabra, posición, dirección, devuelve las letras necesarias para formar la palabra word recibida por parámetro
        """
        needed_letters = Word()
        possible,message = self.isPossible(word, x, y, direction)
        
        if not possible:
            print(message)
        else:
            for c in word.word:
                if self.board[x][y] != c:
                    needed_letters.word.append(c)
                if direction == "V":
                    x += 1
                if direction == "H":
                    y += 1
        return needed_letters  
        
    def showWordPlacement(self, pawns,word):
        """
        Dadas las fichas del jugador y una palabra muestra por pantalla todas las posibles colocaciones de la palabra sobre el tablero
        """
        for direction in ["V", "H"]:
            print("{}:".format("Vertical" if direction == "V" else "Horizontal"))
            for i in range(15):
                for j in range(15):
                    if self.isPossible(word, i, j, direction)[0] == True:
                        needed_pawns = self.getPawns(word, i, j, direction)
                        if FrequencyTable.isSubset(needed_pawns.getFrequency(), pawns.getFrequency()):
                            print("(x = {}, y = {})".format(i, j))
                            
            
        
        
    