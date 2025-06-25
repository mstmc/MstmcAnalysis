import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager


class DataProcess:

    def user_trend_by_day(self, data_set_file_path):
        df = pd.read_excel(data_set_file_path, engine='openpyxl')

        plt.plot(df["时间"], df["累积关注人数"])
        plt.grid(True)
        plt.title("Trend of Attention")

        # add title
        for index, row in df.iterrows():
            if str(row["Title"]) != 'nan':
                plt.text(row["时间"], row["累积关注人数"], row["Title"])

        plt.show()

    def user_trend_by_month(self, data_set_file_path):
        """
UserAnalysis.xlsx
时间	新关注人数	取消关注人数	净增关注人数	累积关注人数
2022-01-01 00:00:00	1	0	1	2068
2022-01-02 00:00:00	2	0	2	2070
        :return:
        """
        df = pd.read_excel(data_set_file_path, engine='openpyxl')

        df["Month"] = df["时间"].apply(lambda x: x.month)

        df_group = df.groupby(["Month"]).agg({
            "新关注人数": sum,
            # "取消关注人数": sum,
            "净增关注人数": sum,
            "累积关注人数": max,
            # "Title": lambda x: x.str.cat(sep=',')
        })
        df_group.reset_index(inplace=True)

        xticks = np.arange(len(df_group["Month"]))

        plt.subplot(211)
        plt.plot(xticks, df_group["累积关注人数"], 'r-o', label="Total Followers: {0}".format(max(df_group["累积关注人数"])))
        plt.grid(True)
        plt.title("Trend of Followers in 2025")
        plt.xticks(xticks, df_group["Month"])
        plt.legend(loc="upper left")
        # plt.xlabel("Month")
        plt.ylabel("Total Followers")
        # add text
        # for index, row in df_group.iterrows():
        #     if str(row["Title"]) != 'nan':
        #         plt.text(row["Month"]-1, row["累积关注人数"], row["Title"])

        plt.subplot(212)
        plt.bar(xticks, df_group["新关注人数"], width=0.5, color='green', label="New Followers: {0}".format(sum(df_group["新关注人数"])))
        plt.grid(True)
        # plt.title("Trend of New Followers")
        plt.xticks(xticks, df_group["Month"])
        plt.legend(loc="upper left")
        plt.xlabel("Month")
        plt.ylabel("New Followers")

        # add text
        # for index, row in df_group.iterrows():
        #     if str(row["Title"]) != 'nan':
        #         plt.text(row["Month"] - 1 - 0.25, row["净增关注人数"], row["Title"])

        plt.show()

    def user_composation(self, data_set_file_path):
        """
DataSet/UserComposition.xlsx
This table data is manually packed from MicrosoftTMC

StartTime	EndTIme	新增关注	搜一搜	扫描二维码	文章页关注	名片分享	他人转载	其他合计
20220101	20220331	124	77	2	29	7	0	9
20220401	20220629	99	41	8	31	13	0	6
        :return:
        """
        df = pd.read_excel(data_set_file_path, engine='openpyxl')

        df_series = df.agg({
            # "StartTime": min,
            # "EndTIme": max,
            "新增关注": sum,
            "搜一搜": sum,
            "扫描二维码": sum,
            "文章页关注": sum,
            "名片分享": sum,
            "他人转载": sum,
            "其他合计": sum
        })
        labels = ["搜一搜", "扫描二维码", "文章页关注", "名片分享", "他人转载", "其他合计"]
        xdata = []
        for label in labels:
            xdata.append(df_series[label])
        xdata.sort(reverse=True)
        sums = df_series["新增关注"]

        # 设置突出显示的标签
        explode = [0.16, 0.0, 0.0, 0, 0, 0]
        # 设置标签颜色，浅黄，橙，绿，红，紫，青
        colors = ['red', 'orange', 'green', 'wheat', 'violet', 'teal']

        # 构造数据
        # plt.rcParams['font.sans-serif'] = 'SimHei'  # 中文显示乱码处理，SimHei是黑体
        # plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示正负号
        font_path = "SimHei.ttf"  # 替换为字体文件的实际路径
        font_prop = font_manager.FontProperties(fname=font_path)

        # 添加标题 Followers Composition
        plt.title("关注者构成 (新增关注{}人)".format(sums), fontproperties=font_prop, fontsize=20)  # 添加图名

        # 设置正圆显示
        plt.axis('equal')

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
            textprops={'fontsize': 12, 'color': 'black', 'fontproperties': font_prop},  # 设置文本属性,字体大小为12，颜色为黑
            wedgeprops={'linewidth': 0.7, 'edgecolor': 'black'},  # 设置边框，宽度为0.7，颜色为黑
            shadow=True,  # 添加阴影
            startangle=90  # 设置开始绘图的角度
        )

        # 创建饼图后更改文本
        for i, a in enumerate(autotexts):
            a.set_text("{0},{1}%".format(xdata[i], int(xdata[i] / sums * 100)))
        plt.legend(loc='right', bbox_to_anchor=(1.1, 0.5), prop=font_prop)

        plt.show()


if __name__ == '__main__':
    obj = DataProcess()
    # obj.user_trend_by_day(data_set_file_path="DataSet_2024/UserAnalysis.xlsx")
    obj.user_trend_by_month(data_set_file_path="DataSet_2025/UserAnalysis.xlsx")
    # obj.user_composation(data_set_file_path="DataSet_2024/UserComposition.xlsx")

    print("done")
