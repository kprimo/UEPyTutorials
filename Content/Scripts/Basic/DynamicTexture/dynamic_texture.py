import unreal_engine as ue
from unreal_engine.enums import EPixelFormat

import time

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

class DynamicTexture:

    def begin_play(self):
        width = 1024
        height = 1024
        dpi = 72.0
        self.texture = ue.create_transient_texture(width, height, EPixelFormat.PF_R8G8B8A8)

        self.uobject.get_owner().Plane.OverrideMaterials[0].set_material_texture_parameter('Texture', self.texture)

        self.fig = plt.figure(1)
        self.fig.set_dpi(dpi)
        self.fig.set_figwidth(width/dpi)
        self.fig.set_figheight(height/dpi)

        self.uobject.get_owner().bind_event('GenerateTexture', self.generate_texture)
    
    def generate_texture(self):

        # 清除当前plot数据
        plt.clf()

        # 获取当前时间
        now = time.localtime()
        hour = now.tm_hour
        minute = now.tm_min
        second = now.tm_sec
        doublepi = 3.1415926535 * 2

        # 创建一个极坐标图
        ax = plt.subplot(111, polar=True)

        # 绘制时针
        ax.plot([0, -hour/12*doublepi], [0, 0.4], linewidth=40, color="red")

        # 绘制分针
        ax.plot([0, -minute/60*doublepi], [0, 0.6], linewidth=30, color="green")

        # 绘制秒针
        ax.plot([0, -second/60*doublepi], [0, 0.8], linewidth=20, color="blue")

        self.fig.canvas.draw()
        self.texture.texture_set_data(bytes(self.fig.canvas.buffer_rgba()))