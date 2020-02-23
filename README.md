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
    and the finger registries.   
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
   
After going through the whole sequence `x_0, x_1, ... x__{n-1}` pick the state with the 
smallest Euclidean distance.   

## Complexity  

- Every `x_j` can take `k` different values.    
- For every button in this sequence there are `2(k-1)` possible finger configurations: 
`k-1` configurations where the left finger is on `x_j` and the right finger is 
somewhere else and vice versa.  
- In the beginning of every iteration you can start with at most `2(k-1)` states, 
generate `4(k-1)` new states and then reduce them to at most `2(k-1)` states.

It follows that:
- The computation time depends linearly on the sequence length `n`, i.e. we have `O(n)` complexity.   
- The computation time depends linearly on number of keys `k`, i.e. we have `O(k)` complexity.   
- The algorithm complexity is `O(nk)`

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
  
- Measure how the model scales by increasing the number sequence length:
    ```bash
    python measure_complexity.py
    ```
