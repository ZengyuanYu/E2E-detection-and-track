#!/usr/bin/env python

import os

def scan_dir(dir_path):
    for name in os.listdir(dir_path):
        path = os.path.join(dir_path, name)
        out_path = os.path.join('./out/',name)
        os.system('./detect.py path weights.npz out_path')
        print(out_path)

if __name__ == "__main__":
    scan_dir('./in/')

