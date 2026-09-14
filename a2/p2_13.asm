.MODEL SMALL
.STACK 100H
.DATA
    msg_time DB 'System Time (HH:MM:SS): $'
    msg_date DB 'System Date (DD/MM/YYYY): $'
.CODE
MAIN PROC
    MOV AX, @DATA
    MOV DS, AX

    LEA DX, msg_time
    MOV AH, 09H
    INT 21H

    MOV AH, 2CH
    INT 21H
    MOV AL, CH
    CALL PRINT_2_DIGITS
    MOV DL, ':'
    MOV AH, 02H
    INT 21H
    
    MOV AL, CL
    CALL PRINT_2_DIGITS
    MOV DL, ':'
    MOV AH, 02H
    INT 21H

    MOV AL, DH
    CALL PRINT_2_DIGITS
    CALL NEWLINE

    LEA DX, msg_date
    MOV AH, 09H
    INT 21H

    MOV AH, 2AH
    INT 21H
    
    MOV AL, DL
    CALL PRINT_2_DIGITS
    MOV DL, '/'
    MOV AH, 02H
    INT 21H
    
    MOV AL, DH
    CALL PRINT_2_DIGITS
    MOV DL, '/'
    MOV AH, 02H
    INT 21H
    
    MOV AX, CX
    CALL PRINT_NUM
    CALL NEWLINE

    MOV AH, 4CH
    INT 21H
MAIN ENDP

; Utility Procedures
PRINT_2_DIGITS PROC
    ; Prints AL (assumed 0-99) as a 2-digit zero-padded number
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX

    MOV AH, 0
    MOV BL, 10
    DIV BL
    ; AL has tens, AH has units
    MOV DL, AL
    ADD DL, '0'
    PUSH AX
    MOV AH, 02H
    INT 21H

    POP AX
    MOV DL, AH
    ADD DL, '0'
    MOV AH, 02H
    INT 21H

    POP DX
    POP CX
    POP BX
    POP AX
    RET
PRINT_2_DIGITS ENDP

PRINT_NUM PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    CMP AX, 0
    JGE POSITIVE
    PUSH AX
    MOV DL, '-'
    MOV AH, 02H
    INT 21H
    POP AX
    NEG AX
POSITIVE:
    MOV CX, 0
    MOV BX, 10
DIV_LOOP:
    MOV DX, 0
    DIV BX
    PUSH DX
    INC CX
    CMP AX, 0
    JNE DIV_LOOP
PRINT_LOOP:
    POP DX
    ADD DL, '0'
    MOV AH, 02H
    INT 21H
    LOOP PRINT_LOOP
    POP DX
    POP CX
    POP BX
    POP AX
    RET
PRINT_NUM ENDP

NEWLINE PROC
    PUSH AX
    PUSH DX
    MOV DL, 13
    MOV AH, 02H
    INT 21H
    MOV DL, 10
    MOV AH, 02H
    INT 21H
    POP DX
    POP AX
    RET
NEWLINE ENDP
END MAIN
