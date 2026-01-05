# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#              SmartClass A.I.ssistant Project - COMP 472 Section AK-X        -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# -              Team member #1: Elise Proulx      - 40125538                 -
# -              Team member #2: Ardalan Jamshidi  - 27079265                 -
# -              Team member #3: Andrada Diaconita - 40245789                 -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

import torch
from PIL import Image
import torch.nn as nn

class CNN(nn.Module):

    def __init__(self):
        super(CNN, self).__init__()
        self.conv_layer = nn.Sequential(

            nn.Conv2d(in_channels=3, out_channels=32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.LeakyReLU(inplace=True),

            nn.Conv2d(in_channels=32, out_channels=32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.LeakyReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),

            nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.LeakyReLU(inplace=True),
            
            nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.LeakyReLU(inplace=True),

        # Added extra convolution layer
            nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.LeakyReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )

        self.fc_layer = nn.Sequential(
            nn.Dropout(p=0.1),
            nn.Linear(56 * 56 * 64, 1000),
            nn.LeakyReLU(inplace=True),
            nn.Linear(1000, 512),
            nn.LeakyReLU(inplace=True),
            nn.Dropout(p=0.1),
            nn.Linear(512, 10)
        )
    
    def forward(self, x):
            # Performs the convolutional layers
            x = self.conv_layer(x)
            # Flatten to 2d 
            x = x.view(x.size(0), -1)
            # Fully connected layer to performs classification base don the feautres that model extracted
            x = self.fc_layer(x)
            return x
