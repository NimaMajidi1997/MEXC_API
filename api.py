from mexc_sdk import Spot
import pprint
import numpy as np
import matplotlib.pyplot as plt
import datetime

client = Spot(api_key='API_KEY', api_secret='API_SECRET')
date = datetime.date.today()
current_date = date.strftime("%Y-%m-%d")
asset= []
amount = []
value = []
c=0

for i in client.account_info()["balances"]:
    asset.append(i["asset"])
    amount.append(float(i["free"]))
    if i["asset"] == "USDT":
        value.append(1.0)
    else:
        value.append(float(client.ticker_price(i["asset"]+"USDT")["price"]))
    c=c+1

asset_sorted = sorted(asset)
amount_sorted = [x for _, x in sorted(zip(asset, amount))]
value_sorted = [x for _, x in sorted(zip(asset, value))]
#pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(asset_sorted)
#pp.pprint(amount_sorted)
#pp.pprint(value_sorted)


arr_amo = np.array(amount_sorted)
arr_val = np.array(value_sorted)

total_val = arr_amo * arr_val
total = np.sum(total_val)
x = np.arange(c)

plt.figure(figsize=(19, 8)) 
plt.stem(x,total_val)
plt.xticks(x, asset_sorted, rotation=90, fontsize=9, ha='right')
y_min = np.min(np.array(total_val))
y_max = np.max(np.array(total_val))
plt.yticks(np.linspace(y_min, y_max, 45))
plt.ylabel('USDT')
chart_title = f"{current_date}    Holding: {np.round(total,2)}$"
plt.title(chart_title, fontname='serif', fontsize=15, fontweight='bold')
plt.grid(True)
plt.tight_layout()
fig_1 = '/mnt/c/Users/z004v63a/Documents/Images/portfolio/' + current_date + '.svg'
plt.savefig(fig_1, format='svg', dpi=1000)

other = []
pi = []
pi_asset = []
explode = np.zeros(c)
per_tot = (total_val / total) * 100
threshold = 1.19
filtered_numbers = [num for num in per_tot if num > threshold]
for i in range(len(per_tot)):
    if per_tot[i] <= threshold:
        other.append(per_tot[i])
    else:
        pi.append(per_tot[i])
        pi_asset.append(asset_sorted[i])

pi.append(np.sum(other))
pi_asset.append("Other")

pi_asset_sorted = sorted(pi_asset)
pi_sorted = [x for _, x in sorted(zip(pi_asset,pi))]

np.random.seed(123)
num_colors = len(pi_sorted)
random_colors = ['#%06x' % np.random.randint(0, 0xFFFFFF) for _ in range(num_colors)]


chart_title = f"{current_date}    Holding: {np.round(total,2)}$"
fig, ax = plt.subplots(figsize=(11, 11))
ax.pie(pi_sorted, labels=pi_asset_sorted, autopct='%1.1f%%',colors=random_colors, textprops={'fontsize': 9})
plt.title(chart_title, fontname='serif', fontsize=18, fontweight='bold')
fig_2 = '/mnt/c/Users/z004v63a/Documents/Images/pi_chart/' + current_date + '.svg'
plt.savefig(fig_2, format='svg', dpi=1000)
