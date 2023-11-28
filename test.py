from database import normalised_data
from main import data
import pprint


# district_per_state = {}
# result = []
# states = data.find({}, {"_id": False, "State/UT": True})
# state_list = [state["State/UT"] for state in states]
# unique_state = set(state_list)
# for state in unique_state:
#     districts = data.find({"State/UT": state}, {"District Names": True, "_id": False})
#     distirct_list = [district["District Names"] for district in districts]
#     district_per_state = {"state": state, "distirct": distirct_list}
#     result.append(district_per_state)
# print(result)

def region_wise(category, groupby):
    region = normalised_data.aggregate([
        {
            "$group": {
                "_id": f"${groupby}",
                "totalmildwomen": {"$sum": f"${category}"}
            }
        },
        {
            "$project": {
                "Region": "$_id",
                "_id": 0,
                "totalmildwomen": 1
            }
        }
    ])
    data_dict = {}
    for datas in region:
        data_dict[datas["Region"]] = datas["totalmildwomen"]
    return data_dict


