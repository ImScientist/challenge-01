# Coding challenge

## Task 
 
We wish to compute the laziest way to dial given n-digit number on a standard push button
telephone (with 12 keys) using two fingers. We assume that the two fingers start out on the * and
\# keys, and that the effort required to move a finger from one button to another is proportional to
the Euclidean distance between them.

Design an algorithm in python that computes the method of dialing that
involves moving your fingers the smallest amount of total distance.

## Solution 

Let `x_0, x_1, ... x__{n-1}` be the sequence of buttons that have to be pressed.    
Define a 'state' as a tuple composed of:   
    - the current fingers position, e.g. *#    
    - the traversed distance   
    - the used fingers registry which show which fingers are used to press the buttons. For example
    'LLRLRL' means that `x_0, x_1, x_3, x_5` were pressed with the left finger and `x_2, x_4` with the 
    right finger. 
    
The initial list of states has only one element: `(*#, 0, '')`.   

For every `x_j` in the sequence of buttons do the following:
  
  - generate all possible states from the initial list of states by moving
    your left or right finger to `x_j`. Update the corresponding traversed Euclidean distances 
    and the finger registries. For example, if `x_j = 5`:  
    ``` bash      
    [('28', 3.41, 'LRR')]      
    ```
    is mapped to  
    ``` bash      
    [('58', 4.41, 'LRRL'),
     ('25', 4.41, 'LRRR')]      
    ```
    
    In the end of this operation the number of states should be at most 44: at most 22 states where 
    the left, right finger is on `x_j`, respectively (this could be proved by induction). 
    
  - reduce the states:  
    If there are several states with the same finger position keep only the state with the smallest 
    traversed distance. For example:    
    ``` bash      
    [('86', 3.41, 'LRR'),
     ('96', 4.41, 'LLR'),         
     ('96', 5.06, 'RLR')]      
    ```
    is reduced to:  
    ``` bash      
    [('86', 3.41, 'LRR'),   
     ('96', 4.41, 'LLR')]      
    ```
    In the end of this operation the number of states should be at most 22: at most 11 states where 
    the left, right finger is on `x_j`, respectively (this could be proved by induction).   
    
    There is 
    a valid reason why states like `('96', 5.06, 'RLR')` are dismissed. If we know the best path 
    for `x_{j+1}, .. x_{n-1}` and apply it to all states with fingers position = '96' then all 
    of them will increase the traversed Euclidean distance by the same amount, i.e. the 
    dismissed state will never become the one with the lowest traversed Euclidean distance. 
    
       
   
After going through the whole sequence `x_0, x_1, ... x__{n-1}` pick the state with the 
smallest Euclidean distance. You can use the finger registry to reconstruct the movement 
of both fingers.   

## Complexity  

- Every `x_j` can take `k` different values.    
- For every button in this sequence there are `2(k-1)` possible finger configurations: 
`k-1` configurations where the left finger is on `x_j` and the right finger is 
somewhere else and vice versa.  
- In every iteration (j):
    - you can start with at most `2(k-1)` states, where either the left or the right 
    finger is on `x_{j-1}`. 
    - you can generate at most `4(k-1)` new states where the left or the right finger is on `x_j`.    
    - you can reduce the states to at most `2(k-1)` states.
    
- I was lazy in the implementation of the function that calculates the distance between two points. 
The `distance_dict` has `k^2` keys that contain all combinations between two points (and the 
corresponding distances)    

Time complexity:     
- The algorithm time complexity is `O(nk)` if we exclude the `distance_dict` initialization. If we 
take it into account the complexity will be `O(nk + k^2)`.  

Space complexity:  
- The space used to store the number sequence is linear in `n`.
- The space used to store all states for every iteration is `kn`. `n` origins from the 
finger registry (the last element of the state tuple) whose length grows to `n` in the 
last iteration. 
- The algorithm space complexity is `O(n + kn)` if we exclude the `distance_dict`. If we take it into 
account it is `O(n + kn + k^2)`.

## Test the algorithm 

- Setup the environment: 
    ```bash
    conda create -n challenge python=3.8 -y  
    conda activate challenge
    pip install -r requirements.txt
    pip install -e . 
    ```

- Compute the laziest path: 
    ```bash
    python compute_laziest_path.py --sequence 89602
    ```
  
- Measure how the computation time scales by increasing the number sequence length:
    ```bash
    python measure_complexity.py
    ```
