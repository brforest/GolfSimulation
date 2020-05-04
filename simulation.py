import numpy as np
import cv2
import math as m
from tkinter import ttk
import tkinter as tk
import PIL.Image, PIL.ImageTk


class Shot:
    def __init__(self, club, from_center, off_target, distance_from_average):
        self.club = club
        self.from_center = from_center
        self.off_target = off_target
        self.distance_from_average = distance_from_average
    
    def get_club(self):
        return self.club

    def get_dist_from_center(self):
        return self.from_center
    
    def get_off_target(self):
        return self.off_target
    
    def get_distance_from_average(self):
        return self.distance_from_average


class Simulation():
    def __init__(self):
        hole_length = 380
        pixel_ratio = 7.4265734265
        self.img_driver = cv2.cvtColor(cv2.imread('images/Hole 18 Riverview/Hole 18 Riverview.jpg'), cv2.COLOR_BGR2RGB)
        self.img_2i = cv2.cvtColor(cv2.imread('images/Hole 18 Riverview/Hole 18 Riverview.jpg'), cv2.COLOR_BGR2RGB)
        height, width, channels = self.img_driver.shape
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
            # cv2.line(img_driver, (341,height-80), (340,height-80-int(carry_distance_driver*pixel_ratio)), (255,255,255), 15)
            cv2.circle(self.img_driver, (341+int(off_center_driver*pixel_ratio),height-80-int(carry_distance_driver*pixel_ratio)), 15, color, -1)
            new_shot = Shot("driver", calculate_dist_to_center(off_center_driver, 300-carry_distance_driver), off_center_driver, 300-carry_distance_driver)
            distance_from_center_driver.append(new_shot)

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
            # cv2.line(img_driver, (341,height-80), (340,height-80-int(carry_distance_driver*pixel_ratio)), (255,255,255), 15)
            cv2.circle(self.img_2i, (341+int(off_center_2i*pixel_ratio),height-80-int(carry_distance_2i*pixel_ratio)), 15, color, -1)
            new_shot = Shot("2i", calculate_dist_to_center(off_center_2i, 250-carry_distance_2i), off_center_2i, 250-carry_distance_2i)
            distance_from_center_2i.append(new_shot)

        avg_driver_score = sum(scores_driver) / len(scores_driver)
        avg_2i_score = sum(scores_2i) / len(scores_2i)
        print("Average driver score:", avg_driver_score)
        print("Average 2i score:", avg_2i_score)
        # create topographical lines
        # 25%
        # 50%
        # 75%
        # 100%
        distance_from_center_driver.sort(key=lambda x: x.from_center)
        distance_from_center_2i.sort(key=lambda x: x.from_center)
        # TODO: find a better way of creating these ellipses???
        # driver first
        first_driver_50 = int(num_simulations/2)
        first_driver_50_shots = distance_from_center_driver[0:first_driver_50]
        first_driver_50_shots.sort(key=lambda x: x.distance_from_average)
        furthest_distance = first_driver_50_shots[first_driver_50-1]
        first_driver_50_distance_from_average_pixels = abs(int(furthest_distance.get_distance_from_average() * pixel_ratio))
        first_driver_50_shots.sort(key=lambda x: x.off_target)
        furthest_off = first_driver_50_shots[first_driver_50-1]
        first_driver_50_off_target_pixels = abs(int(furthest_off.get_off_target() * pixel_ratio))

        first_driver_75 = int(3 * (num_simulations-1) / 4)
        first_driver_75_shots = distance_from_center_driver[0:first_driver_75]
        first_driver_75_shots.sort(key=lambda x: x.distance_from_average)
        furthest_distance = first_driver_75_shots[first_driver_75-1]
        first_driver_75_distance_from_average_pixels = abs(int(furthest_distance.get_distance_from_average() * pixel_ratio))
        first_driver_75_shots.sort(key=lambda x: x.off_target)
        furthest_off = first_driver_75_shots[first_driver_75-1]
        first_driver_75_off_target_pixels = abs(int(furthest_off.get_off_target() * pixel_ratio))

        first_driver_98 = int(98 * (num_simulations-1) / 100)
        first_driver_98_shots = distance_from_center_driver[0:first_driver_98]
        first_driver_98_shots.sort(key=lambda x: x.distance_from_average)
        furthest_distance = first_driver_98_shots[first_driver_98-1]
        first_driver_98_distance_from_average_pixels = abs(int(furthest_distance.get_distance_from_average() * pixel_ratio))
        first_driver_98_shots.sort(key=lambda x: x.off_target)
        furthest_off = first_driver_98_shots[first_driver_98-1]
        first_driver_98_off_target_pixels = abs(int(furthest_off.get_off_target() * pixel_ratio))

        # print(first_driver_50_off_target_pixels)
        # print(first_driver_50_distance_from_average_pixels)
        # print(first_driver_75_off_target_pixels)
        # print(first_driver_75_distance_from_average_pixels)
        # print(first_driver_98_off_target_pixels)
        # print(first_driver_98_distance_from_average_pixels)

        # now the 2i
        first_2i_50 = int(num_simulations/2)
        first_2i_50_shots = distance_from_center_2i[0:first_2i_50]
        first_2i_50_shots.sort(key=lambda x: x.distance_from_average)
        furthest_distance = first_2i_50_shots[first_2i_50-1]
        first_2i_50_distance_from_average_pixels = abs(int(furthest_distance.get_distance_from_average() * pixel_ratio))
        first_2i_50_shots.sort(key=lambda x: x.off_target)
        furthest_off = first_2i_50_shots[first_2i_50-1]
        first_2i_50_off_target_pixels = abs(int(furthest_off.get_off_target() * pixel_ratio))

        first_2i_75 = int(3 * (num_simulations-1) / 4)
        first_2i_75_shots = distance_from_center_2i[0:first_2i_75]
        first_2i_75_shots.sort(key=lambda x: x.distance_from_average)
        furthest_distance = first_2i_75_shots[first_2i_75-1]
        first_2i_75_distance_from_average_pixels = abs(int(furthest_distance.get_distance_from_average() * pixel_ratio))
        first_2i_75_shots.sort(key=lambda x: x.off_target)
        furthest_off = first_2i_75_shots[first_2i_75-1]
        first_2i_75_off_target_pixels = abs(int(furthest_off.get_off_target() * pixel_ratio))

        first_2i_98 = int(98 * (num_simulations-1) / 100)
        first_2i_98_shots = distance_from_center_2i[0:first_2i_98]
        first_2i_98_shots.sort(key=lambda x: x.distance_from_average)
        furthest_distance = first_2i_98_shots[first_2i_98-1]
        first_2i_98_distance_from_average_pixels = abs(int(furthest_distance.get_distance_from_average() * pixel_ratio))
        first_2i_98_shots.sort(key=lambda x: x.off_target)
        furthest_off = first_2i_98_shots[first_2i_98-1]
        first_2i_98_off_target_pixels = abs(int(furthest_off.get_off_target() * pixel_ratio))

        # print(first_2i_50_off_target_pixels)
        # print(first_2i_50_distance_from_average_pixels)
        # print(first_2i_75_off_target_pixels)
        # print(first_2i_75_distance_from_average_pixels)
        # print(first_2i_98_off_target_pixels)
        # print(first_2i_98_distance_from_average_pixels)

        cv2.ellipse(self.img_2i, (341, height-80-int(250*pixel_ratio)), (first_2i_50_off_target_pixels, first_2i_50_distance_from_average_pixels), 0, 0, 360, (0,0,0), 10)
        cv2.ellipse(self.img_2i, (341, height-80-int(250*pixel_ratio)), (first_2i_75_off_target_pixels, first_2i_75_distance_from_average_pixels), 0, 0, 360, (0,0,0), 10)
        cv2.ellipse(self.img_2i, (341, height-80-int(250*pixel_ratio)), (first_2i_98_off_target_pixels, first_2i_98_distance_from_average_pixels), 0, 0, 360, (0,0,0), 10)

        cv2.ellipse(self.img_driver, (341, height-80-int(300*pixel_ratio)), (first_driver_50_off_target_pixels, first_driver_50_distance_from_average_pixels), 0, 0, 360, (0,0,0), 10)
        cv2.ellipse(self.img_driver, (341, height-80-int(300*pixel_ratio)), (first_driver_75_off_target_pixels, first_driver_75_distance_from_average_pixels), 0, 0, 360, (0,0,0), 10)
        cv2.ellipse(self.img_driver, (341, height-80-int(300*pixel_ratio)), (first_driver_98_off_target_pixels, first_driver_98_distance_from_average_pixels), 0, 0, 360, (0,0,0), 10)

        # cv2.imshow('Simulation Results', img_2i)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        scale_percent = 20 # percent of original size
        width = int(self.img_driver.shape[1] * scale_percent / 100)
        height = int(self.img_driver.shape[0] * scale_percent / 100)
        dim = (width, height)
        # resize image
        self.img_driver = cv2.resize(self.img_driver, dim, interpolation = cv2.INTER_AREA) 
        self.img_2i = cv2.resize(self.img_2i, dim, interpolation = cv2.INTER_AREA) 

        self.window = tk.Tk()

        height, width, no_channels = self.img_driver.shape

        self.display_image = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.img_driver))
        self.label = tk.Label(self.window, image=self.display_image)
        self.label.pack()
        # tk_img_2i = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(img_2i))
        # image_id = canvas.create_image(0,0,image=display_image,anchor=tk.NW)
        self.current_club = tk.StringVar()
        button=ttk.Button(self.window, textvariable=self.current_club, width=50, command=self.change_club)
        self.current_club.set("2i")
        button.pack(anchor=tk.CENTER, expand=True)

        self.window.mainloop()

    def change_club(self):
        if self.current_club.get() == "2i":
            # print("switching to 2i")
            self.current_club.set("driver")
            # display the 2i
            self.display_image = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.img_2i))
            self.label.configure(image=self.display_image)

        elif self.current_club.get() == "driver":
            # print("switching to driver")
            self.current_club.set("2i")
            # display the driver
            self.display_image = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.img_driver))
            self.label.configure(image=self.display_image)

simulation = Simulation()