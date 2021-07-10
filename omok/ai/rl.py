
import numpy as np
import os.path
import tensorflow as tf
from omok.ai.minmax import MinMax
from omok.core.board import Board
from omok.gui.gui import GUI
from threading import Thread
from time import sleep
from tqdm import tqdm

class RL():
    def __init__(self, board_height, board_width):
        self.board_height = board_height
        self.board_width = board_width
        self.weights_path = './omok/ai/models_rl/rl_model_{}x{}.h5'.format(board_height, board_width)
        self.model = self.create_model(board_height, board_width)

    def create_model(self, board_height, board_width):
        model = tf.keras.models.Sequential([
            tf.keras.layers.InputLayer(input_shape=(self.board_height, self.board_width, 1)),
            tf.keras.layers.Conv2D(filters=32, kernel_size=5, strides=1, activation='relu'),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(units=board_height*board_width, activation=None)
        ])
        if os.path.isfile(self.weights_path):
            print('Loading model weights from {}'.format(self.weights_path))
            model.load_weights(self.weights_path)
        return model

    def preprocess_observation(self, observation):
        observation = np.array(observation)
        observation = np.where(observation == 'B', 1, observation)
        observation = np.where(observation == 'W', -1, observation)
        observation = np.where(observation == '-', 0, observation)
        observation = np.reshape(observation, (-1, self.board_height, self.board_width, 1))
        observation = observation.astype('float32')
        return observation

    def forward_pass(self, preprocessed_observation):
        flattened_observation = np.reshape(preprocessed_observation, (-1, self.board_height*self.board_width))
        logits = self.model(preprocessed_observation)
        logits = tf.where(flattened_observation!=0, -np.inf, logits)
        action = tf.random.categorical(logits, num_samples=1)
        action = action.numpy().flatten()
        return action

    def decide_next_move(self, board_instance):
        observation = board_instance.board
        preprocessed_observation = self.preprocess_observation(observation)
        if preprocessed_observation.shape[0] != 1:
            raise Exception('function decide_next_move must be called with singleton observation')
        action = self.forward_pass(preprocessed_observation)
        action = int(action[0])
        action = action // self.board_width, action % self.board_width
        return action

    def train(self, num_epochs, batch_size, visualize=False, transfer_minimax=False):
        boards = []
        for _ in range(batch_size):
            boards.append(Board(width=self.board_width, height=self.board_height, silent=True))
        if transfer_minimax:
            thread = Thread(target=lambda : self.__transfer_minmax(boards, num_epochs, batch_size))
        else:
            thread = Thread(target=lambda : self.train_thread(boards, num_epochs, batch_size))
        thread.start()
        if visualize:
            GUI(boards[0])
        thread.join()
    
    def __transfer_minmax(self, boards, num_epochs, batch_size):
        # board = Board(width=self.board_width, height=self.board_height, silent=True)
        board = boards[0]
        minmax = MinMax()
        learning_rate = 1e-3
        optimizer = tf.keras.optimizers.Adam(learning_rate)
        for iter in tqdm(range(num_epochs), desc='Training iteration'):
            board.reset()
            while board.status == Board.BLACK_TURN or board.status == Board.WHITE_TURN:
                if board.status == Board.WHITE_TURN:
                    i, j = minmax.decide_next_move(board)
                    label = np.array([i*self.board_width + j])
                    preprocessed_observation = self.preprocess_observation(board.board)
                    with tf.GradientTape() as tape:
                        logits = self.model(preprocessed_observation)
                        neg_logprob = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=logits, labels=label)
                        loss = tf.reduce_mean(neg_logprob)
                    grads = tape.gradient(loss, self.model.trainable_variables)
                    optimizer.apply_gradients(zip(grads, self.model.trainable_variables))
                    flattened_observation = np.reshape(preprocessed_observation, (-1, self.board_height*self.board_width))
                    logits = tf.where(flattened_observation!=0, -np.inf, logits)
                    action = tf.random.categorical(logits, num_samples=1)
                    action = action.numpy().flatten()
                    action = int(action[0])
                    board.place(action // self.board_width, action % self.board_width)
                else:
                    (i, j) = minmax.decide_next_move(board)
                    board.place(i, j)
            self.model.save_weights(self.weights_path)
        print('Transfer complete')

    def train_thread(self, boards, num_epochs, batch_size):
        
        sleep(3)
        minmax_enemy = MinMax()
        board = boards[0]

        learning_rate = 1e-3
        optimizer = tf.keras.optimizers.Adam(learning_rate)

        for iter in tqdm(range(num_epochs), desc='Training iteration'):
            board.reset()
            preprocessed_observations = []
            actions = []
            while board.status == Board.BLACK_TURN or board.status == Board.WHITE_TURN:
                if board.status == Board.WHITE_TURN:
                    preprocessed_observation = self.preprocess_observation(board.board)
                    preprocessed_observations.append(preprocessed_observation)
                    action = self.forward_pass(preprocessed_observation)
                    action = int(action[0])
                    actions.append(action)
                    board.place(action // self.board_width, action % self.board_width)
                else:
                    (i, j) = minmax_enemy.decide_next_move(board)
                    board.place(i, j)
            final_reward = 1 if board.status == Board.WHITE_WIN else -1
            self.train_step(optimizer, preprocessed_observations, actions, final_reward)
            self.model.save_weights(self.weights_path)
        print('Training complete')
    
    def train_step(self, optimizer, preprocessed_observations, actions, final_reward):
        preprocessed_observations = np.array(preprocessed_observations)
        preprocessed_observations = np.reshape(preprocessed_observations, (-1, self.board_height, self.board_width, 1))
        actions = np.array(actions)
        rewards = RL.calculate_rewards(final_reward, actions)
        with tf.GradientTape() as tape:
            logits = self.model(preprocessed_observations)
            loss = RL.calculate_loss(logits, actions, rewards)
        grads = tape.gradient(loss, self.model.trainable_variables)
        optimizer.apply_gradients(zip(grads, self.model.trainable_variables))

    @staticmethod
    def calculate_rewards(final_reward, actions, discount_rate=0.85):
        rewards = np.zeros_like(actions).astype('float32')
        rewards[-1] = final_reward
        for i in reversed(range(len(rewards) - 1)):
            rewards[i] = rewards[i + 1] * discount_rate
            rewards = (rewards - np.mean(rewards)) / np.std(rewards)
        return rewards
    
    @staticmethod
    def calculate_loss(logits, actions, rewards):
        neg_logprob = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=logits, labels=actions)
        loss = tf.reduce_mean(neg_logprob * rewards)
        return loss
