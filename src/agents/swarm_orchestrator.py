import os
import logging
from dotenv import load_dotenv
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager, register_function
import requests
import json

# Configure enterprise-grade logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("Medica-Empower-Pro-Orchestrator")

# --- THE RAG DATABASE TOOL ---
# --- THE LIVE RAG DATABASE TOOL (PUBMED) ---
def search_medical_database(query: str) -> str:
    """Searches the LIVE US National Library of Medicine (PubMed) for clinical research."""
    logger.info(f"🔍 RAG TRIGGERED: Querying Live PubMed API for '{query}'...")
    
    try:
        # Step 1: Search PubMed for the top 3 most relevant article IDs
        search_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={query}[Title/Abstract]&retmode=json&retmax=3"
        search_resp = requests.get(search_url, timeout=5).json()
        
        id_list = search_resp.get("esearchresult", {}).get("idlist", [])
        if not id_list:
            return f"[LIVE PUBMED RAG]: No recent clinical trials found for '{query}'."
            
        # Step 2: Fetch the actual titles and metadata for those IDs
        ids_string = ",".join(id_list)
        summary_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={ids_string}&retmode=json"
        summary_resp = requests.get(summary_url, timeout=5).json()
        
        results = []
        for uid in id_list:
            title = summary_resp["result"][uid]["title"]
            results.append(f"- {title}")
            
        final_rag_data = f"[LIVE PUBMED RAG - Top Research for '{query}']:\n" + "\n".join(results)
        return final_rag_data
        
    except Exception as e:
        logger.error(f"PubMed API Error: {e}")
        return "[LIVE DB RESULT]: Network timeout. Proceed with standard medical guidelines."
        
class SecureSwarmSystem:
    def __init__(self):
        """Initializes the secure Multi-Agent Swarm with Dual-Engine Auto-Fallback."""
        load_dotenv()
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.groq_key = os.getenv("GROQ_API_KEY")
        
        # The verified robust dual-engine config
        self.llm_config = {
            "config_list": [
                {
                    "model": "llama-3.1-8b-instant", 
                    "api_key": self.groq_key,
                    "api_type": "openai",
                    "base_url": "https://api.groq.com/openai/v1" 
                },
                {
                    "model": "gemini-2.5-flash", 
                    "api_key": self.gemini_key,
                    "api_type": "google"
                }
            ],
            "temperature": 0.1, 
        }

    def build_agents(self):
        """Constructs the specialized medical agents with Tool Execution capabilities."""
        
        radiologist = AssistantAgent(
            name="Radiologist_Agent",
            system_message="You are an expert AI Radiologist. Analyze structural anomaly data derived from Vision Transformers. Provide precise anatomical assessments. DO NOT output the word TERMINATE.",
            llm_config=self.llm_config,
        )

        pharmacologist = AssistantAgent(
            name="Pharmacologist_Agent",
            system_message="""You are an expert Pharmacologist. Analyze genomic pathways. 
            CRITICAL INSTRUCTION: You MUST use the `search_medical_database` tool to look up the latest clinical trials for the specific drugs or biomarkers (like temozolomide, mgmt, or gbm) mentioned in the patient data before you give your recommendation. 
            DO NOT output the word TERMINATE.""",
            llm_config=self.llm_config,
        )

        chief_oncologist = AssistantAgent(
            name="Chief_Oncologist_Agent",
            system_message="""You are the Chief Medical Officer. You must synthesize the structural PyTorch outputs and the live PubMed literature pulled by the Pharmacologist. 
            
            You are FORBIDDEN from giving generic answers. Your final response MUST strictly follow this exact markdown format:
            
            ### 🔬 Clinical Diagnosis
            (Detail the tumor size, location, and genomic biomarkers)
            
            ### 📚 Live PubMed Literature Review
            (Summarize the specific clinical trial data and efficacy rates found by the Pharmacologist's live search)
            
            ### 💊 Synergistic Treatment Protocol
            (List the specific surgical, radiation, and multi-drug interventions recommended)
            
            Once this exact structure is fully completely written, you MUST end your response with the exact word: TERMINATE.""",
            llm_config=self.llm_config,
        )

        # The Proxy now has execution capabilities to run the tools on behalf of the agents
        patient_proxy = UserProxyAgent(
            name="Secure_Data_Pipeline",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=10,
            is_termination_msg=lambda msg: "TERMINATE" in msg.get("content", "").upper(),
            code_execution_config={"use_docker": False} # Allow local tool execution
        )
        
        # --- REGISTER THE TOOL ---
        # This gives the Pharmacologist the "brain" to know the tool exists, 
        # and the Proxy the "hands" to actually run the Python code.
        register_function(
            search_medical_database,
            caller=pharmacologist,
            executor=patient_proxy,
            name="search_medical_database",
            description="Searches the live medical database for clinical trials and drug interactions. Pass a single keyword string like 'temozolomide' or 'gbm'."
        )
        
        return patient_proxy, [radiologist, pharmacologist, chief_oncologist]

    def initiate_tumor_board(self, clinical_data: str):
        """Starts the multi-agent consensus protocol."""
        proxy, agents = self.build_agents()
        
        groupchat = GroupChat(
            agents=[proxy] + agents,
            messages=[],
            max_round=15,
            speaker_selection_method="round_robin" 
        )
        manager = GroupChatManager(groupchat=groupchat, llm_config=self.llm_config)
        
        logger.info("Initiating Multi-Agent Tumor Board Consensus with Live RAG...")
        proxy.initiate_chat(
            manager,
            message=f"SECURE CLINICAL INGESTION:\n{clinical_data}\n\nTask: Debate findings, search literature, and formulate final multimodal treatment plan."
        )