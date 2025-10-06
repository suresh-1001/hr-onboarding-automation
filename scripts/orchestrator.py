
#!/usr/bin/env python3
import argparse, json, os, time, hashlib
from pathlib import Path
TEMPLATES={"Finance Analyst":{"groups":["finance@company.com","all-hands@company.com"],"slack_channels":["#finance","#announcements"],"intune_policy":"Finance_Baseline","jira_project":"OPS"},
           "Engineer":{"groups":["engineering@company.com","all-hands@company.com"],"slack_channels":["#eng","#announcements"],"intune_policy":"Engineer_Baseline","jira_project":"IT"}}
def gen(email, role, source="bamboohr", disable=False):
    role_t=TEMPLATES.get(role,TEMPLATES["Engineer"]); uid=hashlib.sha1(email.encode()).hexdigest()[:10]
    plan={"meta":{"generated_at":time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),"source":source,"email":email,"role":role,"op":"offboard" if disable else "onboard","request_id":uid},
          "actions":[] if disable else [
            {"system":"workspace","op":"create_user","email":email,"groups":role_t["groups"]},
            {"system":"slack","op":"invite","email":email,"channels":role_t["slack_channels"]},
            {"system":"intune","op":"assign_policy","email":email,"policy":role_t["intune_policy"]},
            {"system":"jira","op":"open_task","project":role_t["jira_project"],"summary":f"Onboard {email}"}
          ]}
    if disable:
        plan["actions"]=[
            {"system":"jira","op":"open_task","project":"IT","summary":f"Offboard {email}"},
            {"system":"workspace","op":"suspend_user","email":email},
            {"system":"slack","op":"deactivate","email":email},
            {"system":"intune","op":"retire_device","email":email}
        ]
    return plan
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--email", required=True); ap.add_argument("--role", required=True)
    ap.add_argument("--source", default="bamboohr"); ap.add_argument("--disable", action="store_true")
    ap.add_argument("--out", default="./examples/last_plan.json")
    a=ap.parse_args(); plan=gen(a.email,a.role,a.source,a.disable)
    Path(os.path.dirname(a.out) or ".").mkdir(parents=True, exist_ok=True)
    with open(a.out,"w",encoding="utf-8") as f: json.dump(plan,f,indent=2)
    print("Wrote plan to", a.out); print("---- Dry Run ----"); [print(x) for x in plan["actions"]]
if __name__=="__main__": main()
