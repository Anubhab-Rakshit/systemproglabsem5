import sys
import os

def text_editor_simulator():
    print("="*60)
    print(" Basic Text Editor Simulator ")
    print("="*60)
    
    buffer = []
    
    while True:
        print("\n--- Menu ---")
        print("1. View Document")
        print("2. Append Line")
        print("3. Insert Line at Index")
        print("4. Delete Line")
        print("5. Save to File")
        print("6. Open File")
        print("7. Clear Document")
        print("8. Exit")
        
        choice = input("Select an option: ").strip()
        
        if choice == '1':
            print("\n--- Document ---")
            if not buffer:
                print("(empty)")
            else:
                for i, line in enumerate(buffer):
                    print(f"{i}: {line}")
            print("----------------")
            
        elif choice == '2':
            text = input("Enter text to append: ")
            buffer.append(text)
            print("Line appended.")
            
        elif choice == '3':
            try:
                idx = int(input("Enter line index to insert at: "))
                text = input("Enter text: ")
                if 0 <= idx <= len(buffer):
                    buffer.insert(idx, text)
                    print("Line inserted.")
                else:
                    print("Error: Index out of bounds.")
            except ValueError:
                print("Error: Invalid index.")
                
        elif choice == '4':
            try:
                idx = int(input("Enter line index to delete: "))
                if 0 <= idx < len(buffer):
                    deleted = buffer.pop(idx)
                    print(f"Deleted line: {deleted}")
                else:
                    print("Error: Index out of bounds.")
            except ValueError:
                print("Error: Invalid index.")
                
        elif choice == '5':
            filename = input("Enter filename to save as: ")
            try:
                with open(filename, 'w') as f:
                    for line in buffer:
                        f.write(line + '\n')
                print(f"Document saved to {filename}")
            except Exception as e:
                print(f"Error saving file: {e}")
                
        elif choice == '6':
            filename = input("Enter filename to open: ")
            if os.path.exists(filename):
                try:
                    with open(filename, 'r') as f:
                        buffer = [line.rstrip('\n') for line in f.readlines()]
                    print(f"Document loaded from {filename}")
                except Exception as e:
                    print(f"Error loading file: {e}")
            else:
                print(f"Error: File '{filename}' not found.")
                
        elif choice == '7':
            buffer = []
            print("Document cleared.")
            
        elif choice == '8':
            print("Exiting Text Editor.")
            break
        else:
            print("Invalid choice. Please select 1-8.")

if __name__ == "__main__":
    text_editor_simulator()
