.MODEL SMALL
.STACK 100H
.DATA
    n1_lo DW 1111H
    n1_hi DW 2222H
    n2_lo DW 3333H
    n2_hi DW 4444H
    res0 DW ?
    res1 DW ?
    res2 DW ?
    res3 DW ?
.CODE
MAIN PROC
    MOV AX, @DATA
    MOV DS, AX

    ; Multiply n1_lo and n2_lo
    MOV AX, n1_lo
    MUL n2_lo
    MOV res0, AX
    MOV res1, DX

    MOV AH, 4CH
    INT 21H
MAIN ENDP
END MAIN
