"""
    anpr function
    Copyright (C) Willi
"""
import numpy
import sys
import cv2
import common
import math

from detect import letter_probs_to_code, post_process, make_scaled_ims
import tensorflow as tf
import model

class DeepANPR(object):
    def __init__(self, param_file):
        f = numpy.load(param_file)
        self.param_vals = [f[n] for n in sorted(f.files, key=lambda s: int(s[4:]))]
        self.x, self.y, self.params = model.get_detect_model()
        self.sess = tf.Session(config=tf.ConfigProto())

    def select_code(self, codes):
        if len(codes) > 0:
            return codes[0]
        else:
            return []

    def detect(self, im):
        """
        Detect number plates in an image.

        :param im:
            Image to detect number plates in.

        :returns:
            Iterable of `bbox_tl, bbox_br, letter_probs`, defining the bounding box
            top-left and bottom-right corners respectively, and a 7,36 matrix
            giving the probability distributions of each letter.

        """

        # Convert the image to various scales.
        MIN_SHAPE = (300,500)
        scaled_ims = list(make_scaled_ims(im, MIN_SHAPE))

        # Execute the model at each scale.
        y_vals = []
        for scaled_im in scaled_ims:
            feed_dict = {self.x: numpy.stack([scaled_im])}
            feed_dict.update(dict(zip(self.params, self.param_vals)))
            y_vals.append(self.sess.run(self.y, feed_dict=feed_dict))

        # Interpret the results in terms of bounding boxes in the input image.
        # Do this by identifying windows (at all scales) where the model predicts a
        # number plate has a greater than 50% probability of appearing.
        #
        # To obtain pixel coordinates, the window coordinates are scaled according
        # to the stride size, and pixel coordinates.
        for i, (scaled_im, y_val) in enumerate(zip(scaled_ims, y_vals)):
            for window_coords in numpy.argwhere(y_val[0, :, :, 0] >
                                                        -math.log(1. / 0.99 - 1)):
                letter_probs = (y_val[0,
                                window_coords[0],
                                window_coords[1], 1:].reshape(
                    7, len(common.CHARS)))
                letter_probs = common.softmax(letter_probs)

                img_scale = float(im.shape[0]) / scaled_im.shape[0]

                bbox_tl = window_coords * (8, 4) * img_scale
                bbox_size = numpy.array(model.WINDOW_SHAPE) * img_scale

                present_prob = common.sigmoid(
                    y_val[0, window_coords[0], window_coords[1], 0])

                yield bbox_tl, bbox_tl + bbox_size, present_prob, letter_probs

    def detect_anpr(self, im):
        im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) / 255.

        codes = []
        for pt1, pt2, present_prob, letter_probs in post_process(
                                                      self.detect(im_gray)):
            pt1 = tuple(map(int, reversed(pt1)))
            pt2 = tuple(map(int, reversed(pt2)))

            code = letter_probs_to_code(letter_probs)
            codes.append( code)

        return self.select_code(codes)
