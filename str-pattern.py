import argparse
import codecs

def generate_pattern(length, bad_chars=''):
    upper_orig = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lower_orig = 'abcdefghijklmnopqrstuvwxyz'
    digits_orig = '0123456789'
    
    upper = [c for c in upper_orig if c not in bad_chars]
    lower = [c for c in lower_orig if c not in bad_chars]
    digits = [c for c in digits_orig if c not in bad_chars]
    
    if not upper or not lower or not digits:
        raise ValueError("Alphabets became empty after excluding bad characters.")
    
    pattern = ''
    u_idx = l_idx = d_idx = 0
    
    while len(pattern) < length:
        pattern += upper[u_idx] + lower[l_idx] + digits[d_idx]
        d_idx += 1
        if d_idx == len(digits):
            d_idx = 0
            l_idx += 1
            if l_idx == len(lower):
                l_idx = 0
                u_idx += 1
                if u_idx == len(upper):
                    break  # Cannot generate more unique pattern
    
    return pattern[:length]

def find_offset(query_hex, bad_chars='', endian='little'):
    if len(query_hex) % 2 != 0:
        raise ValueError("Query hex string must have even length.")
    
    byte_pairs = [query_hex[i:i+2] for i in range(0, len(query_hex), 2)]
    bytes_list = [int(pair, 16) for pair in byte_pairs]
    
    if endian == 'little':
        bytes_list.reverse()
    
    sub = ''.join(chr(b) for b in bytes_list)
    
    max_length = len(sub) + 200000  # Arbitrary large length to search in
    try:
        pattern = generate_pattern(max_length, bad_chars)
    except ValueError as e:
        return str(e)
    
    pos = pattern.find(sub)
    if pos == -1:
        return "Not found in the pattern."
    
    return pos

def main():
    parser = argparse.ArgumentParser(description="Pattern create and offset tool with bad character exclusion.")
    parser.add_argument('-l', '--length', type=int, help='Generate pattern of specified length')
    parser.add_argument('-q', '--query', help='Find offset of the hex string in the pattern')
    parser.add_argument('-b', '--bad', default='', help='Bad characters to exclude (e.g., "\\x1a\\x3C")')
    
    args = parser.parse_args()
    
    # Decode bad characters with escape sequences
    if args.bad:
        bad_bytes = codecs.escape_decode(args.bad)[0]
        bad_str = bad_bytes.decode('latin1')
    else:
        bad_str = ''
    
    if args.length and not args.query:
        try:
            pat = generate_pattern(args.length, bad_str)
            print(pat)
        except ValueError as e:
            print(f"Error: {e}")
    elif args.query and not args.length:
        try:
            offset = find_offset(args.query, bad_str)
            print(offset)
        except ValueError as e:
            print(f"Error: {e}")
    else:
        parser.print_help()
        print("\nError: Specify either -l or -q, but not both.")

if __name__ == "__main__":
    main()
