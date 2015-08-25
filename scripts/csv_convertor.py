#! /usr/bin/env python

import sys
import pickle
import pandas as pd
from pandas import *

def extract(desc):
    desc = desc.lower()
    try:
        if ',' in desc:
            code, names = map(lambda x: x.strip(), desc.split(',', 1))
            if '--' in names:
                scientific, common = map(lambda x: x.strip(), names.split('--'))
                return code, scientific, common
            else:
                return code, None, names
        else:
            return desc, None, None
    except:
        print 'Problema!'
        print desc

if __name__ == '__main__':
    input_file, output_file = sys.argv[1:]
    birds = pickle.load(open(input_file, 'r'))
    birds_df = pd.DataFrame(birds)
    birds_df['code'], birds_df['scientific'],birds_df['common']= zip(*birds_df['desc'].map(extract))
    birds_df = birds_df[['code', 'scientific', 'common', 'mp3']]
    birds_df.to_csv(output_file, encoding='utf-8')