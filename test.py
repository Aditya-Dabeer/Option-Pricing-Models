from models import Black_Scholes
from Asset import Asset

BSM = Black_Scholes(139.15, 50.00, 363, 0.681,0.1384)
print(BSM.calc_price("Call Option"))

print(Asset.get_historical_data("TSLA"))
data = Asset.get_historical_data("TSLA")
Asset.plot_data(data, "TSLA", "Close")