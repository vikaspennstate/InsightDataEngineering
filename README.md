This refers to my solution to Insight DataScience Edgar Analytics challenge from following url : 

https://github.com/InsightDataScience/edgar-analytics



# Table of Contents
1. [Requirements](README.md#Requirements)
2. [Approach](README.md#Approach)

# Requirements

We need to install following :

pip install dateutil
 
pip install pytest

# Approach

After understanding the problem. I came up with two approaches.
_The code is only provided for approach 2(that is preferred too) since i could have submitted only one code._

I shall discuss both approaches one by one.

- First Approach:

Create a dictionary.

whenever a new line is read, look if this is in the dictionary:
 
    No: Add this to dictionary and also write this to file.
 
    Yes: compare the visittime with the last access time for this ip address:
 
  If visittime indicates that previous session is expired:
  
    replace the old entry from dict with new one and also write to file
   
  else:
    
    update dictionary item and also the file
    

_Drawbacks of above approach:_
   
   + The main tenat of a distributed application is scalability and high availability. Since we are always stacking the dictionary and never removing the old data, lets say there are more than a million ip addresses that access our application. Having such a dictionary in memory may not be possible and we may have to keep some part in disk/cache which may result in page faults and bad performance.

   + On each line read, we are required to update the file, and file connections resources are expensive. This will slow down each iteration by a constant time as compared to an approach that may write to file in bulk.



- Second Approach:

I created two data structures

1st is  ordred dictionary(visitsDict) that stores key value pair of ip address and a list of _[session start time, latest session visit time, session duration, number of visits till now ,order]_ 
order is the order in which the request was read from log file

2nd shall be a min heap(heapOfLastAccess) of a tuple containing latest session visit time, ip address
this heap is used so we can efficiently extract the expired sessions in log(n) time.

whenever we see a next line from log file, we compare its time with top element from heap and if time difference is greater than timeout, we keep extrating heap top till time difference from heap top is < timeout. 

      All elements taken from heap in this way shall be the ones whose session time has expired now.

Now we check via ip address(that is 2nd value in tuple of heap) into our dictionary, store these items in sorted list(sorted by order field from dictionary as this is the requirement of problem statement -  _If your program is able to detect multiple user sessions ending at the same time, it should write the results to the sessionization.txt output file in the same order as the user's first request for that session appeared in the input log.csv file._), 
write them to file sessionization.txt and and delete all these elements from dictionary

Also if the latest read line's ip was not in dictionary previously, we just add it to both heap and dict.

In the end(log file read is finished) we get all elements from dictionary and put them into sessionization.txt


* Why is this approach better:
          
          As we are keep on removing elemnts from both dictionary and heap, the size shall never grow 
          too much.
          
          We are only writing to files ones we have found a line from stream where atleast one ip 
          address session is expired.
        




