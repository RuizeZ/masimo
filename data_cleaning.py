import cv2
import os
import shutil
good_image_folder = '/home/ruizezhang/Desktop/data_cleaning_on_good/bed/good_image'
bad_image_folder = '/home/ruizezhang/Desktop/data_cleaning_on_good/bed/bad_image'
path = '/media/ruizezhang/16GB/New_labelled_data/Bed/'

def open_image(fileName, path, coordinates_list):
    image = cv2.imread(curr_image_path)
    
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
    while(True):
        x = input('result: ')
        if x == 'y':
            shutil.copy(path+fileName+'.jpg', good_image_folder)
            shutil.copy(path+fileName+'.txt', good_image_folder)
            print('move to good')
            break
        elif x == 'n':
            shutil.copy(path+fileName+'.jpg', bad_image_folder)
            print('move to bad')
            break
    cv2.destroyAllWindows()

os.chdir(path)
valid_coordinates = True
totalImage = int(len(os.listdir()) / 2)
count = 1
for file in os.listdir():
    if file.endswith('.txt'):
        print(f'{str(count)} / {str(totalImage)}')
        coordinates_list = []
        coordinates = []
        curr_file_path = f'{path}/{file}'
        curr_file = open(curr_file_path, 'r')
        lines = curr_file.readlines()
        print("current file: " + file)
        if len(lines) == 0:
            shutil.copy(path+file[0:-4]+'.jpg', bad_image_folder)
            print('empty txt file, move to bad')

        for line in lines:
            coordinates = list(line[2:-1].split(" "))
            for coordinate in coordinates:
                if float(coordinate) > 1:
                    valid_coordinates = False
                    shutil.copy(path+file[0:-4]+'.jpg', bad_image_folder)
                    print('>1 coordinate, move to bad')
                    break
            if valid_coordinates:
                coordinates_list.append(coordinates)
            else:
                coordinates_list = []
                valid_coordinates = True
                break
        print(coordinates_list)
        if len(coordinates_list) != 0:
            curr_image_path = curr_file_path[:-4] + '.jpg'
            open_image(file[0:-4], path, coordinates_list)
        count += 1