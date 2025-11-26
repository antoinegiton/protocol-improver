# analyzer.py - Core protocol analysis using Claude API

from anthropic import Anthropic
from typing import List, Dict, Any
import json
from config import settings

class ProtocolAnalyzer:
    """Analyze laboratory protocols and suggest improvements using Claude AI"""
    
    def __init__(self):
        """Initialize the analyzer with Claude API client"""
        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = settings.ANTHROPIC_MODEL
        
    def analyze_protocol(self, protocol_text: str, filename: str = "") -> Dict[str, Any]:
        """
        Analyze a protocol and return structured improvement suggestions
        
        Args:
            protocol_text: The full text of the protocol
            filename: Optional filename for reference
            
        Returns:
            Dictionary containing analysis results and suggestions
        """
        
        # Create the analysis prompt
        prompt = self._create_analysis_prompt(protocol_text, filename)
        
        try:
            # Call Claude API
            response = self.client.messages.create(
                model=self.model,
                max_tokens=settings.MAX_TOKENS,
                temperature=settings.TEMPERATURE,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            # Extract the response text
            response_text = response.content[0].text
            
            # Parse the structured response
            analysis_result = self._parse_analysis_response(response_text)
            
            # Add metadata
            analysis_result['metadata'] = {
                'filename': filename,
                'model_used': self.model,
                'protocol_length': len(protocol_text),
                'tokens_used': response.usage.input_tokens + response.usage.output_tokens
            }
            
            return analysis_result
            
        except Exception as e:
            return {
                'error': True,
                'message': f"Analysis failed: {str(e)}",
                'suggestions': []
            }
    
    def _create_analysis_prompt(self, protocol_text: str, filename: str = "") -> str:
        """Create the prompt for Claude to analyze the protocol"""
        
        prompt = f"""You are an expert laboratory protocol reviewer. Analyze the following laboratory protocol and identify specific improvements.

{"Protocol File: " + filename if filename else ""}

For each issue you find, provide:
1. The category (safety, clarity, completeness, formatting, or best_practices)
2. The priority level (HIGH, MEDIUM, or LOW)
3. The specific location (step number or section)
4. A clear description of the issue
5. A specific, actionable suggestion for improvement

Focus on:
- **Safety Issues**: Missing warnings, hazard information, PPE requirements
- **Clarity Issues**: Ambiguous instructions, unclear measurements, vague timing
- **Completeness Issues**: Missing materials, equipment, concentrations, temperatures
- **Formatting Issues**: Poor structure, inconsistent numbering, hard to follow
- **Best Practices**: Industry standards, optimization opportunities, quality controls

Return your analysis in this exact JSON format:
{{
    "summary": "Brief overview of the protocol and overall assessment",
    "overall_score": "A score from 1-10",
    "total_issues": "Total number of issues found",
    "suggestions": [
        {{
            "category": "safety|clarity|completeness|formatting|best_practices",
            "priority": "HIGH|MEDIUM|LOW",
            "location": "Step 3" or "Materials section" etc,
            "issue": "Clear description of what's wrong",
            "suggestion": "Specific recommendation to fix it",
            "example": "Optional: How it should look after the fix"
        }}
    ]
}}

Protocol to analyze:

{protocol_text}

Provide your analysis in valid JSON format only, with no additional text before or after."""

        return prompt
    
    def _parse_analysis_response(self, response_text: str) -> Dict[str, Any]:
        """Parse Claude's response into structured format"""
        
        try:
            # Try to find JSON in the response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                json_text = response_text[json_start:json_end]
                analysis = json.loads(json_text)
                
                # Ensure required fields exist
                if 'suggestions' not in analysis:
                    analysis['suggestions'] = []
                if 'summary' not in analysis:
                    analysis['summary'] = 'Analysis completed'
                if 'total_issues' not in analysis:
                    analysis['total_issues'] = len(analysis['suggestions'])
                
                # Sort suggestions by priority
                priority_order = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}
                analysis['suggestions'].sort(
                    key=lambda x: priority_order.get(x.get('priority', 'LOW'), 3)
                )
                
                return analysis
            else:
                # If JSON parsing fails, return a basic structure
                return {
                    'summary': 'Analysis completed but response format was unexpected',
                    'suggestions': [],
                    'total_issues': 0,
                    'raw_response': response_text
                }
                
        except json.JSONDecodeError as e:
            return {
                'error': True,
                'message': f'Could not parse analysis response: {str(e)}',
                'suggestions': [],
                'raw_response': response_text
            }
    
    def generate_improved_protocol(self, 
                                   original_text: str, 
                                   accepted_suggestions: List[Dict]) -> str:
        """
        Generate an improved version of the protocol with accepted suggestions
        
        Args:
            original_text: Original protocol text
            accepted_suggestions: List of suggestions that user accepted
            
        Returns:
            Improved protocol text
        """
        
        if not accepted_suggestions:
            return original_text
        
        # Create prompt for improvement
        suggestions_text = "\n".join([
            f"- {s['location']}: {s['suggestion']}"
            for s in accepted_suggestions
        ])
        
        prompt = f"""You are a laboratory protocol editor. Please rewrite this protocol incorporating the following improvements:

{suggestions_text}

Maintain the original structure and style, but integrate these improvements naturally. Make the protocol clearer and safer while keeping it professional.

Original Protocol:
{original_text}

Provide the improved protocol below:"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=settings.MAX_TOKENS,
                temperature=0.3,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            improved_text = response.content[0].text
            return improved_text
            
        except Exception as e:
            print(f"Error generating improved protocol: {e}")
            return original_text
    
    def quick_check(self) -> bool:
        """Quick check to verify API connection works"""
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=50,
                messages=[
                    {
                        "role": "user",
                        "content": "Respond with 'OK' if you can read this."
                    }
                ]
            )
            return True
        except Exception as e:
            print(f"API connection failed: {e}")
            return False


# Test function
if __name__ == "__main__":
    print("Testing ProtocolAnalyzer...")
    
    analyzer = ProtocolAnalyzer()
    
    # Quick API check
    if analyzer.quick_check():
        print("✅ Claude API connection working")
    else:
        print("❌ Claude API connection failed")
    
    # Test with sample protocol
    sample_protocol = """
    PCR Amplification Protocol
    
    Materials:
    - DNA template
    - Primers
    - Taq polymerase
    - Buffer
    
    Steps:
    1. Mix all reagents
    2. Put in thermocycler
    3. Run program
    4. Check results
    """
    
    print("\nAnalyzing sample protocol...")
    result = analyzer.analyze_protocol(sample_protocol, "sample_pcr.txt")
    
    if 'error' not in result:
        print(f"✅ Found {result.get('total_issues', 0)} issues")
        print(f"Summary: {result.get('summary', 'N/A')}")
        if result.get('suggestions'):
            print(f"First suggestion: {result['suggestions'][0]['issue']}")
    else:
        print(f"❌ Analysis failed: {result.get('message', 'Unknown error')}")
