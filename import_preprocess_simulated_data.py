import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
from pandas import DataFrame as df
import tensorflow as tf
import tensorflow_probability as tfp
from tensorflow.keras.layers import Input, Embedding, Activation, Add, Conv1D, Conv1DTranspose, LSTM, Layer, LayerNormalization, ReLU, Embedding, Bidirectional
from keras.preprocessing.sequence import pad_sequences
import tensorflow_addons as tfa
from tensorflow.keras.models import Model, Sequential
from keras.utils.vis_utils import plot_model
import edward2 as ed
import warnings

#import datafram from txt file
test_dataframe = pd.read_csv('/Users/jeffreyyu/Documents/Sladek/colocalization_neural_network/simulated_gwas.txt', sep='\t')
#remove heading name
test_dataframe.columns.name = None
#sanity: dimensions of df
print(test_dataframe.shape)

#convert to float 64 numpy array
data_frame_array = df.to_numpy(test_dataframe, dtype = 'float64')
#sanity: dimensions and show
print(data_frame_array.shape)     
#data_frame_array

#delete position column
no_positions_array = np.delete(data_frame_array, 0, 1)
print(no_positions_array.shape)
#no_positions_array


#cuts positions to split the dataset
#split_sample_input represents a list of variable length simulated GWAS p-values with 100 samples, 3 traits for each loci (variable number of loci per sample)
cuts = np.sort(random.sample(range(0, data_frame_array.shape[0]-1), 100-1))
print(len(cuts))
#cuts
test_input = np.split(no_positions_array , cuts, axis = 0)
print(test_input[0].shape)
print(test_input[1].shape)
print(test_input[2].shape)


#number of samples
n_samples = len(test_input)
#number of samples (sanity)
print(n_samples)


#maximum length of (maximum number of loci of) all samples
def find_max_list(list):
    list_len = [len(i) for i in list]
    return max(list_len)

#maximum number of loci per sample gene segment
maximum_length = find_max_list(test_input)


#number of loci and number of channels of each sample (sanity)
print('before padding:')
for i in range(0, n_samples):
    print(test_input[i].shape)
#pad input list of samples 
padded_test_input = pad_sequences(test_input, padding='post', dtype='float64')

#number of traits simulated
n_traits = padded_test_input.shape[2]


#number of loci and number of channels of each sample after padding (sanity)
print('after padding:')
for i in range(0, n_samples):
    print(padded_test_input[i].shape)

#first and last sample (sanity)
print('before padding:')
print(test_input[0])
print(test_input[-1])
print('after padding:')
print(padded_test_input[0])
print(padded_test_input[-1])


#embed positional information
position_embedding_layer = Embedding(maximum_length, n_traits)
position_indices = tf.range(maximum_length)
embedded_indices = position_embedding_layer(position_indices)
print(embedded_indices)















#add positional encoding to the padded test imputs
for i in range(0, n_samples-1):
    padded_test_input[i] = tf.convert_to_tensor(padded_test_input[i]) + tf.cast(embedded_indices.numpy(), 'float64')
#reassign to new name
positional_embedded_padded_test_input = padded_test_input
    
#number of samples (padded_test_inputanity)
print(len(positional_embedded_padded_test_input))
#positional embedding (sanity)
print('after positional embedding:')
print(tf.size(positional_embedded_padded_test_input))
print(positional_embedded_padded_test_input)

