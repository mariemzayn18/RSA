import common_functions as cf
import receiverClass as r
import senderClass as s
import time
import matplotlib.pyplot as plt

#--------------------------------- Mathematical attack ------------------------
def MA(C, n, e):
    recovered = ''
    Eve = r.Receiver()
    for p in range(2, int((n**0.5)+1)):
        if n % p == 0:
            Eve.q = n//p
            Eve.e = e
            Eve.p = p
            recovered = Eve.decrypt(cf.ConvertToStr(C))

    return recovered

#--------------------------------- CCA ------------------------

def CCA (C,n,e):
    # M => C
    # generate r that is co-prime with n
    r = cf.generate_e(n) 
    # compute C dash that will be sent to Bob using cipher text of the required msg
    C_dash=C* cf.PowMod( r,e,n)
    # Bob decrypts C dash and sends it back to Eve
    Y = cf.ConvertToInt( Bob.decrypt( cf.ConvertToStr( C_dash)))
    #Now, Eve can get the message:
    M= cf.PowMod( (Y* cf.modInverse(r,n)),1,n)
    recovered= cf.ConvertToStr(M)
    return recovered
 
    
#-------------------- Takes input from user -------------------
msg=input("Enter message: ")
time_or_test= input("To test attacks press 1, to test the key length vs time press 2: ")

if time_or_test=="1": 
    type= input("For MA press 1, For CCA press 2: ")


    #-------------------- Generate e,n,C for the attacks ------------
    Bob= r.Receiver()
    Alice = s.Sender()
    Bob_data = open("pq.txt", "r")
    lines = Bob_data.read().splitlines()
    i =0
    while i < len(lines)-1 :
        Bob.p=int(lines[i])
        Bob.q=int(lines[i+1])
        i+=3
    Bob_data.close() 
    Bob.e=cf.generate_e( (Bob.p-1) * (Bob.q-1))
    e= Bob.e
    #Sender: Alice
    Alice.set_public_key( Bob.p, Bob.q , Bob.e)
    cipher_text = Alice.encrypt(msg)
    C=cf.ConvertToInt(cipher_text)
    #write data in file that attacker will intercept
    with open( 'attacks_test.txt', 'w') as f:
        f.write(str(C)+ "\n")
        f.write(str(Bob.e) + "\n")
        f.write(str(Bob.p*Bob.q))
    f.close()    


    attacker_data = open('attacks_test.txt', "r")
    lines = attacker_data.read().splitlines()
    i =0
    while i < len(lines)-1:
        C=int(lines[i])
        e=int(lines[i+1])
        n=int(lines[i+2])
        i+=4
    attacker_data.close()


    # #---------------------------- Mathematical Attack --------------  
    if type == "1":

        recovered= MA(C, n, e)
        
        #write attack results and original message
        with open('MA_results.txt', 'w') as f:
            f.write("Original message: "+ msg+ "\n")
            f.write("Recovered message: "+ recovered + "\n")
            f.close()

        print("The attack is done, hard luck next time!")


    #------------------------------ CCA ATTACK -----------------

    elif type == "2":
    
        recovered= CCA(C, n, e)

        #write attack results and original message
        with open('CCA_results.txt', 'w') as f:
            f.write("Original message: "+ msg+ "\n")
            f.write("Recovered message: "+ recovered + "\n")
            f.close()

        print("The attack is done, hard luck next time!")

    else:
        print("please choose 1 or 2")




#---------------------------- Plotting -------------------------------

elif time_or_test== "2": 


    # -------------------- Generate p,q for n bits ---------------------
    with open('keylengthVsTimeAttack.txt', 'w') as f:
        for n in range(4,65,2):
            p,q=cf.generate_pq(n)
            f.write(str(p)+ "\n")
            f.write(str(q) + "\n")
            f.write("\n")
    f.close()  

    #---------------------------------------------------

    attack=input("Keylength vs Time, Choose 1 for MA, 2 for CCA: ")
    key_lengths=[]
    time_to_attack=[]
    Alice = s.Sender()
    Bob=r.Receiver()

    Bob_data = open("keylengthVsTimeAttack.txt", "r")
    lines = Bob_data.read().splitlines()
    i=0
    C_list=[]
    e_list=[]
    n_list=[]
    while i < len(lines)-2:
        Bob.p=int(lines[i])
        Bob.q=int(lines[i+1])

        Bob.e=cf.generate_e( (Bob.p-1) * (Bob.q-1))
        e= Bob.e
        #Sender: Alice
        Alice.set_public_key( Bob.p, Bob.q , Bob.e)
        cipher_text = Alice.encrypt(msg)
        C=cf.ConvertToInt(cipher_text)

        e=Bob.e
        n=Bob.p*Bob.q 

        key_lengths.append(len(bin(n).replace("0b", "")))

        start_time=time.time()
        if attack=="1":
            recovered= MA(C, n, e)
        elif attack=="2": 
            recovered= CCA(C, n, e)
    
        end_time=time.time()
        time_to_attack.append( end_time - start_time)

        #----------------- to only save results in a txt file 
        C_list.append(C)
        e_list.append(e)
        n_list.append(n)
        #--------------------------------------------

        i+=3
    
    Bob_data.close() 


    with open('dataForAttacker.txt', 'w') as f:
        for k in range(len(C_list)):
            f.write(str(C_list[k])+ "\n")
            f.write(str(e_list[k]) + "\n")
            f.write(str(n_list[k])+"\n")
            f.write("\n")
    f.close()  


    plt.plot(key_lengths,time_to_attack )
    plt.xlabel('Attack time')
    plt.ylabel('key length in bits')

    if attack== "1":
        plt.title('MA Attack ')
    else: 
        plt.title('CCA Attack ')
    plt.show()

else: 
    print("Please choose 1 or 2")