"""
Generate branded receipt images for the calculator results.

If a custom template exists in assets/templates/, it is used as background.
Otherwise a gradient background is generated programmatically.
"""

import io
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ASSETS = Path(__file__).resolve().parent.parent / "assets"
TEMPLATES = ASSETS / "templates"

WIDTH, HEIGHT = 1080, 1920  # Instagram story dimensions

_FONT_CACHE: dict[tuple[str, int], ImageFont.FreeTypeFont] = {}


def _get_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    key = ("bold" if bold else "regular", size)
    if key not in _FONT_CACHE:
        if bold:
            candidates = ["arialbd", "Arial Bold", "arial"]
        else:
            candidates = ["arial", "Arial"]
        font = None
        for name in candidates:
            try:
                font = ImageFont.truetype(name, size)
                break
            except OSError:
                continue
        if font is None:
            font = ImageFont.load_default(size=size)
        _FONT_CACHE[key] = font
    return _FONT_CACHE[key]


def _make_gradient(width: int, height: int, top_color: tuple, bot_color: tuple) -> Image.Image:
    img = Image.new("RGB", (width, height))
    for y in range(height):
        ratio = y / height
        r = int(top_color[0] + (bot_color[0] - top_color[0]) * ratio)
        g = int(top_color[1] + (bot_color[1] - top_color[1]) * ratio)
        b = int(top_color[2] + (bot_color[2] - top_color[2]) * ratio)
        for x in range(width):
            img.putpixel((x, y), (r, g, b))
    return img


def _load_or_create_bg(template_name: str, top_color: tuple, bot_color: tuple) -> Image.Image:
    path = TEMPLATES / template_name
    if path.exists():
        return Image.open(path).resize((WIDTH, HEIGHT)).convert("RGB")
    return _make_gradient(WIDTH, HEIGHT, top_color, bot_color)


def _draw_rounded_rect(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int, int, int],
    radius: int,
    fill: tuple,
) -> None:
    x1, y1, x2, y2 = xy
    draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
    draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
    draw.pieslice([x1, y1, x1 + 2 * radius, y1 + 2 * radius], 180, 270, fill=fill)
    draw.pieslice([x2 - 2 * radius, y1, x2, y1 + 2 * radius], 270, 360, fill=fill)
    draw.pieslice([x1, y2 - 2 * radius, x1 + 2 * radius, y2], 90, 180, fill=fill)
    draw.pieslice([x2 - 2 * radius, y2 - 2 * radius, x2, y2], 0, 90, fill=fill)


def generate_tourist_receipt(
    months: int,
    total_paid: int,
    total_points: int,
    lang: str = "ru",
) -> bytes:
    """Generate a story-sized image for the tourist calculator result."""
    img = _load_or_create_bg("tourist_bg.png", (0, 102, 204), (0, 51, 102))
    draw = ImageDraw.Draw(img)

    _draw_rounded_rect(draw, (60, 200, WIDTH - 60, HEIGHT - 200), 40, (0, 0, 0, 0))
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)
    _draw_rounded_rect(ov_draw, (60, 200, WIDTH - 60, HEIGHT - 200), 40, (255, 255, 255, 40))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Header
    font_title = _get_font(72, bold=True)
    draw.text((WIDTH // 2, 300), "InLeader", font=font_title, fill="white", anchor="mt")

    font_sub = _get_font(42)
    emoji_ship = "\U0001F6A2"
    subtitle = {"ru": f"{emoji_ship} Калькулятор Туриста", "en": f"{emoji_ship} Tourist Calculator"}.get(lang, f"{emoji_ship} Tourist Calculator")
    draw.text((WIDTH // 2, 400), subtitle, font=font_sub, fill=(200, 230, 255), anchor="mt")

    # Divider
    draw.line([(120, 480), (WIDTH - 120, 480)], fill=(255, 255, 255, 128), width=2)

    # Stats
    font_label = _get_font(38)
    font_value = _get_font(80, bold=True)
    font_unit = _get_font(34)

    y = 540
    label_months = {"ru": "Месяцев накопления", "en": "Months of saving"}.get(lang, "Months")
    draw.text((WIDTH // 2, y), label_months, font=font_label, fill=(180, 210, 255), anchor="mt")
    draw.text((WIDTH // 2, y + 55), str(months), font=font_value, fill="white", anchor="mt")

    y = 730
    label_invested = {"ru": "Вложено", "en": "Invested"}.get(lang, "Invested")
    draw.text((WIDTH // 2, y), label_invested, font=font_label, fill=(180, 210, 255), anchor="mt")
    draw.text((WIDTH // 2, y + 55), f"${total_paid:,}", font=font_value, fill="white", anchor="mt")

    y = 920
    label_points = {"ru": "Reward Points", "en": "Reward Points"}.get(lang, "Reward Points")
    draw.text((WIDTH // 2, y), label_points, font=font_label, fill=(180, 210, 255), anchor="mt")
    draw.text((WIDTH // 2, y + 55), f"{total_points:,}", font=font_value, fill=(255, 215, 0), anchor="mt")

    # Discount highlight
    y = 1140
    _draw_rounded_rect(draw, (120, y, WIDTH - 120, y + 160), 30, (255, 255, 255, 30))
    overlay2 = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    ov2_draw = ImageDraw.Draw(overlay2)
    _draw_rounded_rect(ov2_draw, (120, y, WIDTH - 120, y + 160), 30, (255, 255, 255, 35))
    img = Image.alpha_composite(img.convert("RGBA"), overlay2).convert("RGB")
    draw = ImageDraw.Draw(img)

    font_highlight = _get_font(36)
    tip = {"ru": "Баллы = скидка при бронировании круиза!", "en": "Points = discount when booking a cruise!"}.get(lang, "Points = cruise booking discount!")
    draw.text((WIDTH // 2, y + 50), f"\U0001F4A1 {tip}", font=font_highlight, fill=(255, 255, 200), anchor="mt")
    draw.text((WIDTH // 2, y + 105), f"{total_points:,} RP \u2248 ${total_points // 2:,}+", font=_get_font(44, bold=True), fill=(255, 215, 0), anchor="mt")

    # Footer
    draw.text((WIDTH // 2, HEIGHT - 320), "InLeader", font=_get_font(36, bold=True), fill=(255, 255, 255), anchor="mt")
    draw.text((WIDTH // 2, HEIGHT - 270), "@InLeader_bot", font=_get_font(30), fill=(120, 150, 200), anchor="mt")

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def generate_partner_receipt(
    vips: int,
    members: int,
    vip_total: int,
    member_total: int,
    grand_total: int,
    lang: str = "ru",
) -> bytes:
    """Generate a story-sized image for the partner calculator result."""
    img = _load_or_create_bg("partner_bg.png", (20, 20, 60), (10, 60, 40))
    draw = ImageDraw.Draw(img)

    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)
    _draw_rounded_rect(ov_draw, (60, 200, WIDTH - 60, HEIGHT - 200), 40, (255, 255, 255, 30))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Header
    font_title = _get_font(72, bold=True)
    draw.text((WIDTH // 2, 300), "InLeader", font=font_title, fill="white", anchor="mt")

    font_sub = _get_font(42)
    subtitle = {"ru": "\U0001F4BC Калькулятор Партнёра", "en": "\U0001F4BC Partner Calculator"}.get(lang, "\U0001F4BC Partner Calculator")
    draw.text((WIDTH // 2, 400), subtitle, font=font_sub, fill=(180, 255, 200), anchor="mt")

    draw.line([(120, 480), (WIDTH - 120, 480)], fill=(255, 255, 255, 128), width=2)

    font_label = _get_font(38)
    font_value = _get_font(64, bold=True)

    y = 540
    label_vip = {"ru": "VIP-партнёры", "en": "VIP Partners"}.get(lang, "VIP Partners")
    draw.text((WIDTH // 2, y), f"\U0001F539 {label_vip}: {vips}", font=font_label, fill=(180, 220, 255), anchor="mt")
    draw.text((WIDTH // 2, y + 60), f"${vip_total:,}", font=font_value, fill="white", anchor="mt")

    y = 720
    label_members = {"ru": "Члены клуба", "en": "Club Members"}.get(lang, "Club Members")
    draw.text((WIDTH // 2, y), f"\U0001F538 {label_members}: {members}", font=font_label, fill=(180, 220, 255), anchor="mt")
    draw.text((WIDTH // 2, y + 60), f"${member_total:,}", font=font_value, fill="white", anchor="mt")

    # Grand total highlight
    y = 940
    _draw_rounded_rect(draw, (100, y, WIDTH - 100, y + 220), 35, (0, 0, 0, 50))
    overlay2 = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    ov2_draw = ImageDraw.Draw(overlay2)
    _draw_rounded_rect(ov2_draw, (100, y, WIDTH - 100, y + 220), 35, (46, 204, 113, 60))
    img = Image.alpha_composite(img.convert("RGBA"), overlay2).convert("RGB")
    draw = ImageDraw.Draw(img)

    label_total = {"ru": "ИТОГО ЗАРАБОТОК", "en": "TOTAL EARNINGS"}.get(lang, "TOTAL EARNINGS")
    draw.text((WIDTH // 2, y + 40), f"\U0001F4B0 {label_total}", font=_get_font(40), fill=(200, 255, 200), anchor="mt")
    draw.text((WIDTH // 2, y + 110), f"${grand_total:,}", font=_get_font(96, bold=True), fill=(255, 215, 0), anchor="mt")

    # Tip
    y = 1220
    tip = {"ru": "Это мгновенный бонус! Лидерские бонусы — дополнительно.", "en": "Instant bonus! Leadership bonuses are extra."}.get(lang, "Instant bonus! Leadership bonuses are extra.")
    draw.text((WIDTH // 2, y), f"\U0001F680 {tip}", font=_get_font(30), fill=(180, 220, 180), anchor="mt")

    # Footer
    draw.text((WIDTH // 2, HEIGHT - 320), "InLeader", font=_get_font(36, bold=True), fill=(255, 255, 255), anchor="mt")
    draw.text((WIDTH // 2, HEIGHT - 270), "@InLeader_bot", font=_get_font(30), fill=(120, 170, 140), anchor="mt")

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def generate_cruise_receipt(
    price: float,
    rp_used: int,
    cash: float,
    savings: float,
    lang: str = "ru",
) -> bytes:
    """Generate a story-sized image for the cruise calculator result."""
    img = _load_or_create_bg("cruise_bg.png", (0, 51, 102), (0, 102, 204))
    draw = ImageDraw.Draw(img)

    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)
    _draw_rounded_rect(ov_draw, (60, 200, WIDTH - 60, HEIGHT - 200), 40, (255, 255, 255, 30))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Header
    font_title = _get_font(72, bold=True)
    draw.text((WIDTH // 2, 300), "InLeader", font=font_title, fill="white", anchor="mt")

    font_sub = _get_font(42)
    subtitle = {"ru": "\U0001F6A2 Расчёт Круиза RP", "en": "\U0001F6A2 Cruise RP Calculation"}.get(lang, "\U0001F6A2 Cruise Calculation")
    draw.text((WIDTH // 2, 400), subtitle, font=font_sub, fill=(200, 230, 255), anchor="mt")

    draw.line([(120, 480), (WIDTH - 120, 480)], fill=(255, 255, 255, 128), width=2)

    font_label = _get_font(38)
    font_value = _get_font(64, bold=True)

    y = 540
    label_price = {"ru": "Цена круиза", "en": "Cruise Price"}.get(lang, "Price")
    draw.text((WIDTH // 2, y), label_price, font=font_label, fill=(180, 210, 255), anchor="mt")
    draw.text((WIDTH // 2, y + 60), f"${price:,.2f}", font=font_value, fill="white", anchor="mt")

    y = 720
    label_rp = {"ru": "Использовано RP", "en": "RP Used"}.get(lang, "RP Used")
    draw.text((WIDTH // 2, y), label_rp, font=font_label, fill=(180, 210, 255), anchor="mt")
    draw.text((WIDTH // 2, y + 60), f"{rp_used:,} RP", font=font_value, fill=(255, 215, 0), anchor="mt")

    # Result highlight
    y = 940
    _draw_rounded_rect(draw, (100, y, WIDTH - 100, y + 220), 35, (0, 0, 0, 50))
    overlay2 = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    ov2_draw = ImageDraw.Draw(overlay2)
    _draw_rounded_rect(ov2_draw, (100, y, WIDTH - 100, y + 220), 35, (41, 128, 185, 60))
    img = Image.alpha_composite(img.convert("RGBA"), overlay2).convert("RGB")
    draw = ImageDraw.Draw(img)

    label_cash = {"ru": "К ОПЛАТЕ НАЛИЧНЫМИ", "en": "CASH TO PAY"}.get(lang, "CASH TO PAY")
    draw.text((WIDTH // 2, y + 40), f"\U0001F4B3 {label_cash}", font=_get_font(40), fill=(200, 230, 255), anchor="mt")
    draw.text((WIDTH // 2, y + 110), f"${cash:,.2f}", font=_get_font(96, bold=True), fill="white", anchor="mt")

    # Savings
    y = 1200
    label_save = {"ru": "Ваша экономия", "en": "Your Savings"}.get(lang, "Savings")
    draw.text((WIDTH // 2, y), f"🎉 {label_save}: ${savings:,.2f}", font=_get_font(40, bold=True), fill=(255, 215, 0), anchor="mt")

    # Footer
    draw.text((WIDTH // 2, HEIGHT - 320), "InLeader", font=_get_font(36, bold=True), fill=(255, 255, 255), anchor="mt")
    draw.text((WIDTH // 2, HEIGHT - 270), "@InLeader_bot", font=_get_font(30), fill=(120, 150, 200), anchor="mt")

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def generate_conversion_receipt(
    price: float,
    standard: float,
    converted: float,
    fees: float,
    final: float,
    lang: str = "ru",
) -> bytes:
    """Generate a story-sized image for the conversion calculator result."""
    img = _load_or_create_bg("conversion_bg.png", (44, 62, 80), (52, 152, 219))
    draw = ImageDraw.Draw(img)

    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)
    _draw_rounded_rect(ov_draw, (60, 200, WIDTH - 60, HEIGHT - 200), 40, (255, 255, 255, 30))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Header
    font_title = _get_font(72, bold=True)
    draw.text((WIDTH // 2, 300), "InLeader", font=font_title, fill="white", anchor="mt")

    font_sub = _get_font(42)
    subtitle = {"ru": "\U0001F504 Конвертация ББ (Без доплат)", "en": "\U0001F504 BB Conversion (Zero Cash)"}.get(lang, "\U0001F504 Conversion")
    draw.text((WIDTH // 2, 400), subtitle, font=font_sub, fill=(200, 230, 255), anchor="mt")

    draw.line([(120, 480), (WIDTH - 120, 480)], fill=(255, 255, 255, 128), width=2)

    font_label = _get_font(34)
    font_value = _get_font(56, bold=True)

    y = 520
    draw.text((WIDTH // 2, y), "Цена круиза / Cruise Price", font=font_label, fill=(180, 210, 255), anchor="mt")
    draw.text((WIDTH // 2, y + 50), f"${price:,.0f}", font=font_value, fill="white", anchor="mt")

    y = 660
    draw.text((WIDTH // 2, y), "Доступные баллы / Standard RP", font=font_label, fill=(180, 210, 255), anchor="mt")
    draw.text((WIDTH // 2, y + 50), f"{standard:,.0f} RP", font=font_value, fill="white", anchor="mt")

    y = 800
    draw.text((WIDTH // 2, y), "Конвертация 2 к 1 / Converted RP", font=font_label, fill=(180, 210, 255), anchor="mt")
    draw.text((WIDTH // 2, y + 50), f"{converted:,.0f} RP", font=font_value, fill=(255, 215, 0), anchor="mt")

    y = 940
    draw.text((WIDTH // 2, y), "Налоги и сборы / Fees", font=font_label, fill=(180, 210, 255), anchor="mt")
    draw.text((WIDTH // 2, y + 50), f"${fees:,.0f}", font=font_value, fill="white", anchor="mt")

    # Final highlight
    y = 1080
    _draw_rounded_rect(draw, (100, y, WIDTH - 100, y + 180), 35, (46, 204, 113, 80))
    draw.text((WIDTH // 2, y + 30), "ИТОГО К СПИСАНИЮ / TOTAL RP", font=_get_font(38, bold=True), fill="white", anchor="mt")
    draw.text((WIDTH // 2, y + 90), f"{final:,.0f} RP", font=_get_font(80, bold=True), fill=(255, 255, 200), anchor="mt")

    y = 1290
    draw.text((WIDTH // 2, y), "🔥 НОЛЬ ДОПЛАТ С КАРТЫ! / ZERO CASH!", font=_get_font(44, bold=True), fill=(255, 215, 0), anchor="mt")

    # Footer
    draw.text((WIDTH // 2, HEIGHT - 320), "InLeader", font=_get_font(36, bold=True), fill=(255, 255, 255), anchor="mt")
    draw.text((WIDTH // 2, HEIGHT - 270), "@InLeader_bot", font=_get_font(30), fill=(120, 150, 200), anchor="mt")

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()
