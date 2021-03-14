
#  Copyright (C) 2021 Aayush Soni <aayush.soni795@gmail.com>
# 
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation.
# 
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://gnu.org/licenses/gpl-3.0.txt>

'''
Example Use:
from efficient_fibonacci import Fibonacci as F
f=F()
f.seq(20)
 returns : [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181]
 f.fib(200)
 returns : 280571172992510140037611932413038677189525
 f.fib_dict
 returns : {0: 0, 1: 1, 2: 1, 3: 2, 4: 3, 5: 5, 6: 8, 7: 13, 8: 21, 9: 34, 10: 55, 11: 89, 12: 144, 13: 233, 14: 377, 15: 610, 
 		16: 987, 17: 1597, 18: 2584, 19: 4181, 25: 75025, 24: 46368, 50: 12586269025, 49: 7778742049, 100: 354224848179261915075,
 		99: 218922995834555169026, 200: 280571172992510140037611932413038677189525, 199: 173402521172797813159685037284371942044301}
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
	
	def __init__ (self, def_load = True, debug = False, boot=None, use_log = False):
		# def_load : turn on memoization (update internal dict when calculating any new value)
		#debug : prints internal steps if debog is True.
		#boot : initializes internal dict up to 'n' places (if value is given.)
		#use_log : calculate & store log(F(n))
		
		self.fib_dict={i:self.basic[i] for i in range(len(self.basic))}
		self.default_load = def_load
		self.printerror = debug
		
		if boot is not None : self.boot(boot)
		if use_log :
			self.ld={} #log-dict
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
			
			if f1_style :
				if was_init_1 :
					return fibnum[2]
				else : return (fibnum[2],fibnum[1])
			else: 
				if was_init_1 : return fibnum[0]
				else : return (fibnum[0],fibnum[2]) 
				
				
				
