import random
import numpy as np
import time
from game import Game
from keras.models import Model
from keras.layers import Dense, LeakyReLU, BatchNormalization, Dropout, Concatenate, Input, Activation, Flatten
import matplotlib.pyplot as plt

def build_model(input_shape):
    input_layer = Input(input_shape)

    hid = Flatten()(input_layer)

    hid = Dense(32)(hid)
    hid = LeakyReLU(0.2)(hid)

    hid = Dense(4)(hid)
    out = LeakyReLU(0.2)(hid)

    model = Model(inputs=input_layer, outputs=out)
    model.compile(optimizer='adam', loss='mse')
    return model

# Converts game response to a reward
def reward(response):
    if response == 1: return 1        # Reward for scoring move
    elif response == 0: return 0.01     # Reward for non-scoring but valid move
    elif response == -1: return -0.05   # Reward for invalid move

g = Game((5,5))
model = build_model((5,5))

y = 0.95
eps = 0.5
decay_factor = 0.999
r_avg_list = []
for i in range(100):
    eps *= decay_factor
    done = False
    r_sum = 0
    s = g.board.copy().reshape(-1, 5, 5)
    for _ in range(1000):
        if np.random.random() < eps:
            a = random.choice(range(4))
        else:
            a = np.argmax(model.predict(s))
        r = reward(g.move(g.num_to_dir(a)))
        new_s = g.board.copy().reshape(-1, 5, 5)
        target = r + y * np.max(model.predict(new_s))
        target_vec = model.predict(s)
        target_vec[0,a] = target
        model.fit(s, target_vec.reshape(-1, 4), epochs=1, verbose=0)
        s = new_s
    print("Done run:", i)

g2 = Game((5,5))
plt.figure
for _ in range(100):
    g2.move(g2.num_to_dir(np.argmax(model.predict(g2.board.reshape(-1,5,5)))))
    g2.plot_board()

