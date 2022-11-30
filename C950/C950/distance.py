import csv
from datetime import datetime, timedelta
import math

from package import Package, package_chaining_hash_table

# distance.py
# Time complexity in big-O notation = O(n^2)
# Space complexity in big-O notation = O(n)

# Read distancetable.csv and generate a list
# Time complexity in big-O notation = O(1)
# Space complexity in big-O notation = O(1)
def retrieve_distance_data():
    with open('packagedata/distancetable.csv') as file:
        list_distance_table = list(csv.reader(file, delimiter=','))
    return list_distance_table


# Read packageaddresses.csv and generate a list
# Time complexity in big-O notation = O(1)
# Space complexity in big-O notation = O(1)
def retrieve_address_info():
    with open('packagedata/packageaddresses.csv') as file:
        list_package_addresses = list(csv.reader(file, delimiter=','))
    return list_package_addresses


# Finds distance between two destinations
# Time complexity in big-O notation = O(n)
# Space complexity in big-O notation = O(n)
def distance_from_first_address_to_second_address(address1, address2):
    distance_list = retrieve_distance_data()
    destination_address_list = retrieve_address_info()
    first_address_index = None
    second_address_index = None

    #  Finds the info for first destination address
    for first_address in destination_address_list:
        if first_address[2] == address1:
            first_address_index = int(first_address[0])

    # Finds the info for second destination address
    for second_address in destination_address_list:
        if second_address[2] == address2:
            second_address_index = int(second_address[0])

    # Finds the distance between two addresses using the distance table
    if distance_list[first_address_index][second_address_index] == '':
        return distance_list[second_address_index][first_address_index]
    else:
        return distance_list[first_address_index][second_address_index]


#  Finds the next delivery address based on the packages on the same truck
#  Time complexity in big-O notation = O(n)
#  Space complexity in big-O notation = O(n)
def find_next_delivery_address(address1, truck_packages):
    smallest_distance = 75.5
    next_delivery_address = ''
    package_info = package_chaining_hash_table()
    truck_current_packages = []

    # Gets all info for packages on truck and creates list
    for package_id in truck_packages:
        package_object = format(package_info.search(package_id)).split(',')
        truck_current_packages.append(package_object)

    # Finds closest delivery address based on list
    for package in truck_current_packages:
        address_two = package[1]
        distance = float(distance_from_first_address_to_second_address(address1, address_two))

        # Closest delivery address becomes next destination
        if distance < smallest_distance:
            smallest_distance = distance
            next_delivery_address = str(address_two)

    return next_delivery_address


# Using info based on the packages currently on the truck
# Greedy algo to determine the best path to next destination
# Time complexity in big-O notation = O(n^2)
# Space complexity in big-O notation = O(n)
def determine_best_path(truck_packages):
    best_path = [1]  # Creates list of indexes beginning at WGUPS Package Hub
    packages = truck_packages.copy()  # Copies list of packages so it can be modified without changing the original
    package_data = package_chaining_hash_table()  # Retrieves chaining hash table
    packages_on_truck_info = []  # list for all package info on truck

    # Grabs all info for each package and creates a list
    for package_id in packages:
        package_object = format(package_data.search(package_id)).split(',')
        packages_on_truck_info.append(package_object)

    # Goes through list of all stops
    # Finds shortest stop and best path to take
    for var_x in truck_packages:
        most_recent_stop = retrieve_address_from_id(best_path[truck_packages.index(var_x)])  # Finds the most recent stop
        next_stop = find_next_delivery_address(most_recent_stop, packages)   # Finds next stop
        best_path.append(retrieve_address_index(next_stop))  # Moves next stop to list for delivery

        # If package is delivered, remove from editable copy of list
        for var_y in packages_on_truck_info:
            if next_stop == packages_on_truck_info[packages_on_truck_info.index(var_y)][1]:
                package_delivered = int(packages_on_truck_info[packages_on_truck_info.index(var_y)][0])
                packages.remove(package_delivered)

    # Takes values of None and removes from list
    # Occurs when two packages have the same destination
    if None in list(best_path):
        best_path = list(filter(None, best_path))

    # Sends truck back to hub and ends deliveries for the day
    best_path.append(1)

    return best_path


# Retrieves index for an address
# Time complexity in big-O notation =  O(n)
# Space complexity in big-O notation = O(1)
def retrieve_address_index(address):
    address_info = retrieve_address_info()
    address_idnex = None
    for row in address_info:
        if address == row[2]:
            address_idnex = int(row[0])
    return address_idnex


# Retrieves the address for a given package based on ID
# Time complexity in big-O notation = O(n)
# Space complexity in big-O notation = O(1)
def retrieve_address_from_id(address_id):
    address_data = retrieve_address_info()
    address = None
    for row in address_data[1:28]:
        if address_id == int(row[0]):
            address = str(row[2])
    return address


# Retrieves total distance of addresses based on indexed list
# Time complexity in big-O notation = O(n)
# Space complexity in big-O notation = O(1)
def retrieve_total_distance(address_index_list):
    total_distance = 0.0  # Initializes to 0

    # Adds distance between pairs of indexed addresses
    for i_distance in address_index_list:
        if address_index_list[address_index_list.index(i_distance) + 1]:
            first_address = retrieve_address_from_id(i_distance)
            second_address = retrieve_address_from_id(address_index_list[address_index_list.index(i_distance) + 1])
            total_distance += float(distance_from_first_address_to_second_address(first_address, second_address))
    return total_distance


# Determines delivery time based on path and leave time
# Time complexity in big-O notation = O(n)
# Space complexity in big-O notation = O(n)
def truck_delivery_times(truck_path, truck_leave_time):
    path = truck_path.copy()  # creates copy of path to be modified
    path.pop()  # deletes last item in dictionary to prevent duplicate keys

    # Creates a dictionary of ID and documents time during stop
    time_during_stop = dict.fromkeys(path, None)

    # Key for last stop back at the hub once deliveries are complete
    time_during_stop.update(return_to_hub=None)

    for address_id, time in time_during_stop.items():
        # Sets hub time to leave time (beginning of path)
        if address_id == 1:
            time_during_stop.update({1: truck_leave_time})

        # Determines time of arrival to hub once deliveries are complete
        elif address_id == 'return_to_hub':
            first_address = retrieve_address_from_id(path[-1])
            second_address = retrieve_address_from_id(1)

            # Determines time between stops based on max average speed of truck (18 mph)
            distance = float(distance_from_first_address_to_second_address(first_address, second_address))
            time_between_stops_minutes = math.ceil((distance / 18) * 60)

            # Adds time between stops to get accurate measurement of time
            last_stop_time = datetime.strptime(time_during_stop.get(path[-1]), '%H:%M')
            next_stop_timestamp = last_stop_time + timedelta(minutes=time_between_stops_minutes)
            next_stop_time = next_stop_timestamp.strftime('%H:%M')

            # Updates dictionary with return to hub time
            time_during_stop.update({'return_to_hub': next_stop_time})

        # Determines time of delivery for each package
        else:
            first_address = retrieve_address_from_id(path[path.index(address_id) - 1])
            second_address = retrieve_address_from_id(address_id)

            # Determines time between stops based on max average speed of truck (18 mph)
            distance = float(distance_from_first_address_to_second_address(first_address, second_address))
            time_between_stops_minutes = math.ceil((distance / 18) * 60)

            # Adds time between stops to get accurate measurement of time
            last_stop_time = datetime.strptime(time_during_stop.get(path[path.index(address_id) - 1]), '%H:%M')
            next_stop_timestamp = last_stop_time + timedelta(minutes=time_between_stops_minutes)
            next_stop_time = next_stop_timestamp.strftime('%H:%M')  # extract H:M format from timestamp

            # Update the dictionary with the stop time
            time_during_stop.update({address_id: next_stop_time})

    return time_during_stop


# Update package status based on user input for time
# Time complexity in big-O notation = O(n^2)
# Space complexity in big-O notation = O(n)
def package_status_update(hash_table_package, packages_on_truck, dictionary_time_of_delivery, requested_time):
    packages_on_truck_info = []  # Creates list to store data of package info on truck
    requested_timestamp = datetime.strptime(requested_time, '%H:%M')

    # Gets all info for packages on a truck and creates a list with all info
    for item in packages_on_truck:
        package_object = format(hash_table_package.search(item)).split(',')
        packages_on_truck_info.append(package_object)

    # Looks through dictionary and updates package info if needed
    for address_id, time in dictionary_time_of_delivery.items():
        timestamp = datetime.strptime(time, '%H:%M')  # Convert time in dict to a datetime object

        # If truck leave time is before time input, update package to say "In Transit"
        if address_id == 1 and timestamp <= requested_timestamp:

            for package in packages_on_truck_info:
                # Creates new object with same package infor and updates package status
                object_package = Package(package_id=int(package[0]),
                                         address=package[1],
                                         city=package[2],
                                         state=package[3],
                                         zipcode=package[4],
                                         delivery_deadline=package[5],
                                         weight=package[6],
                                         delivery_status='In Transit')

                # Insert package into hash table
                hash_table_package.insert(int(package[0]), object_package)

        # Finds packages delivered at or before user input for time
        if timestamp <= requested_timestamp:
            address = retrieve_address_from_id(address_id)

            # Looks through packages that are on the truck to see if they have been delivered
            for package in packages_on_truck_info:
                if address == package[1]:


                    # Creates new object with same package infor and updates package status
                    object_package = Package(package_id=int(package[0]),
                                             address=package[1],
                                             city=package[2],
                                             state=package[3],
                                             zipcode=package[4],
                                             delivery_deadline=package[5],
                                             weight=package[6],
                                             delivery_status='Delivered at ' + time)

                    # Insert the package into the package hash table
                    hash_table_package.insert(int(package[0]), object_package)

    return hash_table_package
