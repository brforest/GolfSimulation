import numpy as np

hole_length = 380
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

fairway_driver = True
# get value for driver how far off center of fairway
off_center_driver = np.random.normal(0, 20)
print("Driver off center:", off_center_driver)

# get value for driver carry distance
carry_distance_driver = np.random.normal(300, 10)
print("Driver carry distance:", carry_distance_driver)

if off_center_driver > 10 or off_center_driver < -10:
    print("You drove it in the rough with the driver")
    fairway_driver = False
else:
    print("You drove it in the fairway with the driver")
    pass

driver_score = 1
if off_center_driver < -23:
    print("You hit your driver out of bounds, adding two to score")
    driver_score += 2
if off_center_driver > 50:
    print("You hit your driver in the penalty area, adding one to score")
    driver_score += 1
driver_length_to_hole = hole_length - carry_distance_driver
driver_score += calculate_approach_score(fairway_driver, driver_length_to_hole)
print("Driver score:", driver_score, "\n")

fairway_2i = True
# get value for 2i how far off center of fairway
off_center_2i = np.random.normal(0, 15)
print("2i off center:", off_center_2i)

# get value for driver carry distance
carry_distance_2i = np.random.normal(250, 10)
print("2i carry distance:", carry_distance_2i)

if off_center_2i > 14 or off_center_2i < -14:
    print("You drove it in the rough with the 2i")
    fairway_2i = False
else:
    print("You drove it in the fairway with the 2i")
    pass

score_2i = 1
if off_center_2i < -23:
    print("You hit your 2i out of bounds, adding two to score")
    score_2i += 2
if off_center_2i > 50:
    print("You hit your 2i in the penalty area, adding one to score")
    score_2i += 1
length_to_hole_2i = hole_length - carry_distance_2i
score_2i += calculate_approach_score(fairway_2i, length_to_hole_2i)
print("2i score:", score_2i, "\n")
