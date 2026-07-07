import urllib.request
import urllib.parse
import json

def test_ledger():
    print("Testing /health")
    req = urllib.request.Request("http://127.0.0.1:8081/health")
    with urllib.request.urlopen(req) as resp:
        print(resp.read().decode())
    
    print("\nTesting POST /reviews")
    data = json.dumps({
        "reviewer": "agent-alpha",
        "target": "agent-beta",
        "score": 4,
        "comment": "Good negotiation, but slow response."
    }).encode('utf-8')
    req = urllib.request.Request("http://127.0.0.1:8081/reviews", data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        print(resp.read().decode())
        
    print("\nTesting GET /reviews/{agent_id}")
    req = urllib.request.Request("http://127.0.0.1:8081/reviews/agent-beta")
    with urllib.request.urlopen(req) as resp:
        print(resp.read().decode())
        
if __name__ == "__main__":
    test_ledger()
