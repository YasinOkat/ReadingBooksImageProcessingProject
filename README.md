# Reading Books, Image Processing Project

This is a Python application designed to assist visually impaired individuals in reading books. It utilizes computer vision techniques and optical character recognition (OCR) to capture frames from a video source, process the captured images, and extract text from the images. The extracted text is then converted into an audio format for easy listening.

## Features

- Capture frames from a video source (e.g., webcam, IP camera) and display the resized and rotated frames.
- Allow the user to capture a frame by pressing a key and save it as an image file.
- Process the captured image to enhance text visibility.
- Perform OCR on the processed image to extract the text.
- Convert the extracted text into an audio file using text-to-speech technology.
- Play the audio file automatically for the visually impaired user.

## Requirements

- Python 3.x
- OpenCV (cv2)
- NumPy
- pytesseract
- Tesseract OCR
- gTTS (Google Text-to-Speech)
