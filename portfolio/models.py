from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Ticker(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    symbol = models.CharField(max_length=20)
    zip = models.CharField(max_length=50, null=True, blank=True)
    sector = models.CharField(max_length=255, null=True, blank=True)
    fullTimeEmployees = models.IntegerField(null=True, blank=True)
    longBusinessSummary = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    address1 = models.CharField(max_length=255, null=True, blank=True)
    industry = models.CharField(max_length=255, null=True, blank=True)
    previousClose = models.FloatField(null=True, blank=True)
    regularMarketOpen = models.FloatField(null=True, blank=True)
    twoHundredDayAverage = models.FloatField(null=True, blank=True)
    trailingAnnualDividendYield = models.FloatField(null=True, blank=True)
    payoutRatio = models.FloatField(null=True, blank=True)
    volume24Hr = models.IntegerField(null=True, blank=True)
    regularMarketDayHigh = models.FloatField(null=True, blank=True)
    navPrice = models.FloatField(null=True, blank=True)
    averageDailyVolume10Day = models.IntegerField(null=True, blank=True)
    totalAssets = models.FloatField(null=True, blank=True)
    fiftyDayAverage = models.FloatField(null=True, blank=True)
    trailingAnnualDividendRate = models.FloatField(null=True, blank=True)
    open = models.FloatField(null=True, blank=True)
    averageVolume10days = models.IntegerField(null=True, blank=True)
    t_yield = models.FloatField(null=True, blank=True)
    dividendRate = models.FloatField(null=True, blank=True)
    exDividendDate = models.DateField(null=True, blank=True)
    beta = models.FloatField(null=True, blank=True)
    regularMarketDayLow = models.FloatField(null=True, blank=True)
    currency = models.CharField(max_length=55, null=True, blank=True)
    trailingPE = models.FloatField(null=True, blank=True)
    regularMarketVolume = models.IntegerField(null=True, blank=True)
    marketCap = models.FloatField(null=True, blank=True)
    averageVolume = models.IntegerField(null=True, blank=True)
    priceToSalesTrailing12Months = models.FloatField(null=True, blank=True)
    dayLow = models.FloatField(null=True, blank=True)
    ask = models.FloatField(null=True, blank=True)
    ytdReturn = models.FloatField(null=True, blank=True)
    askSize = models.IntegerField(null=True, blank=True)
    volume = models.FloatField(null=True, blank=True)
    fiftyTwoWeekHigh = models.FloatField(null=True, blank=True)
    forwardPE = models.FloatField(null=True, blank=True)
    fiveYearAvgDividendYield = models.FloatField(null=True, blank=True)
    fiftyTwoWeekLow = models.FloatField(null=True, blank=True)
    bid = models.FloatField(null=True, blank=True)
    dividendYield = models.FloatField(null=True, blank=True)
    bidSize = models.IntegerField(null=True, blank=True)
    dayHigh = models.FloatField(null=True, blank=True)
    exchange = models.CharField(max_length=255, null=True, blank=True)
    shortName = models.CharField(max_length=55, null=True, blank=True)
    longName = models.CharField(max_length=255, null=True, blank=True)
    exchangeTimezoneName = models.CharField(max_length=255, null=True, blank=True)
    quoteType = models.CharField(max_length=255, null=True, blank=True)
    market = models.CharField(max_length=55, null=True, blank=True)
    enterpriseToRevenue = models.FloatField(null=True, blank=True)
    beta3Year = models.FloatField(null=True, blank=True)
    profitMargins = models.FloatField(null=True, blank=True)
    enterpriseToEbitda = models.FloatField(null=True, blank=True)
    fiftyTwoWeekChange = models.FloatField(null=True, blank=True)
    morningStarRiskRating = models.FloatField(null=True, blank=True)
    forwardEps = models.FloatField(null=True, blank=True)
    revenueQuarterlyGrowth = models.FloatField(null=True, blank=True)
    sharesOutstanding = models.BigIntegerField(null=True, blank=True)
    fundInceptionDate = models.DateField(null=True, blank=True)
    annualReportExpenseRatio = models.FloatField(null=True, blank=True)
    bookValue = models.FloatField(null=True, blank=True)
    sharesShort = models.BigIntegerField(null=True, blank=True)
    sharesPercentSharesOut = models.FloatField(null=True, blank=True)
    fundFamily = models.CharField(max_length=255, null=True, blank=True)
    lastFiscalYearEnd = models.DateField(null=True, blank=True)
    heldPercentInstitutions = models.FloatField(null=True, blank=True)
    netIncomeToCommon = models.BigIntegerField(null=True, blank=True)
    trailingEps = models.FloatField(null=True, blank=True)
    lastDividendValue = models.FloatField(null=True, blank=True)
    SandP52WeekChange = models.FloatField(null=True, blank=True)
    priceToBook = models.FloatField(null=True, blank=True)
    heldPercentInsiders = models.FloatField(null=True, blank=True)
    nextFiscalYearEnd = models.DateField(null=True, blank=True)
    mostRecentQuarter = models.DateField(null=True, blank=True)
    shortRatio = models.FloatField(null=True, blank=True)
    sharesShortPreviousMonthDate = models.BigIntegerField(null=True, blank=True)
    floatShares = models.BigIntegerField(null=True, blank=True)
    enterpriseValue = models.FloatField(null=True, blank=True)
    threeYearAverageReturn = models.FloatField(null=True, blank=True)
    lastSplitDate = models.DateField(null=True, blank=True)
    lastSplitFactor = models.CharField(max_length=55, null=True, blank=True)
    legalType = models.CharField(max_length=255, null=True, blank=True)
    lastDividendDate = models.DateField(null=True, blank=True)
    morningStarOverallRating = models.FloatField(null=True, blank=True)
    earningsQuarterlyGrowth = models.FloatField(null=True, blank=True)
    dateShortInterest = models.DateField(null=True, blank=True)
    pegRatio = models.FloatField(null=True, blank=True)
    shortPercentOfFloat = models.FloatField(null=True, blank=True)
    sharesShortPriorMonth = models.BigIntegerField(null=True, blank=True)
    impliedSharesOutstanding = models.BigIntegerField(null=True, blank=True)
    category = models.CharField(max_length=255, null=True, blank=True)
    fiveYearAverageReturn = models.FloatField(null=True, blank=True)
    regularMarketPrice = models.FloatField(null=True, blank=True)
    logo_url = models.URLField(null=True, blank=True)
    def __str__(self):
        return f'{self.symbol} - {self.shortName}'




class Portfolio(models.Model):
    name = models.CharField(max_length=255)
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
    kind = models.CharField(max_length=30, default='Watchlist', choices=(('Portfolio','Portfolio'),('Watchlist','Watchlist')))
    ticker = models.ManyToManyField(Ticker)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    def __str__(self):
        return f'{self.user} - {self.name} - {self.kind}'



