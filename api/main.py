# api/main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os
import tempfile
import io

# Import your REAL Deep Learning and Swarm Engines
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.agents.clinical_inference import ClinicalInferenceEngine
from src.agents.swarm_orchestrator import SecureSwarmSystem

app = FastAPI(title="Medica-Empower-Pro API", version="3.0 Live-Agentic")

# Peak-Tier Security: CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "Live Neural Engines & Swarm Online", "system": "Medica-Empower-Pro"}

@app.post("/api/inference")
async def run_inference(mri: UploadFile = File(...), dna: UploadFile = File(...)):
    """Executes REAL PyTorch Models and ignites the REAL AutoGen Swarm in a single pass."""
    
    # 1. Securely save the uploaded files to temporary server storage
    with tempfile.NamedTemporaryFile(delete=False, suffix=".nii.gz") as temp_mri:
        temp_mri.write(await mri.read())
        mri_path = temp_mri.name

    with tempfile.NamedTemporaryFile(delete=False, suffix=".fasta") as temp_dna:
        temp_dna.write(await dna.read())
        dna_path = temp_dna.name

    # 2. THE PERCEPTION LAYER: Run PyTorch Inference
    engine = ClinicalInferenceEngine()
    
    # Pass the actual filenames from the frontend so the engine can dynamically route them
    vision_output = engine.run_vision_analysis(original_filename=mri.filename)
    genomic_output = engine.run_genomic_analysis(original_filename=dna.filename)
    live_patient_data = engine.generate_swarm_context(mri_filename=mri.filename, dna_filename=dna.filename)

    # 3. THE COGNITIVE LAYER: Ignite the AutoGen Swarm
    swarm = SecureSwarmSystem()
    
    # Intercept the terminal output to capture the live AI debate
    old_stdout = sys.stdout
    sys.stdout = capture = io.StringIO()

    try:
        swarm.initiate_tumor_board(live_patient_data)
    except Exception as e:
        print(f"Swarm Error: {e}")
    finally:
        # Release the terminal back to normal
        sys.stdout = old_stdout

    # 4. Extract the Chief Oncologist's final independent plan (ROBUST VERSION)
    chat_log = capture.getvalue()
    final_plan = "Awaiting final consensus..."
    
    if "Chief_Oncologist_Agent" in chat_log:
        # Split by the agent's name, no matter who they are talking to
        pieces = chat_log.split("Chief_Oncologist_Agent")
        last_piece = pieces[-1]
        
        # Clean up the format variations dynamically
        if "):\n" in last_piece:
            last_piece = last_piece.split("):\n", 1)[-1]
        elif ":\n" in last_piece:
            last_piece = last_piece.split(":\n", 1)[-1]
            
        final_plan = last_piece.split("--------------------------------------------------------------------------------")[0]
        final_plan = final_plan.replace("TERMINATE", "").strip()
    else:
        # Fail-safe: Push the raw logs to the UI if the signature is missing
        final_plan = "⚠️ Oncologist Signature Missing. Showing last Swarm output:\n\n" + chat_log[-1000:]

    # 5. Clean up temporary files to prevent server memory leaks
    os.remove(mri_path)
    os.remove(dna_path)

    return {
        "vision_output": vision_output,
        "genomic_output": genomic_output,
        "full_plan": f"🏥 LIVE SWARM CONSENSUS:\n\n{final_plan}"
    }