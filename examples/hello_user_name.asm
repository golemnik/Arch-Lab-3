jump main       ; main entry
jump interrupt  ; interruption 0 entry

;     W  h   a  t   _  i   s   _  y   o   u   r   _  n   a  m   e   ?  \n
qmsg= 87 104 97 116 32 105 115 32 121 111 117 114 32 110 97 109 101 63 10 0
;     H   e   l   l   o   ,  _
hmsg= 72  101 108 108 111 44 32 0
;     !
fmsg= 33 0
; address of the last symbol of the name
end=  0
; buffer for the received name
name= 0

interrupt:      ; --> R
    pushf       ; --> ZF BF R
    push end    ; --> A ZF BF R
    load        ; --> E ZF BF R
    dup         ; --> E E ZF BF R
    push 0      ; --> 0 E E ZF BF R
    in          ; --> N E E ZF BF R
    swap        ; --> E N E ZF BF R
    save        ; --> E ZF BF R
    push 1      ; --> 1 E ZF BF R
    add         ; --> E+1 ZF BF R
    push end    ; --> A E+1 ZF BF R
    save        ; --> ZF BF R
    dup         ; --> X ZF BF R
    push 2      ; --> 2 X ZF BF R
    out         ; --> ZF BF R
    popf        ; --> R
    cli         ; -->
    ret         ; -->

print:     ; --> A R
    dup    ; --> A A R
    load   ; --> C A R
    push 0 ; --> 0 C A R
    cmp    ; --> C A R   ZF=?
    jz pdone
    push 1 ; --> 1 C A R
    out    ; --> A R
    push 1 ; --> 1 A R
    add    ; --> A+1 R
    jump print
pdone:     ; --> 0 A R
    drop   ; --> A R
    drop   ; --> R
    ret    ; -->

done:
    halt

fprint:
    push done  ; --> R
    push fmsg  ; --> A R
    jump print

nprint:         ; -->
    push fprint ; --> R
    push name   ; --> A R
    jump print

wait:           ; -->
    push 3      ; --> 3
    in          ; --> EOF
    push 0      ; --> 0 EOF
    cmp         ; --> EOF    ?ZF
    drop        ; -->
    jz wait
    push nprint ; --> R
    push hmsg   ; --> A R
    jump print

main:
    push name   ; --> A1
    push end    ; --> A2 A1
    save        ; -->
    push wait   ; --> R
    push qmsg   ; --> A R
    jump print