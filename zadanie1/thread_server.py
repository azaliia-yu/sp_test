from flask import Flask, request, jsonify
import requests
from blocking_parse import parse_page_html
import threading

app = Flask(__name__)
file_lock = threading.Lock()

@app.get("/parse")
def parse_page():
    url = request.args.get("url")
    if not url:
        return {"error": "no url"}, 400

    try:
        r = requests.get(url, timeout=25)
        r.raise_for_status() 
        
        item_names, total = parse_page_html(r.text)
        
        with file_lock:
            with open("thread_results.txt", "a", encoding="utf-8") as f:
                for item_name in item_names:
                    f.write(item_name + "\n")
        
        return jsonify({
            "items": len(item_names),
            "total_price": total
        })
        
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}, 500
    except Exception as e:
        return {"error": "Internal server error"}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, threaded=True)