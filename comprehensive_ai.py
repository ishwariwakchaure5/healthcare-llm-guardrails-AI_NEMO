#!/usr/bin/env python3
"""
Comprehensive Healthcare AI - Extensive Medical Knowledge
========================================================

A comprehensive healthcare AI with extensive medical dataset that analyzes
every word in the query to provide accurate health information.
"""

import asyncio
import re
import logging
from typing import Dict, List, Set

# Disable verbose logging
logging.getLogger().setLevel(logging.ERROR)

class ComprehensiveHealthcareAI:
    """Comprehensive healthcare AI with extensive medical knowledge"""
    
    def __init__(self):
        self.medical_database = self._build_comprehensive_database()
        self.stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'must'}
    
    def _build_comprehensive_database(self) -> Dict:
        """Build extensive medical knowledge database"""
        return {
            # ANATOMY & BODY SYSTEMS
            'anatomy': {
                'heart': 'muscular organ that pumps blood throughout the body via the circulatory system',
                'lungs': 'respiratory organs that facilitate gas exchange, taking in oxygen and expelling carbon dioxide',
                'liver': 'largest internal organ that processes nutrients, filters toxins, and produces bile',
                'kidneys': 'bean-shaped organs that filter waste products and excess water from blood to form urine',
                'brain': 'central organ of the nervous system that controls thoughts, memory, emotion, and body functions',
                'stomach': 'digestive organ that breaks down food using acid and enzymes',
                'intestines': 'long tube-like organs that absorb nutrients and water from digested food',
                'pancreas': 'organ that produces insulin and digestive enzymes',
                'spleen': 'organ that filters blood and helps fight infections',
                'gallbladder': 'small organ that stores bile produced by the liver',
                'thyroid': 'butterfly-shaped gland that regulates metabolism through hormone production',
                'adrenals': 'glands that produce hormones including adrenaline and cortisol',
                'bones': 'hard tissues that form the skeleton, providing structure and protecting organs',
                'muscles': 'tissues that contract to produce movement and maintain posture',
                'skin': 'largest organ that protects the body from external environment',
                'blood': 'fluid that carries oxygen, nutrients, and waste products throughout the body',
                'nerves': 'fibers that transmit electrical signals between brain and body parts',
                'joints': 'connections between bones that allow movement',
                'cartilage': 'flexible tissue that cushions joints and supports structures',
                'tendons': 'fibrous tissues that connect muscles to bones',
                'ligaments': 'tissues that connect bones to other bones',
                'arteries': 'blood vessels that carry oxygenated blood away from the heart',
                'veins': 'blood vessels that return deoxygenated blood to the heart',
                'capillaries': 'smallest blood vessels where gas and nutrient exchange occurs'
            },
            
            # DISEASES & CONDITIONS
            'diseases': {
                'diabetes': 'chronic condition where blood glucose levels are too high due to insulin problems',
                'hypertension': 'condition where blood pressure is consistently elevated, straining cardiovascular system',
                'asthma': 'respiratory condition causing airways to narrow, swell, and produce extra mucus',
                'arthritis': 'inflammation of joints causing pain, stiffness, and reduced range of motion',
                'cancer': 'group of diseases involving abnormal cell growth with potential to invade other tissues',
                'pneumonia': 'infection that inflames air sacs in lungs, which may fill with fluid or pus',
                'bronchitis': 'inflammation of bronchial tubes that carry air to lungs',
                'influenza': 'viral infection that attacks respiratory system including nose, throat, and lungs',
                'tuberculosis': 'bacterial infection that primarily affects lungs but can spread to other organs',
                'hepatitis': 'inflammation of liver tissue, often caused by viral infections',
                'cirrhosis': 'scarring of liver tissue that impairs liver function',
                'nephritis': 'inflammation of kidneys that can affect their filtering ability',
                'gastritis': 'inflammation of stomach lining causing pain and digestive issues',
                'colitis': 'inflammation of colon causing abdominal pain and diarrhea',
                'dermatitis': 'inflammation of skin causing redness, swelling, and itching',
                'conjunctivitis': 'inflammation of thin membrane covering eye and inner eyelid',
                'sinusitis': 'inflammation of sinuses causing congestion and facial pain',
                'tonsillitis': 'inflammation of tonsils causing sore throat and difficulty swallowing',
                'appendicitis': 'inflammation of appendix requiring immediate medical attention',
                'meningitis': 'inflammation of membranes surrounding brain and spinal cord',
                'encephalitis': 'inflammation of brain tissue, often caused by viral infections',
                'osteoporosis': 'condition where bones become weak and brittle',
                'osteoarthritis': 'degenerative joint disease causing cartilage breakdown',
                'rheumatoid': 'autoimmune condition causing joint inflammation and damage',
                'fibromyalgia': 'disorder causing widespread musculoskeletal pain and fatigue',
                'migraine': 'severe headache often accompanied by nausea and light sensitivity',
                'epilepsy': 'neurological disorder causing recurrent seizures',
                'alzheimer': 'progressive brain disorder causing memory loss and cognitive decline',
                'parkinson': 'neurodegenerative disorder affecting movement and coordination',
                'depression': 'mental health condition causing persistent sadness and loss of interest',
                'anxiety': 'mental health condition causing excessive worry and fear',
                'schizophrenia': 'mental disorder affecting thinking, perception, and behavior',
                'bipolar': 'mental health condition causing extreme mood swings',
                'anemia': 'condition where blood lacks enough healthy red blood cells',
                'leukemia': 'cancer of blood-forming tissues including bone marrow',
                'lymphoma': 'cancer that begins in lymphatic system',
                'melanoma': 'serious form of skin cancer developing in melanocytes',
                'stroke': 'interruption of blood supply to brain causing cell death',
                'embolism': 'blockage of blood vessel by blood clot or other substance',
                'thrombosis': 'formation of blood clot inside blood vessel',
                'atherosclerosis': 'buildup of plaque in arteries causing narrowing',
                'arrhythmia': 'irregular heartbeat that can be too fast, slow, or erratic',
                'cardiomyopathy': 'disease of heart muscle affecting its ability to pump blood',
                'endocarditis': 'inflammation of inner lining of heart chambers and valves',
                'pericarditis': 'inflammation of membrane surrounding heart'
            },
            
            # SYMPTOMS
            'symptoms': {
                'fever': 'elevated body temperature above normal range, indicating immune response to infection',
                'headache': 'pain in head or neck region, ranging from mild to severe intensity',
                'cough': 'sudden expulsion of air from lungs to clear airways of irritants or mucus',
                'fatigue': 'extreme tiredness and lack of energy affecting daily activities',
                'nausea': 'feeling of sickness with urge to vomit, often preceding actual vomiting',
                'vomiting': 'forceful expulsion of stomach contents through mouth',
                'diarrhea': 'loose, watery bowel movements occurring more frequently than normal',
                'constipation': 'difficulty passing stools or infrequent bowel movements',
                'dizziness': 'feeling of unsteadiness, lightheadedness, or spinning sensation',
                'vertigo': 'sensation of spinning or moving when actually stationary',
                'syncope': 'temporary loss of consciousness due to insufficient blood flow to brain',
                'dyspnea': 'difficulty breathing or shortness of breath',
                'tachycardia': 'rapid heart rate exceeding normal resting rate',
                'bradycardia': 'slow heart rate below normal resting rate',
                'palpitations': 'awareness of heartbeat, often feeling irregular or forceful',
                'chest pain': 'discomfort in chest area that may indicate various conditions',
                'abdominal pain': 'discomfort in stomach area with various possible causes',
                'back pain': 'discomfort in back region affecting mobility and comfort',
                'joint pain': 'discomfort in areas where bones meet, often with stiffness',
                'muscle pain': 'discomfort in muscle tissue, often from strain or inflammation',
                'numbness': 'loss of sensation in body part, often indicating nerve issues',
                'tingling': 'prickling sensation often described as pins and needles',
                'weakness': 'reduced strength in muscles affecting normal function',
                'paralysis': 'loss of muscle function in part of body',
                'tremor': 'involuntary shaking movement of body parts',
                'seizure': 'sudden electrical disturbance in brain causing various symptoms',
                'confusion': 'state of mental uncertainty or lack of clear thinking',
                'memory loss': 'inability to recall information or past events',
                'hallucination': 'perception of something not actually present',
                'delusion': 'false belief held despite evidence to contrary',
                'insomnia': 'difficulty falling asleep or staying asleep',
                'hypersomnia': 'excessive sleepiness during normal waking hours',
                'appetite loss': 'reduced desire to eat food',
                'weight loss': 'reduction in body weight, may be intentional or concerning',
                'weight gain': 'increase in body weight beyond normal range',
                'swelling': 'enlargement of body part due to fluid accumulation',
                'inflammation': 'body response to injury or infection causing redness and swelling',
                'rash': 'change in skin color, texture, or appearance',
                'itching': 'uncomfortable sensation causing desire to scratch',
                'bleeding': 'loss of blood from circulatory system',
                'bruising': 'discoloration of skin due to blood vessel damage',
                'jaundice': 'yellowing of skin and eyes due to liver problems',
                'cyanosis': 'bluish discoloration of skin due to oxygen deficiency'
            },
            
            # TREATMENTS & PROCEDURES
            'treatments': {
                'medication': 'substances used to treat, cure, prevent, or diagnose diseases',
                'surgery': 'medical procedure involving incision to repair or remove tissue',
                'therapy': 'treatment approach to address medical or psychological conditions',
                'rehabilitation': 'process of restoring function after injury or illness',
                'vaccination': 'administration of vaccine to stimulate immune response',
                'immunization': 'process of making person immune to infectious disease',
                'antibiotics': 'medications that fight bacterial infections',
                'antivirals': 'medications that treat viral infections',
                'analgesics': 'pain-relieving medications',
                'anti-inflammatory': 'medications that reduce inflammation',
                'chemotherapy': 'treatment using chemicals to destroy cancer cells',
                'radiation': 'high-energy treatment used to destroy cancer cells',
                'dialysis': 'procedure to filter waste from blood when kidneys fail',
                'transplant': 'surgical procedure to replace diseased organ with healthy one',
                'biopsy': 'removal of tissue sample for examination',
                'endoscopy': 'procedure using flexible tube to examine internal organs',
                'laparoscopy': 'minimally invasive surgery using small incisions',
                'anesthesia': 'medication to prevent pain during medical procedures',
                'physiotherapy': 'treatment using physical methods to restore movement',
                'occupational therapy': 'treatment to help perform daily activities',
                'psychotherapy': 'treatment for mental health conditions through talking',
                'acupuncture': 'traditional treatment using thin needles at specific points',
                'massage': 'manipulation of soft tissues for therapeutic purposes',
                'exercise': 'physical activity to improve health and fitness'
            },
            
            # MEDICAL SPECIALTIES
            'specialties': {
                'cardiology': 'medical specialty dealing with heart and blood vessel disorders',
                'neurology': 'medical specialty focusing on nervous system disorders',
                'oncology': 'medical specialty dealing with cancer diagnosis and treatment',
                'pediatrics': 'medical specialty focusing on infants, children, and adolescents',
                'geriatrics': 'medical specialty focusing on elderly patient care',
                'psychiatry': 'medical specialty dealing with mental health disorders',
                'dermatology': 'medical specialty focusing on skin, hair, and nail conditions',
                'ophthalmology': 'medical specialty dealing with eye and vision disorders',
                'orthopedics': 'medical specialty focusing on musculoskeletal system',
                'gastroenterology': 'medical specialty dealing with digestive system disorders',
                'pulmonology': 'medical specialty focusing on respiratory system disorders',
                'nephrology': 'medical specialty dealing with kidney disorders',
                'endocrinology': 'medical specialty focusing on hormone-related disorders',
                'rheumatology': 'medical specialty dealing with autoimmune and inflammatory conditions',
                'hematology': 'medical specialty focusing on blood disorders',
                'immunology': 'medical specialty dealing with immune system disorders',
                'infectious disease': 'medical specialty focusing on infections and contagious diseases',
                'emergency medicine': 'medical specialty dealing with acute care and emergencies',
                'anesthesiology': 'medical specialty focusing on pain management and anesthesia',
                'radiology': 'medical specialty using imaging to diagnose and treat diseases',
                'pathology': 'medical specialty studying disease causes and effects',
                'surgery': 'medical specialty involving operative procedures'
            },
            
            # DIAGNOSTIC TESTS
            'diagnostics': {
                'blood test': 'laboratory analysis of blood sample to assess health status',
                'urine test': 'analysis of urine sample to detect various conditions',
                'x-ray': 'imaging technique using electromagnetic radiation to view internal structures',
                'mri': 'magnetic resonance imaging using magnetic fields to create detailed images',
                'ct scan': 'computed tomography creating cross-sectional images of body',
                'ultrasound': 'imaging technique using sound waves to visualize internal structures',
                'ecg': 'electrocardiogram recording electrical activity of heart',
                'eeg': 'electroencephalogram recording electrical activity of brain',
                'colonoscopy': 'examination of colon using flexible tube with camera',
                'mammography': 'x-ray examination of breasts to detect abnormalities',
                'bone scan': 'imaging test to detect bone diseases or injuries',
                'pet scan': 'positron emission tomography showing metabolic activity',
                'stress test': 'evaluation of heart function during physical exertion',
                'spirometry': 'test measuring lung function and breathing capacity',
                'biopsy': 'removal and examination of tissue sample for diagnosis'
            },
            
            # PREVENTION & WELLNESS
            'prevention': {
                'exercise': 'regular physical activity to maintain health and prevent disease',
                'nutrition': 'proper intake of nutrients to support health and prevent illness',
                'hygiene': 'practices to maintain cleanliness and prevent infection',
                'vaccination': 'immunization to prevent infectious diseases',
                'screening': 'testing to detect diseases before symptoms appear',
                'lifestyle': 'daily habits and choices affecting health outcomes',
                'stress management': 'techniques to reduce and cope with stress effectively',
                'sleep hygiene': 'practices to ensure quality sleep for optimal health',
                'weight management': 'maintaining healthy body weight through diet and exercise',
                'smoking cessation': 'quitting tobacco use to improve health outcomes',
                'alcohol moderation': 'limiting alcohol consumption to safe levels',
                'sun protection': 'measures to prevent skin damage from UV radiation',
                'injury prevention': 'safety measures to avoid accidents and trauma',
                'mental health': 'maintaining psychological and emotional well-being'
            }
        }
    
    def _analyze_query_words(self, query: str) -> Dict:
        """Analyze every word in the query against medical database"""
        words = re.findall(r'\b\w+\b', query.lower())
        
        # Remove stop words but keep medical terms
        meaningful_words = []
        for word in words:
            if word not in self.stop_words or len(word) > 3:
                meaningful_words.append(word)
        
        # Find matches in database
        matches = {
            'anatomy': [],
            'diseases': [],
            'symptoms': [],
            'treatments': [],
            'specialties': [],
            'diagnostics': [],
            'prevention': []
        }
        
        # Check if query is actually health-related first
        health_context_score = 0
        health_keywords = ['health', 'medical', 'disease', 'symptom', 'treatment', 'body', 'pain', 'doctor', 'hospital', 'medicine', 'condition', 'illness', 'infection', 'therapy', 'diagnosis']
        
        for word in meaningful_words:
            if word in health_keywords:
                health_context_score += 2
            # Check for direct medical term matches
            for category, items in self.medical_database.items():
                if word in items:
                    health_context_score += 3
        
        # Only proceed with medical matching if there's health context
        if health_context_score < 2:
            return matches, meaningful_words
        
        # Check each word against all categories with better relevance
        for word in meaningful_words:
            for category, items in self.medical_database.items():
                for term, description in items.items():
                    # Exact match (highest priority)
                    if word == term:
                        matches[category].append((term, description))
                    # Word is part of medical term (medium priority)
                    elif word in term and len(word) > 3:
                        matches[category].append((term, description))
                    # Medical term contains the word (lower priority)
                    elif term in word and len(term) > 3:
                        matches[category].append((term, description))
        
        # Remove duplicates and sort by relevance
        for category in matches:
            matches[category] = list(set(matches[category]))
            # Sort by term length (more specific terms first)
            matches[category].sort(key=lambda x: len(x[0]), reverse=True)
        
        return matches, meaningful_words
    
    def _check_medical_advice(self, message: str) -> bool:
        """Check if message requests medical advice"""
        advice_patterns = [
            r'\b(what do i have|diagnose me|what\'s wrong with me|am i sick)\b',
            r'\b(what medication|prescribe|prescription|should i take|how much.*take)\b',
            r'\b(what treatment|how to treat|cure me|fix my|heal my)\b',
            r'\b(do i have|is this|could this be).*\b(cancer|diabetes|disease|condition)\b',
            r'\b(should i see|need to go|visit).*\b(doctor|hospital|clinic)\b',
            r'\b(is it serious|how bad|will i die|am i dying)\b'
        ]
        return any(re.search(p, message.lower()) for p in advice_patterns)
    
    def _check_prompt_injection(self, message: str) -> bool:
        """Check for prompt injection attempts"""
        injection_patterns = [
            r'\b(ignore|forget|override|bypass|disable).*\b(previous|instructions|rules|safety|guidelines)\b',
            r'\b(you are now|pretend|act like|roleplay as|become).*\b(doctor|physician|medical)\b',
            r'\b(system|show|reveal|display).*\b(prompt|instructions|configuration|rules)\b',
            r'\b(developer|administrator|creator|owner|manager).*\b(override|bypass|disable|change)\b',
            r'\b(jailbreak|unrestricted|unlimited|no limits|no restrictions)\b'
        ]
        return any(re.search(p, message.lower()) for p in injection_patterns)
    
    def _check_privacy_violation(self, message: str) -> bool:
        """Check for personal information sharing"""
        privacy_patterns = [
            r'\b(my name is|i am|call me|i\'m).*\b[A-Z][a-z]+\b',
            r'\b(ssn|social security|insurance).*\b\d+\b',
            r'\b(phone|telephone).*\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            r'\b(address|live at).*\b\d+.*\b(street|st|avenue|ave|road|rd)\b',
            r'\b(email|e-mail).*\b\w+@\w+\.\w+\b',
            r'\b(patient.*id|medical.*record|chart.*number).*\b\w+\d+\b',
            r'\b(born on|date.*birth|dob).*\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b'
        ]
        return any(re.search(p, message.lower()) for p in privacy_patterns)
    
    def _check_self_harm(self, message: str) -> bool:
        """Check for self-harm or crisis content"""
        crisis_patterns = [
            r'\b(kill myself|suicide|end my life|hurt myself|harm myself)\b',
            r'\b(want to die|end it all|don\'t want.*live|can\'t go on)\b',
            r'\b(overdose|lethal dose|how.*die|ways.*die)\b',
            r'\b(cutting|self.*harm|self.*injury|self.*mutilation)\b'
        ]
        return any(re.search(p, message.lower()) for p in crisis_patterns)
    
    def _generate_comprehensive_response(self, matches: Dict, query_words: List) -> str:
        """Generate comprehensive response based on matched terms"""
        response_parts = []
        
        # Process matches by priority
        categories_order = ['diseases', 'symptoms', 'anatomy', 'treatments', 'diagnostics', 'prevention', 'specialties']
        
        for category in categories_order:
            if matches[category]:
                # Take top 2 most relevant matches
                for term, description in matches[category][:2]:
                    response_parts.append(f"{term.title()}: {description}")
        
        if response_parts:
            response = ". ".join(response_parts)
            # Add medical disclaimer
            response += ". This information is for educational purposes only. Always consult healthcare professionals for medical advice."
            return response
        
        # If no specific matches, provide general guidance based on query type
        query_lower = " ".join(query_words)
        
        if any(word in query_lower for word in ['what', 'explain', 'tell', 'describe', 'define']):
            return "This appears to be a request for medical information. While I can provide general health education, please consult medical professionals or authoritative medical sources for detailed information about specific health topics."
        
        if any(word in query_lower for word in ['how', 'why', 'when', 'where']):
            return "Medical questions about mechanisms, causes, timing, or locations of health issues require professional medical knowledge. Please consult healthcare providers for accurate information about your specific situation."
        
        if any(word in query_lower for word in ['prevent', 'avoid', 'reduce', 'lower', 'decrease']):
            return "Prevention strategies vary by condition and individual factors. General approaches include healthy lifestyle choices, regular medical checkups, and following medical guidelines. Consult healthcare professionals for personalized prevention advice."
        
        return "I can provide general health information for educational purposes. For specific medical questions, detailed information, or personal health concerns, please consult qualified healthcare professionals or authoritative medical resources."
    
    async def process_message(self, message: str) -> dict:
        """Process message with comprehensive analysis"""
        
        # Check for self-harm (highest priority)
        if self._check_self_harm(message):
            return {
                "blocked": True,
                "response": "🚨 CRISIS SUPPORT: National Suicide Prevention Lifeline: 988 | Crisis Text Line: Text HOME to 741741 | Emergency: 911 | You're not alone - help is available."
            }
        
        # Check for prompt injection
        if self._check_prompt_injection(message):
            return {
                "blocked": True,
                "response": "🔒 SECURITY: I cannot modify my behavior or bypass safety guidelines. Please ask legitimate health questions for educational information."
            }
        
        # Check for privacy violations
        if self._check_privacy_violation(message):
            return {
                "blocked": True,
                "response": "🛡️ PRIVACY: I cannot process personal information. Please ask general health questions without sharing personal details like names, addresses, or medical records."
            }
        
        # Check for medical advice requests
        if self._check_medical_advice(message):
            return {
                "blocked": True,
                "response": "⚕️ MEDICAL SAFETY: I cannot diagnose conditions, prescribe medications, or provide specific medical advice. Please consult qualified healthcare professionals for medical concerns."
            }
        
        # Analyze query comprehensively
        matches, query_words = self._analyze_query_words(message)
        
        # Check if any medical terms were found
        total_matches = sum(len(category_matches) for category_matches in matches.values())
        
        # Check if query is actually health-related
        query_lower = message.lower()
        non_health_indicators = ['mosquito', 'insect', 'pest', 'bug', 'animal', 'plant', 'food', 'cooking', 'recipe', 'weather', 'sports', 'technology', 'computer', 'car', 'house', 'money', 'business']
        
        if any(indicator in query_lower for indicator in non_health_indicators):
            return {
                "blocked": False,
                "response": "I'm designed specifically for health and medical topics. For non-medical questions, please consult appropriate resources or ask health-related questions instead."
            }
        
        if total_matches == 0:
            return {
                "blocked": False,
                "response": "I'm designed to discuss health and medical topics. Please ask questions about health conditions, symptoms, body systems, treatments, or general wellness information."
            }
        
        # Generate comprehensive response
        response = self._generate_comprehensive_response(matches, query_words)
        
        return {
            "blocked": False,
            "response": response
        }

async def main():
    """Main chat loop"""
    ai = ComprehensiveHealthcareAI()
    
    print("🏥 Comprehensive Healthcare AI")
    print("=" * 50)
    print("Advanced medical knowledge system analyzing every word")
    print("Ask any health question - I have extensive medical data")
    print("Type 'quit' to exit")
    print("-" * 50)
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                print("👋 Goodbye! Stay healthy and consult healthcare professionals when needed!")
                break
            
            if not user_input:
                continue
            
            result = await ai.process_message(user_input)
            
            if result['blocked']:
                print(f"🚫 BLOCKED: {result['response']}")
            else:
                print(f"✅ AI: {result['response']}")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye! Stay healthy!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())