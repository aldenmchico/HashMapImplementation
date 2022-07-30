# Name: Alden Chico
# OSU Email: chicoa@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6 - HashMap Implementation
# Due Date: 08/09/2022
# Description: HashMap ADT Implemented Using Dynamic Array and Collision Resolution via Chaining


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updated key/value pair in hash map. If key already exists, associated value replaced with new value. If key
        is not in hash map, a new key / value pair is added.
        :param key: Key to find associated value in hash map
        :param value: Value to be associated with key
        :return:
        """
        #  Use hash function to find linked list associated with key
        hash_val = self._hash_function(key)
        hash_idx = hash_val % self._capacity
        hash_ll = self._buckets[hash_idx]

        #  If the key is found in the linked list, replace the value with the argument value
        if hash_ll.contains(key):
            for node in hash_ll:
                if node.key == key:
                    node.value = value

        #  Append a new node in the linked list with the key/value pair if it does not exist
        else:
            hash_ll.insert(key, value)
            self._size += 1

    def empty_buckets(self) -> int:
        """
        Return the number of empty buckets in the hash table
        :return:
        """
        count = 0

        # Go through each LL in the buckets Dynamic Array and increment count if the bucket is empty
        for idx in range(self._capacity):
            if self._buckets[idx].length() == 0:
                count += 1

        return count

    def table_load(self) -> float:
        """
        Returns the load factor for the hash table
        :return:
        """
        #  Load Factor = Number of elements / Number of Buckets
        return self._size / self._capacity

    def clear(self) -> None:
        """
        Clear the contents of the hash map. Does not change the underlying hash table capacity.
        :return:
        """
        # Replace every bucket with an empty Linked List
        for idx in range(self._capacity):
            self._buckets[idx] = LinkedList()

        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Change capacity of internal hash table and rehash all existing key/value pairs. Return nothing if new_capacity
        is less than 1. If new_capacity is greater than 1, change capacity so that capacity is a prime number.
        :param new_capacity: Baseline capacity for hash map to be resized to.
        :return:
        """
        #  Do nothing if the new_capacity is less than 1
        if new_capacity < 1:
            return

        #  Populate a new Dynamic Array with empty LL's with prime valued capacity
        new_buckets = DynamicArray()
        if self._is_prime(new_capacity) is False:
            new_capacity = self._next_prime(new_capacity)
        for _ in range(new_capacity):
            new_buckets.append(LinkedList())

        #  Hash the values from the old Dynamic Array and insert the values to the appropriate LL in the new DA
        for idx in range(self._capacity):
            current_ll = self._buckets[idx]
            for node in current_ll:
                hash_val = self._hash_function(node.key)
                hash_idx = hash_val % new_capacity
                new_buckets[hash_idx].insert(node.key, node.value)

        #  Set buckets of the hash map to the new Dynamic Array and capacity to the new capacity
        self._buckets = new_buckets
        self._capacity = new_capacity

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key. Returns None if the key does not exist.
        :param key: Key to be searched for
        :return:
        """
        #  Return None automatically if there are no values contained in the hash table
        if self._size == 0:
            return None

        #  Find the linked list in the hash table associated with the key
        hash_val = self._hash_function(key)
        hash_idx = hash_val % self._capacity
        hash_ll = self._buckets[hash_idx]

        #  Traverse the linked list, comparing node's key with the argument key.
        #  If the key is found, return node's value. If not, return None
        for node in hash_ll:
            if node.key == key:
                return node.value
        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns true if the given key is in the hash map, false if not.
        :param key: Key to be searched for
        :return:
        """
        #  Return False automatically if there are no values contained in the hash table
        if self._size == 0:
            return False

        #  Find the linked list in the hash table associated with the key
        hash_val = self._hash_function(key)
        hash_idx = hash_val % self._capacity
        hash_ll = self._buckets[hash_idx]

        #  Traverse the Linked List, comparing node's key with argument key
        #  If the key is found, return True. If not, return False.
        for node in hash_ll:
            if node.key == key:
                return True
        return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map. If the key is not in the hash map, do nothing.
        :param key: Key to be removed from the hash map
        :return:
        """
        #  Do nothing automatically if there are no values contained in the hash table
        if self._size == 0:
            return

        #  Find the linked list in the hash table associated with the key
        hash_val = self._hash_function(key)
        hash_idx = hash_val % self._capacity
        hash_ll = self._buckets[hash_idx]

        #  Remove the element from the hash table if the key exists. Do nothing if it doesn't
        if self.contains_key(key):
            hash_ll.remove(key)
            self._size -= 1
        else:
            return

    def get_keys_and_values(self) -> DynamicArray:
        """
        Return a Dynamic Array where each index contains a tuple of a key/value pair stored in the hash map.
        :return: key_value_da: Dynamic Array with tuples of key-value tuples
        """
        #  Return an empty Dynamic Array if there are no values contained in the hash table
        if self._size == 0:
            return DynamicArray()

        #  Create a new Dynamic Array
        key_value_da = DynamicArray()

        #  Go through each Linked List in buckets. Append key/value tuples to new Dynamic Array
        for idx in range(self._capacity):
            current_ll = self._buckets[idx]
            for node in current_ll:
                key_value_da.append((node.key, node.value))

        #  Return the Dynamic Array
        return key_value_da


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    From the Dynamic Array, return a tuple containing a Dynamic Array with the mode values in the argument Dynamic
    Array, and an integer representing the highest frequency. Assume input array contains at least 1 element and all
    values stored in the array are strings.
    :param da: Dynamic Array to find the mode
    :return: tuple: Dynamic Array containing mode elements and int with frequency
    """

    map = HashMap()
    #  Iterate through da, creating a hash map where the key -> da value, value -> count
    #  If the key is already in the hash map, increment the count associated to the key
    for idx in range(da.length()):
        if map.contains_key(da[idx]):
            key_count = map.get(da[idx])
            map.put(da[idx], key_count + 1)
        else:
            map.put(da[idx], 1)

    #  Go through key value pairs to find highest value among the tuples
    key_value_da = map.get_keys_and_values()
    mode_da = DynamicArray()
    mode_frequency = 0
    for idx in range(key_value_da.length()):
        element, count = key_value_da[idx]
        #  Initialize or count > mode frequency, replace return tuple with DA containing new mode element / frequency
        if idx == 0 or count > mode_frequency:
            mode_da = DynamicArray()
            mode_da.append(element)
            mode_frequency = count
            max_tuple = (mode_da, mode_frequency)
        #  If the tuple count == mode frequency, append the key to the DA
        elif count == mode_frequency:
            mode_da.append(element)
            max_tuple = (mode_da, mode_frequency)
    return max_tuple


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(1)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")

