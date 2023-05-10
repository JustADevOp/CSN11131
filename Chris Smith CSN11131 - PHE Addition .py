#Imports
import Cryptodome                                          #https://pycryptodome.readthedocs.io/en/latest/src/installation.html
from Cryptodome import Random                              #https://pycryptodome.readthedocs.io/en/latest/src/random/random.html?highlight=Random
from Cryptodome.PublicKey import ElGamal                   #https://pycryptodome.readthedocs.io/en/latest/src/public_key/elgamal.html?highlight=Elgamal#Crypto.PublicKey.ElGamal.ElGamalKey.publickey
import libnum                                              #https://pypi.org/project/libnum/

#End Imports

listRawData_array=[]                                        #A global array for testing. To check the plaintext decyphered from ciphertexts in the Decrypt function is correct the plaintext inputs from Enc function are saved here. In a real world system this would not exist.

def main(): 
    key = ElGamal.generate(256, Random.new().read)          #Using the Elgamal library from Crytodome, create a key with a 256bit prime and save it in the object "key"
    public_key = key.publickey()                            #From "key", take the public key and store in "public_key"
    #g = key.g                                              #From the "key" object extract the generator value (g). Use this if you want to use a generated generator rather than a static value set below. 
    #p = key.p                                              #From the "key" object extract the Prime value (p). Use this if you want to use a generated Prime greater than 128 bit instead of the static value set below. Warning, this will increase compute time.
    #x = key.x                                              #From the "key" object extract the private key value (x). Use this if you want to use a generated x rather than a static value set below. 
    #y = public_key.y                                       #From the "key" object extract the public key value (y). Use this if you want to use a generated y rather than a static value set below. 

    g=5                                                     #Manaully set g for testing
    p=9223372036854775807                                   #Manually set prime for testing
    x=7                                                     #Manually set x for testing
    y=(g**x)%p                                              #Calculated public key for testing.

    lista_array=[]                                          #Create an array to hold recieved cyphered a values
    listb_array=[]                                          #Create an array to hold recieved cyphered b values

    randomRounds=Cryptodome.Random.random.getrandbits(6)    #To simulate a varying number of systems sending data. 
    print("_____________________________")                  #Output formatting for visability
    print("Number of submissions will be ",randomRounds)    #Print the number of rounds
    print("-----------------------------")                  #Output formatting for visability
    for rounds in range (0,randomRounds):                   #For loop to create several cipher texts
        a,b =Enc(p,g,y)                                     #Call the Enc function & send the public key (p, g, y) - This function would be done by a remote system in real world. This function returns a and b ciphertext as a real remote system would.
        lista_array.append(a)                               #Save the a Value from the Enc function and save this cipher in the array
        listb_array.append(b)                               #Save the b Value from the Enc function and save this cipher in the array
    
    
    Decrpyt(lista_array, listb_array,x,g,p )                #Start the Decrypt function passing it the two arrays of a and b, plus the prime (p), generator (g) and Private key (x)


def Enc(p,g,y):                                             #Encryption function, takes the p, g and y values from main(). It takes a message, ciphers it and then returns those. This simulates a remote system.
    m=Cryptodome.Random.random.randrange(1, 25, 1)          #Using the Cryptodome library select a random value between 1 and 25 to be the message (m). In real world this would either be manually entered or taken from a database. Randomly creating integer to be ciphers allows for better testing as will be different each loop of this function.
    k=Cryptodome.Random.random.getrandbits(16)              #Create a random number of 16 bit length which will be used to cipher the message (m).
    a=(g**k)%p                                              #Create the "a" value by taking g and powering to the k value (random value), then muliply by the result of generator to power of the mesage (m), finally mod the result by the prime (p)
    b=((y**k)*(g**m))%p                                     #Cipher for additition, this differs to normal ElGamal Ciphering. Create the "b" value by taking the public key (y) to the power of the random value (k), then mulitply this by the generator (g) to the power of the message (m), finally mod the result by the prime (p)
    listRawData_array.append(m)                             #For Testing purposes, log the raw input data into the Global array for later addition + compare to decyphered data. In a real world setup this would not exist.
    return a,b                                              #Return values a and b. This would be the remote system sending the cipher to the central server in a real world setup.
 

def calc_listRawData_array():                               #Test Function to calculate the addition of raw inputs from the Enc function. In a real world setup this would not exist. Called as part of the Decrypt function.
    RawTotal=0                                              #Create a variable to add to for each entry in the listRawData_array.
    for a in listRawData_array:                             #For each a value in the listRawData_array
        RawTotal=RawTotal+a                                 #Take the current total (RawTotal) and the a value from the listRawData_array and add them together and store in the RawTotal variable.
    return RawTotal                                         #Return the RawTotal Variable 
    

def multia(lista):                                          #Function to take the values from lista_array (passed to this function as lista) and add multiply them together to create a=a1*a2*a3*a4... etc. Also counts the number of ciphertexts received to later calculate the Mean.
    aTotal=1                                                #Create the aTotal variable to hold the results of each calculation. Start at 1 so that the first a value to come out the lista_array is multiplied by 1 and gives its own value as the new aTotal.
    counter=0                                               #Create the counter variable to hold the count of ciphertexts processed. 
    for a in lista:                                         #Loop through all entries in the lista array 
        aTotal=aTotal*a                                     #Get the value of the aTotal and multiply it by the current a value take from lista, then store in the aTotal variable.
        counter=counter+1                                   #Get the value of counter and add one to it, then store in counter variable.
    return aTotal, counter                                  #Return the total of the a values being multiplied as one value. aTotal = a = a1*a2*a3*a4... and the total number of ciphertexts received.


def multib(listb):                                          #Function to take the values from listb_array (passed to this function as listb) and add multiply them together to create b=b1*b2*b3*b4... etc
    bTotal=1                                                #Create the bTotal variable to hold the results of each calculation. Start at 1 so that the first a value to come out the listb_array is multiplied by 1 and gives its own value as the new bTotal.
    for b in listb:                                         #Loop through all entries in the listb array
        bTotal=bTotal*b                                     #Get the value of the bTotal and multiply it by the current a value take from listb, then store in the bTotal variable.
    return bTotal                                           #Return the total of the b values being multiplied as one value. bTotal = b = b1*b2*b3*b4... 


def Decrpyt(lista_array, listb_array,x,g,p):                #Function to take the calculated a and b values from multia and multib functions, then bruteforce a check to find a match, after which this is divided by the count of ciphers recieved (as counted in multia3 function). Called by main function and passed lista_array, listb_array, Private key (x), generator (g) and the prime (p).
    a,CiphersRecieved =multia(lista_array)                  #Call the function multia and pass it the lista_array which holds all the received a values. Returns the values a (all a values multiplied a = a1*a2*a3*a4...) and the total number of ciphers.
    b=multib(listb_array)                                   #Call the function multib and pass it the listb_array which holds all the received b values. Returns the values b (all b values multiplied b = b1*b2*b3*b4...)
    m=(b*libnum.invmod(((a**x)%p),p)) % p                   #create m variable to hold the computed addition. This takes the b value (b = b1*b2*b3*b4...) and inverse mods the result of a (a = a1*a2*a3*a4...) to the power of private key x mod prime (p) by prime (p).
    print("_____________________________")                  #Output formatting for visability
    print("Resulting Cipher Text (m) ",m)                   #Print the result of the m calculation adding the ciphers together.
    print("-----------------------------")                  #Output formatting for visability
    plainTextnumber=0                                       #Create plainTextnumber variable. This will be used to store each round of the brute force attempt to find a match of plaintext to the ciphertext.
    for i in range (1,10000000):                            #For every integer between 1 and 10000000 the program will take the integer and encrypt it. If the encrypted value of i matches the m value (ciphered result of additions) then i is the plaintext number of m.
        BruteforceAttempt=(g**i)%p                          #Create a variale to store the ciphered i integer. Take the integer i and cipher it by powering to the generator (g) and modding the result by the prime (p)
        if BruteforceAttempt==m:                            #Check to see if the BruteforceAttempt variable storing the ciphered i value matches the message m.
            print("_____________________________")          #Output formatting for visability            
            print("Deciphered Number is = ",i)              #Print to report the match was found and print the value of i .
            print("-----------------------------")          #Output formatting for visability
            plainTextnumber=i                               #set the variable plainTextnumber previously created and store the value of i.
            break                                           #End the for loop.
        else:                                               #If the last check of BruteforceAttempt against message (m) didn't match, then add 1 to the value i and start the loop again.
            i=i+1                                           #Take the value of i and add 1, then store this in i for the next loop.
    addedRaw_Data=calc_listRawData_array()                  #Create a new variable addedRaw_Data and call the function calc_listRawData_array. This is a testing function and would not exist in the real world. This function takes the plaintext values from listRawData_array and adds them together and returns the value. This exists only to check the deciphered output matches the raw data addition.
    print("_____________________________")                  #Output formatting for visability.
    print("Rawdata is ", addedRaw_Data)                     #Print the Test data additions. This would not exist in the real world and is only here for testing / verification.
    print("-----------------------------")                  #Output formatting for visability.
    MeanAverage=plainTextnumber//CiphersRecieved            #Create a new variable MeanAverage to store the result of plainTextnumber (the plaintext value of m) divided to a round figure by CyphersRecieved (Ciphers were counted in function multia).
    print("_____________________________")                  #Output formatting for visability.
    print("Deciphered Number/Number of Ciphers")            #Print the Calculation explained.
    print(plainTextnumber,"/",CiphersRecieved,"=",MeanAverage)#Print the calculation
    print("-----------------------------")                  #Output formatting for visability
if __name__ in "__main__":                                  #On start look for function main.
    main()                                                  #If main exists run the main function.
