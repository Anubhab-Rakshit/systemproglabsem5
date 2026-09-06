.MODEL SMALL
.STACK 100H
.DATA
    old_file DB 'old.txt', 0
    new_file DB 'new.txt', 0
.CODE
MAIN PROC
    MOV AX, @DATA
    MOV DS, AX
    MOV ES, AX

    MOV AH, 56H
    LEA DX, old_file
    LEA DI, new_file
    INT 21H

    MOV AH, 4CH
    INT 21H
MAIN ENDP
END MAIN
