from fastapi import FastAPI
from database import data, normalised_data
from fastapi.middleware.cors import CORSMiddleware
from test import region_wise
import json
import pprint

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)


def presure_calc(diastolic_severity, gender):
    district = "District Names"
    state = "State/UT"
    gender = "Number of Women age 15-49 years interviewed"
    result_1 = data.find({}, {district: 1, state: 1, gender: 1, diastolic_severity: 1, "_id": 0})
    statewise_total = {}
    districtwise_total = {}
    for result in result_1:
        districtwise_total[result[district]] = result[gender] * result[diastolic_severity] // 100
        if result[state] in statewise_total:
            statewise_total[result[state]] += result[gender] * result[diastolic_severity] // 100
        else:
            statewise_total[result[state]] = result[gender] * result[diastolic_severity] // 100
    return statewise_total, districtwise_total


@app.get("/statewisedistricts")
def state_district():
    district_per_state = {}
    result = []
    states = data.find({}, {"_id": False, "State/UT": True})
    state_list = [state["State/UT"] for state in states]
    unique_state = set(state_list)
    for state in unique_state:
        districts = data.find({"State/UT": state}, {"District Names": True, "_id": False})
        distirct_list = [district["District Names"] for district in districts]
        district_per_state = {"state": state, "distirct": distirct_list}
        result.append(district_per_state)
    return result


men = "Number of Men age 15-54 years interviewed"
women = "Number of Women age 15-49 years interviewed"


@app.get("/mildwomen")
async def getresult1():
    pressure = "Women age 15 years and above wih Mildly elevated blood pressure (Systolic 140-159 mm of Hg and/or Diastolic 90-99 mm of Hg) (%)"
    return presure_calc(pressure, women)


@app.get("/mildmen")
async def getresult2():
    pressure = "Men age 15 years and above wih Mildly elevated blood pressure (Systolic 140-159 mm of Hg and/or Diastolic 90-99 mm of Hg) (%)"
    return presure_calc(pressure, men)


@app.get("/severewomen")
async def getresult3():
    pressure = "Women age 15 years and above wih Moderately or severely elevated blood pressure (Systolic ≥160 mm of Hg and/or Diastolic ≥100 mm of Hg) (%)"
    return presure_calc(pressure, women)


@app.get("/severemen")
async def getresult4():
    pressure = "Men age 15 years and above wih Moderately or severely elevated blood pressure (Systolic ≥160 mm of Hg and/or Diastolic ≥100 mm of Hg) (%)"
    return presure_calc(pressure, men)


@app.get("/elevatedewomen")
async def getresult3():
    pressure = "Women age 15 years and above wih Elevated blood pressure (Systolic ≥140 mm of Hg and/or Diastolic ≥90 mm of Hg) or taking medicine to control blood pressure (%)"
    return presure_calc(pressure, women)


@app.get("/elevatedmen")
async def getresult4():
    pressure = "Men age 15 years and above wih Elevated blood pressure (Systolic ≥140 mm of Hg and/or Diastolic ≥90 mm of Hg) or taking medicine to control blood pressure (%)"
    return presure_calc(pressure, men)


@app.get("/regionwise")
async def getresult5():
    women_mild = region_wise("Women MILD", "REGION")
    women_moderate = region_wise("Women Moderate", "REGION")
    women_extreme = region_wise("Women Extreme", "REGION")
    men_mild = region_wise("MEN MILD", "REGION")
    men_moderate = region_wise("MEN MODERATE", "REGION")
    men_extreme = region_wise("MEN EXTREME", "REGION")
    return women_mild, women_moderate, women_extreme, men_mild, men_moderate, men_extreme

@app.get("/statewise")
async def getresult6():
    women_mild = region_wise("Women MILD", "State/UT")
    women_moderate = region_wise("Women Moderate", "State/UT")
    women_extreme = region_wise("Women Extreme", "State/UT")
    men_mild = region_wise("MEN MILD", "State/UT")
    men_moderate = region_wise("MEN MODERATE", "State/UT")
    men_extreme = region_wise("MEN EXTREME", "State/UT")
    return women_mild, women_moderate, women_extreme, men_mild, men_moderate, men_extreme



