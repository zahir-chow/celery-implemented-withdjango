



# arr = [5, 3, 8, 6, 7, 2]
# n = len(arr) # size of array is 5
# for i in range(n):
     
#      # Traverse through all array elements after index i 5
  
#     for  j in range(i + 1, n): 
#             if arr[i] > arr[j]:
#                arr[i], arr[j] = arr[j], arr[i]
               

# # find the avarage of largest and second largest elements
# largest = arr[-1]
# second_largest = arr[-2]

# key = (largest + second_largest) // 2  # (-2 + -4) // 2 = -3
# print("Key =", key)

# # Step 4: Binary Search
# low = 0
# high = len(arr) - 1
# found = False

# while low <= high:
#     mid = (low + high) // 2
#     if arr[mid] == key:
#         print(f"Key {key} found at index {mid}")
#         found = True
#         break
#     elif arr[mid] < key:
#         low = mid + 1   # search right half
#     else:
#         high = mid - 1  # search left half

# if not found:
#     print(f"Key {key} not found.")



def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    

    left = merge_sort(arr[:mid])   # Divide left
    print("Left:", left)
    right = merge_sort(arr[mid:])  # Divide right

    # Merge phase
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged += left[i:]
    merged += right[j:]

    return merged

# Example
arr = [5, 2, 8, 1, 4, 7, 3, 6]
sorted_arr = merge_sort(arr)
# print("Original:", arr)
# print("Sorted:", sorted_arr)
