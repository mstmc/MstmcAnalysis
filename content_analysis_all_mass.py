import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class DataProcess:

    def content_groupby_source(self, data_set_file_path):
        """
日期	阅读次数	阅读人数	分享次数	分享人数	阅读原文次数	阅读原文人数	收藏次数	收藏人数	群发篇数	渠道
20220331	3	2	0	0	0	0	0	0	0	公众号消息
20220331	4	1	0	0	0	0	0	0	0	聊天会话
        :return:
        """
        # file_path = "DataSet/ContentAnalysis_AllMass_2024.xlsx"
        df = pd.read_excel(data_set_file_path, engine='openpyxl')

        df_group = df.groupby(by=["渠道"]).agg({
            "阅读次数": sum,
            # "阅读人数": sum
        })
        # df_sort = df_group.sort_values(by="阅读次数", ascending=False, ignore_index=False)
        # df_sort = df_sort[df_sort.index != "全部"]
        # print(df_sort)

        # 搜一搜+看一看
        # df_group.loc["搜一搜+看一看", "阅读次数"] = \
        #     df_group.loc["搜一搜", "阅读次数"] + \
        #     df_group.loc["看一看精选", "阅读次数"] + \
        #     df_group.loc["朋友在看", "阅读次数"]
        df_group.loc["搜一搜+看一看", "阅读次数"] = \
            df_group.loc["搜一搜", "阅读次数"]
        labels = ["聊天会话", "公众号消息", "朋友圈", "公众号主页", "其它", "搜一搜+看一看"]
        xdata = []
        for label in labels:
            xdata.append(int(df_group.loc[label, "阅读次数"]))
        xdata.sort(reverse=True)
        sums = int(df_group.loc["全部", "阅读次数"])

        # 设置突出显示的标签
        explode = [0 for _ in range(len(xdata))]
        explode[0] = 0.16
        explode[-1] = 0.14
        # 设置标签颜色，浅黄，橙，绿，红，紫，青
        colors = ['red', 'orange', 'green', 'wheat', 'violet', 'teal']

        # 添加标题 Followers Composition
        plt.title("渠道构成 (阅读次数{}次)".format(sums), fontproperties='KaiTi', fontsize=20)  # 添加图名

        # 设置正圆显示
        plt.axis('equal')

        # 构造数据
        plt.rcParams['font.sans-serif'] = 'SimHei'  # 中文显示乱码处理，SimHei是黑体
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示正负号

        # 开始绘制
        p, tx, autotexts = plt.pie(
            xdata,
            explode=explode,  # 突出显示的项
            labels=labels,  # 各球队标签
            colors=colors,  # 颜色属性
            radius=1,  # 设置饼图半径
            counterclock=False,  # 设置为顺时针方向开始绘图
            labeldistance=1,  # 设置标签位置
            autopct="",
            #     autopct='%.2f%%',  # 设置百分比格式，这里保存两位小数
            textprops={'fontsize': 12, 'color': 'black'},  # 设置文本属性,字体大小为12，颜色为黑
            wedgeprops={'linewidth': 0.7, 'edgecolor': 'black'},  # 设置边框，宽度为0.7，颜色为黑
            shadow=True,  # 添加阴影
            startangle=90  # 设置开始绘图的角度
        )

        # # 创建饼图后更改文本
        for i, a in enumerate(autotexts):
            a.set_text("{0},{1}%".format(xdata[i], int(xdata[i] / sums * 100)))
        plt.legend(loc='right', bbox_to_anchor=(1.1, 0.5))

        plt.show()


if __name__ == '__main__':
    obj = DataProcess()
    obj.content_groupby_source(data_set_file_path="DataSet_2024/ContentAnalysis_AllMass.xlsx")

    print("done")

