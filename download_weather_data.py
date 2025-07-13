import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry

# Set up the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://historical-forecast-api.open-meteo.com/v1/forecast"
params = {
    # Amsterdam area (you can change)
    "latitude": 52.37,
    "longitude": 4.89,
    "start_date": "2020-08-10",
    "end_date": "2024-08-23",
    "hourly": "temperature_2m",
    "daily": "temperature_2m_mean"
}

responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Elevation: {response.Elevation()} masl")
print(f"Timezone: {response.Timezone()} {response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()} s")

# Process hourly data
hourly = response.Hourly()
hourly_temperature = hourly.Variables(0).ValuesAsNumpy()
hourly_data = {
    "date": pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    )
}
hourly_data["temperature_2m"] = hourly_temperature
hourly_dataframe = pd.DataFrame(data=hourly_data)
print(hourly_dataframe)

# Process daily data
daily = response.Daily()
daily_temperature = daily.Variables(0).ValuesAsNumpy()
daily_data = {
    "date": pd.date_range(
        start=pd.to_datetime(daily.Time(), unit="s", utc=True),
        end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=daily.Interval()),
        inclusive="left"
    )
}
daily_data["temperature_2m_mean"] = daily_temperature
daily_dataframe = pd.DataFrame(data=daily_data)
print(daily_dataframe)

# Handle missing data using interpolation
# Check for missing values in hourly data
print(f"\nMissing values in hourly data before interpolation: {hourly_dataframe.isna().sum().sum()}")

# Interpolate missing values in hourly data
hourly_dataframe_clean = hourly_dataframe.copy()

# Set date as index for time-based interpolation
hourly_dataframe_clean = hourly_dataframe_clean.set_index('date')

# Interpolate using the index (which is now a DatetimeIndex)
hourly_dataframe_clean['temperature_2m'] = hourly_dataframe_clean['temperature_2m'].interpolate(method='time')

# For any remaining NaN values at the beginning or end, use forward/backward fill
hourly_dataframe_clean['temperature_2m'] = hourly_dataframe_clean['temperature_2m'].fillna(method='ffill').fillna(method='bfill')

# Reset index to get 'date' back as a column
hourly_dataframe_clean = hourly_dataframe_clean.reset_index()

print(f"Missing values in hourly data after interpolation: {hourly_dataframe_clean.isna().sum().sum()}")

# Check for missing values in daily data
print(f"\nMissing values in daily data before interpolation: {daily_dataframe.isna().sum().sum()}")

# Interpolate missing values in daily data
daily_dataframe_clean = daily_dataframe.copy()

# Set date as index for time-based interpolation
daily_dataframe_clean = daily_dataframe_clean.set_index('date')

# Interpolate using the index (which is now a DatetimeIndex)
daily_dataframe_clean['temperature_2m_mean'] = daily_dataframe_clean['temperature_2m_mean'].interpolate(method='time')

# For any remaining NaN values at the beginning or end, use forward/backward fill
daily_dataframe_clean['temperature_2m_mean'] = daily_dataframe_clean['temperature_2m_mean'].fillna(method='ffill').fillna(method='bfill')

# Reset index to get 'date' back as a column
daily_dataframe_clean = daily_dataframe_clean.reset_index()

print(f"Missing values in daily data after interpolation: {daily_dataframe_clean.isna().sum().sum()}")

# Save dataframes to CSV for later use in notebooks
hourly_dataframe_clean.to_csv('hourly_data.csv', index=False)
daily_dataframe_clean.to_csv('daily_data.csv', index=False)

# Also save the original data with missing values for comparison if needed
hourly_dataframe.to_csv('hourly_data_with_missing.csv', index=False)
daily_dataframe.to_csv('daily_data_with_missing.csv', index=False)
