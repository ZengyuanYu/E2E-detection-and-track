
 1 def pasteWord(word):
 2     '''输入一个文字，输出一张包含该文字的图片'''
 3     pygame.init()
 4     font = pygame.font.Font(os.path.join("./fonts", "a.ttf"), 22)
 5     text = word.decode('utf-8')
 6     imgName = "E:/dataset/chinesedb/chinese/"+text+".png"
 7     paste(text,font,imgName)
 8         
 9 def paste(text,font,imgName,area = (0, -9)):
10     '''根据字体，将一个文字黏贴到图片上，并保存'''
11     im = Image.new("RGB", (32, 32), (255, 255, 255))
12     rtext = font.render(text, True, (0, 0, 0), (255, 255, 255))
13     sio = StringIO.StringIO()
14     pygame.image.save(rtext, sio)
15     sio.seek(0)
16     line = Image.open(sio)
17     im.paste(line, area)
18     #im.show()
19     im.save(imgName)
