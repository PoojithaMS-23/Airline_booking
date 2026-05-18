import xmlrpc.client

# CONNECT TO RPC SERVER
proxy = xmlrpc.client.ServerProxy(
    "http://localhost:8000/"
)

print("\n===== RPC CLIENT STARTED =====\n")

try:

    # REMOTE PROCEDURE CALL
    result = proxy.book_ticket(

        1,              # user_id
        1,              # schedule_id
        "Economy",      # class
        2               # seats
    )

    print("RPC Response:")

    print(result)

except Exception as e:

    print("RPC Error:")

    print(e)