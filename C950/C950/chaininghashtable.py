# Zybooks C950: Data Structures and Algorithms II home
# Section 7.8 : Python: Hash Tables
# Figure 7.8.2 - Hash table using chaining

# HashTable class using chaining.
# Time complexity in big-O notation = O(n)
# Space complexity in big-O notation = O(n)
class HashTableChaining:
    # Constructor with size parameter.
    # Assigns all buckets with an empty list.
    # Time complexity in big-O notation = O(1)
    # Space complexity in big-O notation = 0(n)
    def __init__(self, size):
        # initialize the hash table with empty bucket list entries.
        self.table = []
        for i in range(size):
            self.table.append([])

    # Inserts a new item into the hash table.
    # Time complexity in big-O notation = O(n)
    # Space complexity in big-O notation = O(1)
    def insert(self, key, item):  # does both insert and update
        # get the bucket list where this item will go.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # update key if it is already in the bucket
        for keyvalue in bucket_list:
            if keyvalue[0] == key:
                keyvalue[1] = item
                return True

        # if not, insert the item to the end of the bucket list.
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    # Searches for an item with matching key in the hash table.
    # Returns the item if found, or None if not found.
    # Time complexity in big-O notation = O(n)
    # Space complexity in big-O notation = O(1)
    def search(self, key):
        # get the bucket list where this key would be.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        # print(bucket_list)

        # search for the key in the bucket list
        for kv in bucket_list:
            # print (key_value)
            if kv[0] == key:
                return kv[1]  # value
        return None

    # Removes an item with matching key from the hash table.
    # Time complexity in big-O notation = O(n)
    # Space complexity in big-O notation = O(1)
    def remove(self, key):
        # get the bucket list where this item will be removed from.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # remove the item from the bucket list if it is present.
        for keyvalue in bucket_list:
            # print (key_value)
            if keyvalue[0] == key:
                bucket_list.remove([keyvalue[0], keyvalue[1]])
