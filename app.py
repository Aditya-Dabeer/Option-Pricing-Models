from datetime import datetime, timedelta
from models import Black_Scholes, MonteCarlo, Binomial
from Asset import Asset
from option import Choices, Option

# Third party imports
import streamlit as st

st.set_page_config("Option Pricing Models")

@st.cache_data
def get_asset_price(ticker):
    """Getting historical data for speified ticker and caching it with streamlit app."""
    return Asset.get_historical_data(ticker)

# Ignore the Streamlit warning for using st.pyplot()
st.set_option('deprecation.showPyplotGlobalUse', False)

# Main title
st.title('Option pricing')

# User selected model from sidebar 
pricing_method = st.sidebar.radio('Please select option pricing method', options=[model.value for model in Choices])

# Displaying specified model
st.subheader(f'Pricing method: {pricing_method}')

if pricing_method == Choices.BLACK_SCHOLES.value:
    # Parameters for Black-Scholes model
    ticker = st.text_input('Ticker symbol', 'AAPL')
    option = st.selectbox(
    'CALL OR PUT', [ty.value for ty in Option])
    strike_price = st.number_input('Strike price', value=300)
    risk_free_rate = st.slider('Risk-free rate (%)', 0, 100, 10)
    vol = st.slider('Sigma (%)', 0, 100, 20)
    exercise_date = st.date_input('Exercise date', min_value=datetime.today() + timedelta(days=1), value=datetime.today() + timedelta(days=365))

    if st.button(f'Calculate option price for {ticker}'):
        # Getting data for selected ticker
        data = Asset.get_historical_data(ticker)
        st.write(data.tail())
        Asset.plot_data(data, ticker, 'Adj Close')
        st.pyplot()

        price = Asset.get_last_price(data, 'Adj Close') 
        risk_free_rate = risk_free_rate / 100
        vol = vol / 100
        days_to_maturity = (exercise_date - datetime.now().date()).days

        # Calculating option price
        BSM = Black_Scholes(price, strike_price, days_to_maturity, risk_free_rate, vol)
        # call_option_price = BSM.calc_price('Call Option')
        # put_option_price = BSM.calc_price('Put Option')
        option_price = BSM.calc_price(option)

        # Displaying call/put option price
        st.subheader(f'{option} option price: {option_price}')



elif pricing_method == Choices.BINOMIAL.value:
    ticker = st.text_input('Ticker symbol', 'AAPL')
    option = st.selectbox(
    'CALL OR PUT', [ty.value for ty in Option])
    strike_price = st.number_input('Strike price', value = 300)
    risk_free_rate = st.slider('Risk-free rate (%)', 0, 100, 10)
    vol = st.slider('VOL (%)', 0, 100, 20)
    exercise_date = st.date_input('Exercise date', min_value=datetime.today() + timedelta(days=1), value=datetime.today() + timedelta(days=365))
    number_of_time_steps = st.slider('Number of time steps', 1000, 100000, 10000)

    if st.button(f'Calculate option price for {ticker}'):
         # Getting data for selected ticker
        data = get_asset_price(ticker)
        st.write(data.tail())
        Asset.plot_data(data, ticker, 'Adj Close')
        st.pyplot()

        # Formating simulation parameters
        underlying = Asset.get_last_price(data, 'Adj Close') 
        risk_free_rate = risk_free_rate / 100
        volitility = vol / 100
        days_to_maturity = (exercise_date - datetime.now().date()).days

        # Calculating option price
        B = Binomial(underlying, strike_price, days_to_maturity, risk_free_rate, volitility, number_of_time_steps)
        option_price = B.calc_price(option)

        # Displaying call/put option price
        st.subheader(f'{option} option price: {option_price}')


elif pricing_method == Choices.MONTE_CARLO.value:
    ticker = st.text_input('Ticker symbol', 'AAPL')
    option = st.selectbox(
    'CALL OR PUT', [ty.value for ty in Option])
    strike_price = st.number_input('Strike price', value=300)
    risk_free_rate = st.slider('Risk-free rate (%)', 0, 100, 10)
    vol = st.slider('Sigma (%)', 0, 100, 20)
    exercise_date = st.date_input('Exercise date', min_value=datetime.today() + timedelta(days=1), value=datetime.today() + timedelta(days=365))
    number_of_simulations = st.slider('Number of simulations', 100, 100000, 10000)
    num_of_movements = st.slider('Number of price movement simulations to be visualized ', 0, int(number_of_simulations/10), 100)

    if st.button(f'Calculate option price for {ticker}'):
        # Getting data for selected ticker
        data = get_asset_price(ticker)
        st.write(data.tail())
        Asset.plot_data(data, ticker, 'Adj Close')
        st.pyplot()

        # Formating simulation parameters
        spot_price = Asset.get_last_price(data, 'Adj Close') 
        risk_free_rate = risk_free_rate / 100
        vol = vol / 100
        days_to_maturity = (exercise_date - datetime.now().date()).days

        # ESimulating stock movements
        MC = MonteCarlo(spot_price, strike_price, days_to_maturity, risk_free_rate, vol, number_of_simulations)
        MC.simulate_prices()

        # Visualizing Monte Carlo Simulation
        MC.plot_simulation_results(num_of_movements)
        st.pyplot()

        # Calculating call/put option price
        option_price = MC.calc_price(option)
        # Displaying call/put option price
        st.subheader(f'{option} option price: {option_price}')
