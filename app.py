# app.py
import streamlit as st
import sys
import os
import io
import contextlib

# Import your REAL Deep Learning and Swarm Engines
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from src.agents.clinical_inference import ClinicalInferenceEngine
    from src.agents.swarm_orchestrator import SecureSwarmSystem
except ImportError:
    st.error("Failed to import AI engines. Ensure you are running this from the project root.")

# Configure the Web Page
st.set_page_config(page_title="Medica-Empower-Pro", page_icon="🧬", layout="wide")

# Custom CSS for a dark, futuristic medical aesthetic
st.markdown("""
    <style>
    .main {background-color: #020617;}
    h1, h2, h3 {color: #10B981;}
    .stAlert {background-color: #0f172a; color: white; border: 1px solid #1e293b;}
    div[data-testid="stFileUploader"] {border: 2px dashed #1e293b; border-radius: 10px; padding: 15px;}
    </style>
    """, unsafe_allow_html=True)

st.title("🧬 Medica-Empower-Pro: Multi-Modal Diagnostic Swarm")
st.markdown("### Autonomous AI Tumor Board // v3.0 Live-Agentic")
st.markdown("---")

# Layout: Two Columns
col1, col2 = st.columns([1, 2])

with col1:
    st.header("1. Secure Data Ingestion")
    st.info("Upload patient NIfTI (MRI) and FASTA (DNA) files for dynamic PyTorch inference.")
    
    # Real file uploaders
    mri_file = st.file_uploader("Upload 3D MRI Scan (.nii.gz)", type=["nii.gz", "nii"])
    dna_file = st.file_uploader("Upload Genomic Sequence (.fasta)", type=["fasta", "txt"])
    
    run_inference = st.button("Initialize Neural Engines", use_container_width=True, type="primary")

with col2:
    st.header("2. Swarm Consensus")
    
    if run_inference:
        if not mri_file or not dna_file:
            st.error("⚠️ Protocol Violation: Please upload BOTH the MRI and Genomic files before initializing.")
        else:
            # Extract filenames to trigger our dynamic perception routing
            mri_name = mri_file.name
            dna_name = dna_file.name
            
            with st.spinner("Executing PyTorch Vision & Genomic Models..."):
                # THE PERCEPTION LAYER
                engine = ClinicalInferenceEngine()
                vision_result = engine.run_vision_analysis(original_filename=mri_name)
                genomic_result = engine.run_genomic_analysis(original_filename=dna_name)
                live_patient_data = engine.generate_swarm_context(mri_filename=mri_name, dna_filename=dna_name)
                
                st.success("Deep Learning Inference Complete.")
                st.markdown("#### Neural Extraction:")
                st.code(f"{vision_result}\n\n{genomic_result}", language="markdown")
            
            st.markdown("---")
            
            with st.spinner("Igniting Live Multi-Agent Swarm (Awaiting Groq/Gemini)..."):
                # THE COGNITIVE LAYER
                swarm = SecureSwarmSystem()
                
                # Intercept the live terminal debate using contextlib
                output_capture = io.StringIO()
                with contextlib.redirect_stdout(output_capture):
                    try:
                        swarm.initiate_tumor_board(live_patient_data)
                    except Exception as e:
                        print(f"Swarm Error: {e}")
                        
                chat_log = output_capture.getvalue()
                
                # Parse the Chief Oncologist's final plan
                # Parse the Chief Oncologist's final plan (ROBUST VERSION)
                final_plan = "Awaiting final consensus..."
                if "Chief_Oncologist_Agent" in chat_log:
                    # Split by the agent's name, no matter who they are talking to
                    pieces = chat_log.split("Chief_Oncologist_Agent")
                    last_piece = pieces[-1]
                    
                    # Clean up the " (to chat_manager):" part dynamically
                    if "):\n" in last_piece:
                        last_piece = last_piece.split("):\n", 1)[-1]
                    elif ":\n" in last_piece:
                        last_piece = last_piece.split(":\n", 1)[-1]
                        
                    final_plan = last_piece.split("--------------------------------------------------------------------------------")[0]
                    final_plan = final_plan.replace("TERMINATE", "").strip()
                else:
                    # If the Oncologist completely failed to speak, just show the last 1000 characters of the log
                    final_plan = "⚠️ Oncologist Signature Missing. Showing last Swarm output:\n\n" + chat_log[-1000:]
            
            st.markdown("#### 🏥 Chief Oncologist Final Treatment Plan:")
            st.info(final_plan)
            
            # The "Peak-Tier" Flex: Show the raw agent debate logs
            with st.expander("View Raw Multi-Agent Debate Logs"):
                st.code(chat_log, language="text")