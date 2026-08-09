.MODEL SMALL
.STACK 100H

.DATA
    msg1 DB 'Enter a character: $'
    msg2 DB 13,10,'You entered: $'

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

    ; Save character
    MOV BL, AL

    ; Display result message
    LEA DX, msg2
    MOV AH, 09H
    INT 21H

    ; Print character
    MOV DL, BL
    MOV AH, 02H
    INT 21H

    ; Exit
    MOV AH, 4CH
    INT 21H

MAIN ENDP
END MAIN