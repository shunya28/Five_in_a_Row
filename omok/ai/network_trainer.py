import numpy as np
from threading import Thread
from time import sleep
from omok.ai.network import Network
from omok.ai.minmax import MinMax
from omok.core.board import Board
from omok.gui.gui import GUI

def train(filename, total_epochs, learning_rate, decay, opponent, show_gui=False):
    train_ground = Board(Network.WIDTH, Network.HEIGHT, silent=True)
    train_thread = Thread(target=lambda : run_training(
        filename, total_epochs, learning_rate, decay, opponent, train_ground))
    train_thread.start()
    if show_gui:
        GUI(train_ground)
    train_thread.join()

def run_training(filename, total_epochs, learning_rate, decay, opponent, train_ground):
    print('Initiating training...')
    sleep(3.0)

    trainee = Network(filename)

    if opponent == 'minmax':
        opponent = MinMax()
    else:
        opponent = trainee

    for i in range(total_epochs):
        print('  Epoch {}...\n'.format(i + 1))

        hidden_states_history = []
        prediction_history = []

        if i % 2 == 0:
            trainee_condition = Board.BLACK_TURN
        else:
            trainee_condition = Board.WHITE_TURN
            train_ground.place(int(train_ground.height / 2), int(train_ground.width / 2))

        while train_ground.status == Board.BLACK_TURN or\
                train_ground.status == Board.WHITE_TURN:
            if train_ground.status == trainee_condition:
                trainee_decision, hidden_states, prediction = trainee.decide_next_move(
                    train_ground, training=True)
                train_ground.place(*trainee_decision)
                hidden_states_history.append(hidden_states)
                prediction_history.append(prediction)
            else:
                opponent_decision = opponent.decide_next_move(train_ground)
                train_ground.place(*opponent_decision)
        
        label = 1.0
        if (train_ground.status == Board.BLACK_WIN and trainee_condition == Board.WHITE_TURN) or\
            (train_ground.status == Board.WHITE_WIN and trainee_condition == Board.BLACK_TURN):
            label = 0.0

        full_gradients = []
        for j in range(len(prediction_history) - 1, -1, -1):
            hidden_states = hidden_states_history[j]
            gradients = np.zeros_like(prediction_history[j])
            gradients[np.argmax(prediction_history[j])] = prediction_history[j][np.argmax(prediction_history[j])] - label
            full_gradients.append(trainee.calculate_gradients(hidden_states, gradients))
            if len(full_gradients) > 10:
                break
        
        full_gradients_sum = [np.zeros_like(full_gradients[0][j]) for j in range(len(full_gradients[0]))]
        for j in range(len(full_gradients)):
            for l in range(len(full_gradients[j])):
                full_gradients_sum[l] += full_gradients[j][l] * (decay ** j)

        trainee.feed_backward(full_gradients_sum, learning_rate)
        train_ground.reset()

        if (i + 1) % 100 == 0:
            model_num = (i + 1) // 50
            print('Saving model {}...'.format(model_num))
            trainee.save_model('{}train_backup/iteration {}.npy'.format(trainee.MODEL_DIR, model_num))
    
    print('Training complete')