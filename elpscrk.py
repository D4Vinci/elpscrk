#Author:D4Vinci
#A Script That Looks Like The BruteForce Script That Eliot Used it in Mr.Robot Series Episode 01 :D :v
#For Any Advice Contact Me At : fb/kareem.shoair

import itertools,time,sys,threading
from time import gmtime, strftime

m1=[];m2=[]
f1=[];f2=[];f3=[];f4=[]
ff5=[];ff6=[];ff7=[];ff8=[];ff9=[];ff10=[];ff11=[];ff12=[]
start_time = time.time()
def cw(lista,n):             #split one list to two
    return lista[:len(lista)/n],lista[len(lista)/n:]

def all(l1,l2,n):
    lol=[]          #Combine the strings of two lists and add it to list
    for a in l1:
        for b in l2:
            o=a+b
            lol.append(o)
    latest=[]

    def now_fuck(lol,latest,n):  #Creating random strings from list and add it to another list
        for latest_fuckin_thing in lol:
            za3bola=[''.join(x for x in t) for t in itertools.product(latest_fuckin_thing,repeat=n)]
            latest.append(za3bola)
    now_fuck(lol,latest,n)
    return latest

def combin(lolo, lala):
    for lelo in lolo:   #Combine the strings of two lists
        for lola in lala:
            yield lelo + lola

def main():
    print "\n[!]Started at "+str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))+"\n"

    keys=raw_input("Info (Split It)->").replace(" ",";").replace(",",";").split(";")
    num=input("\nLength Of The Pwd: ")
    print "\n[+]Spliting Chars....\n" #To make it faster and simpler
    m1,m2=cw(keys,2)
    nn=2
    if keys:
        if len(keys)>=16: #use it if info is more than 16 or equal
            f1,f2=cw(m1,len(m1)/nn)
            f3,f4=cw(m2,len(m2)/nn)

            ff5,ff6=cw(f1,len(f1)/nn)
            ff7,ff8=cw(f2,len(f2)/nn)
            ff9,ff10=cw(f3,len(f3)/nn)
            ff11,ff12=cw(f4,len(f4)/nn)
            print "[+]Generating Passlist 1...\n"
            oo1=all(ff5,ff6,num)
            print "[+]Generating Passlist 2...\n"
            oo2=all(ff7,ff8,num)
            print "[+]Generating Passlist 3...\n"
            oo3=all(ff9,ff10,num)
            print "[+]Generating Passlist 4...\n"
            oo4=all(ff11,ff12,num)
            print "[+]Combining and Generating Finallist...\n"
            cl1=list(combin(oo1,oo2))
            cl2=list(combin(oo3,oo4))
            combined_list=list(combin(cl1,cl2))

        elif len(keys)>8 and len(keys)<16: #use it if info is more than 8 or less than 16
            f1,f2=cw(m1,len(m1)/nn)
            f3,f4=cw(m2,len(m2)/nn)
            print "[+]Generating Passlist 1...\n"
            oo1=all(f1,f2,num)
            print "[+]Generating Passlist 2...\n"
            oo2=all(f3,f4,num)
            print "[+]Combining and Generating Finallist...\n"
            combined_list=list(combin(oo1,oo2))

        elif len(keys)<=8:  #use it if info is less than 8 or equal
            nn=1
            print "[+]Generating Passlist ...\n"
            oo=all(m1,m2,num)
            print "[+]Combining and Generating Finallist...\n"
            combined_list=list(oo)

        final_list=[]

        for soso in combined_list: #Make all of that shit in one list
            for fofo in soso:
                final_list.append(fofo)
        cleared_list=dict.fromkeys(final_list).keys() #Remove Repeated strings from the list
        final_list=cleared_list

        #Finally Finished :D
        wordlist_file=open('Wordlist.txt','w') #write it in a text file
        for pwd in final_list:
            wordlist_file.write(str(pwd)+'\n')
        wordlist_file.close()

        print "~#~ Wordlist Created >> {} Passwords".format(len(final_list))
        print '\n~#~Passwords Written in Wordlist.txt'
        print "\n[!]Finished In {} Second(s).".format(int(time.time() - start_time))
        print "\n# # # Happy Hunting # # #\n"

t1 = threading.Thread(target=main)
t1.start()
t1.join()
#if raw_input("Do You Wanna Print It (Y/N) : ").lower() in ['y','yes']:
#    print final_list
