import cv2
from imgaug.augmentables.bbs import BoundingBox, BoundingBoxesOnImage
from imgaug import augmenters as iaa
import imgaug as ia
import os
path = '/home/ruizezhang/Desktop/phase2_result/bed/good_image'
target = '/home/ruizezhang/Desktop/imgaug/demo/'
total_aug_image = 0


def convert_to_Yolo(x1, y1, x2, y2, image_w, image_h):
    return [((x2 + x1)/(2*image_w)), ((y2 + y1)/(2*image_h)), (x2 - x1)/image_w, (y2 - y1)/image_h]


def open_image(fileName, path, coordinates_list):
    global total_aug_image
    print("current file1: " + fileName)
    image = cv2.imread(fileName + '.jpg')
    window_name = fileName
    BoundingBoxList = []
    # convert from Yolo to Pascal_VOC, put bounding box in the BoundingBoxList
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
        color = (255, 0, 0)
        BoundingBoxList.append(BoundingBox(xmin, ymin, xmax, ymax))
    # cv2.imshow(window_name, image)
    # cv2.waitKey(0)

    bbs = BoundingBoxesOnImage(BoundingBoxList, shape=image.shape)
    for img_num in range(5):
        new_file_name = fileName + '_aug_' + str(img_num)
        image_aug, bbs_aug = iaa.Affine(scale=(0.5, 1), translate_percent={"x": (-0.2, 0.2), "y": (-0.2, 0.2)}, rotate=(-90, 90), shear=(-45, 45), fit_output=True)(
            image=image, bounding_boxes=bbs)
        # remove out side bounding box
        f = open(target + new_file_name + ".txt", "w")
        for i in range(len(BoundingBoxList)):
            curr_bounding_box = bbs_aug.remove_out_of_image().clip_out_of_image()[i].shift(
                left=0, top=0).draw_on_image(image_aug, size=2, color=color)
            image_h = curr_bounding_box.shape[0]
            image_w = curr_bounding_box.shape[1]
            after = bbs_aug.remove_out_of_image().clip_out_of_image()[i].shift(
                left=0, top=0)
            # convert to Yolo format
            Yolo_coordinates_list = convert_to_Yolo(
                after.x1, after.y1, after.x2, after.y2, image_w, image_h)
            # write Yolo format to txt file
            f.write('0 ')
            f.write(str(Yolo_coordinates_list[0]) + ' ')
            f.write(str(Yolo_coordinates_list[1]) + ' ')
            f.write(str(Yolo_coordinates_list[2]) + ' ')
            f.write(str(Yolo_coordinates_list[3]) + '\n')
        f.close()
        # cv2.imshow(window_name, image_aug)
        # cv2.waitKey(0)
        cv2.imwrite(target + new_file_name + '.jpg', image_aug)
        total_aug_image += 1
        print('total_aug_image: ' + str(total_aug_image))
    # cv2.destroyAllWindows()


os.chdir(path)
valid_coordinates = True
totalImage = int(len(os.listdir()) / 2)
count = 1
for file in os.listdir():
    if count == 50:
        break
    if file.endswith('.txt'):
        print(f'{str(count)} / {str(totalImage)}')
        coordinates_list = []
        coordinates = []
        curr_file_path = f'{path}/{file}'
        curr_file = open(curr_file_path, 'r')
        lines = curr_file.readlines()
        print("current file: " + file)
        for line in lines:
            coordinates = list(line[:-1].split(" "))
            coordinates_list.append(coordinates[1:])
        print(coordinates_list)
        if len(coordinates_list) != 0:
            open_image(file[0:-4], path, coordinates_list)
        count += 1
