"""
Test script to verify Anthropic API integration
"""

import os
import asyncio
import logging
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

async def test_anthropic():
    """Test Anthropic API directly"""
    
    logger.info("=" * 60)
    logger.info("TESTING ANTHROPIC API INTEGRATION")
    logger.info("=" * 60)
    
    # Check environment
    logger.info(f"SPOON_LLM_PROVIDER: {os.getenv('SPOON_LLM_PROVIDER', 'not set')}")
    logger.info(f"ANTHROPIC_API_KEY: {'set' if os.getenv('ANTHROPIC_API_KEY') else 'NOT SET'}")
    
    # Test SpoonOS LLMManager
    try:
        from spoon_ai.llm import LLMManager
        from spoon_ai.chat import ChatBot
        
        logger.info("\n1. Testing LLMManager initialization...")
        llm_manager = LLMManager()
        logger.info(f"✅ LLMManager initialized")
        logger.info(f"   Default provider: {llm_manager.default_provider}")
        
        logger.info("\n2. Testing ChatBot initialization...")
        chatbot = ChatBot(llm_manager=llm_manager)
        logger.info(f"✅ ChatBot initialized")
        
        logger.info("\n3. Making test API call to Anthropic...")
        
        # Check available methods
        logger.info(f"   LLMManager methods: {[m for m in dir(llm_manager) if not m.startswith('_')]}")
        
        # Import Message class
        from spoon_ai.schema import Message, Role
        
        # Create proper Message objects
        messages = [
            Message(role=Role.SYSTEM, content="You are a helpful assistant. Respond concisely."),
            Message(role=Role.USER, content="Say 'Hello from Anthropic API!' in exactly 5 words.")
        ]
        
        response = await llm_manager.chat(
            messages=messages,
            provider="anthropic",
            max_tokens=1000  # Set reasonable limit
        )
        
        logger.info(f"✅ API CALL SUCCESSFUL!")
        logger.info(f"   Response: {response}")
        logger.info("\n🎉 Anthropic integration is working! Check your console at https://console.anthropic.com")
        
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        logger.error(f"   Type: {type(e).__name__}")
        import traceback
        logger.error(traceback.format_exc())
        
        # Additional debugging
        logger.info("\n📋 Debugging info:")
        logger.info(f"   Python path: {os.sys.executable}")
        logger.info(f"   Working dir: {os.getcwd()}")
        
        # Try to import anthropic directly
        try:
            import anthropic
            logger.info(f"   anthropic module found: {anthropic.__version__}")
        except ImportError:
            logger.error("   anthropic module NOT found - run: pip install anthropic")

if __name__ == "__main__":
    asyncio.run(test_anthropic())
