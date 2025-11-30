"""
Custom runner configuration for the study guide agent.

This file configures the ADK Runner with memory service support.
Use this when you want to run the agent with custom configuration.

For local development:
    python -m study_guide_agent.runner

For production with memory bank:
    Set AGENT_ENGINE_ID environment variable before running
"""

import os
from google.adk import Runner
from google.adk.memory import VertexAiMemoryBankService, InMemoryMemoryService
from .agent import root_agent


def create_runner_with_memory():
    """Create a Runner with memory service configured

    Returns:
        Runner instance with appropriate memory service
    """
    # Check if we're in a deployed environment with Agent Engine
    agent_engine_id = os.getenv("AGENT_ENGINE_ID")
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION")

    memory_service = None

    if agent_engine_id and project_id and location:
        # Production: Use Vertex AI Memory Bank
        try:
            memory_service = VertexAiMemoryBankService(
                project=project_id,
                location=location,
                agent_engine_id=agent_engine_id
            )
            print(f"✅ Using Vertex AI Memory Bank (Agent Engine ID: {agent_engine_id})")
        except Exception as e:
            print(f"⚠️ Failed to create Vertex AI Memory Bank: {e}")
            print("⚠️ Falling back to in-memory storage")
            memory_service = InMemoryMemoryService()
    else:
        # Local development: Use in-memory storage
        memory_service = InMemoryMemoryService()
        print("✅ Using in-memory storage (data will not persist between sessions)")

    # Create the runner with memory service
    runner = Runner(
        agent=root_agent,
        memory_service=memory_service
    )

    return runner


# Create the default runner instance
runner = create_runner_with_memory()


if __name__ == "__main__":
    # Run the agent interactively
    import asyncio

    async def main():
        session = runner.start_session(user_id="local_user")

        print("\n" + "="*60)
        print("Study Guide Agent - Interactive Mode")
        print("="*60)
        print("\nType your request (or 'quit' to exit)")

        while True:
            user_input = input("\n> ")

            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break

            if not user_input.strip():
                continue

            print("\n" + "-"*60)

            async for event in runner.run(
                session=session,
                message=user_input
            ):
                if hasattr(event, 'text'):
                    print(event.text, end='', flush=True)

            print("\n" + "-"*60)

    asyncio.run(main())
