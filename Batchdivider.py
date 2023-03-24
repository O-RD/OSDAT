import shutil, os

path = '/Users/krina/Library/Application Support/Bitcoin/blocks'

from os import mkdir, walk

filenames = next(walk(path), (None, None, []))[2]

#print(filenames)

i = 1

while(len(filenames)):
    directory = 'Batch' + str(i)
    newdirectoryPath = os.path.join('/Users/krina/Library/Application Support/Bitcoin/BATCHES/',directory)
    os.mkdir(newdirectoryPath)
    for j in range(0,6):
        shutil.move(path + '/' + filenames[j],newdirectoryPath)
        filenames.pop(j)

    i= i + 1