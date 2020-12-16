print('Initializing...\n')
from os import listdir, mkdir, getcwd
from os.path import isfile, isdir, splitext, join, dirname
from scipy.signal import find_peaks, peak_widths
import cv2
import numpy as np
import csv

''' Used for visualization '''
edges = False   #Graph the edge used for aligning the strip
graphs = False  #Graph pixel intensity along the strip (spike == activated strip)
saveBoxes = True   #Save the processed image corresponding to its table entry
showBoxes = False   #Show the processed image immediately
if edges or graphs:
    from matplotlib import pyplot

''' Tuning adjustments '''
y_range = 100   #Sets the height of each detected box
x_range = 200   #Sets the width of each detected box

#About half the width of the strip, if nothing's found check this first
defaultCenterSpace = 200
                            
#Reaction strips should fall within this range of y-values
crop_y1, crop_y2 = 1900, 3000

#Determines the y-values around which the reference boxes should be centered
referenceDistance1, referenceDistance2 = 1500, 3000

#Sets the minimum number of detected points to be accepted as a line (250 is good)
#If you aren't finding any edges, try lowering this
#(although it's more likely an image problem at that point)
minLine = 250

def getData(imagePath, drawLines, graphPeaks):
    x = cv2.imread(imagePath)
    x_x, y_x = x.shape[0:2]
    
    # convert the image to grayscale, blur it, and find edges
    gray = cv2.cvtColor(x, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5,5),0)
    edges = cv2.Canny(gray, 50, 200, apertureSize = 5)
    
    
    # last parameter sets minimum number of points to classifly line; the more the better as long as there aren't any crazy outliers... could be more robust
    
    lines = cv2.HoughLines(edges,1,np.pi/180,minLine)
    mid_x = []
    try:
        for line in lines:
            for rho, theta in line:
                #store the projected x-value at the center for each line
                mid_x.append(rho * np.cos(theta) - (y_x/2 - rho * np.sin(theta)) * np.tan(theta))
    except:
        print('\tUnable to find edges, adjust minLine?')
        return [0,0],x
    
    # separate left bounds from right bounds
    bounds = sorted(mid_x)
    center = 0
    if (sd := np.std(bounds)) > 80:
        mid = 0
        for i in range(1, len(bounds)):
            if bounds[i] - bounds[i - 1] > sd:
                mid = i
                break
        lastBounds = [np.mean(bounds[:mid]), np.mean(bounds[mid:])]
        center = np.mean(lastBounds)
    
    if center == 0 :
        bound = int(np.mean(bounds))
        center = bound - defaultCenterSpace if (np.mean(x[int(y_x/2)][bound - defaultCenterSpace]) > np.mean(x[int(y_x / 2)][bound + defaultCenterSpace])) else bound + defaultCenterSpace

    crop_left, crop_right = int(center - x_range / 2), int(center + x_range / 2)

    
    # use the average line tilt
    r = np.mean(lines[0,:,1])
    r = np.rad2deg(r)
    r = r if r <= 90 else r - 180
    r = r if r <= 90 else r - 180

    # draws detected lines, the first of which is used for alignment
    if (drawLines):
        for line in lines:
            for rho,theta in line:
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a*rho
                y0 = b*rho
                x1 = int(x0 + 4000*(-b))
                y1 = int(y0 + 4000*(a))
                x2 = int(x0 - 4000*(-b))
                y2 = int(y0 - 4000*(a))
                cv2.line(x,(x1,y1),(x2,y2),(0,0,255),2)
        cv2.line(x,(int(center), int(y_x/2) + 1000), (int(center), int(y_x/2) - 50),(255,100,100),5)
        #Uncomment this to view edges before rotation
        cv2.imshow(imagePath + ' edge...',x)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    #rotate about center of image.
    M = cv2.getRotationMatrix2D(center=(mid_x[0], y_x/2), angle = r, scale=1)
    rotatedImg = cv2.warpAffine(x, M, dsize=(y_x, x_x))
    croppedImg = rotatedImg[crop_y1:crop_y2, crop_left:crop_right,:]
        
    #produce a 'heat map' for pixel intesity with each point being the sum of a row
    lateralSum = np.sum(np.sum(croppedImg, axis = 2),axis = 1)
    
    #find the peaks and return the coordinates (will return the indexes of ROWS from the image)
    prom = 1
    while(True):
        peaks,properties = find_peaks(lateralSum, prominence = prom, width = 20, distance=200)
        if len(peaks) != 0:
            break
        prom = prom - .2
        
    #adjust the detected peak to hit the middle of the strip
    widths, width_heights, left_ips, right_ips = peak_widths(lateralSum, peaks, rel_height = 0.5,prominence_data=None, wlen=None)
    
    
        #graph the pixel intensity along the strip
    if (graphPeaks):
        pyplot.plot(range(len(lateralSum)),lateralSum)
        pyplot.plot(peaks, lateralSum[peaks], "x")
        pyplot.plot(left_ips, lateralSum[[int(l) for l in left_ips]], ".", c="r")
        pyplot.plot(right_ips, lateralSum[[int(r) for r in right_ips]], ".", c= "r")
        pyplot.title(imagePath)
        pyplot.show()
    
        
    peaks += crop_y1
    left_ips += crop_y1
    right_ips += crop_y1
    
    if len(peaks) == 1:
        peaks =  np.append(peaks,[peaks[0] + 400])
        left_ips = np.append(left_ips,[peaks[0] + 400 - int(y_range/2)])
        right_ips = np.append(right_ips,[peaks[0] + 400 + int(y_range/2)])
    
    #produce return array
    values = []
    for i in range(len(peaks)):
        peak = int((left_ips[i] + right_ips[i]) / 2)
        values.append(np.sum(np.sum(np.sum(rotatedImg[(peak-int(y_range/2)):(peak+int(y_range/2)),crop_left:crop_right,:], axis=2), axis=1)))
    
    #delete extra strips
    while(len(values) > 2):
        min_index = values.index(min(values[1:]))
        values.pop(min_index)
        peaks = np.append(peaks[:min_index], peaks[min_index+1:]) if min_index < len(peaks) - 1 else peaks[:-1]
        left_ips = np.append(left_ips[:min_index], left_ips[min_index+1:]) if min_index < len(left_ips) - 1 else left_ips[:-1]
        right_ips = np.append(right_ips[:min_index],right_ips[min_index+1:]) if min_index < len(right_ips) - 1 else right_ips[:-1]
        
    #find reference data points
    values.append(np.sum(np.sum(np.sum(rotatedImg[(referenceDistance1-int(y_range/2)):(referenceDistance1+int(y_range/2)),crop_left:crop_right,:], axis=2), axis=1)))
    values.append(np.sum(np.sum(np.sum(rotatedImg[(referenceDistance2-int(y_range/2)):(referenceDistance2+int(y_range/2)),crop_left:crop_right,:], axis=2), axis=1)))

    
    #visualize the bounds of summation
    for i in range(len(peaks)):
        #use the FWHM bounds to find the box center
        peak = int((left_ips[i] + right_ips[i]) / 2)
        rotatedImg = cv2.rectangle(rotatedImg, (crop_left, peak + int(y_range/2)), (crop_right, peak - int(y_range/2)), (255, 100, 200), 10)
    
    #visualize reference points as well
    rotatedImg = cv2.rectangle(rotatedImg, (crop_left, referenceDistance1 + int(y_range/2)), (crop_right, referenceDistance1 - int(y_range/2)), (255, 100, 200), 10)
    rotatedImg = cv2.rectangle(rotatedImg, (crop_left, referenceDistance2 + int(y_range/2)), (crop_right, referenceDistance2 - int(y_range/2)), (255, 100, 200), 10)

    #Label boxes
    for i in range(len(peaks)):
        peak = int((left_ips[i] + right_ips[i]) / 2)
        label = 'Ctrl' if i == 0 else 'Test' if i == 1 else 'Err'
        rotatedImg = cv2.putText(rotatedImg, label, (crop_right, peak - int(y_range/2)), cv2.FONT_HERSHEY_SIMPLEX,
                       3, (255,100,200), 2, cv2.LINE_AA)
    rotatedImg = cv2.putText(rotatedImg, 'Ref 1', (crop_right, referenceDistance1 - int(y_range/2)), cv2.FONT_HERSHEY_SIMPLEX,
                       3, (255,100,200), 2, cv2.LINE_AA)
    rotatedImg = cv2.putText(rotatedImg, 'Ref 2', (crop_right, referenceDistance2 - int(y_range/2)), cv2.FONT_HERSHEY_SIMPLEX,
                       3, (255,100,200), 2, cv2.LINE_AA)
    
    return values, rotatedImg
    
def processImages(path, folder, imageList, drawLines, saveBounds, showBounds, graphPeaks):
    #Process images, and write each folder's data to a spreadsheet
    with open(path + folder + '.csv','w', newline='') as sheet:
        #Builds a directory for the processed images
        try:
            mkdir(path + 'Processed_' + folder)
            print('\tLoading...')
        except OSError:
            print('\tOverwriting...')
        savePath = path + 'Processed_' + folder + '/'
        writer = csv.writer(sheet, delimiter = ',')
        writer.writerow(['Image', 'Control strip', 'Test strip', 'Ref 1', 'Ref 2'])
        for image in imageList:
            boxSums, processedImage = getData(path + image, drawLines, graphPeaks)
            writer.writerow([str(image)] + boxSums)
            if saveBounds:
                if not cv2.imwrite(savePath + 'processed_' + image, processedImage):
                    print('Failed to save image...')
            if showBounds:
                cv2.imshow('processed_' + image, processedImage)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
        print('\tDone.' + '\n')
        
def processFolders(folderName, drawLines, saveBounds, showBounds, graphPeaks):
    found = False
    if (folderName == 'quit'):
        return
    if (folderName == 'help'):
        print('\tAlternatively, enter \'all\' to search all available directories. \n\tTo exit, enter \'quit\'.\n\tFor more documentation: https://github.com/sudo-quinnmaloney/LFAreader\n')
        found = True
    if (folderName == 'all'):
        for folder in listdir(getcwd()):
            if not isdir(folder):
                continue
            path = getcwd() + '/' + str(folder) + '/'
            imageList = [f for f in listdir(path) if isfile(join(path, f)) and splitext(f)[1] == '.jpg']
            if len(imageList)==0:
                continue
            print('\tFound folder: ' + folder)
            imageList = sorted(imageList)
            print('\t' + str(len(imageList)) + ' images imported...')
            processImages(path, folder, imageList, drawLines, saveBounds, showBounds, graphPeaks)
            found = True
                
    for folder in listdir(getcwd()):
        if folder == folderName and isdir(folder):
            found = True
            path = getcwd() + '/' + str(folder) + '/'
            imageList = [f for f in listdir(path) if isfile(join(path, f)) and splitext(f)[1] == '.jpg']
            if len(imageList)==0:
                print('\tNo jpg\'s in that folder.\n')
                break
            imageList = sorted(imageList)
            print('\t' + str(len(imageList)) + ' images imported...')
            processImages(path, folder, imageList, drawLines, saveBounds, showBounds, graphPeaks)
    if not found:
        print('\tFolder not found!\n')
    main()

def main():
    #processImages(folderName, drawLines, drawBounds, graphPeaks)
    processFolders(input('Enter the folder name, or \'help\': '), edges, saveBoxes, showBoxes, graphs)

if __name__ == '__main__':
    main()
