#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 13:06:48 2021

"""
import sys
import numpy as np


def getInfoDict(args, NDist=1, error_thres=None, eps=0.2):
    """ Takes input args and save it in a dictionary.
    """
    inf = dict()
    inf['input'] = args.input
    inf['interval'] = args.i
    inf['nblock'] = args.j
    inf['crop_frac'] = args.k
    inf['channel'] = args.c
    
    
    inf['v_max']= int(np.ceil(inf['block_len']/3))
    inf['WS05-neighborhood_dist'] = NDist
    inf['WS05-eps'] = eps
    inf['WS05-error_thres'] = error_thres
    return inf


def cropMarginInfo(camera, inf):
    """
    Returns crop boundaries, block locations and frame info in a dictionary. 
    """
    frame = camera.snapshot()
    frame_height = frame.data.shape[0]
    frame_width = frame.data.shape[1]
    inf['frame_height'] = frame_height
    inf['frame_width'] = frame_width
    inf = getCropMargin(inf)
    return inf


def getCropMargin(inf):
    """ Computes crop area from the settings from 'inf' and appends it to the same dictionary. 
    """
    crop_len = min(inf['frame_height'], inf['frame_width'])*inf['crop_frac']
    inf['block_len'] = np.floor(crop_len/inf['nblock'])
    
    #Here we choose error threshold for NMF based on resolution
    inf['WS05-error_thres'] = inf['block_len']/6
    
    crop_len = inf['block_len'] * inf['nblock']
    
    if(crop_len >= crop_len):
        exit("Unexpected Error: The original frame size is smaller than \
             the provided crop-dimensions.")
             
    inf['cent_x'] = int(inf['frame_width']/2)
    inf['cent_y'] = int(inf['frame_height']/2)
    
    #crop a square region of interest to accomodate 
    inf['y1'] = int(inf['cent_y'] - crop_len/2)
    inf['y2'] = int(inf['cent_y'] + crop_len/2)
    inf['x1'] = int(inf['cent_x'] - crop_len/2)
    inf['x2'] = int(inf['cent_x'] + crop_len/2)
    
    #compute approximate central points of each block
    mid_loc = np.arange((inf['block_len']/2) - 1, crop_len, inf['block_len'])
    inf['block_mid']= mid_loc.astype('int32')
    
    return inf


def cropFrame(sample, fcount, inf):
    """ Extract and crops frame using crop margins from the 'inf'.
    """
    frame = sample.data
    sky = frame[inf['y1']:inf['y2'], inf['x1']:inf['x2'], inf['channel']]
    fcount += 1
    
    #sys.stdout.write('Current Frame:' + str(fcount)+ '\r')
    #sys.stdout.flush()

    return fcount, sky

