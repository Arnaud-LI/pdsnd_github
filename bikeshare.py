import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters(city, month, day):
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # Start showing bicycles!
    print("\n-----  __@       __@       __@        __@       __@\n"
    "---- _  /< _    _ /< _    _ /< _     _ /< _    _ /< _\n"
    "---- (*)/ (*)  (*)/ (*)  (*)/ (*)  (*)/ (*)  (*)/ (*)\n"
    " ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    print('\nHi there! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington)

    while True:
        city = input("1 - Enter a choice of city, with either, Chicago, New York City or Washington: ").lower()
        if (city  not in ["chicago", "new york city", "washington"]):
            print("\nSorry! {} is not a valid choice\n".format(city))
            continue
        else:
            print("Good, let's go with {}\n".format(city.title()))
            break

    # get user input for month filter (all or january, february, ... june)
    while True:
        month = input("2 - Enter a choice of period to explore with either, January, February, March, April, May, June or All: ").lower()
        if (month not in ["january", "february", "march", "april", "may", "june", "all"]):
            print("\nSorry! {} is not a valid choice of month or period\n".format(month))
            continue
        else:
            print("Good, let's go with {}\n".format(month.title()))
            break

    # get user input for day of week (all or monday, tuesday, ... sunday)
    while True:
        day = input("3 - Enter the day of the week or period to explore with either Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or All: ").lower()
        if (day not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']):
            print("\nSorry! {} is not a valid choice of week day\n".format(day))
            continue
        else:
            print("All set, here we go for the city of {}, with the period filter month = {} & day = {}!\n".format(city.title(),month.title(),day.title()))
            break

    print("-"*40)
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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df["Start Time"] = pd.to_datetime(df["Start Time"])

    # extract month, day of week and hours from Start Time to create new columns
    df["Month"] = df["Start Time"].dt.month_name()
    df["Day_of_week"] = df["Start Time"].dt.day_name()
    df["Hour"] = df["Start Time"].dt.hour

    # create a combination of start & end station colunm
    df["Separator"] = " >>> "
    df["Station_combo"] = df["Start Station"] + df["Separator"] + df["End Station"]

    # filter by month if applicable
    if month != "all":
        # filter by month to create the new dataframe
        df = df[df["Month"] == month.title()]

    # filter by day of week if applicable
    if day != "all":
        # filter by day of week to create the new dataframe
        df = df[df["Day_of_week"] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # display the most common month
    popular_month = df["Month"].mode()[0]
    print("Most Frequent Start Month:", popular_month)

    # display the most common day of week
    popular_day = df["Day_of_week"].mode()[0]
    print("Most Frequent Start Day:", popular_day)

    # display the most common start hour
    popular_hour = df["Hour"].mode()[0]
    print("Most Frequent Start Hour:", popular_hour)

    print("\nDamned was fast! This took %s seconds." % (time.time() - start_time))
    print("-"*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # display most commonly used / popular start station
    popular_start_station = df["Start Station"].mode()[0]
    print("Most Popular Start Station:", popular_start_station)

    # display most commonly used / popular end station
    popular_end_station = df["End Station"].mode()[0]
    print("Most Popular End Station:", popular_end_station)

    # display most frequent combination of start station and end station trip
    popular_station_combo = df["Station_combo"].mode()[0]
    print("Most Popular Combo of Start Station and End Station:", popular_station_combo)

    print("\nDamned was fast! This took %s seconds." % (time.time() - start_time))
    print("-"*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    # function to convert seconds to day, hours, minutes borrowed to Anant Agarwal.
    # from https://www.geeksforgeeks.org/converting-seconds-into-days-hours-minutes-and-seconds/

    def ConvertSectoDay(n):
        day = n // (24 * 3600)
        n = n % (24 * 3600)
        hour = n // 3600
        n %= 3600
        minutes = n // 60
        n %= 60
        seconds = n

        return("{} days {} hours {} minutes {} seconds".format(int(day), int(hour), int(minutes), int(seconds)))

    # display total travel time
    total_travel_time = df["Trip Duration"].sum()
    print("Total travel time: ", ConvertSectoDay(total_travel_time))

    # display mean travel time
    mean_travel_time = df["Trip Duration"].mean()
    mean_travel_time = time.strftime("%H hours %M minutes %S seconds", time.gmtime(mean_travel_time))
    print("Mean travel time: ", mean_travel_time)

    # display most commun travel time
    most_commun_travel_time = df["Trip Duration"].mode()[0]
    most_commun_travel_time = time.strftime("%H hours %M minutes %S seconds", time.gmtime(most_commun_travel_time))
    print("Most commun travel time: ", most_commun_travel_time)

    # display maximum travel time
    max_travel_time = df["Trip Duration"].max()
    print("Maximum travel time: ", ConvertSectoDay(max_travel_time))

    print("\nDamned was fast! This took %s seconds." % (time.time() - start_time))
    print("-"*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print("\nCalculating User Stats...\n")
    start_time = time.time()

    # Display counts & percentage of user types
    user_types = df["User Type"].value_counts()
    df_user = pd.DataFrame(user_types)
    df_user[" % "] = user_types / user_types.sum()
    df_user = df_user.rename(columns={"User Type":"Count"})
    print("User Type Split\n",df_user)

    # Display counts & percentage of gender
    if "Gender" in df:
        Suscribers_gender = df["Gender"].value_counts()
        df_gender = pd.DataFrame(Suscribers_gender)
        df_gender[" % "] = Suscribers_gender / Suscribers_gender.sum()
        df_gender = df_gender.rename(columns={"Gender":"Count"})
        print("\nSuscribers Gender Split\n",df_gender)
    else:
        print("\nHint: Try to filter with Chicago or New York City to see gender & year birth based info")

    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df:
        early_bd = df["Birth Year"].min()
        print("\nSuscribers birth year")
        print("\nEarliest: ", int(early_bd))
        recent_bd = df["Birth Year"].max()
        print("Most recent : ", int(recent_bd))
        mode_bd = df["Birth Year"].mode()[0]
        print("Most common : ", int(mode_bd))

    print("\nDamned was fast! This took %s seconds." % (time.time() - start_time))

    # Show more with random sample of 5 line of dataframe raw data upon user input and go for more if user got some apetite mutliplying number of raw by 2
    # from the 4th yes (or y, sure, why not)

def more_data(df):
    """Displays more raw data from dataframe"""
    start_time = time.time()
    loop_count = 0
    x = 5
    while True:
        want_some_more = input("\nDo you feel like seeing more line of raw data or you're done, enter yes or no : ")
        if want_some_more.lower() in ['yes','y','sure','why not']:
            loop_count += 1
            print(df.sample(n=x))
            if loop_count == 2:
                print("\nWoaw you're really a fan of raw data!")
                continue
            elif loop_count == 3:
                print("\nReally!?")
                continue
            elif loop_count == 4:
                x *= 2
                print("\nDon't you think it's enough!?")
                continue
            elif loop_count >= 5:
                x *= 2
                print("\nWhat about now?")
                continue

        elif want_some_more.lower() not in ['yes','no', 'y','sure', 'why not']:
            print("\nSorry {} isn't a valid entry, please type either yes or no".format(want_some_more.lower()))
            continue
        elif want_some_more.lower() == 'no':
            print("\nAll right!")
            break
    print("\nHum, this took %s seconds." % (time.time() - start_time))


def main():
    city = ""
    month = ""
    day = ""
    while True:
        city, month, day = get_filters(city, month, day)
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        more_data(df)

        restart = input('\nWould you like to restart? Enter yes or no. ')
        if restart.lower() != 'yes':
            print("\nHope you've enjoyed the ride, thanks for your time folks!")
            print("\n-----  __@       __@       __@        __@       __@\n"
            "---- _  /< _    _ /< _    _ /< _     _ /< _    _ /< _\n"
            "---- (*)/ (*)  (*)/ (*)  (*)/ (*)  (*)/ (*)  (*)/ (*)\n"
            " ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            break

if __name__ == "__main__":
	main()
