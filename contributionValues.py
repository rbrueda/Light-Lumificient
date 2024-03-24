# Purpose: defining points and action points to calculate contribution of light and window fixtures for calculating total brightness

#used to perform distance metric
from scipy.spatial import distance

class Contribution:
    def __init__(self, option):

        print("sensors checking for coordinates ....")

        #coordinates for windows
        self.W1_point = (38, 352)
        self.W2_point = (92, 25)

        #checks for which option is chosen and creates coordinates of locations accordingly 

        # profile tells us that user studies in desk
        if (option == "study"):
            self.option_point = (113, 290)
            self.L1_point = (240, 292)
            self.L2_point = (101, 285)
            self.L3_point = (269, 82)
            self.L4_point = (505, 74)

        # profile tells us that user is watching movie in bench near bed
        if (option == "movie"):
            self.option_point = (404, 260)
            self.L1_point = (385, 256)
            self.L2_point = (100, 267)
            self.L3_point = (292, 85)
            self.L4_point = (521, 86)

        # profile tells us that user is listening to music in couch
        if (option == "music"):
            self.option_point = (129, 97)
            self.L1_point = (261, 241)
            self.L2_point = (85, 258)
            self.L3_point = (255, 63)
            self.L4_point = (500, 61)

        # profile tells us that user is sleeping in bed
        if (option == "sleep"):
            self.option_point = (403, 112)
            self.L1_point = (339, 221)
            self.L2_point = (100, 267)
            self.L3_point = (308, 75)
            self.L4_point = (505, 74)

        #special case for clean option -- user is constantly moving around, so contribution factor is uniform
        if (option != "clean"):
            euclidean_distance_L1 = distance.euclidean(self.option_point, self.L1_point)
            euclidean_distance_L2 = distance.euclidean(self.option_point, self.L2_point)
            euclidean_distance_L3 = distance.euclidean(self.option_point, self.L3_point)
            euclidean_distance_L4 = distance.euclidean(self.option_point, self.L4_point)

            #to calculate contribution for outside brightness levels
            euclidean_distance_W1 = distance.euclidean(self.option_point, self.W1_point)
            euclidean_distance_W2 = distance.euclidean(self.option_point, self.W2_point)
            
            #get the inverse of all the euclidean values (so that the smaller vales represent higher ratio values)
            inverse_L1 = 1 / euclidean_distance_L1
            inverse_L2 = 1 / euclidean_distance_L2
            inverse_L3 = 1 / euclidean_distance_L3
            inverse_L4 = 1 / euclidean_distance_L4

            sumOfInvertedDistances = inverse_L1 + inverse_L2 + inverse_L3 + inverse_L4
            self.ratio_L1 = inverse_L1/sumOfInvertedDistances
            self.ratio_L2 = inverse_L2/sumOfInvertedDistances
            self.ratio_L3 = inverse_L3/sumOfInvertedDistances
            self.ratio_L4 = inverse_L4/sumOfInvertedDistances

            #include outside values
            inverse_W1 = 1 / euclidean_distance_W1
            inverse_W2 = 1 / euclidean_distance_W2
            totalIntensity = sumOfInvertedDistances + inverse_W1 + inverse_W2

            self.ratio_W1 = inverse_W1 / totalIntensity
            self.ratio_W2 = inverse_W2 / totalIntensity
            
            print ("RESULTS: ")
            print(f"W1 Total Light Contribution: {self.ratio_W1}")
            print(f"W2 Total Light COntribution: {self.ratio_W2}")

            self.outsideBrightnessContribution = self.ratio_W1 + self.ratio_W2
            print(f"outsideBrightness contribution: {self.outsideBrightnessContribution}") #make up 40% of total brightness from outside

            print(f"L1 Total Light Contribution: {self.ratio_L1}")
            print(f"L2 Total Light Contribution: {self.ratio_L2}")
            print(f"L3 Total Light Contribution: {self.ratio_L3}")
            print(f"L4 Total Light Contribution: {self.ratio_L4}")

        else: # clean option
            self.ratio_L1 = 0.25
            self.ratio_L2 = 0.25
            self.ratio_L3 = 0.25
            self.ratio_L4 = 0.25
            self.outsideBrightnessContribution = 0.5

    #a dictionary with all the ratio based values
    def getValues(self):
        contribution = {
            'L1': self.ratio_L1,
            'L2': self.ratio_L2,
            'L3': self.ratio_L3,
            'L4': self.ratio_L4,
            'outsideContribution': self.outsideBrightnessContribution
        }
        return contribution
