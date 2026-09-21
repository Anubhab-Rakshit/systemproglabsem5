import sys

def simulate_hindi_keyboard():
    print("="*60)
    print(" Hindi Phonetic Keyboard Simulator ")
    print("="*60)
    print("Type in English phonetics to see Hindi (Devanagari) translation.")
    print("Type 'EXIT' on a new line to quit.\n")
    
    # A simplified phonetic mapping dictionary
    phonetic_map = {
        'k': 'क', 'kh': 'ख', 'g': 'ग', 'gh': 'घ', 'ng': 'ङ',
        'c': 'च', 'ch': 'छ', 'j': 'ज', 'jh': 'झ', 'ny': 'ञ',
        'T': 'ट', 'Th': 'ठ', 'D': 'ड', 'Dh': 'ढ', 'N': 'ण',
        't': 'त', 'th': 'थ', 'd': 'द', 'dh': 'ध', 'n': 'न',
        'p': 'प', 'f': 'फ', 'ph': 'फ', 'b': 'ब', 'bh': 'भ', 'm': 'म',
        'y': 'य', 'r': 'र', 'l': 'ल', 'v': 'व', 'w': 'व',
        'sh': 'श', 'S': 'ष', 's': 'स', 'h': 'ह',
        
        # Vowels (Simplified for mapping, no kar/matra handling for simplicity)
        'a': 'आ', 'o': 'अ', 'i': 'इ', 'I': 'ई',
        'u': 'उ', 'U': 'ऊ', 'e': 'ए', 'O': 'ओ', 'OI': 'ऐ', 'OU': 'औ',
        
        # Numbers
        '0': '०', '1': '१', '2': '२', '3': '३', '4': '४',
        '5': '५', '6': '६', '7': '७', '8': '८', '9': '९'
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
            
            print(f"Hindi: {output}")
            
        except EOFError:
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    simulate_hindi_keyboard()
