"""Commands for testing a trained classifier."""
import sys
import os
import logging
import pickle
import numpy as np
import tensorflow as tf
import network as network
import sampling as sampling
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

def test_model(logdir, infile, embedfile):
    """Test a classifier to label ASTs"""

    with open(infile, 'rb') as fh:
        _, trees, labels = pickle.load(fh)

    with open(embedfile, 'rb') as fh:
        embeddings, embed_lookup = pickle.load(fh)
        num_feats = len(embeddings[0])

    # build the inputs and outputs of the network
    nodes_node, children_node, hidden_node = network.init_net(
        num_feats,
        len(labels)
    )
    out_node = network.out_layer(hidden_node)

    ### init the graph
    sess = tf.Session()#config=tf.ConfigProto(device_count={'GPU':0}))
    sess.run(tf.global_variables_initializer())

    with tf.name_scope('saver'):
        saver = tf.train.Saver()
        ckpt = tf.train.get_checkpoint_state(logdir)
        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(sess, ckpt.model_checkpoint_path)
        else:
            raise 'Checkpoint not found.'

    correct_labels = []
    # make predicitons from the input
    predictions = []
    step = 0
    for batch in sampling.batch_samples(
        sampling.gen_fast_samples(trees, labels, embeddings, embed_lookup), 1
    ):
        nodes, children, batch_labels = batch
        output = sess.run([out_node],
            feed_dict={
                nodes_node: nodes,
                children_node: children,
            }
        )
        correct_labels.append(np.argmax(batch_labels))
        predictions.append(np.argmax(output))
        step += 1
        print(step, '/', len(trees))

    target_names = list(labels)
    print('Accuracy:', accuracy_score(correct_labels, predictions))
    print(classification_report(correct_labels, predictions, target_names=target_names))
    print(confusion_matrix(correct_labels, predictions))



def main():
    logdir = "./tbcnn/logs/2"
   


    # sample input for sys.argv[1]
    inputs = "./data/10_clasess_algorithms_trees.pkl"
    
    # sample input for sys.argv[2]
    embeddings = "./data/fast_pretrained_vectors.pkl"


    # train_model(logdir,inputs,embeddings) 

    test_model(logdir,sys.argv[1],sys.argv[2])


if __name__ == "__main__":
    main()