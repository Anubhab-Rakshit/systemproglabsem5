.MODEL SMALL
.STACK 100H

.DATA
    msg1 DB 'Enter an uppercase letter: $'
    msg2 DB 13,10,'Lowercase letter: $'

.CODE
MAIN PROC
    MOV AX, @DATA
    MOV DS, AX

    ; Display prompt
    LEA DX, msg1
    MOV AH, 09H
    INT 21H

    ; Read character
    MOV AH, 01H
    INT 21H

    ; Convert uppercase to lowercase
    ADD AL, 20H
    MOV BL, AL

    ; Display result message
    LEA DX, msg2
    MOV AH, 09H
    INT 21H

    ; Display lowercase character
    MOV DL, BL
    MOV AH, 02H
    INT 21H

    ; Exit
    MOV AH, 4CH
    INT 21H

MAIN ENDP
END MAIN