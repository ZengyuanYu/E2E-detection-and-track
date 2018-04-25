from PIL import Image, ImageDraw, ImageFont
import codecs as cs

def genFontImage(font, char):
    size = font.size
    image = Image.new('1', (size, size))
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), char, font=font, fill='#ff0000')
    return image



if __name__ == '__main__':
    size = 14
    font = ImageFont.truetype('platech.ttf', size)
    hansfile = cs.open('1.txt', 'r', 'utf-8')
    hans = hansfile.read()
    hansfile.close()

    for han in hans[:10]:
        image = genFontImage(font,han)
        image.save(str(hans.index(han))+'.png')
