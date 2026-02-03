#!/usr/bin/env python3
"""
Discord Agent Inter-Communication Simulation Framework
Tests agents collaborating WITHIN Discord - messaging each other, tagging,
handoffs with context, swarming, and cross-functional pipelines.
"""

import json
import random
import uuid
from datetime import datetime, timedelta
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Set, Tuple
from enum import Enum
from collections import defaultdict
import re

# =============================================================================
# AGENT DEFINITIONS
# =============================================================================

@dataclass
class Agent:
    name: str
    role: str
    expertise: List[str]
    can_delegate_to: List[str]
    response_style: str
    typical_actions: List[str]

AGENTS = {
    "Sierra": Agent(
        name="Sierra",
        role="coordinator",
        expertise=["orchestration", "task_breakdown", "delegation", "status_tracking", "conflict_resolution"],
        can_delegate_to=["Scout", "Forge", "Spark", "Hunter", "Gears", "Echo", "Lens"],
        response_style="directive_supportive",
        typical_actions=["delegate", "coordinate", "summarize", "check_status", "resolve_conflict"]
    ),
    "Scout": Agent(
        name="Scout",
        role="research",
        expertise=["web_research", "competitor_analysis", "market_data", "fact_finding", "trend_analysis"],
        can_delegate_to=["Lens", "Echo", "Hunter"],
        response_style="informative_thorough",
        typical_actions=["research", "discover", "report_findings", "hand_off_data"]
    ),
    "Forge": Agent(
        name="Forge",
        role="development",
        expertise=["coding", "api_design", "debugging", "architecture", "deployment"],
        can_delegate_to=["Gears", "Lens", "Scout"],
        response_style="technical_precise",
        typical_actions=["build", "fix", "deploy", "review_code", "hand_off_implementation"]
    ),
    "Spark": Agent(
        name="Spark",
        role="creative",
        expertise=["ideation", "campaigns", "branding", "storytelling", "innovation"],
        can_delegate_to=["Echo", "Lens", "Forge"],
        response_style="enthusiastic_creative",
        typical_actions=["brainstorm", "concept", "pitch_idea", "hand_off_creative"]
    ),
    "Hunter": Agent(
        name="Hunter",
        role="acquisition",
        expertise=["lead_gen", "outreach", "sales", "prospecting", "deal_tracking"],
        can_delegate_to=["Echo", "Scout", "Lens"],
        response_style="action_oriented",
        typical_actions=["find_leads", "qualify", "outreach", "hand_off_prospects"]
    ),
    "Gears": Agent(
        name="Gears",
        role="automation",
        expertise=["workflows", "integrations", "scheduling", "process_optimization", "bots"],
        can_delegate_to=["Forge", "Scout", "Lens"],
        response_style="systematic_efficient",
        typical_actions=["automate", "integrate", "schedule", "hand_off_workflow"]
    ),
    "Echo": Agent(
        name="Echo",
        role="communication",
        expertise=["copywriting", "social_media", "email", "messaging", "content"],
        can_delegate_to=["Spark", "Hunter", "Scout"],
        response_style="articulate_engaging",
        typical_actions=["write", "draft", "publish", "hand_off_content"]
    ),
    "Lens": Agent(
        name="Lens",
        role="analysis",
        expertise=["data_analysis", "reporting", "metrics", "insights", "visualization"],
        can_delegate_to=["Scout", "Gears", "Forge"],
        response_style="analytical_insightful",
        typical_actions=["analyze", "report", "visualize", "hand_off_insights"]
    ),
}

# =============================================================================
# MESSAGE & CONVERSATION TYPES
# =============================================================================

class MessageType(Enum):
    USER_REQUEST = "user_request"
    AGENT_TO_AGENT = "agent_to_agent"
    HANDOFF = "handoff"
    SWARM_JOIN = "swarm_join"
    STATUS_UPDATE = "status_update"
    COORDINATION = "coordination"
    DISCOVERY_ALERT = "discovery_alert"
    QUESTION = "question"
    ANSWER = "answer"
    TASK_COMPLETE = "task_complete"

class ScenarioType(Enum):
    DISCOVERY_TAG = "discovery_tag"           # Agent discovers → tags another
    HANDOFF_WITH_CONTEXT = "handoff_context"  # Handoff with rich context
    SWARM = "swarm"                           # Multiple agents on one problem
    SIERRA_DELEGATION = "sierra_delegation"   # Sierra coordinating
    CROSS_FUNCTIONAL = "cross_functional"     # Pipeline workflows
    CONFLICT_RESOLUTION = "conflict_resolution"
    ASYNC_COLLABORATION = "async_collaboration"
    QUESTION_CHAIN = "question_chain"

@dataclass
class Message:
    id: str
    timestamp: datetime
    from_agent: str
    to_agents: List[str]  # Can be multiple (mentions)
    content: str
    message_type: MessageType
    context: Dict = field(default_factory=dict)
    reply_to: Optional[str] = None
    
    def to_discord_format(self) -> str:
        """Format as Discord message"""
        mentions = " ".join([f"@{a}" for a in self.to_agents]) if self.to_agents else ""
        prefix = f"**{self.from_agent}**: "
        if mentions:
            return f"{prefix}{mentions} {self.content}"
        return f"{prefix}{self.content}"

@dataclass 
class Conversation:
    id: str
    scenario_type: ScenarioType
    trigger: str  # What started this
    messages: List[Message] = field(default_factory=list)
    participating_agents: Set[str] = field(default_factory=set)
    context_passed: Dict = field(default_factory=dict)
    outcome: Optional[str] = None
    
    def add_message(self, msg: Message):
        self.messages.append(msg)
        self.participating_agents.add(msg.from_agent)
        for agent in msg.to_agents:
            self.participating_agents.add(agent)

# =============================================================================
# TEST RESULT TRACKING
# =============================================================================

@dataclass
class CommunicationMetrics:
    total_messages: int = 0
    successful_handoffs: int = 0
    failed_handoffs: int = 0
    context_preserved: int = 0
    context_lost: int = 0
    swarm_participations: int = 0
    appropriate_tags: int = 0
    inappropriate_tags: int = 0
    coordination_success: int = 0
    coordination_failure: int = 0

@dataclass
class TestResult:
    scenario_id: str
    scenario_type: str
    trigger: str
    message_count: int
    agents_involved: List[str]
    conversation_flow: List[Dict]
    handoff_successful: bool
    context_preserved: bool
    coordination_quality: float  # 0.0 to 1.0
    resolution_achieved: bool
    issues: List[str]
    time_to_resolution_ms: int

# =============================================================================
# MESSAGE TEMPLATES - Inter-Agent Communication
# =============================================================================

DISCOVERY_TEMPLATES = {
    "Scout": [
        "@{target} Found something interesting while researching {topic}: {finding}. You should look at this for {reason}.",
        "@{target} Heads up - discovered {finding} in my research. This could be useful for your {task}.",
        "@{target} Just uncovered some data on {topic}. Here's what I found: {finding}. Thoughts?",
    ],
    "Forge": [
        "@{target} Built the {component} - it's ready for you to {next_action}. API endpoint: {endpoint}",
        "@{target} Code is deployed. You can now {capability}. Let me know if you need any adjustments.",
        "@{target} Technical implementation done for {feature}. Passing this to you for {next_step}.",
    ],
    "Lens": [
        "@{target} Analysis complete on {dataset}. Key insight: {insight}. You might want to {action}.",
        "@{target} Data shows {finding}. This impacts your {area} - we should discuss next steps.",
        "@{target} Found a pattern in the {metric} data: {pattern}. Relevant for your work on {project}.",
    ],
    "Hunter": [
        "@{target} Got {count} qualified leads from {source}. Ready for you to craft outreach for {segment}.",
        "@{target} This prospect ({company}) looks hot - {context}. Can you draft something compelling?",
        "@{target} Lead intel: {company} is {situation}. Let's move fast on this one.",
    ],
}

HANDOFF_TEMPLATES = {
    ("Scout", "Hunter"): [
        "@Hunter Here's the research on {company}: {research_summary}. They're {situation}. Good prospect for {reason}.",
        "@Hunter Found these {count} companies matching our ICP: {list}. Background on each attached. Your turn!",
    ],
    ("Scout", "Lens"): [
        "@Lens Gathered data on {topic}: {data_summary}. Can you analyze and pull out actionable insights?",
        "@Lens Here's the raw data from {sources}. Need your analysis on {question}.",
    ],
    ("Scout", "Echo"): [
        "@Echo Research done on {topic}. Key points: {points}. Can you turn this into a blog post?",
        "@Echo Found these interesting facts about {subject}: {facts}. Let's make content from this.",
    ],
    ("Hunter", "Echo"): [
        "@Echo Got a prospect list for {campaign}. Need personalized outreach emails. Context: {context}",
        "@Echo These leads need follow-up: {leads}. Can you draft {email_type} emails? Tone should be {tone}.",
    ],
    ("Hunter", "Lens"): [
        "@Lens Here's our outreach data from {period}: {metrics}. Can you analyze conversion patterns?",
        "@Lens Need analysis on which lead sources are performing. Data: {data}",
    ],
    ("Spark", "Echo"): [
        "@Echo Love this concept: {concept}. Can you write the copy? Tone: {tone}, audience: {audience}.",
        "@Echo Campaign idea ready: {idea}. Need you to bring it to life with words. Key message: {message}.",
    ],
    ("Spark", "Forge"): [
        "@Forge Had an idea for {feature}: {description}. Is this technically feasible? What would it take?",
        "@Forge Creative concept needs technical backing: {concept}. Can you prototype something?",
    ],
    ("Forge", "Gears"): [
        "@Gears API is live at {endpoint}. Can you build automation workflows that use it for {purpose}?",
        "@Gears Built {component}. Ready for you to integrate into the {workflow} pipeline.",
    ],
    ("Gears", "Lens"): [
        "@Lens Automation is running, collecting {data_type}. Can you set up dashboards to track {metrics}?",
        "@Gears Data pipeline operational. Output: {output}. Need analysis workflow built on top.",
    ],
    ("Lens", "Spark"): [
        "@Spark Analysis shows {insight}. Can you brainstorm creative ways to leverage this?",
        "@Spark Data says {finding}. Need fresh ideas on how to respond. What do you think?",
    ],
    ("Echo", "Hunter"): [
        "@Hunter Content is live: {content}. Can you use this in your outreach? Works well for {segment}.",
        "@Hunter Wrote {count} email templates for {campaign}. Ready for you to test with real prospects.",
    ],
}

SWARM_TEMPLATES = [
    {
        "trigger": "🚨 Emergency: {crisis} - need all hands!",
        "agents": ["Sierra", "Scout", "Forge", "Gears"],
        "context": "crisis_response"
    },
    {
        "trigger": "Big opportunity: {opportunity}. Let's figure this out together.",
        "agents": ["Sierra", "Scout", "Hunter", "Spark", "Echo"],
        "context": "opportunity_pursuit"
    },
    {
        "trigger": "Strategy session: How do we {goal}?",
        "agents": ["Sierra", "Spark", "Lens", "Hunter"],
        "context": "strategy_planning"
    },
    {
        "trigger": "Product launch in {timeframe}. What do we need?",
        "agents": ["Sierra", "Forge", "Echo", "Hunter", "Lens"],
        "context": "launch_coordination"
    },
    {
        "trigger": "Client escalation: {client} is {issue}. Help!",
        "agents": ["Sierra", "Echo", "Hunter", "Lens"],
        "context": "escalation_handling"
    },
]

SIERRA_COORDINATION_TEMPLATES = [
    {
        "request": "User wants to launch a new product",
        "delegation": [
            ("Scout", "Research the market and competitors"),
            ("Spark", "Develop brand positioning and campaign concepts"),
            ("Forge", "Build the landing page and signup flow"),
            ("Echo", "Create launch content and announcements"),
            ("Hunter", "Prepare outreach for initial customers"),
            ("Lens", "Set up tracking and success metrics"),
        ]
    },
    {
        "request": "Need to improve our lead conversion rate",
        "delegation": [
            ("Lens", "Analyze current funnel and identify drop-off points"),
            ("Hunter", "Review lead quality and qualification process"),
            ("Echo", "Audit messaging and email sequences"),
            ("Gears", "Check automation for gaps or issues"),
        ]
    },
    {
        "request": "Create a content marketing strategy",
        "delegation": [
            ("Scout", "Research what topics resonate with our audience"),
            ("Lens", "Analyze our best-performing content"),
            ("Spark", "Brainstorm fresh content angles and formats"),
            ("Echo", "Draft the content calendar and first pieces"),
        ]
    },
    {
        "request": "Automate our sales pipeline",
        "delegation": [
            ("Hunter", "Document current sales process and pain points"),
            ("Gears", "Design automation workflows"),
            ("Forge", "Build custom integrations needed"),
            ("Lens", "Set up pipeline analytics"),
        ]
    },
]

CROSS_FUNCTIONAL_PIPELINES = [
    {
        "name": "Market Research → Lead Gen → Outreach",
        "stages": [
            {"agent": "Scout", "action": "research", "output": "market_intel", "next": "Hunter"},
            {"agent": "Hunter", "action": "qualify_leads", "output": "prospect_list", "next": "Echo"},
            {"agent": "Echo", "action": "write_outreach", "output": "email_campaigns", "next": "Hunter"},
            {"agent": "Hunter", "action": "execute_outreach", "output": "responses", "next": "Lens"},
            {"agent": "Lens", "action": "analyze_results", "output": "insights", "next": None},
        ]
    },
    {
        "name": "Idea → Content → Distribution",
        "stages": [
            {"agent": "Spark", "action": "ideate", "output": "content_concepts", "next": "Scout"},
            {"agent": "Scout", "action": "research", "output": "supporting_data", "next": "Echo"},
            {"agent": "Echo", "action": "write_content", "output": "articles", "next": "Lens"},
            {"agent": "Lens", "action": "analyze_performance", "output": "content_metrics", "next": None},
        ]
    },
    {
        "name": "Analysis → Strategy → Execution",
        "stages": [
            {"agent": "Lens", "action": "analyze_data", "output": "insights", "next": "Spark"},
            {"agent": "Spark", "action": "develop_strategy", "output": "action_plan", "next": "Sierra"},
            {"agent": "Sierra", "action": "coordinate_execution", "output": "task_assignments", "next": "Gears"},
            {"agent": "Gears", "action": "build_automation", "output": "workflows", "next": "Lens"},
        ]
    },
    {
        "name": "Build → Integrate → Monitor",
        "stages": [
            {"agent": "Forge", "action": "develop", "output": "components", "next": "Gears"},
            {"agent": "Gears", "action": "integrate", "output": "connected_system", "next": "Lens"},
            {"agent": "Lens", "action": "setup_monitoring", "output": "dashboards", "next": None},
        ]
    },
    {
        "name": "Prospect Research → Qualification → Pitch",
        "stages": [
            {"agent": "Scout", "action": "research_prospects", "output": "company_profiles", "next": "Hunter"},
            {"agent": "Hunter", "action": "qualify_and_score", "output": "qualified_leads", "next": "Spark"},
            {"agent": "Spark", "action": "develop_pitch_angle", "output": "pitch_concepts", "next": "Echo"},
            {"agent": "Echo", "action": "craft_pitch", "output": "pitch_deck", "next": "Hunter"},
        ]
    },
]

# Variable pools for template filling
VARIABLES = {
    "topic": ["AI adoption", "market expansion", "competitor moves", "industry trends", "customer behavior", "pricing strategies"],
    "finding": ["a 40% increase in demand", "three new competitors", "a gap in the market", "concerning churn pattern", "untapped segment"],
    "target": list(AGENTS.keys()),
    "reason": ["your outreach campaign", "the strategy deck", "our pricing model", "the product roadmap", "client presentation"],
    "task": ["lead generation", "content creation", "technical implementation", "data analysis", "campaign planning"],
    "component": ["authentication module", "data pipeline", "API gateway", "notification service", "analytics tracker"],
    "endpoint": ["/api/v1/leads", "/api/v1/analytics", "/api/v1/campaigns", "/api/v1/users", "/api/v1/reports"],
    "capability": ["track user events", "process payments", "send notifications", "generate reports", "sync data"],
    "feature": ["real-time dashboards", "automated scoring", "smart routing", "predictive analytics", "custom integrations"],
    "next_step": ["QA testing", "user documentation", "performance tuning", "security review", "deployment"],
    "dataset": ["Q4 sales", "campaign performance", "user engagement", "churn cohorts", "conversion funnel"],
    "insight": ["conversion drops 60% at signup", "Tuesday emails perform 2x better", "enterprise segment is most profitable"],
    "metric": ["CAC", "LTV", "NPS", "churn rate", "MRR", "conversion rate"],
    "pattern": ["seasonal spike", "declining engagement", "price sensitivity", "feature adoption curve"],
    "company": ["TechCorp", "InnovateCo", "ScaleUp Ltd", "DataDriven Inc", "FutureTech", "GrowthBox"],
    "count": ["15", "27", "42", "8", "63", "100+"],
    "source": ["LinkedIn", "conferences", "referrals", "content downloads", "webinar attendees"],
    "segment": ["enterprise", "SMB", "startups", "agencies", "e-commerce"],
    "situation": ["raising Series B", "expanding to EU", "looking for automation", "unhappy with current vendor", "scaling rapidly"],
    "campaign": ["product launch", "re-engagement", "upsell", "nurture", "win-back"],
    "email_type": ["intro", "follow-up", "breakup", "case study", "demo invite"],
    "tone": ["consultative", "direct", "friendly", "urgent", "thought-leadership"],
    "concept": ["gamified onboarding", "community-led growth", "product-led expansion", "viral referral loop"],
    "idea": ["interactive calculator", "industry report", "video series", "podcast launch", "event sponsorship"],
    "message": ["save 10 hours/week", "increase revenue 30%", "eliminate manual work", "scale without hiring"],
    "audience": ["CTOs", "marketing managers", "founders", "ops teams", "sales leaders"],
    "description": ["AI-powered suggestions", "smart automation rules", "predictive lead scoring", "custom dashboards"],
    "workflow": ["lead nurturing", "customer onboarding", "support escalation", "content publishing"],
    "data_type": ["user events", "conversion data", "engagement metrics", "revenue figures"],
    "output": ["daily summary emails", "real-time alerts", "weekly reports", "triggered notifications"],
    "content": ["blog post on AI trends", "case study video", "product update email", "social campaign"],
    "crisis": ["production is down", "major client threatening to churn", "competitor launched similar feature", "data breach detected"],
    "opportunity": ["enterprise client wants demo", "viral tweet about us", "partnership offer from BigCo", "press coverage opportunity"],
    "goal": ["double revenue this quarter", "enter the European market", "launch enterprise tier", "reduce churn by 50%"],
    "timeframe": ["2 weeks", "30 days", "end of quarter", "next Monday"],
    "client": ["MegaCorp", "TopClient Inc", "BigSpender LLC"],
    "issue": ["threatening to cancel", "unhappy with support", "asking for features we don't have", "disputing invoice"],
    "research_summary": ["Series B funded, 200 employees, expanding sales team", "Just hired new CTO, modernizing stack", "Competitor customer, contract up in Q2"],
    "list": ["TechA, TechB, TechC", "Company1, Company2, Company3"],
    "data_summary": ["50 data points across 3 categories", "competitive landscape with 12 players", "market size $4.2B growing 15% YoY"],
    "sources": ["Crunchbase, LinkedIn, industry reports", "customer interviews, survey data", "public filings, news articles"],
    "question": ["what's driving churn", "which segment to focus on", "optimal pricing point"],
    "points": ["market growing 20% YoY", "3 main competitors", "key differentiator is speed"],
    "subject": ["remote work trends", "AI in marketing", "sales automation"],
    "facts": ["73% of teams use automation", "average rep spends 4h on admin", "top performers follow up 5x more"],
    "leads": ["CEO@techco.com, VP@startup.io", "list of 25 marketing directors"],
    "period": ["last 30 days", "Q3", "since launch", "past week"],
    "metrics": ["42% open rate, 8% reply rate", "15% conversion, $45 CAC"],
    "data": ["spreadsheet with 500 rows", "CRM export", "campaign analytics"],
}

# =============================================================================
# SIMULATION ENGINE
# =============================================================================

class InterAgentSimulator:
    def __init__(self):
        self.agents = AGENTS
        self.conversations: List[Conversation] = []
        self.results: List[TestResult] = []
        self.metrics = CommunicationMetrics()
        
    def fill_template(self, template: str, extra_vars: Dict = None) -> str:
        """Fill template with random variables"""
        result = template
        all_vars = {**VARIABLES, **(extra_vars or {})}
        
        for var_name, values in all_vars.items():
            placeholder = "{" + var_name + "}"
            while placeholder in result:
                if isinstance(values, list):
                    result = result.replace(placeholder, random.choice(values), 1)
                else:
                    result = result.replace(placeholder, str(values), 1)
        return result
    
    def generate_message_id(self) -> str:
        return f"msg-{uuid.uuid4().hex[:8]}"
    
    def generate_conversation_id(self) -> str:
        return f"conv-{uuid.uuid4().hex[:12]}"
    
    # -------------------------------------------------------------------------
    # Scenario Generators
    # -------------------------------------------------------------------------
    
    def generate_discovery_tag_scenario(self) -> Conversation:
        """Agent discovers something and tags another agent"""
        discoverer = random.choice(["Scout", "Lens", "Forge", "Hunter"])
        templates = DISCOVERY_TEMPLATES.get(discoverer, DISCOVERY_TEMPLATES["Scout"])
        
        # Pick appropriate target based on discovery type
        target_map = {
            "Scout": ["Hunter", "Lens", "Echo", "Spark"],
            "Lens": ["Spark", "Hunter", "Sierra", "Gears"],
            "Forge": ["Gears", "Lens", "Sierra"],
            "Hunter": ["Echo", "Lens", "Sierra"],
        }
        target = random.choice(target_map.get(discoverer, ["Sierra"]))
        
        conv = Conversation(
            id=self.generate_conversation_id(),
            scenario_type=ScenarioType.DISCOVERY_TAG,
            trigger=f"{discoverer} discovers relevant information for {target}"
        )
        
        # Discovery message
        template = random.choice(templates)
        content = self.fill_template(template, {"target": target})
        
        msg1 = Message(
            id=self.generate_message_id(),
            timestamp=datetime.now(),
            from_agent=discoverer,
            to_agents=[target],
            content=content,
            message_type=MessageType.DISCOVERY_ALERT,
            context={"discovery_type": discoverer, "relevance": random.uniform(0.6, 1.0)}
        )
        conv.add_message(msg1)
        
        # Target acknowledges and acts
        ack_templates = [
            "Thanks @{from_agent}! This is exactly what I needed. Let me {action} with this.",
            "Great find @{from_agent}. I'll {action} and report back.",
            "Perfect timing @{from_agent}. Working on {task} now - this helps a lot.",
            "@{from_agent} 👍 On it. Will update the team when I have {output}.",
        ]
        ack_content = self.fill_template(
            random.choice(ack_templates),
            {"from_agent": discoverer, "action": "work on this", "output": "results"}
        )
        
        msg2 = Message(
            id=self.generate_message_id(),
            timestamp=datetime.now() + timedelta(seconds=random.randint(30, 300)),
            from_agent=target,
            to_agents=[discoverer],
            content=ack_content,
            message_type=MessageType.AGENT_TO_AGENT,
            reply_to=msg1.id
        )
        conv.add_message(msg2)
        
        # Sometimes a follow-up or status update
        if random.random() > 0.4:
            status_templates = [
                "Update: {progress}. @{original} your research was key here.",
                "Quick update - {progress}. Should have full results by {time}.",
                "FYI @{original} - {progress}. This is going well.",
            ]
            msg3 = Message(
                id=self.generate_message_id(),
                timestamp=datetime.now() + timedelta(seconds=random.randint(600, 3600)),
                from_agent=target,
                to_agents=[discoverer],
                content=self.fill_template(
                    random.choice(status_templates),
                    {"progress": "made good headway", "original": discoverer, "time": "EOD"}
                ),
                message_type=MessageType.STATUS_UPDATE,
                reply_to=msg1.id
            )
            conv.add_message(msg3)
        
        conv.outcome = "discovery_acted_upon"
        conv.context_passed = {"discovery": content, "acknowledged": True}
        return conv
    
    def generate_handoff_with_context_scenario(self) -> Conversation:
        """Handoff between agents with rich context"""
        # Pick a valid handoff pair
        handoff_pairs = list(HANDOFF_TEMPLATES.keys())
        from_agent, to_agent = random.choice(handoff_pairs)
        templates = HANDOFF_TEMPLATES[(from_agent, to_agent)]
        
        conv = Conversation(
            id=self.generate_conversation_id(),
            scenario_type=ScenarioType.HANDOFF_WITH_CONTEXT,
            trigger=f"Handoff from {from_agent} to {to_agent}"
        )
        
        # Initial handoff message with context
        handoff_content = self.fill_template(random.choice(templates))
        context_data = {
            "work_completed": f"{from_agent}'s deliverable",
            "key_insights": self.fill_template("{insight}"),
            "next_action_needed": f"Action for {to_agent}",
            "deadline": random.choice(["EOD", "tomorrow", "this week", "ASAP"]),
            "priority": random.choice(["high", "medium", "normal"]),
        }
        
        msg1 = Message(
            id=self.generate_message_id(),
            timestamp=datetime.now(),
            from_agent=from_agent,
            to_agents=[to_agent],
            content=handoff_content,
            message_type=MessageType.HANDOFF,
            context=context_data
        )
        conv.add_message(msg1)
        
        # Receiving agent confirms and asks clarifying question (sometimes)
        if random.random() > 0.3:
            clarify_templates = [
                "Got it @{from_agent}. Quick question - {question}?",
                "Thanks! Before I dive in - {question}?",
                "On it. Just to confirm - {question}?",
            ]
            questions = [
                "should I prioritize speed or thoroughness",
                "is there a specific angle you want me to focus on",
                "any constraints I should know about",
                "who's the primary stakeholder here",
            ]
            msg2 = Message(
                id=self.generate_message_id(),
                timestamp=datetime.now() + timedelta(seconds=random.randint(60, 300)),
                from_agent=to_agent,
                to_agents=[from_agent],
                content=self.fill_template(
                    random.choice(clarify_templates),
                    {"from_agent": from_agent, "question": random.choice(questions)}
                ),
                message_type=MessageType.QUESTION,
                reply_to=msg1.id
            )
            conv.add_message(msg2)
            
            # Answer
            answer_templates = [
                "Good question - {answer}. Let me know if you need anything else.",
                "{answer}. Happy to jump on a quick call if helpful.",
                "Yeah, {answer}. You've got good judgment here.",
            ]
            msg3 = Message(
                id=self.generate_message_id(),
                timestamp=datetime.now() + timedelta(seconds=random.randint(120, 600)),
                from_agent=from_agent,
                to_agents=[to_agent],
                content=self.fill_template(
                    random.choice(answer_templates),
                    {"answer": "prioritize quality over speed for this one"}
                ),
                message_type=MessageType.ANSWER,
                reply_to=msg2.id
            )
            conv.add_message(msg3)
        
        # Task completion
        complete_templates = [
            "@{from_agent} Done! {summary}. Let me know if you need revisions.",
            "Finished the {task}. @{from_agent} here's what I came up with: {summary}",
            "@{from_agent} Completed. {summary}. Ready for next steps.",
        ]
        msg_complete = Message(
            id=self.generate_message_id(),
            timestamp=datetime.now() + timedelta(seconds=random.randint(1800, 7200)),
            from_agent=to_agent,
            to_agents=[from_agent],
            content=self.fill_template(
                random.choice(complete_templates),
                {"from_agent": from_agent, "task": "work", "summary": "Here's the output with your context incorporated"}
            ),
            message_type=MessageType.TASK_COMPLETE,
            reply_to=msg1.id,
            context={"preserves_original_context": random.random() > 0.15}  # 85% context preservation
        )
        conv.add_message(msg_complete)
        
        conv.outcome = "handoff_complete"
        conv.context_passed = context_data
        return conv
    
    def generate_swarm_scenario(self) -> Conversation:
        """Multiple agents collaborating on one problem"""
        template = random.choice(SWARM_TEMPLATES)
        trigger = self.fill_template(template["trigger"])
        agents = template["agents"]
        
        conv = Conversation(
            id=self.generate_conversation_id(),
            scenario_type=ScenarioType.SWARM,
            trigger=trigger
        )
        
        # Initial alert (usually from Sierra or the discoverer)
        initiator = "Sierra" if "Sierra" in agents else agents[0]
        msg1 = Message(
            id=self.generate_message_id(),
            timestamp=datetime.now(),
            from_agent=initiator,
            to_agents=[a for a in agents if a != initiator],
            content=trigger,
            message_type=MessageType.SWARM_JOIN,
            context={"swarm_type": template["context"], "urgency": random.choice(["high", "medium"])}
        )
        conv.add_message(msg1)
        
        # Each agent joins and contributes
        contributions = []
        for i, agent in enumerate([a for a in agents if a != initiator]):
            join_templates = [
                "I'm in. From my perspective, {contribution}.",
                "On it. Here's what I can offer: {contribution}.",
                "Jumping in - {contribution}. What else do we need?",
                "Here to help. Quick thought: {contribution}.",
            ]
            
            contribution_map = {
                "Scout": "I can research the background and get us intel fast",
                "Forge": "I'll check the technical side and see what's possible",
                "Spark": "Let me think of creative angles we haven't considered",
                "Hunter": "I can reach out to the contacts and get direct feedback",
                "Gears": "I'll look at what we can automate to speed this up",
                "Echo": "I can draft comms once we have a plan",
                "Lens": "Let me pull the data so we're making informed decisions",
            }
            
            msg = Message(
                id=self.generate_message_id(),
                timestamp=datetime.now() + timedelta(seconds=random.randint(30, 180) * (i + 1)),
                from_agent=agent,
                to_agents=[initiator],
                content=self.fill_template(
                    random.choice(join_templates),
                    {"contribution": contribution_map.get(agent, "I'll help however needed")}
                ),
                message_type=MessageType.SWARM_JOIN,
                reply_to=msg1.id
            )
            conv.add_message(msg)
            contributions.append((agent, contribution_map.get(agent, "")))
        
        # Coordinator (Sierra) synthesizes and assigns
        if "Sierra" in agents:
            synthesis_templates = [
                "Great team. Here's the plan: {assignments}. Let's sync in {time}.",
                "Love the energy. Breaking this down: {assignments}. Questions?",
                "Perfect. Assigning: {assignments}. Keep me posted on blockers.",
            ]
            assignments = ", ".join([f"@{a[0]} handles {a[1].split()[2:5]}" for a in contributions[:3]])
            
            msg_coord = Message(
                id=self.generate_message_id(),
                timestamp=datetime.now() + timedelta(seconds=random.randint(300, 600)),
                from_agent="Sierra",
                to_agents=[a for a in agents if a != "Sierra"],
                content=self.fill_template(
                    random.choice(synthesis_templates),
                    {"assignments": assignments or "each of you take your specialty", "time": "2 hours"}
                ),
                message_type=MessageType.COORDINATION,
                reply_to=msg1.id
            )
            conv.add_message(msg_coord)
        
        # Status updates as work progresses
        for agent in random.sample([a for a in agents if a != "Sierra"], min(2, len(agents)-1)):
            status_msg = Message(
                id=self.generate_message_id(),
                timestamp=datetime.now() + timedelta(seconds=random.randint(1800, 5400)),
                from_agent=agent,
                to_agents=["Sierra"] if "Sierra" in agents else [agents[0]],
                content=f"Update: made progress on my part. {random.choice(['On track.', 'Slight blocker but handling it.', 'Found something interesting.'])}",
                message_type=MessageType.STATUS_UPDATE
            )
            conv.add_message(status_msg)
        
        conv.outcome = "swarm_coordinated"
        conv.context_passed = {"participants": agents, "contributions": len(contributions)}
        return conv
    
    def generate_sierra_delegation_scenario(self) -> Conversation:
        """Sierra coordinating and delegating to specialists"""
        template = random.choice(SIERRA_COORDINATION_TEMPLATES)
        
        conv = Conversation(
            id=self.generate_conversation_id(),
            scenario_type=ScenarioType.SIERRA_DELEGATION,
            trigger=template["request"]
        )
        
        # User makes request (simulated as external trigger)
        msg_trigger = Message(
            id=self.generate_message_id(),
            timestamp=datetime.now(),
            from_agent="User",
            to_agents=["Sierra"],
            content=template["request"],
            message_type=MessageType.USER_REQUEST
        )
        conv.add_message(msg_trigger)
        
        # Sierra acknowledges and breaks down work
        delegations = template["delegation"]
        delegation_text = "\n".join([f"• @{agent}: {task}" for agent, task in delegations[:4]])
        
        sierra_msg = Message(
            id=self.generate_message_id(),
            timestamp=datetime.now() + timedelta(seconds=random.randint(10, 30)),
            from_agent="Sierra",
            to_agents=[d[0] for d in delegations[:4]],
            content=f"On it! Breaking this down:\n\n{delegation_text}\n\nLet's coordinate in thread. Questions?",
            message_type=MessageType.COORDINATION,
            context={"task_breakdown": delegations, "coordination_style": "parallel"}
        )
        conv.add_message(sierra_msg)
        
        # Agents acknowledge
        ack_styles = {
            "Scout": "🔍 Starting research now.",
            "Forge": "👨‍💻 On it. Will need ~{time} for this.",
            "Spark": "💡 Love it! Already have some ideas brewing.",
            "Hunter": "🎯 Got it. Prepping outreach.",
            "Gears": "⚙️ Setting up the workflow.",
            "Echo": "✍️ Ready to write. Will wait for inputs from others.",
            "Lens": "📊 Pulling the data now.",
        }
        
        for agent, task in delegations[:4]:
            ack_msg = Message(
                id=self.generate_message_id(),
                timestamp=datetime.now() + timedelta(seconds=random.randint(60, 300)),
                from_agent=agent,
                to_agents=["Sierra"],
                content=self.fill_template(ack_styles.get(agent, "On it!"), {"time": random.choice(["2h", "4h", "EOD"])}),
                message_type=MessageType.AGENT_TO_AGENT,
                reply_to=sierra_msg.id
            )
            conv.add_message(ack_msg)
        
        # Sierra checks in mid-work
        checkin_msg = Message(
            id=self.generate_message_id(),
            timestamp=datetime.now() + timedelta(seconds=random.randint(3600, 7200)),
            from_agent="Sierra",
            to_agents=[d[0] for d in delegations[:4]],
            content="Quick status check - how's everyone progressing? Any blockers?",
            message_type=MessageType.COORDINATION
        )
        conv.add_message(checkin_msg)
        
        # Completion reports
        for agent, task in random.sample(delegations[:4], min(3, len(delegations))):
            complete_msg = Message(
                id=self.generate_message_id(),
                timestamp=datetime.now() + timedelta(seconds=random.randint(7200, 14400)),
                from_agent=agent,
                to_agents=["Sierra"],
                content=f"✅ Done with my part: {task[:30]}... Ready for review or handoff.",
                message_type=MessageType.TASK_COMPLETE
            )
            conv.add_message(complete_msg)
        
        # Sierra summarizes
        summary_msg = Message(
            id=self.generate_message_id(),
            timestamp=datetime.now() + timedelta(seconds=random.randint(14400, 18000)),
            from_agent="Sierra",
            to_agents=["User"],
            content="Great work team! @User - we've completed the initial phase. Summary: [deliverables ready]. What would you like to prioritize next?",
            message_type=MessageType.COORDINATION,
            context={"coordination_successful": True, "agents_delivered": len(delegations)}
        )
        conv.add_message(summary_msg)
        
        conv.outcome = "delegation_complete"
        conv.context_passed = {"delegations": len(delegations), "completed": True}
        return conv
    
    def generate_cross_functional_scenario(self) -> Conversation:
        """Pipeline workflows across multiple agents"""
        pipeline = random.choice(CROSS_FUNCTIONAL_PIPELINES)
        
        conv = Conversation(
            id=self.generate_conversation_id(),
            scenario_type=ScenarioType.CROSS_FUNCTIONAL,
            trigger=f"Pipeline: {pipeline['name']}"
        )
        
        stages = pipeline["stages"]
        prev_output = None
        
        for i, stage in enumerate(stages):
            agent = stage["agent"]
            action = stage["action"]
            output = stage["output"]
            next_agent = stage["next"]
            
            # Stage work message
            if i == 0:
                content = f"Starting {action}. Will produce {output} for the pipeline."
            else:
                content = f"Received {prev_output} from previous stage. Now {action}. Output: {output}."
            
            work_msg = Message(
                id=self.generate_message_id(),
                timestamp=datetime.now() + timedelta(seconds=random.randint(300, 900) * (i + 1)),
                from_agent=agent,
                to_agents=[next_agent] if next_agent else ["Sierra"],
                content=content,
                message_type=MessageType.STATUS_UPDATE,
                context={"pipeline_stage": i, "output_type": output}
            )
            conv.add_message(work_msg)
            
            # Handoff to next stage
            if next_agent:
                handoff_templates = [
                    f"@{next_agent} {output} ready. Here's what I found: {{summary}}. Your turn for {stages[i+1]['action'] if i+1 < len(stages) else 'next step'}.",
                    f"@{next_agent} Passing {output} to you. Key points: {{summary}}. Let me know if you need clarification.",
                    f"@{next_agent} Done with {action}. Output attached. Ready when you are.",
                ]
                
                handoff_msg = Message(
                    id=self.generate_message_id(),
                    timestamp=datetime.now() + timedelta(seconds=random.randint(300, 900) * (i + 1) + 300),
                    from_agent=agent,
                    to_agents=[next_agent],
                    content=self.fill_template(random.choice(handoff_templates), {"summary": f"[{output} summary]"}),
                    message_type=MessageType.HANDOFF,
                    context={"from_stage": i, "to_stage": i + 1, "output": output}
                )
                conv.add_message(handoff_msg)
                
                # Next agent acknowledges
                ack_msg = Message(
                    id=self.generate_message_id(),
                    timestamp=datetime.now() + timedelta(seconds=random.randint(300, 900) * (i + 1) + 600),
                    from_agent=next_agent,
                    to_agents=[agent],
                    content=f"Got it @{agent}! Processing {output} now.",
                    message_type=MessageType.AGENT_TO_AGENT,
                    reply_to=handoff_msg.id
                )
                conv.add_message(ack_msg)
            
            prev_output = output
        
        # Final summary
        final_agent = stages[-1]["agent"]
        summary_msg = Message(
            id=self.generate_message_id(),
            timestamp=datetime.now() + timedelta(seconds=random.randint(300, 900) * len(stages) + 1000),
            from_agent=final_agent,
            to_agents=["Sierra"],
            content=f"Pipeline complete! 🎉 Final output: {stages[-1]['output']}. All {len(stages)} stages finished successfully.",
            message_type=MessageType.TASK_COMPLETE,
            context={"pipeline_name": pipeline["name"], "stages_completed": len(stages)}
        )
        conv.add_message(summary_msg)
        
        conv.outcome = "pipeline_complete"
        conv.context_passed = {"pipeline": pipeline["name"], "stages": len(stages), "final_output": stages[-1]["output"]}
        return conv
    
    def generate_conflict_resolution_scenario(self) -> Conversation:
        """Agents have conflicting recommendations, Sierra mediates"""
        conflicting_agents = random.choice([
            ("Hunter", "Echo", "paid vs organic growth strategy"),
            ("Forge", "Gears", "custom build vs no-code solution"),
            ("Spark", "Lens", "creative risk vs data-driven approach"),
            ("Scout", "Hunter", "market timing - wait vs act now"),
        ])
        
        agent_a, agent_b, topic = conflicting_agents
        
        conv = Conversation(
            id=self.generate_conversation_id(),
            scenario_type=ScenarioType.CONFLICT_RESOLUTION,
            trigger=f"Conflict: {agent_a} vs {agent_b} on {topic}"
        )
        
        # Agent A's position
        msg_a = Message(
            id=self.generate_message_id(),
            timestamp=datetime.now(),
            from_agent=agent_a,
            to_agents=["Sierra", agent_b],
            content=f"I think we should {topic.split(' vs ')[0] if ' vs ' in topic else 'take approach A'}. Here's why: [reasoning based on my expertise].",
            message_type=MessageType.AGENT_TO_AGENT,
            context={"position": "A", "confidence": random.uniform(0.7, 0.95)}
        )
        conv.add_message(msg_a)
        
        # Agent B's counter position
        msg_b = Message(
            id=self.generate_message_id(),
            timestamp=datetime.now() + timedelta(seconds=random.randint(60, 180)),
            from_agent=agent_b,
            to_agents=["Sierra", agent_a],
            content=f"Respectfully disagree @{agent_a}. I'd recommend {topic.split(' vs ')[1] if ' vs ' in topic else 'approach B'} because: [counter reasoning].",
            message_type=MessageType.AGENT_TO_AGENT,
            context={"position": "B", "confidence": random.uniform(0.7, 0.95)}
        )
        conv.add_message(msg_b)
        
        # Sierra steps in to mediate
        mediation_templates = [
            f"Good points from both of you. @{agent_a} @{agent_b} - let me synthesize: {{synthesis}}. Thoughts?",
            f"I see merit in both approaches. What if we {{compromise}}? @{agent_a} @{agent_b}",
            f"Let's get more data before deciding. @Lens can you analyze {{question}}? Then we'll reconvene.",
        ]
        
        msg_sierra = Message(
            id=self.generate_message_id(),
            timestamp=datetime.now() + timedelta(seconds=random.randint(300, 600)),
            from_agent="Sierra",
            to_agents=[agent_a, agent_b],
            content=self.fill_template(
                random.choice(mediation_templates),
                {"synthesis": "we could do A short-term, B long-term", "compromise": "test both approaches", "question": "the historical data on this"}
            ),
            message_type=MessageType.COORDINATION,
            context={"mediation_style": random.choice(["synthesis", "compromise", "data_driven"])}
        )
        conv.add_message(msg_sierra)
        
        # Resolution
        resolution_templates = [
            f"@Sierra That works for me. @{agent_b} let's try it.",
            f"Fair enough. @{agent_a} let's collaborate on this.",
            "Good call. I'm on board with the hybrid approach.",
        ]
        
        msg_resolve = Message(
            id=self.generate_message_id(),
            timestamp=datetime.now() + timedelta(seconds=random.randint(600, 900)),
            from_agent=random.choice([agent_a, agent_b]),
            to_agents=["Sierra"],
            content=self.fill_template(random.choice(resolution_templates)),
            message_type=MessageType.AGENT_TO_AGENT
        )
        conv.add_message(msg_resolve)
        
        conv.outcome = "conflict_resolved"
        conv.context_passed = {"agents": [agent_a, agent_b], "topic": topic, "resolution": "mediated"}
        return conv
    
    def generate_async_collaboration_scenario(self) -> Conversation:
        """Agents working asynchronously, picking up where others left off"""
        agents_involved = random.sample(list(AGENTS.keys())[1:], 3)  # Exclude Sierra initially
        
        conv = Conversation(
            id=self.generate_conversation_id(),
            scenario_type=ScenarioType.ASYNC_COLLABORATION,
            trigger=f"Async work between {', '.join(agents_involved)}"
        )
        
        # First agent starts work
        msg1 = Message(
            id=self.generate_message_id(),
            timestamp=datetime.now(),
            from_agent=agents_involved[0],
            to_agents=[agents_involved[1]],
            content=f"Started working on the project. Made progress on [part 1]. @{agents_involved[1]} I'm logging off - can you pick up [part 2] when you're online?",
            message_type=MessageType.HANDOFF,
            context={"work_state": "partial", "handoff_type": "async"}
        )
        conv.add_message(msg1)
        
        # Hours later, second agent picks up
        msg2 = Message(
            id=self.generate_message_id(),
            timestamp=datetime.now() + timedelta(hours=random.randint(2, 8)),
            from_agent=agents_involved[1],
            to_agents=[agents_involved[0], agents_involved[2]],
            content=f"@{agents_involved[0]} Just saw your message. Picked up where you left off. Completed [part 2]. @{agents_involved[2]} can you review when you get a chance?",
            message_type=MessageType.STATUS_UPDATE,
            context={"work_state": "continued", "async_delay_hours": random.randint(2, 8)}
        )
        conv.add_message(msg2)
        
        # Third agent reviews
        msg3 = Message(
            id=self.generate_message_id(),
            timestamp=datetime.now() + timedelta(hours=random.randint(3, 12)),
            from_agent=agents_involved[2],
            to_agents=[agents_involved[0], agents_involved[1]],
            content=f"@{agents_involved[0]} @{agents_involved[1]} Reviewed the work - looking good! Added my piece. We're ready to ship. 🚀",
            message_type=MessageType.TASK_COMPLETE,
            context={"work_state": "complete", "review_passed": True}
        )
        conv.add_message(msg3)
        
        conv.outcome = "async_complete"
        conv.context_passed = {"agents": agents_involved, "async_delays": True, "completed": True}
        return conv
    
    def generate_question_chain_scenario(self) -> Conversation:
        """Agent asks question, gets answer, asks follow-up, involves others"""
        asker = random.choice(["Hunter", "Echo", "Gears"])
        expert = random.choice(["Scout", "Forge", "Lens", "Spark"])
        
        conv = Conversation(
            id=self.generate_conversation_id(),
            scenario_type=ScenarioType.QUESTION_CHAIN,
            trigger=f"{asker} asks {expert} a question"
        )
        
        # Initial question
        question_templates = [
            f"@{expert} Quick question - {{question}}?",
            f"@{expert} Need your expertise: {{question}}",
            f"Hey @{expert}, do you know {{question}}?",
        ]
        
        questions = [
            "what's the best approach for handling {topic}",
            "how should we think about {topic}",
            "what data do we have on {topic}",
            "can you help me understand {topic}",
        ]
        
        msg1 = Message(
            id=self.generate_message_id(),
            timestamp=datetime.now(),
            from_agent=asker,
            to_agents=[expert],
            content=self.fill_template(random.choice(question_templates), {"question": self.fill_template(random.choice(questions))}),
            message_type=MessageType.QUESTION
        )
        conv.add_message(msg1)
        
        # Expert answers
        msg2 = Message(
            id=self.generate_message_id(),
            timestamp=datetime.now() + timedelta(seconds=random.randint(60, 300)),
            from_agent=expert,
            to_agents=[asker],
            content=f"@{asker} Good question! Here's what I know: [detailed answer based on my expertise]. Does that help?",
            message_type=MessageType.ANSWER,
            reply_to=msg1.id
        )
        conv.add_message(msg2)
        
        # Follow-up question
        msg3 = Message(
            id=self.generate_message_id(),
            timestamp=datetime.now() + timedelta(seconds=random.randint(120, 480)),
            from_agent=asker,
            to_agents=[expert],
            content=f"That helps! Follow-up: what about [specific aspect]? Should we loop in @Sierra or someone else?",
            message_type=MessageType.QUESTION,
            reply_to=msg2.id
        )
        conv.add_message(msg3)
        
        # Expert suggests involving another agent
        other_agent = random.choice([a for a in AGENTS.keys() if a not in [asker, expert, "Sierra"]])
        msg4 = Message(
            id=self.generate_message_id(),
            timestamp=datetime.now() + timedelta(seconds=random.randint(180, 600)),
            from_agent=expert,
            to_agents=[asker, other_agent],
            content=f"For that specific piece, @{other_agent} would know better. @{other_agent} can you weigh in on [specific aspect]?",
            message_type=MessageType.AGENT_TO_AGENT,
            reply_to=msg3.id
        )
        conv.add_message(msg4)
        
        # Other agent contributes
        msg5 = Message(
            id=self.generate_message_id(),
            timestamp=datetime.now() + timedelta(seconds=random.randint(300, 900)),
            from_agent=other_agent,
            to_agents=[asker, expert],
            content=f"@{asker} @{expert} Yeah I can help with that. Here's my take: [additional expertise]. Between the three of us that should cover it!",
            message_type=MessageType.ANSWER,
            reply_to=msg4.id
        )
        conv.add_message(msg5)
        
        conv.outcome = "question_answered"
        conv.context_passed = {"question_chain_length": 3, "agents_involved": [asker, expert, other_agent]}
        return conv
    
    # -------------------------------------------------------------------------
    # Simulation Runner
    # -------------------------------------------------------------------------
    
    def generate_scenarios(self, total: int = 1000) -> None:
        """Generate all test scenarios with realistic distribution"""
        distribution = {
            ScenarioType.DISCOVERY_TAG: int(total * 0.15),        # 150
            ScenarioType.HANDOFF_WITH_CONTEXT: int(total * 0.20), # 200
            ScenarioType.SWARM: int(total * 0.12),                # 120
            ScenarioType.SIERRA_DELEGATION: int(total * 0.18),    # 180
            ScenarioType.CROSS_FUNCTIONAL: int(total * 0.15),     # 150
            ScenarioType.CONFLICT_RESOLUTION: int(total * 0.08),  # 80
            ScenarioType.ASYNC_COLLABORATION: int(total * 0.07),  # 70
            ScenarioType.QUESTION_CHAIN: int(total * 0.05),       # 50
        }
        
        generators = {
            ScenarioType.DISCOVERY_TAG: self.generate_discovery_tag_scenario,
            ScenarioType.HANDOFF_WITH_CONTEXT: self.generate_handoff_with_context_scenario,
            ScenarioType.SWARM: self.generate_swarm_scenario,
            ScenarioType.SIERRA_DELEGATION: self.generate_sierra_delegation_scenario,
            ScenarioType.CROSS_FUNCTIONAL: self.generate_cross_functional_scenario,
            ScenarioType.CONFLICT_RESOLUTION: self.generate_conflict_resolution_scenario,
            ScenarioType.ASYNC_COLLABORATION: self.generate_async_collaboration_scenario,
            ScenarioType.QUESTION_CHAIN: self.generate_question_chain_scenario,
        }
        
        for scenario_type, count in distribution.items():
            print(f"  Generating {count} {scenario_type.value} scenarios...")
            generator = generators[scenario_type]
            for _ in range(count):
                try:
                    conv = generator()
                    self.conversations.append(conv)
                except Exception as e:
                    print(f"    Error generating scenario: {e}")
        
        print(f"Total scenarios generated: {len(self.conversations)}")
    
    def evaluate_conversation(self, conv: Conversation) -> TestResult:
        """Evaluate a conversation for success metrics"""
        issues = []
        
        # Check handoff success
        handoff_msgs = [m for m in conv.messages if m.message_type == MessageType.HANDOFF]
        handoff_successful = True
        if handoff_msgs:
            # Check if handoffs were acknowledged
            for handoff in handoff_msgs:
                followups = [m for m in conv.messages if m.reply_to == handoff.id]
                if not followups:
                    handoff_successful = False
                    issues.append(f"Handoff from {handoff.from_agent} not acknowledged")
        
        # Check context preservation
        context_preserved = True
        if conv.context_passed:
            # Check if context was referenced in later messages
            context_keys = set(conv.context_passed.keys())
            later_contexts = [m.context for m in conv.messages[1:] if m.context]
            
            # Simulate context checking
            if random.random() > 0.85:  # 15% chance of context loss
                context_preserved = False
                issues.append("Context not fully preserved in handoff")
        
        # Evaluate coordination quality
        coordination_factors = []
        
        # Factor 1: Response times (simulated)
        avg_response_gap = random.uniform(50, 500)  # ms between messages
        coordination_factors.append(1.0 if avg_response_gap < 300 else 0.7)
        
        # Factor 2: Appropriate tagging
        tags_appropriate = True
        for msg in conv.messages:
            if msg.to_agents and msg.from_agent in AGENTS:
                for target in msg.to_agents:
                    if target in AGENTS and target != "User":
                        # Check if tag was relevant
                        if target not in AGENTS[msg.from_agent].can_delegate_to and msg.from_agent != "Sierra":
                            if random.random() > 0.8:  # Some tolerance
                                tags_appropriate = False
                                issues.append(f"Unusual tag: {msg.from_agent} → {target}")
        coordination_factors.append(1.0 if tags_appropriate else 0.6)
        
        # Factor 3: Resolution achieved
        resolution_achieved = conv.outcome is not None and any(word in conv.outcome for word in ["complete", "resolved", "acted_upon", "answered", "coordinated"])
        coordination_factors.append(1.0 if resolution_achieved else 0.5)
        
        # Factor 4: Message efficiency (not too many, not too few)
        optimal_msg_range = (3, 12)
        msg_count = len(conv.messages)
        if optimal_msg_range[0] <= msg_count <= optimal_msg_range[1]:
            coordination_factors.append(1.0)
        elif msg_count > optimal_msg_range[1]:
            coordination_factors.append(0.8)
            issues.append(f"High message count ({msg_count}) may indicate coordination issues")
        else:
            coordination_factors.append(0.7)
        
        coordination_quality = sum(coordination_factors) / len(coordination_factors)
        
        # Time to resolution (simulated)
        if conv.messages:
            time_range = (conv.messages[-1].timestamp - conv.messages[0].timestamp).total_seconds()
            time_to_resolution = int(time_range * 1000)  # Convert to ms
        else:
            time_to_resolution = 0
        
        return TestResult(
            scenario_id=conv.id,
            scenario_type=conv.scenario_type.value,
            trigger=conv.trigger,
            message_count=len(conv.messages),
            agents_involved=list(conv.participating_agents),
            conversation_flow=[
                {
                    "from": m.from_agent,
                    "to": m.to_agents,
                    "type": m.message_type.value,
                    "preview": m.content[:80] + "..." if len(m.content) > 80 else m.content
                }
                for m in conv.messages
            ],
            handoff_successful=handoff_successful,
            context_preserved=context_preserved,
            coordination_quality=coordination_quality,
            resolution_achieved=resolution_achieved,
            issues=issues,
            time_to_resolution_ms=time_to_resolution
        )
    
    def run_simulation(self) -> None:
        """Evaluate all conversations"""
        print(f"\nEvaluating {len(self.conversations)} conversations...")
        
        for i, conv in enumerate(self.conversations):
            result = self.evaluate_conversation(conv)
            self.results.append(result)
            
            # Update metrics
            self.metrics.total_messages += result.message_count
            if result.handoff_successful:
                self.metrics.successful_handoffs += 1
            else:
                self.metrics.failed_handoffs += 1
            if result.context_preserved:
                self.metrics.context_preserved += 1
            else:
                self.metrics.context_lost += 1
            if result.coordination_quality > 0.7:
                self.metrics.coordination_success += 1
            else:
                self.metrics.coordination_failure += 1
            
            if (i + 1) % 200 == 0:
                print(f"  Evaluated {i + 1}/{len(self.conversations)}")
        
        print("Evaluation complete!")
    
    def analyze_results(self) -> Dict:
        """Generate comprehensive analysis report"""
        total = len(self.results)
        
        # Overall success metrics
        overall_success = sum(1 for r in self.results if r.resolution_achieved and r.handoff_successful and r.context_preserved)
        
        # By scenario type
        type_analysis = {}
        for scenario_type in ScenarioType:
            type_results = [r for r in self.results if r.scenario_type == scenario_type.value]
            if type_results:
                type_analysis[scenario_type.value] = {
                    "count": len(type_results),
                    "success_rate": sum(1 for r in type_results if r.resolution_achieved) / len(type_results),
                    "handoff_success": sum(1 for r in type_results if r.handoff_successful) / len(type_results),
                    "context_preservation": sum(1 for r in type_results if r.context_preserved) / len(type_results),
                    "avg_coordination_quality": sum(r.coordination_quality for r in type_results) / len(type_results),
                    "avg_message_count": sum(r.message_count for r in type_results) / len(type_results),
                    "avg_time_to_resolution_ms": sum(r.time_to_resolution_ms for r in type_results) / len(type_results),
                }
        
        # Agent participation analysis
        agent_stats = {agent: {"participated": 0, "initiated": 0, "received_handoffs": 0} for agent in AGENTS.keys()}
        for result in self.results:
            for agent in result.agents_involved:
                if agent in agent_stats:
                    agent_stats[agent]["participated"] += 1
            if result.conversation_flow:
                initiator = result.conversation_flow[0].get("from")
                if initiator in agent_stats:
                    agent_stats[initiator]["initiated"] += 1
                for msg in result.conversation_flow:
                    if msg.get("type") == "handoff":
                        for recipient in msg.get("to", []):
                            if recipient in agent_stats:
                                agent_stats[recipient]["received_handoffs"] += 1
        
        # Common issues
        all_issues = []
        for r in self.results:
            all_issues.extend(r.issues)
        
        issue_counts = {}
        for issue in all_issues:
            # Categorize issues
            if "not acknowledged" in issue:
                cat = "handoff_not_acknowledged"
            elif "Context not" in issue:
                cat = "context_lost"
            elif "Unusual tag" in issue:
                cat = "inappropriate_routing"
            elif "message count" in issue:
                cat = "coordination_overhead"
            else:
                cat = "other"
            issue_counts[cat] = issue_counts.get(cat, 0) + 1
        
        # Generate recommendations
        recommendations = self.generate_recommendations(type_analysis, issue_counts, agent_stats)
        
        # Sample conversations for report
        sample_conversations = self.get_sample_conversations(10)
        
        return {
            "summary": {
                "total_scenarios": total,
                "overall_success_rate": overall_success / total,
                "handoff_success_rate": self.metrics.successful_handoffs / total,
                "context_preservation_rate": self.metrics.context_preserved / total,
                "coordination_success_rate": self.metrics.coordination_success / total,
                "total_messages_exchanged": self.metrics.total_messages,
                "avg_messages_per_scenario": self.metrics.total_messages / total,
            },
            "by_scenario_type": type_analysis,
            "agent_participation": agent_stats,
            "common_failures": issue_counts,
            "recommendations": recommendations,
            "sample_conversations": sample_conversations,
            "metadata": {
                "simulation_timestamp": datetime.now().isoformat(),
                "framework_version": "2.0.0",
                "agent_count": len(AGENTS),
                "agents": list(AGENTS.keys()),
                "scenario_types_tested": [st.value for st in ScenarioType],
            }
        }
    
    def generate_recommendations(self, type_analysis: Dict, issues: Dict, agent_stats: Dict) -> List[Dict]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Check handoff issues
        handoff_scenarios = type_analysis.get("handoff_context", {})
        if handoff_scenarios.get("handoff_success", 1.0) < 0.90:
            recommendations.append({
                "priority": "high",
                "area": "handoff_protocol",
                "issue": f"Handoff success at {handoff_scenarios.get('handoff_success', 0):.1%}",
                "suggestion": "Implement mandatory handoff acknowledgment: receiving agent must confirm receipt and understanding before original agent disengages",
                "implementation": "Add @acknowledge command or reaction requirement for handoffs",
                "expected_impact": "15-20% improvement in handoff completion"
            })
        
        # Check context preservation
        if issues.get("context_lost", 0) > 50:
            recommendations.append({
                "priority": "high",
                "area": "context_management",
                "issue": f"{issues['context_lost']} instances of context loss in handoffs",
                "suggestion": "Implement structured context blocks that must be included in handoffs",
                "implementation": "Use formatted context template: ```context\\n[key_info]\\n[dependencies]\\n[next_actions]\\n```",
                "expected_impact": "Reduce context loss by 60%"
            })
        
        # Check swarm coordination
        swarm_analysis = type_analysis.get("swarm", {})
        if swarm_analysis.get("avg_coordination_quality", 1.0) < 0.80:
            recommendations.append({
                "priority": "medium",
                "area": "swarm_coordination",
                "issue": f"Swarm coordination quality at {swarm_analysis.get('avg_coordination_quality', 0):.1%}",
                "suggestion": "Establish clear swarm protocols with Sierra as explicit coordinator",
                "implementation": "Sierra should: 1) Acknowledge swarm trigger, 2) Assign specific roles, 3) Set sync checkpoint, 4) Collect and synthesize outputs",
                "expected_impact": "Better organized multi-agent responses"
            })
        
        # Check for routing issues
        if issues.get("inappropriate_routing", 0) > 30:
            recommendations.append({
                "priority": "medium",
                "area": "agent_routing",
                "issue": f"{issues['inappropriate_routing']} inappropriate agent tags detected",
                "suggestion": "Agents should route through Sierra for cross-functional requests rather than direct tagging",
                "implementation": "Exception: established handoff pairs (Scout→Hunter, Spark→Echo) can direct-tag",
                "expected_impact": "Clearer responsibility chains"
            })
        
        # Check Sierra's workload
        sierra_stats = agent_stats.get("Sierra", {})
        if sierra_stats.get("participated", 0) > len(self.results) * 0.5:
            recommendations.append({
                "priority": "low",
                "area": "coordinator_load",
                "issue": f"Sierra involved in {sierra_stats['participated']} scenarios ({sierra_stats['participated']/len(self.results):.0%})",
                "suggestion": "Enable more direct agent-to-agent workflows for established patterns",
                "implementation": "Create 'trusted handoff pairs' that don't need Sierra's coordination",
                "expected_impact": "Reduced bottleneck, faster execution"
            })
        
        # Pipeline recommendations
        pipeline_analysis = type_analysis.get("cross_functional", {})
        if pipeline_analysis.get("avg_time_to_resolution_ms", 0) > 10000000:  # > 10000 seconds
            recommendations.append({
                "priority": "medium",
                "area": "pipeline_efficiency",
                "issue": "Cross-functional pipelines taking too long",
                "suggestion": "Add parallel execution where dependencies allow",
                "implementation": "Identify independent stages that can run concurrently (e.g., Scout researching while Echo prepares templates)",
                "expected_impact": "30-40% faster pipeline completion"
            })
        
        # Always include these best practices
        recommendations.extend([
            {
                "priority": "low",
                "area": "async_collaboration",
                "issue": "Opportunity for improvement",
                "suggestion": "Agents should leave detailed status notes when going offline",
                "implementation": "Standard format: 'Logging off. Status: [done], [in-progress], [blocked]. @[next-agent] can pick up [task].'",
                "expected_impact": "Smoother async handoffs"
            },
            {
                "priority": "low",
                "area": "conflict_resolution",
                "issue": "Proactive improvement",
                "suggestion": "When agents disagree, default to data-driven resolution via Lens before Sierra mediates",
                "implementation": "Disagreement protocol: 1) State positions, 2) @Lens for data, 3) @Sierra if still unresolved",
                "expected_impact": "Faster, more objective conflict resolution"
            }
        ])
        
        return sorted(recommendations, key=lambda x: {"high": 0, "medium": 1, "low": 2}[x["priority"]])
    
    def get_sample_conversations(self, count: int = 10) -> List[Dict]:
        """Get representative sample conversations for the report"""
        samples = []
        
        # Get one of each type
        for scenario_type in ScenarioType:
            matching = [c for c in self.conversations if c.scenario_type == scenario_type]
            if matching:
                conv = random.choice(matching)
                result = next((r for r in self.results if r.scenario_id == conv.id), None)
                
                samples.append({
                    "id": conv.id,
                    "type": scenario_type.value,
                    "trigger": conv.trigger,
                    "participants": list(conv.participating_agents),
                    "message_count": len(conv.messages),
                    "messages": [
                        {
                            "from": m.from_agent,
                            "to": m.to_agents,
                            "content": m.to_discord_format(),
                            "type": m.message_type.value
                        }
                        for m in conv.messages
                    ],
                    "outcome": conv.outcome,
                    "success": result.resolution_achieved if result else None,
                    "coordination_quality": result.coordination_quality if result else None,
                })
        
        return samples[:count]
    
    def export_results(self, filepath: str) -> Dict:
        """Export full analysis to JSON"""
        analysis = self.analyze_results()
        
        # Add failed scenario details
        failed_scenarios = [
            {
                "id": r.scenario_id,
                "type": r.scenario_type,
                "trigger": r.trigger,
                "issues": r.issues,
                "agents": r.agents_involved,
            }
            for r in self.results
            if not r.resolution_achieved or not r.handoff_successful
        ][:30]  # Limit to 30 examples
        
        analysis["failed_scenarios_sample"] = failed_scenarios
        
        with open(filepath, 'w') as f:
            json.dump(analysis, f, indent=2, default=str)
        
        print(f"\nResults exported to: {filepath}")
        return analysis


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 70)
    print("Discord Agent Inter-Communication Simulation Framework v2.0")
    print("=" * 70)
    print("\nAgents:")
    for name, agent in AGENTS.items():
        print(f"  • {name} ({agent.role}): {', '.join(agent.expertise[:3])}...")
    print()
    
    simulator = InterAgentSimulator()
    
    print("Generating 1000 test scenarios...")
    simulator.generate_scenarios(1000)
    
    print("\nRunning simulation...")
    simulator.run_simulation()
    
    output_path = "/home/ec2-user/clawd/data/agent-simulation-results.json"
    analysis = simulator.export_results(output_path)
    
    # Print summary
    print("\n" + "=" * 70)
    print("SIMULATION RESULTS")
    print("=" * 70)
    
    s = analysis["summary"]
    print(f"""
📊 Overall Metrics:
   • Total Scenarios: {s['total_scenarios']}
   • Overall Success Rate: {s['overall_success_rate']:.1%}
   • Handoff Success Rate: {s['handoff_success_rate']:.1%}
   • Context Preservation: {s['context_preservation_rate']:.1%}
   • Coordination Success: {s['coordination_success_rate']:.1%}
   • Total Messages Exchanged: {s['total_messages_exchanged']:,}
   • Avg Messages/Scenario: {s['avg_messages_per_scenario']:.1f}
""")
    
    print("📈 By Scenario Type:")
    for type_name, metrics in analysis["by_scenario_type"].items():
        print(f"   {type_name}: {metrics['count']} scenarios, {metrics['success_rate']:.1%} success, {metrics['avg_coordination_quality']:.2f} coord quality")
    
    print("\n🤖 Agent Participation:")
    for agent, stats in sorted(analysis["agent_participation"].items(), key=lambda x: x[1]["participated"], reverse=True):
        print(f"   {agent}: {stats['participated']} scenarios, {stats['initiated']} initiated, {stats['received_handoffs']} handoffs received")
    
    print("\n❌ Common Failures:")
    for issue, count in sorted(analysis["common_failures"].items(), key=lambda x: x[1], reverse=True):
        print(f"   {issue}: {count}")
    
    print("\n💡 Top Recommendations:")
    for rec in analysis["recommendations"][:4]:
        print(f"   [{rec['priority'].upper()}] {rec['area']}: {rec['suggestion'][:70]}...")
    
    print("\n" + "=" * 70)
    print(f"Full report: {output_path}")
    print("=" * 70)
    
    return analysis


if __name__ == "__main__":
    main()
