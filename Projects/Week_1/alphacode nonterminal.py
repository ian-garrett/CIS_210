CONSANANTS = "bcdfghjklmnpqrstvwyz"
VOWELS = "aeiou"

pincode =int( input("Enter PIN number "))
chunk_1 = pincode%100
new_pincode_1 = pincode//100
chunk_2 = new_pincode_1%100

consonant1 = CONSANANTS[chunk_1//5]
vowel1 = VOWELS[chunk_1%5]

consonant2 = CONSANANTS [chunk_2//5]
vowel2 = VOWELS[chunk_2%5]

pair1 = (consonant1 + vowel1)
pair2 =(consonant2 + vowel2)

print ("Encoding of", pincode, "is", pair1 + pair2)
