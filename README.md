# LeadingEconomicIndicatorsUS

*Disclaimer: This product uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis.*

- lei.py comiles a series of leading economic indicators in the U.S. using a custom class and subclass. The indicators have been lifted from the [Conference Board](https://en.wikipedia.org/wiki/Conference_Board_Leading_Economic_Index). Sources for them are listed below.

- Visualistions.ipynb visualizes the data, the executed notebook can be found as Visualistions.html


### Sources

United States department of labor:
    
    - Monthly:
        * Unemployment rate (UNRATE - https://fred.stlouisfed.org/series/UNRATE),
        * Average hourly earnings (AHETPI - https://fred.stlouisfed.org/series/AHETPI) and
        * Average workweek hours (AWHAETP - https://fred.stlouisfed.org/series/AWHAETP) 
    
    
    - Weekly:
        * Initial unemployment claims (ICSA - https://fred.stlouisfed.org/series/ICSA)

United States Census Bureau:

    - Monthly:
        * Manufacturers' Shipments (AMTMVS - https://fred.stlouisfed.org/series/AMTMVS)
        * Manufacturers' Inventories (AMTMTI - https://fred.stlouisfed.org/series/AMTMTI)
        * Manufacturers' Orders (AMTMNO - https://fred.stlouisfed.org/series/AMTMNO)
    
        * Manufacturers' non-defense capital goods Inventories (ANDETI - https://fred.stlouisfed.org/series/ANDETI)
        * Manufacturers' non-defense capital goods Shipments (ANDEVS - https://fred.stlouisfed.org/series/ANDEVS)
        * Manufacturers' non-defense capital goods Orders (ANDENO - https://fred.stlouisfed.org/series/ANDENO)
    
        * Building Permits (PERMIT - https://fred.stlouisfed.org/series/PERMIT)

Federal reserve:

    - 10-year Treasury minus federal funds rate (T10YFF - https://fred.stlouisfed.org/series/T10YFF)
    
    - Inflation-adjusted M2 money supply (M2 - https://fred.stlouisfed.org/series/M2)

S&P500

    - https://fred.stlouisfed.org/series/SP500

University of Michigan Consumer Sentiment Index
    
    - UMCSENT - https://fred.stlouisfed.org/series/UMCSENT


Leading Index

    - (USSLIND - https://fred.stlouisfed.org/graph/?g=l1a)
    
    
Recession dates:
    - USREC - https://fred.stlouisfed.org/series/USREC
