jump main   ; main entry
ret         ; interruption 0 entry

; [Project Euler. Problem 1](https://projecteuler.net/problem=1)
; If we list all the natural numbers below 10 that are multiples of 3 or 5,
; we get 3, 5, 6 and 9. The sum of these multiples is 23.
; Find the sum of all the multiples of 3 or 5 below 1000.

; --> s0 s1 s2 ...

main:
    push 0 ; --> sum
    push 0 ; --> cur sum
loop:
    push 3 ; --> 3 cur sum
    add    ; --> cur+3 sum
    dup    ; --> cur+3 cur+3 sum
    rol    ; --> sum cur+3 cur+3
    add    ; --> sum cur+3
    push 998 ; --> 1000-2 sum cur+3
    cmp    ; --> sum cur+3                  ZF=(s0 == s1), BF=(s0 < s1)
    jz result ; jump if ZF
    jb result ; jump if BF
    swap   ; --> cur+3 sum

    push 2 ; --> 2 cur+3 sum
    add    ; --> cur+5 sum
    dup    ; --> cur+5 cur+5 sum
    rol    ; --> sum cur+5 cur+5
    add    ; --> sum cur+5
    push 999 ; --> 1000-1 sum cur+5
    cmp    ; sum cur+5                  ZF=(s0 == s1), BF=(s0 < s1)
    jz result ; jump if ZF
    jb result ; jump if BF
    swap   ; --> cur+5 sum

    push 1 ; --> 1 cur+5 sum
    add    ; --> cur+6 sum
    dup    ; --> cur+6 cur+6 sum
    rol    ; --> sum cur+6 cur+6
    add    ; --> sum cur+6
    push 997 ; --> 1000-3 sum cur+6
    cmp    ; --> sum cur+6                  ZF=(s0 == s1), BF=(s0 < s1)
    jz result ; jump if ZF
    jb result ; jump if BF
    swap   ; --> cur+6 sum
    jump loop

done:
    halt

result:
    push done   ; --> A N
    swap        ; --> N A
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

