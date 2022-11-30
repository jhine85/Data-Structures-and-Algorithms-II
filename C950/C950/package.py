import csv

from chaininghashtable import HashTableChaining

# package.py
# Time complexity in big-O notation = O(n)
# Space complexity in big-O notation = O(n)
# Package class
class Package:
    def __init__(self, package_id, address, city, state, zipcode, delivery_deadline, weight, delivery_status):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zipcode
        self.delivery_deadline = delivery_deadline
        self.weight = weight
        self.delivery_status = delivery_status

    # Returns desired info
    # not reference to object
    def __str__(self):
        return '%s,%s,%s,%s,%s,%s,%s,%s' % (self.package_id, self.address, self.city, self.state, self.zip,
                                            self.delivery_deadline, self.weight, self.delivery_status)


# Reads data stored in csv and places in a hash table
# Time complexity in big-O notation = O(n)
# Space complexity in big-O notation = O(n)
def package_chaining_hash_table():
    # Creates object for hash table
    hash_table_package_object = HashTableChaining(40)

    # CSV FILE READER
    with open('packagedata/wgupspackages.csv') as packages:
        package_info = csv.reader(packages, delimiter=',')
        next(package_info)  # skip the header row
        for info in package_info:
            package_id = int(info[0])
            address = info[1]
            city = info[2]
            state = info[3]
            zip_code = info[4]
            deadline = info[5]
            weight = info[6]
            delivery_status = 'At the hub'

            # Creates object for package
            object_pack = Package(package_id, address, city, state, zip_code, deadline, weight, delivery_status)

            # Places package in hash table
            hash_table_package_object.insert(package_id, object_pack)

    return hash_table_package_object


# Retrieves info for package info at user input of time
# Time complexity in big-O notation = O(n)
# Space complexity in big-O notation = O(1)
def retrieve_package_details(package_hash_table, package_id):
    object_package_hash = format(package_hash_table.search(package_id)).split(',')
    object_package_hash.pop()
    return object_package_hash
