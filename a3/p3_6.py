import sys
import os
import webbrowser

def simulate_hindi_keyboard():
    print("="*60)
    print(" Hindi Phonetic Keyboard Simulator (Advanced) ")
    print("="*60)
    print("Type in English phonetics to see Hindi (Devanagari) translation.")
    print("Type 'EXIT' on a new line to quit.\n")
    
    consonants = {
        'k': 'क', 'kh': 'ख', 'g': 'ग', 'gh': 'घ', 'ng': 'ङ',
        'c': 'च', 'ch': 'छ', 'j': 'ज', 'jh': 'झ', 'ny': 'ञ',
        'T': 'ट', 'Th': 'ठ', 'D': 'ड', 'Dh': 'ढ', 'N': 'ण',
        't': 'त', 'th': 'थ', 'd': 'द', 'dh': 'ध', 'n': 'न',
        'p': 'प', 'f': 'फ', 'ph': 'फ', 'b': 'ब', 'bh': 'भ', 'm': 'म',
        'y': 'य', 'r': 'र', 'l': 'ल', 'v': 'व', 'w': 'व',
        'sh': 'श', 'S': 'ष', 's': 'स', 'h': 'ह'
    }

    # Independent Vowels
    vowels_indep = {
        'a': 'आ', 'o': 'अ', 'i': 'इ', 'I': 'ई',
        'u': 'उ', 'U': 'ऊ', 'e': 'ए', 'O': 'ओ', 'OI': 'ऐ', 'OU': 'औ'
    }
    
    # Dependent Vowels (Matras)
    vowels_dep = {
        'a': 'ा', 'o': 'ो', 'i': 'ि', 'I': 'ी', 
        'u': 'ु', 'U': 'ू', 'e': 'े', 'O': 'ो', 'OI': 'ै', 'OU': 'ौ'
    }
    
    numbers = {
        '0': '०', '1': '१', '2': '२', '3': '३', '4': '४',
        '5': '५', '6': '६', '7': '७', '8': '८', '9': '९'
    }

    html_file = "hindi_output.html"
    
    # Write initial HTML to trigger open
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write("<html><head><meta charset='utf-8'><meta http-equiv='refresh' content='2'></head><body><h1>Hindi Output:</h1><h2>(Waiting for input...)</h2></body></html>")
    
    # Open browser ONCE
    webbrowser.open('file://' + os.path.realpath(html_file))
    print("[INFO] Opened browser tab once. Keep it open! It will auto-refresh as you type.\n")

    while True:
        try:
            line = input("> ").strip()
            if line.upper() == 'EXIT':
                break
            
            output = ""
            i = 0
            prev_was_consonant = False
            
            while i < len(line):
                match_found = False
                
                # Check for 2-character matches
                if i < len(line) - 1:
                    pair = line[i:i+2]
                    if pair in consonants:
                        output += consonants[pair]
                        prev_was_consonant = True
                        i += 2
                        match_found = True
                    elif pair in vowels_indep:
                        output += vowels_dep[pair] if prev_was_consonant else vowels_indep[pair]
                        prev_was_consonant = False
                        i += 2
                        match_found = True

                if not match_found:
                    single = line[i]
                    if single in consonants:
                        output += consonants[single]
                        prev_was_consonant = True
                    elif single in vowels_indep:
                        output += vowels_dep[single] if prev_was_consonant else vowels_indep[single]
                        prev_was_consonant = False
                    elif single in numbers:
                        output += numbers[single]
                        prev_was_consonant = False
                    else:
                        output += single
                        prev_was_consonant = False
                    i += 1
            
            print(f"Hindi: {output}")
            
            # Write to HTML to bypass macOS Terminal rendering bugs (with auto-refresh)
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(f"<html><head><meta charset='utf-8'><meta http-equiv='refresh' content='1'></head><body><h1>Hindi Output:</h1><h2 style='font-family: sans-serif; font-size: 40px; color: #333;'>{output}</h2><p>Notice how the browser renders it perfectly without dotted circles! (This page auto-refreshes)</p></body></html>")
            
        except EOFError:
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    simulate_hindi_keyboard()
