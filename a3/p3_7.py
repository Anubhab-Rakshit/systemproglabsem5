import sys

def simulate_linker_loader():
    print("="*60)
    print(" Static Linker & Loader Simulator ")
    print("="*60)
    print("Simulating linking of two Object Modules (Module A and Module B).")
    
    # Simulated Object Modules
    module_A = {
        'name': 'Module_A',
        'size': 100,  # bytes
        'entry_point': 0,
        'exports': {'VAR_A': 10},  # Symbol exported at relative offset 10
        'imports': {'FUNC_B': [30, 50]}  # Symbol imported, to be patched at relative offsets 30 and 50
    }
    
    module_B = {
        'name': 'Module_B',
        'size': 150,
        'entry_point': 0,
        'exports': {'FUNC_B': 25}, # Symbol exported at relative offset 25
        'imports': {'VAR_A': [100]} # Symbol imported, to be patched at offset 100
    }
    
    print("\n--- Object Files Provided ---")
    print(f"[{module_A['name']}] Size: {module_A['size']}, Exports: {module_A['exports']}, Imports: {module_A['imports']}")
    print(f"[{module_B['name']}] Size: {module_B['size']}, Exports: {module_B['exports']}, Imports: {module_B['imports']}")
    
    input("\nPress Enter to start the Linking process...")
    
    # -----------------------
    # Step 1: Linker (Memory Map & Global Symbol Table)
    # -----------------------
    print("\n--- Step 1: Linker (Memory Mapping & Symbol Resolution) ---")
    base_address = 0x4000 # Typical starting address for user space
    
    memory_map = {}
    global_symbol_table = {}
    
    current_address = base_address
    
    # Assign Addresses for Module A
    memory_map['Module_A'] = {'start': current_address, 'end': current_address + module_A['size'] - 1}
    for sym, rel_offset in module_A['exports'].items():
        global_symbol_table[sym] = current_address + rel_offset
    
    current_address += module_A['size']
    
    # Assign Addresses for Module B
    memory_map['Module_B'] = {'start': current_address, 'end': current_address + module_B['size'] - 1}
    for sym, rel_offset in module_B['exports'].items():
        global_symbol_table[sym] = current_address + rel_offset
        
    print("Global Symbol Table:")
    for sym, addr in global_symbol_table.items():
        print(f"  {sym} -> 0x{addr:04X}")
        
    print("\nMemory Map:")
    for mod, addrs in memory_map.items():
        print(f"  {mod}: 0x{addrs['start']:04X} - 0x{addrs['end']:04X}")
        
    input("\nPress Enter to start the Loading process...")
    
    # -----------------------
    # Step 2: Loader (Relocation & Patching)
    # -----------------------
    print("\n--- Step 2: Loader (Relocating and Patching Code) ---")
    
    # Patch Module A
    for sym, offsets in module_A['imports'].items():
        if sym in global_symbol_table:
            abs_addr = global_symbol_table[sym]
            for offset in offsets:
                patch_addr = memory_map['Module_A']['start'] + offset
                print(f"  [Patching {module_A['name']}] Inserted absolute address 0x{abs_addr:04X} for '{sym}' at memory location 0x{patch_addr:04X}")
        else:
            print(f"  Linker Error: Undefined symbol '{sym}' referenced in {module_A['name']}")

    # Patch Module B
    for sym, offsets in module_B['imports'].items():
        if sym in global_symbol_table:
            abs_addr = global_symbol_table[sym]
            for offset in offsets:
                patch_addr = memory_map['Module_B']['start'] + offset
                print(f"  [Patching {module_B['name']}] Inserted absolute address 0x{abs_addr:04X} for '{sym}' at memory location 0x{patch_addr:04X}")
        else:
            print(f"  Linker Error: Undefined symbol '{sym}' referenced in {module_B['name']}")
            
    print("\nLoading Complete. Program is ready to execute at entry point: 0x4000.")

if __name__ == "__main__":
    simulate_linker_loader()
