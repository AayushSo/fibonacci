'''
f(n) represents the n'th fibonacci number.
f(0) = 0
f(1) = 1

f(n) = f(k)f(n-k) + f(k-1) f(n-k-1) (This proof is left to the reader)
Taking appropriate values for k : 
(a)	f(n) =	f( (n+1)/2 )^2 + f( (n-1)/2 )^2	  if n is odd, 2 means square
(b)	f(n) =	f(n/2)* [   f(n/2 -1) + f(n/2 +1) ]	if n is even
(c)	 	 =	f(n/2)* [   2* f(n/2 -1) + f(n/2) ]	if n is even
(d)	 	 =	f(n/2)* [   2* f(n/2 +1) - f(n/2) ]	if n is even

Defining :
f0(n) = (c) (Even case 0)
f1(n) = (d) (Even case 1)
f2(n) = (a) (Odd case)
( (b) is not used)

fib_dict is cache of fibonacci numbers. It can be updated/ reset as required.
By default it containts f(0) till f(10) inclusive

The function works by calculating pairs of fibonacci numbers (what I'm calling as a fibonacci vector or vibo for short). 
Each vector decomposes into another vibo vector, the exact on it decomposes into depending on whether the even or odd term is greater in the vector
'''


'''	
basic = [0,1,1,2,3,5,8,13,21,34,55]
fib_dict={i:basic[i] for i in range(len(basic))}

def rebasic(): #reset cache to basic_cache
	global fib_dict 
	fib_dict = {i:basic[i] for i in range(len(basic))}

def f1(fa,fb): #a>b
	#even case 1
	fa,fb = max(fa,fb) , min(fa,fb)
	return fb * (2*fa -fb)

def f0(fa,fb): #a>b
	#even case 0
	fa,fb = max(fa,fb) , min(fa,fb)
	return fa * (2*fb + fa)
	
def f2(fa,fb): #a>b
	#odd case
	#fa,fb = max(fa,fb) , min(fa,fb)
	return (fa**2) + (fb**2)

def vibo(n , update_dict = False): #vector_fibonacci
	# e.g. n = (1201,1200)
	was_init_1 = False
	#initial checks
	if type(n) is int:
		if n in fib_dict : return fib_dict[n]
		n = (n,n-1)
		was_init_1 = True
	if type(n) is float :
		n = (int(n),int(n)-1)
		was_init_1 = True
	if type(n[0]) is float or type(n[1]) is float:
		return None
	if n[1] > n[0] :
		print ("Input vector is flipped. Recalculating n")
		n = (n[1],n[0])
		print(n)
	if n[0] - n[1] != 1:
		print ("Input vector is not a fibonacci vector. Recalculating n")
		n = (n[0],n[0]-1)
		print(n)
	#step 1 : determine if lower of n is in basic. If so, we can directly return values from basic set
	if (n[0] in  fib_dict) and (n[1] in fib_dict) :
		return fib_dict[n[0]] , fib_dict[n[1]]
	
	else :
		#step 2 : determine odd value to generate a,b
		if n[0]%2==1 : i,f1_style = n[0], True #i,e,f1_style = n[0],n[1], True
		else : i, f1_style = n[1], False #i,e, f1_style = n[1],n[0], False
		
		#step 3 determine a,b to generate f(n[0]) , f(n[1])
		a,b = (i+1)>>1 , (i-1)>>1
		#print ("Calculating f(",a,") & f(",b,")")
		
		#step 4 : get f(a),f(b)
		fa,fb = vibo((a,b),update_dict)
		if update_dict :
			fib_dict[a] = fa
			fib_dict[b] = fb
		#print ("f(",a,")=",fa," & f(",b,")=",fb)
		
		#step 5 : use fa,fb to generate fn0, fn1
		if f1_style :
			#print("f1 style")
			if was_init_1 : return f2(fa,fb)
			else : return ( f2(fa,fb) , f1(fa,fb) )
		else: 
			#print("f0 style")
			if was_init_1 : return f0(fa,fb)
			else : return( f0(fa,fb) , f2(fa,fb) ) 
			
			
			
'''
from math import log10 as log 	
class Fibonacci:
	#fibonacci-number-generator object
	
	#Define core set of fibonacci numbers. Size can be determined based on size/speed trade-off of your project
	#By default, I have taken f(0)=0 till f(10)=55
	basic = (0,1,1,2,3,5,8,13,21,34,55)
		
	def fprint(self,*vars): #print if debugging is on
		if self.printerror:
			print(*vars)
	
	def __init__ (self, def_load = True, debug = False, boot=None):
		
		self.fib_dict={i:self.basic[i] for i in range(len(self.basic))}
		self.default_load = def_load
		self.printerror = debug
		self.ld={}
		
		if boot is not None : self.boot(boot)
		self.update_logtable()
	
	def restart(self): #reset cache to basic_cache
		self.fib_dict = {i:self.basic[i] for i in range(len(self.basic))}
	
	def update_logtable(self): #added log10(f(n)) support. IDK why but someone might want it I guess...
		self.ld={i:log(self.fib_dict[i]) for i in self.fib_dict if self.fib_dict[i]>0}# if i not in self.ld}
	
	def seq(self, stop, start=1,step=1): #returns sequence of fibonacci numbers start -> stop with default step =1
		return [self.fib(i) for i in range(start, stop, step)]
	
	def fib(self,n): #returns fib(n)
		if n in self.fib_dict : return self.fib_dict[n]
		else: return self.vibo(n)
			#if self.default_load : self.fib_dict[n]
	
	def f1(self,fa,fb): #a>b #magic spice
		#even case 1
		fa,fb = max(fa,fb) , min(fa,fb)
		return fb * (2*fa -fb)

	def f0(self,fa,fb): #a>b #magic spice
		#even case 0
		fa,fb = max(fa,fb) , min(fa,fb)
		return fa * (2*fb + fa)
		
	def f2(self,fa,fb): #a>b #magic spice
		#odd case
		return (fa**2) + (fb**2)

	def boot(self,n): #add values to internal dict up to 'n' whether or not default_load is False or not
		for i in range(n,max(self.fib_dict),-1):
			if not i in self.fib_dict: self.fib_dict[i] = self.vibo(i)
		
	def vibo(self,n): #vector_fibonacci
		was_init_1 = False
		update_dict = self.default_load
		
		#initial checks
		if type(n) is int:
			if n in self.fib_dict :
				self.fprint("int found in dict")
				return self.fib_dict[n]
			n = (n,n-1)
			was_init_1 = True
		if type(n) is float :
			n=int(n)
			if n in self.fib_dict : return self.fib_dict[n]
			n = (n,n-1)
			was_init_1 = True
		if type(n[0]) is float or type(n[1]) is float:
			raise Exception
		if n[1] > n[0] :
			self.fprint ("Input vector is flipped. Recalculating n")
			n = (n[1],n[0])
			self.fprint(n)
		if n[0] - n[1] != 1:
			self.fprint ("Input vector is not a fibonacci vector. Recalculating n")
			n = (n[0],n[0]-1)
			self.fprint(n)
		
		#step 1 : determine if n is in basic. If so, we can directly return values from basic set
		if set(n) <= set(self.fib_dict) : #(n[0] in  fib_dict) and (n[1] in fib_dict) :
			self.fprint("Values found in dict.")
			return self.fib_dict[n[0]] , self.fib_dict[n[1]]
		
		else :
			#step 2 : determine odd value to generate a,b
			if n[0]%2==1 : i,f1_style = n[0], True #i,e,f1_style = n[0],n[1], True
			else : i, f1_style = n[1], False #i,e, f1_style = n[1],n[0], False
			self.fprint("i,f1_style:",i,f1_style)
			
			#step 3 determine a,b to generate f(n[0]) , f(n[1])
			a,b = (i+1)>>1 , (i-1)>>1
			self.fprint("a,b=",a,b)
			
			#step 4 : get f(a),f(b)
			fa,fb = self.vibo((a,b))
			self.fprint("a,fa,b,fb=",a,fa,b,fb)
			
			#step 5 : use fa,fb to generate fn0, fn1, fn2
			fibnum = (self.f0(fa,fb),self.f1(fa,fb),self.f2(fa,fb))
			
			#optional step : memoization
			if update_dict :
				if not n[0] in self.fib_dict : self.fib_dict[n[0]] = fibnum[2] if f1_style else fibnum[0]
				if not n[1] in self.fib_dict : self.fib_dict[n[1]] = fibnum[1] if f1_style else fibnum[2]
				# if f1_style:
					# if not n[0] in self.fib_dict : self.fib_dict[n[0]] = fibnum[2]
					# if not n[1] in self.fib_dict : self.fib_dict[n[1]] = fibnum[1]
				# else:
					# if not n[0] in self.fib_dict : self.fib_dict[n[0]] = fibnum[0]
					# if not n[1] in self.fib_dict : self.fib_dict[n[1]] = fibnum[2]
			
				
			if f1_style :
				if was_init_1 :
					return fibnum[2]#self.f2(fa,fb)
				else : return (fibnum[2],fibnum[1])#( self.f2(fa,fb) , self.f1(fa,fb) )
			else: 
				#print("f0 style")
				if was_init_1 : return fibnum[0] #self.f0(fa,fb)
				else : return (fibnum[0],fibnum[2]) #( self.f0(fa,fb) , self.f2(fa,fb) ) 
				
				
				
