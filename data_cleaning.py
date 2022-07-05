import cv2
import os
import shutil

def open_image(fileName, curr_image_path, curr_file_path, coordinates_list):
    image = cv2.imread(curr_image_path)
    dst_path= '/home/ruizezhang/Desktop/data_cleaning_on_good/tap/new_good_image'
    window_name = fileName
    # draw the rectangle
    for coordinates in coordinates_list:
        height = image.shape[0]
        width = image.shape[1]
        x = float(coordinates[0])
        y = float(coordinates[1])
        w = float(coordinates[2])
        h = float(coordinates[3])
        xmax = int((x*width) + (w * width)/2.0)
        xmin = int((x*width) - (w * width)/2.0)
        ymax = int((y*height) + (h * height)/2.0)
        ymin = int((y*height) - (h * height)/2.0)
        start_point = (xmin, ymin)
        end_point = (xmax, ymax)
        color = (255, 0, 0)
        thickness = 2
        image = cv2.rectangle(image, start_point, end_point, color, thickness)
    cv2.imshow(window_name, image)
    cv2.waitKey(500)
    x = input('result: ')
    if x == 'y':
        shutil.copy(curr_image_path, dst_path)
        shutil.copy(curr_file_path, dst_path)
    cv2.destroyAllWindows()

good_image_folder = '/home/ruizezhang/Desktop/data_cleaning_on_good/tap/Good_Image'
os.chdir(good_image_folder)
valid_coordinates = True
totalImage = int(len(os.listdir()) / 2)
count = 1
for file in os.listdir():
    if file.endswith('.txt'):
        print(f'{str(count)} / {str(totalImage)}')
        coordinates_list = []
        coordinates = []
        curr_file_path = f'{good_image_folder}/{file}'
        curr_file = open(curr_file_path, 'r')
        lines = curr_file.readlines()
        print("current file: " + file)
        for line in lines:
            coordinates = list(line[2:-1].split(" "))
            for coordinate in coordinates:
                if float(coordinate) > 1:
                    valid_coordinates = False
                    break
            if valid_coordinates:
                coordinates_list.append(coordinates)
            else:
                valid_coordinates = True
                break
        print(coordinates_list)
        if len(coordinates_list) != 0:
            curr_image_path = curr_file_path[:-4] + '.jpg'
            open_image(file, curr_image_path, curr_file_path, coordinates_list)
        count += 1