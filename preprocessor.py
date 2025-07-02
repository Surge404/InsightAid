import re
import pandas as pd
from datetime import datetime

def preprocess(data):
    # More flexible pattern to catch various date formats
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    
    # Very flexible date parsing
    def parse_date_flexible(date_str):
        # Remove the trailing " - " 
        clean_date = date_str.strip().rstrip(' -').strip()
        
        # Try different formats
        formats_to_try = [
            '%d/%m/%Y, %H:%M',  # 4-digit year
            '%d/%m/%y, %H:%M',  # 2-digit year
            '%m/%d/%Y, %H:%M',  # US format 4-digit
            '%m/%d/%y, %H:%M',  # US format 2-digit
        ]
        
        for fmt in formats_to_try:
            try:
                return datetime.strptime(clean_date, fmt)
            except ValueError:
                continue
        
        # If all specific formats fail, let pandas try to infer
        try:
            return pd.to_datetime(clean_date, dayfirst=True)
        except:
            # Last resort - return current time (shouldn't happen with valid WhatsApp exports)
            print(f"Warning: Could not parse date '{date_str}', using current time")
            return datetime.now()
    
    # Apply the flexible date parsing
    df['message_date'] = df['message_date'].apply(parse_date_flexible)
    df['message_date'] = pd.to_datetime(df['message_date'])

    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df
