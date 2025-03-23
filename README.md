# Introduction

Car auctions are a popular way to purchase vehicles at prices lower than market value. At one point, I considered buying a BMW F30 from an auction but found myself uncertain about the average price, the best locations to purchase from, and other key factors. Lacking knowledge about the auction process, I decided to leverage my data analysis skills to better understand how BMW vehicles perform in auctions.


### **Note:**
Since plotly graphs cannot be displayed on github, I have uploaded snapshots of these visualizations.

To view all graphs, you can use NBViewer (https://nbviewer.org/) by pasting the following link(link to notebook file from github): https://github.com/Yaroslav1405/carAuctionAnalysis/blob/main/carAuctionAnalysis.ipynb

or using this link to google colab: https://colab.research.google.com/drive/1IzE2xKaOSzfxkePk8GN8Ff6U9wmj6VBE?usp=sharing


# Project Overview
This project was implemented using Python frameworks such as BeautifulSoup, Selenium, Pandas, Matplotlib, Seaborn, Plotly, and SkLearn. The data was scrapped from bid.cars/en/. During the process and at the analysis stage, the structure of pages has changed, so scrapping code may no longer function as expected. The dataset contains 1280 samples.

# Main Stages 
1. Learning Web Scraping Techniques:
Before this project, I had no prior experience with web scraping. I only had some knowledge in Python, and Google search. Initially, I explored different approaches and found that BeautifulSoup was widely used. The first roadblock happened when it was time to pass captcha on the website. This issue led me to discover Selenium, which greatly improved my ability to navigate and extract data. By combining Selenium, BeautifulSoup (where applicable), Pandas, and visualization tools, I developed an effective workflow for data extraction.

2. Scrapping the data:
The website structure changed multiple times during the project, requiring a complete overhaul of the scraping script. 

* Optimized Data Collection Process:
    - Implemented a reverse for-loop logic, reducing unnecessary requests by checking only the lot numbers of 50 vehicles per iteration.
    - Each iteration served as a checkpoint, saving progress to a CSV file to prevent data loss.
* Error Handling & Data Integrity Issues:
    - Some listings displayed "Log in to see the final bid" instead of a numerical price, causing errors in list indexing.
    - The scraping process incorrectly extracted document details instead of damage information due to HTML class conflicts.
    - Implemented manual inspections and exception handling to resolve inconsistencies.

3. Data Analysis Approach: 
Initially, my attempt at analysis was unfocused, as I generated multiple graphs without a clear direction. To improve this, I redefined my goals: 
* Key Questions:
    - Best Locations for Vehicles: Determine which states or locations offer the best vehicles based on average price, year, and mileage.

    - Best Day to Purchase a Vehicle: Analyze trends to identify the most favorable day for buying a vehicle.

    - Auction Bidding vs. Buy Now Option: Assess whether bidding at auctions provides better deals compared to the "Buy Now" option.

    - Optimal Trim-Year-Mileage-Price Combination: Identify the best balance of trim, year, mileage, and price.

    - Condition vs. Mileage Correlation: Examine whether higher mileage reduces the likelihood of a vehicle being in a "Run and Drive" condition.

    - Correlation Analysis: Explore relationships between damage, trim, mileage, and price to understand their impact on vehicle valuation.
By refining my objectives, I structured my analysis more effectively and gained deeper insights.I suggest reading more about working on data preprocessing and data analysis on the notebook file or through the nbviewer (to see it with graphs).

# Conclusion
Conclusion section on data analysis can also be found in the notebook file. Overally, this project significantly improved my skills in web scraping, data analysis, and visualization, allowing me to extract meaningful insights from real-world auction data. This is the big step up in my analytics road, as now I will be able to acquire data from the sources that really interest me. While I ultimately did not purchase a BMW F30, this analysis helped me successfully acquire another vehicle through an auction.

# Future Improvements
To enhance this analysis, future work could include:
* Expanding the Dataset: Scraping additional data would allow for more detailed insights, particularly on vehicle trim options.
* Refining Damage Analysis: Conducting separate analyses on specific damage categories (e.g., Run and Drive vs. Static cars) for more precise evaluations.
* Automating Updates: Implementing a more robust scraping approach that adapts to website structure changes dynamically.
This project serves as a foundation for understanding vehicle auction trends and can be expanded to analyze other brands and auction platforms in the future.