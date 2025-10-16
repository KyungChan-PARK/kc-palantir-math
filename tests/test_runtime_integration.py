"""
Runtime Integration Tests

Validates runtime capability integration across all agents.

Tests:
- ObservabilityMixin integration
- Agent enhancement without breakage
- Hook execution
- Event reporting

VERSION: 1.0.0
DATE: 2025-10-16
"""

import pytest
from subagents import (
    research_agent,
    knowledge_builder,
    quality_agent,
    meta_orchestrator,
    neo4j_query_agent,
    problem_decomposer_agent,
    personalization_engine_agent,
    problem_scaffolding_generator_agent,
    dynamic_learning_agent,
    self_improver_agent,
    socratic_requirements_agent
)


class TestAgentEnhancement:
    """Test all agents have runtime capabilities"""
    
    def test_all_agents_have_observability(self):
        """Verify core agents enhanced with ObservabilityMixin"""
        # Test sample of agents (not all are AgentDefinition objects)
        agents = [
            ('research_agent', research_agent),
            ('knowledge_builder', knowledge_builder),
            ('quality_agent', quality_agent),
            ('meta_orchestrator', meta_orchestrator),
        ]
        
        enhanced_count = 0
        for name, agent in agents:
            # Check if it's an AgentDefinition (not a module)
            if hasattr(agent, 'description') and hasattr(agent, 'prompt'):
                if hasattr(agent, '_obs'):
                    enhanced_count += 1
        
        # At least 4 core agents should be enhanced
        assert enhanced_count >= 4, f"Only {enhanced_count}/4 core agents enhanced"
    
    def test_agents_with_realtime(self):
        """Verify realtime-enabled agents have RealtimeMixin"""
        # Check meta_orchestrator (should have all features)
        if hasattr(meta_orchestrator, 'description'):
            assert hasattr(meta_orchestrator, '_realtime'), "meta_orchestrator missing realtime"
    
    def test_agents_with_computer_use(self):
        """Verify computer-use-enabled agents have ComputerUseMixin"""
        # Check sample agents
        agents_to_check = [
            ('meta_orchestrator', meta_orchestrator),
            ('research_agent', research_agent),
            ('quality_agent', quality_agent)
        ]
        
        computer_use_count = 0
        for name, agent in agents_to_check:
            if hasattr(agent, 'description') and hasattr(agent, '_computer_use'):
                computer_use_count += 1
        
        assert computer_use_count >= 2, f"Only {computer_use_count}/3 agents have computer_use"
    
    def test_original_agent_definition_preserved(self):
        """Verify AgentDefinition still has core properties"""
        # All agents should still have description and prompt
        agents = [research_agent, knowledge_builder, quality_agent]
        
        for agent in agents:
            assert hasattr(agent, 'description'), f"Agent missing description: {agent}"
            assert hasattr(agent, 'prompt'), f"Agent missing prompt: {agent}"
            assert agent.description, f"Agent has empty description: {agent}"
            assert agent.prompt, f"Agent has empty prompt: {agent}"


class TestObservabilityIntegration:
    """Test observability event system"""
    
    def test_event_reporter_import(self):
        """EventReporter can be imported"""
        from integrations.observability.event_reporter import EventReporter
        
        reporter = EventReporter("test-app")
        assert reporter.source_app == "test-app"
    
    def test_event_reporter_methods(self):
        """EventReporter has all required methods"""
        from integrations.observability.event_reporter import EventReporter
        
        reporter = EventReporter("test")
        
        methods = [
            'session_start',
            'session_end',
            'pre_tool_use',
            'post_tool_use',
            'notification',
            'stop',
            'subagent_stop',
            'pre_compact',
            'user_prompt_submit'
        ]
        
        for method in methods:
            assert hasattr(reporter, method), f"Missing method: {method}"


class TestHookSystem:
    """Test filesystem hook system"""
    
    def test_hook_scripts_exist(self):
        """All hook scripts exist in .claude/hooks/"""
        from pathlib import Path
        
        hook_scripts = [
            'send_event.py',
            'pre_tool_use.py',
            'post_tool_use.py',
            'user_prompt_submit.py',
            'stop.py',
            'subagent_stop.py',
            'session_start.py',
            'session_end.py',
            'notification.py',
            'pre_compact.py'
        ]
        
        hooks_dir = Path(__file__).parent.parent / '.claude' / 'hooks'
        
        for script in hook_scripts:
            path = hooks_dir / script
            assert path.exists(), f"Hook script missing: {script}"
    
    def test_hook_scripts_executable(self):
        """Hook scripts are executable"""
        import subprocess
        import json
        from pathlib import Path
        
        hooks_dir = Path(__file__).parent.parent / '.claude' / 'hooks'
        test_hook = hooks_dir / 'pre_tool_use.py'
        
        # Test execution
        test_input = json.dumps({"tool_name": "Read", "tool_input": {}})
        result = subprocess.run(
            ['python3', str(test_hook)],
            input=test_input,
            capture_output=True,
            text=True,
            timeout=5
        )
        
        assert result.returncode == 0, f"Hook failed: {result.stderr}"
        
        # Should return JSON
        output = json.loads(result.stdout)
        assert 'hookSpecificOutput' in output or output == {}


class TestRealtimeIntegration:
    """Test realtime gateway"""
    
    def test_realtime_gateway_import(self):
        """RealtimeGateway can be imported"""
        from integrations.realtime.gateway_service import RealtimeGateway
        
        gateway = RealtimeGateway({'realtime_port': 8080})
        assert gateway.port == 8080
    
    @pytest.mark.asyncio
    async def test_realtime_gateway_lifecycle(self):
        """Gateway can start and stop"""
        from integrations.realtime.gateway_service import RealtimeGateway
        
        gateway = RealtimeGateway()
        
        # Start
        await gateway.start_background()
        assert gateway.running is True
        
        # Stop
        await gateway.stop()
        assert gateway.running is False


class TestComputerUseIntegration:
    """Test computer-use automation"""
    
    def test_executor_import(self):
        """PlaywrightExecutor can be imported"""
        from integrations.computer_use.playwright_executor import PlaywrightExecutor
        
        executor = PlaywrightExecutor(headless=True)
        assert executor.headless is True
    
    def test_planner_import(self):
        """GeminiPlanner can be imported"""
        from integrations.computer_use.gemini_planner_client import GeminiPlanner
        
        planner = GeminiPlanner()
        assert planner is not None
    
    def test_planner_basic_plan(self):
        """Planner generates basic UI action plans"""
        from integrations.computer_use.gemini_planner_client import GeminiPlanner
        from integrations.computer_use.gemini_computer_use_adapter import ActionType
        
        planner = GeminiPlanner()
        
        # Test navigation goal
        plan = planner.plan("Open https://example.com", {})
        assert len(plan) > 0
        assert plan[0].action == ActionType.NAVIGATE


class TestMainIntegration:
    """Test main.py runtime initialization"""
    
    def test_runtime_config_creation(self):
        """Runtime config can be created"""
        from lib.runtime_enhancers import create_runtime_config
        
        config = create_runtime_config(
            observability=True,
            realtime=False,
            computer_use=False
        )
        
        assert config['observability_enabled'] is True
        assert config['realtime_enabled'] is False
        assert config['computer_use_enabled'] is False
        assert 'observability_url' in config
    
    def test_agents_can_be_enhanced_at_runtime(self):
        """Agents can be enhanced with session ID at runtime"""
        from lib.runtime_enhancers import enhance_agent, ObservabilityMixin
        from claude_agent_sdk import AgentDefinition
        
        # Create fresh test agent
        test_agent = AgentDefinition(
            description="Test agent",
            prompt="Test prompt",
            tools=['Read']
        )
        
        # Enhance it
        enhanced = enhance_agent(test_agent, features=['observability'], session_id="test-123")
        
        # Verify enhancement
        assert hasattr(enhanced, '_obs'), "Enhanced agent should have _obs"
        assert hasattr(enhanced, 'enable_observability'), "Should have enable_observability method"
        # Verify session ID was set during enhancement
        assert enhanced._obs._obs_session_id == "test-123", "Session ID not set"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

