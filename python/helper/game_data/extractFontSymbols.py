from PIL import Image
import numpy as np
from pathlib import Path
from config import INPUT_PATH, OUTPUT_PATH
# =========================
# CONFIG (edit only here)
# =========================

INPUT_TGA_GAMEFONT = Path(INPUT_PATH / "Assets/res/Fonts/GameFont.tga")
OUTPUT_DIR_GAMEFONT = Path(OUTPUT_PATH / "Assets/Symbols/font")
GAME_FONT_ROW_BLOCKS = [
    {"count": 4, "height": 17, "spacing": 1},
    {"count": 4, "height": 20, "spacing": 1},
    {"count": 4, "height": 20, "spacing": 1},
    {"count": 2, "height": 20, "spacing": 1},
]

INPUT_TGA_GAMEFONT_75 = Path(INPUT_PATH / "Assets/res/Fonts/GameFont_75.tga")
OUTPUT_DIR_GAMEFONT_75 = Path(OUTPUT_PATH / "Assets/Symbols/font_75")
GAME_FONT_75_ROW_BLOCKS = [
    {"count": 4, "height": 13, "spacing": 1},
    {"count": 11, "height": 16, "spacing": 1},
]

ALPHA_THRESHOLD = 0  # alpha > 0 = foreground pixel


def extract_glyphs_from_tga(input_tga, output_dir, row_blocks, alpha_treshold):
        
    # =========================
    # SETUP
    # =========================

    Path(output_dir).mkdir(exist_ok=True)

    img = Image.open(input_tga).convert("RGBA")
    arr = np.array(img)

    mask = arr[:, :, 3] > alpha_treshold
    h, w = mask.shape

    glyphs = []

    # =========================
    # BUILD ROW REGIONS
    # =========================

    y = 0
    row_id = 0

    for block in row_blocks:
        for _ in range(block["count"]):
            row_h = block["height"]

            y0 = y
            y1 = y + row_h

            if y1 > h:
                raise ValueError("Row definition exceeds image height")

            row_mask = mask[y0:y1, :]

            # =========================
            # HORIZONTAL SPLITTING
            # =========================

            col_has_pixels = row_mask.any(axis=0)

            in_glyph = False
            start_x = 0
            glyph_id_in_row = 0

            for x in range(w):
                if col_has_pixels[x] and not in_glyph:
                    in_glyph = True
                    start_x = x

                elif not col_has_pixels[x] and in_glyph:
                    in_glyph = False
                    end_x = x

                    glyph = arr[y0:y1, start_x:end_x]

                    # skip accidental empty slices
                    if glyph[:, :, 3].sum() == 0:
                        continue
                    # rows and glyphs start with 1 for better readability
                    out_name = f"glyph_r{row_id:02d}_{glyph_id_in_row:02d}.png"
                    Image.fromarray(glyph).save(Path(output_dir) / out_name)

                    glyphs.append({
                        "row": row_id,
                        "x": int(start_x),
                        "y": int(y0),
                        "width": int(end_x - start_x),
                        "height": int(row_h),
                        "file": out_name
                    })

                    glyph_id_in_row += 1

            # handle glyph reaching end of row
            if in_glyph:
                end_x = w
                glyph = arr[y0:y1, start_x:end_x]

                if glyph[:, :, 3].sum() > 0:
                    # rows and glyphs start with 1 for better readability
                    out_name = f"glyph_r{row_id:02d}_{glyph_id_in_row:02d}.png"
                    out_file_path = Path(output_dir).realtive_to(OUTPUT_PATH) / out_name
                    Image.fromarray(glyph).save(Path(output_dir) / out_name)

                    glyphs.append({
                        "row": row_id,
                        "x": int(start_x),
                        "y": int(y0),
                        "width": int(end_x - start_x),
                        "height": int(row_h),
                        "file": out_name
                    })

            row_id += 1
            y += row_h + block["spacing"]

    print(f"Extracted {len(glyphs)} glyphs")
    return glyphs

