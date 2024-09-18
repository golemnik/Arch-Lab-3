# Used instructions:

## stack manipulations:
* load - read data memory using address A from top of stack: A --> M
* save - write data memory: A N -->
* push <N_or_label> - put N or label address A on the top of stack: --> N_or_A
* drop - drop then top of stack: N -->
* push <label> - put label data/program address A on the top of stack: --> A
* dup - put the top of stack on the top of stack: N -> N N
* swap - swap two top stack values: N V --> V N
* over - put next the top of stack on the top of stack: N V -> V N V
* rol - roll three top stack values: N X V --> V N X
* pushf - push flags on the top of stack: --> BF ZF
* popf - pop flags from the top of stack: BF ZF -->

## arithmetic operations:
* add - N M -> N+M
* sub - N M -> N-M
* mul - N M -> N*M
* div - N M -> N/M
* mod - N M -> N%M

## comparison operations:
* cmp - compare two the top of stack values, set flags and drop the top: N M --> M ?ZF(N == M) ?BF(N < M)

## control flow operations:
* jump <label> - unconditional jump to <label>
* jz <label> - jump to <label> when ZF is set
* jb <label> - jump to <label> when BF is set
* halt - stop the program
* ret - jump to address from the top of stack: A -->     IP=A

## input/output operations:
* in - read V from port P: P --> V
* out - write V to port P: P V -->

available ports:
* 0 - input
* 1 - output
* 2 - input stream status: 0 - closed, !0 - open

## supported flags:
* ZF - set by "cmp" when two top of stack values are equal
* BF - set by "cmp" when top of stack value is less when the below one
* RF - set by control unit when interrupt occured

## internal registers:
* IP - current command position
* AV - address/data value
* BV - address/data value
* CV - address/data value

## Data definition:
* label= <N1> ... <Nx>

# Language syntax

```
line ::= comment_or_none 
            | variable numbers comment_or_none 
            | label_or_none comment_or_none
            | label_or_none command comment_or_none

comment_or_none := <EMPTY> | comment
comment ::= ';'string

string ::= <ASCII> | <ASCII>string
word ::= <LETTER_DIGIT> | <LETTER_DIGIT>word 

label_or_none ::= <EMPTY> | label
label ::= word':'

variable ::= word'='

digits ::= <DIGIT> | <DIGIT>digits
number ::= '+'digits | '-'digits | digits
numbers ::= <EMPTY> | number numbers
number_or_variable ::= number | word

command ::= command_without_arg
            | command_with_arg number_or_variable
            | command_with_label label

command_without_arg ::= 'dup'
            | 'swap'
            | 'rol'
            | 'add'
            | 'mul'
            | 'dec'
            | 'cmp'
            | 'halt'
            | 'in'
            | 'out'
            | 'ret'

command_with_arg ::= 'push'

command_with_label ::= 'jump'
            | 'je'
            | 'jb' 

```

# Language semantic
## calculation strategy:
- strict straightforward calculations
- step by step execution
## visibility area:
- global visibility in a single stack
## types:
- only signed integers (64 bits)

# Memory
- distinct program segment
- distinct data segment
- single global data stack
- no registers

# I/O interruption
## procedure:
1. push IP on the top of stack: --> IP
2. jump to the begin of interruption hook

## predefined labels:
- "main:" - program entry point
- "interrupt:" - interrupt entry point

## interruption reentrant strategy:
silent drop interruption
