def get_crop_box(
    img_size: tuple[int, int], target_aspect: float = 1.5
) -> tuple[int, int, int, int]:
    """Return crop box to achieve a target aspect ratio"""

    w, h = img_size
    aspect = w / h

    if aspect > target_aspect:
        # photo is too wide, remove from the L/R to make photo narrower, but keep height the same
        new_width = h * target_aspect
        diff_w = w - new_width
        each_side = diff_w / 2
        box = (each_side, 0, w - each_side, h)

    elif aspect < target_aspect:
        # photo is too narrow, remove from the T/B, but keep width the same
        new_height = w / target_aspect
        diff_h = h - new_height
        each_side = diff_h / 2
        box = (0, each_side, w, h - each_side)
    else:
        box = (0, 0, w, h)

    return box
