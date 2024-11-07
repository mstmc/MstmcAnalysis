import pandas as pd


class DataProcess:

    def content_summary(self):
        """
DataSet/ContentAnalysis_SingleMass.xlsx
内容标题	发表时间	总阅读人数	总阅读次数	总分享人数	总分享次数	阅读后关注人数	送达人数	公众号消息阅读次数	送达阅读率	首次分享次数	分享产生阅读次数	首次分享率	每次分享带来阅读次数	阅读完成率	内容url
微软头马会议 | 婚姻与家庭?	20220329	94	163	7	10	0	2112	79	0.0374	5	69	0.0633	6.9	0.6889	xxx
微软头马会议 | Be Yourself?	20220322	133	209	7	11	0	2109	59	0.028	4	135	0.0678	12.2727	0.7045	xxx
        :return:
        """
        file_path = "DataSet/ContentAnalysis_SingleMass.xlsx"
        df = pd.read_excel(file_path, engine='openpyxl')

        df_series = df.agg({
            "内容标题": "count",
            "总阅读人数": sum,
            "总阅读次数": sum
        })
        # theis is 4 pages are not weekly meetings
        df_series["会议场数"] = df_series["内容标题"] - 4

        df_series["平均阅读人数"] = df_series["总阅读人数"] // df_series["内容标题"]
        df_series["平均阅读次数"] = df_series["总阅读次数"] // df_series["内容标题"]

        print(df_series)

    def content_top_read(self, top_k=5):
        file_path = "DataSet/ContentAnalysis_SingleMass.xlsx"
        df = pd.read_excel(file_path, engine='openpyxl')

        keep_columns = ["内容标题", "发表时间", "总阅读人数", "总阅读次数"]
        # top k
        df_sort = df.sort_values(by="总阅读人数", ascending=False, ignore_index=True)
        df_sort = df_sort[keep_columns]
        print(df_sort.head(top_k))

        # 联合会议
        df_filter = df[df['内容标题'].str.contains("联合", na=False)].reset_index()
        df_filter = df_filter[keep_columns]

        print(df_filter)


if __name__ == '__main__':
    obj = DataProcess()
    obj.content_summary()
    # obj.content_top_read()

    print("done")

