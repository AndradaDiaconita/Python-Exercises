# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#              SmartClass A.I.ssistant Project - COMP 472 Section AK-X        -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# -              Team member #1: Elise Proulx      - 40125538                 -
# -              Team member #2: Ardalan Jamshidi  - 27079265                 -
# -              Team member #3: Andrada Diaconita - 40245789                 -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

import os
import cv2

import matplotlib.pyplot as plt

directory = r'\Users\ardal\Downloads\472\Histogram\FED\Engaged'

output_directory = os.path.join(directory, 'histograms')

os.makedirs(output_directory, exist_ok=True)

for filename in os.listdir(directory):

    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):

        filepath = os.path.join(directory, filename)
        im = cv2.imread(filepath)
        
        if im is not None:
            
            vals = im.mean(axis=2).flatten()
            
            plt.figure()
            plt.hist(vals, 255)
            plt.xlim([0, 255])
            
            plot_filename = os.path.join(output_directory, f"{os.path.splitext(filename)[0]}_plt.png")
            plt.savefig(plot_filename)
            plt.close()
