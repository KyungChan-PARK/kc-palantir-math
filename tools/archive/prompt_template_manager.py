"""
Prompt Template Manager with {{variables}} Support

Manages reusable prompt templates for consistent agent delegation:
- Template registration and storage
- {{variable}} substitution
- Effectiveness tracking
- Best template selection

Features:
- Claude Console compatible {{variable}} syntax
- Template versioning
- Usage analytics
- Automatic effectiveness learning

Usage:
    from tools.prompt_template_manager import PromptTemplateManager
    
    manager = PromptTemplateManager()
    
    # Register template
    manager.register_template(
        "research_task",
        template="Research {{CONCEPT}} using {{METHOD}}...",
        effectiveness=9.2
    )
    
    # Instantiate with variables
    prompt = manager.instantiate_template("research_task", {
        "CONCEPT": "Fourier Transform",
        "METHOD": "web search + documentation"
    })

VERSION: 1.0.0
DATE: 2025-10-16
"""

from typing import Dict, Optional, List
from pathlib import Path
import json
from datetime import datetime


class PromptTemplateManager:
    """
    Manage reusable prompt templates with {{variables}}.
    
    Compatible with Claude Console template syntax.
    Tracks effectiveness for continuous improvement.
    """
    
    def __init__(self, templates_dir: Path = None):
        """
        Initialize template manager.
        
        Args:
            templates_dir: Directory for template storage
        """
        self.templates_dir = templates_dir or Path("/home/kc-palantir/math/.claude/templates")
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        self.templates: Dict[str, Dict] = {}
        self.metadata_file = self.templates_dir / "metadata.json"
        self._load_templates()
    
    def _load_templates(self):
        """Load all templates from disk."""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r') as f:
                    self.templates = json.load(f)
            except Exception as e:
                print(f"WARNING: Failed to load templates metadata: {e}")
                self.templates = {}
        
        # Load individual template files
        for template_file in self.templates_dir.glob("*.md"):
            name = template_file.stem
            if name not in self.templates:
                # Register from file
                template_text = template_file.read_text()
                self.templates[name] = {
                    "template": template_text,
                    "effectiveness": 0.0,
                    "usage_count": 0,
                    "success_count": 0,
                    "created_at": datetime.now().isoformat()
                }
    
    def _save_metadata(self):
        """Save templates metadata."""
        try:
            with open(self.metadata_file, 'w') as f:
                json.dump(self.templates, f, indent=2)
        except Exception as e:
            print(f"WARNING: Failed to save templates metadata: {e}")
    
    def _save_template(self, name: str):
        """Save individual template to file."""
        if name not in self.templates:
            return
        
        template_file = self.templates_dir / f"{name}.md"
        template_text = self.templates[name]["template"]
        
        try:
            template_file.write_text(template_text)
        except Exception as e:
            print(f"WARNING: Failed to save template {name}: {e}")
    
    def register_template(
        self,
        name: str,
        template: str,
        effectiveness: float = 0.0,
        category: str = ""
    ):
        """
        Register a prompt template.
        
        Args:
            name: Unique template identifier
            template: Template text with {{variables}}
            effectiveness: Initial effectiveness score (0-10)
            category: Template category (research, build, validate, etc.)
        """
        self.templates[name] = {
            "template": template,
            "effectiveness": effectiveness,
            "usage_count": 0,
            "success_count": 0,
            "category": category,
            "created_at": datetime.now().isoformat(),
            "last_used": None
        }
        
        self._save_template(name)
        self._save_metadata()
    
    def instantiate_template(self, name: str, variables: Dict[str, str]) -> str:
        """
        Fill {{variables}} in template.
        
        Args:
            name: Template name
            variables: Dictionary of variable_name -> value
        
        Returns:
            Instantiated template with variables replaced
        
        Raises:
            ValueError: If template not found
        """
        if name not in self.templates:
            raise ValueError(f"Template '{name}' not found. Available: {list(self.templates.keys())}")
        
        template = self.templates[name]["template"]
        
        # Replace {{variable}} with values
        for var_name, var_value in variables.items():
            placeholder = f"{{{{{var_name}}}}}"
            template = template.replace(placeholder, var_value)
        
        # Update usage statistics
        self.templates[name]["usage_count"] += 1
        self.templates[name]["last_used"] = datetime.now().isoformat()
        self._save_metadata()
        
        return template
    
    def record_success(self, name: str, success: bool):
        """
        Record template usage outcome for effectiveness tracking.
        
        Args:
            name: Template name
            success: Whether the template led to successful outcome
        """
        if name not in self.templates:
            return
        
        if success:
            self.templates[name]["success_count"] += 1
        
        # Recalculate effectiveness (success rate)
        usage = self.templates[name]["usage_count"]
        successes = self.templates[name]["success_count"]
        
        if usage > 0:
            self.templates[name]["effectiveness"] = (successes / usage) * 10
        
        self._save_metadata()
    
    def get_best_template(self, category: str) -> Optional[str]:
        """
        Get highest-effectiveness template for category.
        
        Args:
            category: Template category to search
        
        Returns:
            Template name or None if no templates in category
        """
        category_templates = [
            (name, meta) for name, meta in self.templates.items()
            if meta.get("category") == category or category in name
        ]
        
        if not category_templates:
            return None
        
        # Sort by effectiveness (usage-weighted)
        def score_template(item):
            name, meta = item
            effectiveness = meta.get("effectiveness", 0)
            usage = meta.get("usage_count", 0)
            # Weight by usage (prefer proven templates)
            return effectiveness * (1 + min(usage / 10, 1))
        
        best = max(category_templates, key=score_template)
        return best[0]
    
    def list_templates(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List all templates or templates in specific category.
        
        Args:
            category: Optional category filter
        
        Returns:
            List of template info dictionaries
        """
        templates = []
        
        for name, meta in self.templates.items():
            if category and meta.get("category") != category and category not in name:
                continue
            
            templates.append({
                "name": name,
                "category": meta.get("category", "uncategorized"),
                "effectiveness": meta.get("effectiveness", 0),
                "usage_count": meta.get("usage_count", 0),
                "success_rate": (meta.get("success_count", 0) / max(meta.get("usage_count", 1), 1)) * 100
            })
        
        # Sort by effectiveness
        templates.sort(key=lambda x: x["effectiveness"], reverse=True)
        return templates


def create_template_manager(templates_dir: str = None) -> PromptTemplateManager:
    """Factory function for easy template manager creation."""
    if templates_dir:
        return PromptTemplateManager(Path(templates_dir))
    return PromptTemplateManager()

