import re, datetime, uuid, csv
import boto3
import io
import pandas as pd

# Settings
timeFormat = "%Y-%m-%d"
bucket_name = 'nike-mayo'
nikemayo_authorized_users = "AuthorizedUsers.csv"

s3 = boto3.resource('s3')
file_obj = s3.Object(bucket_name, nikemayo_authorized_users)

def get_auth_users_dataframe():
    # Read the file content as bytes
    file_content = file_obj.get()['Body'].read()
    # Load the content into a pandas dataframe
    df = pd.read_csv(io.BytesIO(file_content), header=None)
    # set temptory header
    df.columns = ["regist_code", "expiry_date"]
    return df

def save_auth_users(df):
    # Create a file buffer to write the updated dataframe
    file_buffer = io.BytesIO()
    df.to_csv(file_buffer, index=False, header=False)
    # Put the updated file back to the bucket
    file_obj.put(Body=file_buffer.getvalue())

def foundUser(macAddress, df):
    ''' if user found return the row number, false if not found '''
    return len(df.loc[df["regist_code"] == macAddress, "expiry_date"]) != 0

def getMAC():
  # return this machine's MAC address
  return str(hex(uuid.getnode()))

def add_days(per:datetime, day):
    return per + datetime.timedelta(days=day)

def time_to_str(time):
    return datetime.datetime.strftime(time, timeFormat)

def str_to_time(string):
    return datetime.datetime.strptime(string.strip(), timeFormat)

def get_UTC():
    return datetime.datetime.strptime(datetime.datetime.now(datetime.timezone.utc).strftime(timeFormat), timeFormat)

def get_testing_dataframe():
    return pd.read_csv("AuthorizedUsers.csv")

def register_new_user(mac, days, df):
    if not foundUser(mac, df):
        new_time = time_to_str(add_days(get_UTC(), days))
        new_user = pd.DataFrame([[mac, new_time]], \
            columns = ['regist_code', 'expiry_date'])
        df = pd.concat([df, new_user])
        df = df.reset_index(drop=True)
        print(f"{mac} added. with {days} days left")
        return df
    else:
        print("Failed to add new user, user exist")
        return False

def update_mac(old_mac, new_mac, df):
    if foundUser(old_mac, df):
        df.loc[df["regist_code"] == old_mac, "regist_code"] = new_mac
        print(f"{old_mac} replaced with {new_mac}")
        return df
    else:
        print("Failed to update new mac, mac not found")
        return False

def update_date_add_days(mac, days, df):
    """ found the user and update the expriy date to a new date with added days """
    if foundUser(mac, df):
        cell = df.loc[df["regist_code"] == mac, "expiry_date"]
        if len(cell) > 1:
            print("Error, one or more same mac found.")
            return False
        new_date = add_days(str_to_time(cell.iloc[0]), days)
        day_left = (new_date - get_UTC()).days
        df.loc[df["regist_code"] == mac, "expiry_date"] = time_to_str(new_date)
        print(f"{mac} updated, now with {day_left} days left")
        return df
    else:
        print("Failed to update date, mac not found")
        return False

def update_date_up_to_days(mac, days, df):
    """ found the user and update the expriy date days left """
    if foundUser(mac, df):
        cell = df.loc[df["regist_code"] == mac, "expiry_date"]
        if len(cell) > 1:
            print("Error, one or more same mac found.")
            return False
        new_date = add_days(get_UTC(), days)
        day_left = (new_date - get_UTC()).days
        df.loc[df["regist_code"] == mac, "expiry_date"] = time_to_str(new_date)
        print(f"{mac} updated, now with {day_left} days left")
        return df
    else:
        print("Failed to update date, mac not found")
        return False

df = get_auth_users_dataframe()
df = update_date_up_to_days(getMAC(), 365, df)
print(df)
# save_auth_users(df)