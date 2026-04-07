import os
import logging
from dotenv import load_dotenv
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

# Configure enterprise-grade logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("Medica-Empower-Pro-Orchestrator")

class SecureSwarmSystem:
    def __init__(self):
        """Initializes the secure Multi-Agent Swarm with a Dual-Engine Auto-Fallback."""
        load_dotenv()
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.groq_key = os.getenv("GROQ_API_KEY")
        
        if not self.gemini_key or not self.groq_key:
            logger.error("CRITICAL: Missing API Keys in environment.")
            raise ValueError("System Initialization Failed: Secure credentials incomplete.")
            
        # The Dual-Engine Config List
        # AutoGen will try Gemini first. If it hits a rate limit or fails, it instantly falls back to Groq.
        # The Dual-Engine Config List (Groq Promoted to Primary)
        self.llm_config = {
            "config_list": [
                {
                    # Tier 1: Primary Engine (Meta Llama 3 70B via Groq)
                    # Uses standard OpenAI structure, flawless AutoGen integration, massive free quota.
                    "model": "llama-3.3-70b-versatile", 
                    "api_key": self.groq_key,
                    "api_type": "openai",
                    "base_url": "https://api.groq.com/openai/v1" 
                },
                {
                    # Tier 2: Fallback Engine (Gemini 2.5 Flash)
                    "model": "gemini-2.5-flash",
                    "api_key": self.gemini_key,
                    "api_type": "google"
                }
            ],
            "temperature": 0.1, 
        }
        logger.info("Secure Swarm System Initialized: Groq Primary -> Gemini Fallback.")

    def build_agents(self):
        """Constructs the specialized medical agents."""
        
        radiologist = AssistantAgent(
            name="Radiologist_Agent",
            system_message="You are an expert AI Radiologist. Analyze structural anomaly data derived from Vision Transformers. Provide precise anatomical assessments.",
            llm_config=self.llm_config,
        )

        pharmacologist = AssistantAgent(
            name="Pharmacologist_Agent",
            system_message="You are an expert Pharmacologist. Analyze genomic pathways and graph data. Formulate targeted therapies and flag drug interactions.",
            llm_config=self.llm_config,
        )

        chief_oncologist = AssistantAgent(
            name="Chief_Oncologist_Agent",
            system_message="You are the lead physician. Synthesize multi-modal inputs. Mediate discrepancies. Output a structured, actionable treatment plan. When the final plan is complete, you MUST end your response with the exact word: TERMINATE.",
            llm_config=self.llm_config,
        )

        patient_proxy = UserProxyAgent(
            name="Secure_Data_Pipeline",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=10,
            is_termination_msg=lambda msg: "TERMINATE" in msg.get("content", "").upper(), # <-- The Kill Switch
            code_execution_config=False 
        )
        
        return patient_proxy, [radiologist, pharmacologist, chief_oncologist]

    def initiate_tumor_board(self, clinical_data: str):
        """Starts the multi-agent consensus protocol."""
        proxy, agents = self.build_agents()
        
        groupchat = GroupChat(
            agents=[proxy] + agents,
            messages=[],
            max_round=12
        )
        manager = GroupChatManager(groupchat=groupchat, llm_config=self.llm_config)
        
        logger.info("Initiating Multi-Agent Tumor Board Consensus...")
        proxy.initiate_chat(
            manager,
            message=f"SECURE CLINICAL INGESTION:\n{clinical_data}\n\nTask: Debate findings and formulate final multimodal treatment plan."
        )

if __name__ == "__main__":
    # Test execution
    swarm = SecureSwarmSystem()
    
    # Mock data (This will later be replaced by the output from your Colab-trained models)
    mock_ingestion = """
    [ViT Output]: 3D scan indicates 4.2cm irregular mass in left frontal lobe.
    [GNN Output]: Patient exhibits MGMT promoter methylation; high sensitivity to alkylating agents.
    """
    
    swarm.initiate_tumor_board(mock_ingestion)