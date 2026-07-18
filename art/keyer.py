"""
Deer Colony — magenta chroma-key + sprite extractor (v2)
=========================================================
Removes the #D90FB8 magenta background from an AI-generated sprite sheet WITHOUT
leaving a coloured halo, and slices each sprite out as a clean RGBA PNG.

Why v2 beats naive keying:
  - Naive "distance from magenta + 1px erosion" trims the outer ring but leaves the
    surviving anti-aliased edge pixels colour-contaminated (part sprite + part magenta),
    which shows up as a purple/grey rim — worst on dark outlines against magenta.
  - v2 fixes this with three ideas:
      1. CONNECTIVITY: background = magenta that is reachable from the image border.
         Anything enclosed by the sprite (pink cheeks, purple flowers, banners) is
         therefore NEVER removed.
      2. UNMIX (decontaminate): for each anti-aliased edge pixel, estimate the magenta
         fraction p and solve for the true sprite colour  S = (P - p*M) / (1 - p).
         The rim takes the sprite's real colour instead of a purple blend.
      3. HOLES + HARD CUT: genuine see-through gaps (e.g. between watchtower legs) are
         very saturated magenta (p high) so a strength threshold clears them; a final
         hard cut zeroes any pixel still above flower-intensity magenta.

Key signal:  p = clip( min(R-G, B-G) / K , 0, 1 )   ("magenta-ness")
  - pure magenta bg  -> p ~ 1.0        (removed)
  - purple flower     -> p ~ 0.55       (kept: interior + below hard cut)
  - pink deer cheek   -> p ~ 0.0..0.1   (kept: B-G ~ 0 so min term is ~0)
  - warm browns/greens-> p ~ 0          (kept)

Tunables (defaults are what shipped the deer + core-building sheets):
  K=135, band_it=3, strong=0.82, hardcut=0.62

Usage (as a library):
    from keyer import keyer, order, tight
    rgb, alpha = keyer("sheet.png")              # full-sheet cleaned RGB + alpha
    objs, ids  = order(...)                       # detect + order blobs
    crop       = tight(rgb, alpha, ys, xs)        # one sprite, tight-cropped RGBA

Requires: numpy, scipy, pillow.
"""
import numpy as np
from PIL import Image
from scipy import ndimage


def keyer(src, K=135, band_it=3, strong=0.82, hardcut=0.62):
    """Return (rgb uint8 HxWx3, alpha uint8 HxW) for a whole sheet, magenta removed."""
    im = Image.open(src).convert('RGB')
    a = np.asarray(im).astype(np.float64)
    # sample the background colour from the four corners
    cor = np.concatenate([a[:10, :10].reshape(-1, 3), a[:10, -10:].reshape(-1, 3),
                          a[-10:, :10].reshape(-1, 3), a[-10:, -10:].reshape(-1, 3)])
    M = np.median(cor, 0)
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    p = np.clip(np.minimum(R - G, B - G) / K, 0, 1)          # magenta fraction
    # background = magenta reachable from the border  OR  very-strong magenta (holes)
    lbl, _ = ndimage.label(p > 0.45)
    border = set(np.unique(lbl[0, :])) | set(np.unique(lbl[-1, :])) \
        | set(np.unique(lbl[:, 0])) | set(np.unique(lbl[:, -1]))
    border.discard(0)
    bg = np.isin(lbl, list(border)) | (p > strong)
    band = ndimage.binary_dilation(bg, iterations=band_it) & ~bg   # AA rim just inside sprite
    alpha = np.ones(p.shape)
    alpha[bg] = 0
    alpha[band] = np.clip(1 - p[band], 0, 1)                 # feather the rim
    alpha[p > hardcut] = 0                                   # kill any residual magenta-ish pixel
    # unmix magenta out of the rim pixels
    S = a.copy()
    pb = p[band]
    denom = np.maximum(1 - pb, 1e-3)
    S[band] = np.clip((a[band] - pb[:, None] * M) / denom[:, None], 0, 255)
    return S.astype(np.uint8), (alpha * 255).astype(np.uint8)


def order(src, mag_fn, area_min, extra, key):
    """Detect blobs on a sheet and return (find_objects list, ordered label-id list).
    mag_fn(R,G,B)->bool mask of foreground; extra(ys,xs,h,w)->keep?; key=sort key on (id,ys,xs)."""
    a = np.asarray(Image.open(src).convert('RGB')).astype(int)
    lbl, n = ndimage.label(mag_fn(a[:, :, 0], a[:, :, 1], a[:, :, 2]))
    objs = ndimage.find_objects(lbl)
    rows = []
    for i, sl in enumerate(objs, 1):
        ys, xs = sl
        h, w = ys.stop - ys.start, xs.stop - xs.start
        area = int((lbl[sl] == i).sum())
        if area < area_min or not extra(ys, xs, h, w):
            continue
        rows.append((i, ys, xs))
    rows.sort(key=key)
    return objs, [r[0] for r in rows]


def tight(rgb, al, ys, xs, pad=4):
    """Crop one sprite tightly by its alpha, from cleaned full-sheet rgb+alpha."""
    y0 = max(0, ys.start - pad); y1 = min(al.shape[0], ys.stop + pad)
    x0 = max(0, xs.start - pad); x1 = min(al.shape[1], xs.stop + pad)
    ca = al[y0:y1, x0:x1]; cr = rgb[y0:y1, x0:x1]
    yy, xx = np.where(ca > 8)
    return np.dstack([cr[yy.min():yy.max() + 1, xx.min():xx.max() + 1],
                      ca[yy.min():yy.max() + 1, xx.min():xx.max() + 1]])


# ---- example detectors used for the shipped sheets ----
def deer_mag(R, G, B):
    m = (R > 150) & (G < 90) & (B > 120) & (R - G > 80) & (B - G > 60)
    return ndimage.binary_opening(~m, iterations=2)


def building_mag(R, G, B):
    f = ~((R > 150) & (G < 95) & (B > 120) & (R - G > 75) & (B - G > 55))
    return ndimage.binary_opening(ndimage.binary_closing(f, iterations=2), iterations=2)


# Verify a finished PNG is halo-free (should print 0):
def audit(path):
    a = np.asarray(Image.open(path).convert('RGBA')).astype(int)
    R, G, B, A = a[:, :, 0], a[:, :, 1], a[:, :, 2], a[:, :, 3]
    return int(((A > 30) & (np.minimum(R - G, B - G) > 85)).sum())
