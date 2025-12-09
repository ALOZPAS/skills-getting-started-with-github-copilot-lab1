from fastapi.testclient import TestClient
import src.app as app_module

client = TestClient(app_module.app)

activity = "Chess Club"
email = "manualtest@mergington.edu"

print("GET /activities (before)")
resp = client.get("/activities")
print(resp.status_code)
print(resp.json()[activity]["participants"])

print(f"\nPOST signup {email} to {activity}")
resp = client.post(f"/activities/{activity}/signup?email={email}")
print(resp.status_code, resp.json())

print("\nGET /activities (after signup)")
resp = client.get("/activities")
print(resp.status_code)
print(resp.json()[activity]["participants"])

print(f"\nDELETE participant {email} from {activity}")
resp = client.delete(f"/activities/{activity}/participants?email={email}")
print(resp.status_code, resp.json())

print("\nGET /activities (after delete)")
resp = client.get("/activities")
print(resp.status_code)
print(resp.json()[activity]["participants"])
