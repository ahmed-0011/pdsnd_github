import time
import pandas as pd

CITIES_DATA_DICT = {
    "chicago": "chicago.csv",
    "new york city": "new_york_city.csv",
    "washington": "washington.csv",
}
DATA_MONTHS = ["January", "February", "March", "April", "May", "June"]
DAYS_OF_WEEK = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("\nHello! Let's explore some US bikeshare data!")

    while True:
        city = input(
            "Please enter the name of one of the following cities: Chicago, "
            "New York City, or Washington.\nCity name: "
        )
        if city.lower() in CITIES_DATA_DICT:
            break
        else:
            print(
                f"\n{city} is not valid, you should enter one of the "
                "following cites: Chicago, New York City, or Washington.\n"
            )

    while True:
        month = input(
            "Please enter a month (from January to June) that you are "
            "interested in examining. If you want to select all these months, "
            'enter "all".\nMonth: '
        )
        month = month.lower()
        month = month.title() if month != "all" else month

        if month in DATA_MONTHS or month == "all":
            break
        else:
            print(
                f"\n{month} is not a valid month, you should enter one of the "
                "following months: January, February, March, April, May or June"
                ".\n"
            )

    while True:
        day = input(
            "Please enter the day of the week you are interested in examining. "
            'If you want to select all days, enter "all".\nDay: '
        )
        day = day.lower()
        day = day.title() if day != "all" else day

        if day in DAYS_OF_WEEK or day == "all":
            break
        else:
            print(
                f"\n{day} is not a valid day name, you should enter one of the "
                "following days: Saturday, Sunday, Monday, Tuesday, Wednesday, "
                "Thursday, Friday.\n"
            )
    print("-" * 40)
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

    df = pd.read_csv(CITIES_DATA_DICT[city])

    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["End Time"] = pd.to_datetime(df["End Time"])
    df["total_travel_time"] = df["End Time"] - df["Start Time"]
    df["month"] = df["Start Time"].dt.month
    df["day_of_week"] = df["Start Time"].dt.day_name()
    df["start_hour"] = df["Start Time"].dt.hour

    if month != "all":
        month = DATA_MONTHS.index(month)
        df = df[df["month"] == month + 1]

    if day != "all":
        df = df[df["day_of_week"] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()

    most_common_month = df["month"].mode()[0]
    print(f"Most common month: {DATA_MONTHS[most_common_month - 1]}")

    most_common_day = df["day_of_week"].mode()[0]
    print(f"Most common month: {most_common_day}")

    most_common_start_hour = df["start_hour"].mode()[0]
    print(f"Most common start hour: {most_common_start_hour}")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    most_common_start_station = df["Start Station"].mode()[0]
    print(f"Most common start station: {most_common_start_station}")

    most_common_end_station = df["End Station"].mode()[0]
    print(f"Most common end station: {most_common_end_station}")

    most_start_end_trip_combination = (
        df[["Start Station", "End Station"]].value_counts().index[0]
    )
    most_start_end_trip_combination = ", ".join(most_start_end_trip_combination)
    print(
        "Most frequent combination of start station and end station trip: "
        f"{most_start_end_trip_combination}"
    )
    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    total_travel_time = df["total_travel_time"].dt.seconds.div(60).sum()
    print(f"Total travel time: {int(total_travel_time)} minutes")

    mean_travel_time = df["total_travel_time"].dt.seconds.div(60).mean()
    print(f"Mean travel time: {int(mean_travel_time)} minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print("\nCalculating User Stats...\n")
    start_time = time.time()

    print("Count of each user type:")
    for user_type, count in df["User Type"].value_counts().to_dict().items():
        print(f"{user_type}: {count}")

    if city != "washington":
        print("\nCount of each gender:")
        for user_gender, count in df["Gender"].value_counts().to_dict().items():
            print(f"{user_gender}: {count}")

        most_common_year_of_birth = int(df["Birth Year"].mode()[0])
        most_earliest_year_of_birth = int(df["Birth Year"].min())
        most_recent_year_of_birth = int(df["Birth Year"].max())
        print("\nYear of birth Statistics:")
        print(f"Most common year of birth: {most_common_year_of_birth}")
        print(f"Most earliest year of birth: {most_earliest_year_of_birth}")
        print(f"Most recent year of birth: {most_recent_year_of_birth}")
        print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def display_data(df):
    """Display a specific number of rows every time the user enters yes"""
    NUM_OF_ROWS = 5
    row_index = 0
    total_number_of_rows = df.shape[0]
    prompt = None

    while row_index + NUM_OF_ROWS <= total_number_of_rows:
        prompt = input(
            '\nPlease enter "yes" if you want to display the '
            f"{'first' if row_index == 0 else 'next'} 5 rows."
            "\nInput: "
        )
        if prompt.lower() == "yes":
            print(df.iloc[row_index : (row_index + NUM_OF_ROWS)])
            row_index += NUM_OF_ROWS
        else:
            break
    """Display any remaining rows if any"""
    if row_index < total_number_of_rows and prompt in [None, "yes"]:
        prompt = input(
            f"\nA few number of rows (less than {NUM_OF_ROWS} rows) remained; "
            "do you want to display them ?\nInput: "
        )
        if prompt.lower() == "yes":
            print(df.iloc[row_index:])

    print("-" * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df)

        restart = input(
            "\nIf you Would you like to restart? PLease enter yes.\nInput: "
        )
        if restart.lower() != "yes":
            break


if __name__ == "__main__":
    main()
