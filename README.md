# fibonacci
## Efficient algorithm to calculate the n'th fibonacci number in O(log(n)) time 
F<sub>n</sub> represents the n'th fibonacci number.
F<sub>0</sub> = 0
F<sub>1</sub> = 1

F<sub>n</sub> = F<sub>k</sub>F<sub>n-k</sub> + F<sub>k-1</sub> F<sub>n-k-1</sub> (This proof is left to the reader)

Taking appropriate values for k : 

F<sub>n</sub> =	F<sup>2</sup><sub>(n+1)/2</sub> + F<sup>2</sup><sub>(n-1)/2</sub>	  if n is odd

F<sub>n</sub> =	F<sub>n/2</sub>* [   F<sub>n/2-1</sub> + F<sub>n/2+1</sub> ]	= F<sub>n/2</sub>* [   2* F<sub>n/2-1</sub> + F<sub>n/2</sub> ]	=	F<sub>n/2</sub>* [   2* F<sub>n/2+1</sub> - F<sub>n/2</sub> ]	if n is even


The function works by calculating pairs of fibonacci numbers (what I'm calling as a fibonacci vector or vibo for short). 
Each vector decomposes into another vibo vector. The exact one it decomposes into depends on whether the even or odd term is the greater one in the vector.
The process repeats until a known vector is gotten. By default the first 10 (F<sub>0</sub> = 0 to F<sub>10</sub> = 55 ) are stored. 
