#1
name = input("Enter your fullname: ")
print(name.upper()) 

#2
word = "python"
print(" first charact is", word[0],  "\n last charact is", word[-1])

#3
name = input("Enter your name: ")
print("Hello, !", name)

#4
text = "Welcome to python"
print(text.find(text[-1]))

#5
word_2 = "Hello world"
new_word_2 = word_2.replace("world", "python")
print(new_word_2)

#6
print("python"  in new_word_2)

#7
a ="Hello"
print(a[-1:-6:-1])

#8
word_2 = "  Hello world   "
# print(word_2.strip())

#9
vowel_count = input("Enter a short sentence: ")
a = vowel_count.count("a")
e = vowel_count.count("e")
i = vowel_count.count("i")
o = vowel_count.count("o")
u = vowel_count.count("u")
total_vowel = a+e+i+o+u
print("the total vowel in the sentence is:", total_vowel)

#10
string_1 = "1234"
conv_string = int(string_1) * 2
print("conv_string")

#11
string_1 = "apple banana orange"
print(string_1.split())

#12
user_input = input("Enter a sentence: ")
input_conv = user_input.split()
print("\n/".join(input_conv))

#13
string_1 = "Hello user welcome"
print(string_1.replace(" ","_"))

#14
string_1 = "banana"
string_count = string_1.count("a")
print(string_count)


#15
word_1 = "https://"
print("word_1".isalpha())