import os
import numpy as np
import tensorflow as tf
from collections import deque
import random
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.optimizers import adam_v2


# Habilitar XLA
tf.config.optimizer.set_jit(True)

os.environ['CUDA_VISIBLE_DEVICES'] = '0'
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'


print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))
print(tf.__version__)
physical_devices = tf.config.list_physical_devices('GPU')
print("Num GPUs Available: ", len(physical_devices))
print(physical_devices)


class DQNAgent:
    def __init__(self, input_shape, num_actions):
        self.input_shape = input_shape
        self.num_actions = num_actions
        self.memory = deque(maxlen=10000)
        self.gamma = 0.95  # factor de descuento
        self.epsilon = 1.0  # factor de exploración
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.0005
        self.model = self._build_model()

    def _build_model(self):
        model = Sequential()
        model.add(Dense(16, input_dim=self.input_shape[0], activation='relu')) # Reducir el número de neuronas en la primera capa
        model.add(Dense(8, activation='relu')) # Eliminar la capa intermedia con 64 neuronas y dejar solo una capa oculta
        model.add(Dense(self.num_actions, activation='linear'))
        model.compile(loss='mse', optimizer=adam_v2.Adam(learning_rate=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.num_actions)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target += self.gamma * np.amax(self.model.predict(next_state)[0])
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        logical_gpus = tf.config.experimental.list_logical_devices('GPU')
        print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
    except RuntimeError as e:
        print(e)










# import os
# import numpy as np
# import tensorflow as tf
# from collections import deque
# import random
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense
# from tensorflow.keras.optimizers import Adam

# # Configurar TensorFlow para usar la GPU
# gpus = tf.config.experimental.list_physical_devices('GPU')
# if gpus:
#     try:
#         for gpu in gpus:
#             tf.config.experimental.set_memory_growth(gpu, True)
#         logical_gpus = tf.config.experimental.list_logical_devices('GPU')
#         print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
#     except RuntimeError as e:
#         print(e)


# class DQNAgent:
#     def __init__(self, input_shape, num_actions):
#         self.input_shape = input_shape
#         self.num_actions = num_actions
#         self.memory = deque(maxlen=2000)
#         self.gamma = 0.95  # factor de descuento
#         self.epsilon = 1.0  # factor de exploración
#         self.epsilon_min = 0.01
#         self.epsilon_decay = 0.995
#         self.learning_rate = 0.001
#         self.model = self._build_model()

#     def _build_model(self):
#         model = Sequential()
#         model.add(Dense(24, input_dim=self.input_shape[0], activation='relu'))
#         model.add(Dense(24, activation='relu'))
#         model.add(Dense(self.num_actions, activation='linear'))
#         model.compile(loss='mse', optimizer=Adam(learning_rate=self.learning_rate))
#         return model

#     def remember(self, state, action, reward, next_state, done):
#         self.memory.append((state, action, reward, next_state, done))

#     def act(self, state):
#         if np.random.rand() <= self.epsilon:
#             return random.randrange(self.num_actions)
#         act_values = self.model.predict(state)
#         return np.argmax(act_values[0])

#     def replay(self, batch_size):
#         minibatch = random.sample(self.memory, batch_size)
#         for state, action, reward, next_state, done in minibatch:
#             target = reward
#             if not done:
#                 target += self.gamma * np.amax(self.model.predict(next_state)[0])
#             target_f = self.model.predict(state)
#             target_f[0][action] = target
#             self.model.fit(state, target_f, epochs=1, verbose=0)
#         if self.epsilon > self.epsilon_min:
#             self.epsilon *= self.epsilon_decay