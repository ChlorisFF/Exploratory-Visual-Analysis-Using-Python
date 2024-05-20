import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('Data/owid-energy-data.csv')

#------------------------------------------------

def Find_Columns_and_their_DataTypes(df):

    column_names = df.columns.tolist()

    print ("DataFrame Sample:")
    print(df.head())

    #print("Columns:")
    #print(column_names)

    data_types = [df[col].dtype.name for col in column_names]

    non_null_counts = df.count()

    dtype_dict = dict(zip(column_names, data_types))

    column_info = pd.DataFrame({
        'Column Name': column_names,
        'Data Type': data_types,
        'Non-Null Count': non_null_counts
    })

    print("Column info:")
    print(column_info)

#------------------------------------------------

def DataFrame_Stats(df):

    numeric_stats = df.describe()

    numeric_columns = df.select_dtypes(include=['number']).columns
    numeric_columns = [col for col in numeric_columns if col != 'year']
    additional_stats = pd.DataFrame({
        'Sum': df[numeric_columns].sum(),
        'Range': df[numeric_columns].max() - df[numeric_columns].min()
    })

    # Combine both sets of statistics
    statistics = pd.concat([numeric_stats, additional_stats.transpose()])

    # Rename the index to include 'count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max', 'Sum', 'Range'
    statistics.index = ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max', 'Sum', 'Range']

    return statistics

#------------------------------------------------

def EU_Data(df):

    EU_countries = ['Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Republic of Cyprus', 'Czech Republic', 'Denmark',
                    'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary', 'Ireland', 'Italy', 'Latvia',
                    'Lithuania', 'Luxembourg', 'Malta', 'Netherlands', 'Poland', 'Portugal', 'Romania', 'Slovakia',
                    'Slovenia', 'Spain', 'Sweden']

    EU_df = df[df['country'].isin(EU_countries)]
    return EU_df

EU_df = EU_Data(df)

#-------------------------------------------------------

def Ratio_Of_Null_Entries(df):

    # Count null (or empty) and non-null entries for each column
    null_counts = df.isnull().sum()  # Count null (or empty) entries for each column
    non_null_counts = df.notnull().sum()  # Count non-null entries for each column

    # Combine the counts into a DataFrame
    summary_df = pd.DataFrame({
        'Null Counts': null_counts,
        'Non-Null Counts': non_null_counts
    })

    # Print the summary
    print(summary_df)

# Filter the DataFrame to keep only the rows where the 'country' column is 'Austria'
austria_data = df[df['country'] == 'Austria']

#---------------------------------------------------
def plot_energy_time_series(df, energy_source):

    plt.figure(figsize=(10, 6))

    # Plot the time series data for the specified energy source
    plt.plot(df['year'], df[energy_source], marker='o')

    plt.title(f'{energy_source.capitalize()} Energy Consumption Over Time')
    plt.xlabel('Year')
    plt.ylabel('Electricity Consumption (TWh)')
    plt.grid(True)
    plt.show()


#----------------------------------

def plot_energy_time_series(df, energy_sources, colors):
    num_sources = len(energy_sources)
    fig, axes = plt.subplots(1, num_sources, figsize=(15, 6))

    # Loop through each energy source and plot its time series data
    for i, (source, color) in enumerate(zip(energy_sources, colors)):
        ax = axes[i]
        ax.plot(df['year'], df[source], marker='o', label=source, color=color)
        ax.set_title(f'{source.capitalize()} Energy Consumption')
        ax.set_xlabel('Year')
        ax.set_ylabel('Electricity Consumption (TWh)')
        ax.grid(True)
        ax.legend()

    plt.tight_layout()
    #plt.show()

#----------------------------------------------------------------------------

def electricityRelated(df, energy_columns):
    df.columns.tolist()
    return df[energy_columns]



















