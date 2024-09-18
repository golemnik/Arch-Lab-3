jump loop       ; main entry
jump interrupt  ; interruption 0 entry

interrupt:
    cli
    ret

loop:
    push 2   ; --> 2
    in       ; --> READY
    push 1   ; --> 1 READY
    cmp      ; --> READY
    drop     ; -->
    jz ready ;
    push 3   ; --> 3
    in       ; --> EOF
    push 0   ; --> 0 EOF
    cmp      ; --> EOF
    drop     ; -->
    jz loop
    push 2   ; --> 2
    in       ; --> READY
    push 1   ; --> 1 READY
    cmp      ; --> READY
    drop     ; -->
    jz ready ;
    halt

ready:
    push 0   ; --> 0
    in       ; --> N
    push 1   ; --> 1 N
    out      ; -->
    push 2   ; --> 2
    dup      ; --> 2 2
    out      ; -->
    jump loop
