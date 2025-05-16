#!/usr/bin/env python
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Función para mostrar múltiples imágenes
def show_images(images, titles, cmap='gray'):
    plt.figure(figsize=(12, 8))
    for i, (img, title) in enumerate(zip(images, titles)):
        plt.subplot(2, 3, i+1)
        plt.imshow(img, cmap=cmap)
        plt.title(title)
        plt.axis('off')
    plt.tight_layout()
    plt.show()

# Cargar imagen en escala de grises
image = cv2.imread('lena.png', cv2.IMREAD_GRAYSCALE)

#Filtros paso bajas
#Filtro Promedio (Blur)
kernelSizeLow = (21,21)
blurred_image = cv2.blur(image, kernelSizeLow)
#Filtro Gaussiano
gaussian_blur = cv2.GaussianBlur(image, kernelSizeLow, 0)

#Filtros paso altas (detección de bordes)
kernelSizeHigh = 3
#Filtro Sobel
sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=kernelSizeHigh)  # Derivada en x
sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=kernelSizeHigh)  # Derivada en y
sobel_combined = cv2.magnitude(sobel_x, sobel_y)  # Magnitud del gradiente
#Laplaciano
laplacian = cv2.Laplacian(image, cv2.CV_64F)
#Canny
edges_canny = cv2.Canny(image, 100, 200)

#Filtros morfológicos
kernelSizeMorph = (10, 10)
kernel = np.ones(kernelSizeMorph,np.uint8)
erosion = cv2.erode(image, kernel, iterations = 1)
dilation = cv2.dilate(image, kernel, iterations = 1)
#Fourier
hist = cv2.calcHist([image], [0], None, [256], [0, 256])
equalized_image = cv2.equalizeHist(image)

# Realzar sumando el Laplaciano (sharpening)
sharpened = cv2.addWeighted(image.astype(np.float64), 1.0, laplacian, 1.0, 0)
sharpened = np.clip(sharpened, 0, 255).astype(np.uint8)

# Mostrar todas las imágenes
images = [image, blurred_image, gaussian_blur, sobel_combined, laplacian, edges_canny]
titles = ['Original', 'Blur (Promedio)', 'Gaussian Blur', 'Sobel (Bordes)', 'Laplacian', 'Canny (Bordes)']
show_images(images, titles)


# Mostrar todas las imágenes
images = [image, erosion, dilation, equalized_image, sharpened]
titles = ['Original', 'Erosión', 'Dilatación', 'Imagen ecualizada', "Imagen realzada"]
show_images(images, titles)
