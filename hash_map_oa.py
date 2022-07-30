# Name: Alden Chico
# OSU Email: chicoa@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6 - HashMap Implementation
# Due Date: 08/09/2022
# Description: HashMap ADT Implemented Using Dynamic Array and Collision Resolution via Chaining


from a6_include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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
        Update the key/value pair in the hash map. If the key already exists in the hash map, its associated value
        is replaced with the new value. If the key is not in the hash map, a new key/value pair must be added.
        Resize the table to the closest prime number to double current capacity if load factor >= 0.5.
        :param key: Key to be inserted into the hash table.
        :param value: Value to be inserted into the hash table.
        :return:
        """
        #  Use hash function to find hash index associated with key
        hash_val = self._hash_function(key)
        hash_idx = hash_val % self._capacity
        init_hash_idx = hash_idx
        quad_val = 0

        #  If the key is found in the linked list, replace the value with the argument value
        if self.contains_key(key) is True:
            while self._buckets[hash_idx].key != key:
                quad_val += 1
                hash_idx = (init_hash_idx + quad_val ** 2) % self._capacity
            self._buckets[hash_idx].value = value

        #  Create new hash entry with the key/value pair and insert it to the first available spot if it does not exist
        else:
            #  Resize the table before adding the element if load factor exceeds 0.5
            if self.table_load() >= 0.5:
                self.resize_table(2 * self._capacity)
                #  Recompute hash index associated with key if resize occurred
                hash_val = self._hash_function(key)
                hash_idx = hash_val % self._capacity
                init_hash_idx = hash_idx

            while self._buckets[hash_idx] is not None:
                #  If the element is a tombstone, allow the program to override the element with a new hash entry
                if self._buckets[hash_idx].is_tombstone is True:
                    break
                quad_val += 1
                hash_idx = (init_hash_idx + quad_val ** 2) % self._capacity
            new_entry = HashEntry(key, value)
            self._buckets[hash_idx] = new_entry
            self._size += 1

    def table_load(self) -> float:
        """
        Return the hash table's load factor
        :return: self._size / self._capacity: The load factor of the hash map
        """
        #  Load Factor = Number of elements / Number of available addresses in the Dynamic Array
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Return the number of empty addresses in the hash table
        :return:
        """
        count = 0
        # Go through each value in the hash table and increment count if the hash entry is not a tombstone
        for idx in range(self._capacity):
            if self._buckets[idx] is None:
                count += 1
            elif self._buckets[idx].is_tombstone is True:
                count += 1
        return count

    def resize_table(self, new_capacity: int) -> None:
        """
        Change the capacity of the internal hash table. Rehash all existing key/value pairs. If the argument
        new_capacity is less than the number of elements in the hash table, do nothing. If new_capacity is valid,
        make sure the new hash table capacity is a prime number.
        :param new_capacity: Baseline capacity for the new hash table
        :return:
        """
        #  Do nothing if the new_capacity is less than size of the hash table
        if new_capacity < self._size:
            return

        #  Populate a new Dynamic Array with None values with prime valued capacity
        new_buckets = DynamicArray()
        new_capacity = self._next_prime(new_capacity)
        load_factor = self._size / new_capacity
        while load_factor > 0.5:
            new_capacity = self._next_prime(new_capacity + 1)
            load_factor = self._size / new_capacity
        for _ in range(new_capacity):
            new_buckets.append(None)

        #  Hash the values from the old Dynamic Array and insert the values to the new Dynamic Array
        for idx in range(self._capacity):
            quad_val = 0
            current_entry = self._buckets[idx]
            if current_entry is not None:
                #  Only add non-tombstone entries to new Dynamic Array
                if current_entry.is_tombstone is False:
                    hash_val = self._hash_function(current_entry.key)
                    hash_idx = (hash_val + quad_val ** 2) % new_capacity
                    init_hash_idx = hash_idx
                    #  Rehash until an empty spot is found
                    while new_buckets[hash_idx] is not None:
                        quad_val += 1
                        hash_idx = (init_hash_idx + quad_val ** 2) % new_capacity
                    new_buckets[hash_idx] = current_entry

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

        #  If the key exists in the hash table, return the value associated with the key
        if self.contains_key(key) is True:
            hash_val = self._hash_function(key)
            hash_idx = hash_val % self._capacity
            init_hash_idx = hash_idx
            quad_val = 0
            while self._buckets[hash_idx].key != key:
                quad_val += 1
                hash_idx = (init_hash_idx + quad_val ** 2) % self._capacity
            return self._buckets[hash_idx].value

        return None

    def contains_key(self, key: str) -> bool:
        """
        Return True if the key is in the hash map. False otherwise.
        :param key: Key to be searched for
        :return: bool: True if the key is in the hash map. False otherwise.
        """
        #  Return False automatically if there are no values contained in the hash table
        if self._size == 0:
            return False

        #  Find the hash entry in the hash table associated with the key
        hash_val = self._hash_function(key)
        hash_idx = hash_val % self._capacity
        init_hash_idx = hash_idx
        quad_val = 0

        #  Go through buckets in the hash table. Return True if the key matches and hash entry is not a tombstone.
        #  Return False if the hash index circled back to its original position, preventing an infinite loop.
        #  Otherwise, update hash index and probe for the next entry.
        while self._buckets[hash_idx] is not None:
            if self._buckets[hash_idx].key == key and self._buckets[hash_idx].is_tombstone is False:
                return True
            elif hash_idx == init_hash_idx and quad_val > 0:
                return False
            else:
                quad_val += 1
                hash_idx = (init_hash_idx + quad_val ** 2) % self._capacity
        return False

    def remove(self, key: str) -> None:
        """
        Remove the given key and its associated value from the hash map. If the key is not in the hash map, do nothing.
        :param key:
        :return:
        """
        if self._size == 0 or self.contains_key(key) is False:
            return

        #  Find the hash entry in the hash table associated with the key
        hash_val = self._hash_function(key)
        hash_idx = hash_val % self._capacity
        init_hash_idx = hash_idx
        quad_val = 0
        while self._buckets[hash_idx].key != key:
            quad_val += 1
            hash_idx = (init_hash_idx + quad_val ** 2) % self._capacity

        #  Remove the element by setting its tombstone value to True
        self._buckets[hash_idx].is_tombstone = True
        self._size -= 1

    def clear(self) -> None:
        """
        Clears the contents of the hash map without changing the underlying hash table capacity.
        :return:
        """
        for idx in range(self._buckets.length()):
            self._buckets[idx] = None
        self._size = 0

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

        #  Go through each hash entry in buckets. Append key/value tuples to new Dynamic Array
        for idx in range(self._capacity):
            current_entry = self._buckets[idx]
            if current_entry is not None:
                if current_entry.is_tombstone is False:
                    key_value_da.append((current_entry.key, current_entry.value))

        #  Return the Dynamic Array
        return key_value_da


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    m = HashMap(53, hash_function_1)
    for i in range(54):
        m.put('str' + str(i), i * 100)
    if i % 25 == 24:
        print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())
    m.put('str' + str(54), 54 * 100)


    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
    if i % 25 == 24:
        print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())



    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

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

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

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
    m = HashMap(11, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

