import pandas as pd
import numpy as np
import re

# Load data
influencers = pd.read_csv("data/influencers.csv")
posts = pd.read_csv("data/posts.csv")
payouts = pd.read_csv("data/payouts.csv")
tracking_data = pd.read_csv("data/tracking_data.csv")

# Clean column names and ensure proper types
for df in [influencers, posts, payouts, tracking_data]:
    df.columns = df.columns.str.strip().str.lower()
    df['influencer_id'] = df['influencer_id'].astype(str)

# Preprocess merged data
merged = tracking_data.merge(influencers, on='influencer_id', how='left')
merged = merged.merge(payouts[['influencer_id', 'total_payout']], on='influencer_id', how='left')
merged = merged.merge(posts[['influencer_id', 'likes', 'comments', 'reach']], on='influencer_id', how='left')

merged['revenue'] = merged['revenue'].fillna(0)
merged['orders'] = merged['orders'].fillna(0)
merged['total_payout'] = merged['total_payout'].fillna(0)
merged['roas'] = merged['revenue'] / merged['total_payout']
merged['roas'] = merged['roas'].replace([np.inf, -np.inf], 0).fillna(0)

def chatbot_response(user_input: str) -> str:
    if not user_input:
        return "Please enter a question."

    query = user_input.lower()

    if "total revenue" in query:
        revenue = int(merged['revenue'].sum())
        return f"🧾 Total revenue is ₹{revenue:,}"

    elif "top influencers" in query and "roas" in query:
        top = merged.groupby(['name'])['roas'].mean().sort_values(ascending=False).head(5)
        return "🏆 Top Influencers by ROAS:\n" + "\n".join([f"{i+1}. {name} ({round(roas,2)}x)" for i, (name, roas) in enumerate(top.items())])

    elif "recommend influencers" in query:
        platform_match = re.search(r"on (instagram|youtube|twitter)", query)
        platform = platform_match.group(1).capitalize() if platform_match else None

        cat_match = re.search(r"in (\w+)", query)
        category = cat_match.group(1).capitalize() if cat_match else None

        count_match = re.search(r"over (\d+)[kK] followers", query)
        min_followers = int(count_match.group(1)) * 1000 if count_match else 0

        df = influencers.copy()
        if platform:
            df = df[df['platform'] == platform]
        if category:
            df = df[df['category'].str.lower() == category.lower()]
        if min_followers:
            df = df[df['follower_count'] >= min_followers]

        if not df.empty:
            return "📢 Recommended Influencers:\n" + "\n".join(df['name'].head(5))
        else:
            return "No influencers match that criteria."

    else:
        return "❓ Sorry, I didn't understand. Try asking about revenue, ROAS, or recommendations."
