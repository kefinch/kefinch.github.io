#!/usr/bin/python
import os, shutil, json
from PIL import Image

# 'sudo pip install pillow' to get the Python Imaging Library

def isImage(fileName):
	imgExtensions = ['jpg', 'jpeg', 'gif', 'png', 'tiff']
	for ext in imgExtensions:
		if fileName.endswith('.' + ext):
			return True
	return False

# Remove the old thumbnail directory if it exists and create a new one
imageDir = os.getcwd() + '/images'
thumbnailDir = imageDir + '/thumbnails'
if os.path.exists(thumbnailDir):
	shutil.rmtree(thumbnailDir)
os.makedirs(thumbnailDir)

# Get a list of all image files in the current directory
imageFiles = [f for f in os.listdir(imageDir) if os.path.isfile(imageDir + '/' + f) and isImage(f)]

maxSize = 256, 256

imageMetaData = []

# Create thumbnails for all images, get image names & resolutions for jekyll
for imageFile in imageFiles:
	file, ext = os.path.splitext(imageFile)
	thumbnailName = file + '-thumbnail' + ext
	im = Image.open(imageDir + '/' + imageFile)

	# Add photo name & resolution to image data array
	imageData = {}
	imageData['image'] = imageFile
	imageData['thumbnail'] = thumbnailName
	imageData['resolution'] = str(im.size[0]) + 'x' + str(im.size[1])
	imageMetaData.append(imageData)

	# Create and save thumbnail
	im.thumbnail(maxSize)
	im.save(thumbnailDir + '/' + thumbnailName)

# Write image metadata to a JSON file
dataDir = os.getcwd() + '/_data'
with open(dataDir + '/imageData.json', 'w') as outfile:
    json.dump(imageMetaData, outfile)

print 'Processed', len(imageFiles), 'images.'