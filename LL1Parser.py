'''
Lab Question Name: LL(1) Parser
Made By: Aahan Singh Charak
Section:CSE-A
Registration Number:189301024
License:M.I.T

'''

'''
E -> TL
L -> +TL | empty
T -> FM
M -> *FM | empty
F -> a | (E)
========================================================================================
========================================================================================

First Follow table is :

Variable         |         First         |          Follow                 |
----------------------------------------------------------------------------
E                |        {a,(}          |           {$,)}                 |
---------------------------------------------------------------------------
L                |        {+,empty}      |           {$,)}                 |
----------------------------------------------------------------------------
T                |        {a,(}          |           {+,$,)}               |
----------------------------------------------------------------------------
M                |        {*,empty}      |           {+,$,)}               |
----------------------------------------------------------------------------
F                |        {a,(}         |           {*,+,$,)}              |
----------------------------------------------------------------------------
========================================================================================
========================================================================================


The LL(1) parse table can be given by:

Variable         |    a     |     +    |     *    |    (     |    )     |   $
--------------------------------------------------------------------------------
E                |E ->TL    |          |          |E -> TL   |          |  
--------------------------------------------------------------------------------
L                |          |L->+TL    |          |          |L->empty  |L->empty
--------------------------------------------------------------------------------
T                |T ->FM    |          |          |T -> FM   |          |       
--------------------------------------------------------------------------------
M                |          |M->empty  |M->*FM    |          |M->empty  |M->empty
--------------------------------------------------------------------------------
F                |F->a      |          |          |F->(E)    |          |  
========================================================================================
========================================================================================




'''
results=['|'.join(['Stack'.center(60,' '),'Symbol'.center(60,' '),'Rule'.center(60,' ')])]
# stack creater
class Stack:
    def __init__(self) -> None:
        self.stack=['$']
    def push(self,symbol):
        self.stack.append(symbol)
    def pop(self):
        self.stack.pop()

#main parser
class Parser:
    def __init__(self,parseString) -> None:
        self.table={
            'E':{
                'a':'TL',
                '+':None,
                '*':None,
                '(':'TL',
                ')':None,
                '$':None
            },
            'L':{
                 'a':None,
                '+':'+TL',
                '*':None,
                '(':None,
                ')':'empty',
                '$':'empty'
            },
            'T':{
                'a':'FM',
                '+':None,
                '*':None,
                '(':'FM',
                ')':None,
                '$':None

            },
            'M':{
                'a':None,
                '+':'empty',
                '*':'*FM',
                '(':None,
                ')':'empty',
                '$':'empty'
            },
            'F':{
                 'a':'a',
                '+':None,
                '*':None,
                '(':'(E)',
                ')':None,
                '$':None
            }
        }
        self.terminals=['E','L','T','M','F']
        self.nonTerminals=['a','+','*','(',')','$']
        self.string=parseString

    #method to exit the programme on failing
    def printErrorMessage(self):
        print('String cannot be parsed using this parser')
        print('**************************')
        exit()

    
    #method to start parsing
    def parse(self,st):
        st.push('E')
        pointer=0
        valid=True
        while(valid):
            char=self.string[pointer]
            resString='{}'.format(st.stack).center(60,' ')+'|'+'{}'.format(char).center(60,' ')
            if char not in self.terminals and char not in self.nonTerminals:
                valid=False
                self.printErrorMessage()
            else:
                stackTop=st.stack[len(st.stack)-1]
                if stackTop=='$' and char=='$':
                    print('String parsed by the parser')
                    break
                elif stackTop==char:
                    st.pop()
                    pointer+=1
                    resString+='|'+'{}'.format('').center(60,' ')
                    results.append(resString)
                    continue
                try:
                    transition=self.table[stackTop][char]
                    if not transition:
                        raise Exception()
                    elif transition=='empty':
                        st.pop()
                    else:
                        st.pop()
                        st.stack.extend(list(transition)[::-1])
                    resString+='|'+'{}'.format(transition).center(60,' ')
                    results.append(resString)


                except:
                    print('Transition does not exist for {} on {}'.format(stackTop,char))
                    self.printErrorMessage()


#runner
parser=Parser('a*(E)+(E)$')
st=Stack()
parser.parse(st)
seperator='\n'.ljust(159,'-')+'\n'
results=seperator.join(results)
try:
    fhand=open('parseFile.txt','w')
    fhand.write(results)
    fhand.close()
    import time
    time.sleep(2)
    print('\n')
    print('*************Written to parseFile.txt*******************')
    print('\n\n')

except:
    print('Cant write to parseFile.txt some error')
    print('\n\n')
print('The required LL(R) parser table is : \n*******************************************')
print('\n\n')
print(results)
