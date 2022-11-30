# Jared Hines  -  001497856
# C950 - NHP2

from package import package_chaining_hash_table, retrieve_package_details
from distance import determine_best_path, truck_delivery_times, package_status_update, retrieve_total_distance

# main.py
# Time complexity in big-O notation = O(n)
# Space complexity in big-O notation = O(1)

# Creates a hash table for packages
package_info = package_chaining_hash_table()

# Beginning address for trucks
# WGUPS package hub
WGUPS_package_hub = '4001 South 700 East'

# Manually loaded trucks with packages listed by ID
truck_1 = [1, 8, 13, 14, 15, 16, 19, 20, 21, 29, 30, 31, 34, 37, 39]
truck_2 = [2, 3, 6, 7, 17, 18, 25, 26, 27, 28, 33, 35, 36, 38, 40]
truck_3 = [4, 5, 9, 10, 11, 12, 22, 23, 24, 32]

# Creates a path for the trucks to travel using package ID
truck_1_path = determine_best_path(truck_1)
truck_2_path = determine_best_path(truck_2)
truck_3_path = determine_best_path(truck_3)

# Times for each truck leaving the hub
truck_1_leave_time = '08:00'
truck_2_leave_time = '09:15'
truck_3_leave_time = '10:30'

# Times for delivery based on path
# Truck leave time for WGUPS hub
truck_1_delivery_times = truck_delivery_times(truck_1_path, truck_1_leave_time)
truck_2_delivery_times = truck_delivery_times(truck_2_path, truck_2_leave_time)
truck_3_delivery_times = truck_delivery_times(truck_3_path, truck_3_leave_time)

# Prints message showing user that program has been started
print('-----------------------------------------------------')
print('\nWGUPS Package Delivery System.')
print('-----------------------------------------------------')


# User interface to allow user to view package status
# View package details
# View how far trucks have traveled
# Time complexity in big-O notation = O(n)
# Space complexity in big-O notation = O(1)
def user_interface():
    user_option = input('\nPlease type a number corresponding to the desired option and press ENTER:\n'
                           '1 - View all package statuses for a specific time\n'
                           '2 - View packagedata for a specific package (ID needed)\n'
                           '3 - View total distance traveled by trucks\n'
                           '4 - Exit the program\n')

    # Using entered time
    # Updates status of packages
    # Prints list of updated packages
    if user_option == '1':
        user_input_time = input('Please type a time in 24-hour clock format (HH:MM) and press ENTER.\n')
        print('\nCurrent package statuses for time:', user_input_time)
        print('-------------------------')

        package_status_update(package_info, truck_1, truck_1_delivery_times, user_input_time)
        package_status_update(package_info, truck_2, truck_2_delivery_times, user_input_time)
        package_status_update(package_info, truck_3, truck_3_delivery_times, user_input_time)
        print('ID | Address | City | State | Zip | Due | Weight | Status')
        for i in range(len(package_info.table)):
            package_statuses = format(package_info.search(i + 1)).split(',')
            print(package_statuses[0], '|', package_statuses[1], '|', package_statuses[2], '| ', package_statuses[3],
                  ' |', package_statuses[4], '|', package_statuses[5], '|', package_statuses[6],
                  '|', package_statuses[7])

        input('\nPress ENTER to continue.')
        user_interface()

    # Function to print specific information for one package
    elif user_option == '2':
        package_id = input('Please type ID for desired package and press ENTER.\n')
        package_details = retrieve_package_details(package_info, int(package_id))
        print('Information for package number', package_id + ':')
        print('Package ID:', package_details[0],
              '\nDestination Address:', package_details[1],
              '\nCity:', package_details[2],
            '\nState:', package_details[3],
              '\nZip:', package_details[4],
              '\nDeadline:', package_details[5],
              '\nWeight:', package_details[6])

        input('\nPress ENTER to continue.')
        user_interface()

    # Print the distance traveled by each truck
    # Print the distance traveled by all trucks combined
    elif user_option == '3':
        truck_1_total_distance = round(retrieve_total_distance(truck_1_path), 2)
        truck_2_total_distance = round(retrieve_total_distance(truck_2_path), 2)
        truck_3_total_distance = round(retrieve_total_distance(truck_3_path), 2)

        print('Truck 1 total distance traveled:', truck_1_total_distance)
        print('Truck 2 total distance traveled:', truck_2_total_distance)
        print('Truck 3 total distance traveled:', truck_3_total_distance)
        print('All trucks total distance traveled:', truck_1_total_distance + truck_2_total_distance + truck_3_total_distance)

        input('\nPress ENTER to return to main menu.')
        user_interface()

    # End the program and exit
    elif user_option == '4':
        print('Program successfully ended. Have a great day.')
        SystemExit

    # Error message given wrong entry
    # Asks user to try again using correct number
    else:
        print('Sorry, that option was not recognized. Please try again using the correct number.\n')
        user_interface()


# Allows the interface to run
user_interface()
