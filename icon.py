import math
from PIL import Image, ImageDraw, ImageFont

def create_pro_icon(output_path="icon.ico"):
    size = 512
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 1. Base Dark Slate con angoli arrotondati e bordo neon Cyan
    pad = 24
    radius = 110
    draw.rounded_rectangle(
        [pad, pad, size - pad, size - pad],
        radius=radius,
        fill="#0b0f19",
        outline="#38bdf8",
        width=16
    )
    
    # Bordo interno scuro di profondità
    draw.rounded_rectangle(
        [pad + 12, pad + 12, size - pad - 12, size - pad - 12],
        radius=radius - 10,
        outline="#1e293b",
        width=6
    )

    # 2. Cubo inclinato centrale (Roblox Style)
    center_x, center_y = size // 2 - 10, size // 2 - 20
    cube_size = 130
    tilt_angle = math.radians(-15)

    def transform_point(x, y):
        rx = x * math.cos(tilt_angle) - y * math.sin(tilt_angle)
        ry = x * math.sin(tilt_angle) + y * math.cos(tilt_angle)
        return (center_x + rx, center_y + ry)

    outer_pts = [
        transform_point(-cube_size, -cube_size),
        transform_point(cube_size, -cube_size),
        transform_point(cube_size, cube_size),
        transform_point(-cube_size, cube_size)
    ]

    hole_size = 50
    inner_pts = [
        transform_point(-hole_size, -hole_size),
        transform_point(hole_size, -hole_size),
        transform_point(hole_size, hole_size),
        transform_point(-hole_size, hole_size)
    ]

    # Corpo del cubo
    draw.polygon(outer_pts, fill="#1e293b")
    for i in range(4):
        p1 = outer_pts[i]
        p2 = outer_pts[(i + 1) % 4]
        draw.line([p1, p2], fill="#0284c7", width=14)

    # Foro interno centrale
    draw.polygon(inner_pts, fill="#0b0f19")
    for i in range(4):
        p1 = inner_pts[i]
        p2 = inner_pts[(i + 1) % 4]
        draw.line([p1, p2], fill="#0369a1", width=8)

    # 3. Nucleo verde neon
    core_r = 20
    draw.ellipse(
        [center_x - core_r, center_y - core_r, center_x + core_r, center_y + core_r],
        fill="#22c55e",
        outline="#4ade80",
        width=4
    )

    # 4. Badge "PRO" Dorato
    badge_x1, badge_y1 = 280, 360
    badge_x2, badge_y2 = 470, 440
    badge_radius = 20

    draw.rounded_rectangle(
        [badge_x1 + 4, badge_y1 + 4, badge_x2 + 4, badge_y2 + 4],
        radius=badge_radius,
        fill="#05070c"
    )

    draw.rounded_rectangle(
        [badge_x1, badge_y1, badge_x2, badge_y2],
        radius=badge_radius,
        fill="#f59e0b",
        outline="#fbbf24",
        width=5
    )

    try:
        font = ImageFont.truetype("arialbd.ttf", 46)
    except Exception:
        font = ImageFont.load_default()

    text = "PRO"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    
    text_x = badge_x1 + ((badge_x2 - badge_x1) - text_w) // 2
    text_y = badge_y1 + ((badge_y2 - badge_y1) - text_h) // 2 - 4

    draw.text((text_x, text_y), text, fill="#0f172a", font=font)

    # 5. Generazione di tutti i livelli di risoluzione reali
    target_sizes = [256, 128, 64, 48, 32, 16]
    resized_layers = [img.resize((s, s), Image.Resampling.LANCZOS) for s in target_sizes]

    # Salvataggio con layer principale a 256x256 e tutti i sottomultipli inclusi
    resized_layers[0].save(
        output_path,
        format="ICO",
        append_images=resized_layers[1:]
    )
    print(f"[OK] Icona salvata con layer 256x256, 128x128, 64x64, 48x48, 32x32, 16x16 in: {output_path}")

if __name__ == "__main__":
    create_pro_icon("icon.ico")
