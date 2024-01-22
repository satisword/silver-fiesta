import os

import matplotlib.pyplot as plt
import pandas as pd
import requests
from bs4 import BeautifulSoup

output_directory = "./data"


def get_data_from_wikipedia():
    print("No CSV file found, creating one...")

    # URL of the Wikipedia page with the data
    url = "https://en.wikipedia.org/wiki/List_of_aspect_ratios_of_national_flags"

    # Get the HTML content of the page and parse it
    response = requests.get(url, timeout=4)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the table
    table = soup.find("table", {"class": "wikitable"})

    # Iterate over each row in the table
    flag_data = []
    for row in table.find_all("tr")[1:]:  # Skip the header row
        cols = row.find_all("td")
        if cols:
            country = cols[1].text.strip()
            aspect_ratio = cols[2].text.strip()
            # The aspect ratio is in the format "1:2 (0.5)"
            # so just a little bit of string manipulation to get the double
            aspect_ratio = aspect_ratio[
                aspect_ratio.find("(") + 1 : aspect_ratio.find(")")
            ]
            flag_data.append({"country": country, "aspect_ratio": aspect_ratio})

    # Save the data to a CSV file
    pd.DataFrame(flag_data).to_csv(f"{output_directory}/flag_data.csv", index=False)


def main():
    # Check if the CSV file exists so we don't have to scrape the data again
    if not os.path.exists(f"{output_directory}/flag_data.csv"):
        get_data_from_wikipedia()
    else:
        print("Flag CSV file found!")
        print("Reading CSV, and plotting...")

    # Read the CSV file
    flag_df = pd.read_csv(f"{output_directory}/flag_data.csv")

    # Plot the most common aspect ratios
    plt.figure(figsize=(15, 6))
    flag_df["aspect_ratio"].value_counts().head(10).plot(kind="bar")

    plt.ylabel("Number of flags")
    plt.xlabel("Aspect ratio")
    plt.title("Most common aspect ratios of national flags")

    # Save and show the plot
    if not os.path.exists("flag_aspect_ratios.png"):
        plt.savefig("flag_aspect_ratios.png", dpi=600)
    else:
        print("Flag aspect ratio plot found!")
        print("Showing plot...")

    plt.show()


if __name__ == "__main__":
    main()
