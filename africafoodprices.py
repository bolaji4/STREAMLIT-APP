import numpy as np
import pandas as pd
import seaborn as sns
import plotly.express as px
from scipy import stats
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import altair as alt

print('installation is ready')


# get the data

#@st.cache # it save the data to the browser.
def get_data():
    url = ('./datasets/africa_food_prices.csv')
    df = pd.read_csv(url)
    all_cols = ['Unnamed: 0', 'country_id', 'country', 'state_id', 'state', 'market_id',
       'market', 'produce_id', 'produce', 'currency_id', 'currency', 'pt_id',
       'market_type', 'um_unit_id', 'quantity', 'month', 'year', 'price',
       'mp_commoditysource'],

      
    cols_to_drop = ['country_id','state_id',
                    'currency_id','pt_id',
                    'mp_commoditysource']
    df = df.drop(columns=cols_to_drop)
    new_names = {'Unname: 0': 'bags_produce',
            'country': 'country',
            'state': 'state',
            'market_id': 'mkt_id',
            'market': 'mkt_name',
            'produce_id': 'pd_id',
            'market_type': 'producer',
            'um_unit_id': 'measurement_id',
            'quantity': 'weight',
            'month':'month_recorded',
            'year':'year_recorded',
            'price':'price_paid'}
    df = df.rename(columns=new_names)
    df = df.drop(columns=df.columns[0])
    return df
# display the result using python
print(get_data())

#title
st.write("# Africa Food Prices App")

#df # magic command and is actually == st.write(df)



#to clean the data now we will need to take it to jupiterlab and reajust it
# sidebar
with st.container():
    
    try:
        st.sidebar.header("User input controls") # what ever 
        df = get_data()
        country = st.sidebar.multiselect("Choose country",df.country.unique(),"Algeria") #,#"Algeria" you can put a defult value and u must make sure it is in the list
        produce = st.sidebar.selectbox("Choose produce",df.produce.unique())  
        state = st.sidebar.selectbox("Choose state",df.state.unique())
    # error checking
   
        if not country:
            st.sidebar.error("Please select at least one country")
        else:
            for i, index in enumerate(country):
                data = df[df.country == country[i]]
                st.write(f"### Prices of Goods in {country[i]} country")
                st.write(data.head(60))
      #pass .. this is use to pass in function if to show if not select
    # using the data let's build a line chart
    # we build a pivot table
                pvt = pd.pivot_table(data, index=['country','state','mkt_name','produce','year_recorded'],values=['price_paid'], aggfunc='mean')
                pvt_df = pvt.reset_index()
                pvt_df
                selected_country = country[i]
                st.write(selected_country)
                pvt_df = pvt_df[pvt_df['country'] == selected_country]
    # selected product
                selected_produce = produce
                selected_state = state
                pvt_df = pvt_df[pvt_df["produce"] == selected_produce]
    #line chart
                chart = alt.Chart(pvt_df).mark_area().encode(
                x='year_recorded', y='price_paid', tooltip=['mkt_name','price_paid'])
                st.write(f"### Price Chart {selected_produce} in {selected_country}")
                st.altair_chart(chart, use_container_width=True)
    # area chart for different markets
                                
                chart = alt.Chart(pvt_df).mark_area().encode(
                x='year_recorded', y='price_paid', tooltip=['mkt_name', 'price_paid'])
                st.write(f"### Price Chart {selected_produce} in {selected_country}")
                st.altair_chart(chart, use_container_width=True)
    # area chart with different market
                chart = alt.Chart(pvt_df).mark_area().encode(
                x='year_recorded', color='mkt_name', y='price_paid', tooltip=['year_recorded','price_paid']).interactive()
                st.write(f"### Price Chart {selected_produce} in {selected_country}")
                st.altair_chart(chart, use_container_width=True)
                st.write("-----")
    except RuntimeError as e: # try and except
        st.error(e.reason)
