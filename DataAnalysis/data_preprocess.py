import os
import pandas as pd
import re


class DataPreProcess:

    def read_merge_data(self, data_raw_folder, data_raw_file_prefix, data_set_folder, data_set_file_name):
        # TODO: First manually save xls as xlsx file:
        listdir = os.listdir(data_raw_folder)

        df = pd.DataFrame()
        for file in listdir:
            if file.startswith(data_raw_file_prefix) and file.endswith(".xlsx"):
                df_tmp = pd.read_excel(data_raw_folder + file, header=1, engine='openpyxl')  # openpyxl
                df_tmp.dropna(inplace=True)
                df = pd.concat([df, df_tmp])

        # df.to_excel(data_set_folder + prefix + "20240101_20241105.xlsx", index=False)
        df.to_excel(data_set_folder + data_set_file_name, index=False)

    def read_merge_ContentAnalysis(self, data_raw_folder, data_raw_file_pattern, data_set_folder, data_set_file_name):
        listdir = os.listdir(data_raw_folder)

        # df_tmp = pd.read_excel(data_raw_folder + "ContentAnalysis_SingleMass_0101~0331.xls")

        df = pd.DataFrame()
        for filename in listdir:
            if re.match(data_raw_file_pattern, filename):
                df_tmp = pd.read_excel(data_raw_folder + filename)
                df_tmp.dropna(inplace=True)
                df = pd.concat([df, df_tmp])

        df.to_excel(data_set_folder + data_set_file_name, index=False, engine='openpyxl')


if __name__ == '__main__':
    obj = DataPreProcess()
    obj.read_merge_data(
        data_raw_folder="DataRaw_2025/", data_raw_file_prefix="user_analysis_2025",
        data_set_folder="DataSet_2025/", data_set_file_name="UserAnalysis.xlsx")
    # obj.read_merge_ContentAnalysis(
    #     data_raw_folder="DataRaw_2024/", data_raw_file_pattern="ContentAnalysis_AllMass_2024.*.xls",
    #     data_set_folder="DataSet_2024/", data_set_file_name="ContentAnalysis_AllMass.xlsx")

    print("done")

"""
user_analysis.xlsx schema
时间	新关注人数	取消关注人数	净增关注人数	累积关注人数
2022-01-01 00:00:00	1	0	1	2068
2022-01-02 00:00:00	2	0	2	2070

DataSet/user_composation.xlsx
StartTime	EndTIme	新增关注	搜一搜	扫描二维码	文章页关注	名片分享	他人转载	其他合计
20220101	20220331	124	77	2	29	7	0	9
20220401	20220629	99	41	8	31	13	0	6

"""
