import csv
import time
import matplotlib.pyplot as plt
import random

# Define Bid structure
class Bid:
    def __init__(self, bid_id, title, fund, amount):
        # Basic constructor for Bid objects
        self.bid_id = bid_id
        self.title = title
        self.fund = fund
        self.amount = amount

class LinkedListNode:
    def __init__(self, bid):
        # Node for LinkedList, holding a bid and reference to next node
        self.bid = bid
        self.next = None

class LinkedList:
    def __init__(self):
        # Initialize LinkedList with head as None
        self.head = None

    def append(self, bid):
        # O(n) operation - append bid to end of list, requires traversing the list
        if not self.head:
            self.head = LinkedListNode(bid)
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = LinkedListNode(bid)

    def search(self, bid_id):
        # O(n) operation - linear search for a bid by its ID
        current = self.head
        while current:
            if current.bid.bid_id == bid_id:
                return current.bid
            current = current.next
        return None

    def print_all_bids(self):
        # O(n) operation - prints all bids, requires traversing the list
        current = self.head
        while current:
            print(f"Bid ID: {current.bid.bid_id}, Title: {current.bid.title}, Fund: {current.bid.fund}, Amount: {current.bid.amount}")
            current = current.next

# Load bids from CSV into LinkedList
# This function's efficiency depends on the number of bids in the CSV, as each insertion is O(n).
def load_bids_into_linkedlist(file_path):
    bids_linkedlist = LinkedList()
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip the header
        for row in reader:
            bid = Bid(row[0], row[1], row[2], float(row[3]))
            bids_linkedlist.append(bid)  # Each append is O(n), making this loop potentially O(n^2) for large datasets
    return bids_linkedlist

class Node:
    def __init__(self, bid):
        # Node for BinarySearchTree, contains bid, left child, and right child
        self.bid = bid
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        # Initialize BST with root as None
        self.root = None

    def insert(self, bid):
        # O(log n) average case, O(n) worst case - insert bid into BST
        if not self.root:
            self.root = Node(bid)
        else:
            self._insert_recursive(self.root, bid)

    def _insert_recursive(self, current_node, bid):
        # Recursive helper for insert, maintains BST properties
        if bid.bid_id < current_node.bid.bid_id:
            if current_node.left is None:
                current_node.left = Node(bid)
            else:
                self._insert_recursive(current_node.left, bid)
        else:
            if current_node.right is None:
                current_node.right = Node(bid)
            else:
                self._insert_recursive(current_node.right, bid)

    def search(self, bid_id):
        # O(log n) average case, O(n) worst case - search for bid by ID
        return self._search_recursive(self.root, bid_id)

    def _search_recursive(self, current_node, bid_id):
        # Recursive helper for search, utilizes BST properties to optimize search
        if current_node is None:
            return None
        if bid_id == current_node.bid.bid_id:
            return current_node.bid
        elif bid_id < current_node.bid.bid_id:
            return self._search_recursive(current_node.left, bid_id)
        else:
            return self._search_recursive(current_node.right, bid_id)

# Sorting Algorithms - Each has its own time complexity and use cases.
# Quick Sort: O(n log n) average case, O(n^2) worst case. Efficient for large datasets, not stable.
def quick_sort(data):
    if len(data) <= 1:
        return data
    pivot = data[len(data) // 2]
    left = [x for x in data if x < pivot]
    middle = [x for x in data if x == pivot]
    right = [x for x in data if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

# Merge Sort: O(n log n) for all cases. Efficient and stable, but requires additional memory for merging.
def merge_sort(data):
    if len(data) <= 1:
        return data
    middle = len(data) // 2
    left = merge_sort(data[:middle])
    right = merge_sort(data[middle:])
    return merge(left, right)

def merge(left, right):
    result = []
    left_index, right_index = 0, 0
    while left_index < len(left) and right_index < len(right):
        if left[left_index] < right[right_index]:
            result.append(left[left_index])
            left_index += 1
        else:
            result.append(right[right_index])
            right_index += 1
    result += left[left_index:]
    result += right[right_index:]
    return result

# Bubble Sort: O(n^2) for all cases. Inefficient for large datasets, but simple and stable.
def bubble_sort(data):
    n = len(data)
    for i in range(n):
        for j in range(0, n-i-1):
            if data[j] > data[j+1]:
                data[j], data[j+1] = data[j+1], data[j]
    return data

# Search Algorithms - Note the importance of data structure choice on search efficiency.
# Binary Search: O(log n), requires sorted data. Efficient for large datasets.
def binary_search(data, target):
    data.sort()  # Sorting data first, complexity depends on the sorting algorithm used
    low = 0
    high = len(data) - 1
    while low <= high:
        mid = (low + high) // 2
        if data[mid] == target:
            return mid
        elif data[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return None

# Linear Search: O(n), does not require sorted data. Simple but inefficient for large datasets.
def linear_search(data, target):
    for i in range(len(data)):
        if data[i] == target:
            return i
    return None

# Measure and plot algorithm efficiency
def measure_efficiency():
    # Generate random data for testing
    data = [random.randint(0, 1000) for _ in range(1000)]
    timings = {}

    start_time = time.time()
    quick_sort(data.copy())  # Use copy to ensure each sort starts with the same unsorted data
    timings['Quick Sort'] = time.time() - start_time

    start_time = time.time()
    merge_sort(data.copy())
    timings['Merge Sort'] = time.time() - start_time

    start_time = time.time()
    bubble_sort(data.copy())
    timings['Bubble Sort'] = time.time() - start_time

    # Optionally, print the timings or plot them
    for sort, time_taken in timings.items():
        print(f"{sort} Time: {time_taken}")
    
    # Plotting the results (optional)
    plt.bar(timings.keys(), timings.values())
    plt.xlabel('Sorting Algorithm')
    plt.ylabel('Time (seconds)')
    plt.title('Sorting Algorithm Efficiency')
    plt.show()

    

# Main function for CLI interactions
def main():
    # Initialize a BinarySearchTree to hold bids
    bst = BinarySearchTree()

    # Load bids from the "bids.csv" file. This step involves reading from a file and inserting each bid into the BST.
    # The efficiency of loading bids depends on the insert operation of the BST, which is O(log n) on average but can degrade to O(n) in the worst-case scenario (e.g., when the tree becomes unbalanced).
    bids = load_bids("bids.csv")
    for bid in bids:
        # Insert each bid into the Binary Search Tree.
        # This loop has a complexity that depends on the number of bids and the structure of the BST.
        bst.insert(bid)
    
    # After loading the bids into the BST, you could perform various operations such as searching for a specific bid,
    # displaying all bids, or even measuring the efficiency of different operations (as done in the measure_efficiency function).
    
    # Example of searching for a bid. The efficiency of this search is O(log n) on average due to the properties of the BST,
    # making it significantly faster than a linear search in a large dataset.
    search_bid_id = "some_bid_id"  # Placeholder for an actual bid ID you might be searching for
    found_bid = bst.search(search_bid_id)
    if found_bid:
        print(f"Found bid: ID={found_bid.bid_id}, Title={found_bid.title}, Amount={found_bid.amount}")
    else:
        print("Bid not found.")

    # Insert more CLI options as needed
    # For a comprehensive CLI, consider implementing options to allow the user to:
    # - Add a new bid
    # - Search for a bid by ID
    # - List all bids
    # Each option would call the appropriate function and display the results to the user.

# Utility function to load bids from a CSV file
# This function reads each row from the CSV, creating a Bid object and appending it to a list.
# The efficiency of this operation is primarily O(n) where n is the number of rows in the CSV file.
def load_bids(file_path):
    bids = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip the header row, assuming the first row is headers
        for row in reader:
            # Create a Bid object from each row and append to the list
            bids.append(Bid(row[0], row[1], row[2], float(row[3])))
    return bids

if __name__ == "__main__":
    main()
