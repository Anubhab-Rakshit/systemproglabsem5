import sys

def simulate_bangla_keyboard():
    print("="*60)
    print(" Bangla Phonetic Keyboard Simulator (Avro Style) ")
    print("="*60)
    print("Type in English phonetics to see Bangla translation.")
    print("Type 'EXIT' on a new line to quit.\n")
    
    # A simplified phonetic mapping dictionary
    phonetic_map = {
        'k': 'ক', 'kh': 'খ', 'g': 'গ', 'gh': 'ঘ', 'ng': 'ঙ',
        'c': 'চ', 'ch': 'ছ', 'j': 'জ', 'jh': 'ঝ', 'ny': 'ঞ',
        't': 'ট', 'th': 'ঠ', 'd': 'ড', 'dh': 'ঢ', 'n': 'ন',
        'T': 'ত', 'Th': 'থ', 'D': 'দ', 'Dh': 'ধ', 'N': 'ণ',
        'p': 'প', 'f': 'ফ', 'ph': 'ফ', 'b': 'ব', 'bh': 'ভ', 'm': 'ম',
        'z': 'য', 'r': 'র', 'l': 'ল',
        'sh': 'শ', 'S': 'ষ', 's': 'স', 'h': 'হ',
        'R': 'ড়', 'Rh': 'ঢ়', 'y': 'য়',
        
        # Vowels (Simplified for mapping, no kar/matra handling for simplicity)
        'a': 'আ', 'o': 'অ', 'i': 'ই', 'I': 'ঈ',
        'u': 'উ', 'U': 'ঊ', 'e': 'এ', 'O': 'ও', 'OI': 'ঐ', 'OU': 'ঔ',
        
        # Numbers
        '0': '০', '1': '১', '2': '২', '3': '৩', '4': '৪',
        '5': '৫', '6': '৬', '7': '৭', '8': '৮', '9': '৯'
    }

    while True:
        try:
            line = input("> ").strip()
            if line.upper() == 'EXIT':
                break
            
            output = ""
            i = 0
            while i < len(line):
                # Try 2-character matches first
                if i < len(line) - 1 and line[i:i+2] in phonetic_map:
                    output += phonetic_map[line[i:i+2]]
                    i += 2
                # Try 1-character match
                elif line[i] in phonetic_map:
                    output += phonetic_map[line[i]]
                    i += 1
                else:
                    # Keep character as is if not mapped
                    output += line[i]
                    i += 1
            
            print(f"Bangla: {output}")
            
        except EOFError:
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    simulate_bangla_keyboard()
