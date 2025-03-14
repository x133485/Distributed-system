import xmlrpc.client
from datetime import datetime

PORTS = [8000, 8001, 8002]

def get_server_proxy():
    for port in PORTS:
        try:
            server = xmlrpc.client.ServerProxy(f"http://localhost:{port}", allow_none=True)
            server.add_note("test", "Checking server status", datetime.now().isoformat())  #Check if works or not
            print(f"Connected to server on port {port}")
            return server
        except:
            print(f"Server on port {port} is unavailable.")
    raise ConnectionError("No available servers found.")

server = get_server_proxy()

def show_menu():
    print("\nSelect an option:")
    print("1. Add a note")
    print("2. Get notes for a topic")
    print("3. Append Wikipedia info to a topic")
    print("4. Exit")

def main():
    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            topic = input("Enter topic: ").strip()
            text = input("Enter note text: ").strip()
            timestamp = datetime.now().isoformat()
            result = server.add_note(topic, text, timestamp)
            print(result)
        elif choice == "2":
            topic = input("Enter topic to retrieve notes: ").strip()
            result = server.get_topic(topic)
            print("\n" + result)
        elif choice == "3":
            topic = input("Enter topic to append Wikipedia info: ").strip()
            search_term = input("Enter Wikipedia search term: ").strip()
            result = server.append_wikipedia(topic, search_term)
            print(result)
        elif choice == "4":
            print("Exiting.")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
