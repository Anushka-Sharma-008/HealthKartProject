import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np
import base64

# Set page config
st.set_page_config(page_title="HealthKart Influencer Dashboard", layout="wide")

# Function to display logo
def add_logo_header(image_path="healthkart_logo.png", width=120):
    with open(image_path, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data).decode()

    st.markdown(
        f"""
        <div style="display: flex; justify-content: flex-end; align-items: center; padding: 10px 20px 0 0;">
            <img src="data:image/png;base64,{encoded}" width="{width}">
        </div>
        """,
        unsafe_allow_html=True
    )

# Load data
influencers = pd.read_csv("data/influencers.csv")
posts = pd.read_csv("data/posts.csv")
payouts = pd.read_csv("data/payouts.csv")
tracking_data = pd.read_csv("data/tracking_data.csv")

# Clean column names
for df in [influencers, posts, payouts, tracking_data]:
    df.columns = df.columns.str.strip().str.lower()
    df['influencer_id'] = df['influencer_id'].astype(str)

# Sidebar filters
st.sidebar.header("🔍 Filters")
products = ['All'] + sorted(tracking_data['product'].dropna().unique().tolist())
platforms = ['All'] + sorted(influencers['platform'].dropna().unique().tolist())
categories = ['All'] + sorted(influencers['category'].dropna().unique().tolist())

selected_product = st.sidebar.selectbox("Select Product", products)
selected_platform = st.sidebar.selectbox("Select Platform", platforms)
selected_category = st.sidebar.selectbox("Select Influencer Category", categories)

# Apply filters
filtered_influencers = influencers.copy()
if selected_platform != 'All':
    filtered_influencers = filtered_influencers[filtered_influencers['platform'] == selected_platform]
if selected_category != 'All':
    filtered_influencers = filtered_influencers[filtered_influencers['category'] == selected_category]

filtered_tracking = tracking_data[tracking_data['influencer_id'].isin(filtered_influencers['influencer_id'])]
if selected_product != 'All':
    filtered_tracking = filtered_tracking[filtered_tracking['product'] == selected_product]

# Merge data
merged = filtered_tracking.merge(filtered_influencers, on='influencer_id', how='left')
merged = merged.merge(payouts[['influencer_id', 'total_payout']], on='influencer_id', how='left')
merged = merged.merge(posts[['influencer_id', 'likes', 'comments', 'reach']], on='influencer_id', how='left')

merged['revenue'] = merged['revenue'].fillna(0)
merged['orders'] = merged['orders'].fillna(0)
merged['total_payout'] = merged['total_payout'].fillna(0)
merged['roas'] = merged['revenue'] / merged['total_payout']
merged['roas'] = merged['roas'].replace([np.inf, -np.inf], 0).fillna(0)

# Tabs as pages
page = st.sidebar.radio("Go to", ["Campaign Overview", "Influencer Insights", "Payout Tracker", "Forecast ROI", "Chatbot"])

# --- Page 1: Campaign Overview ---
if page == "Campaign Overview":
    add_logo_header("assets\healthkart_logo.png")  # ✅ Shows logo + title header on all pages
    st.title("📊 Campaign Overview")

    tracking_data['date'] = pd.to_datetime(tracking_data['date'])
    merged['month'] = pd.to_datetime(merged['date']).dt.to_period('M')
    months = merged['month'].astype(str).unique().tolist()
    selected_month = st.selectbox("Select Month", ['All'] + months)

    campaigns = merged['campaign'].dropna().unique().tolist()
    selected_campaign = st.selectbox("Select Campaign", ['All'] + list(campaigns))

    if selected_month != 'All':
        merged = merged[merged['month'].astype(str) == selected_month]
    if selected_campaign != 'All':
        merged = merged[merged['campaign'] == selected_campaign]

    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📸 Total Posts", f"{posts.shape[0]:,}")
    col2.metric("💰 Revenue", f"₹{int(merged['revenue'].sum()):,}")
    col3.metric("📦 Orders", f"{int(merged['orders'].sum()):,}")
    col4.metric("📈 Avg ROAS", f"{round(merged['roas'].mean(), 2)}x")

    st.subheader("📈 Revenue by Product")
    if not merged.empty:
        fig = px.bar(
            merged.groupby('product')['revenue'].sum().reset_index(),
            x='product', y='revenue',
            color='product',
            color_discrete_sequence=px.colors.qualitative.Set2,
            title='💸 Revenue Distribution by Product'
        )
        fig.update_layout(xaxis_title="", yaxis_title="Revenue", title_x=0.5)
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("📉 ROAS by Platform")
    fig2 = px.box(merged, x='platform', y='roas', points="all", color='platform')
    fig2.update_layout(title='📊 ROAS by Platform', title_x=0.5)
    st.plotly_chart(fig2, use_container_width=True)

# --- Page 2: Influencer Insights ---
elif page == "Influencer Insights":
    add_logo_header("assets\healthkart_logo.png")  # ✅ Shows logo + title header on all pages
    st.title("👥 Influencer Insights")

    summary = merged.groupby(['influencer_id', 'name', 'platform', 'category']).agg({
        'revenue': 'sum',
        'orders': 'sum',
        'total_payout': 'sum',
        'roas': 'mean',
        'likes': 'mean',
        'comments': 'mean',
        'reach': 'mean'
    }).reset_index()

    col1, col2, col3 = st.columns(3)
    col1.metric("📈 Avg ROAS", f"{round(summary['roas'].mean(), 2)}x")
    col2.metric("📦 Total Orders", f"{int(summary['orders'].sum()):,}")
    col3.metric("💸 Total Payout", f"₹{int(summary['total_payout'].sum()):,}")

    st.subheader("📊 Influencer Revenue Contribution")
    fig3 = px.pie(summary, values='revenue', names='name', title='🎯 Revenue Share by Influencer')
    st.plotly_chart(fig3, use_container_width=True)

    with st.expander("📋 Show Full Influencer Breakdown"):
        st.dataframe(summary.sort_values(by='revenue', ascending=False), use_container_width=True)

# --- Page 3: Payout Tracker ---
elif page == "Payout Tracker":
    add_logo_header("assets\healthkart_logo.png")  # ✅ Shows logo + title header on all pages
    st.title("💰 Payout Tracker")

    payout_data = influencers.merge(payouts, on='influencer_id', how='left')

    platforms_filter = ['All'] + sorted(payout_data['platform'].dropna().unique())
    categories_filter = ['All'] + sorted(payout_data['category'].dropna().unique())

    selected_platform_pt = st.selectbox("Filter by Platform", platforms_filter)
    selected_category_pt = st.selectbox("Filter by Category", categories_filter)

    if selected_platform_pt != 'All':
        payout_data = payout_data[payout_data['platform'] == selected_platform_pt]
    if selected_category_pt != 'All':
        payout_data = payout_data[payout_data['category'] == selected_category_pt]

    payout_data['total_payout'] = payout_data['total_payout'].fillna(0)

    with st.expander("📄 Show Payout Table"):
        st.dataframe(payout_data[['name', 'platform', 'category', 'basis', 'rate', 'orders', 'total_payout']], use_container_width=True)

# --- Page 4: Forecast ROI ---
elif page == "Forecast ROI":
    add_logo_header("assets\healthkart_logo.png")  # ✅ Shows logo + title header on all pages
    st.title("🔮 Forecast ROI")
    platform = st.selectbox("Select Platform", platforms[1:])
    followers = st.slider("Follower Count (in thousands)", 1, 1000, 100)
    engagement_rate = st.slider("Engagement Rate (%)", 0, 100, 10)

    X = influencers[['follower_count']].fillna(0)
    y = payouts['total_payout'].fillna(0)
    model = LinearRegression()
    model.fit(X, y)

    predicted_payout = model.predict([[followers * 1000]])[0]
    predicted_roi = round((engagement_rate / 100) * predicted_payout * 0.5, 2)

    st.success(f"📌 Estimated ROI: ₹{predicted_roi:,}")
    st.caption("*Note: Based on a simple regression model; not reflective of all factors.")

# --- Page 5: Chatbot ---
elif page == "Chatbot":
    add_logo_header("assets\healthkart_logo.png")  # ✅ Shows logo + title header on all pages
    st.title("🤖 Chatbot")
    from chatbot import chatbot_response

    st.markdown("<h2>Ask Me Anything</h2>", unsafe_allow_html=True)
    st.markdown("Ask questions like:")
    st.markdown("- What was the total revenue?")
    st.markdown("- Who are the top influencers by ROAS?")
    st.markdown("- Recommend influencers with over 50K followers on Instagram in fitness.")

    user_input = st.text_input("Ask your question:")

    if user_input:
        response = chatbot_response(user_input)
        st.text_area("Bot Response:", response, height=200)


# Footer
st.markdown("---")
st.caption("Built with ❤️ by Anushka Sharma | Powered by Streamlit")
