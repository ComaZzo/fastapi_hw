from fastapi import FastAPI
import datetime
import sqlite3
import re


app = FastAPI()

con = sqlite3.connect("../action_user.db")
cur = con.cursor()


@app.get("/api/users") # ?unique={unique_bool}&date_to={date_to}&date_from={date_from}")
async def users(unique: bool = False,
                date_to: str = str(datetime.datetime.today().date()),
                date_from: str = "2020-01-01"):
    reg_exp = '(19\d\d|20\d\d)[-](0[1-9]|1[012])[-](0[1-9]|[12][0-9]|3[01])'

    if len(re.findall(reg_exp, date_to)) == 1 and len(re.findall(reg_exp, date_from)) == 1:
        unique_string = ""
        if unique: unique_string = "DISTINCT"
        cur.execute(f"""SELECT {unique_string} date,
                        ROW_NUMBER() OVER (PARTITION BY date) AS count 
                        FROM actions
                        JOIN users 
                        ON actions.userid = users.userid
                        WHERE strftime('%s', date) < strftime('%s','{date_to}') 
                        AND  strftime('%s', date) >  strftime('%s','{date_from}');""")
        response_list = cur.fetchall()
        response_dict = {"data": {}}
        for i in range(len(response_list)):
            response_dict["data"][i] = {"date": response_list[i][0], "count": response_list[i][1]}
        return response_dict
    return


@app.get("/api/actions")
async def actions():
    cur.execute("""SELECT date, 
                   ROW_NUMBER() OVER (PARTITION BY date) AS count,
                   action
                   FROM actions;""")
    response_list = cur.fetchall()
    response_dict = {"data": {}}
    for i in range(len(response_list)):
        response_dict["data"][i] = {"date": response_list[i][0],
                                    "count": response_list[i][1],
                                    "action": response_list[i][2]}
    return response_dict


@app.get("/api/usage")
async def usage():
    cur.execute("""SELECT date,
                    ROW_NUMBER() OVER (PARTITION BY date) AS count, 
                    action 
                    FROM actions;""")
    query_result = cur.fetchall()

    # group by date
    response_list = []
    j = 0
    for i in range(len(query_result) - 1):
        if query_result[i-1][0] != query_result[i][0] or i != 0:
            response_list[j-1][2].append(query_result[i][2])
        else:
            response_list.append([query_result[i][0], query_result[i][1], []])
            j += 1

    response_dict = {"data": {}}
    for i in range(len(response_list)):
        response_dict["data"][i] = {"date": response_list[i][0],
                                    "count": response_list[i][1],
                                    "actions": response_list[i][2]}
    return response_dict
