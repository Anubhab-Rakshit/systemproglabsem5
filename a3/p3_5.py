import sys
import os
import webbrowser

def simulate_bangla_keyboard():
    print("="*60)
    print(" Bangla Phonetic Keyboard Simulator (Advanced Avro Style) ")
    print("="*60)
    print("Type in English phonetics to see Bangla translation.")
    print("Type 'EXIT' on a new line to quit.\n")
    
    consonants = {
        'k': 'ক', 'kh': 'খ', 'g': 'গ', 'gh': 'ঘ', 'ng': 'ঙ',
        'c': 'চ', 'ch': 'ছ', 'j': 'জ', 'jh': 'ঝ', 'ny': 'ঞ',
        'T': 'ট', 'Th': 'ঠ', 'D': 'ড', 'Dh': 'ঢ', 'N': 'ণ',
        't': 'ত', 'th': 'থ', 'd': 'দ', 'dh': 'ধ', 'n': 'ন',
        'p': 'প', 'f': 'ফ', 'ph': 'ফ', 'b': 'ব', 'bh': 'ভ', 'm': 'ম', 'v': 'ভ',
        'z': 'য', 'r': 'র', 'l': 'ল',
        'sh': 'শ', 'S': 'ষ', 's': 'স', 'h': 'হ',
        'R': 'ড়', 'Rh': 'ঢ়', 'y': 'য়'
    }

    # Independent Vowels (Start of word or after another vowel)
    vowels_indep = {
        'a': 'আ', 'o': 'অ', 'i': 'ই', 'I': 'ঈ',
        'u': 'উ', 'U': 'ঊ', 'e': 'এ', 'O': 'ও', 'OI': 'ঐ', 'OU': 'ঔ'
    }
    
    # Dependent Vowels (Matras - added after a consonant)
    vowels_dep = {
        'a': 'া', 'o': 'ো', 'i': 'ি', 'I': 'ী', 
        'u': 'ু', 'U': 'ূ', 'e': 'ে', 'O': 'ো', 'OI': 'ৈ', 'OU': 'ৌ'
    }
    
    numbers = {
        '0': '০', '1': '১', '2': '২', '3': '৩', '4': '৪',
        '5': '৫', '6': '৬', '7': '৭', '8': '৮', '9': '৯'
    }

    html_file = "bangla_output.html"
    
    # Write initial HTML to trigger open
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write("<html><head><meta charset='utf-8'><meta http-equiv='refresh' content='2'></head><body><h1>Bangla Output:</h1><h2>(Waiting for input...)</h2></body></html>")
    
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
                
                # Check for 2-character matches (e.g. 'kh', 'bh', 'OI')
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
                        # Space or unmapped punctuation resets the consonant flag
                        output += single
                        prev_was_consonant = False
                    i += 1
            
            print(f"Bangla: {output}")
            
            # Write to HTML to bypass macOS Terminal rendering bugs (with auto-refresh)
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(f"<html><head><meta charset='utf-8'><meta http-equiv='refresh' content='1'></head><body><h1>Bangla Output:</h1><h2 style='font-family: sans-serif; font-size: 40px; color: #333;'>{output}</h2><p>Notice how the browser renders it perfectly without dotted circles! (This page auto-refreshes)</p></body></html>")
            
        except EOFError:
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    simulate_bangla_keyboard()
