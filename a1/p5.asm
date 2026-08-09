.MODEL SMALL
.STACK 100H

.DATA
    msg DB 'Program is terminating...',13,10
        DB 'Thank you!',13,10,'$'

.CODE
MAIN PROC
    MOV AX, @DATA
    MOV DS, AX

    ; Display terminating message
    LEA DX, msg
    MOV AH, 09H
    INT 21H

    ; Terminate program
    MOV AH, 4CH
    MOV AL, 00H
    INT 21H

MAIN ENDP
END MAIN