from ChatBot import Mail

q = Mail()

while 1:
    text = input()
    q.inbox(message=text)
    ans = q.outbox()
    print(ans)

print(q.outbox())
