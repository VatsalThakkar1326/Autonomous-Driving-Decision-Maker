import numpy as np
import cv2
from ultralytics import YOLO
from collections import defaultdict
import time

# Initialize the YOLO models on GPU
model1 = YOLO(r'C:\\Users\\14374\\Downloads\\best.pt').cuda()
model2 = YOLO('yolov8n-seg.pt').cuda()

cap = cv2.VideoCapture(0)

# Store the track history for model1
track_history1 = defaultdict(lambda: [])

# Open the text files for writing output
output_file1 = open("C:\\Users\\14374\\Downloads\\track1.txt", "a")
output_file2 = open("C:\\Users\\14374\\Downloads\\coordinates_output.txt", "w")
output_file_trap1 = open("C:\\Users\\14374\\Downloads\\trap1.txt", "a")  # File for trapezoid 1
output_file_trap2 = open("C:\\Users\\14374\\Downloads\\trap2.txt", "a")  # File for trapezoid 2
output_file_trap3 = open("C:\\Users\\14374\\Downloads\\trap3.txt", "a")  # File for trapezoid 3

# Function to process frame for model1
def process_frame_model1(frame):
    results = model1.track(frame, persist=True)
    if results is not None and results[0].boxes is not None and results[0].boxes.id is not None:
        boxes = results[0].boxes.xywh.cpu()
        track_ids = results[0].boxes.id.int().cpu().tolist()
        classes = results[0].boxes.cls.int().cpu().tolist()
        for box, track_id, cls in zip(boxes, track_ids, classes):
            x, y, w, h = box
            factor2 = 25
            bottom_left = (int(x - w / 2) + factor2, (int(y - h / 2)))
            top_right = (int(x + w / 2), (int(y + h / 2)))
            top_left = (int(x - w / 2), (int(y + h / 2)))  # Adding bottom left coordinate
            bottom_right = (int(x + w / 2) - factor2, (int(y - h / 2)))  # Adding top right coordinate
            track = track_history1[track_id]
            track.append((top_left, bottom_right))  # Appending only top left and bottom right for consistency with visualization
            if len(track) > 30:
                track.pop(0)
            class_name = results[0].names[cls]
            output_file1.write(f'Track ID {track_id} coordinates for {class_name}: {top_left}, {bottom_left}, {bottom_right}, {top_right}\n')
            output_file1.flush()

            # Calculate the coordinates of the trapezoids
            #**change code from here**

            factor1 = 45
            hfactor1 = 25
            hfactor2 = 50
            hfactor3 = 75

            bottom_left1 = bottom_left
            top_right1 = (int(x + w / 2) - factor1, (int(y - h / 2) - hfactor1))
            top_left1 = (int(x - w / 2) + factor1, (int((y - h / 2) - hfactor1)) ) # Adding bottom left coordinate
            bottom_right1 = bottom_right  # Adding top right coordinate
            output_file_trap1.write(f'Track ID {track_id} coordinates for {class_name}: {top_left1}, {bottom_left1}, {bottom_right1}, {top_right1}\n')
            output_file_trap1.flush()

            bottom_left2 = (int(x - w / 2), (int(y - h / 2) - hfactor1))
            top_right2 = (int(x + w / 2) - factor1, (int(y - h / 2) - hfactor2))
            top_left2 = (int(x - w / 2) + factor1, (int(y - h / 2) - hfactor2))  # Adding bottom left coordinate
            bottom_right2 = (int(x + w / 2), (int(y - h / 2) - hfactor1))  # Adding top right coordinate

            output_file_trap2.write(f'Track ID {track_id} coordinates for {class_name}: {top_left2}, {bottom_left2}, {bottom_right2}, {top_right2}\n')
            output_file_trap2.flush()

            bottom_left3 = (int(x - w / 2), (int(y - h / 2) - hfactor2))
            top_right3 = (int(x + w / 2) - factor1, (int(y - h / 2) - hfactor3))
            top_left3 = (int(x - w / 2) + factor1, (int(y - h / 2) - hfactor3)) # Adding bottom left coordinate
            bottom_right3 = (int(x + w / 2), (int(y - h / 2) - hfactor2))  # Adding top right coordinate

            output_file_trap3.write(f'Track ID {track_id} coordinates for {class_name}: {top_left3}, {bottom_left3}, {bottom_right3}, {top_right3}\n')
            output_file_trap3.flush()

            cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)
            cv2.putText(frame, f'Track ID: {track_id}', (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.imshow('Frame', frame)


# Function to process frame for model2
def process_frame_model2(frame):
    results = model2.track(frame, persist=True)
    if results is not None and results[0].masks is not None:
        masks = results[0].masks
        segments_as_strings = [np.array2string(np.array(segment)) for segment in masks.xy]
        array_as_string = ''.join(segments_as_strings)
        array_as_string = array_as_string.replace('\n', '').replace('[', '').replace(']', '').replace(',', '')
        coordinates_list = array_as_string.split()
        
        # Filter out non-numeric values and ensure pairs of coordinates
        coordinates_list = [coord for coord in coordinates_list if coord.replace('.', '', 1).isdigit()]
        coordinates_list = [[float(coordinates_list[i]), float(coordinates_list[i+1])] for i in range(0, len(coordinates_list), 2) if i + 1 < len(coordinates_list)]

        # Visualize the results on the frame
        annotated_frame = results[0].plot()
        cv2.imshow("YOLOv8 Inference", annotated_frame)

        return coordinates_list


# Initialize the start time for
# Initialize the start time for model2 and model1
start_time_model2 = time.time()
start_time_model1 = time.time()  # Add this line to initialize start_time_model1

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Process the frame for model1
    process_frame_model1(frame)
    
    # Process the frame for model2
    coordinates_list = process_frame_model2(frame)

    # If coordinates_list is not None, write coordinates to the text file for model2
    if coordinates_list is not None and len(coordinates_list) > 0:
        # Check if 5 minutes have passed since the last overwrite
        if time.time() - start_time_model2 >= 300:  # 300 seconds = 5 minutes
            # Close the current file and open a new one for writing
            output_file2.close()
            output_file2 = open("C:\\Users\\14374\\Downloads\\coordinates_output.txt", "w")
            # Reset the start time
            start_time_model2 = time.time()

        output_file2.write("Coordinates: [")
        for i, coordinates in enumerate(coordinates_list):
            if i > 0:
                output_file2.write(", ")
            output_file2.write(f"({int(coordinates[0])}, {int(coordinates[1])})")
        output_file2.write("]")
        output_file2.write("\n")
        output_file2.flush()  # Flush the file buffer

    # Delete the content in txt file after 10 minutes for model1
    if time.time() - start_time_model1 > 50:  # 600 seconds = 10 minutes
        output_file1.close()  # Close the file before clearing
        open("C:\\Users\\14374\\Downloads\\track1.txt", "w").close()
        output_file1 = open("C:\\Users\\14374\\Downloads\\track1.txt", "a")  # Reopen the file for appending

        output_file_trap1.close()
        open("C:\\Users\\14374\\Downloads\\trap1.txt", "a").close()
        output_file_trap1 = open("C:\\Users\\14374\\Downloads\\trap1.txt", "a")

        output_file_trap2.close()
        open("C:\\Users\\14374\\Downloads\\trap2.txt", "a").close()
        output_file_trap2 = open("C:\\Users\\14374\\Downloads\\trap2.txt", "a")
        
        output_file_trap3.close()
        open("C:\\Users\\14374\\Downloads\\trap3.txt", "a").close()
        output_file_trap3 = open("C:\\Users\\14374\\Downloads\\trap3.txt", "a")
        
        start_time_model1 = time.time()
            
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# Release the video capture and close the text files
cap.release()
output_file1.close()
output_file2.close()
cv2.destroyAllWindows()
