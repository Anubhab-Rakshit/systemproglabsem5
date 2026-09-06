.MODEL SMALL
.STACK 100H
.DATA
    n1 DW 12
    n2 DW 15
    n3 DW 20
    gcd_res DW ?
.CODE
MAIN PROC
    MOV AX, @DATA
    MOV DS, AX

    ; GCD of n1 and n2
    MOV AX, n1
    MOV BX, n2
GCD_LOOP:
    CMP AX, BX
    JE FOUND_GCD
    JA SUB_A
    SUB BX, AX
    JMP GCD_LOOP
SUB_A:
    SUB AX, BX
    JMP GCD_LOOP
FOUND_GCD:
    MOV gcd_res, AX

    MOV AH, 4CH
    INT 21H
MAIN ENDP
END MAIN
