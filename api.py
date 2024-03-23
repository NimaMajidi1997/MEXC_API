from mexc_sdk import Spot
import pprint
import numpy as np
import matplotlib.pyplot as plt

client = Spot(api_key='***', api_secret='***')

asset= []
amount = []
value = [1]
c=0

for i in client.account_info()["balances"]:
    ##pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(i["asset"] + " = " + i["free"])
    asset.append(i["asset"])
    amount.append(float(i["free"]))
    if i["asset"] != "USDT":
        value.append(float(client.ticker_price(i["asset"]+"USDT")["price"]))
    c=c+1

arr_amo = np.array(amount)
arr_val = np.array(value)

total_val = arr_amo * arr_val
total = np.sum(total_val)
x = np.arange(c)

plt.figure(figsize=(19, 8)) 
plt.stem(x,total_val)
plt.xticks(x, asset, rotation=90, fontsize=12, ha='right')
y_min = np.min(np.array(total_val))
y_max = np.max(np.array(total_val))
plt.yticks(np.linspace(y_min, y_max, 15))
plt.ylabel('USDT')
plt.title('My Spot Holding')
plt.grid(True)
plt.tight_layout()
plt.savefig('portfolio.svg', format='svg', dpi=500)

other = []
pi = []
pi_asset = []
explode = np.zeros(c)
per_tot = (total_val / total) * 100
threshold = 1.5
filtered_numbers = [num for num in per_tot if num > threshold]
for i in range(len(per_tot)):
    if per_tot[i] <= threshold:
        other.append(per_tot[i])
    else:
        pi.append(per_tot[i])
        pi_asset.append(asset[i])

pi.append(np.sum(other))
pi_asset.append("Other")


chart_title = f"Total Holding: {np.round(total,2)} $"
fig, ax = plt.subplots(figsize=(12, 12))
ax.pie(pi, labels=pi_asset, autopct='%1.1f%%')
plt.title(chart_title, fontname='serif', fontsize=20, fontweight='bold')
plt.savefig('portfolio1.svg', format='svg', dpi=1000)
