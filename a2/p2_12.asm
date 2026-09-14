.MODEL SMALL
.STACK 100H
.DATA
    msg_old DB 'Enter old filename: $'
    msg_new DB 'Enter new filename: $'
    msg_ok DB 'Renamed successfully!', 13, 10, '$'
    msg_err DB 'Error renaming file (does it exist?).', 13, 10, '$'

    old_buf DB 50
    old_len DB ?
    old_file DB 50 DUP(0)

    new_buf DB 50
    new_len DB ?
    new_file DB 50 DUP(0)
.CODE
MAIN PROC
    MOV AX, @DATA
    MOV DS, AX
    MOV ES, AX

    ; Read old filename
    LEA DX, msg_old
    MOV AH, 09H
    INT 21H
    
    LEA DX, old_buf
    MOV AH, 0AH
    INT 21H
    CALL NEWLINE

    ; Null-terminate old_file
    MOV AL, old_len
    MOV AH, 0
    MOV SI, AX
    MOV old_file[SI], 0

    ; Read new filename
    LEA DX, msg_new
    MOV AH, 09H
    INT 21H

    LEA DX, new_buf
    MOV AH, 0AH
    INT 21H
    CALL NEWLINE

    ; Null-terminate new_file
    MOV AL, new_len
    MOV AH, 0
    MOV SI, AX
    MOV new_file[SI], 0

    ; Rename File using INT 21H, AH=56H
    MOV AH, 56H
    LEA DX, old_file
    LEA DI, new_file
    INT 21H
    JC ERR

    ; Success
    LEA DX, msg_ok
    MOV AH, 09H
    INT 21H
    JMP DONE
ERR:
    ; Failure
    LEA DX, msg_err
    MOV AH, 09H
    INT 21H
DONE:
    MOV AH, 4CH
    INT 21H
MAIN ENDP

; Utility Procedures
NEWLINE PROC
    PUSH AX
    PUSH DX
    MOV DL, 13
    MOV AH, 02H
    INT 21H
    MOV DL, 10
    MOV AH, 02H
    INT 21H
    POP DX
    POP AX
    RET
NEWLINE ENDP

END MAIN
