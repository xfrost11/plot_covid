import pandas as pd
import pylab as plt
import os

cdf = pd.read_csv(r'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv')

pdf = pd.read_excel(r'population.xlsx')

pdf_fixed = pdf[pdf['COUNTY'] != 0]

mdf = pd.merge(cdf, pdf_fixed, 
            left_on=['state', 'county'],
            right_on=['STNAME', 'CTYNAME'],
            how='inner')

mdf.to_csv('out.csv')

mdf['per_100k'] = mdf['cases'] / mdf['POPESTIMATE2019'] * 100000

print (mdf)

states = mdf['state'].unique()

for state in states:
    state_path = os.path.join('plots', state)
    if not os.path.exists(state_path):
        os.mkdir(state_path)
    state_df = mdf[mdf['state'] == state]
    counties = state_df['county'].unique()
    for county in counties:
        ymin = 0
        ymax = 15
        county_df = state_df[state_df['county'] == county]
        county_df['per_100k_ra'] = county_df['per_100k'].rolling(7).mean()
        county_df['new_cases'] = county_df['per_100k'].diff()
        county_df['new_cases_ra'] = county_df['new_cases'].rolling(7).mean()
        county_path = os.path.join(state_path, county)

        print (county_path)

        ax = plt.gca()

        county_df.plot(x='date', y='new_cases', ax=ax)
        county_df.plot(x='date', y='new_cases_ra', ax=ax)
        plt.title(f'{state} - {county}')

        plt.xlabel('')

        plt.xticks(rotation =45, fontsize='small')
        xmin, xmax = plt.xlim()  
        ymin_T, ymax_T = plt.ylim()
        ymax = max(ymax, ymax_T)
        

        plt.ylim(ymin, ymax)
        
        
        plt.axhspan(7, ymax, color = "purple", alpha = 0.5)
        plt.axhspan(4, 7, color = "red", alpha = 0.5)
        plt.axhspan(1, 4, color = "orange", alpha = 0.5)
        plt.axhspan(ymin, 1, color = "yellow", alpha = 0.5)

        plt.ylabel('Cases per 100k')

        plt.grid()
        
        plt.savefig(f'{county_path}.png')        
        # plt.show()
        plt.clf()
        county_df.to_csv(f'{county_path}.csv')
    
    



    
    
