

import torch
import torch.nn as nn
import torchvision.datasets as datasets
import torchvision.transforms.functional as TF
import numpy as np
import matplotlib.pyplot as plt

from torchvision import transforms
from torch.utils.data import DataLoader, random_split, SubsetRandomSampler 
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, precision_score, recall_score, f1_score
from PIL import Image

from CNN_Main import CNN
from CNN_Variant1 import CNN as CNNVar1
from CNN_Variant2 import CNN as CNNVar2

# K-Fold library
from sklearn.model_selection import KFold

datasetPath = r'C:\Users\andra\OneDrive\Desktop\portfolio\AI Photos Project & Report'

# Model load feature (optional)
loadModel = False


# Data transformation templates
data_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]) # Standard from ImageNet
])

# Application of data transformations
dataset = datasets.ImageFolder(datasetPath, transform=data_transforms)
print("Dataset classes: ", dataset.classes)

# Calculate lengths for train and validation sets based on dataset size
total_length = len(dataset)
train_length = int(0.85 * total_length)
val_length = total_length - train_length

# Split dataset into train, val, test using the calculated lengths
trainSet, valSet = random_split(dataset, [train_length, val_length])

# K-Fold parameters
kFoldsNum = 10
kFold = KFold(n_splits=kFoldsNum, shuffle=True)
results = {}

# Number of epochs used is set to 10
num_epochs = 10

# Number of classes is set to 4 to account for the "angry", "engaged", "neutral" and "happy" classes
num_classes = 4

# Default learning rate of 0.001
learning_rate = 0.001

# Create the 4 classes
classes = dataset.classes

# K-Fold 
for fold, (trainFold, valFold) in enumerate(kFold.split(dataset)):

    checkpoint_path = 'fold_{}_model.pth'.format(fold)
    
    if loadModel:
        checkpoint = torch.load(checkpoint_path)
        model.load_state_dict(checkpoint['model_state_dict'])
        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        fold = checkpoint['fold']

    print(f'K-Fold Process: {fold}')
    print('--------------------------------')

    # Sampling elements randomly from a given list of indices
    train_sampler = SubsetRandomSampler(trainFold)
    val_sampler = SubsetRandomSampler(valFold)

    trainloader = DataLoader(dataset, batch_size=32, sampler=train_sampler)
    valloader = DataLoader(dataset, batch_size=32, sampler=val_sampler)
    
    # Change the path to save the models to a different file
    def save_checkpoint(state_dict, filename='./testmodel.pth.tar'):
        print("Saving Checkpoint")
        torch.save(state_dict, filename)

    model = CNN()
    
    # Loss function 
    criterion = nn.CrossEntropyLoss()
    
    # Updates the weight of the model
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    total_step = len(trainloader)
    loss_list = []
    acc_list = []

    # Early Stopping Protocol
    # The best validation loss observed to a large value
    epochLoss = 500

    # Keeps track of how many epochs the validation loss has not improved consecutively
    counter = 0

    #Threshold after which training will stop if the validation loss does not improve
    stopping_threshold = 3

    for epoch in range(num_epochs):
    
        print(f'Beginning epoch {epoch+1}')
        
        for i, (image, label) in enumerate(trainloader):
            
            # Forward pass
            outputs= model(image)
            loss = criterion(outputs, label)
            loss_list.append(loss.item())

            # Backprop and optimisation
            optimizer.zero_grad()
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), 0.75)
            optimizer.step()

            # Train accuracy
            total = label.size(0)
            _, predicted = torch.max(outputs.data, 1)
            correct = (predicted == label).sum().item()
            acc_list.append(correct / total)
            
            if (i + 1) % 50 == 0:
                print('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}, Accuracy: {:.2f}%'
                    .format(epoch + 1, num_epochs, i + 1, total_step, loss.item(),
                    (correct / total) * 100))
                       
    model.eval()
    
    val_loss = 0.0
    correct = 0
    total = 0
    
    val_predictions = []
    val_labels = []

    with torch.no_grad():
    
        for images, labels in valloader:
            outputs = model(images)
            loss = criterion(outputs, labels)
            val_loss += loss.item() * images.size(0)
            
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

            val_predictions.extend(predicted.cpu().numpy())
            val_labels.extend(labels.cpu().numpy())
    
    val_accuracy = correct / total
    avg_val_loss = val_loss / len(valloader.sampler)
    
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
    
    # Micro and macro calculation of the metrics
    precision = precision_score(val_labels, val_predictions, average='macro')
    precision = precision_score(val_labels, val_predictions, average='micro')

    recall = recall_score(val_labels, val_predictions, average='macro')
    recall = recall_score(val_labels, val_predictions, average='micro')
    
    f1 = f1_score(val_labels, val_predictions, average='macro')
    f1 = f1_score(val_labels, val_predictions, average='micro')


    print(f'Fold {fold}, Epoch [{epoch+1}/{num_epochs}], Validation Loss: {avg_val_loss:.4f}, Validation Accuracy: {val_accuracy * 100:.2f}%, Precision: {precision:.4f}, Recall: {recall:.4f}, F1-Score: {f1:.4f}')
        
    # Confusion matrix
    cm = confusion_matrix(val_labels, val_predictions)
    plt.figure(figsize=(8, 6))
    ConfusionMatrixDisplay(cm, display_labels=classes).plot(cmap='Blues')
    plt.title(f'Confusion Matrix FOLD {fold}')
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.show()    

    # Save current fold progress
    torch.save({
        'fold': fold,
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
    }, 'fold_{}_model.pth'.format(fold))

    # Store the results for each fold in macro and micro templates
    results[fold] = {
            'accuracy': val_accuracy * 100,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            
            'precision_mi': precision_mi,
            'recall_mi': recall_mi,
            'f1_score_mi': f1_mi
    }
    num = num + 1

# Print fold results
print(f'K-Fold Cross-validation for {kFoldsNum} number of folds')
print('--------------------------------')

sum_accuracy = 0.0
sum_precision = 0.0
sum_recall = 0.0
sum_f1 = 0.0

sum_precision_MI = 0.0
sum_recall_MI = 0.0
sum_f1_MI = 0.0

for key, value in results.items():
    print(f'Fold {key}: Accuracy: {value["accuracy"]:.2f}%, Precision: {value["precision"]:.4f}, Recall: {value["recall"]:.4f}, F1-Score: {value["f1_score"]:.4f}, Precision MI: {value["precision_mi"]:.4f}, Recall MI: {value["recall_mi"]:.4f}, F1-Score MI: {value["f1_score_mi"]:.4f}')
    

    sum_accuracy += value['accuracy']
    sum_precision += value['precision']
    sum_recall += value['recall']
    sum_f1 += value['f1_score']
    
    sum_precision_MI += value['precision_mi']
    sum_recall_MI += value['recall_mi']
    sum_f1_MI += value['f1_score_mi']

num_folds = len(results.items())
print(f'Average: Accuracy: {sum_accuracy/num_folds:.2f}%, Precision: {sum_precision/num_folds:.4f}, Recall: {sum_recall/num_folds:.4f}, F1-Score: {sum_f1/num_folds:.4f}, Precision MI: {sum_precision_MI/num_folds:.4f}, Recall MI: {sum_recall/num_folds:.4f}, F1-Score: {sum_recall_MI/num_folds:.4f}, Precision MI: {sum_precision_MI/num_folds:.4f}, F1-Score MI: {sum_f1_MI/num_folds:.4f}')