import unreal_engine as ue
import os
from PIL import Image

class ScreenShotter:
    # 注意不能直接在begin_play后跟screenshot函数，否则会引发编辑器崩溃（因为此时屏幕数据尚未加载完毕）
    def begin_play(self):
        owner = self.uobject.get_owner()
        owner.bind_event('ScreenShot', self.screenshot)

    def screenshot(self):
        width, height = ue.editor_get_pie_viewport_size()
        pixels = ue.editor_get_pie_viewport_screenshot()

        ue.log("{0} {1} {2}".format(width, height, len(pixels)))

        pixels_array = []

        for y in range(0, height):
            for x in range(0, width):
                index = y * width + x
                pixel = pixels[index]
                pixels_array.append((pixel.r, pixel.g, pixel.b, 255))

        img = Image.new('RGBA', (width, height))
        img.putdata(pixels_array)
        path = os.path.expanduser("~\Desktop\pie_screenshot.png")
        img.save(path)
        ue.log("Shot Complete. Image has been saved to {0}".format(path))