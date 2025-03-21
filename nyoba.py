import gdown
import pandas as pd

# Daftar ID file dari Google Drive
file_id = [
    "19t0PyBIgMO7ZxzQlcLRr0pMQk5B5G1VC",
    "1oYy-uUOfAWThLnYP8x0FjLj8Nbpndq3Y",
    "11QB0O9-R7NJi4fVU8yELCqbQ7SWX-7K-",
    "1iarrW5V2FKfUDF2hZrBGam1FXs30Eg3Y",
    "1z-cZD2r6UdfKsac-YrODNzYzFo-swcrC",
    "1oxmU3TVyTsL967nlR5aQQKymfmOldxlS",
    "12Qum7pbdtma1KW0RNlup726DUkSfjhPl",
    "15hZUOK0fu1-XqdZ8uZ8OGSp_GLhIFTbB",
    "1QjhNVSRIDhbwEB9N89ob093gSRmzrlvV"
]

# Mengunduh file dengan nama output1.csv, output2.csv, ...
for idx, file in enumerate(file_id, start=1):
    url = f"https://drive.google.com/uc?id={file}"
    output = f"output{idx}.csv"
    print(f"Mengunduh {output} dari {url}...")
    gdown.download(url, output, quiet=False)

# Membaca file CSV ke dalam dataframe
seller_df = pd.read_csv("output1.csv")
product_df = pd.read_csv("output2.csv")
translate_df = pd.read_csv("output3.csv")
orders_df = pd.read_csv("output4.csv")
review_df = pd.read_csv("output5.csv")
payment_df = pd.read_csv("output6.csv")
item_df = pd.read_csv("output7.csv")
geolocation_df = pd.read_csv("output8.csv")
customers_df = pd.read_csv("output9.csv")
customers_df.head()