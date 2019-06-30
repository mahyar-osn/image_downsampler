"""
A simple module to downsample images using OpenCV.
"""
import os
import argparse

import cv2
import math

INTERPOLATION_KEY = dict(nearest=cv2.INTER_NEAREST,
                         linear=cv2.INTER_LINEAR,
                         area=cv2.INTER_AREA,
                         cubic=cv2.INTER_CUBIC,
                         lanczos4=cv2.INTER_LANCZOS4)


class ProgramArguments(object):
    pass


def _save_image(path, image):
    cv2.imwrite(path, image)


def _resize(im, size, interpolant):
    return cv2.resize(im, dsize=size, interpolation=interpolant)


def _get_new_size(height, width, pixel_area):
    aspect_ratio = width / height
    new_height = int(math.sqrt(pixel_area / aspect_ratio) + 0.5)
    new_width = int((new_height * aspect_ratio) + 0.5)
    return new_height, new_width


def downsampler(input_image, output_image, factor=0.3, interpolant=INTERPOLATION_KEY['cubic']):
    image_object = cv2.imread(input_image)
    height, width, _ = image_object.shape
    scale_factor = 1.0 - factor
    source_pixel_area = height * width
    target_pixel_area = source_pixel_area * scale_factor
    new_height, new_width = _get_new_size(height, width, target_pixel_area)

    print(new_height / height, new_width / width)

    new_image_object = _resize(image_object, (math.ceil(new_width), math.ceil(new_height)), interpolant=interpolant)
    _save_image(output_image, new_image_object)


def main():
    args = parse_args()
    if os.path.exists(args.input_image):

        input_image = args.input_image

        file_path, _ = os.path.split(args.input_image)
        file_name_path, image_format = os.path.splitext(args.input_image)
        file_name = file_name_path.split('\\')[-1]

        if args.output_image is None:
            output_path = file_path + '\\resized_images\\'
            if not os.path.exists(output_path):
                os.mkdir(output_path)
            output_image = output_path + '\\' + file_name + '_DownSized{}'.format(image_format)
        else:
            output_image = args.output_image

        if os.path.exists(output_image):
            os.remove(output_image)

        if args.downsampling_factor is None:
            downsampling = 0.3
        else:
            downsampling = float(args.downsampling_factor)

        if args.interpolant is None:
            interpolant = INTERPOLATION_KEY['cubic']
        else:
            interpolant = args.interpolant

        # Downsample
        downsampler(input_image, output_image, factor=downsampling, interpolant=interpolant)


def parse_args():
    parser = argparse.ArgumentParser(description="Downsampling of 2D image data.")
    parser.add_argument("input_image", help="Location of the input image file.")
    parser.add_argument("--output_image", help="Location of the output downsampled image file. "
                                               "[defaults to the location of the input file if not set.]")
    parser.add_argument("--downsampling_factor", help="A downsample factor to reduce the data file. "
                                                      "[default is 0.3 (30%)]")
    parser.add_argument("--interpolant", help="Interpolation parameter."
                                              "Options: \n"
                                              "\t nearest - a nearest-neighbor interpolation\n"
                                              "\t linear - a bilinear interpolation (used by default)\n"
                                              "\t area  -  resampling using pixel area relation. "
                                              "It may be a preferred method for image decimation, as it gives "
                                              "moire’-free results. But when the image is zoomed, it is "
                                              "similar to the INTER_NEAREST method.\n"
                                              "\t cubic - a bicubic interpolation over 4x4 pixel "
                                              "neighborhood\n"
                                              "lanczos4 - a Lanczos interpolation over 8x8 pixel "
                                              "neighborhood\n"
                                              "[default is cubic]")

    program_arguments = ProgramArguments()
    parser.parse_args(namespace=program_arguments)

    return program_arguments


if __name__ == '__main__':
    main()
