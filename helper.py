from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
from textblob import TextBlob
import plotly.express as px
import plotly.graph_objects as go

extract = URLExtract()

def fetch_stats(selected_user, df):
    """Fetch basic statistics for the selected user"""
    
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # fetch the number of messages
    num_messages = df.shape[0]

    # fetch the total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # fetch number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # fetch number of links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)

def most_busy_users(df):
    """Find the most active users in the group"""
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x, df

def create_wordcloud(selected_user, df):
    """Generate a word cloud for the selected user"""
    
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user, df):
    """Find the most common words used"""
    
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user, df):
    """Analyze emoji usage"""
    
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        # Use emoji.is_emoji() to check if character is an emoji
        emojis.extend([c for c in message if emoji.is_emoji(c)])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def monthly_timeline(selected_user, df):
    """Create monthly activity timeline"""
    
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user, df):
    """Create daily activity timeline"""
    
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user, df):
    """Show activity by day of week"""
    
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):
    """Show activity by month"""
    
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user, df):
    """Create activity heatmap by day and time period"""
    
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap

# Sentiment Analysis Functions

def analyze_sentiment(selected_user, df):
    """Analyze sentiment of messages"""
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    # Filter out system messages and media
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    temp = temp[temp['message'].str.len() > 2]  # Skip very short messages
    
    def get_sentiment_score(message):
        try:
            blob = TextBlob(str(message))
            return blob.sentiment.polarity
        except:
            return 0
    
    def get_sentiment_label(score):
        if score > 0.1:
            return 'Positive'
        elif score < -0.1:
            return 'Negative'
        else:
            return 'Neutral'
    
    # Calculate sentiment scores
    temp['sentiment_score'] = temp['message'].apply(get_sentiment_score)
    temp['sentiment'] = temp['sentiment_score'].apply(get_sentiment_label)
    
    return temp

def sentiment_timeline(selected_user, df):
    """Create sentiment timeline"""
    sentiment_df = analyze_sentiment(selected_user, df)
    
    # Group by date and calculate average sentiment
    daily_sentiment = sentiment_df.groupby('only_date')['sentiment_score'].mean().reset_index()
    
    return daily_sentiment

def sentiment_distribution(selected_user, df):
    """Get sentiment distribution counts"""
    sentiment_df = analyze_sentiment(selected_user, df)
    
    sentiment_counts = sentiment_df['sentiment'].value_counts()
    
    return sentiment_counts

def user_sentiment_comparison(df):
    """Compare sentiment across users"""
    # Filter out system messages
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    
    def get_sentiment_score(message):
        try:
            blob = TextBlob(str(message))
            return blob.sentiment.polarity
        except:
            return 0
    
    temp['sentiment_score'] = temp['message'].apply(get_sentiment_score)
    
    # Calculate average sentiment per user
    user_sentiment = temp.groupby('user')['sentiment_score'].agg(['mean', 'count']).reset_index()
    user_sentiment = user_sentiment[user_sentiment['count'] >= 10]  # Only users with 10+ messages
    user_sentiment = user_sentiment.sort_values('mean', ascending=False)
    
    return user_sentiment

def sentiment_by_hour(selected_user, df):
    """Analyze sentiment patterns by hour of day"""
    sentiment_df = analyze_sentiment(selected_user, df)
    
    hourly_sentiment = sentiment_df.groupby('hour')['sentiment_score'].mean().reset_index()
    
    return hourly_sentiment

def most_positive_negative_messages(selected_user, df, n=5):
    """Get most positive and negative messages"""
    sentiment_df = analyze_sentiment(selected_user, df)
    
    # Get most positive messages
    most_positive = sentiment_df.nlargest(n, 'sentiment_score')[['user', 'message', 'sentiment_score', 'date']]
    
    # Get most negative messages
    most_negative = sentiment_df.nsmallest(n, 'sentiment_score')[['user', 'message', 'sentiment_score', 'date']]
    
    return most_positive, most_negative

# NEW: Mental Health Analysis Functions

def analyze_mental_health_indicators(selected_user, df):
    """Analyze potential mental health indicators in messages"""
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    # Filter out system messages and media
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    temp = temp[temp['message'].str.len() > 3]  # Skip very short messages
    
    # First, calculate sentiment scores
    def get_sentiment_score(message):
        try:
            blob = TextBlob(str(message))
            return blob.sentiment.polarity
        except:
            return 0
    
    temp['sentiment_score'] = temp['message'].apply(get_sentiment_score)
    
    # Define keyword patterns for different mental health indicators
    anxiety_keywords = [
        'anxious', 'anxiety', 'worried', 'worry', 'nervous', 'panic', 'stress', 'stressed',
        'overthinking', 'cant sleep', "can't sleep", 'insomnia', 'restless', 'tense',
        'fear', 'scared', 'afraid', 'overwhelmed', 'pressure', 'tension'
    ]
    
    depression_keywords = [
        'depressed', 'depression', 'sad', 'sadness', 'lonely', 'alone', 'hopeless',
        'worthless', 'empty', 'numb', 'tired', 'exhausted', 'unmotivated', 'crying',
        'tears', 'hurt', 'pain', 'dark', 'heavy', 'burden', 'broken'
    ]
    
    sleep_keywords = [
        'cant sleep', "can't sleep", 'insomnia', 'sleepless', 'awake', 'tired',
        'exhausted', 'sleep', 'sleepy', 'nightmare', 'dreams'
    ]
    
    def count_keywords(message, keywords):
        message_lower = message.lower()
        return sum(1 for keyword in keywords if keyword in message_lower)
    
    # Count indicators
    temp['anxiety_indicators'] = temp['message'].apply(lambda x: count_keywords(x, anxiety_keywords))
    temp['depression_indicators'] = temp['message'].apply(lambda x: count_keywords(x, depression_keywords))
    temp['sleep_indicators'] = temp['message'].apply(lambda x: count_keywords(x, sleep_keywords))
    
    return temp

def mental_health_summary(selected_user, df):
    """Generate mental health summary statistics"""
    mh_df = analyze_mental_health_indicators(selected_user, df)
    
    total_messages = len(mh_df)
    if total_messages == 0:
        return {
            'total_messages': 0,
            'anxiety_indicators': {'count': 0, 'percentage': 0},
            'depression_indicators': {'count': 0, 'percentage': 0},
            'sleep_indicators': {'count': 0, 'percentage': 0},
            'night_messaging': {'count': 0, 'percentage': 0},
            'avg_sentiment': 0
        }
    
    anxiety_messages = len(mh_df[mh_df['anxiety_indicators'] > 0])
    depression_messages = len(mh_df[mh_df['depression_indicators'] > 0])
    sleep_messages = len(mh_df[mh_df['sleep_indicators'] > 0])
    
    # Calculate percentages
    anxiety_pct = (anxiety_messages / total_messages * 100)
    depression_pct = (depression_messages / total_messages * 100)
    sleep_pct = (sleep_messages / total_messages * 100)
    
    # Night messaging pattern (potential indicator)
    night_messages = len(mh_df[(mh_df['hour'] >= 23) | (mh_df['hour'] <= 5)])
    night_pct = (night_messages / total_messages * 100)
    
    # Average sentiment
    avg_sentiment = mh_df['sentiment_score'].mean()
    
    summary = {
        'total_messages': total_messages,
        'anxiety_indicators': {
            'count': anxiety_messages,
            'percentage': round(anxiety_pct, 1)
        },
        'depression_indicators': {
            'count': depression_messages,
            'percentage': round(depression_pct, 1)
        },
        'sleep_indicators': {
            'count': sleep_messages,
            'percentage': round(sleep_pct, 1)
        },
        'night_messaging': {
            'count': night_messages,
            'percentage': round(night_pct, 1)
        },
        'avg_sentiment': round(avg_sentiment, 2)
    }
    
    return summary

def get_mental_health_insights(selected_user, df):
    """Generate insights and recommendations based on analysis"""
    summary = mental_health_summary(selected_user, df)
    
    if summary['total_messages'] == 0:
        return {
            'insights': ["No messages found for analysis"],
            'risk_level': "Low",
            'summary': summary
        }
    
    insights = []
    risk_level = "Low"
    
    # Analyze patterns
    if summary['anxiety_indicators']['percentage'] > 15:
        insights.append("High frequency of anxiety-related expressions detected")
        risk_level = "Moderate"
    
    if summary['depression_indicators']['percentage'] > 10:
        insights.append("Frequent use of words associated with low mood")
        risk_level = "Moderate"
    
    if summary['night_messaging']['percentage'] > 25:
        insights.append("High late-night messaging activity detected")
    
    if summary['avg_sentiment'] < -0.2:
        insights.append("Overall sentiment appears consistently negative")
        risk_level = "High"
    
    if summary['sleep_indicators']['percentage'] > 8:
        insights.append("Sleep-related concerns mentioned frequently")
    
    # Combined risk assessment
    high_risk_indicators = 0
    if summary['anxiety_indicators']['percentage'] > 20:
        high_risk_indicators += 1
    if summary['depression_indicators']['percentage'] > 15:
        high_risk_indicators += 1
    if summary['avg_sentiment'] < -0.3:
        high_risk_indicators += 1
    
    if high_risk_indicators >= 2:
        risk_level = "High"
    elif high_risk_indicators >= 1 or summary['anxiety_indicators']['percentage'] > 10:
        risk_level = "Moderate"
    
    return {
        'insights': insights,
        'risk_level': risk_level,
        'summary': summary
    }

def mental_health_timeline(selected_user, df):
    """Track mental health indicators over time"""
    mh_df = analyze_mental_health_indicators(selected_user, df)
    
    if len(mh_df) == 0:
        return pd.DataFrame()
    
    # Group by date
    daily_mh = mh_df.groupby('only_date').agg({
        'anxiety_indicators': 'sum',
        'depression_indicators': 'sum',
        'sleep_indicators': 'sum',
        'sentiment_score': 'mean'
    }).reset_index()
    
    return daily_mh
