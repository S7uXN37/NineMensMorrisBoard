#!/usr/bin/env python
# Modified code from: https://github.com/asrivat1/DeepLearningVideoGames

# Network rates positions:
#   Pieces on bad positions will be moved to better positions if possible
#   Pieces will be set down on best positions
#   Opponent pieces on best positions will be taken
#   
#   Input: 24 nodes, own piece=1, enemy piece=-1, empty=0
#   Output: 24 nodes, rating, higher is better

import tensorflow as tf
import morris as game
import random
import numpy as np
from collections import deque

GAME = 'morris' # the name of the game being played for log files
GAMMA = 0.9 # decay rate of past observations
OBSERVE = 500. # timesteps to observe before training
EXPLORE = 500. # frames over which to anneal epsilon
FINAL_EPSILON = 0.05 # final value of epsilon
INITIAL_EPSILON = 1.0 # starting value of epsilon
REPLAY_MEMORY = 1000 # number of previous transitions to remember
BATCH = 32 # size of minibatch

def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev = 0.01)
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.01, shape = shape)
    return tf.Variable(initial)

def variable_summaries(var):
    """Attach a lot of summaries to a Tensor (for TensorBoard visualization)."""
    with tf.name_scope('summaries'):
        mean = tf.reduce_mean(var)
        tf.summary.scalar('mean', mean)
        with tf.name_scope('stddev'):
            stddev = tf.sqrt(tf.reduce_mean(tf.square(var - mean)))
        tf.summary.scalar('stddev', stddev)
        tf.summary.scalar('max', tf.reduce_max(var))
        tf.summary.scalar('min', tf.reduce_min(var))
        tf.summary.histogram('histogram', var)
    
def nn_layer(input_tensor, input_dim, output_dim, layer_name, act=tf.nn.relu):
    """Reusable code for making a simple neural net layer.
    It does a matrix multiply, bias add, and then uses relu to nonlinearize.
    It also sets up name scoping so that the resultant graph is easy to read,
    and adds a number of summary ops.
    """
    # Adding a name scope ensures logical grouping of the layers in the graph.
    with tf.name_scope(layer_name):
        # This Variable will hold the state of the weights for the layer
        with tf.name_scope('weights'):
            weights = weight_variable([input_dim, output_dim])
            variable_summaries(weights)
        with tf.name_scope('biases'):
            biases = bias_variable([output_dim])
            variable_summaries(biases)
        with tf.name_scope('Wx_plus_b'):
            preactivate = tf.matmul(input_tensor, weights) + biases
            tf.summary.histogram('pre_activations', preactivate)
        activations = act(preactivate, name='activation')
        tf.summary.histogram('activations', activations)
        return activations
    
def createNetwork():
    # input layer
    with tf.name_scope('input'):
        s = tf.placeholder("float", [None, 24], name='board-input')

    # layers
    hidden1 = nn_layyer(s, 24, 512, 'layer1', act=tf.nn.relu)
    readout = nn_layer(hidden1, 512, 24, 'layer2', act=tf.identity)

    return s, readout, h_fc1
    
def trainNetwork(s, readout, h_fc1, sess):
    # define the cost function                                                              TODO!!!
    a = tf.placeholder("float", [None, 24])
    y = tf.placeholder("float", [None])
    readout_action = tf.reduce_sum(tf.mul(readout, a), reduction_indices = 1)
    cost = tf.reduce_mean(tf.square(y - readout_action))
    with tf.name_scope('train'):
        train_step = tf.train.AdamOptimizer(1e-6).minimize(cost)

    # open up a game state to communicate with emulator
    game_state = game.GameState()

    # store the previous observations in replay memory
    D = deque()

    # get the first state by doing nothing
    do_nothing = np.zeros(24)
    s_t, r_0, terminal = game_state.frame_step(do_nothing)

    # saving and loading networks
    saver = tf.train.Saver()
    # Merge all sumarries and write
    merged = tf.summary.merge_all()
    train_writer = tf.summary.FileWriter('morris/train', sess.graph)
    tf.global_variables_initializer().run()
    
    checkpoint = tf.train.get_checkpoint_state("saved_networks")
    if checkpoint and checkpoint.model_checkpoint_path:
        saver.restore(sess, checkpoint.model_checkpoint_path)
        print "Successfully loaded:", checkpoint.model_checkpoint_path
    else:
        print "Could not find old network weights"

    epsilon = INITIAL_EPSILON
    t = 0
    try:
        while "pigs" != "fly" && t < 10000:
            # choose an action epsilon greedily
            a_t = readout.eval(feed_dict = {s : [s_t]})[0]
            if random.random() <= epsilon or t <= OBSERVE:
                a_t = np.random.rand(24)

            # scale down epsilon
            if epsilon > FINAL_EPSILON and t > OBSERVE:
                epsilon -= (INITIAL_EPSILON - FINAL_EPSILON) / EXPLORE

            # run the selected action and observe next state and reward
            s_t1, r_t, terminal = game_state.frame_step(a_t)

            # store the transition in D
            D.append((s_t, a_t, r_t, s_t1, terminal))
            if len(D) > REPLAY_MEMORY:
                D.popleft()

            # only train if done observing
            if t > OBSERVE:
                # sample a minibatch to train on
                minibatch = random.sample(D, BATCH)

                # get the batch variables
                s_j_batch = [d[0] for d in minibatch]
                a_batch = [d[1] for d in minibatch]
                r_batch = [d[2] for d in minibatch]
                s_j1_batch = [d[3] for d in minibatch]

                y_batch = []
                readout_j1_batch = readout.eval(feed_dict = {s : s_j1_batch})
                for i in range(0, len(minibatch)):
                    # if terminal only equals reward
                    if minibatch[i][4]:
                        y_batch.append(r_batch[i])
                    else:
                        y_batch.append(r_batch[i] + GAMMA * np.max(readout_j1_batch[i]))

                # perform gradient step
                '''
                train_step.run(feed_dict = {
                    y : y_batch,
                    a : a_batch,
                    s : s_j_batch})
                '''
                if t % 100 == 0:  # Record execution stats
                    run_options = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE)
                    run_metadata = tf.RunMetadata()
                    summary, _ = sess.run([merged, train_step], feed_dict={
                        y : y_batch,
                        a : a_batch,
                        s : s_j_batch}, options=run_options, run_metadata=run_metadata)
                    train_writer.add_run_metadata(run_metadata, 'step%03d' % t)
                    train_writer.add_summary(summary, t)
                    print('Adding run metadata for', t)
                else:  # Record a summary
                    summary, _ = sess.run([merged, train_step], feed_dict={
                        y : y_batch,
                        a : a_batch,
                        s : s_j_batch})
                    train_writer.add_summary(summary, t)

            # update the old values
            s_t = s_t1
            t += 1

            # save progress every 10000 iterations
            if t % 10000 == 0:
                saver.save(sess, 'morris/checkpoint morris-dqn', global_step = t)

            # print info
            state = ""
            if t <= OBSERVE:
                state = "observe"
            elif t > OBSERVE and t <= OBSERVE + EXPLORE:
                state = "explore"
            else:
                state = "train"
            print "TIMESTEP", t, "/ STATE", state, "/ LINES", game_state.total_lines, "/ EPSILON", epsilon, "/ ACTION", action_index, "/ REWARD", r_t, "/ Q_MAX %e" % np.max(readout_t)
    except KeyboardInterrupt:
        train_writer.close()
        
        export_path = 'morris/out'
        print ('Exporting trained model to', export_path)
        saver = tf.train.Saver(sharded=True)
        model_exporter = exporter.Exporter(saver)
        model_exporter.init(
            sess.graph.as_graph_def(),
            named_graph_signatures={
                'inputs': exporter.generic_signature({'board': s}),
                'outputs': exporter.generic_signature({'values': readout})})
        model_exporter.export(export_path, tf.constant(1), sess)
        
def playGame():
    sess = tf.InteractiveSession()
    s, readout, h_fc1 = createNetwork()
    trainNetwork(s, readout, h_fc1, sess)

def main():
    playGame()

if __name__ == "__main__":
    main()