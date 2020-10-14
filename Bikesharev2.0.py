# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 18:53:56 2020

@author: garcia.david
"""
#sources
#https://docs.python.org/2/library/time.html
#https://pandas.pydata.org/pandas-docs/stable/reference/api
#https://realpython.com/python-while-loop/
#https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.iloc.html

import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    while True:
        city = input('Please input the name of the city you would like to explore ').lower()
        if city not in CITY_DATA:
            print('\nThe city you entered in not valid, please try again \n')
            continue
        else:
            break
    month = None
    while month not in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
        month = input('What month would you like to filter the data, you can also use "all" to not apply a filter ').lower()

    day = None                                                        
    while day not in ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']:
        day = input ('What day of the week would you like to filter the day?, you can also use "all" to not apply a filter ').lower()

    print('-'*40)
    return city, month, day



def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

     # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        # data in the csv shows the only active months are January - June
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['month'].mode()[0]
    print('\nThe most common month of ridership is ', common_month)


    # TO DO: display the most common day of week
    common_day_of_week = df['day_of_week'].mode()[0]
    print('\nThe most common day of ridership is ', common_day_of_week)

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    pop_start_hour = df['hour'].mode()[0]

    print('\nThe most common start time is ', pop_start_hour,':00 hours')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]

    print('\nThe most common start station is \n', common_start_station)


    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode()[0]

    print('\nThe most common end station is\n', common_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    pop_combo_stations = (df['Start Station']+ ' and '+ df['End Station']).mode()[0]

    print('\nThe most common start station and end station combination is\n', pop_combo_stations)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    #convert the time from seconds to hours:minutes:seconds
    total_travel_time = time.strftime("%H:%M:%S", time.gmtime(total_travel_time))
    print ('\nThe total travel time is\n', total_travel_time)

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    #convert the time from seconds to hours:minutes:seconds
    mean_travel_time = time.strftime("%H:%M:%S", time.gmtime(mean_travel_time))
    print ('\nThe mean tavel time is\n', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].fillna('Unknown', inplace=False)
    user_types = user_types.value_counts()

    print('\nThe differente user types are\n', user_types)

    # TO DO: Display counts of gender
    #loop checks to see if the city collects Personal identifying information such as Gender
    if 'Gender' in df:
        #If gender is NaN then we count that as "Not Specified" to account for all riders
        #including those that did not want to specify
        user_gender = df['Gender'].fillna('Not Specified', inplace=False)
        user_gender = user_gender.value_counts()
        print('\nThe user gender breakdown is\n', user_gender)
    else:
        print('\nThis city does not collect user gender\n')

    # TO DO: Display earliest, most recent, and most common year of birth
    #loop checks to see if the city collects Personal identifying information such as YOB
    if 'Birth Year' in df:
        earliest_YOB = int(df['Birth Year'].min())
        most_recent_YOB = int(df['Birth Year'].max())
        common_YOB = int(df['Birth Year'].mode()[0])

        print('\nThe earliest Birth Year is\n', earliest_YOB)
        print('\nThe most recent Birth Year is\n', most_recent_YOB)
        print('\nThe most common Birthy Year is\n', common_YOB)
    else:
        print('\nThis city does not collect user Birth Year\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    trip_details = 0
    #put the question outside the loop so the user answer can be used to continue to add to the lines of data
    print('Would you like to view individual trip data?')
    while True:
        ans = input( 'Yes or No ').lower()
        if ans == 'yes':
            #starting at the first row then ending 5 after
            print(df.iloc[trip_details: trip_details+5])
            #start the rows where you left off in case user wants to continue
            trip_details += 5
            print('\n Would you like to see the next 5 rows?')
            continue
        elif ans == 'no':
            break
        else:
            print('Please enter a valid entry')
            return

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        print("Thank you for exploring this data with me!")

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
 	main()
