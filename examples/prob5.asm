jump main   ; main entry
ret         ; interruption 0 entry

; [Project Euler. Problem 5](https://projecteuler.net/problem=5)
; 2520 is the smallest number that can be divided by each of the numbers
; from 1 to 10 without any remainder.
; What is the smallest positive number that is evenly divisible by all of the numbers
; from 1 to 20?

; any number from 1 to 10 is part of other numbers from 1 to 20
; so only that numbers should be multiplied:
; 11 12 13 14 15 16 17 18 19 20

main:
    push 1  ; --> mul=1
    push 10 ; --> last=10 mul=1
loop:
    swap    ; --> mul=1 last=20
    over    ; --> 10 mul=1 last=20
    push 10 ; --> 10 10 mul=1 last=20
    add     ; --> 20 mul=1 last=20
    mul     ; --> mul last
    swap    ; --> last mul
    push -1 ; --> -1 last mul
    add     ; --> last-1 mul
    push 0  ; --> 0 last-1 mul
    cmp     ; --> last-1 mul            ZF=(s0==0)
    jz result ; jump if ZF
    jump loop

done:
    halt

result:
    drop        ; last-1 mul --> mul
    push done   ; --> A mul
    swap        ; --> mul A
    jump print

print:      ; --> N A
    push 10 ; --> 10 N A
    cmp     ; --> N A ?BF=(10 < N)
    jb next
    jz next

prev:       ; --> N A
    push 48 ; --> '0' N A
    add     ; --> C A
    push 1  ; --> 1 C A
    out     ; --> A
    ret

next:
    dup     ; --> N N A0
    push 10 ; --> 10 N N A0
    swap    ; --> N 10 N A0
    mod     ; --> N%10 N A0
    swap    ; --> N N%10 A0
    push 10 ; --> 10 N N%10 A0
    swap    ; --> N 10 N%10 A0
    div     ; --> N/10 N%10 A0
    push prev ; --> A N/10 N%10 A0
    swap    ; --> N/10 A N%10 A0
    jump print
