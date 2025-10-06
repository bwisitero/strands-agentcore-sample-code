"""
Demo 1: Hello Agent (5 min)
Goal: Get everyone's first agent running

Key Teaching Points:
- Default uses Bedrock Claude 4 Sonnet
- Model-driven approach - no complex workflow needed
"""

from strands import Agent

# Simplest possible agent
agent = Agent()
response = agent("What are the key considerations for building a chatbot?")
print(response)


"""
Sample output:

strands-agentcore-demo) emil@Franklins-MacBook-Pro strands-agentcore-demo % python3 demo_1_hello_agent.py
Here are the key considerations for building a chatbot:

## 1. **Define Purpose and Scope**
- Clearly identify what problems the chatbot will solve
- Determine target audience and use cases
- Define success metrics and KPIs
- Set realistic expectations for capabilities

## 2. **Choose the Right Type**
- **Rule-based**: Simple, predictable interactions
- **AI-powered**: More natural, contextual conversations
- **Hybrid**: Combines both approaches
- Consider complexity vs. development resources

## 3. **Platform and Integration**
- Select deployment channels (website, messaging apps, voice assistants)
- Ensure compatibility with existing systems (CRM, databases, APIs)
- Plan for multi-platform consistency

## 4. **User Experience Design**
- Create intuitive conversation flows
- Design clear prompts and error handling
- Plan fallback options for unrecognized inputs
- Consider accessibility requirements

## 5. **Natural Language Processing**
- Choose appropriate NLP tools and frameworks
- Plan for multiple languages if needed
- Handle variations in user input (typos, slang, context)
- Design intent recognition and entity extraction

## 6. **Data and Training**
- Gather relevant training data
- Plan for ongoing data collection and improvement
- Ensure data privacy and security compliance
- Consider bias in training data

## 7. **Technical Architecture**
- Scalability and performance requirements
- Security measures and data protection
- Monitoring and analytics capabilities
- Maintenance and update processes

## 8. **Testing and Iteration**
- Comprehensive testing across scenarios
- User acceptance testing
- Continuous improvement based on user feedback
- Regular performance monitoring

Would you like me to elaborate on any of these areas?Here are the key considerations for building a chatbot:

## 1. **Define Purpose and Scope**
- Clearly identify what problems the chatbot will solve
- Determine target audience and use cases
- Define success metrics and KPIs
- Set realistic expectations for capabilities

## 2. **Choose the Right Type**
- **Rule-based**: Simple, predictable interactions
- **AI-powered**: More natural, contextual conversations
- **Hybrid**: Combines both approaches
- Consider complexity vs. development resources

## 3. **Platform and Integration**
- Select deployment channels (website, messaging apps, voice assistants)
- Ensure compatibility with existing systems (CRM, databases, APIs)
- Plan for multi-platform consistency

## 4. **User Experience Design**
- Create intuitive conversation flows
- Design clear prompts and error handling
- Plan fallback options for unrecognized inputs
- Consider accessibility requirements

## 5. **Natural Language Processing**
- Choose appropriate NLP tools and frameworks
- Plan for multiple languages if needed
- Handle variations in user input (typos, slang, context)
- Design intent recognition and entity extraction

## 6. **Data and Training**
- Gather relevant training data
- Plan for ongoing data collection and improvement
- Ensure data privacy and security compliance
- Consider bias in training data

## 7. **Technical Architecture**
- Scalability and performance requirements
- Security measures and data protection
- Monitoring and analytics capabilities
- Maintenance and update processes

## 8. **Testing and Iteration**
- Comprehensive testing across scenarios
- User acceptance testing
- Continuous improvement based on user feedback
- Regular performance monitoring

Would you like me to elaborate on any of these areas?

"""