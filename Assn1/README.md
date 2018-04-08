## Assignment 1
Submitted on October 2, 2017<br>
 
### Problem: Uniform Cost Search
Implement uniform cost search for a program that can find a route between any two cities. Your program will be called find_route, and will take exactly three command-line arguments, as follows:
```
$ python find_route.py [input_filename] [origin_city] [destination_city]
```
An example command line is:
`$ find_route.py input1.txt Munich Berlin`

### Solution: Dijkstra's Algorithm
I used Dijkstra's algorithm for solution, which is a well known algorithm for finding shortest paths in a graph with only positive path costs. Here is [a video from YouTube](https://www.youtube.com/watch?v=GazC3A4OQTE) that helped me enormously for this solution.