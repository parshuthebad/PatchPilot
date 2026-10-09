import os, json, re, difflib
import streamlit as st
from openai import OpenAI
st.set_page_config(page_title="PatchPilot", page_icon="🛠️", layout="wide")
st.title("🛠️ PatchPilot")
st.caption("A test-first coding agent: understand a bug, propose a patch, and verify it safely.")
with st.sidebar:
    st.subheader("Model configuration")
    api_key=st.text_input("Nebius API key",value=os.getenv("NEBIUS_API_KEY",""),type="password")
    base_url=st.text_input("Token Factory API URL",value=os.getenv("NEBIUS_BASE_URL","https://api.tokenfactory.nebius.com/v1"))
    model=st.text_input("Model",value=os.getenv("NEBIUS_MODEL","nvidia/nemotron-3-super-120b-a12b"))
    st.caption("NVIDIA Nemotron via Nebius Token Factory")
samples={"Python: off-by-one":"def average(nums):\n    return sum(nums) / (len(nums) - 1)\n\nprint(average([2, 4, 6]))", "Python: broken lookup":"def find_user(users, user_id):\n    for user in users:\n        if user['id'] = user_id:\n            return user\n    return None", "JavaScript: null access":"function displayName(user) {\n  return user.profile.name.toUpperCase();\n}\nconsole.log(displayName(null));"}
a,b=st.columns(2)
with a: task=st.text_area("What should the code do?","Fix the bug while preserving intended behavior. Add a concise explanation and relevant tests.",height=90)
with b: choice=st.selectbox("Load an example",["Custom"]+list(samples))
code=st.text_area("Code to inspect",samples.get(choice,"def add(a, b):\n    return a - b"),height=250)
run=st.button("Analyze, patch & test",type="primary",use_container_width=True)
SYSTEM="You are PatchPilot, a cautious senior engineer. Respond ONLY valid JSON with keys summary, findings (array), fixed_code (complete replacement), tests (array of objects name/code/expected; Python unittest-compatible where appropriate), test_command. Never claim tests ran. Preserve behavior and avoid unrelated changes. For non-Python set tests to []."
def parse(s):
    s=re.sub(r"^```(?:json)?\s*|\s*```$","",s.strip(),flags=re.I)
    try: return json.loads(s)
    except json.JSONDecodeError: return json.loads(re.search(r"\{.*\}",s,re.S).group())
if run:
    if not api_key: st.error("Add a Nebius API key in the sidebar or set NEBIUS_API_KEY.")
    elif not code.strip(): st.warning("Paste code first.")
    else:
        try:
            c=OpenAI(api_key=api_key,base_url=base_url)
            with st.spinner("Nemotron is reviewing the code…"):
                r=c.chat.completions.create(model=model,temperature=.2,messages=[{"role":"system","content":SYSTEM},{"role":"user","content":f"Request:\n{task}\n\nSource code:\n{code}"}])
            st.session_state.result=parse(r.choices[0].message.content); st.session_state.original=code
        except Exception as e: st.error(f"Request failed: {e}")
if "result" in st.session_state:
    d=st.session_state.result; st.divider(); st.subheader("Agent review"); st.write(d.get("summary",""))
    for x in d.get("findings",[]): st.markdown("- "+x)
    original=st.session_state.original; fixed=d.get("fixed_code","")
    t1,t2,t3=st.tabs(["Patch","Tests","Diff"])
    with t1:
        st.code(fixed,language="python"); st.download_button("Download patched code",fixed,file_name="patched_code.py")
    with t2:
        tests=d.get("tests",[])
        if tests:
            for x in tests:
                st.markdown(f"**{x.get('name','Test')}** — expected: `{x.get('expected','')}`"); st.code(x.get("code",""),language="python")
        else: st.info("No executable tests generated for this language.")
        st.caption("Suggested command: "+d.get("test_command","Review and run tests in your own environment."))
        st.warning("For safety, generated code is never executed in this app. Review and test it in your own sandbox.")
    with t3:
        st.code("\n".join(difflib.unified_diff(original.splitlines(),fixed.splitlines(),fromfile="before",tofile="after",lineterm="")) or "No textual changes",language="diff")
st.divider(); st.caption("Model output can be wrong. Review every patch; this app does not execute generated code.")
