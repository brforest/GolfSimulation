import numpy as np
import cv2
import math as m

hole_length = 380
pixel_ratio = 7.4265734265
img = cv2.imread('images/Hole 18 Riverview/Hole 18 Riverview.jpg')
height, width, channels = img.shape
statistics = {
    "fairway_50-75": 2.95,
    "rough_50-75": 3.0,
    "fairway_75-100": 2.86,
    "rough_75-100": 3.1,
    "fairway_100-125": 2.87,
    "rough_100-125": 3.08,
    "fairway_125-150": 2.91,
    "rough_125-150": 3.13,
    "fairway_150-175": 3.0,
    "rough_150-175": 3.17,
    "fairway_175-200": 3.04,
    "rough_175-200": 3.25
}

def calculate_approach_score(fairway, distance):
    dict_string = ""
    if fairway:
        dict_string += "fairway_"
    else:
        dict_string += "rough_"
    if distance < 75:
        dict_string += "50-75"
    elif 75 <= distance < 100:
        dict_string += "75-100"
    elif 100 <= distance < 125:
        dict_string += "100-125"
    elif 125 <= distance < 150:
        dict_string += "125-150"
    elif 150 <= distance < 175:
        dict_string += "150-175"
    else:
        dict_string += "175-200"

    return statistics[dict_string]

def calculate_dist_to_center(off_line, off_yardage):
    return m.sqrt(off_line**2 + off_yardage**2)

scores_driver = []
scores_2i = []
distance_from_center_driver = []
distance_from_center_2i = []
num_simulations = 1000
for i in range(num_simulations):
    
    fairway_driver = True
    # get value for driver how far off center of fairway
    off_center_driver = np.random.normal(0, 20)
    # print("Driver off center:", off_center_driver)

    # get value for driver carry distance
    carry_distance_driver = np.random.normal(300, 10)
    # print("Driver carry distance:", carry_distance_driver)

    if off_center_driver > 10 or off_center_driver < -10:
        # print("You drove it in the rough with the driver")
        fairway_driver = False
    else:
        # print("You drove it in the fairway with the driver")
        pass

    driver_score = 1
    if off_center_driver < -23:
        # print("You hit your driver out of bounds, adding two to score")
        driver_score += 2
    if off_center_driver > 50:
        # print("You hit your driver in the penalty area, adding one to score")
        driver_score += 1
    driver_length_to_hole = hole_length - carry_distance_driver
    driver_score += calculate_approach_score(fairway_driver, driver_length_to_hole)
    # print("Driver score:", driver_score, "\n")
    scores_driver.append(driver_score)
    color = (255,0,0)
    if driver_score > 4.0:
        color = (0, 255, 0)
    elif driver_score < 4.0:
        color = (0, 0, 255)

    # draw on picture
    # cv2.line(img, (341,height-80), (340,height-80-int(carry_distance_driver*pixel_ratio)), (255,255,255), 15)
    cv2.circle(img, (341+int(off_center_driver*pixel_ratio),height-80-int(carry_distance_driver*pixel_ratio)), 15, color, -1)
    distance_from_center_driver.append(calculate_dist_to_center(off_center_driver, 300-carry_distance_driver))

    fairway_2i = True
    # get value for 2i how far off center of fairway
    off_center_2i = np.random.normal(0, 15)
    # print("2i off center:", off_center_2i)

    # get value for driver carry distance
    carry_distance_2i = np.random.normal(250, 10)
    # print("2i carry distance:", carry_distance_2i)

    if off_center_2i > 14 or off_center_2i < -14:
        # print("You drove it in the rough with the 2i")
        fairway_2i = False
    else:
        # print("You drove it in the fairway with the 2i")
        pass

    score_2i = 1
    if off_center_2i < -23:
        # print("You hit your 2i out of bounds, adding two to score")
        score_2i += 2
    if off_center_2i > 50:
        # print("You hit your 2i in the penalty area, adding one to score")
        score_2i += 1
    length_to_hole_2i = hole_length - carry_distance_2i
    score_2i += calculate_approach_score(fairway_2i, length_to_hole_2i)
    # print("2i score:", score_2i, "\n")
    scores_2i.append(score_2i)
    
    color = (150,0,0)
    if score_2i > 4.0:
        color = (0, 150, 0)
    elif score_2i < 4.0:
        color = (0, 0, 150)

    # draw on picture
    # cv2.line(img, (341,height-80), (340,height-80-int(carry_distance_driver*pixel_ratio)), (255,255,255), 15)
    cv2.circle(img, (341+int(off_center_2i*pixel_ratio),height-80-int(carry_distance_2i*pixel_ratio)), 15, color, -1)
    distance_from_center_2i.append(calculate_dist_to_center(off_center_2i, 250-carry_distance_2i))

avg_driver_score = sum(scores_driver) / len(scores_driver)
avg_2i_score = sum(scores_2i) / len(scores_2i)
print("Average driver score:", avg_driver_score)
print("Average 2i score:", avg_2i_score)
# create topographical lines
# 25%
# 50%
# 75%
# 100%
distance_from_center_driver.sort()
distance_from_center_2i.sort()
# driver first
first_50 = distance_from_center_driver[int((len(distance_from_center_driver)-1) / 2)]
first_75 = distance_from_center_driver[int(3 * (len(distance_from_center_driver)-1) / 4)]
first_98 = distance_from_center_driver[int(98 * (len(distance_from_center_driver) - 1) / 100)]
cv2.circle(img, (341, height-80-int(300*pixel_ratio)), int(first_50*pixel_ratio), (0,0,0), 10)
cv2.circle(img, (341, height-80-int(300*pixel_ratio)), int(first_75*pixel_ratio), (0,0,0), 10)
cv2.circle(img, (341, height-80-int(300*pixel_ratio)), int(first_98*pixel_ratio), (0,0,0), 10)
# now the 2i
first_50 = distance_from_center_2i[int((len(distance_from_center_2i)-1) / 2)]
first_75 = distance_from_center_2i[int(3 * (len(distance_from_center_2i)-1) / 4)]
first_98 = distance_from_center_2i[int(98 * (len(distance_from_center_2i) - 1) / 100)]
cv2.circle(img, (341, height-80-int(250*pixel_ratio)), int(first_50*pixel_ratio), (250,250,250), 10)
cv2.circle(img, (341, height-80-int(250*pixel_ratio)), int(first_75*pixel_ratio), (250,250,250), 10)
cv2.circle(img, (341, height-80-int(250*pixel_ratio)), int(first_98*pixel_ratio), (250,250,250), 10)
cv2.imshow('Simulation Results', img)
cv2.waitKey(0)
cv2.destroyAllWindows()