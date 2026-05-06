import hashlib
import pandas as pd
import streamlit as st

st.set_page_config(page_title='Oasis Retail Dashboard', layout='wide')


@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Country'] = df['Customer ID'].apply(assign_country)
    df['Total Amount'] = pd.to_numeric(df['Total Amount'], errors='coerce')
    return df


@st.cache_data
def assign_country(customer_id):
    countries = [
        'United States', 'Canada', 'United Kingdom', 'Germany',
        'France', 'Australia', 'Spain', 'Netherlands'
    ]
    key = int(hashlib.sha256(customer_id.encode('utf-8')).hexdigest(), 16)
    return countries[key % len(countries)]


@st.cache_data
def compute_customer_profiles(df):
    today = df['Date'].max() + pd.Timedelta(days=1)
    rfm = df.groupby('Customer ID').agg(
        recency=('Date', lambda x: (today - x.max()).days),
        frequency=('Transaction ID', 'count'),
        monetary=('Total Amount', 'sum'),
        first_purchase=('Date', 'min'),
        last_purchase=('Date', 'max'),
        country=('Country', 'first')
    ).reset_index()
    rfm['avg_order_value'] = rfm['monetary'] / rfm['frequency']
    rfm['recency_score'] = pd.qcut(rfm['recency'], 5, labels=[
                                   5, 4, 3, 2, 1]).astype(int)
    rfm['frequency_score'] = pd.qcut(rfm['frequency'].rank(
        method='first'), 5, labels=[1, 2, 3, 4, 5]).astype(int)
    rfm['monetary_score'] = pd.qcut(rfm['monetary'], 5, labels=[
                                    1, 2, 3, 4, 5]).astype(int)
    rfm['rfm_score'] = rfm['recency_score'] + \
        rfm['frequency_score'] + rfm['monetary_score']
    rfm['segment'] = rfm.apply(label_segment, axis=1)
    return rfm


@st.cache_data
def label_segment(row):
    if row['rfm_score'] >= 13:
        return 'Champion'
    if row['rfm_score'] >= 10:
        return 'Loyal Customer'
    if row['rfm_score'] >= 8:
        return 'Potential Loyalist'
    if row['rfm_score'] >= 6:
        return 'At Risk'
    return 'Needs Attention'


@st.cache_data
def summarize_business(df):
    revenue = df['Total Amount'].sum()
    customers = df['Customer ID'].nunique()
    transactions = len(df)
    aov = revenue / transactions if transactions else 0
    return_rate = 0.0
    repeat_rate = (df.groupby('Customer ID')[
                   'Transaction ID'].count() > 1).mean() * 100
    daily_revenue = df.set_index('Date').resample('W')['Total Amount'].sum()
    revenue_by_country = df.groupby(
        'Country')['Total Amount'].sum().sort_values(ascending=False)
    top_products = df.groupby('Product Category')[
        'Total Amount'].sum().sort_values(ascending=False)
    return {
        'revenue': revenue,
        'customers': customers,
        'aov': aov,
        'return_rate': return_rate,
        'repeat_rate': repeat_rate,
        'daily_revenue': daily_revenue,
        'revenue_by_country': revenue_by_country,
        'top_products': top_products,
    }


@st.cache_data
def get_recommendation(segment):
    if segment == 'Champion':
        return 'Offer VIP rewards, exclusive bundles, and early access to new releases.'
    if segment == 'Loyal Customer':
        return 'Send a loyalty discount and recommend premium products in their favorite categories.'
    if segment == 'Potential Loyalist':
        return 'Encourage repeat purchases with a targeted offer on top categories.'
    if segment == 'At Risk':
        return 'Re-engage with a personalized promo and remind them of their best-loved items.'
    return 'Send a win-back offer and suggest products similar to their previous purchases.'


@st.cache_data
def get_customer_details(df, customer_id):
    customer_df = df[df['Customer ID'] == customer_id].copy()
    if customer_df.empty:
        return None
    country = customer_df['Country'].iloc[0]
    first_purchase = customer_df['Date'].min()
    last_purchase = customer_df['Date'].max()
    total_revenue = customer_df['Total Amount'].sum()
    transaction_count = customer_df['Transaction ID'].nunique()
    aov = total_revenue / transaction_count if transaction_count else 0
    products = customer_df.groupby('Product Category')[
        'Total Amount'].sum().sort_values(ascending=False)
    categories = customer_df['Product Category'].value_counts()
    return {
        'country': country,
        'first_purchase': first_purchase,
        'last_purchase': last_purchase,
        'total_revenue': total_revenue,
        'transaction_count': transaction_count,
        'avg_order_value': aov,
        'top_products': products,
        'category_counts': categories,
    }


# Load data
DATA_PATH = 'retail_sales_dataset.csv'
df = load_data(DATA_PATH)
customer_rfm = compute_customer_profiles(df)
summary = summarize_business(df)

st.markdown('# Oasis Retail Dashboard')
page = st.sidebar.radio('Select dashboard page', [
                        'Business Overview', 'Customer RFM Analysis'])

if page == 'Business Overview':
    st.markdown('## Business Overview')
    st.markdown(
        'A high-level snapshot of revenue, customer behavior, and product performance.')

    col1, col2, col3, col4 = st.columns(4)
    col1.metric('Revenue', f'${summary["revenue"]:,.0f}')
    col2.metric('Customers', f'{summary["customers"]:,}')
    col3.metric('AOV', f'${summary["aov"]:,.2f}')
    col4.metric('Return Rate', f'{summary["return_rate"]:.1f}%')

    st.markdown('### Revenue & Customer Insights')
    insight1, insight2 = st.columns(2)
    insight1.write('**Repeat purchase rate**')
    insight1.write(
        f'{summary["repeat_rate"]:.1f}% of customers have purchased more than once.')
    insight2.write('**Top product category**')
    insight2.write(
        f'{summary["top_products"].index[0]} with ${summary["top_products"].iloc[0]:,.0f} revenue.')

    st.markdown('### Revenue Trend')
    st.line_chart(summary['daily_revenue'])

    st.markdown('### Geographic Revenue Analysis')
    st.bar_chart(summary['revenue_by_country'])

    st.markdown('### Product Performance')
    top_products = summary['top_products'].head(10)
    st.bar_chart(top_products)

    st.markdown('### Product Category Revenue')
    category_revenue = df.groupby('Product Category')[
        'Total Amount'].sum().sort_values(ascending=False)
    st.bar_chart(category_revenue)

else:
    st.markdown('## Customer RFM Analysis')
    st.markdown(
        'Search for a customer to see their segment, financial summary, and purchase behavior.')

    customer_options = customer_rfm['Customer ID'].sort_values().tolist()
    selected_customer = st.selectbox('Select customer', customer_options)
    if selected_customer:
        profile = customer_rfm[customer_rfm['Customer ID']
                               == selected_customer].iloc[0]
        details = get_customer_details(df, selected_customer)

        st.subheader(f'Customer {selected_customer}')
        st.markdown(f'**Segment:** {profile.segment}')
        st.info(get_recommendation(profile.segment))

        summary_cols = st.columns(3)
        summary_cols[0].metric('Location', details['country'])
        summary_cols[1].metric(
            'Total Revenue', f'${details["total_revenue"]:,.0f}')
        summary_cols[2].metric('AOV', f'${details["avg_order_value"]:,.2f}')

        stats_cols = st.columns(3)
        stats_cols[0].metric('Transactions', details['transaction_count'])
        stats_cols[1].metric(
            'First Purchase', details['first_purchase'].strftime('%Y-%m-%d'))
        stats_cols[2].metric(
            'Last Purchase', details['last_purchase'].strftime('%Y-%m-%d'))

        st.markdown('### Top Products Purchased')
        st.bar_chart(details['top_products'].head(8))

        st.markdown('### Product Categories Purchased')
        st.bar_chart(details['category_counts'].head(8))

        st.markdown('### Segment details')
        st.write(
            'This view highlights the customer’s purchase frequency, monetary value, and recency to determine a meaningful segment for personalized outreach.'
        )
