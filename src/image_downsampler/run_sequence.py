import os

from downsampler import downsampler


path = 'D:\\sparc\\experimental_data\\Tompkins\\Sample_1_07sept18\\image_sequence'
image_files = os.listdir(path)

output_dir = path + '\\' + 'resized'
if not os.path.exists(output_dir):
    os.mkdir(output_dir)

for image_file in image_files:
    image = os.path.join(path, image_file)

    image_file_name = image_file.split('.')[0]
    image_format = image_file.split('.')[1]
    output_image_name = image_file_name + '_DownSized' + '.' + image_format
    output_image = os.path.join(output_dir, output_image_name)
    downsampler(image, output_image, factor=0.95)
