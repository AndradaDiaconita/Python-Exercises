
# 1) dataset.zip: 
  contains all images in the new data set. These images have been collected from public datasets from various sources. Please reference the attached report (report.pdf) in this GitHub repository. 
# 2) dataset_clean.py: 
  conains Python code that both converts the images to greyscale and resizes all images in dimensions in order to standardize the dataset. 
# 3) histograms.py: 
  contains Python code using matlibplot to create histograms outlining pixel density distributions and sample imagine
# 4) Main.py:
  main program that builds the CNN model defined in CNN_xxx.py. This can imply one of three .py files included in this repo (i.e. _Main, _Variant1, _Variant2). Regardless of which model is applied, the program will take the path hardcoded by the prorgammer (i.e. variable datasetPath) and subsequentally open a set of pre-labeled images, as outlined in project #1. 
    ACCESSING PROPER DATASET:
      line 27 --> ensure that you have downloaded dataset.zip prior and opened the file. The location in which the file is saved must be copied and replace the string within        the bracket () and single quotes to access the dataset used in this project. 
    TO ACCESS VARIANTS AND MAIN MODELS:
      line 70 --> uncomment 'model = CNNVar1()' to run variant 1
      line 71 --> uncomment 'model = CNNVar2()' to run variant 2
      line 72 --> uncomment 'model = CNN()' to run the main model
# 5) CNN_Main.py: 
  main CNN model class. includes main CNN object definition and its convolution and fully connected layers. The forward() function calls on these layers separately with a flattening of data between the two processess. 
# 6) CNN_Variant1.py: 
  variante 1 CNN model class. this differs from the main CNN model class as, ontop of the main CNN object definition, it has a higher number of kernels within the convolution layers. The forward() function calls on these layers separately with a flattening of data between the two processess. 
# 7) CNN_Variant2.py:
variante 2 CNN model class. this differs from the main CNN model class as, ontop of the main CNN object definition, there is an addiditional layer withinn self.conv_layer. The forward() function calls on these layers separately with a flattening of data between the two processess. 
