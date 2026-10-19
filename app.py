import streamlit as st
import json, random, datetime
from pathlib import Path

st.set_page_config(page_title="MVS / TK5 Realtime Console", page_icon="🖥️", layout="wide")
STATE = Path("state.json")

def initial():
    return {
      "console": [], "audit": [], "jobs": [], "held": [], "spool": [],
      "datasets": {
        "SYS1.LINKLIB":{"type":"PDS","recfm":"U","lrecl":0,"vol":"TK5001","members":["IEFBR14","IEBGENER","IDCAMS","IKJEFT01"]},
        "SYS1.PROCLIB":{"type":"PDS","recfm":"FB","lrecl":80,"vol":"TK5001","members":["START","MOUNT","IEFBR14","JES2"]},
        "USER.CNTL":{"type":"PDS","recfm":"FB","lrecl":80,"vol":"PUB000","members":[]},
        "USER.OUTPUT":{"type":"PS","recfm":"FB","lrecl":133,"vol":"PUB000","members":[]},
        "SMPE.GLOBAL.CSI":{"type":"PS","recfm":"VB","lrecl":32756,"vol":"TK5001","members":[]},
        "SMPE.TARGET.LINKLIB":{"type":"PDS","recfm":"U","lrecl":0,"vol":"TK5001","members":[]}
      },
      "volumes":{"PUB000":{"status":"ONLINE","device":"0481","type":"3390"},"WORK01":{"status":"ONLINE","device":"0482","type":"3390"},"TK5001":{"status":"ONLINE","device":"0483","type":"3390"}},
      "devices":{"0481":"3390 DASD","0482":"3390 DASD","0483":"3390 DASD","0581":"3480 TAPE","00E":"3270 TERMINAL"},
      "smpe":{"zones":{"TK5GLOB":"GLOBAL","TK5TZN":"TARGET","TK5DLB":"DISTRIBUTION"},"sysmods":{}},
      "system":{"ipl":"COMPLETE","master":"TK5","cpu":"%048","storage":"512M","jes":"JES2"}
    }

def load():
    if STATE.exists():
        try: return json.loads(STATE.read_text())
        except: pass
    return initial()

if "s" not in st.session_state:
    st.session_state.s = load()
    if not st.session_state.s["console"]:
        log("IEA101A SPECIFY SYSTEM PARAMETERS FOR IPL", "sys")
        log("IEE252I MVS/TK5 REALTIME SIMULATION INITIALIZED", "sys")
        log("IEE041I THE SYSTEM LOG IS NOW ACTIVE", "sys")
        log("READY", "sys")

def save(): STATE.write_text(json.dumps(st.session_state.s, indent=2))
def log(m,k="info"):
    t=datetime.datetime.now().strftime("%H:%M:%S")
    st.session_state.s["console"].append({"t":t,"m":m,"k":k})
    st.session_state.s["audit"].append({"t":t,"m":m})
    save()
def now(): return datetime.datetime.now().strftime("%H:%M:%S")

s=st.session_state.s
st.title("🖥️ MVS / TK5 Realtime Operations Console")
st.caption("Expanded MVS, JES2, VTAM, DASD, and SMP/E practice screens. Simulation only.")

tabs=st.tabs(["MCS Console","SDSF Jobs","Job Output","Devices & Volumes","IPL / System","SMP/E","Notes & Q&A"])

with tabs[0]:
    st.subheader("Master Console — MCS")
    c1,c2,c3,c4=st.columns(4)
    c1.metric("System",s["system"]["master"]); c2.metric("IPL",s["system"]["ipl"])
    c3.metric("CPU",s["system"]["cpu"]); c4.metric("JES",s["system"]["jes"])
    st.code("\n".join(f'[{x["t"]}] {x["m"]}' for x in s["console"][-300:]) or "READY", language="text")
    cmd=st.text_input("Enter MVS / JES2 command",placeholder="D A,L | D ASM | $DJ(*) | VARY 0581,ONLINE | HELP")
    if st.button("Execute",type="primary") and cmd.strip():
        c=cmd.strip().upper(); t=c.split(); log(f"> {cmd}","cmd")
        def reply(lines,k="info"):
            for l in lines: log(l,k)
        if c in ("HELP","?"):
            reply(["MVS: D A,L | D A | D T | D M=DEV | D M=CHP | D VOLID | D ASM | D U | D XCF | D PARMLIB",
            "JOB: S proc | P proc | C job | C job,A | F job,APPL | DISPLAY? use D A,L",
            "JES2: $DSPL | $DJ | $DJ(*) | $DI | $TI | $S INIT | $P INIT | $C JOB | $H J | $O J | $T",
            "DEVICE: VARY dev,ONLINE | VARY dev,OFFLINE | MOUNT vol | UNMOUNT vol",
            "VTAM: D NET | D NET,MAJNODES | VARY NET,ACT,ID=NODE | VARY NET,INACT,ID=NODE",
            "SMP/E: SMPE RECEIVE | SMPE APPLY | SMPE ACCEPT | SMPE RESTORE | SMPE QUERY",
            "OTHER: LISTDS ds | LISTA | SEND 'text',U=ALL | RO *ALL,text | CLEAR"])
        elif c.startswith("D A"): 
            if s["jobs"]:
                for j in s["jobs"]: log(f"{j['name']} JOB{j['id']} {j['status']} CLASS={j['class']} PHASE=EXECUTION")
            else: log("IEE105I NO ACTIVE JOBS")
        elif c=="D T": log(f"IEE136I LOCAL={now()} DATE=2026.288 TZ=IST")
        elif c.startswith("D M=DEV"):
            for d,desc in s["devices"].items(): log(f"IEE174I {d} {desc} ONLINE")
        elif c.startswith("D M=CHP"): log("IEE174I CHP 00-0F ONLINE  CHP 10-1F ONLINE")
        elif c.startswith("D VOLID"):
            for v,d in s["volumes"].items(): log(f"IEE459I {v} {d['status']} DEV={d['device']} TYPE={d['type']}")
        elif c=="D ASM": log("IEE451I ASM  PAGTOT=512M  PAGIN=0  PAGOUT=0  SLOTS=98%")
        elif c=="D U": log("IEE451I UNIT=0481 STATUS=ONLINE VOL=PUB000")
        elif c=="D XCF": log("IXL153I XCF STATUS: LOCAL XCF GROUP ACTIVE")
        elif c=="D PARMLIB": log("IEE252I IEASYS00 PARMLIB MEMBER ACTIVE")
        elif c.startswith("S "):
            n=t[1] if len(t)>1 else "UNKNOWN"; jid=str(random.randint(100,999))
            s["jobs"].append({"name":n,"id":jid,"status":"ACTIVE","class":"A","owner":"OPER","retcode":"RUNNING"})
            log(f"IEF403I {n} STARTED TIME={now()}","sys"); save()
        elif c.startswith("P "):
            n=t[1] if len(t)>1 else ""; b=len(s["jobs"])
            s["jobs"]=[j for j in s["jobs"] if j["name"]!=n]
            reply([f"IEF404I {n} ENDED TIME={now()}"] if len(s["jobs"])<b else [f"IEE341I {n} NOT ACTIVE"],"sys" if len(s["jobs"])<b else "error"); save()
        elif c.startswith("C "):
            n=t[1] if len(t)>1 else ""; b=len(s["jobs"])
            s["jobs"]=[j for j in s["jobs"] if j["name"]!=n]
            reply([f"IEE818I {n} CANCELLED"] if len(s["jobs"])<b else [f"IEE341I {n} NOT FOUND"],"sys" if len(s["jobs"])<b else "error"); save()
        elif c.startswith("F "):
            parts=c.split(maxsplit=2)
            if len(parts)>=3: log(f"IEE252I MODIFY COMMAND ACCEPTED FOR {parts[1]}: {parts[2]}","sys")
            else: log("USAGE: F jobname,parameters","error")
        elif c.startswith("$DJ"):
            if s["jobs"]:
                for j in s["jobs"]: log(f"$HASP890 JOB({j['name']}) STATUS={j['status']} CLASS={j['class']}")
            else: log("$HASP890 NO JOBS FOUND")
        elif c=="$DSPL": log("$HASP609 JES2 STATUS: SPOOL 100% AVAILABLE, NODES 1, MEMBERS 1")
        elif c=="$DI": log("$HASP609 INITIATORS: 1 DRAINED 2 DRAINED 3 DRAINED 4 DRAINED")
        elif c=="$TI": log("$HASP609 ALL INITIATORS SET TO DRAINED")
        elif c=="$S INIT": log("$HASP609 INITIATOR 1 STARTED","sys")
        elif c=="$P INIT": log("$HASP609 INITIATOR 1 DRAINED","sys")
        elif c.startswith("$C JOB"):
            n=t[2] if len(t)>2 else ""; b=len(s["jobs"])
            s["jobs"]=[j for j in s["jobs"] if j["name"]!=n]
            reply([f"$HASP890 JOB {n} CANCELLED"] if len(s["jobs"])<b else [f"$HASP890 JOB {n} NOT FOUND"],"sys" if len(s["jobs"])<b else "error"); save()
        elif c.startswith("$H J"):
            n=t[2] if len(t)>2 else ""; s["held"].append(n); log(f"$HASP890 JOB {n} HELD","sys"); save()
        elif c.startswith("$O J"):
            n=t[2] if len(t)>2 else ""; s["held"]=[x for x in s["held"] if x!=n]; log(f"$HASP890 JOB {n} RELEASED","sys"); save()
        elif c=="$T": log("$HASP609 JES2 PARAMETERS DISPLAYED: SPOOL=OK, JOBCLASS=A AVAILABLE")
        elif c.startswith("VARY"):
            p=c.replace(","," ").split()
            if len(p)>=3:
                log(f"IEE301I {p[1]} {p[2]}","sys")
                if p[1] in s["devices"] and p[2]=="OFFLINE": s["devices"][p[1]]+=" (OFFLINE)"
                save()
            else: log("USAGE: VARY dev,ONLINE|OFFLINE","error")
        elif c.startswith("MOUNT"):
            v=t[1] if len(t)>1 else ""
            if v in s["volumes"]: log(f"IEF502I {v} MOUNTED ON DEVICE {s['volumes'][v]['device']}")
            else: log(f"IEF203I VOLUME {v} NOT KNOWN","error")
        elif c.startswith("UNMOUNT"):
            v=t[1] if len(t)>1 else ""
            if v in s["volumes"]: log(f"IEF503I {v} UNMOUNTED","sys")
            else: log(f"IEF203I VOLUME {v} NOT KNOWN","error")
        elif c=="D NET": log("IST350I DISPLAY TYPE = MAJOR NODES  IST089I TK5NET ACTIVE")
        elif c.startswith("D NET,MAJNODES"): log("IST089I TK5NET ACTIVE  IST089I APPLMAJ ACTIVE")
        elif c.startswith("VARY NET"):
            p=c.replace(","," ").split()
            if len(p)>=4: log(f"IST093I {p[3].split('=')[1]} {p[2]} COMPLETE","sys")
            else: log("USAGE: VARY NET,ACT|INACT,ID=node","error")
        elif c=="SMPE RECEIVE": s["smpe"]["sysmods"]["DUMY001"]="RECEIVED"; log("GIM20501I RECEIVE COMPLETE FOR DUMY001","sys"); save()
        elif c=="SMPE APPLY":
            if s["smpe"]["sysmods"].get("DUMY001")=="RECEIVED": s["smpe"]["sysmods"]["DUMY001"]="APPLIED"; log("GIM23906I APPLY COMPLETE IN TK5TZN","sys")
            else: log("GIM20502I DUMY001 MUST BE RECEIVED FIRST","error")
            save()
        elif c=="SMPE ACCEPT":
            if s["smpe"]["sysmods"].get("DUMY001")=="APPLIED": s["smpe"]["sysmods"]["DUMY001"]="ACCEPTED"; log("GIM23906I ACCEPT COMPLETE IN TK5DLB","sys")
            else: log("GIM20502I DUMY001 MUST BE APPLIED FIRST","error")
            save()
        elif c=="SMPE RESTORE":
            if s["smpe"]["sysmods"].get("DUMY001")=="APPLIED": s["smpe"]["sysmods"]["DUMY001"]="RECEIVED"; log("GIM23906I RESTORE COMPLETE FOR DUMY001","sys")
            else: log("GIM20502I DUMY001 NOT IN APPLIED STATUS","error")
            save()
        elif c=="SMPE QUERY": log("GIM20501I DUMY001 STATUS=" + s["smpe"]["sysmods"].get("DUMY001","NOT RECEIVED"))
        elif c.startswith("LISTDS"):
            d=t[1] if len(t)>1 else ""
            if d in s["datasets"]:
                x=s["datasets"][d]; log(f"{d} {x['type']} VOL={x['vol']} RECFM={x['recfm']} LRECL={x['lrecl']} MEMBERS={','.join(x['members']) or 'NONE'}")
            else: log(f"IDC3012I ITEM '{d}' DOES NOT EXIST","error")
        elif c=="LISTA": log("IDC3203I ALLOCATION: USER.CNTL, USER.OUTPUT, SMPE.GLOBAL.CSI")
        elif c.startswith("SEND"): log("IEE763I MESSAGE SENT TO ALL USERS","sys")
        elif c.startswith("RO "): log("IEE763I ROUTED MESSAGE DELIVERED","sys")
        elif c=="CLEAR": s["console"]=[]; log("CONSOLE CLEARED","sys"); save()
        else: log(f"IEE341I {cmd}: COMMAND NOT RECOGNIZED","error")
        st.rerun()

with tabs[1]:
    st.subheader("SDSF-style job queue")
    if s["jobs"]:
        st.table([{"Job":j["name"],"JobID":"JOB"+j["id"],"Owner":j["owner"],"Class":j["class"],"Status":j["status"],"Return code":j["retcode"]} for j in s["jobs"]])
    else: st.info("No jobs. Use `S START` or submit sample JCL.")
    if s["held"]: st.warning("Held output: "+", ".join(s["held"]))

with tabs[2]:
    st.subheader("Simulated job output")
    st.code("""1                        J E S 2  J O B  L O G
0  DUMYJOB  JOB00421  IEF452I DUMYJOB JOB00421 ENDED - RC=0000
0  DUMYJOB  JOB00421  IEF404I DUMYJOB ENDED - TIME=07.45.00
0  DUMYJOB  JOB00421  $HASP309 INIT1  INACTIVE
0  DUMYJOB  JOB00421  IEF375I  JOB/STEP1/START  RC=0000
0  DUMYJOB  JOB00421  IEF376I  JOB/STEP1/STOP   RC=0000""",language="text")

with tabs[3]:
    st.subheader("Devices")
    st.table([{"Device":d,"Description":v} for d,v in s["devices"].items()])
    st.subheader("Volumes")
    st.table([{"Volume":v,"Status":d["status"],"Device":d["device"],"Type":d["type"]} for v,d in s["volumes"].items()])
    st.subheader("Datasets")
    st.table([{"Dataset":k,"Type":v["type"],"Volume":v["vol"],"RECFM":v["recfm"],"LRECL":v["lrecl"],"Members":", ".join(v["members"]) or "None"} for k,v in s["datasets"].items()])

with tabs[4]:
    st.subheader("IPL / system status")
    st.code("""IEA101A SPECIFY SYSTEM PARAMETERS FOR IPL
IEE252I MVS/TK5 SYSTEM INITIALIZATION COMPLETE
IEE041I THE SYSTEM LOG IS NOW ACTIVE
IEE360I PAGE DATASET STATUS: ALL DATASETS AVAILABLE
$HASP426 SPECIFY OPTIONS - JES2 INITIALIZATION
$HASP100 DUMYJOB ON READER1
$HASP375 DUMYJOB ESTIMATED  LINES=00000000
$HASP373 DUMYJOB STARTED - INIT 1 - CLASS A
IEF403I DUMYJOB - STARTED - TIME=07.45.00
IEF404I DUMYJOB - ENDED - TIME=07.45.02""",language="text")
    if st.button("Simulate IPL"):
        s["system"]["ipl"]="IN PROGRESS"; log("IEA101A IPL STARTED","sys"); save(); st.rerun()
    if st.button("Complete IPL"):
        s["system"]["ipl"]="COMPLETE"; log("IEE252I IPL COMPLETE - SYSTEM READY","sys"); save(); st.rerun()

with tabs[5]:
    st.subheader("SMP/E zones")
    st.table([{"Zone":z,"Type":r} for z,r in s["smpe"]["zones"].items()])
    st.subheader("SYSMOD status")
    st.code(json.dumps(s["smpe"]["sysmods"],indent=2),language="json")
    st.info("Lifecycle: RECEIVE -> APPLY -> ACCEPT. RESTORE backs out an applied SYSMOD.")

with tabs[6]:
    st.markdown(Path("notes/walkthrough.md").read_text())
    st.markdown(Path("notes/qa.md").read_text())
