#%%
def hash_password(text):
    hash=0
    for char in text:
        hash =  ( hash*281  ^ ord(char)*997) & 0xFFFFFFFF
    return hash

# %%
to_crack = 2868533088

# list of ASCII characters
ascii_chars = [chr(i) for i in range(32, 127)]

#%%
# brute force v1
break_flag = False
for c1 in ascii_chars:
    for c2 in ascii_chars:
        for c3 in ascii_chars:
            for c4 in ascii_chars:
                if hash_password(c1+c2+c3+c4) == to_crack:
                    print(f"Your password is '{c1+c2+c3+c4}'.")
                    break_flag = True
                    break
            if break_flag:
                break
        if break_flag:
            break
    if break_flag:
        break
# %%
# brute force v2
def crack(hash_to_crack):
    for c1 in ascii_chars:
        for c2 in ascii_chars:
            for c3 in ascii_chars:
                for c4 in ascii_chars:
                    if hash_password(c1+c2+c3+c4) == hash_to_crack:
                        return c1+c2+c3+c4
    return None

print(crack(to_crack))
