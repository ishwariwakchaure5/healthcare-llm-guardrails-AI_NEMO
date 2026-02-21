#!/usr/bin/env python3
"""
Healthcare Conversational AI with NVIDIA NeMo Guardrails
========================================================

This application implements a healthcare chatbot with comprehensive safety guardrails
using NVIDIA NeMo Guardrails framework. The system includes:
- Healthcare-specific safety rules
- Privacy protection (HIPAA compliance)
- Prompt injection prevention
- General safety measures

Author: Healthcare AI Safety Team
License: MIT
"""

import os
import sys
import asyncio
from typing import Optional, Dict, Any
import logging
from pathlib import Path

try:
    from nemoguardrails import RailsConfig, LLMRails
    from nemoguardrails.logging import set_verbose
except ImportError:
    print("Error: NVIDIA NeMo Guardrails not installed.")
    print("Please install with: pip install nemoguardrails")
    sys.exit(1)

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

class HealthcareAI:
    """
    Healthcare Conversational AI with Safety Guardrails
    
    This class implements a healthcare chatbot that uses NVIDIA NeMo Guardrails
    to ensure safe, compliant, and helpful interactions while preventing:
    - Medical misuse (diagnosis, prescriptions)
    - Privacy violations (PHI exposure)
    - Prompt injection attacks
    - Harmful content generation
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
        
        # Initialize the guardrails system
        self._initialize_guardrails()
        
    def _initialize_guardrails(self) -> None:
        """
        Load and initialize the NeMo Guardrails configuration
        
        This method:
        1. Loads the configuration from config.yml
        2. Initializes all guardrail rules (.co files)
        3. Sets up the LLM backend
        4. Configures safety monitoring
        """
        try:
            logger.info("Initializing Healthcare AI Guardrails...")
            
            # Check if configuration directory exists
            if not self.config_path.exists():
                raise FileNotFoundError(f"Configuration directory not found: {self.config_path}")
            
            # Load the guardrails configuration
            config = RailsConfig.from_path(self.config_path)
            logger.info(f"Loaded configuration from: {self.config_path}")
            
            # Initialize the LLM Rails with healthcare guardrails
            self.rails_app = LLMRails(config)
            logger.info("Healthcare AI Guardrails initialized successfully")
            
            # Enable verbose logging for safety monitoring (optional)
            # set_verbose(True)
            
        except Exception as e:
            logger.error(f"Failed to initialize guardrails: {str(e)}")
            raise RuntimeError(f"Guardrails initialization failed: {str(e)}")
    
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
            
            # Process message through guardrails
            response = await self.rails_app.generate_async(
                messages=[{"role": "user", "content": user_message.strip()}]
            )
            
            # Extract the response content
            bot_response = response.get("content", "I apologize, but I couldn't process your request safely.")
            
            # Log successful interaction (without storing personal data)
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
        """
        Get the standard healthcare safety disclaimer
        
        Returns:
            str: Healthcare safety disclaimer text
        """
        return """
⚠️ IMPORTANT HEALTHCARE DISCLAIMER:
This AI assistant provides general health information for educational purposes only. 
It is not a substitute for professional medical advice, diagnosis, or treatment. 
Always consult with qualified healthcare providers for medical concerns.
In case of emergency, contact emergency services (911) immediately.
        """.strip()
    
    def print_welcome_message(self) -> None:
        """Print welcome message and safety information"""
        print("=" * 70)
        print("🏥 HEALTHCARE AI ASSISTANT WITH SAFETY GUARDRAILS")
        print("=" * 70)
        print(self.get_safety_disclaimer())
        print("\n" + "=" * 70)
        print("💬 You can ask general health questions. Type 'quit' to exit.")
        print("🔒 Your privacy is protected - no personal information is stored.")
        print("=" * 70 + "\n")

async def main():
    """
    Main application entry point
    
    This function:
    1. Initializes the Healthcare AI system
    2. Runs the interactive chat loop
    3. Handles user input and displays responses
    4. Manages graceful shutdown
    """
    try:
        # Initialize the Healthcare AI system
        healthcare_ai = HealthcareAI()
        
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
                print(f"\nHealthcare AI: {result['response']}\n")
                
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
    """
    Check if the environment is properly configured
    
    Returns:
        bool: True if environment is ready, False otherwise
    """
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
    
    # Check for OpenAI API key (if using OpenAI backend)
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY environment variable not set.")
        print("   You may need to set this if using OpenAI as your LLM backend.")
    
    return True

if __name__ == "__main__":
    """
    Application entry point with environment validation
    """
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