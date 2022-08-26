from tweet_analysis import team_sentiment_df
import streamlit as st

st.markdown("""
<style>
.big-font {
    font-size:40px !important;
    margin-left:0;
    margin-right:0;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="big-font">NBA Twitter: Fan Happiness Ratings</h1>', unsafe_allow_html=True)
st.bar_chart(team_sentiment_df, width=1000, height=750)
st.x = 'Team'
