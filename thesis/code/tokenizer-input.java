/**
    Returns the largest int in a list of integers
 */
public int getLargestInt(List<Integer> items) {
    int largestElement = Integer.MIN_VALUE;

    for (int i = 0; i < items.size(); i++) {
        if (items.get(i) > largestElement) {
            largestElement = items.get(i);
        }
    }

    return largestElement;
}