# IBOBS-2002 Speaker Notes

## Session Metadata

- Session ID: IBOBS-2002
- Session Title: Automated Resolution, Accelerated Insights: AI Remediation Agents in Splunk Observability Cloud
- Session Type: Interactive Breakout
- Speaker: Marcio Kugler Rodrigues
- Co-Presenter: Leila Reyhani

## Audience and Tone

This script is written for customer executives and technical leaders.

Tone guidance:

- customer-relevant first
- strategic, but technically credible
- clear and conversational
- confident without sounding like product marketing
- focused on trust, operational value, and customer impact

What this session is not:

- not a generic observability overview
- not a generic GenAI talk
- not a claim that AI should automate everything

What this session is:

- a practical story about what changes when AI enters the production path
- a trust and operations story, not just a tooling story
- a customer-facing discussion of how to move from insight to governed action

## Core Customer Story

A company launches an AI-powered claims portal to improve customer experience and scale claims operations. Customers expect fast, accurate, always-on digital service. During peak usage, a cache volume pressure degrades response quality and latency. Splunk RUM and Digital Experience Analytics can show browser impact, while APM and Infrastructure provide the reliable proof path. Splunk Observability Cloud then provides the evidence needed to understand what is happening. A separate remediation orchestrator receives the detector alert, accepts a human-in-the-loop summary from Splunk AI Assistant or Troubleshooting Agent, enriches missing structured fields through targeted Splunk API lookups, and passes a bounded evidence package to the remediation agent. The team applies policy, approves the action, validates the outcome, and preserves the audit trail.

The core message for customers:

AI is now part of the customer experience. That means AI failures are no longer experimental failures. They are customer trust failures. The winning pattern is not blind automation. It is automation with evidence, guardrails, and validation.

## Industry Context and Trends

Use this section early in the talk to make the story timely.

Marcio:

"A lot of customers in this room are no longer asking whether AI will show up in the customer journey. It already has. It is in support, self-service, search, recommendations, and digital assistance."

"That changes the operating model. When AI becomes customer-facing, latency is visible immediately. Bad responses are visible immediately. And trust is lost much faster than it is rebuilt."

Leila:

"The second shift is operational complexity. These AI experiences are not single systems. They depend on models, tools, data sources, APIs, cache volumes, and service dependencies. So the risk surface gets wider."

"And the third shift is visibility. Customers increasingly want to start with the real digital experience: what happened in the browser, where users hesitated, where they abandoned, and what the actual session looked like."

"And the fourth shift is governance. Customers want speed, but they also want control. They want to know why the system made a recommendation, why it took an action, and whether that action was safe."

Key line to land:

"The challenge is no longer just observing the application. It is observing the digital experience, the application, the AI workflow, and the remediation path together."

Transition to next act:

Marcio:

"That is why this session is not just about faster troubleshooting. It is about how to move from accelerated insight to safe, bounded resolution."

## Full Session Script by Act

### Act 1: Opening Hook

Speaker first: Marcio

Key line to land:

"Customer trust is now directly tied to how well you operate AI in production."

Marcio:

"Let me start with a situation that is becoming very common. A company launches an AI-powered claims portal. The business loves it because it reduces pressure on human agents, it improves self-service, and it gives customers faster answers at any hour."

"Then one day, during a high-volume period, response times jump. Some answers come back slowly. Some fail entirely. Internally, the teams eventually see alerts, traces, and infrastructure metrics. But the customer does not see telemetry. The customer only sees a broken experience."

"And that is the operational shift we want to talk about today. Once AI is in the customer journey, operational issues become trust issues immediately."

Transition sentence to Leila:

"So the real question is no longer whether we can detect a problem. The real question is whether we can move from evidence to action safely. Leila, that is where the AI remediation conversation gets interesting."

Leila:

"Exactly. Customers are not asking for autonomous everything. They are asking for confidence. They want to know that if AI participates in operations, it does so with clear evidence, clear boundaries, and clear accountability."

"That is the lens for this session. We are going to show what it means to use Splunk Observability Cloud not just to detect and explain a problem, but to support a governed remediation flow."

### Act 2: Why This Is Not a Generic Observability Talk

Speaker first: Leila

Key line to land:

"Traditional observability explains problems. Modern operations also need a trustworthy path to action."

Leila:

"A lot of observability conversations stop at insight. You detect the issue, correlate signals, identify likely cause, and then hand the problem to humans to decide what to do next."

"That is still valuable. But when customer-facing AI services are involved, we have to start even earlier. We have to start with what the user experienced in the browser, in the session, and in the journey itself."

"That is why Splunk RUM and Digital Experience Analytics matter in this story. They let us start from customer truth when browser data is available, and then APM plus Infrastructure give us the reliable proof path."

"And when customer-facing AI services are involved, that last mile from insight to action matters more. The delay there can be where customer trust erodes."

"So this is not a generic observability talk. It is a talk about that operational gap between knowing and acting."

Marcio:

"And from a customer perspective, that gap is expensive. It shows up as slower resolution, more handoffs, more pressure on experts, and more time spent debating next steps while the business impact continues."

"So when we say accelerated insights, we mean more than faster dashboards. We mean evidence that is good enough to support a safe decision."

Transition sentence to next act:

Leila:

"Which brings us to the central idea of this session: if AI is going to help with remediation, then the remediation agent itself becomes part of what we need to observe."

### Act 3: The Two-Agent Model

Speaker first: Leila

Key line to land:

"The remediation agent is not magic. It is production software, and it needs production-grade observability."

Leila:

"Here is the model we want you to keep in mind. First, Splunk Observability Cloud helps detect the issue, correlate the telemetry, and provide the investigation context. In this session, that starts with digital experience telemetry, then moves into APM evidence and service relationships. That is the evidence layer."

"Second, a separate remediation orchestrator and remediation agent use that evidence to propose a bounded action. The orchestrator takes the detector alert, accepts the AI Assistant summary, enriches whatever structured fields are missing, and only then hands a bounded evidence package to the agent. That is the action layer."

"We want to be very precise here. We are not claiming that Splunk AI Assistant directly calls an arbitrary external remediation agent. In our story, Splunk provides the detection, evidence, and observability. A separate remediation path handles the action."

"That distinction matters because it keeps the architecture credible and it keeps the governance model clear."

Marcio:

"For customers, this means two things. First, you can accelerate understanding with observability. Second, you can improve action with policy-driven automation. But you should not blur those together in a way that reduces trust."

"If the remediation agent is going to recommend or execute action, you need to know what it saw, why it made that recommendation, which tool it wanted to use, and whether the result actually improved the customer experience."

Transition sentence to next act:

Leila:

"So let us make this concrete with a customer scenario."

### Act 4: Customer Scenario Setup

Speaker first: Marcio

Key line to land:

"The customer problem is visible in the business experience before it is fully understood in the telemetry."

Marcio:

"Imagine a company that has rolled out an AI claims portal. Customers use it to troubleshoot issues, ask product questions, and resolve common problems without opening a ticket."

"The experience is working well. Adoption is increasing. Leadership is happy because the portal improves satisfaction and lowers support cost."

"And importantly, this is not a one-workflow app. It has multiple business transactions. Customers can ask for claim status, check policy coverage, and search claims FAQ content. That matters because in production, not everything breaks at once."

"Now we introduce pressure in the dependency path. In this demo, the claims knowledge cache volume fills up, which is the kind of operational issue students can inspect with out-of-the-box infrastructure and APM signals."

"The result is simple: customers start waiting longer, some requests fail, and confidence in the experience starts to drop."

Leila:

"That scenario matters because it is realistic. This is how most customer-facing AI systems fail in the real world. Not with a dramatic crash, but with degraded latency, partial failure, and uncertainty about where the problem actually is."

"So in the demo, we will start by showing the degraded customer experience through the portal and RUM if it is available. Then we will use APM service behavior and host filesystem metrics as the reliable path to the root cause before moving into the remediation decision."

"And because we have multiple transactions instrumented, we can show something very important: one workflow is unhealthy, while the others remain healthy. That is a much more realistic customer story."

"And that is exactly where teams need both observability and a controlled path to remediation."

Transition sentence to demo:

Marcio:

"So now let us walk you through how that looks in practice."

## Demo Transition Script

Pre-demo setup line:

Marcio:

"As we move into the demo, what we want you to watch for is not just the incident itself. Watch how we begin with the digital experience, how the evidence builds through the backend, how the action gets proposed, and where the trust decision happens."

Leila:

"And one important note before we start: Splunk Observability Cloud is providing the detection, evidence, and observability in this flow. The remediation decision and execution happen through a separate orchestrator and remediation agent. We are keeping that line explicit on purpose."

### Demo Narrative

Speaker first: Marcio

Key line to land:

"The audience should see the customer impact first, then the evidence, then the governance decision."

Marcio:

"We start in a healthy state. The claims portal is responding normally. Customer interactions are flowing through the browser, the backend, the assistant service, and the dependency path behind it."

"Now we trigger the scenario. Cache volume pressure in the dependency path introduces latency and errors."

"From the customer side, the experience degrades immediately. Responses take longer. Some requests fail. If RUM details are available, DEA shows friction in the journey; either way, APM and Infrastructure show the service and filesystem evidence. If this were production, this is the moment where trust starts to fall."

"Now we move into Splunk Observability Cloud. We start from the browser experience, then move into the business transaction, the service behavior, and the service map. We can see the latency and error pattern. We can correlate the affected path and identify where the system is under stress."

Leila:

"And this is the important pivot. We are not stopping at detection. We are using the evidence to support a remediation decision."

"The remediation orchestrator receives the incident context. In the demo, that starts with the detector webhook and the AI Assistant summary. If that summary does not contain everything we need, the orchestrator enriches the incident with targeted Splunk API lookups."

"Then the remediation agent, which we are instrumenting as a Python agent so we can observe it clearly, evaluates a bounded set of actions. It is not allowed to do anything it wants. It has a small, visible toolset and a policy model."

"It proposes an action. In our primary path, that action is to clean the claims knowledge cache volume associated with the degraded path."

"Now we ask the governance question: should this be recommend only, approval required, or auto-execute? In a customer-facing production scenario like this, the default answer is approval required."

Marcio:

"And that is the moment we want the audience to focus on. The value is not just that the system found a likely action. The value is that the team can review the action with evidence, confidence, and a validation plan they can verify in Splunk."

Leila:

"Once approved, the action executes. Then we validate. We confirm whether latency drops, whether error rates recover, and whether the customer experience returns to normal."

"If the action works, we preserve the audit trail. If it does not, the system should show that clearly as well. That validation step is essential. Automation without validation is just faster risk."

Validation and recovery wrap-up:

Marcio:

"And now you see the full story: customer impact, telemetry evidence, a bounded remediation decision, and verified recovery. That is the operating model customers are asking for."

Transition sentence to audience interaction:

Leila:

"So let us pause there and make this interactive, because this is exactly where customer teams make different choices."

## Audience Interaction Script

### Interaction 1: First instinct

Speaker first: Marcio

Exact audience question:

"If you were the incident owner in this moment, what would you want the system to do first: clean the cache, restart the service, or scale the service?"

Marcio:

"We like asking this because it shows how quickly different teams form different instincts under pressure."

Leila:

"And that is why evidence matters. The best next action is not the most familiar action. It is the action that best matches the observed failure mode."

### Interaction 2: Trust boundary

Speaker first: Leila

Exact audience question:

"How many of you would allow that action to auto-execute in production, and how many would require approval first?"

Leila:

"This is the real trust conversation. Not whether AI can produce an answer, but whether the organization is comfortable with the control model behind that answer."

Marcio:

"Different customers will draw that line differently. That is fine. The point is that you should be able to define that line intentionally."

### Interaction 3: Required evidence

Speaker first: Leila

Exact audience question:

"Before letting an agent take action in production, what evidence would you need to see?"

Leila:

"Usually the answers are some combination of confidence, customer impact, service evidence, filesystem metrics, and validation plan."

"That is exactly the point. Customers do not want black-box action. They want explainable action, and they want it connected all the way back to the customer session that triggered the investigation."

"That is also why we like the hybrid model. The AI Assistant gives us the narrative explanation, and the API enrichment gives us the structured data we need for policy and decision-making."

Transition sentence to close:

Marcio:

"And once you frame it that way, the path forward becomes much more practical."

## Closing and Call to Action

### Closing Script

Speaker first: Marcio

Key line to land:

"The goal is not autonomous everything. The goal is trusted action at the right boundary."

Marcio:

"If there is one thing we want you to take away, it is this: once AI enters the customer journey, your operating model has to change with it."

"It is no longer enough to know that something is wrong. You need a way to move from insight to action without losing control."

"For many customers, the first step is not full autonomy. The first step is creating enough evidence, enough policy, and enough validation to trust a bounded action."

Leila:

"And that is where observability becomes more important, not less important. You need observability for the digital experience, for the application, for the dependencies, for the AI workflow, and for the remediation agent itself."

"Because if the agent cannot explain what it saw, why it recommended an action, and what happened after it acted, then it does not belong in the production path."

### Three Customer Takeaways

Marcio:

"Here are the three takeaways we would leave with."

"First, AI is now part of the customer experience, so AI failures are customer trust failures."

"Second, modern observability has to start with the digital experience and connect that experience to the backend and the remediation path."

"Third, the right target is not unlimited automation. It is bounded automation with evidence, policy, and validation."

### Call to Action

Leila:

"As you think about your own environment, pick one customer-facing incident class that happens repeatedly. Then ask a simple question: can your current operating model only describe that problem, or can it help you resolve it with trust?"

"That gap is where the next wave of customer value will be created."

## Presenter Split and Handoff Notes

### Marcio Ownership

- opening hook
- customer and business impact framing
- incident pressure and operational narrative
- demo narration from the customer point of view
- three takeaways introduction

### Leila Ownership

- trust and governance framing
- explanation of the two-agent model
- explicit architecture credibility statement
- policy gate and approval language
- validation and safe autonomy close

### Shared Moments

- demo handoff
- audience questions
- remediation approval moment
- final call to action

### Handoff Guidance

Use these handoffs consistently:

- Marcio to Leila: use when moving from business impact to trust and governance
- Leila to Marcio: use when moving from architecture or policy back to customer impact

Do not interrupt each other mid-thought. Each handoff should sound like a deliberate expansion of the same story.

### Rehearsal Notes

- keep the opening under 3 minutes
- do not over-explain product internals before the demo
- pause after each audience question
- keep the architecture credibility statement intact
- if Session Replay is available in the environment, use one short replay clip only
- keep the phrase "bounded automation with evidence, policy, and validation" consistent across both presenters
