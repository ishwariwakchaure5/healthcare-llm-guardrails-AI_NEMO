#!/usr/bin/env python3
"""
Simple Healthcare AI Chat - Clean Interface
==========================================

A clean, simple interface for the healthcare AI with minimal output.
"""

import asyncio
import re
import logging

# Disable verbose logging
logging.getLogger().setLevel(logging.ERROR)

class SimpleHealthcareAI:
    """Simple healthcare AI with clean responses"""
    
    def __init__(self):
        pass
    
    def _check_medical_advice(self, message: str) -> bool:
        """Check if message requests medical advice"""
        patterns = [
            r'\b(what do i have|diagnose|diagnosis)\b',
            r'\b(what medication|prescribe|prescription)\b', 
            r'\b(what treatment|how to treat|cure)\b',
            r'\b(am i sick|do i have cancer|what\'s wrong)\b',
            r'\b(should i take|how much should i take)\b'
        ]
        return any(re.search(p, message.lower()) for p in patterns)
    
    def _check_prompt_injection(self, message: str) -> bool:
        """Check for prompt injection"""
        patterns = [
            r'\b(ignore previous|forget everything|override|bypass)\b',
            r'\b(you are now|pretend you are|act like)\b',
            r'\b(system message|show.*prompt|reveal)\b'
        ]
        return any(re.search(p, message.lower()) for p in patterns)
    
    def _check_privacy_violation(self, message: str) -> bool:
        """Check for personal information"""
        patterns = [
            r'\b(my name is|ssn|social security)\b',
            r'\b(phone number|address|email)\b',
            r'\b(patient id|medical record)\b'
        ]
        return any(re.search(p, message.lower()) for p in patterns)
    
    def _check_self_harm(self, message: str) -> bool:
        """Check for self-harm content"""
        patterns = [
            r'\b(kill myself|suicide|hurt myself)\b',
            r'\b(end it all|don\'t want to live)\b'
        ]
        return any(re.search(p, message.lower()) for p in patterns)
    
    def _get_health_response(self, message: str) -> str:
        """Get appropriate health education response"""
        message_lower = message.lower()
        
        if 'diabetes' in message_lower:
            return "Diabetes is a condition where blood sugar levels are too high. Type 1 occurs when the body doesn't make insulin, Type 2 when the body doesn't use insulin properly. Consult your doctor for personal advice."
        
        elif 'heart' in message_lower or 'cardiovascular' in message_lower:
            return "The heart pumps blood throughout your body. Regular exercise, healthy diet, and not smoking help maintain heart health. See a healthcare provider for specific heart concerns."
        
        elif 'immune system' in message_lower:
            return "The immune system protects your body from infections and diseases using white blood cells, antibodies, and other defenses. Good nutrition, sleep, and exercise support immune function."
        
        elif 'flu' in message_lower or 'influenza' in message_lower:
            return "Flu symptoms include fever, cough, body aches, and fatigue. It's caused by influenza viruses and typically lasts 1-2 weeks. Annual vaccination helps prevent flu."
        
        elif 'exercise' in message_lower:
            return "Regular exercise strengthens your heart, muscles, and bones while improving mental health. Adults should aim for 150 minutes of moderate activity weekly. Start slowly and consult your doctor."
        
        elif 'blood pressure' in message_lower:
            return "Blood pressure measures the force of blood against artery walls. Normal is usually below 120/80. High blood pressure increases heart disease risk. Regular monitoring is important."
        
        elif 'cholesterol' in message_lower:
            return "Cholesterol is a waxy substance in blood. HDL (good) cholesterol protects the heart, LDL (bad) can clog arteries. Diet, exercise, and sometimes medication help manage levels."
        
        elif 'sleep' in message_lower:
            return "Adults typically need 7-9 hours of sleep nightly. Good sleep supports immune function, mental health, and physical recovery. Maintain regular sleep schedules for better rest."
        
        elif 'stress' in message_lower:
            return "Chronic stress can affect physical and mental health, increasing risk of various conditions. Exercise, relaxation techniques, and social support help manage stress effectively."
        
        elif 'nutrition' in message_lower or 'diet' in message_lower:
            return "A balanced diet includes fruits, vegetables, whole grains, lean proteins, and healthy fats. Limit processed foods, excess sugar, and sodium for optimal health."
        
        else:
            return "I can provide general health information for educational purposes. For specific medical questions, please consult with qualified healthcare professionals."
    
    async def process_message(self, message: str) -> dict:
        """Process message and return response"""
        
        # Check for self-harm (highest priority)
        if self._check_self_harm(message):
            return {
                "blocked": True,
                "response": "🚨 CRISIS SUPPORT: National Suicide Prevention Lifeline: 988 | Crisis Text Line: Text HOME to 741741 | Emergency: 911"
            }
        
        # Check for prompt injection
        if self._check_prompt_injection(message):
            return {
                "blocked": True, 
                "response": "🔒 SECURITY: I cannot modify my behavior or bypass safety guidelines. Please ask legitimate health questions."
            }
        
        # Check for privacy violations
        if self._check_privacy_violation(message):
            return {
                "blocked": True,
                "response": "🛡️ PRIVACY: I cannot process personal information. Please ask general health questions without sharing personal details."
            }
        
        # Check for medical advice requests
        if self._check_medical_advice(message):
            return {
                "blocked": True,
                "response": "⚕️ MEDICAL SAFETY: I cannot diagnose, prescribe, or provide medical advice. Please consult a healthcare professional."
            }
        
        # Provide health education
        return {
            "blocked": False,
            "response": self._get_health_response(message)
        }

async def main():
    """Main chat loop"""
    ai = SimpleHealthcareAI()
    
    print("🏥 Healthcare AI - Simple Chat")
    print("=" * 40)
    print("Ask health questions or type 'quit' to exit")
    print("-" * 40)
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            result = await ai.process_message(user_input)
            
            if result['blocked']:
                print(f"🚫 BLOCKED: {result['response']}")
            else:
                print(f"✅ AI: {result['response']}")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())