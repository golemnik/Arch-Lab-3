jump main   ; main entry
ret         ; interruption 0 entry

;    H   e   l   l   o   !
msg= 72  101 108 108 111 33 0

main:
    push msg    ; --> A
loop:
    dup         ; --> A A
    load        ; --> H A
    push 0      ; --> 0 H A
    cmp         ; --> H A   ZF=?
    jz done
    push 1      ; --> 1 H A
    out         ; --> A
    push 1      ; --> 1 A
    add         ; --> A+1
    jump loop
done:
    halt        ; --> 0 A+6
