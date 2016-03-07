import argparse

from PIL import Image
from matplotlib import pyplot

import solution

parser = argparse.ArgumentParser(description='Visualize your homework.')
parser.add_argument('file', type=str, help="JPEG file to manipulate")
parser.add_argument('operation',
                    choices=['create_histogram', 'lighten', 'darken',
                             'invert', 'rotate_left', 'rotate_right'],
                    help="Operation to be executed on given image.")
parser.add_argument('args', default=[], nargs="*", type=float,
                    help="Opearion arguments")

args = parser.parse_args()

image = Image.open(args.file)
pixels = list(image.getdata())
picture = []
for h in range(image.size[1]):
    picture.append(pixels[(h*image.size[0]):((h+1)*image.size[0])])

try:
    operation_result = getattr(solution, args.operation)(picture, *args.args)
    filename = '{}_{}.jpg'.format(args.file.split('.')[0], args.operation)
except Exception as exc:
    print("There's something wrong with your implementation of "
          "{0}()!\n".format(args.operation))
    raise exc

if args.operation == 'create_histogram':
    for color, histogram in operation_result.items():
        pyplot.bar(histogram.keys(), histogram.values(), alpha=0.6,
                   color=color)

    pyplot.savefig(filename)
else:
    new_pixels = [pixel for row in operation_result for pixel in row]
    new_image = None
    if args.operation in ('rotate_left', 'rotate_right'):
        new_image = Image.new('RGB', (image.size[1], image.size[0]))
    else:
        new_image = Image.new('RGB', image.size)
    new_image.putdata(new_pixels)
    new_image.save(filename, 'JPEG')


print("File saved as {}".format(filename))
