from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import os

W, H = 1400, 520
FPS = 16
DURATION = 9
FRAMES = FPS * DURATION
BG = (10, 12, 16)
ORANGE = (212, 83, 43)
GOLD = (244, 201, 132)
MINT = (92, 205, 170)
BLUE = (88, 146, 255)
WHITE = (245, 242, 235)
GRAY = (155, 163, 175)
DIM = (69, 74, 82)

out_path = os.path.join(os.path.dirname(__file__), 'hero.gif')


def font(size, bold=False, serif=False):
    candidates = []
    if serif:
        candidates += [
            r'C:\\Windows\\Fonts\\NotoSerifSC-Bold.otf',
            r'C:\\Windows\\Fonts\\SourceHanSerifSC-Bold.otf',
            r'C:\\Windows\\Fonts\\simfang.ttf',
        ]
    else:
        candidates += [
            r'C:\\Windows\\Fonts\\Inter-SemiBold.ttf',
            r'C:\\Windows\\Fonts\\Inter-Regular.ttf',
            r'C:\\Windows\\Fonts\\arialbd.ttf' if bold else r'C:\\Windows\\Fonts\\arial.ttf',
        ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size=size)
            except Exception:
                pass
    return ImageFont.load_default()


f_title = font(92, bold=True, serif=True)
f_sub = font(26, bold=True, serif=True)
f_ui = font(16)
f_small = font(12)
f_tiny = font(10)

questions = [
    '这个问题真的成立吗',
    '先开天，再回答',
    '把问题重写对',
    '从人物到领域',
    '从观点到协议',
]

protocols = [
    ('人物协议', '心智模型 · 启发式 · 边界'),
    ('领域协议', '结构 · 进入路径 · 失效条件'),
    ('审计工具', '诊断 · 提炼 · 验收'),
    ('开天能力', '伪前提 · 重写问题'),
]

categories = [
    ('科技与半导体', BLUE),
    ('金融与支付网络', MINT),
    ('工业与制造', GOLD),
    ('农业与供应链', ORANGE),
    ('政商与叙事', (204, 120, 255)),
]

people = [
    'Elon Musk', 'Tim Cook', 'Jensen Huang', 'Larry Fink',
    'Jane Fraser', 'Kelly Ortberg', 'Brian Sikes', 'Donald Trump'
]


def lerp(a, b, t):
    return a + (b - a) * t


def ease(t):
    return 0.5 - 0.5 * math.cos(math.pi * max(0.0, min(1.0, t)))


def draw_glow(base, xy, text, font_obj, fill, glow=(255, 255, 255), anchor=None):
    layer = Image.new('RGBA', base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for ox, oy, alpha in [(0, 0, 80), (1, 0, 40), (-1, 0, 40), (0, 1, 40), (0, -1, 40)]:
        d.text((xy[0]+ox, xy[1]+oy), text, font=font_obj, fill=glow + (alpha,), anchor=anchor)
    layer = layer.filter(ImageFilter.GaussianBlur(6))
    base.alpha_composite(layer)
    d = ImageDraw.Draw(base)
    d.text(xy, text, font=font_obj, fill=fill + (255,), anchor=anchor)


def pill(draw, x, y, w, h, label, fill, text_color=(15, 18, 22)):
    draw.rounded_rectangle((x, y, x+w, y+h), radius=h//2, fill=fill)
    draw.text((x+w/2, y+h/2-1), label, font=f_tiny, fill=text_color, anchor='mm')

frames = []
for i in range(FRAMES):
    p = i / FRAMES
    img = Image.new('RGBA', (W, H), BG + (255,))
    d = ImageDraw.Draw(img)

    # background ambience
    for cx, cy, r, col, alpha in [
        (180, 120, 220, ORANGE, 28),
        (1100, 120, 260, BLUE, 22),
        (990, 400, 300, MINT, 18),
    ]:
        layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        ld.ellipse((cx-r, cy-r, cx+r, cy+r), fill=col + (alpha,))
        layer = layer.filter(ImageFilter.GaussianBlur(40))
        img.alpha_composite(layer)

    # motion phases
    q = ease(min(1, p / 0.28))
    c = ease(min(1, max(0, (p - 0.22) / 0.24)))
    r = ease(min(1, max(0, (p - 0.46) / 0.28)))
    l = ease(min(1, max(0, (p - 0.74) / 0.22)))

    # title area
    draw_glow(img, (90, 132), '盘古.skill', f_title, WHITE)
    draw_glow(img, (94, 210), 'Pangu turns questions into protocols', f_ui, GRAY)
    draw_glow(img, (92, 252), '人物协议 · 领域协议 · 开天能力', f_sub, (240, 242, 238))

    # headline ticker
    ticker_x = 92 + (1 - q) * -40
    draw_glow(img, (ticker_x, 316), questions[min(len(questions)-1, int(p * len(questions) * 1.4))], f_ui, ORANGE)

    # left pipeline nodes
    px = 520
    py = 110
    node_y = [120, 200, 280, 360]
    for idx, (label, desc) in enumerate(protocols):
        yy = node_y[idx]
        alpha = 60 + int(170 * ease(max(0, min(1, (p - idx*0.08) / 0.25))))
        box_w = 280 if idx != 3 else 240
        box_h = 58
        x = px + (idx % 2) * 22
        rr = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        rd = ImageDraw.Draw(rr)
        rd.rounded_rectangle((x, yy, x+box_w, yy+box_h), radius=18, outline=ORANGE + (alpha,), width=2, fill=(18, 21, 28, alpha//5))
        rr = rr.filter(ImageFilter.GaussianBlur(0.2))
        img.alpha_composite(rr)
        d.text((x+18, yy+13), label, font=f_ui, fill=WHITE)
        d.text((x+18, yy+34), desc, font=f_small, fill=GRAY)

    # arrows between nodes
    for ay in [170, 250, 330]:
        d.line((800, ay, 860, ay), fill=ORANGE + (120,), width=3)
        d.polygon([(860, ay), (846, ay-8), (846, ay+8)], fill=ORANGE + (150,))

    # center gateway / funnel
    gateway_x = 845
    gw_scale = 1 + 0.15 * c
    top_w = int(140 * gw_scale)
    bot_w = int(54 * gw_scale)
    top_y = 96 + int(6 * math.sin(p * math.pi * 4))
    bot_y = 410
    poly = [(gateway_x-top_w//2, top_y), (gateway_x+top_w//2, top_y), (gateway_x+bot_w//2, bot_y), (gateway_x-bot_w//2, bot_y)]
    d.polygon(poly, fill=(41, 21, 15, 180), outline=ORANGE + (200,))
    d.text((gateway_x, 76), 'OPEN THE SKY', font=f_small, fill=ORANGE, anchor='mm')

    # output cards
    card_base_x = 980
    card_y = 104
    for j, (name, col) in enumerate(categories):
        x = card_base_x + int(j * 70 * (0.7 + 0.3 * l))
        y = card_y + int((j % 2) * 18)
        alpha = int(80 + 120 * ease(max(0, min(1, (p - 0.5 - j*0.03) / 0.22))))
        layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        ld.rounded_rectangle((x, y, x+250, y+82), radius=18, fill=(16, 19, 24, alpha), outline=col + (alpha+40,), width=2)
        ld.rectangle((x+18, y+18, x+34, y+34), fill=col + (alpha+50,))
        ld.text((x+48, y+16), name, font=f_ui, fill=WHITE + (255,))
        ld.text((x+48, y+41), people[j*2 % len(people)], font=f_small, fill=GRAY + (255,))
        layer = layer.filter(ImageFilter.GaussianBlur(0.15))
        img.alpha_composite(layer)

    # bottom summary ribbon
    ribbon_y = 454
    d.rounded_rectangle((86, ribbon_y, 1288, ribbon_y+38), radius=19, fill=(14, 17, 21), outline=(44, 48, 58))
    draw_glow(img, (110, ribbon_y+19), '18 人物协议 + 1 主题协议', f_ui, GOLD)
    draw_glow(img, (390, ribbon_y+19), 'Protocol factory for AI skills', f_ui, WHITE)
    draw_glow(img, (760, ribbon_y+19), 'Research → extract → audit → ship', f_ui, GRAY)
    draw_glow(img, (1168, ribbon_y+19), 'MIT', f_ui, ORANGE)

    # moving grain / sparks
    for s in range(16):
        xx = int(90 + (i*17 + s*97) % 1220)
        yy = int(78 + ((i*13 + s*53) % 360))
        rad = 1 + (s % 3)
        d.ellipse((xx-rad, yy-rad, xx+rad, yy+rad), fill=(255, 255, 255, 70))

    frames.append(img.convert('P', palette=Image.Palette.ADAPTIVE, colors=256))

frames[0].save(out_path, save_all=True, append_images=frames[1:], duration=int(1000/FPS), loop=0, optimize=True, disposal=2)
print(out_path)
