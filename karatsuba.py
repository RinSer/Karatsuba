#!/usr/bin/env python
"""
My script to multiply ultra-long decimal numbers
using the Karatsuba algorithm.

created by RinSer
"""

FIRST = '3141592653589793238462643383279502884197169399375105820974944592'
SECOND = '2718281828459045235360287471352662497757247093699959574966967627'
ANSWER = '8539734222673567065463550869546574495034888535765114961879601127067743044893204848617875072216249073013374895871952806582723184'


class Decimal:
    """
    Class for objects that store ultra-long
    decimal numbers.
    Contains 3 fields:
    string to store the text representation of number
    length to store the length of number
    decimal array to store the digits as ints from 0 to 9
    """
    def __init__(self, string):
        self.string = string
        # Check the string for leading zeros
        if len(string) > 0 and string[0] == '0':
        	leading_zeros = 0
        	while leading_zeros < len(string) and string[leading_zeros] == '0':
        		leading_zeros += 1
        	string = string[leading_zeros:]
        self.length = len(string)
        self.digits = list()
        for char in string:
            self.digits.append(int(char))
        self.digits = list(reversed(self.digits))

    def __str__(self):
        return self.string

    def add(self, other_decimal):
        """
        Method to summate current Decimal number
        with another one.
        Returns the sum as Decimal number object.
        """
        sum = Decimal('0')
        # Find the longest number
        if self.length > other_decimal.length:
            first = self.digits
            second = other_decimal.digits
        else:
            first = other_decimal.digits
            second = self.digits
        # Summation
        for index in range(len(first)):
            if index < len(second):
                digit = first[index] + second[index]
                if index < len(sum.digits):
                    sum.digits[index] += digit
                else:
                    sum.digits.append(digit)
            else:
                if index < len(sum.digits):
                    sum.digits[index] += first[index]
                else:
                    sum.digits.append(first[index])
            if sum.digits[index] > 9:
                sum.digits[index] = sum.digits[index] % 10
                sum.digits.append(1)
        # Adjust sum object
        sum.string = ''
        for digit in reversed(sum.digits):
            sum.string += str(digit)
        sum.length = len(sum.string)

        return sum

    def subtract(self, other_decimal):
		"""
		Method to subract current Decimal from the other.
		!The other decimal should be smaller than current!
		Returns the difference as Decimal number object.
		"""
		# Subtraction
		difference = list(self.digits)
		for index in range(len(other_decimal.digits)):
			try:
				p = difference[index] < other_decimal.digits[index]
			except:
				print self.string
				print other_decimal.string
				print difference
			if difference[index] < other_decimal.digits[index]:
				difference[index] = difference[index] + 10 - other_decimal.digits[index]
				if difference[index+1] > 0:
					difference[index+1] -= 1
				else:
					jndex = 1
					while difference[index+jndex] == 0:
						difference[index+jndex] = 9
						jndex += 1
					difference[index+jndex] -= 1
			else:
				difference[index] -= other_decimal.digits[index]
		# Create the difference object
		string = ''
		for digit in reversed(difference):
			string += str(digit)
		if len(string) > 1 and string[0] == '0':
			string = string[1:]
		
		return Decimal(string)

    def multiply(self, other_decimal):
		"""
		Method to multiply current Decimal by the other 
		using the Karatsuba algorithm.
		Return the product as Decimal number object.
		"""
		# Base case
		if self.length < 2 or other_decimal.length < 2:
			first = int(self.string)
			second = int(other_decimal.string)
			return Decimal(str(first*second))
        # The algorithm
        # Find the n to cut numbers
		length_cut = max(self.length, other_decimal.length)
		cut = length_cut/2
		if length_cut % 2 != 0:
			cut += 1
		# Find a, b, c and d strings
		strings = list()
		strings.append(self.string[::-1][cut:][::-1])
		strings.append(self.string[::-1][:cut][::-1])
		strings.append(other_decimal.string[::-1][cut:][::-1])
		strings.append(other_decimal.string[::-1][:cut][::-1])
		# Check for empty numbers
		for string in strings:
			if string == '':
				first = int(self.string)
				second = int(other_decimal.string)
				return Decimal(str(first*second))
		# Create a, b, c and d numbers
		number_a = Decimal(strings[0])
		number_b = Decimal(strings[1])
		number_c = Decimal(strings[2])
		number_d = Decimal(strings[3])
		# Calculate z0=b*d, z1=(a+b)*(c+d)-a*c-b*d, z2=a*c
		b_times_d = number_b.multiply(number_d)
		a_times_c = number_a.multiply(number_c)
		a_plus_b = number_a.add(number_b)
		c_plus_d = number_c.add(number_d)
		a_plus_b_times_c_plus_d = a_plus_b.multiply(c_plus_d)
		ad_plus_bc_minus_a_times_c = a_plus_b_times_c_plus_d.subtract(a_times_c)
		ad_plus_bc = ad_plus_bc_minus_a_times_c.subtract(b_times_d)
		# Assemble the product: (z2*10)^(2*n)+z1*10^n+z0
		upper = Decimal(a_times_c.string+('0'*(cut*2)))
		middle = Decimal(ad_plus_bc.string+('0'*cut))
		lower = middle.add(b_times_d)
		return upper.add(lower)
		


first = Decimal(FIRST)
second = Decimal(SECOND)
product = first.multiply(second)
assert product.string == ANSWER
print product

