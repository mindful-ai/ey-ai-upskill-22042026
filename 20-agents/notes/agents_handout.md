**Agents Workshop — Student Handout**

This handout expands each topic from `notes.md` into concise explanations, practical LangChain examples, Crew AI (pseudocode) examples where applicable, and real-world use cases for learning and workshop exercises.

**1. Fundamentals of Agents & Real-world Use Cases**
- **Concept:** An "agent" is a program that perceives its environment, makes decisions, and acts to achieve goals. Modern AI agents combine LLMs with tools, memory, and planning.
- **LangChain example:** Use a `LLMChain` or `Agent` with tools (search, python REPL).

```python
from langchain.agents import initialize_agent, Tool
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI()
search_tool = Tool(name="search", func=search_function, description="Web search")
agent = initialize_agent([search_tool], llm, agent="zero-shot-react-description")
agent.run("Find the release date of Project X and summarize it")
```

- **Crew AI (pseudocode):**
```
# pseudocode - generic Crew AI SDK pattern
crew = CrewClient(api_key=...)
agent = crew.create_agent(name="researcher", tools=["web_search","code_exec"])
agent.ask("When was Project X released?")
```
- **Use cases:** automated research assistants, customer support triage, data extraction pipelines.

**2. Agent Lifecycle & Planning**
- **Concept:** Lifecycle stages: goal definition → plan generation → tool selection → execution → observation → refinement → termination.
- **LangChain example (planning):** Prompt a planner chain to produce step-by-step subtasks, then invoke tools.

```python
from langchain import LLMChain, PromptTemplate
prompt = PromptTemplate(input_variables=["goal"], template="Generate steps to accomplish: {goal}")
planner = LLMChain(llm=ChatOpenAI(), prompt=prompt)
plan = planner.run(goal="Collect quarterly sales figures and make a summary")
```

- **Crew AI (pseudocode):**
```
plan = agent.plan(goal="ingest invoices and extract totals")
for step in plan.steps:
    agent.execute(step)
```
- **Use cases:** ETL automation, experiment orchestration, multi-step content generation.

**3. Frameworks for Agentic Systems**
- **Concept:** Frameworks (LangChain, Rasa, AutoGen, Ray, Crew) provide building blocks: prompts, chains, tools, memory, and orchestrators.
- **LangChain note:** LangChain focuses on chains, agents, tools, retrievers, and memory primitives.
- **Crew AI note:** Crew abstracts agent orchestration and often provides managed tool integrations and observability.
- **Use cases:** Rapid prototyping of assistants, reproducible agent pipelines, enterprise integrations.

**4. Tools & API Integration**
- **Concept:** Tools expose external capabilities (APIs, DBs, search, code execution) the agent can call to augment LLM reasoning.
- **LangChain example:** Wrap an API as a `Tool` with a description so the agent can decide when to call it.

```python
from langchain.agents import Tool

def weather_api(query):
    # call external weather API
    return call_weather(query)

weather_tool = Tool(name="weather", func=weather_api, description="Get weather for a location")
```

- **Crew AI (pseudocode):**
```
agent.register_tool("slack", token=...)
agent.call_tool("slack", channel="#alerts", message="Job finished")
```
- **Use cases:** Real-time data enrichment, triggering workflows, issuing commands to SaaS systems.

**5. Agent Architectures (Router vs Autonomous)**
- **Concept:** Router architecture dispatches tasks to specialized agents; autonomous architecture has self-contained agents that plan and act independently.
- **LangChain pattern:** Use an orchestration layer to route queries to different chains/agents.
- **Use cases:** Large orgs: router for domain specialists (finance, legal); autonomous for single-domain assistants.

**6. Single-Agent vs Multi-Agent Systems**
- **Concept:** Single-agent: centralized intelligence. Multi-agent: multiple agents coordinate or compete; enables specialization and parallelism.
- **LangChain example (multi-agent coordination):** Create multiple agent instances each with specific tools and combine results.
- **Use cases:** Complex workflows (sales + legal + ops), simulation environments, negotiation bots.

**7. Native AI Applications Architecture**
- **Concept:** Building apps that treat LLMs/agents as first-class components with layers: UI, orchestration, tools, data, model platform.
- **Pattern:** Separate concerns—stateless LLM calls, stateful memory/retrieval, tool layer for side-effects.
- **Use cases:** Copilots embedded in IDEs, AI-native CRMs, intelligent dashboards.

**8. Agent Collaboration Models**
- **Concept:** Collaboration patterns include synchronous turn-taking, shared workspace (blackboard), and publish/subscribe events.
- **LangChain pattern:** Use a shared retriever or vector store as a common memory for multiple agents.
- **Use cases:** Cross-team document synthesis, research assistants that delegate tasks, multi-agent data validation.

**9. Communication Protocols**
- **Concept:** Define message formats and APIs for agent interaction: structured JSON messages, event semantics, retries, acknowledgements.
- **Example:** Use JSON-RPC or a lightweight HTTP event bus for inter-agent calls.
- **Use cases:** Agent orchestration in microservices, telemetry and auditing of agent actions.

**10. State Management**
- **Concept:** State includes short-term context, long-term memory, and external persistence (DBs, vector stores). Decide what to keep in memory vs persistent stores.
- **LangChain example:** Use `ConversationBufferMemory` for session state and `Chroma`/`FAISS` for long-term retrieval.

```python
from langchain.memory import ConversationBufferMemory
memory = ConversationBufferMemory()
```

- **Use cases:** Personalized assistants, progressive task automation that learns over sessions.

**11. Retry & Failure Handling**
- **Concept:** Agents must detect tool failures, timeouts, and provide fallbacks (retries, alternate tools, graceful degradation).
- **Pattern:** Wrap tool calls with retry policies and circuit breaker patterns; log failures for debugging.
- **Use cases:** Reliable automation pipelines, resilient customer-facing assistants.

**12. Goal Setting & Planning**
- **Concept:** Goals should be explicit, measurable, and decomposable; planners convert goals into action sequences.
- **LangChain example:** Use a planning prompt to generate subtasks, then execute them sequentially or in parallel.
- **Use cases:** Automated report generation, multi-step data processing.

**13. Hierarchical vs Reactive Planning**
- **Concept:** Hierarchical planning builds a tree of subgoals (top-down). Reactive planning responds to environment signals in near real-time.
- **Use cases:** Hierarchical for batch pipelines; reactive for monitoring/incident response.

**14. Multi-Agent Strategies**
- **Concept:** Strategies include competition (market simulation), cooperation (task decomposition), and hybrid approaches.
- **Example:** Assign roles (researcher, verifier, synthesizer) and coordinate via a shared task queue.
- **Use cases:** Complex decision workflows, automated vetting systems, negotiation simulations.

**15. Reinforcement Loops in Planning**
- **Concept:** Use feedback loops—observations and outcomes—to refine policies and prompts. Reinforcement can be explicit (RL) or implicit (prompt tuning, reward models).
- **Pattern:** Track metrics, use A/B prompt variants, and adopt bandit or RL-based strategies when appropriate.
- **Use cases:** Improving agent task efficiency, refining retrieval and ranking, continual learning in deployed assistants.

---

Notes & workshop suggestions:
- Each section contains a short LangChain snippet and a Crew AI pseudocode example to illustrate patterns without depending on a specific SDK version.
- Exercises: (1) Build a simple LangChain agent with a search tool. (2) Create two agents (research + verifier) that exchange via a shared vector store. (3) Add retry logic to a tool and observe failure handling.


