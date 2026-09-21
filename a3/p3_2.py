import sys

def simulate_two_pass_assembler_loops():
    print("="*60)
    print(" 8086 Two-Pass Assembler Simulator (Loop Constructs) ")
    print("="*60)
    print("Supported: LOAD, ADD, SUB, WHILE <cond>, ENDWHILE, FOR <init> <cond> <step>, ENDFOR")
    print("Enter your code block (type 'COMPILE' on a new line to start):")

    source_code = []
    while True:
        try:
            line = input("> ").strip()
            if line.upper() == 'COMPILE':
                break
            if line:
                source_code.append(line)
        except EOFError:
            break

    if not source_code:
        print("No source code provided.")
        return

    # Pass 1: Build Symbol Table and Assign Addresses
    print("\n--- PASS 1: Building Symbol Table ---")
    loc_ctr = 0x0100
    symbol_table = {}
    pass1_output = []
    
    loop_stack = []
    label_counter = 1

    for line_num, line in enumerate(source_code):
        parts = line.split()
        opcode = parts[0].upper()
        
        pass1_output.append({'addr': loc_ctr, 'line': line, 'opcode': opcode, 'parts': parts})

        if opcode == 'WHILE':
            start_label = f"L_START_{label_counter}"
            end_label = f"L_END_{label_counter}"
            label_counter += 1
            
            symbol_table[start_label] = loc_ctr
            loop_stack.append(('WHILE', start_label, end_label))
            pass1_output[-1]['start_label'] = start_label
            pass1_output[-1]['end_label'] = end_label
            
            loc_ctr += 4 # Assume CMP + JMP takes 4 bytes
        elif opcode == 'ENDWHILE':
            if not loop_stack or loop_stack[-1][0] != 'WHILE':
                print(f"Error: Unmatched ENDWHILE at line {line_num+1}")
                return
            
            _, start_label, end_label = loop_stack.pop()
            loc_ctr += 2 # JMP back takes 2 bytes
            symbol_table[end_label] = loc_ctr # End label points to the instruction AFTER the loop
            pass1_output[-1]['start_label'] = start_label
            pass1_output[-1]['end_label'] = end_label
        elif opcode == 'FOR':
            # FOR R1=0, R1<5, R1++
            start_label = f"L_START_{label_counter}"
            end_label = f"L_END_{label_counter}"
            label_counter += 1
            
            loc_ctr += 3 # init instruction
            symbol_table[start_label] = loc_ctr
            loop_stack.append(('FOR', start_label, end_label))
            pass1_output[-1]['start_label'] = start_label
            pass1_output[-1]['end_label'] = end_label
            
            loc_ctr += 4 # CMP + JMP
        elif opcode == 'ENDFOR':
            if not loop_stack or loop_stack[-1][0] != 'FOR':
                print(f"Error: Unmatched ENDFOR at line {line_num+1}")
                return
                
            _, start_label, end_label = loop_stack.pop()
            loc_ctr += 5 # Step operation + JMP back
            symbol_table[end_label] = loc_ctr
            pass1_output[-1]['start_label'] = start_label
            pass1_output[-1]['end_label'] = end_label
        else:
            loc_ctr += 3 # Standard instruction takes 3 bytes

    print("Symbol Table generated:")
    for sym, addr in symbol_table.items():
        print(f"  {sym}: {addr:04X}")

    # Pass 2: Generate Object Code
    print("\n--- PASS 2: Object Code Generation ---")
    machine_code = []
    
    for item in pass1_output:
        addr = item['addr']
        opcode = item['opcode']
        parts = item['parts']
        
        hex_code = ""
        
        if opcode == 'WHILE':
            cond = "".join(parts[1:])
            # Simulated CMP and JZ
            hex_code = f"3B (CMP {cond}) 74 {symbol_table[item['end_label']]:04X}"
        elif opcode == 'ENDWHILE':
            hex_code = f"EB {symbol_table[item['start_label']]:04X} (JMP)"
        elif opcode == 'FOR':
            hex_code = f"B8 (INIT) 3B (CMP) 74 {symbol_table[item['end_label']]:04X}"
        elif opcode == 'ENDFOR':
            hex_code = f"40 (STEP) EB {symbol_table[item['start_label']]:04X} (JMP)"
        elif opcode == 'LOAD':
            hex_code = f"B8 {parts[1]}"
        elif opcode == 'ADD':
            hex_code = f"03 {parts[1]}"
        elif opcode == 'SUB':
            hex_code = f"2B {parts[1]}"
        else:
            hex_code = f"?? {opcode}"

        print(f"[{addr:04X}]  {hex_code:<25}  ; {item['line']}")

if __name__ == "__main__":
    simulate_two_pass_assembler_loops()
