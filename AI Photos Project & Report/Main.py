


import torch
import torch.nn as nn
import torchvision.datasets as datasets
import torchvision.transforms.functional as TF
import numpy as np
import matplotlib.pyplot as plt

from torchvision import transforms 
from torch.utils.data import DataLoader, random_split
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from PIL import Image

from CNN_Main import CNN
from CNN_Variant1 import CNN as CNNVar1
from CNN_Variant2 import CNN as CNNVar2

# Dataset path
datasetPath = r'C:\Users\andra\OneDrive\Desktop\portfolio\AI Photos Project & Report\dataset'

data_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]) # Standard from ImageNet
])

dataset = datasets.ImageFolder(datasetPath, transform=data_transforms)
print("Dataset classes: ", dataset.classes)

# Calculate lengths for train, test, and validation sets based on dataset size
total_length = len(dataset)
train_length = int(0.7 * total_length)
val_length = int(0.15 * total_length)
test_length = total_length - train_length - val_length

# Split dataset into train, val, test using the calculated lengths
trainSet, valSet, testSet = random_split(dataset, [train_length, val_length, test_length])

# Initialize the DataLoader
trainLoader = DataLoader(trainSet, shuffle=True, batch_size=32, pin_memory=True)
testLoader = DataLoader(testSet, shuffle=True, batch_size=32, pin_memory=True)
ValidationLoader = DataLoader(valSet, shuffle=True, batch_size=32, pin_memory=True)

# Number of epochs used is set to 10
num_epochs = 3

# Number of classes is set to 4 to account for the "angry", "engaged", "neutral" and "happy" classes
num_classes = 4

# Leaning rate is set at a default rate of 0.001
learning_rate = 0.001

# Create the 4 classes
classes = dataset.classes

# Change the path to save the models to a different file
def save_checkpoint(state_dict, filename='./testmodel.pth.tar'):
    print("Saving Checkpoint")
    torch.save(state_dict,filename)
    
# To test variants 1 or 2 replace the line with either of these
# model = CNNVar1()
# model = CNNVar2()
model = CNN()

# Loss function 
criterion = nn.CrossEntropyLoss()
# Updates the weight of the model
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

total_step = len(trainLoader)
loss_list = []
acc_list = []

# Early Stopping Protocol

# The best validation loss observed to a large value
epochLoss = 500

# Keeps track of how many epochs the validation loss has not improved consecutively
counter = 0

# Threshold after which training will stop if the validation loss does not improve
stopping_threshold = 3

# If you would like to load a model and continue working it change the path 
loadModel = False
if loadModel:
    # Change the path you to the model you want to load
   model.load_state_dict(torch.load('./testmodel.pth.tar'))

for epoch in range(num_epochs):
    for i, (image, label) in enumerate(trainLoader, 0):
        
        # Forward pass
        # Image is extracted and ran through cnn
        outputs= model(image)
        
        # Loss function is given the CNN output and the actual label to calculated the loss
        loss = criterion(outputs, label)
        # Loss differene is appended to list
        loss_list.append(loss.item())

        # Backprop and optimisation
        # Claculate loss gradients and optimizer updates model parameters base don gradients 
        optimizer.zero_grad()
        loss.backward()
        # Gradient clipping
        nn.utils.clip_grad_norm_(model.parameters(), 0.75)
        optimizer.step()
    
        # Train accuracy
        total = label.size(0)
        _, predicted = torch.max(outputs.data, 1)
        # Compare the predicted label with the real label, correct hold of correct label for the current batch 
        correct = (predicted == label).sum().item()
        # Compute batch accuracy
        acc_list.append(correct / total)
        
        print(i)

        # Print progress after each epoch session
        if (i + 1) % 50 == 0:
            print('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}, Accuracy: {:.2f}%'
                .format(epoch + 1, num_epochs, i + 1, total_step, loss.item(),
                (correct / total) * 100))
            
    model.eval()
    
    with torch.no_grad():
        correct = 0
        total = 0
        val_loss = 0.0
        # Getting total for images proccesed and the number of correct procced 
        for images, labels in ValidationLoader:
            # Getting the predictions
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            # Getting the accuracy
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            # Getting the loss
            loss = criterion(outputs, labels)
            val_loss +=loss.item()*images.size(0)
            
    val_accuracy = correct / total
    avg_val_loss = val_loss / len(ValidationLoader.sampler)
    
    # Early Stopping Break
    if avg_val_loss <= epochLoss:
        save_checkpoint(model.state_dict())
        epochLoss = avg_val_loss
        counter = 0
        
    else:
        counter += 1
        if counter >= stopping_threshold:
            print(f'Validation loss hasn\'t improved for {stopping_threshold} epochs. Stopping training.')
            break 
        
    
    print(f'Epoch [{epoch+1}/{num_epochs}], Validation Loss: {avg_val_loss:.4f}, Validation Accuracy: {val_accuracy * 100:.2f}%')
        
matrixAcutal = []
matrixPredictions = []
  
model.eval()

with torch.no_grad():

    correct = 0
    total = 0
 
    for images, labels in testLoader:
        matrixAcutal.append(labels)
        
        # Prediction generator
        outputs = model(images)
        _, predicted = torch.max(outputs.data, 1)
        matrixPredictions.append(predicted)
        
        # Accuracy calculation
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
    
    print('Test Accuracy of the model on the test images: {} %'
            .format((correct / total) * 100))


# Flatten the lists of tensors
matrix_actual_flat = np.concatenate([labels.numpy().flatten() for labels in matrixAcutal])
matrix_predictions_flat = np.concatenate([predictions.numpy().flatten() for predictions in matrixPredictions])

# Compute confusion matrix
cm = confusion_matrix(matrix_actual_flat, matrix_predictions_flat)

# Define class names
classes = ['Angry', 'Engaged', 'Happy', 'Neutral']

# Plot confusion matrix
plt.figure(figsize=(8, 6))
ConfusionMatrixDisplay(cm, display_labels=classes).plot(cmap='Blues')
plt.title('Confusion Matrix')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.show()
