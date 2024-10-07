# pip install streamlit fbprophet yfinance plotly
import streamlit as st
from datetime import date

import yfinance as yf
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go

START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.title('Stock Forecast App')

stocks = ("A", "AAPL", "ABBV", "ABMD", "ACN", "ADBE", "ADI", "ADM", "ADP", "ADSK", 
"AEE", "AEP", "AFL", "AIG", "AKAM", "ALB", "ALGN", "ALL", "AMAT", "AMCR", 
"AMD", "AMGN", "AMT", "AMZN", "ANET", "ANSS", "AON", "APA", "APD", "APH", 
"APTV", "ARM", "ASML", "ATVI", "AVB", "AVGO", "AVNT", "AXP", "AZN", 
"BA", "BAC", "BABA", "BAJFINANCE", "BAJAJFINSV", "BANDHANBNK", "BAX", 
"BBL", "BBWI", "BBY", "BCE", "BEP", "BFAM", "BGNE", "BHP", "BIO", 
"BIOCON", "BKR", "BLK", "BLL", "BMRN", "BMY", "BPCL", "BR", "BRK.B", 
"BSAC", "BSX", "BSY", "BUD", "BYND", "BZUN", "C", "CAJ", "CARR", 
"CAT", "CB", "CBOE", "CCI", "CCL", "CCXI", "CDNS", "CDW", "CE", 
"CEG", "CERN", "CF", "CFG", "CHD", "CHRW", "CI", "CINF", "CIPLA", 
"CL", "CLX", "CM", "CMA", "CMC", "CMCSA", "CME", "CMI", "CMS", 
"CNC", "CNI", "COF", "COIN", "COLPAL", "COP", "COST", "CP", "CPB", 
"CRH", "CRWD", "CSCO", "CSX", "CTAS", "CTLT", "CTRA", "CTSH", "CVS", 
"CVX", "DAL", "DALMIASUG", "DASH", "DD", "DE", "DG", "DGX", "DHR", 
"DIA", "DISH", "DLTR", "DMLP", "DMTK", "DOV", "DPZ", "DRE", "DRI", 
"DTE", "DUK", "DVN", "DXCM", "EA", "EBAY", "ED", "EL", "ELV", 
"EMN", "EMR", "ENB", "EOG", "EPD", "EQIX", "EQR", "EQNR", "EQT", 
"ESS", "ET", "ETN", "ETR", "EXC", "EXPD", "EXPE", "EXR", "F", 
"FAST", "FCX", "FDX", "FE", "FIS", "FISV", "FITB", "FIVE", "FLT", 
"FMX", "FND", "FNGD", "FSLR", "FTI", "FTNT", "FTV", "FUBO", "GAIL", 
"GD", "GE", "GEHC", "GEN", "GILD", "GIS", "GL", "GLBE", "GLW", 
"GME", "GMRE", "GNRC", "GO", "GOOG", "GOOGL", "GPC", "GPN", "GPS", 
"GRASIM", "GRMN", "GS", "GSK", "HAL", "HAS", "HCA", "HD", "HDB", 
"HDFC", "HDFCLIFE", "HES", "HIG", "HII", "HLT", "HOLX", "HON", "HP", 
"HPQ", "HRL", "HSBC", "HST", "HSY", "HUBS", "HUM", "HWM", "IBKR", 
"IBM", "ICE", "IDXX", "IEX", "IFF", "ILMN", "INCY", "INFY", "INTC", 
"INTU", "INVH", "IONQ", "IQV", "IR", "ISRG", "ITC", "ITW", "IVZ", 
"J", "JBHT", "JCI", "JD", "JEF", "JKHY", "JNJ", "JPM", "K", "KBH", 
"KDP", "KEY", "KEYS", "KHC", "KLAC", "KMB", "KO", "KR", "KSS", 
"KYMR", "L", "L&T", "LAC", "LAD", "LAMR", "LAZ", "LCID", "LDOS", 
"LEN", "LH", "LICI", "LIN", "LKQ", "LLY", "LMT", "LNG", "LOW", 
"LRCX", "LUMN", "LUV", "LYFT", "M", "MA", "MAR", "MAS", "MAT", 
"MATV", "MCD", "MCK", "MCO", "MDB", "MDLZ", "MDT", "MET", "META", 
"MGM", "MHCP", "MKC", "MKTX", "MLM", "MMM", "MNST", "MO", "MOS", 
"MPWR", "MRK", "MRO", "MS", "MSFT", "MSI", "MT", "MTB", "MTCH", 
"MTD", "MTN", "MU", "MUFG", "MVST", "NDAQ", "NEE", "NEM", "NFLX", 
"NGG", "NKE", "NLOK", "NLSN", "NOC", "NOV", "NOW", "NRG", "NSC", 
"NTAP", "NTES", "NTR", "NU", "NUE", "NVDA", "NVR", "NWL", "O", 
"ODFL", "OGE", "OKE", "OLN", "OMC", "ON", "ORCL", "ORLY", "OTIS", 
"OXY", "PAG", "PARA", "PAYX", "PEAK", "PENN", "PEP", "PFE", "PG", 
"PGR", "PH", "PHG", "PINS", "PLD", "PLTR", "PM", "PNC", "PNR", 
"PNW", "POOL", "PPG", "PRGO", "PRU", "PSA", "PTC", "PYPL", "QCOM", 
"QRVO", "RBLX", "RCL", "RELIANCE", "RF", "RGA", "RHI", "RIG", "RIO", 
"RIVN", "RMD", "ROK", "ROP", "ROST", "RTX", "RY", "S", "SBIN", 
"SBUX", "SCCO", "SCHW", "SCS", "SE", "SEDG", "SGEN", "SHW", "SI", 
"SID", "SIRI", "SLB", "SMFG", "SNAP", "SO", "SPLK", "SPOT", "SPWR", 
"SQ", "SRF", "SRPT", "STLD", "STX", "STZ", "SWKS", "SYY", "T", 
"TAP", "TATASTEEL", "TECHM", "TEL", "TER", "TFC", "TFX", "TGT", 
"TJX", "TMO", "TMUS", "TROW", "TSCO", "TSLA", "TSM", "TT", "TTD", 
"TWLO", "TWTR", "TXN", "TXT", "UAL", "UBER", "UHS", "ULTA", "ULTRACEMCO", 
"UNH", "UNP", "UPS", "USB", "UTZ", "V", "VEEV", "VFC", "VLO", 
"VMW", "VOD", "VRSK", "VTR", "VTRS", "VZ", "WAB", "WAL", "WAT", 
"WBA", "WBD", "WEC", "WELL", "WFC", "WHR", "WM", "WMT", "WOLF", 
"WPC", "WRB", "WY", "WYNN", "XEL", "XOM", "XYL", "YUM", "ZBH", 
"ZBRA", "ZIM", "ZM", "ZTS")

selected_stock = st.selectbox('Select dataset for prediction', stocks)

n_years = st.slider('Years of prediction:', 1, 10)
period = n_years * 365


@st.cache
def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data

	
data_load_state = st.text('Loading data...')
data = load_data(selected_stock)
data_load_state.text('Loading data... done!')

st.subheader('Raw data')
st.write(data.tail())

# Plot raw data
def plot_raw_data():
	fig = go.Figure()
	fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
	fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
	fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
	st.plotly_chart(fig)
	
plot_raw_data()

# Predict forecast with Prophet.
df_train = data[['Date','Close']]
df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

m = Prophet()
m.fit(df_train)
future = m.make_future_dataframe(periods=period)
forecast = m.predict(future)

# Show and plot forecast
st.subheader('Forecast data')
st.write(forecast.tail())
    
st.write(f'Forecast plot for {n_years} years')
fig1 = plot_plotly(m, forecast)
st.plotly_chart(fig1)

st.write("Forecast components")
fig2 = m.plot_components(forecast)
st.write(fig2)