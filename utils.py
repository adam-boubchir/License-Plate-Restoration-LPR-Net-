import numpy as np
import cv2


# =========================
# PSF (motion blur)
# =========================
def motion_blur_psf(length, angle):
    psf = np.zeros((length, length))
    center = length // 2

    for i in range(length):
        x = int(center + (i - center) * np.cos(angle))
        y = int(center + (i - center) * np.sin(angle))

        if 0 <= x < length and 0 <= y < length:
            psf[y, x] = 1

    psf /= psf.sum()
    return psf


# =========================
# Apply blur
# =========================
def apply_motion_blur(image, psf):
    return cv2.filter2D(image, -1, psf)


# =========================
# FFT
# =========================
def compute_fft(image):
    f = np.fft.fft2(image)
    fshift = np.fft.fftshift(f)
    magnitude = np.log(np.abs(fshift) + 1)
    return magnitude


# =========================
# Estimate angle (AMÉLIORÉ)
# =========================
def estimate_angle(spectrum):
    spec_norm = cv2.normalize(spectrum, None, 0, 255, cv2.NORM_MINMAX)
    spec_uint8 = np.uint8(spec_norm)

    edges = cv2.Canny(spec_uint8, 50, 150)

    lines = cv2.HoughLines(edges, 1, np.pi/180, 120)

    if lines is None:
        return 0

    angles = []

    for rho, theta in lines[:, 0]:
        angles.append(theta)

    # médiane = robuste
    angle = np.median(angles)

    # correction (important)
    angle = angle - np.pi/2

    return angle


# =========================
# Wiener filter (CORRIGÉ)
# =========================
def wiener_filter(img, psf, K=0.05):
    img_fft = np.fft.fft2(img)

    H, W = img.shape
    h, w = psf.shape

    psf_padded = np.zeros((H, W))

    # 🔥 placement centré SANS erreur
    y = (H - h) // 2
    x = (W - w) // 2

    psf_padded[y:y+h, x:x+w] = psf

    # shift obligatoire
    psf_fft = np.fft.fft2(np.fft.ifftshift(psf_padded))

    psf_fft_conj = np.conj(psf_fft)

    result_fft = psf_fft_conj / (np.abs(psf_fft)**2 + K) * img_fft
    result = np.fft.ifft2(result_fft)

    result = np.abs(result)
    result = cv2.normalize(result, None, 0, 255, cv2.NORM_MINMAX)

    return result
# =========================
# PSNR
# =========================
def psnr(original, restored):
    mse = np.mean((original - restored) ** 2)

    if mse == 0:
        return 100

    return 10 * np.log10(255**2 / mse)