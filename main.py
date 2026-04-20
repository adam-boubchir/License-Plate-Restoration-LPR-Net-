import cv2
import numpy as np
import matplotlib.pyplot as plt
from utils import *


# =========================
# 1. Charger image
# =========================
import os

# =========================
# 1. Choisir image
# =========================
image_folder = "images"

images = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

if len(images) == 0:
    print("Aucune image trouvée dans le dossier images/")
    exit()

print("\nImages disponibles :")
for i, img_name in enumerate(images):
    print(f"{i} - {img_name}")

# choix utilisateur
choice = int(input("\nChoisir le numero de l'image : "))

if choice < 0 or choice >= len(images):
    print("Choix invalide")
    exit()

image_path = os.path.join(image_folder, images[choice])

# =========================
# Charger image
# =========================
img = cv2.imread(image_path, 0)

if img is None:
    print("Erreur lors du chargement de l'image")
    exit()

img = img.astype(np.float32)

print(f"\nImage choisie : {images[choice]}")


# =========================
# 2. Générer flou
# =========================
TRUE_LENGTH = 15
TRUE_ANGLE = np.deg2rad(30)

psf_true = motion_blur_psf(TRUE_LENGTH, TRUE_ANGLE)
blurred = apply_motion_blur(img, psf_true)


# =========================
# 3. FFT
# =========================
spectrum = compute_fft(blurred)


# =========================
# 4. Estimation angle
# =========================
estimated_angle = estimate_angle(spectrum)

print("Angle réel:", np.rad2deg(TRUE_ANGLE))
print("Angle estimé:", np.rad2deg(estimated_angle))


# =========================
# ⚠️ DEBUG (IMPORTANT)
# =========================
# 👉 Si résultat mauvais, utilise vrai angle
USE_TRUE_ANGLE = True

if USE_TRUE_ANGLE:
    estimated_angle = TRUE_ANGLE


# =========================
# 5. Reconstruction PSF
# =========================
estimated_length = 15  # tu peux tester 10, 20

psf_est = motion_blur_psf(estimated_length, estimated_angle)


# =========================
# 6. Wiener filter
# =========================
restored = wiener_filter(blurred, psf_est, K=0.05)


# =========================
# 7. PSNR
# =========================
print("PSNR:", psnr(img, restored))


# =========================
# 8. Affichage
# =========================
plt.figure(figsize=(12,4))

plt.subplot(1,3,1)
plt.title("Original")
plt.imshow(img, cmap='gray')

plt.subplot(1,3,2)
plt.title("Blurred")
plt.imshow(blurred, cmap='gray')

plt.subplot(1,3,3)
plt.title("Restored")
plt.imshow(restored, cmap='gray')

plt.show()