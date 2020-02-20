import importlib
import subprocess
import sys


def getpack(package,installname = None):
    if installname is None:
        installname = package
    try:
        # import package
        return importlib.import_module(package)
    except ImportError:
        # install package
        subprocess.call([sys.executable, "-m", "pip", "install", installname],stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)
        # import package
        return importlib.import_module(package)


fredapi = getpack("fredapi")
from fredapi import Fred
fred = Fred(api_key=open("./apikey.txt").readlines()[0].strip())
yf = getpack("yfinance")


class Indicator:

    def __init__(self, name, data, description, frequency, unit, source):
        self.name = name
        self.data = data
        self.descr = description
        self.freq = frequency
        self.unit = unit
        self.src = source

    def copy(self):
        return Indicator(self.name, self.data, self.descr, self.freq, self.unit, self.src)

    def __repr__(self):
        return f"Class: Indicator\nName: {self.name}\nDescription: {self.descr}\nFrequency: {self.freq}\nUnit: {self.unit}" \
            f"\nSource: {self.src}"

    def __str__(self):
        return f"Name: {self.name}\n{self.data}\nDescription: {self.descr}\nFrequency: {self.freq}" \
            f"\nSource: {self.src}"


class LeadingEconIndic:
    
    def __init__(self):

        SP_data = yf.Ticker("^GSPC").history(period="max").iloc[:,3]
        self.sp500 = Indicator("SP500", SP_data, "Daily", "Points", "SP500 Index", "Yahoo Finance.")

        self.leadind_index = Indicator("Leading Index for the United States", fred.get_series('USSLIND'), "The leading "
            "index, includes variables that lead the economy: state-level housing permits (1 to 4 units), state initial "
            "unemployment insurance claims, delivery times from the Institute for Supply Management (ISM) manufacturing "
            "survey, and the interest rate spread between the 10-year Treasury bond and the 3-month Treasury bill.",
            "Monthly", "Percent", "Federal Reserve Bank of Philadelphia, retrieved from FRED;"
                                  " https://fred.stlouisfed.org/series/USSLIND.")

        self.t10yr_fedfunds = Indicator("10-Year Treasury Constant Maturity Minus Federal Funds Rate",
            fred.get_series('T10YFF'), "Series is calculated as the spread between 10-Year Treasury Constant Maturity "
            "(BC_10YEAR) and Effective Federal Funds Rate.", "Daily", "Percent", "Federal Reserve Bank of St. Louis; "
            "https://fred.stlouisfed.org/series/T10YFF.")

        sent = fred.get_series('UMCSENT')
        self.consumer_sentiment = Indicator("Consumer Sentiment", sent[sent.index >= "1978-01-01"], "University of Michigan: "
            "Consumer Sentiment Index", "Monthly", "Index 1966:Q1=100", "University of Michigan, retrieved from FRED;"
                                                                        " https://fred.stlouisfed.org/series/UMCSENT.")

        self.manu_goods_ord = Indicator("Value of Manufacturers' New Orders for All Manufacturing Industries", fred.get_series('AMTMNO'),
            "Data on New Orders for the Semiconductor Industry are not available.", "Monthly", "Million of Dollars", "U.S. Census Bureau, retrieved from FRED;"
            " https://fred.stlouisfed.org/series/AMTMNO.")

        self.manu_goods_ship = Indicator("Value of Manufacturers' Shipments for All Manufacturing Industries", fred.get_series('AMTMVS'),
            "Estimates of Shipments for the semiconductor industry are no longer shown separately, but are included in Computers "
            "and Electronic Products industry and in all other applicable aggregate totals.", "Monthly", "Million of Dollars", "U.S. Census Bureau, retrieved from FRED"
            "; https://fred.stlouisfed.org/series/AMTMVS.")

        self.manu_goods_inv = Indicator("Value of Manufacturers' Total Inventories for All Manufacturing Industries",
            fred.get_series('AMTMTI'), "Estimates of Shipments for the semiconductor industry are no longer shown separately, "
            "but are included in Computers and Electronic Products industry and in all other applicable aggregate totals.",
            "Monthly", "Million of Dollars", "U.S. Census Bureau, retrieved from FRED; https://fred.stlouisfed.org/series/AMTMT.")

        self.building_perm = Indicator("New Private Housing Units Authorized by Building Permits", fred.get_series('PERMIT'),
            "Thousands of Units, Seasonally Adjusted Annual Rate", "Monthly", "Thousands of Units", "U.S. Census Bureau, retrieved from FRED;"
            " https://fred.stlouisfed.org/series/PERMIT.")

        self.init_unempl_claim = Indicator("Initial Unemployment Claims", fred.get_series('ICSA'), "Unemployment insurance "
            "weekly claims report ending saturday", "Weekly", "Number", "U.S. ETA, retrieved from FRED; https://fred.stlouisfed.org/series/ICSA.")

        self.avg_wweek_hrs = Indicator("Average Weekly Hours of All Employees, Total Private", fred.get_series('AWHAETP'),
            "Average weekly hours relate to the average hours per worker for which pay was received and is different from "
            "standard or scheduled hours. Factors such as unpaid absenteeism, labor turnover, part-time work, and stoppages "
            "cause average weekly hours to be lower than scheduled hours of work for an establishment. Group averages further "
            "reflect changes in the workweek of component industries. Average weekly hours are the total weekly hours divided "
            "by the employees paid for those hours.", "Monthly", "Hours", "U.S. BLS, retrieved from FRED; https://fred.stlouisfed.org/series/AWHAETP.")

        self.avg_hrly_earn = Indicator("Average Hourly Earnings of Production and Nonsupervisory Employees, Total Private",
            fred.get_series('AHETPI'), "Production and related employees include working supervisors and all nonsupervisory "
            "employees (including group leaders and trainees) engaged in fabricating, processing, assembling, inspecting, "
            "receiving, storing, handling, packing, warehousing, shipping, trucking, hauling, maintenance, repair, janitorial, "
            "guard services, product development, auxiliary production for plant's own use (for example, power plant), recordkeeping, "
            "and other services closely associated with the above production operations. Nonsupervisory employees include "
            "those individuals in private, service-providing industries who are not above the working-supervisor level. "
            "This group includes individuals such as office and clerical workers, repairers, salespersons, operators, drivers, "
            "physicians, lawyers, accountants, nurses, social workers, research aides, teachers, drafters, photographers, "
            "beauticians, musicians, restaurant workers, custodial workers, attendants, line installers and repairers, laborers, "
            "janitors, guards, and other employees at similar occupational levels whose services are closely associated with those "
            "of the employees listed.", "Monthly", "Dollars per Hour", "U.S. BLS, retrieved from FRED; https://fred.stlouisfed.org/series/AHETPI.")

        self.unempl_rate = Indicator("Unemployment Rate", fred.get_series('UNRATE'), "The unemployment rate represents the "
            "number of unemployed as a percentage of the labor force. Labor force data are restricted to people 16 years of age "
            "and older, who currently reside in 1 of the 50 states or the District of Columbia, who do not reside in institutions "
            "(e.g., penal and mental facilities, homes for the aged), and who are not on active duty in the Armed Forces.",
            "Monthly", "Percent", "U.S. BLS, Unemployment Rate from FRED; https://fred.stlouisfed.org/series/UNRATE.")

        self.m2 = Indicator("M2 Money Stock", fred.get_series('M2'), "M2 includes a broader set of financial assets held "
            "principally by households. M2 consists of M1 plus: (1) savings deposits (which include money market deposit "
            "accounts, or MMDAs); (2) small-denomination time deposits (time deposits in amounts of less than $100,000); "
            "and (3) balances in retail money market mutual funds (MMMFs). Seasonally adjusted M2 is computed by summing "
            "savings deposits, small-denomination time deposits, and retail MMMFs, each seasonally adjusted separately, "
            "and adding this result to seasonally adjusted M1.", "Weekly", "Billions of Dollars", "Board of Governors of the Federal Reserve "
            "System (US), retrieved from FRED; https://fred.stlouisfed.org/series/M2.")

        self.non_def_cap_goods_ord = Indicator("Value of Manufacturers' New Orders for Capital Goods: Nondefense Capital "
            "Goods Industries", fred.get_series('ANDENO'), "This series is a topical regrouping of the separate industry "
            "categories. Nondefense capital goods industries include: small arms and ordnance; farm machinery and equipment; "
            "construction machinery; mining, oil, and gas field machinery; industrial machinery.", "Monthly",
            "Million of Dollars", "U.S. Census Bureau, retrieved from FRED; https://fred.stlouisfed.org/series/ANDENO.")

        self.non_def_cap_goods_ship = Indicator("Value of Manufacturers' Shipments for Capital Goods: Nondefense Capital Goods Industries",
            fred.get_series('ANDEVS'), "This series is a topical regrouping of the separate industry categories. Nondefense "
            "capital goods industries include: small arms and ordnance; farm machinery and equipment; construction machinery; "
            "mining, oil, and gas field machinery; industrial machinery; vending, laundry, and other machinery; photographic "
            "equipment; metalworking machinery; turbines and generators; other power transmission equipment; pumps and "
            "compressors; material handling equipment; all other machinery; electronic computers; computer storage devices; "
            "other computer peripheral equipment; communications equipment; search and navigation equipment; electromedical, "
            "measuring, and control instruments; electrical equipment; other electrical equipment, appliances, and components; "
            "heavy duty trucks; aircraft; railroad rolling stock; ships and boats; office and institutional furniture; and medical "
            "equipment and supplies.", "Monthly", "Million of Dollars", "U.S. Census Bureau, retrieved from FRED; "
            "https://fred.stlouisfed.org/series/ANDEVS.")

        self.non_def_cap_goods_inv = Indicator(" Value of Manufacturers' Total Inventories for Capital Goods: Nondefense "
            "Capital Goods Industries", fred.get_series('ANDETI'), "This series is a topical regrouping of the separate "
            "industry categories. Nondefense capital goods industries include: small arms and ordnance; farm machinery and "
            "equipment; construction machinery; mining, oil, and gas field machinery; industrial machinery; vending, laundry, "
            "and other machinery; photographic equipment; metalworking machinery; turbines and generators; other power transmission equipment; "
            "pumps and compressors; material handling equipment; all other machinery; electronic computers; computer storage "
            "devices; other computer peripheral equipment; communications equipment; search and navigation equipment; "
            "electromedical, measuring, and control instruments; electrical equipment; other electrical equipment, appliances, "
            "and components; heavy duty trucks; aircraft; railroad rolling stock; ships and boats; office and institutional "
            "furniture; and medical equipment and supplies.", "monthly", "Million of Dollars", "U.S. Census Bureau, retrieved from FRED;"
            " https://fred.stlouisfed.org/series/ANDETI.")

        self.rec_dates = Indicator("NBER based Recession Indicators for the United States from the Period following the "
            "Peak through the Trough", fred.get_series('USREC'), "This time series is an interpretation of US Business "
            "Cycle Expansions and Contractions data provided by The National Bureau of Economic Research (NBER). Our time "
            "series is composed of dummy variables that represent periods of expansion and recession. The NBER identifies "
            "months and quarters of turning points without designating a date within the period that turning points occurred. "
            "The dummy variable adopts an arbitrary convention that the turning point occurred at a specific date within the period. "
            "The arbitrary convention does not reflect any judgment on this issue by the NBER's Business Cycle Dating Committee. "
            "A value of 1 is a recessionary period, while a value of 0 is an expansionary period. For this time series, the recession "
            "begins the first day of the period following a peak and ends on the last day of the period of the trough. For more options "
            "on recession shading, see the notes and links below. The recession shading data that we provide initially comes from the "
            "source as a list of dates that are either an economic peak or trough. We interpret dates into recession shading data "
            "using one of three arbitrary methods. All of our recession shading data is available using all three interpretations. "
            "The period between a peak and trough is always shaded as a recession. The peak and trough are collectively extrema. "
            "Depending on the application, the extrema, both individually and collectively, may be included in the recession period "
            "in whole or in part. In situations where a portion of a period is included in the recession, the whole period is deemed "
            "to be included in the recession period. The first interpretation, known as the midpoint method, is to show a recession "
            "from the midpoint of the peak through the midpoint of the trough for monthly and quarterly data. For daily data, "
            "the recession begins on the 15th of the month of the peak and ends on the 15th of the month of the trough. "
            "Daily data is a disaggregation of monthly data. For monthly and quarterly data, the entire peak and trough "
            "periods are included in the recession shading. This method shows the maximum number of periods as a recession "
            "for monthly and quarterly data. The Federal Reserve Bank of St. Louis uses this method in its own publications. "
            "One version of this time series is represented using the midpoint method The second interpretation, known as the "
            "trough method, is to show a recession from the period following the peak through the trough (i.e. the peak is "
            "not included in the recession shading, but the trough is). For daily data, the recession begins on the first "
            "day of the first month following the peak and ends on the last day of the month of the trough. Daily data is "
            "a disaggregation of monthly data. The trough method is used when displaying data on FRED graphs. The trough "
            "method is used for this series. The third interpretation, known as the peak method, is to show a recession "
            "from the period of the peak to the trough (i.e. the peak is included in the recession shading, but the trough "
            "is not). For daily data, the recession begins on the first day of the month of the peak and ends on the last "
            "day of the month preceding the trough. Daily data is a disaggregation of monthly data. Here is an example of "
            "this time series represented using the peak method.", "Monthly", "+1 or 0", "Federal Reserve Bank of St. Louis, NBER "
            "based Recession Indicators; https://fred.stlouisfed.org/series/USREC.")

    def __repr__(self):
        return "U.S. leading economic indicators: "+', '.join("%s: %s" % i for i in vars(self).items())

    def __print__(self):
        return repr(self)
