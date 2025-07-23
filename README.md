# 🏋️‍♀️ HealthKart Influencer Campaign Dashboard | Data Analytics Project

This Streamlit-based interactive dashboard helps **track and analyze the performance of influencer marketing campaigns** at HealthKart across platforms like Instagram, YouTube, and Twitter.  
It offers **ROI estimation, performance insights, payout tracking, and chatbot-based queries**—all powered by simulated campaign data.

🔗 **Live Dashboard:** [Click here to explore the deployed dashboard](https://healthkartproject.streamlit.app/)  

<img src="assets/preview_1.png">

---

## ✨ Features

- 📊 Interactive **multi-page Streamlit dashboard**
- 👥 Influencer filtering by platform, category, and product
- 📈 **Campaign overview** with KPIs like Revenue, ROAS, Orders
- 💰 **Payout tracker** with post/order-based calculation
- 🔮 **ROI forecasting** using regression
- 🤖 Inbuilt **natural-language chatbot**
- 🧪 Realistic **data simulation using Faker**

---

## 🧰 Technologies Used

| Category          | Technology / Library      | Purpose                                      |
|------------------|---------------------------|----------------------------------------------|
| 💻 Frontend       | `Streamlit`               | Interactive UI for dashboard                 |
| 📊 Visualization  | `Plotly Express`          | Graphs, charts, and plots                    |
| 🧮 Modeling       | `Scikit-learn`            | Simple regression for ROI forecasting        |
| 📦 Data Handling  | `Pandas`, `NumPy`         | Data cleaning, merging, and transformation   |
| 🤖 NLP/Chatbot    | `Regex`, basic logic      | Intent-based rule matching for chatbot       |
| 🧪 Data Creation  | `Faker`, `random`         | Simulate realistic influencer campaign data  |
| 🐍 Language       | `Python 3.x`              | Core programming language                    |

---

## 🔍 How It Works

This dashboard uses **simulated datasets** representing influencers, posts, tracking data, and payouts.  
Users can navigate through five main pages:

1. **Campaign Overview:** Platform-wide KPIs, product revenue, and ROAS distribution.
2. **Influencer Insights:** Breakdown of performance by influencer with pie charts.
3. **Payout Tracker:** View how payouts are distributed based on posts/orders.
4. **Forecast ROI:** Predict ROI based on follower count and engagement.
5. **Chatbot:** Ask natural-language questions like "Top influencers by ROAS".

Filtering options are available in the sidebar to slice data by platform, category, and product.

---

## 📷 Preview

![Page1](assets/preview_1.png)
![Page2](assets/preview_2.png)
![Page3](assets/preview_3.png)
![Page4](assets/preview_4.png)
![Page5](assets/preview_5.png)

---

## 📁 Folder Structure
```
HealthKartProject/
├── README.md                  # Project overview and usage guide
├── Project_documentation.pdf            # Full project documentation/report
├── data/                      # Simulated datasets
│   ├── data_simulation.py
│   ├── influencers.csv
│   ├── posts.csv
│   ├── payouts.csv
│   └── tracking_data.csv
├── app.py                 # Main dashboard script
├── chatbot.py             # Chatbot logic and data interface
├── assets/                # Visuals and assets
│   ├── preview_1.png      # Preview of Page 1   
│   ├── preview_2.png      # Preview of Page 2   
│   ├── preview_3.png      # Preview of Page 3   
│   ├── preview_4.png      # Preview of Page 4   
│   ├── preview_5.png      # Preview of Page 5   
│   └── healthkart_logo.png   # Logo of the brand
└── requirements.txt           # Python dependencies
```

---

## 💡 Use Cases

- 💼 For **marketing teams** to measure influencer ROI
- 📊 For **data analysts** to derive campaign insights
- 🧑‍💻 For **students** learning data visualization & Streamlit
- 🧪 For **simulation & experimentation** without real campaign data

---

## ⚙️ Setup Instructions

1. **Clone this Repository**
   ```bash
   git clone https://github.com/Anushka-Sharma-008/HealthKartProject.git
   cd healthkart-dashboard
   ```
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Simulate data**
   ```bash
   python data_simulation.py
   ```
4. **Run the Dashboard**
   ```bash
   streamlit run app.py
   ```

---

## 📎 Project Documentation

Full project documentation is available in the attached PDF:  
📄 [Click here to view the full project documentation (PDF)](./Project_documentation.pdf)

---

## 🧾 Assumptions Made

- Influencer payout basis is either **per post** or **per order**
- Campaigns, products, and platforms are predefined (simulated)
- ROAS = Revenue / Total Payout (with NaN and ∞ handled)
- Forecast model is **simple linear regression** based only on followers
- One influencer can have multiple posts and campaign entries
- Data is synthesized using `Faker` and does not represent actual HealthKart campaigns

---

## 📊 Insights Summary

- 💰 **Total Revenue:** Derived from tracking data across campaigns
- 🧑‍🤝‍🧑 **Top Influencers:** Identified by highest ROAS and total orders
- 💸 **Cost Efficiency:** Campaign ROAS varies widely by platform
- 📦 **Product Insights:** Certain products drive significantly higher revenue
- 🛠️ **Chatbot Utility:** Offers quick query handling for common business questions

---

## 🙋‍♀️ Author

**Anushka Sharma**  
🌐 [LinkedIn](https://www.linkedin.com/in/anushkasharma008/) • 🐱 [GitHub](https://github.com/Anushka-Sharma-008) 
🎓 Learning Data Science, Analytics & Machine Learning

---

## ⭐ Show Your Support

If you found this project helpful or inspiring:

- ⭐ Star this repository  
- 🛠️ Fork it to build upon or adapt it for your own use  
- 💬 Share feedback or suggestions via Issues/Discussions
