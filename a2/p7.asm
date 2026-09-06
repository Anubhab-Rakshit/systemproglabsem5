.MODEL SMALL
.STACK 100H
.DATA
    str DB 'hello world', '$'
    res DB 20 DUP('$')
.CODE
MAIN PROC
    MOV AX, @DATA
    MOV DS, AX
    MOV ES, AX

    MOV SI, OFFSET str
    ADD SI, 6 ; skip 'hello '
    MOV DI, OFFSET res

L1:
    MOV AL, [SI]
    CMP AL, '$'
    JE DONE
    MOV [DI], AL
    INC SI
    INC DI
    JMP L1
DONE:
    
    MOV AH, 4CH
    INT 21H
MAIN ENDP
END MAIN
