import string

import re
subject = '🎙️[CP] ENGIE et EDPR se félicitent de la confirmation de leurs projets éoliens en mer en France https://t.co/Lf0GBw5cnt https://t.co/K0ovEr0aRN'
result = re.sub(r"http\S+", "", subject)
print(result)
"l*ots! o(f. p@u)n[c}t]u[a'ti\"on#$^?/".translate(str.maketrans({a:None for a in string.punctuation}))

print("j'aime pas 'trop, les !!! et les ... à)àç_è-(-(".translate(str.maketrans({a:None for a in string.punctuation})))