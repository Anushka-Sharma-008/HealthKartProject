import pandas as pd
import numpy as np
from faker import Faker
import random

fake = Faker()

## Dataset-1 influencers.csv

# Define options
categories = ['Fitness', 'Beauty', 'Nutrition', 'Lifestyle', 'Tech']
platforms = ['Instagram', 'YouTube', 'Twitter']
genders = ['Male', 'Female', 'Other']

# Simulate influencers
num_influencers = 50
influencers = []

for i in range(1, num_influencers + 1):
    influencers.append({
        'id': i,
        'name': fake.name(),
        'category': random.choice(categories),
        'gender': random.choice(genders),
        'follower_count': random.randint(5000, 500000),
        'platform': random.choice(platforms)
    })

df_influencers = pd.DataFrame(influencers)
df_influencers.to_csv('influencers.csv', index=False)
df_influencers.head()

## Dataset-2 posts.csv

from datetime import datetime, timedelta

num_posts = 200
posts = []

for _ in range(num_posts):
    influencer_id = random.randint(1, num_influencers)
    date = fake.date_between(start_date='-90d', end_date='today')
    platform = df_influencers.loc[df_influencers['id'] == influencer_id, 'platform'].values[0]
    
    posts.append({
        'influencer_id': influencer_id,
        'platform': platform,
        'date': date,
        'url': fake.url(),
        'caption': fake.sentence(nb_words=6),
        'reach': random.randint(1000, 100000),
        'likes': random.randint(100, 20000),
        'comments': random.randint(10, 1000),
    })

df_posts = pd.DataFrame(posts)
df_posts.to_csv('posts.csv', index=False)
df_posts.head()

## Dataset-3 tracking_data.csv

products = ['Whey Protein', 'Multivitamin', 'Energy Drink', 'Omega 3', 'Gummies']
campaigns = ['SummerBlast', 'FitFeb', 'WellnessWave', 'ShredJuly']
sources = ['Instagram', 'YouTube', 'Twitter']

tracking = []

for _ in range(300):
    influencer_id = random.randint(1, num_influencers)
    product = random.choice(products)
    campaign = random.choice(campaigns)
    date = fake.date_between(start_date='-60d', end_date='today')
    
    tracking.append({
        'source': random.choice(sources),
        'campaign': campaign,
        'influencer_id': influencer_id,
        'user_id': fake.uuid4(),
        'product': product,
        'date': date,
        'orders': random.randint(0, 20),
        'revenue': round(random.uniform(0, 10000), 2)
    })

df_tracking = pd.DataFrame(tracking)
df_tracking.to_csv('tracking_data.csv', index=False)
df_tracking.head()

## Dataset-4 payouts.csv

basis_choices = ['post', 'order']

payouts = []
for i in range(1, num_influencers + 1):
    basis = random.choice(basis_choices)
    rate = random.randint(500, 5000) if basis == 'post' else round(random.uniform(10, 50), 2)
    orders = random.randint(5, 100)
    total_payout = rate * (10 if basis == 'post' else orders)
    
    payouts.append({
        'influencer_id': i,
        'basis': basis,
        'rate': rate,
        'orders': orders,
        'total_payout': round(total_payout, 2)
    })

df_payouts = pd.DataFrame(payouts)
df_payouts.to_csv('payouts.csv', index=False)
df_payouts.head()