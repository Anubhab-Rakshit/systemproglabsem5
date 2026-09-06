.MODEL SMALL
.STACK 100H
.DATA
    bin_str DB '1010', '$'
    dec_val DW 0
.CODE
MAIN PROC
    MOV AX, @DATA
    MOV DS, AX

    ; Binary string to decimal
    MOV SI, OFFSET bin_str
    MOV AX, 0
    MOV CX, 4
L1:
    MOV BL, [SI]
    SUB BL, '0'
    SHL AX, 1
    ADD AL, BL
    INC SI
    LOOP L1
    MOV dec_val, AX

    ; Exit
    MOV AH, 4CH
    INT 21H
MAIN ENDP
END MAIN
