'''
Deep neural network that plays omok
'''
import numpy as np
from omok.core.board import Board

class Network:
    EMPTY_SLOT = 0.0
    PLAYER_SLOT = 1.0
    ENEMY_SLOT = -1.0

    WIDTH = 40
    HEIGHT = 30
    STRUCTURE = [200]

    MODEL_DIR = 'omok/ai/models/'

    @staticmethod
    def sigmoid(X):
        X = 1.0 / (1.0 + np.exp(-X))
        return X

    @staticmethod
    def sigmoid_derivative(Y):
        Y = Y * (1 - Y)
        return Y
    
    @staticmethod
    def ReLU(X):
        X[X < 0] = 0
        return X
    
    @staticmethod
    def ReLU_derivative(Y):
        Y[Y > 0] = 1
        Y[Y < 0] = 0
        return Y

    def __init__(self, filename=None):
        self.size = Network.WIDTH * Network.HEIGHT
        if filename==None:
            network_builder = [self.size] + Network.STRUCTURE + [self.size]
            self.model = [np.random.randn(network_builder[i + 1], network_builder[i])\
                                for i in range(len(network_builder) - 1)]
        else:
            self.model = list(np.load(filename, allow_pickle=True))
        
    def decide_next_move(self, board_instance, training=False):
        board = board_instance.board
        condition = board_instance.status
        preprocessed_board, original_dimension = self.preprocess(board, condition)
        prediction, _ = self.feed_forward(preprocessed_board)

        (i_start, i_end), (j_start, j_end) = original_dimension

        prediction[:i_start * Network.WIDTH] = -1
        prediction[i_end * Network.WIDTH:] = -1
        for i in range(i_start, i_end):
            prediction[i * Network.WIDTH:i * Network.WIDTH + j_start] = -1
            prediction[i * Network.WIDTH + j_end:(i + 1) * Network.WIDTH] = -1
            for j in range(j_start, j_end):
                if board[i - i_start][j - j_start] != Board.EMPTY_SLOT:
                    prediction[i * Network.WIDTH + j] = -1

        prediction_max = np.argmax(prediction)
        i = prediction_max // Network.WIDTH - i_start
        j = prediction_max % Network.WIDTH - j_start
        if not training:
            return (i, j)
        else:
            return (i, j), _, prediction

    def preprocess(self, board, condition):
        width = len(board[0])
        height = len(board)

        preprocessed_board = np.zeros(self.size)
        i_start, j_start = (Network.HEIGHT - height) // 2, (Network.WIDTH - width) // 2
        i_end, j_end = i_start + height, j_start + width
        player_slot = Board.BLACK_SLOT if condition == Board.BLACK_TURN else Board.WHITE_SLOT

        for i in range(i_start, i_end):
            for j in range(j_start, j_end):
                preprocessed_board[i * Network.WIDTH + j] =\
                    Network.PLAYER_SLOT if board[i - i_start][j - j_start] == player_slot else (
                        Network.EMPTY_SLOT if board[i - i_start][j - j_start] == Board.EMPTY_SLOT else 
                            Network.ENEMY_SLOT
                    )
        
        original_dimension = (i_start, i_end), (j_start, j_end)
        return preprocessed_board, original_dimension
    
    def feed_forward(self, preprocessed_board):
        hidden_states = []
        hidden_states.append(preprocessed_board)
        for layer in self.model[:-1]:
            hidden_states.append(np.dot(layer, hidden_states[-1]))
            hidden_states[-1] = Network.sigmoid(hidden_states[-1])
        prediction = np.dot(self.model[-1], hidden_states[-1])
        prediction = Network.sigmoid(prediction)
        return prediction, hidden_states
    
    def calculate_gradients(self, hidden_states, gradients):
        full_gradients = [np.empty_like(self.model[i]) for i in range(len(self.model))]
        current_gradients = gradients
        for i in range(len(self.model) - 1, -1, -1):
            for j in range(len(self.model[i])):
                full_gradients[i][j] = current_gradients[j] * hidden_states[i]
            current_gradients = np.dot(current_gradients, self.model[i])
            current_gradients = Network.sigmoid_derivative(current_gradients)
        return full_gradients
    
    def feed_backward(self, full_gradients, learning_rate):
        for i in range(len(self.model)):
            self.model[i] += learning_rate * full_gradients[i]
    
    def save_model(self, filename):
        np.save(filename, self.model)