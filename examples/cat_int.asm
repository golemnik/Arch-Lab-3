    jump loop
    jump interrupt

loop:
    push 3   ; --> 3
    in       ; --> EOF
    push 0   ; --> 0 EOF
    cmp      ; --> EOF   | ?ZF
    drop     ; -->
    jz loop
    halt

interrupt:
    pushf  ; --> BF ZF A
    push 0 ; --> 0 BF ZF A
    in     ; --> N BF ZF A
    push 1 ; --> 1 N BF ZF A
    out    ; --> BF ZF A
    dup    ; --> X BF ZF A
    push 2 ; --> 2 X BF ZF A
    out    ; --> BF ZF A
    popf   ; --> A
    cli    ; -->
    ret    ; -->
