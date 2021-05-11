## 이미지를 [imagename,classname,label, vec] 형식의 tsv 파일로 저장
## BASE_PATH/TRAIN/CLASS/image.jpg 형식으로 저장되어 있어야 한다.
## 대문자 부분들은 pyimagesearch / config.py 에서 설정

# import the necessary packages
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import load_img
from pyimagesearch import config
from imutils import paths
import numpy as np
import pickle
import random
import os

def split_class(imagepath):
	idx2 = imagepath.rfind('/')
	if idx2 < 0:
		exit(77777)
	idx = imagepath[:idx2].rfind('/')
	if idx < 0:
		exit(77777)
	return imagepath[idx+1:idx2]

def split_file(imagepath):
	idx = imagepath.rfind('/')
	if idx < 0:
		exit(77777)
	return imagepath[idx:]

# load the ResNet50 network and initialize the label encoder
print("[INFO] loading network...")
model = ResNet50(weights="imagenet", include_top=False)
le = None
# loop over the data splits
for split in (config.TRAIN, config.TEST, config.VAL):
	# grab all image paths in the current split
	print("[INFO] processing '{} split'...".format(split))
	p = os.path.sep.join([config.BASE_PATH, split])
	imagePaths = list(paths.list_images(p))
	# randomly shuffle the image paths and then extract the class
	# labels from the file paths
	random.shuffle(imagePaths)
	labels = [p.split(os.path.sep)[-2] for p in imagePaths]

	# if the label encoder is None, create it
	if le is None:
		le = LabelEncoder()
		le.fit(labels)
	# open the output CSV file for writing
	tsvPath = os.path.sep.join([config.BASE_CSV_PATH, "{}.tsv".format(split)])
	tsv = open(tsvPath, "w", encoding='utf-8')
	# loop over the images in batches
	# loop over the images in batches
	for (b, i) in enumerate(range(0, len(imagePaths), config.BATCH_SIZE)):
		# extract the batch of images and labels, then initialize the
		# list of actual images that will be passed through the network
		# for feature extraction
		print("[INFO] processing batch {}/{}".format(b + 1, int(np.ceil(len(imagePaths) / float(config.BATCH_SIZE)))))
		batchPaths = imagePaths[i:i + config.BATCH_SIZE]
		batchLabels = le.transform(labels[i:i + config.BATCH_SIZE])
		batchImages = []

		# loop over the images and labels in the current batch
		for imagePath in batchPaths:
			# load the input image using the Keras helper utility
			# while ensuring the image is resized to 224x224 pixels
			image = load_img(imagePath, target_size=(224, 224))
			image = img_to_array(image)
			# preprocess the image by (1) expanding the dimensions and
			# (2) subtracting the mean RGB pixel intensity from the
			# ImageNet dataset
			image = np.expand_dims(image, axis=0)
			image = preprocess_input(image)
			# add the image to the batch
			batchImages.append(image)
		
		# pass the images through the network and use the outputs as
		# our actual features, then reshape the features into a
		# flattened volume
		batchImages = np.vstack(batchImages)
		features = model.predict(batchImages, batch_size=config.BATCH_SIZE)
		features = features.reshape((features.shape[0], 7 * 7 * 2048))
		# loop over the class labels and extracted features
		for (imagePath, label, vec) in zip(batchPaths,batchLabels, features):
			# construct a row that exists of the class label and
			# extracted features
			classname = split_class(imagePath)
			imagePath = split_file(imagePath)
			#print(imagePath, classname)
			vec = ",".join([str(v) for v in vec])
			tsv.write("{},{},{},{}\n".format(imagePath,classname,label, vec))
	# close the CSV file
	tsv.close()
# serialize the label encoder to disk
f = open(config.LE_PATH, "wb")
f.write(pickle.dumps(le))
f.close()
