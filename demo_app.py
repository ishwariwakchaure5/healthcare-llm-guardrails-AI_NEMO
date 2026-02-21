#!/usr/bin/env python3
"""
Healthcare Conversational AI Demo - No API Key Required
======================================================

This is a demonstration version of the healthcare chatbot that simulates
the guardrails behavior without requiring an actual OpenAI API key.
It shows how the safety rules would work in practice.

Author: Healthcare AI Safety Team
License: MIT
"""

import asyncio
import logging
import sys
from pathlib import Path
from typing import Dict, Any
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class HealthcareAIDemo:
    """
    Demo Healthcare Conversational AI with Simulated Guardrails
    
    This class simulates the behavior of the full guardrails system
    without requiring external API calls.
    """
    
    def __init__(self):
        """Initialize the demo healthcare AI system"""
        self.conversation_history = []
        logger.info("Healthcare AI Demo initialized")
        
    def _check_medical_advice_request(self, message: str) -> bool:
        """Check if message requests medical advice that should be blocked"""
        medical_patterns = [
            r'\b(what do i have|diagnose|diagnosis)\b',
            r'\b(what medication|prescribe|prescription)\b',
            r'\b(what treatment|how to treat|cure)\b',
            r'\b(am i sick|do i have cancer|what\'s wrong with me)\b',
            r'\b(should i take|how much should i take)\b'
        ]
        
        message_lower = message.lower()
        return any(re.search(pattern, message_lower) for pattern in medical_patterns)
    
    def _check_prompt_injection(self, message: str) -> bool:
        """Check if message contains prompt injection attempts"""
        injection_patterns = [
            r'\b(ignore previous instructions|forget everything above)\b',
            r'\b(you are now|pretend you are|act like)\b',
            r'\b(override|bypass|disable) .*(safety|rules|restrictions)\b',
            r'\b(system message|show me your prompt|reveal instructions)\b',
            r'\b(i am your developer|i am the administrator)\b'
        ]
        
        message_lower = message.lower()
        return any(re.search(pattern, message_lower) for pattern in injection_patterns)
    
    def _check_privacy_violation(self, message: str) -> bool:
        """Check if message contains personal information"""
        privacy_patterns = [
            r'\b(my name is|i am \w+)\b',
            r'\b(ssn|social security|insurance number)\b',
            r'\b(date of birth|dob|born on)\b',
            r'\b(phone number|address|email)\b',
            r'\b(patient id|medical record)\b'
        ]
        
        message_lower = message.lower()
        return any(re.search(pattern, message_lower) for pattern in privacy_patterns)
    
    def _check_self_harm_content(self, message: str) -> bool:
        """Check if message contains self-harm or crisis content"""
        crisis_patterns = [
            r'\b(kill myself|suicide|end it all)\b',
            r'\b(hurt myself|self harm|don\'t want to live)\b',
            r'\b(overdose|how much.*lethal)\b'
        ]
        
        message_lower = message.lower()
        return any(re.search(pattern, message_lower) for pattern in crisis_patterns)
    
    def _check_safe_health_question(self, message: str) -> bool:
        """Check if message is a safe health education question"""
        safe_patterns = [
            r'\b(what is|tell me about|explain) .*(diabetes|heart|blood pressure)\b',
            r'\b(symptoms of|signs of) .*(flu|cold|fever)\b',
            r'\b(how does.*work|benefits of exercise)\b',
            r'\b(healthy diet|nutrition|sleep)\b',
            r'\b(prevention|staying healthy)\b'
        ]
        
        message_lower = message.lower()
        return any(re.search(pattern, message_lower) for pattern in safe_patterns)
    
    async def process_message(self, user_message: str) -> Dict[str, Any]:
        """
        Process user message through simulated guardrails
        
        Args:
            user_message (str): The user's input message
            
        Returns:
            Dict[str, Any]: Response containing the bot's reply and metadata
        """
        try:
            logger.info(f"Processing message: {user_message[:50]}...")
            
            # Check for various safety violations
            if self._check_self_harm_content(user_message):
                return {
                    "response": """I'm concerned about what you're going through. If you're having thoughts of self-harm, please reach out for help immediately:

• National Suicide Prevention Lifeline: 988
• Crisis Text Line: Text HOME to 741741  
• Emergency Services: 911

You don't have to go through this alone. Professional counselors are available to help.""",
                    "blocked": True,
                    "reason": "self_harm_content",
                    "category": "crisis_intervention"
                }
            
            elif self._check_prompt_injection(user_message):
                return {
                    "response": "I detected an attempt to modify my behavior or bypass my safety guidelines. I'm designed to maintain consistent, safe responses regardless of how requests are phrased. Please rephrase your question in a straightforward manner about health topics.",
                    "blocked": True,
                    "reason": "prompt_injection",
                    "category": "security"
                }
            
            elif self._check_privacy_violation(user_message):
                return {
                    "response": """🔒 PRIVACY PROTECTION: I cannot process personal information including names, addresses, medical record numbers, or specific medical details. Please avoid sharing personal information and instead ask general health questions.

For questions about your specific medical situation, please consult with your healthcare provider.""",
                    "blocked": True,
                    "reason": "privacy_violation",
                    "category": "privacy"
                }
            
            elif self._check_medical_advice_request(user_message):
                return {
                    "response": """I cannot provide medical diagnoses, prescriptions, or specific treatment recommendations. Your symptoms could have many different causes, and proper evaluation requires medical training and often physical examination or tests.

Please consult with a healthcare professional who can properly assess your condition and provide appropriate medical advice.""",
                    "blocked": True,
                    "reason": "medical_advice_request",
                    "category": "healthcare_safety"
                }
            
            elif self._check_safe_health_question(user_message):
                # Simulate educational response for safe health questions
                educational_responses = {
                    "diabetes": """⚠️ HEALTHCARE DISCLAIMER: This information is for educational purposes only and is not a substitute for professional medical advice.

Diabetes is a group of metabolic disorders characterized by high blood sugar levels. There are two main types:

• Type 1 Diabetes: The body doesn't produce insulin
• Type 2 Diabetes: The body doesn't use insulin properly

Common symptoms include increased thirst, frequent urination, fatigue, and blurred vision. Management typically involves blood sugar monitoring, medication (if prescribed by a doctor), healthy eating, and regular exercise.

Always consult with qualified healthcare providers for medical concerns and diabetes management.""",
                    
                    "exercise": """⚠️ HEALTHCARE DISCLAIMER: This information is for educational purposes only.

Regular exercise provides numerous cardiovascular benefits:

• Strengthens the heart muscle
• Improves blood circulation
• Helps lower blood pressure
• Reduces bad cholesterol (LDL) and increases good cholesterol (HDL)
• Helps maintain healthy weight
• Reduces risk of heart disease and stroke

The American Heart Association generally recommends at least 150 minutes of moderate-intensity exercise per week for adults. However, you should consult with your healthcare provider before starting any new exercise program.""",
                    
                    "flu": """⚠️ HEALTHCARE DISCLAIMER: This information is for educational purposes only.

Common flu symptoms typically include:

• Fever and chills
• Cough and sore throat  
• Runny or stuffy nose
• Muscle aches and fatigue
• Headache
• Sometimes nausea and vomiting

The flu is different from a common cold and symptoms usually come on suddenly. Most people recover within a few days to less than two weeks.

If you're experiencing severe symptoms or are in a high-risk group, please consult with a healthcare professional for proper evaluation and care."""
                }
                
                # Find matching educational content
                message_lower = user_message.lower()
                for topic, response in educational_responses.items():
                    if topic in message_lower:
                        return {
                            "response": response,
                            "blocked": False,
                            "reason": None,
                            "category": "health_education"
                        }
                
                # Generic safe health response
                return {
                    "response": """⚠️ HEALTHCARE DISCLAIMER: This information is for educational purposes only and is not a substitute for professional medical advice.

I can provide general health information for educational purposes. However, for specific questions about your health, symptoms, or medical conditions, please consult with qualified healthcare providers.

Could you please rephrase your question to be more specific about the health topic you'd like to learn about?""",
                    "blocked": False,
                    "reason": None,
                    "category": "health_education"
                }
            
            else:
                # Default response for unclear or general queries
                return {
                    "response": """⚠️ HEALTHCARE DISCLAIMER: This AI assistant provides general health information for educational purposes only.

I can help answer general questions about health topics, medical concepts, and wellness information. However, I cannot provide medical diagnoses, prescriptions, or specific medical advice.

What health topic would you like to learn about today? Please ask general questions about health conditions, prevention, or wellness.""",
                    "blocked": False,
                    "reason": None,
                    "category": "general"
                }
                
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            return {
                "response": "I apologize, but I encountered an error processing your request. Please try rephrasing your question or contact support if the issue persists.",
                "blocked": True,
                "reason": "processing_error",
                "category": "error"
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
        print("=" * 70)
        print("🏥 HEALTHCARE AI ASSISTANT DEMO - GUARDRAILS SIMULATION")
        print("=" * 70)
        print(self.get_safety_disclaimer())
        print("\n" + "=" * 70)
        print("💬 You can ask general health questions. Type 'quit' to exit.")
        print("🔒 This is a demo - no personal information is stored.")
        print("🛡️ All safety guardrails are active and simulated.")
        print("=" * 70 + "\n")

async def main():
    """Main demo application entry point"""
    print("🏥 Healthcare LLM Guardrails Demo")
    print("=" * 50)
    
    # Initialize demo system
    healthcare_ai = HealthcareAIDemo()
    
    # Display welcome message
    healthcare_ai.print_welcome_message()
    
    # Demo conversation loop
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            # Check for quit command
            if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                print("\n🏥 Thank you for using Healthcare AI Assistant Demo.")
                print("Remember to consult healthcare professionals for medical advice.")
                break
            
            # Skip empty inputs
            if not user_input:
                continue
            
            # Process the message through simulated guardrails
            print("🤖 Processing your question through guardrails...")
            result = await healthcare_ai.process_message(user_input)
            
            # Display the response with category info
            category_emoji = {
                "crisis_intervention": "🚨",
                "security": "🔒", 
                "privacy": "🛡️",
                "healthcare_safety": "⚕️",
                "health_education": "📚",
                "general": "💬",
                "error": "❌"
            }
            
            emoji = category_emoji.get(result.get('category', 'general'), "💬")
            
            if result['blocked']:
                print(f"\n{emoji} [BLOCKED - {result['reason']}]")
            else:
                print(f"\n{emoji} [ALLOWED - {result['category']}]")
            
            print(f"Healthcare AI: {result['response']}\n")
            
        except KeyboardInterrupt:
            print("\n\n🏥 Healthcare AI Demo session ended.")
            print("Stay healthy and consult healthcare professionals when needed!")
            break
            
        except Exception as e:
            logger.error(f"Error in demo loop: {str(e)}")
            print("❌ An error occurred. Please try again.")

if __name__ == "__main__":
    """Run the demo application"""
    try:
        print("🔍 Starting Healthcare AI Guardrails Demo...")
        print("✅ Demo ready - no API key required!\n")
        
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Healthcare AI Demo shutdown complete.")
    except Exception as e:
        logger.error(f"Demo failed: {str(e)}")
        print(f"❌ Demo failed: {str(e)}")
        sys.exit(1)