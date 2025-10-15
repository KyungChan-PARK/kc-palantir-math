"""
Background Log Optimizer - Async log processing without blocking

Based on:
- Q2-1: Background processing (async worker)
- Q6: Adaptive triggers (>9.5 immediate, 8-9.5 batch)
- claude-code-2-0-deduplicated-final.md async patterns

VERSION: 1.0.0
DATE: 2025-10-15
"""

import asyncio
import time
import json
from typing import Dict, List, Any
from pathlib import Path
from dataclasses import dataclass, asdict


@dataclass
class OptimizationJob:
    """Background optimization job."""
    log_id: str
    log_data: Dict
    effectiveness_score: float
    priority: str  # "immediate" | "batch" | "low"
    queued_at: float


class BackgroundLogOptimizer:
    """
    Optimizes meta-cognitive logs in background without blocking sessions.
    
    Pattern: async task-based background worker
    Based on: async with ClaudeSDKClient + asyncio.create_task
    """
    
    def __init__(self, storage_dir: str = "logs/optimized"):
        self.queue = asyncio.Queue()
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        self.running = False
        self.worker_task = None
        
        # Statistics
        self.stats = {
            "processed": 0,
            "immediate": 0,
            "batch": 0,
            "templates_generated": 0
        }
    
    async def start(self):
        """Start background worker."""
        if not self.running:
            self.running = True
            self.worker_task = asyncio.create_task(self._worker_loop())
    
    async def stop(self):
        """Stop background worker gracefully."""
        self.running = False
        if self.worker_task:
            await self.worker_task
    
    async def queue_log(
        self,
        log_id: str,
        log_data: Dict,
        effectiveness_score: float
    ):
        """
        Queue log for optimization.
        
        Adaptive prioritization (Q6: D):
        - >9.5: Immediate (high value)
        - 8-9.5: Batch (medium value)
        - <8: Skip optimization (keep raw only)
        """
        if effectiveness_score < 8.0:
            # Skip optimization for low quality
            return
        
        priority = "immediate" if effectiveness_score >= 9.5 else "batch"
        
        job = OptimizationJob(
            log_id=log_id,
            log_data=log_data,
            effectiveness_score=effectiveness_score,
            priority=priority,
            queued_at=time.time()
        )
        
        await self.queue.put(job)
    
    async def _worker_loop(self):
        """
        Background worker loop.
        
        Pattern: Continuous async loop (non-blocking)
        """
        while self.running:
            try:
                # Wait for job (timeout to allow graceful shutdown)
                job = await asyncio.wait_for(
                    self.queue.get(),
                    timeout=1.0
                )
                
                # Process based on priority
                if job.priority == "immediate":
                    await self._optimize_immediate(job)
                    self.stats["immediate"] += 1
                else:
                    await self._optimize_batch(job)
                    self.stats["batch"] += 1
                
                self.stats["processed"] += 1
                
            except asyncio.TimeoutError:
                # No jobs, continue waiting
                continue
            except Exception as e:
                print(f"⚠️ Background optimizer error: {e}")
    
    async def _optimize_immediate(self, job: OptimizationJob):
        """
        Immediate optimization for high-quality logs.
        
        Multi-layer optimization (Q2: D):
        1. Compress to key points
        2. Extract patterns
        3. Generate template
        """
        log = job.log_data
        
        # Layer 1: Compression
        compressed = {
            "session_id": log['session_id'],
            "key_decisions": self._extract_key_decisions(log['trace']['decisions']),
            "key_learnings": self._extract_key_learnings(log['trace']['learnings']),
            "key_impacts": self._extract_key_impacts(log['trace']['impacts'])
        }
        
        # Layer 2: Pattern extraction
        patterns = {
            "decision_patterns": self._extract_decision_patterns(compressed['key_decisions']),
            "learning_patterns": self._extract_learning_patterns(compressed['key_learnings'])
        }
        
        # Layer 3: Template generation
        if job.effectiveness_score >= 9.5:
            template = self._generate_template(patterns, log)
            self._save_template(template)
            self.stats["templates_generated"] += 1
        
        # Save optimized version
        output_file = self.storage_dir / f"optimized_{job.log_id}.json"
        with open(output_file, 'w') as f:
            json.dump({
                "original_id": job.log_id,
                "compressed": compressed,
                "patterns": patterns,
                "effectiveness": job.effectiveness_score,
                "optimized_at": time.time()
            }, f, indent=2)
    
    async def _optimize_batch(self, job: OptimizationJob):
        """Batch optimization (less aggressive)."""
        # Simpler processing for medium-quality logs
        compressed = self._compress_to_key_points(job.log_data)
        
        output_file = self.storage_dir / f"batch_{job.log_id}.json"
        with open(output_file, 'w') as f:
            json.dump(compressed, f, indent=2)
    
    def _extract_key_decisions(self, decisions: List[Dict]) -> List[Dict]:
        """Extract high-confidence decisions only."""
        return [
            {
                "decision": d['decision'],
                "reasoning": d['reasoning'],
                "confidence": d['confidence']
            }
            for d in decisions
            if d.get('confidence', 0) >= 0.9
        ]
    
    def _extract_key_learnings(self, learnings: List[Dict]) -> List[Dict]:
        """Extract high-value learnings."""
        return [
            {
                "insight": l['insight'],
                "source": l['source'],
                "confidence": l['confidence']
            }
            for l in learnings
            if l.get('confidence', 0) >= 0.9
        ]
    
    def _extract_key_impacts(self, impacts: List[Dict]) -> List[Dict]:
        """Extract accurate impact predictions."""
        return [
            {
                "change": i['change'],
                "accuracy": i['prediction_accuracy']
            }
            for i in impacts
            if i.get('prediction_accuracy', 0) >= 0.8
        ]
    
    def _extract_decision_patterns(self, decisions: List[Dict]) -> List[str]:
        """Extract reusable decision patterns."""
        patterns = []
        for d in decisions:
            pattern = f"WHEN: {{trigger}} → DO: {d['decision']} (confidence: {d['confidence']})"
            patterns.append(pattern)
        return patterns
    
    def _extract_learning_patterns(self, learnings: List[Dict]) -> List[str]:
        """Extract reusable learning patterns."""
        return [
            f"{l['insight']} (source: {l['source']}, conf: {l['confidence']})"
            for l in learnings
        ]
    
    def _generate_template(self, patterns: Dict, log: Dict) -> Dict:
        """
        Generate reusable prompt template.
        
        Pattern: claude-code-2-0-deduplicated-final.md {{variable}} style
        """
        return {
            "template_id": f"template_{log['session_id']}",
            "task_type": log.get('task_type', 'unknown'),
            "template": "{{USER_REQUEST}}\n\n[LEARNED PATTERNS]\n" + "\n".join(patterns['decision_patterns']),
            "variables": ["USER_REQUEST"],
            "effectiveness": log['effectiveness_score'],
            "patterns": patterns,
            "created_at": time.time()
        }
    
    def _save_template(self, template: Dict):
        """Save template for reuse."""
        template_file = self.storage_dir / f"template_{template['template_id']}.json"
        with open(template_file, 'w') as f:
            json.dump(template, f, indent=2)
    
    def _compress_to_key_points(self, log: Dict) -> Dict:
        """Compress log to essential information only."""
        return {
            "session_id": log['session_id'],
            "task_type": log.get('task_type'),
            "effectiveness": log.get('effectiveness_score'),
            "key_points": {
                "best_decision": max(log['trace']['decisions'], key=lambda x: x.get('confidence', 0)) if log['trace']['decisions'] else None,
                "best_learning": max(log['trace']['learnings'], key=lambda x: x.get('confidence', 0)) if log['trace']['learnings'] else None,
                "most_accurate_impact": max(log['trace']['impacts'], key=lambda x: x.get('prediction_accuracy', 0)) if log['trace']['impacts'] else None
            }
        }
    
    def get_stats(self) -> Dict:
        """Get optimization statistics."""
        return self.stats.copy()

