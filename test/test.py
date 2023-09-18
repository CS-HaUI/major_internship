import cv2
import numpy as np

# Initialize the CUDA context
cv2.cuda.setDevice(0)  # Use the first GPU (change the index as needed)

# Create a VideoCapture object to capture video from a camera or file
cap = cv2.VideoCapture(0)  # Use the default camera (change as needed)

# Check if the camera or file is opened successfully
if not cap.isOpened():
    print("Error: Could not open video source.")
    exit()



while True:
    # Capture a frame from the video source
    ret, frame = cap.read()

    if not ret:
        print("Error: Could not read a frame.")
        break

    # Create GPU Mat object and upload the frame
    gpu_frame = cv2.cuda_GpuMat()
    gpu_frame.upload(frame)


    # Download the result frame from GPU to CPU
    result_frame = gpu_frame.download()

    # Display the result frame
    cv2.imshow('CUDA Gaussian Blur', result_frame)

    # Check for the 'q' key to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()

# Reset the CUDA device
cv2.cuda.resetDevice()
