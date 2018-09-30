import random
import string
from PIL import Image, ImageDraw, ImageFont


class Captcha(object):
    # 验证码位数
    number = 4
    # 验证码宽度和高度
    size = (100, 30)
    fontsize = 25
    line_nunber = 2
    SOURCE = list(string.ascii_letters)
    for index in range(0, 10):
        SOURCE.append(str(index))

    @classmethod
    def __gene_line(cls, draw, width, height):
        begin = (random.randint(0, width), random.randint(0, height))
        end = (random.randint(0, width), random.randint(0, height))
        draw.line([begin, end], fill=cls.__gene_random_color(), width=2)

    @classmethod
    def __gene_points(cls, draw, point_chance, width, height):
        chance = min(100, max(0, int(point_chance)))
        for w in range(width):
            for h in range(height):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    draw.point((w, h), fill=cls.__gene_random_color())

    @classmethod
    def __gene_random_color(cls, start=0, end=255):
        random.seed()
        return (random.randint(start, end), random.randint(start, end), random.randint(start, end))

    @classmethod
    def __gene_random_font(cls):
        # fonts = ['Courgette-Regular.ttf', 'LHANDW.TTF', 'Lobster-Regular.ttf', 'verdana.ttf']
        fonts = ['Courgette-Regular.ttf','Lobster-Regular.ttf']
        font = random.choice(fonts)
        print(font)
        return 'utils/captcha/' + font

    @classmethod
    def gene_text(cls, number):
        return ''.join(random.sample(cls.SOURCE, number))

    @classmethod
    def gene_graph_captcha(cls):
        width, height = cls.size
        # A:透明度
        image = Image.new('RGBA', (width, height), cls.__gene_random_color(0, 100))
        font = ImageFont.truetype(cls.__gene_random_font(), cls.fontsize)
        draw = ImageDraw.Draw(image)
        text = cls.gene_text(cls.number)
        font_width, font_height = font.getsize(text)
        draw.text(((width - font_width) / 2, (height - font_height) / 2),text, font=font,
                  fill=cls.__gene_random_color(150, 255))
        for x in range(0, cls.line_nunber):
            cls.__gene_line(draw, width, height)
        cls.__gene_points(draw, 10, width, height)
        # with open('captcha.png', 'wb') as fp:
        #     image.save(fp)
        return (text, image)