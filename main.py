import boto3
from dotenv import load_dotenv
import os
import pandas as pd
import re

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION")

f = 'faulty_data.csv'

data = pd.read_csv(f, index_col=None)
df = pd.DataFrame(data)

print("\nBefore Transformation:\n")
print(df.info())


def email_check(email):
    if pd.isna(email) or not isinstance(email, str):
        return None  
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return email if re.match(pattern, email) else None


def date_check(date):
    try:
        parsed_date = pd.to_datetime(date, format="%Y-%m-%d", errors="coerce")
        return parsed_date if pd.notna(parsed_date) else None
    except:
        return None


def age_check(age):
    if age.isdigit():
        if int(age) < 120 and int(age) > 18:
            return pd.to_numeric(age, errors="coerce")
    return None

df['Email'] = df['Email'].apply(email_check)
df['Signup Date'] = df['Signup Date'].apply(date_check)
df['Age'] = df['Age'].apply(age_check)

df.drop_duplicates()
df.dropna(subset=['Name', 'Email', 'Signup Date', 'Age'], inplace=True)

print("\nAfter Transformation:\n")
print(df.info())

df.to_csv('processed_data.csv', index=False)


try:
    bucket_name = "myfirstbucket-abbcccdddd"
    s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_DEFAULT_REGION
)

    s3.head_bucket(Bucket=bucket_name)
    print(f"Connected to S3 bucket: {bucket_name}")

    s3.upload_file('processed_data.csv', bucket_name, 'processed_data.csv')
    print(f"Uploaded processed_data.csv to {bucket_name}")
except Exception as e:
    print(f"Error: {e}")