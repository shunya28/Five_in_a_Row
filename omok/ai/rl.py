import tensorflow as tf
import numpy as np

class RL():
    def __init__(self, board_height, board_width):
        self.board_height = board_height
        self.board_width = board_width
        self.model = RL.create_model(board_height, board_width)

    @staticmethod 
    def create_model(board_height, board_width):
        model = tf.keras.models.Sequential([
            tf.keras.layers.Conv2D(filters=32, kernel_size=5, strides=1, activation='relu'),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(units=board_height*board_width, activation=None)
        ])
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
        action = action // 32, action % 32
        return action
