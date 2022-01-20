import pandas as pd
import sort_by_date
def save(userID, location, date, time, ocr):
    idx = len(pd.read_csv("database.csv"))
    new_df = pd.DataFrame({"userID" : userID,
                           "location":location,
                           "date": date,
                          "time":time,
                          "ocr" : ocr},
                         index = [idx])
    new_df.to_csv("database.csv",mode = "a", header = False)
    return None

def load_list(user):
    house_list = []
    df = pd.read_csv("database.csv")
    for i in range(len(df)):
        if df.iloc[i]["userID"] == user:
            house_list.append(df.iloc[i].tolist())
        #print(df.iloc[i])
        #print(df.iloc[i].tolist)
        #house_list.append(df.iloc[i].tolist())
    #print(house_list)
    return house_list

def now_index():
    df = pd.read_csv("database.csv")
    return len(df)-1


def load_house(idx):
    df = pd.read_csv("database.csv")
    house_info = df.iloc[idx]
    return house_info


if __name__ =="__main__":
    load_list()
