import sys

def simulate_one_pass_assembler():
    print("="*60)
    print(" 8086 One-Pass Assembler Calculator Simulator ")
    print("="*60)
    print("Supported Instructions: LOAD, ADD, SUB, MUL, DIV, MOD, PRINT")
    print("Registers: R1, R2, R3, R4")
    print("Format: OPCODE REG, VALUE/REG  (e.g., LOAD R1, 10  or  ADD R1, R2)")
    print("Type 'EXIT' to quit.\n")

    # Pseudo-Opcodes for Machine Code generation
    OPCODES = {
        'LOAD': 'B8',
        'ADD':  '03',
        'SUB':  '2B',
        'MUL':  'F7',
        'DIV':  'F7',
        'MOD':  'F7',
        'PRINT':'CD'
    }
    
    registers = {'R1': 0, 'R2': 0, 'R3': 0, 'R4': 0}

    address = 0x0100 # Standard COM file starting address

    while True:
        try:
            line = input(f"[{address:04X}] > ").strip()
            if not line:
                continue
            if line.upper() == 'EXIT':
                break

            parts = line.replace(',', ' ').split()
            opcode = parts[0].upper()

            if opcode not in OPCODES:
                print(f"Error: Unknown instruction '{opcode}'")
                continue

            machine_code = OPCODES[opcode]

            if opcode == 'PRINT':
                if len(parts) < 2:
                    print("Error: PRINT requires a register (e.g. PRINT R1)")
                    continue
                reg = parts[1].upper()
                if reg in registers:
                    print(f"  [SIMULATOR OUTPUT] {reg} = {registers[reg]}")
                    machine_code += f" {reg}"
                else:
                    print("Error: Invalid register")
                    continue
            else:
                if len(parts) < 3:
                    print(f"Error: {opcode} requires a register and a value/register.")
                    continue
                
                reg = parts[1].upper()
                val_str = parts[2].upper()
                
                if reg not in registers:
                    print(f"Error: Invalid destination register '{reg}'")
                    continue
                
                val = 0
                is_reg = False
                if val_str in registers:
                    val = registers[val_str]
                    is_reg = True
                else:
                    try:
                        val = int(val_str)
                    except ValueError:
                        print(f"Error: Invalid value '{val_str}'")
                        continue

                # Simulate Execution
                if opcode == 'LOAD':
                    registers[reg] = val
                elif opcode == 'ADD':
                    registers[reg] += val
                elif opcode == 'SUB':
                    registers[reg] -= val
                elif opcode == 'MUL':
                    registers[reg] *= val
                elif opcode == 'DIV':
                    if val == 0:
                        print("Error: Division by zero")
                        continue
                    registers[reg] //= val
                elif opcode == 'MOD':
                    if val == 0:
                        print("Error: Modulo by zero")
                        continue
                    registers[reg] %= val

                operand_code = val_str if is_reg else f"{val:04X}"
                machine_code += f" {reg} {operand_code}"

            print(f"  [PASS 1] Translated to Machine Code: {machine_code}")
            address += len(machine_code.split())

        except EOFError:
            break
        except Exception as e:
            print(f"Error processing line: {e}")

if __name__ == "__main__":
    simulate_one_pass_assembler()
