import cv2

# Load the pre-trained Haar Cascade face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Read the image
image_path = "image.jpeg"  # Assuming image is in the current directory
img = cv2.imread(image_path)

# Convert image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect faces in the image
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

# Check if any faces were detected
if len(faces) == 0:
    print("No faces detected.")
else:
    # Redact faces
    for (x, y, w, h) in faces:
        # Option 1: Redact face by applying a black rectangle
        img[y:y+h, x:x+w] = (0, 0, 0)  # Black rectangle

        # Option 2: Redact face by applying Gaussian blur
        # img[y:y+h, x:x+w] = cv2.GaussianBlur(img[y:y+h, x:x+w], (99, 99), 30)

    # Save the result to output image
    cv2.imwrite("/mnt/output.jpg", img)

    print("Face detection complete! Result saved as 'output.jpg'.")