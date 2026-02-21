#!/usr/bin/env python3
"""
Healthcare Conversational AI with NVIDIA NeMo Guardrails - Full Demo
====================================================================

This application demonstrates the full NVIDIA NeMo Guardrails framework
for healthcare AI safety, with graceful handling for demo environments.

Author: Healthcare AI Safety Team
License: MIT
"""

import os
import sys
import asyncio
from typing import Optional, Dict, Any
import logging
from pathlib import Path

# Set demo API key if none exists
if not os.getenv("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = "sk-demo-key-for-testing-healthcare-guardrails"

try:
    from nemoguardrails import RailsConfig, LLMRails
    # Try to import set_verbose, but don't fail if it's not available
    try:
        from nemoguardrails.logging import set_verbose
    except ImportError:
        set_verbose = None
    NEMO_AVAILABLE = True
except ImportError as e:
    print(f"Warning: NVIDIA NeMo Guardrails import failed: {e}")
    print("Falling back to demo mode...")
    NEMO_AVAILABLE = False
    set_verbose = None

# Configure logging for safety monitoring
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('healthcare_ai_safety.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class HealthcareAIFull:
    """
    Healthcare Conversational AI with Full NeMo Guardrails Integration
    
    This class implements the complete healthcare chatbot using NVIDIA NeMo Guardrails
    with fallback to demo mode if the framework is not available.
    """
    
    def __init__(self, config_path: str = "config"):
        """
        Initialize the Healthcare AI with guardrails configuration
        
        Args:
            config_path (str): Path to the guardrails configuration directory
        """
        self.config_path = Path(config_path)
        self.rails_app: Optional[LLMRails] = None
        self.conversation_history = []
        self.demo_mode = not NEMO_AVAILABLE
        
        # Initialize the guardrails system
        self._initialize_guardrails()
        
    def _initialize_guardrails(self) -> None:
        """
        Load and initialize the NeMo Guardrails configuration
        """
        try:
            logger.info("Initializing Healthcare AI Guardrails...")
            
            if not NEMO_AVAILABLE:
                logger.warning("NeMo Guardrails not available - running in demo mode")
                return
            
            # Check if configuration directory exists
            if not self.config_path.exists():
                raise FileNotFoundError(f"Configuration directory not found: {self.config_path}")
            
            # Load the guardrails configuration
            config = RailsConfig.from_path(self.config_path)
            logger.info(f"Loaded configuration from: {self.config_path}")
            
            # Initialize the LLM Rails with healthcare guardrails
            self.rails_app = LLMRails(config)
            logger.info("Healthcare AI Guardrails initialized successfully")
            self.demo_mode = False
            
        except Exception as e:
            logger.error(f"Failed to initialize guardrails: {str(e)}")
            logger.warning("Falling back to demo mode...")
            self.demo_mode = True
    
    def _demo_process_message(self, user_message: str) -> Dict[str, Any]:
        """
        Demo processing when NeMo Guardrails is not available
        """
        import re
        
        # Simple pattern matching for demo
        message_lower = user_message.lower()
        
        # Check for medical advice requests
        if any(pattern in message_lower for pattern in [
            'diagnose', 'what do i have', 'prescribe', 'medication', 'treatment'
        ]):
            return {
                "response": "I cannot provide medical diagnoses, prescriptions, or specific treatment recommendations. Please consult with a healthcare professional who can properly assess your condition.",
                "blocked": True,
                "reason": "medical_advice_request"
            }
        
        # Check for prompt injection
        if any(pattern in message_lower for pattern in [
            'ignore previous', 'you are now', 'override', 'bypass'
        ]):
            return {
                "response": "I detected an attempt to modify my behavior. I'm designed to maintain consistent, safe responses. Please rephrase your question about health topics.",
                "blocked": True,
                "reason": "prompt_injection"
            }
        
        # Check for self-harm content
        if any(pattern in message_lower for pattern in [
            'kill myself', 'suicide', 'hurt myself', 'end it all'
        ]):
            return {
                "response": """I'm concerned about what you're going through. If you're having thoughts of self-harm, please reach out for help immediately:

• National Suicide Prevention Lifeline: 988
• Crisis Text Line: Text HOME to 741741
• Emergency Services: 911

You don't have to go through this alone.""",
                "blocked": True,
                "reason": "self_harm_content"
            }
        
        # Safe health education
        if any(pattern in message_lower for pattern in [
            'what is', 'symptoms of', 'how does', 'benefits of', 'diabetes', 'exercise', 'flu'
        ]):
            return {
                "response": f"""⚠️ HEALTHCARE DISCLAIMER: This information is for educational purposes only and is not a substitute for professional medical advice.

I can provide general information about health topics. However, for specific questions about your health, symptoms, or medical conditions, please consult with qualified healthcare providers.

Regarding your question about {user_message.lower()}: This appears to be a general health education question. In a full system, I would provide educational information with appropriate medical disclaimers.""",
                "blocked": False,
                "reason": None
            }
        
        # Default response
        return {
            "response": """⚠️ HEALTHCARE DISCLAIMER: This AI assistant provides general health information for educational purposes only.

I can help answer general questions about health topics, medical concepts, and wellness information. However, I cannot provide medical diagnoses, prescriptions, or specific medical advice.

What health topic would you like to learn about today?""",
            "blocked": False,
            "reason": None
        }
    
    async def process_message(self, user_message: str) -> Dict[str, Any]:
        """
        Process user message through the guardrails system
        
        Args:
            user_message (str): The user's input message
            
        Returns:
            Dict[str, Any]: Response containing the bot's reply and metadata
        """
        try:
            logger.info(f"Processing user message (length: {len(user_message)})")
            
            # Validate input
            if not user_message or not user_message.strip():
                return {
                    "response": "Please provide a valid question about health topics.",
                    "blocked": False,
                    "reason": "empty_input"
                }
            
            # Use demo mode if NeMo Guardrails not available
            if self.demo_mode or not self.rails_app:
                logger.info("Processing in demo mode")
                return self._demo_process_message(user_message.strip())
            
            # Process message through full NeMo Guardrails
            logger.info("Processing through NeMo Guardrails")
            response = await self.rails_app.generate_async(
                messages=[{"role": "user", "content": user_message.strip()}]
            )
            
            # Extract the response content
            bot_response = response.get("content", "I apologize, but I couldn't process your request safely.")
            
            # Log successful interaction
            logger.info("Message processed successfully through guardrails")
            
            return {
                "response": bot_response,
                "blocked": False,
                "reason": None
            }
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            
            # Return safe fallback response
            return {
                "response": "I apologize, but I encountered an error processing your request. Please try rephrasing your question or contact support if the issue persists.",
                "blocked": True,
                "reason": "processing_error"
            }
    
    def get_safety_disclaimer(self) -> str:
        """Get the standard healthcare safety disclaimer"""
        return """⚠️ IMPORTANT HEALTHCARE DISCLAIMER:
This AI assistant provides general health information for educational purposes only. 
It is not a substitute for professional medical advice, diagnosis, or treatment. 
Always consult with qualified healthcare providers for medical concerns.
In case of emergency, contact emergency services (911) immediately."""
    
    def print_welcome_message(self) -> None:
        """Print welcome message and safety information"""
        mode_info = "DEMO MODE" if self.demo_mode else "FULL NEMO GUARDRAILS"
        
        print("=" * 70)
        print(f"🏥 HEALTHCARE AI ASSISTANT - {mode_info}")
        print("=" * 70)
        print(self.get_safety_disclaimer())
        print("\n" + "=" * 70)
        print("💬 You can ask general health questions. Type 'quit' to exit.")
        print("🔒 Your privacy is protected - no personal information is stored.")
        
        if self.demo_mode:
            print("⚠️ Running in demo mode - NeMo Guardrails simulation active.")
        else:
            print("✅ Full NeMo Guardrails framework active.")
            
        print("=" * 70 + "\n")

async def main():
    """Main application entry point"""
    print("🏥 Healthcare LLM Guardrails - Full System")
    print("=" * 50)
    
    try:
        # Initialize the Healthcare AI system
        healthcare_ai = HealthcareAIFull()
        
        # Display welcome message and safety information
        healthcare_ai.print_welcome_message()
        
        # Main conversation loop
        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()
                
                # Check for quit command
                if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                    print("\n🏥 Thank you for using Healthcare AI Assistant.")
                    print("Remember to consult healthcare professionals for medical advice.")
                    break
                
                # Skip empty inputs
                if not user_input:
                    continue
                
                # Process the message through guardrails
                print("🤖 Processing your question safely...")
                result = await healthcare_ai.process_message(user_input)
                
                # Display the response
                status_indicator = "🚫 [BLOCKED]" if result['blocked'] else "✅ [ALLOWED]"
                if result['blocked'] and result['reason']:
                    status_indicator += f" ({result['reason']})"
                
                print(f"\n{status_indicator}")
                print(f"Healthcare AI: {result['response']}\n")
                
                # Log if message was blocked (for monitoring)
                if result['blocked']:
                    logger.warning(f"Message blocked - Reason: {result['reason']}")
                
            except KeyboardInterrupt:
                print("\n\n🏥 Healthcare AI Assistant session ended.")
                print("Stay healthy and consult healthcare professionals when needed!")
                break
                
            except Exception as e:
                logger.error(f"Error in conversation loop: {str(e)}")
                print("❌ An error occurred. Please try again or restart the application.")
    
    except Exception as e:
        logger.error(f"Critical error in main application: {str(e)}")
        print(f"❌ Failed to start Healthcare AI Assistant: {str(e)}")
        print("Please check your configuration and try again.")
        sys.exit(1)

def check_environment() -> bool:
    """Check if the environment is properly configured"""
    # Check for required configuration files
    required_files = [
        "config/config.yml",
        "rails/healthcare.co",
        "rails/safety.co", 
        "rails/injection.co",
        "rails/privacy.co"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing required configuration files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    
    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️ Warning: OPENAI_API_KEY environment variable not set.")
        print("   Using demo API key for testing purposes.")
        os.environ["OPENAI_API_KEY"] = "sk-demo-key-for-testing-healthcare-guardrails"
    
    return True

if __name__ == "__main__":
    """Application entry point with environment validation"""
    print("🔍 Checking environment configuration...")
    
    if not check_environment():
        print("\n❌ Environment check failed. Please ensure all configuration files exist.")
        sys.exit(1)
    
    print("✅ Environment check passed. Starting Healthcare AI Assistant...\n")
    
    # Run the async main function
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Healthcare AI Assistant shutdown complete.")
    except Exception as e:
        logger.error(f"Unhandled exception: {str(e)}")
        print(f"❌ Critical error: {str(e)}")
        sys.exit(1)