# import streamlit as st
# import preprocessor,helper
# import matplotlib.pyplot as plt
# import seaborn as sns

# st.sidebar.title("Whatsapp Chat Analyzer")

# uploaded_file = st.sidebar.file_uploader("Choose a file")
# if uploaded_file is not None:
#     bytes_data = uploaded_file.getvalue()
#     data = bytes_data.decode("utf-8")
#     df = preprocessor.preprocess(data)

#     # fetch unique users
#     user_list = df['user'].unique().tolist()
#     user_list.remove('group_notification')
#     user_list.sort()
#     user_list.insert(0,"Overall")

#     selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)

#     if st.sidebar.button("Show Analysis"):

#         # Stats Area
#         num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user,df)
#         st.title("Top Statistics")
#         col1, col2, col3, col4 = st.columns(4)

#         with col1:
#             st.header("Total Messages")
#             st.title(num_messages)
#         with col2:
#             st.header("Total Words")
#             st.title(words)
#         with col3:
#             st.header("Media Shared")
#             st.title(num_media_messages)
#         with col4:
#             st.header("Links Shared")
#             st.title(num_links)

#         # monthly timeline
#         st.title("Monthly Timeline")
#         timeline = helper.monthly_timeline(selected_user,df)
#         fig,ax = plt.subplots()
#         ax.plot(timeline['time'], timeline['message'],color='green')
#         plt.xticks(rotation='vertical')
#         st.pyplot(fig)

#         # daily timeline
#         st.title("Daily Timeline")
#         daily_timeline = helper.daily_timeline(selected_user, df)
#         fig, ax = plt.subplots()
#         ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
#         plt.xticks(rotation='vertical')
#         st.pyplot(fig)

#         # activity map
#         st.title('Activity Map')
#         col1,col2 = st.columns(2)

#         with col1:
#             st.header("Most busy day")
#             busy_day = helper.week_activity_map(selected_user,df)
#             fig,ax = plt.subplots()
#             ax.bar(busy_day.index,busy_day.values,color='purple')
#             plt.xticks(rotation='vertical')
#             st.pyplot(fig)

#         with col2:
#             st.header("Most busy month")
#             busy_month = helper.month_activity_map(selected_user, df)
#             fig, ax = plt.subplots()
#             ax.bar(busy_month.index, busy_month.values,color='orange')
#             plt.xticks(rotation='vertical')
#             st.pyplot(fig)

#         st.title("Weekly Activity Map")
#         user_heatmap = helper.activity_heatmap(selected_user,df)
#         fig,ax = plt.subplots()
#         ax = sns.heatmap(user_heatmap)
#         st.pyplot(fig)

#         # finding the busiest users in the group(Group level)
#         if selected_user == 'Overall':
#             st.title('Most Busy Users')
#             x,new_df = helper.most_busy_users(df)
#             fig, ax = plt.subplots()

#             col1, col2 = st.columns(2)

#             with col1:
#                 ax.bar(x.index, x.values,color='red')
#                 plt.xticks(rotation='vertical')
#                 st.pyplot(fig)
#             with col2:
#                 st.dataframe(new_df)

#         # WordCloud
#         st.title("Wordcloud")
#         df_wc = helper.create_wordcloud(selected_user,df)
#         fig,ax = plt.subplots()
#         ax.imshow(df_wc)
#         st.pyplot(fig)

#         # most common words
#         most_common_df = helper.most_common_words(selected_user,df)

#         fig,ax = plt.subplots()

#         ax.barh(most_common_df[0],most_common_df[1])
#         plt.xticks(rotation='vertical')

#         st.title('Most commmon words')
#         st.pyplot(fig)

#         # emoji analysis
#         emoji_df = helper.emoji_helper(selected_user,df)
#         st.title("Emoji Analysis")

#         col1,col2 = st.columns(2)

#         with col1:
#             st.dataframe(emoji_df)
#         with col2:
#             fig,ax = plt.subplots()
#             ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
#             st.pyplot(fig)
# import streamlit as st
# import preprocessor, helper
# import matplotlib.pyplot as plt
# import seaborn as sns
# import plotly.express as px

# st.sidebar.title("Whatsapp Chat Analyzer")

# uploaded_file = st.sidebar.file_uploader("Choose a file")
# if uploaded_file is not None:
#     bytes_data = uploaded_file.getvalue()
#     data = bytes_data.decode("utf-8")
#     df = preprocessor.preprocess(data)

#     # fetch unique users
#     user_list = df['user'].unique().tolist()
#     user_list.remove('group_notification')
#     user_list.sort()
#     user_list.insert(0,"Overall")

#     selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)

#     if st.sidebar.button("Show Analysis"):

#         # Stats Area
#         num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user,df)
#         st.title("Top Statistics")
#         col1, col2, col3, col4 = st.columns(4)

#         with col1:
#             st.header("Total Messages")
#             st.title(num_messages)
#         with col2:
#             st.header("Total Words")
#             st.title(words)
#         with col3:
#             st.header("Media Shared")
#             st.title(num_media_messages)
#         with col4:
#             st.header("Links Shared")
#             st.title(num_links)

#         # SENTIMENT ANALYSIS SECTION - NEW!
#         st.title("😊 Sentiment Analysis")
        
#         col1, col2 = st.columns(2)
        
#         with col1:
#             st.subheader("Sentiment Distribution")
#             sentiment_counts = helper.sentiment_distribution(selected_user, df)
#             fig, ax = plt.subplots()
#             colors = ['#ff9999', '#66b3ff', '#99ff99']  # Red, Blue, Green
#             ax.pie(sentiment_counts.values, labels=sentiment_counts.index, autopct='%1.1f%%', colors=colors)
#             st.pyplot(fig)
        
#         with col2:
#             st.subheader("Sentiment Over Time")
#             sentiment_timeline = helper.sentiment_timeline(selected_user, df)
#             fig, ax = plt.subplots()
#             ax.plot(sentiment_timeline['only_date'], sentiment_timeline['sentiment_score'], color='purple')
#             ax.axhline(y=0, color='black', linestyle='--', alpha=0.3)
#             plt.xticks(rotation='vertical')
#             ax.set_ylabel('Sentiment Score')
#             ax.set_title('Daily Sentiment Trend')
#             st.pyplot(fig)

#         # Sentiment by Hour
#         st.subheader("Sentiment Throughout the Day")
#         hourly_sentiment = helper.sentiment_by_hour(selected_user, df)
#         fig, ax = plt.subplots()
#         ax.bar(hourly_sentiment['hour'], hourly_sentiment['sentiment_score'], color='orange', alpha=0.7)
#         ax.axhline(y=0, color='black', linestyle='--', alpha=0.3)
#         ax.set_xlabel('Hour of Day')
#         ax.set_ylabel('Average Sentiment')
#         st.pyplot(fig)

#         # User Sentiment Comparison (only for Overall)
#         if selected_user == 'Overall':
#             st.subheader("User Sentiment Comparison")
#             user_sentiment = helper.user_sentiment_comparison(df)
#             fig, ax = plt.subplots()
#             ax.barh(user_sentiment['user'], user_sentiment['mean'], color='teal')
#             ax.axvline(x=0, color='black', linestyle='--', alpha=0.3)
#             ax.set_xlabel('Average Sentiment Score')
#             st.pyplot(fig)

#         # Most Positive/Negative Messages
#         st.subheader("Extreme Sentiment Messages")
#         col1, col2 = st.columns(2)
        
#         most_positive, most_negative = helper.most_positive_negative_messages(selected_user, df)
        
#         with col1:
#             st.write("**Most Positive Messages:**")
#             for idx, row in most_positive.iterrows():
#                 st.write(f"😊 **{row['user']}**: {row['message'][:100]}..." if len(row['message']) > 100 else f"😊 **{row['user']}**: {row['message']}")
#                 st.write(f"*Score: {row['sentiment_score']:.2f} | Date: {row['date'].strftime('%Y-%m-%d')}*")
#                 st.write("---")
        
#         with col2:
#             st.write("**Most Negative Messages:**")
#             for idx, row in most_negative.iterrows():
#                 st.write(f"😔 **{row['user']}**: {row['message'][:100]}..." if len(row['message']) > 100 else f"😔 **{row['user']}**: {row['message']}")
#                 st.write(f"*Score: {row['sentiment_score']:.2f} | Date: {row['date'].strftime('%Y-%m-%d')}*")
#                 st.write("---")

#         # monthly timeline
#         st.title("Monthly Timeline")
#         timeline = helper.monthly_timeline(selected_user,df)
#         fig,ax = plt.subplots()
#         ax.plot(timeline['time'], timeline['message'],color='green')
#         plt.xticks(rotation='vertical')
#         st.pyplot(fig)

#         # daily timeline
#         st.title("Daily Timeline")
#         daily_timeline = helper.daily_timeline(selected_user, df)
#         fig, ax = plt.subplots()
#         ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
#         plt.xticks(rotation='vertical')
#         st.pyplot(fig)

#         # activity map
#         st.title('Communication Behavior Analysis')
#         col1,col2 = st.columns(2)

#         with col1:
#             st.header("Most busy day")
#             busy_day = helper.week_activity_map(selected_user,df)
#             fig,ax = plt.subplots()
#             ax.bar(busy_day.index,busy_day.values,color='purple')
#             plt.xticks(rotation='vertical')
#             st.pyplot(fig)

#         with col2:
#             st.header("Most busy month")
#             busy_month = helper.month_activity_map(selected_user, df)
#             fig, ax = plt.subplots()
#             ax.bar(busy_month.index, busy_month.values,color='orange')
#             plt.xticks(rotation='vertical')
#             st.pyplot(fig)

#         st.title("Weekly Activity Map")
#         user_heatmap = helper.activity_heatmap(selected_user,df)
#         fig,ax = plt.subplots()
#         ax = sns.heatmap(user_heatmap)
#         st.pyplot(fig)

#         # finding the busiest users in the group(Group level)
#         if selected_user == 'Overall':
#             st.title('Most Busy Users')
#             x,new_df = helper.most_busy_users(df)
#             fig, ax = plt.subplots()

#             col1, col2 = st.columns(2)

#             with col1:
#                 ax.bar(x.index, x.values,color='red')
#                 plt.xticks(rotation='vertical')
#                 st.pyplot(fig)
#             with col2:
#                 st.dataframe(new_df)

#         # WordCloud
#         st.title("Wordcloud")
#         df_wc = helper.create_wordcloud(selected_user,df)
#         fig,ax = plt.subplots()
#         ax.imshow(df_wc)
#         st.pyplot(fig)

#         # most common words
#         most_common_df = helper.most_common_words(selected_user,df)

#         fig,ax = plt.subplots()

#         ax.barh(most_common_df[0],most_common_df[1])
#         plt.xticks(rotation='vertical')

#         st.title('Most commmon words')
#         st.pyplot(fig)

#         # emoji analysis
#         emoji_df = helper.emoji_helper(selected_user,df)
#         st.title("Emoji Analysis")

#         col1,col2 = st.columns(2)

#         with col1:
#             st.dataframe(emoji_df)
#         with col2:
#             fig,ax = plt.subplots()
#             ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
#             st.pyplot(fig)


















































import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.sidebar.title("InsightAid")

uploaded_file = st.sidebar.file_uploader("Upload your chat export to analyze anxiety patterns")
if st.sidebar.button("📖 Learn how to export chats", help="Click to learn how to export your WhatsApp chat"):
    st.sidebar.markdown("[📱 How to Export WhatsApp Chat →](https://faq.whatsapp.com/1180414079177245/?cms_platform=web)")
    st.sidebar.info("💡 Tip: Export without media for faster processing")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Analyze anxiety patterns for:",user_list)

    if st.sidebar.button("Run Anxiety Analysis"):

        # Stats Area
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user,df)
        st.title("Communication Pattern Overview")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)

        # NEW: MENTAL HEALTH ANALYSIS SECTION
        st.title("🧠 Mental Health Insights")
        
        if selected_user != 'Overall':
            # Get mental health analysis
            mh_insights = helper.get_mental_health_insights(selected_user, df)
            
            # Risk Level Indicator
            col1, col2 = st.columns([1, 2])
            with col1:
                risk_color = {"Low": "🟢", "Moderate": "🟡", "High": "🔴"}[mh_insights['risk_level']]
                st.metric("Risk Level", f"{risk_color} {mh_insights['risk_level']}")
            
            with col2:
                st.subheader("Key Indicators")
                summary = mh_insights['summary']
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Anxiety Indicators", f"{summary['anxiety_indicators']['percentage']}%")
                with col_b:
                    st.metric("Mood Indicators", f"{summary['depression_indicators']['percentage']}%")
                with col_c:
                    st.metric("Sleep Concerns", f"{summary['sleep_indicators']['percentage']}%")
            
            # Insights and Recommendations
            if mh_insights['insights']:
                st.subheader("⚠️ Patterns Detected")
                for insight in mh_insights['insights']:
                    st.write(f"• {insight}")
                
                st.subheader("💡 Recommendations")
                if mh_insights['risk_level'] == "High":
                    st.warning("Consider reaching out to a mental health professional or trusted friend for support.")
                elif mh_insights['risk_level'] == "Moderate":
                    st.info("Pay attention to stress levels and consider self-care activities.")
                else:
                    st.success("Mental health indicators appear stable.")
            
            # Mental Health Timeline
            st.subheader("Mental Health Trends Over Time")
            mh_timeline = helper.mental_health_timeline(selected_user, df)
            if len(mh_timeline) > 1:
                fig, ax = plt.subplots(figsize=(12, 6))
                ax2 = ax.twinx()
                
                # Plot indicators as bars
                ax.bar(mh_timeline['only_date'], mh_timeline['anxiety_indicators'], 
                       alpha=0.7, color='red', label='Anxiety Indicators')
                ax.bar(mh_timeline['only_date'], mh_timeline['depression_indicators'], 
                       alpha=0.7, color='blue', label='Mood Indicators', bottom=mh_timeline['anxiety_indicators'])
                
                # Plot sentiment as line
                ax2.plot(mh_timeline['only_date'], mh_timeline['sentiment_score'], 
                        color='green', linewidth=2, label='Sentiment Score')
                ax2.axhline(y=0, color='black', linestyle='--', alpha=0.3)
                
                ax.set_ylabel('Mental Health Indicators Count')
                ax2.set_ylabel('Average Sentiment Score')
                ax.set_xlabel('Date')
                ax.legend(loc='upper left')
                ax2.legend(loc='upper right')
                plt.xticks(rotation=45)
                plt.tight_layout()
                st.pyplot(fig)
        else:
            st.info("Select a specific user to view mental health insights.")

        # SENTIMENT ANALYSIS SECTION
        st.title("😊 Emotional State Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Sentiment Distribution")
            sentiment_counts = helper.sentiment_distribution(selected_user, df)
            fig, ax = plt.subplots()
            colors = ['#ff9999', '#66b3ff', '#99ff99']  # Red, Blue, Green
            ax.pie(sentiment_counts.values, labels=sentiment_counts.index, autopct='%1.1f%%', colors=colors)
            st.pyplot(fig)
        
        with col2:
            st.subheader("Sentiment Over Time")
            sentiment_timeline = helper.sentiment_timeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.plot(sentiment_timeline['only_date'], sentiment_timeline['sentiment_score'], color='purple')
            ax.axhline(y=0, color='black', linestyle='--', alpha=0.3)
            plt.xticks(rotation='vertical')
            ax.set_ylabel('Sentiment Score')
            ax.set_title('Daily Sentiment Trend')
            st.pyplot(fig)

        # Sentiment by Hour
        st.subheader("Sentiment Throughout the Day")
        hourly_sentiment = helper.sentiment_by_hour(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(hourly_sentiment['hour'], hourly_sentiment['sentiment_score'], color='orange', alpha=0.7)
        ax.axhline(y=0, color='black', linestyle='--', alpha=0.3)
        ax.set_xlabel('Hour of Day')
        ax.set_ylabel('Average Sentiment')
        st.pyplot(fig)

        # User Sentiment Comparison (only for Overall)
        if selected_user == 'Overall':
            st.subheader("Comparison of User's Emotional States")
            user_sentiment = helper.user_sentiment_comparison(df)
            fig, ax = plt.subplots()
            ax.barh(user_sentiment['user'], user_sentiment['mean'], color='teal')
            ax.axvline(x=0, color='black', linestyle='--', alpha=0.3)
            ax.set_xlabel('Average Sentiment Score')
            st.pyplot(fig)

        # Most Positive/Negative Messages
        st.subheader("Extreme Sentiment Messages")
        col1, col2 = st.columns(2)
        
        most_positive, most_negative = helper.most_positive_negative_messages(selected_user, df)
        
        with col1:
            st.write("**Most Positive Messages:**")
            for idx, row in most_positive.iterrows():
                st.write(f"😊 **{row['user']}**: {row['message'][:100]}..." if len(row['message']) > 100 else f"😊 **{row['user']}**: {row['message']}")
                st.write(f"*Score: {row['sentiment_score']:.2f} | Date: {row['date'].strftime('%Y-%m-%d')}*")
                st.write("---")
        
        with col2:
            st.write("**Most Negative Messages:**")
            for idx, row in most_negative.iterrows():
                st.write(f"😔 **{row['user']}**: {row['message'][:100]}..." if len(row['message']) > 100 else f"😔 **{row['user']}**: {row['message']}")
                st.write(f"*Score: {row['sentiment_score']:.2f} | Date: {row['date'].strftime('%Y-%m-%d')}*")
                st.write("---")

        # monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.title('Communication Behavior Analysis')
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # finding the busiest users in the group(Group level)
        if selected_user == 'Overall':
            st.title('Most socially active users')
            x,new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # WordCloud
        st.title("Language Pattern Analysis")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        most_common_df = helper.most_common_words(selected_user,df)

        fig,ax = plt.subplots()

        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')

        st.title('Most repeated words')
        st.pyplot(fig)

        # emoji analysis
        emoji_df = helper.emoji_helper(selected_user,df)
        st.title("Emotional Expression Through Emojis")

        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)
