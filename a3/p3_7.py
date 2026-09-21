import sys

def get_module_from_user(index):
    print(f"\n--- Define Object Module {index} ---")
    name = input(f"Enter name for Module {index} (e.g. Mod_{index}): ").strip()
    if not name: name = f"Mod_{index}"
    
    while True:
        try:
            size = int(input(f"Enter size of {name} in bytes (e.g. 100): ").strip())
            break
        except ValueError:
            print("Please enter a valid integer.")
    
    exports = {}
    while True:
        exp = input(f"Enter an EXPORTED symbol name for {name} (or press Enter to finish exports): ").strip()
        if not exp: break
        try:
            offset = int(input(f"  At what relative offset is '{exp}' located? (e.g. 10): ").strip())
            exports[exp] = offset
        except ValueError:
            print("  Invalid offset. Symbol ignored.")
        
    imports = {}
    while True:
        imp = input(f"Enter an IMPORTED symbol name for {name} (or press Enter to finish imports): ").strip()
        if not imp: break
        offsets_str = input(f"  At what relative offsets is '{imp}' referenced? (comma separated, e.g. 30,50): ").strip()
        try:
            offsets = [int(x.strip()) for x in offsets_str.split(',')]
            imports[imp] = offsets
        except ValueError:
            print("  Invalid offsets. Import ignored.")
        
    return {
        'name': name,
        'size': size,
        'exports': exports,
        'imports': imports
    }

def simulate_linker_loader():
    print("="*60)
    print(" Static Linker & Loader Simulator (Interactive) ")
    print("="*60)
    
    try:
        num_modules = int(input("How many object modules do you want to link together? (e.g. 2): ").strip())
    except ValueError:
        print("Invalid number. Exiting.")
        return
        
    modules = []
    for i in range(num_modules):
        modules.append(get_module_from_user(i+1))
    
    print("\n============================================================")
    print("--- Object Files Provided ---")
    for mod in modules:
        print(f"[{mod['name']}] Size: {mod['size']}, Exports: {mod['exports']}, Imports: {mod['imports']}")
    
    input("\nPress Enter to start the Linking process...")
    
    # -----------------------
    # Step 1: Linker (Memory Map & Global Symbol Table)
    # -----------------------
    print("\n--- Step 1: Linker (Memory Mapping & Symbol Resolution) ---")
    base_address = 0x4000 # Typical starting address for user space
    
    memory_map = {}
    global_symbol_table = {}
    
    current_address = base_address
    
    # Assign Addresses for all Modules
    for mod in modules:
        memory_map[mod['name']] = {'start': current_address, 'end': current_address + mod['size'] - 1}
        for sym, rel_offset in mod['exports'].items():
            if sym in global_symbol_table:
                print(f"  Warning: Symbol '{sym}' is redefined in {mod['name']}")
            global_symbol_table[sym] = current_address + rel_offset
        
        current_address += mod['size']
        
    print("Global Symbol Table Generated:")
    if not global_symbol_table:
        print("  (No symbols exported)")
    for sym, addr in global_symbol_table.items():
        print(f"  {sym} -> 0x{addr:04X}")
        
    print("\nMemory Map Generated:")
    for mod_name, addrs in memory_map.items():
        print(f"  {mod_name}: 0x{addrs['start']:04X} - 0x{addrs['end']:04X}")
        
    input("\nPress Enter to start the Loading process...")
    
    # -----------------------
    # Step 2: Loader (Relocation & Patching)
    # -----------------------
    print("\n--- Step 2: Loader (Relocating and Patching Code) ---")
    
    # Patch all Modules
    for mod in modules:
        has_imports = False
        for sym, offsets in mod['imports'].items():
            has_imports = True
            if sym in global_symbol_table:
                abs_addr = global_symbol_table[sym]
                for offset in offsets:
                    patch_addr = memory_map[mod['name']]['start'] + offset
                    print(f"  [Patching {mod['name']}] Inserted absolute address 0x{abs_addr:04X} for '{sym}' at memory location 0x{patch_addr:04X}")
            else:
                print(f"  Linker Error: Undefined symbol '{sym}' referenced in {mod['name']}")
        if not has_imports:
            print(f"  [Patching {mod['name']}] No external dependencies to patch.")
            
    print(f"\nLoading Complete. Program is ready to execute at entry point: 0x{base_address:04X}.")

if __name__ == "__main__":
    simulate_linker_loader()
