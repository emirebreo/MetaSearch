try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")

# to search
query = "Geeksforgeeks"

for j in search(query, tld="co.in", num=10, pause=1):
    print(j)

print(20*"#")

for j in search(query, tld="co.in", num=5, start=1, pause=1):
    print(j)

print(20*"#")

for j in search(query, tld="co.in", num=5, start=6, pause=1):
    print(j)
