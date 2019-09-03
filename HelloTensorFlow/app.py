#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import tensorflow as tf


# Main Entry

def main():
    message = tf.constant('Hello World!')
    with tf.Session() as sess:
        print(sess.run(message))


# App

if __name__ == '__main__':
    main()
