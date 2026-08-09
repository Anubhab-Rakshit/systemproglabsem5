.MODEL SMALL
.STACK 100H

.DATA
    titleMsg DB 13,10,'SYSTEM PROGRAMMING LAB',13,10
             DB 'Assignment 1 - MASM Program',13,10,'$'

    nameMsg  DB 'Name: Anubhab Rakshit',13,10,'$'

.CODE
MAIN PROC
    MOV AX, @DATA
    MOV DS, AX

    ; Display program title
    LEA DX, titleMsg
    MOV AH, 09H
    INT 21H

    ; Display name
    LEA DX, nameMsg
    MOV AH, 09H
    INT 21H

    ; Exit
    MOV AH, 4CH
    INT 21H

MAIN ENDP
END MAIN