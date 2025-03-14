import xml.etree.ElementTree as ET
from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn
from datetime import datetime
import requests
import os


XML_FILE = "notes.xml"
def init_xml():

    if not os.path.exists(XML_FILE):
        root = ET.Element("notes")
        tree = ET.ElementTree(root)
        tree.write(XML_FILE)

def add_note(topic, text, timestamp):
    init_xml()
    tree = ET.parse(XML_FILE)
    root = tree.getroot()

    topic_elem = None
    for t in root.findall("topic"):
        if t.get("name") == topic:
            topic_elem = t
            break

    if topic_elem is None:
        topic_elem = ET.SubElement(root, "topic", name=topic)


    note_elem = ET.SubElement(topic_elem, "note")
    text_elem = ET.SubElement(note_elem, "text")
    text_elem.text = text

    timestamp_elem = ET.SubElement(note_elem, "timestamp")
    timestamp_elem.text = timestamp

    tree.write(XML_FILE)
    return "Note added successfully."

def get_topic(topic):

    init_xml()
    tree = ET.parse(XML_FILE)
    root = tree.getroot()
    topic_elem = None
    for t in root.findall("topic"):
        if t.get("name") == topic:
            topic_elem = t
            break
    if topic_elem is None:
        return "Topic not found."
    
    notes = []
    for note in topic_elem.findall("note"):
        text_val = note.find("text").text if note.find("text") is not None else ""
        timestamp_val = note.find("timestamp").text if note.find("timestamp") is not None else ""
        notes.append(f"Note: {text_val} (at {timestamp_val})")
    return "\n".join(notes)

def append_wikipedia(topic, search_term):

    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": search_term,
        "format": "json"
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return "Failed to fetch from Wikipedia."
    data = response.json()
    search_results = data.get("query", {}).get("search", [])
    if not search_results:
        return "No Wikipedia article found for the search term."
    
    article = search_results[0]
    pageid = article.get("pageid")
    wiki_link = f"https://en.wikipedia.org/?curid={pageid}"
    
    # Append the Wikipedia link as a note for the topic.
    timestamp = datetime.now().isoformat
    note_text = f"Wikipedia article for '{search_term}': {wiki_link}"
    add_note(topic, note_text, timestamp)
    return f"Wikipedia info added to topic '{topic}'."

def get_wikipedia_link(search_term):
    """
    (Optional) Return only a Wikipedia link based on a search term without appending it.
    """
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": search_term,
        "format": "json"
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return "Failed to fetch from Wikipedia."
    data = response.json()
    search_results = data.get("query", {}).get("search", [])
    if not search_results:
        return "No Wikipedia article found for the search term."
    
    article = search_results[0]
    pageid = article.get("pageid")
    wiki_link = f"https://en.wikipedia.org/?curid={pageid}"
    return wiki_link

# Define a threaded XML-RPC server to handle multiple client requests concurrently.
class ThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

if __name__ == "__main__":
    server = ThreadedXMLRPCServer(("localhost", 8000), allow_none=True)
    print("Server is running on port 8000...")
    
    # Register the functions so they can be called remotely.
    server.register_function(add_note, "add_note")
    server.register_function(get_topic, "get_topic")
    server.register_function(append_wikipedia, "append_wikipedia")
    server.register_function(get_wikipedia_link, "get_wikipedia_link")
    
    # Start the server’s main loop.
    server.serve_forever()





