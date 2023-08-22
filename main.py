import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('nyc_311_data_2022.csv')
#Task 1
# Remove the data records where either of 'incident_zip', 'latitude', 'longitude' columns has missing values or NaN
columns_to_check = ['incident_zip', 'latitude', 'longitude']
data = data.dropna(subset=columns_to_check)
# Filter the 'created_date' column to keep the data just for December 2022.
data['created_date'] = pd.to_datetime(data['created_date'])
data['created_date'] = data['created_date'][
    (data['created_date'].dt.year == 2022) &
    (data['created_date'].dt.month == 12)
]
data = data.dropna(subset='created_date')

#Task 2
#Get the total number of requests for each complaint type ('complaint_type') and plot a pie chart depicting
# the % share of each complaint type within the total activity and identify the top three complaint types.
complaint_type_totals = data['complaint_type'].value_counts()

plt.figure(figsize=(10, 6))
plt.pie(complaint_type_totals, labels=complaint_type_totals.index, autopct='%1.1f%%', startangle=90)
plt.title("Complaint Type Distribution")
plt.axis('equal')
plt.show()

top_complaint_types = complaint_type_totals.head(3)
print("Top Three Complaint Types:")
print(top_complaint_types)

#Task 3
#Plot the hourly distribution of total complaints activity in a bar plot.
# (Use 'created_date' column to get the hour for each complaint record)
hourly_complaint_totals = data['created_date'].dt.hour.value_counts().sort_index()

plt.figure(figsize=(10, 6))
hourly_complaint_totals.plot(kind='bar', color='cyan')
plt.xlabel('Hour of the Day')
plt.ylabel('Number of Complaints')
plt.title('Hourly Distribution of Complaint Activity')
plt.xticks(rotation=0)
plt.show()

#Plot the proportions (%) of the top three complaint types (from task 2.) by each hour in a single bar plot.
# Each of the three complaint types can be visualized by a separate color. (Use 'created_date'
# column to get the hour for each complaint record).
hourly_proportions = data.groupby([data['created_date'].dt.hour, 'complaint_type']).size().unstack(fill_value=0)
hourly_proportions[top_complaint_types.index] = (hourly_proportions[top_complaint_types.index]
                                                 .div(hourly_proportions.sum(axis=1), axis=0) * 100)
plt.figure(figsize=(12, 6))
hourly_proportions[top_complaint_types.index].plot(kind='bar', stacked=True)
plt.xlabel('Hour of the Day')
plt.ylabel('Proportion (%)')
plt.title('Proportions (%) of Top Complaint Types by Hour')
plt.xticks(rotation=0)
plt.legend(title='Complaint Type')
plt.show()

#Task 4
#Evaluate the service processing times for city agencies

# Remove rows where 'closed_date' is earlier than 'created_date' or processing lastet less then 1 sec
data['closed_date'] = pd.to_datetime(data['closed_date'])
data = data[data['closed_date'] > data['created_date']]

#Get the processing time for each data record. Columns 'created_date' represents the time when the complaint
# was made and 'closed_date' when it was resolved.
data['processing_time'] = data['closed_date'] - data['created_date']

#Get the median processing time by each city agency and sort to get the 3 fastest and 3 slowest city agency
# ('agency_name' column represents city agency)
median_processing_times = data.groupby('agency_name')['processing_time'].median()

# Sort to get the 3 fastest and 3 slowest city agencies
fastest_agencies = median_processing_times.nsmallest(3)
slowest_agencies = median_processing_times.nlargest(3)

print()
print("Fastest City Agencies (Median Processing Time):")
print(fastest_agencies)
print("\nSlowest City Agencies (Median Processing Time):")
print(slowest_agencies)
