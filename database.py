from pymongo import MongoClient
import pandas as pd
import pprint

connection_string = "mongodb://localhost:27017"
client = MongoClient(connection_string)
database = client["Hypertension"]
data = database["Data"]
# datas = data.find({},{"_id": 0})
# for d in datas:
#     pprint.pprint(d)

# path = "C:/Users/shara/PycharmProjects/dbms/data.xls"
# df = pd.read_excel(path)
# dict_df = df.to_dict(orient='records')
# data.insert_many(dict_df)

normalised_data = database["Normalised"]
path = "C:/Users/shara/PycharmProjects/dbms/district_wise.csv"
nf_df = pd.read_csv(path)
nf_dict = nf_df.to_dict(orient="records")
normalised_data.insert_many(nf_dict)


# state_wise = data.aggregate([
#     {
#         "$group": {
#             "_id": "$State/UT",
#             "totalHouseholds": {"$sum": "$Number of Households surveyed"}
#         }
#     },
#     {
#         "$project": {
#             "State": "$_id",
#             "_id": 0,
#             "totalHouseholds": 1
#         }
#     }
# ])
# # pprint.pprint(state_wise)
# # for state in state_wise:
# #     print(state)
#
# district_wise = data.aggregate([
#     {
#         "$group": {
#             "_id": "$District Names",
#             "totalHouseholds": {"$sum": "$Number of Households surveyed"}
#         }
#     },
#     {
#         "$project": {
#             "District": "$_id",
#             "_id": 0,
#             "totalHouseholds": 1
#         }
#     }
# ])
#
# # for district in district_wise:
# #     pprint.pprint(district)
#
# pressure_report = data.aggregate([
#     {
#         "$group": {
#             "_id": "$District Names",
#             "Pressure": {
#                 "$sum": "$Women age 15 years and above wih Mildly elevated blood pressure (Systolic 140-159 mm of Hg "
#                         "and/or Diastolic 90-99 mm of Hg) (%)"}
#         }
#
#     },
#     {
#         "$project": {
#             "District": "$_id",
#             "_id": 0,
#             "Pressure": 1
#         }
#     }
# ])

# for report in pressure_report:
#     pprint.pprint(report)
