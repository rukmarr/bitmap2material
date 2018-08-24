#cmd entrance file
from skimage import io
from shorcuts import process_image
import os


path = input('Enter image name/path: ')
filename = os.path.split(path)[1].split('.')[0]
print(filename)

try:
    photo = io.imread(path)
except FileNotFoundError:
    print('File don\'t exist!')

for map, map_name in zip(process_image(photo, verbose=True),
                     ('DIFFUSE', 'NORM', 'BUMP', 'AO', 'SPECULAR')):

    io.imsave('{0}_{1}.bmp'.format(filename, map_name), map)

print('ready.')

