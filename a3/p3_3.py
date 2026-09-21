import sys

def simulate_macro_processor():
    print("="*60)
    print(" 8086 Two-Pass Macro Processor Simulator ")
    print("="*60)
    print("Example format:")
    print("  MACRO ADD_TWO &X, &Y")
    print("    LOAD R1, &X")
    print("    ADD R1, &Y")
    print("  MEND")
    print("  ADD_TWO 5, 10")
    print("Enter your code (type 'COMPILE' on a new line to start):")

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

    # Pass 1: Build MNT and MDT
    print("\n--- PASS 1: Building MNT and MDT ---")
    
    mnt = {} # Macro Name Table: name -> (MDT_index, args_list)
    mdt = [] # Macro Definition Table: lines of macro body
    
    in_macro = False
    current_macro = ""
    current_args = []
    
    pass1_output = []

    for line in source_code:
        parts = line.split()
        if not parts: continue
        
        if parts[0].upper() == 'MACRO':
            if len(parts) < 2:
                print("Error: MACRO requires a name.")
                return
            
            in_macro = True
            current_macro = parts[1].upper()
            
            # Parse arguments if any (e.g., &X, &Y)
            if len(parts) > 2:
                args_str = "".join(parts[2:])
                current_args = [arg.strip() for arg in args_str.split(',')]
            else:
                current_args = []
                
            mnt[current_macro] = (len(mdt), current_args)
            print(f"  Found Macro: {current_macro} with args {current_args}")
            
        elif parts[0].upper() == 'MEND':
            if not in_macro:
                print("Error: MEND without MACRO")
                return
            mdt.append("MEND")
            in_macro = False
            current_macro = ""
            current_args = []
            
        elif in_macro:
            # Store line in MDT
            mdt.append(line)
        else:
            # Normal code
            pass1_output.append(line)

    print("\nMNT (Macro Name Table):")
    for name, (idx, args) in mnt.items():
        print(f"  {name} -> MDT Index: {idx}, Args: {args}")

    print("\nMDT (Macro Definition Table):")
    for i, line in enumerate(mdt):
        print(f"  [{i}] {line}")

    # Pass 2: Macro Expansion
    print("\n--- PASS 2: Macro Expansion ---")
    expanded_code = []
    
    for line in pass1_output:
        parts = line.split()
        opcode = parts[0].upper()
        
        if opcode in mnt:
            # Macro Call
            mdt_idx, formal_args = mnt[opcode]
            
            # Parse actual arguments
            actual_args = []
            if len(parts) > 1:
                args_str = "".join(parts[1:])
                actual_args = [arg.strip() for arg in args_str.split(',')]
                
            if len(actual_args) != len(formal_args):
                print(f"Error: Macro {opcode} expects {len(formal_args)} args, got {len(actual_args)}")
                return
                
            # Create Argument List Array (ALA) mapping
            ala = dict(zip(formal_args, actual_args))
            print(f"  Expanding {opcode} with ALA: {ala}")
            
            # Expand from MDT
            idx = mdt_idx
            expanded_code.append(f"; --- Start Expansion: {opcode} ---")
            while idx < len(mdt) and mdt[idx] != "MEND":
                body_line = mdt[idx]
                # Substitute arguments
                for f_arg, a_arg in ala.items():
                    body_line = body_line.replace(f_arg, a_arg)
                expanded_code.append(body_line)
                idx += 1
            expanded_code.append(f"; --- End Expansion: {opcode} ---")
        else:
            expanded_code.append(line)

    print("\n--- Final Expanded Source Code ---")
    for line in expanded_code:
        print(f"  {line}")

if __name__ == "__main__":
    simulate_macro_processor()
