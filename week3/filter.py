import numpy as np

def gaussian_filter_freq(image: np.ndarray, D0: float, mode: str = "high") -> np.ndarray:
    f = np.fft.fft2(image)
    fshift = np.fft.fftshift(f)

    M, N = image.shape
    u = np.arange(M)
    v = np.arange(N)
    v_mesh, u_mesh = np.meshgrid(v, u)

    center_u, center_v = M / 2, N / 2
    D_uv = np.sqrt((u_mesh - center_u)**2 + (v_mesh - center_v)**2)

    if mode == "low":
        H = np.exp(-(D_uv**2) / (2 * (D0**2)))
    elif mode == "high":
        H = 1 - np.exp(-(D_uv**2) / (2 * (D0**2)))
    else:
        raise ValueError("mode phải là 'low' hoặc 'high'")

    G_shift = fshift * H
    G = np.fft.ifftshift(G_shift)
    image_back = np.fft.ifft2(G)

    return np.abs(image_back)

def gaussian_lowpass_filter(image, D0):
    return gaussian_filter_freq(image, D0, mode="low")

def gaussian_highpass_filter(image, D0):
    return gaussian_filter_freq(image, D0, mode="high")

def apply_filter_multipass(image, D0, passes):
    f = np.fft.fft2(image)
    fshift = np.fft.fftshift(f)

    M, N = image.shape
    u = np.arange(M)
    v = np.arange(N)
    v_mesh, u_mesh = np.meshgrid(v, u)

    center_u, center_v = M / 2, N / 2
    D_uv = np.sqrt((u_mesh - center_u)**2 + (v_mesh - center_v)**2)

    H = 1 - np.exp(-(D_uv**2) / (2 * (D0**2)))
    H_final = H ** passes

    G_shift = fshift * H_final

    G = np.fft.ifftshift(G_shift)
    image_back = np.fft.ifft2(G)

    return np.abs(image_back)


def normalize_for_display(img):
    img = img.astype(np.float32)
    img = img - img.min()
    max_val = img.max()
    if max_val > 0:
        img /= max_val
    return img
