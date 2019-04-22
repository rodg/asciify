from PIL import Image

ASCII_CHARS = ['.',',',':',';','+','*','?','%','S','#','@']
ASCII_CHARS = ASCII_CHARS[::-1]
BINARY = ['0', '1']
BINARY = BINARY[::-1]

'''
method resize():
    - takes as parameters the image, and the final width
    - resizes the image into the final width while maintaining aspect ratio
'''
def resize(image, new_width=100):
    (old_width, old_height) = image.size
    aspect_ratio = float(old_height)/float(old_width)
    new_height = int(aspect_ratio * new_width)
    new_dim = (new_width, new_height)
    new_image = image.resize(new_dim)
    return new_image
'''
method grayscalify():
    - takes an image as a parameter
    - returns the grayscale version of image
'''
def grayscalify(image):
    return image.convert('L')

'''
method modify():
    - replaces every pixel with a character whose intensity is similar
'''
def modify(image, buckets=25, use_binary=False):
    if use_binary:
        buckets=240
        initial_pixels = list(image.getdata())
        #for pixel_value in initial_pixels:
        #    print(pixel_value)
        new_pixels = [BINARY[pixel_value//buckets] for pixel_value in initial_pixels]
    else:
        initial_pixels = list(image.getdata())
        new_pixels = [ASCII_CHARS[pixel_value//buckets] for pixel_value in initial_pixels]
    return ''.join(new_pixels)

'''
method do():
    - does all the work by calling all the above functions
'''
def do(image, new_width=100, use_binary=False):
    image = resize(image, new_width)
    image = grayscalify(image)

    pixels = modify(image, use_binary=use_binary)
    len_pixels = len(pixels)

    # Construct the image from the character list
    if use_binary:
        bit_map = []
        for index in range(0, len_pixels, 8):
            entry = pixels[index:index+8]
            entry = hex(int(entry, 2))
            bit_map.append(entry)
        print('{', end=' ')
        i = 0
        for byte in bit_map:
            if i%8 is 0:
                e = ',\n'
            else:
                e = ', '
            print(str(byte), end=e)
            i+=1
        print('};', end='\n')

    new_image = [pixels[index:index+new_width] for index in range(0, len_pixels, new_width)]

    return '\n'.join(new_image)

'''
method runner():
    - takes as parameter the image path and runs the above code
    - handles exceptions as well
    - provides alternative output options
'''
def runner(path, destination, new_width, use_binary):
    image = None
    try:
        image = Image.open(path)
    except Exception:
        print("Unable to find image in",path)
        #print(e)
        return
    image = do(image, new_width, use_binary)

    # To print on console
    if not use_binary:
        print(image)

    # Else, to write into a file
    # Note: This text file will be created by default under
    #       the same directory as this python file,
    #       NOT in the directory from where the image is pulled.
    f = open(destination,'w')
    f.write(image)
    f.close()

'''
method main():
    - reads input from console
    - profit
'''
if __name__ == '__main__':
    import argparse
    import urllib.request
    parser = argparse.ArgumentParser(description='jpg to ascii')
    parser.add_argument('target', default=None)
    parser.add_argument('-o', '--output',
                        #type='string',
                        dest='destination',
                        default='img.txt',
                        help='output filename')
    parser.add_argument('-r', '--resize',
                        type=int,
                        dest='new_width',
                        default=100,
                        help='width of resized image')
    parser.add_argument('-b', '--binary',
                        action='store_true',
                        default=False,
                        dest='use_binary',
                        help='convert image into binary')
    args = parser.parse_args()
    if args.target.startswith('http://') or args.target.startswith('https://'):
        urllib.request.urlretrieve(args.target, "asciify.jpg")
        path = "asciify.jpg"
    else:
        path = args.target
    runner(path, destination=args.destination,
            new_width=args.new_width,
            use_binary=args.use_binary)
