.MODEL SMALL
.STACK 100H

.DATA
    msg DB 'Characters from A to Z:',13,10,'$'

.CODE
MAIN PROC
    MOV AX, @DATA
    MOV DS, AX

    ; Display message
    LEA DX, msg
    MOV AH, 09H
    INT 21H

    ; Start from A
    MOV DL, 'A'

PRINT_LOOP:

    ; Print character
    MOV AH, 02H
    INT 21H

    ; Print space
    MOV DL, ' '
    MOV AH, 02H
    INT 21H

    ; Next character
    INC DL

    ; Check if beyond Z
    CMP DL, 'Z'
    JBE PRINT_LOOP

    ; Exit
    MOV AH, 4CH
    INT 21H

MAIN ENDP
END MAIN