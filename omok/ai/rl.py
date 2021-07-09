import tensorflow as tf
import numpy as np

class RL():
    def __init__(self):
        self.model = RL.create_model()

    @staticmethod 
    def create_model():
        model = tf.keras.models.Sequential([
            tf.keras.layers.Conv2D(filters=32, kernel_size=5, strides=1),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(units=32*20, activation=None)
        ])
        return model

    @staticmethod
    def preprocess_observation(observation):
        observation = np.array(observation)
        observation = np.where(observation == 'B', 1, observation)
        observation = np.where(observation == 'W', -1, observation)
        observation = np.where(observation == '-', 0, observation)
        if len(observation.shape) == 2:
            observation = np.expand_dims(observation, axis=0)
        observation = np.expand_dims(observation, axis=3)
        observation = observation.astype('float32')
        return observation

    def forward_pass(self, preprocessed_observation):
        flattened_observation = np.reshape(preprocessed_observation, (1, -1))
        logits = self.model(preprocessed_observation)
        logits = tf.where(flattened_observation!=0, -np.inf, logits)
        action = tf.random.categorical(logits, num_samples=1)
        action = np.squeeze(action)
        return action

    def decide_next_move(self, board_instance):
        observation = board_instance.board
        preprocessed_observation = self.preprocess_observation(observation)
        action = self.forward_pass(preprocessed_observation)
        action = int(action // 32), int(action % 32)
        return action
