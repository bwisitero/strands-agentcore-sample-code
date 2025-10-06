"""
Demo 3: MCP Server Integration (7 min)
Goal: Show how to use thousands of pre-built tools

Key Teaching Points:
- How to connect to MCP servers
- Using AWS documentation MCP server as example
- Accessing external tool ecosystems
"""

from strands import Agent
from strands.tools.mcp import MCPClient
from mcp import stdio_client, StdioServerParameters

# Connect to AWS documentation MCP server
aws_docs_client = MCPClient(
    lambda: stdio_client(
        StdioServerParameters(
            command="uvx",
            args=["awslabs.aws-documentation-mcp-server@latest"]
        )
    )
)

with aws_docs_client:
    agent = Agent(tools=aws_docs_client.list_tools_sync())
    response = agent("How do I set up DynamoDB with Python?")
    print(response)


"""
Sample output:
emil@Franklins-MacBook-Pro strands-agentcore-demo % uv run demo_3_mcp_integration.py      
[10/04/25 15:01:41] INFO     Processing request of type ListToolsRequest                                                                                       server.py:664
I'll help you find information about setting up DynamoDB with Python. Let me search the AWS documentation for relevant guides.
Tool #1: search_documentation
[10/04/25 15:01:45] INFO     Processing request of type CallToolRequest                                                                                        server.py:664
[10/04/25 15:01:47] INFO     HTTP Request: POST https://proxy.search.docs.aws.amazon.com/search?session=da9d5538-a93d-439e-aa08-90146b61f260 "HTTP/1.1 200   _client.py:1740
                             OK"                                                                                                                                            
Perfect! I found some excellent resources. Let me get the detailed information from the main DynamoDB Python programming guide and the code examples.
Tool #2: read_documentation
[10/04/25 15:01:50] INFO     Processing request of type CallToolRequest                                                                                        server.py:664
[10/04/25 15:01:51] INFO     HTTP Request: GET                                                                                                               _client.py:1740
                             https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/programming-with-python.html?session=da9d5538-a93d-439e-aa08-9                
                             0146b61f260&query_id=e7121137-4bf0-4542-bbd1-113ed639d495 "HTTP/1.1 200 OK"                                                                    
Let me also get some practical code examples from the Python code examples documentation:
Tool #3: read_documentation
[10/04/25 15:01:53] INFO     Processing request of type CallToolRequest                                                                                        server.py:664
[10/04/25 15:01:54] INFO     HTTP Request: GET                                                                                                               _client.py:1740
                             https://docs.aws.amazon.com/code-library/latest/ug/python_3_dynamodb_code_examples.html?session=da9d5538-a93d-439e-aa08-90146b6                
                             1f260&query_id=e7121137-4bf0-4542-bbd1-113ed639d495 "HTTP/1.1 200 OK"                                                                          
Now let me get some additional setup information to provide a complete guide:
Tool #4: search_documentation
[10/04/25 15:01:57] INFO     Processing request of type CallToolRequest                                                                                        server.py:664
[10/04/25 15:01:58] INFO     HTTP Request: POST https://proxy.search.docs.aws.amazon.com/search?session=da9d5538-a93d-439e-aa08-90146b61f260 "HTTP/1.1 200   _client.py:1740
                             OK"                                                                                                                                            
Based on the AWS documentation I've retrieved, here's a comprehensive guide on how to set up DynamoDB with Python:

## Setting up DynamoDB with Python

### 1. Installation and Prerequisites

**Install Boto3 (AWS SDK for Python):**
```bash
pip install boto3
```

**Configure AWS Credentials:**
You need to set up your AWS credentials. You can do this in several ways:

- **AWS CLI configuration:**
  ```bash
  aws configure
  ```
  This will prompt you to enter:
  - AWS Access Key ID
  - AWS Secret Access Key
  - Default region name (e.g., `us-east-1`)
  - Default output format (e.g., `json`)

- **Environment variables:**
  ```bash
  export AWS_ACCESS_KEY_ID="your-access-key"
  export AWS_SECRET_ACCESS_KEY="your-secret-key"
  export AWS_DEFAULT_REGION="us-east-1"
  ```

- **IAM roles** (if running on AWS services like EC2, Lambda)

### 2. Basic Setup and Connection

**Simple connection to DynamoDB:**
```python
import boto3

# Create a DynamoDB client (low-level interface)
dynamodb = boto3.client('dynamodb')

# Or create a DynamoDB resource (high-level interface)
dynamodb = boto3.resource('dynamodb')

# List existing tables
paginator = dynamodb.get_paginator("list_tables")
page_iterator = paginator.paginate(Limit=10)

print("DynamoDB tables in your account:")
for page in page_iterator:
    for table_name in page.get("TableNames", []):
        print(f"- {table_name}")
```

### 3. Two Main Interfaces

#### **Client Interface (Low-level)**
- Provides 1-to-1 mapping to DynamoDB API
- Uses DynamoDB JSON format (requires type specification)
- More verbose but offers complete functionality

```python
import boto3

dynamodb = boto3.client('dynamodb')

# Put item using client interface
dynamodb.put_item(
    TableName='YourTableName',
    Item={
        'pk': {'S': 'id#1'},
        'sk': {'S': 'cart#123'},
        'name': {'S': 'SomeName'},
        'inventory': {'N': '500'},
    }
)
```

#### **Resource Interface (High-level)**
- More Pythonic and convenient
- Automatic data type handling
- Simplified syntax

```python
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('YourTableName')

# Put item using resource interface
table.put_item(
    Item={
        'pk': 'id#1',
        'sk': 'cart#123',
        'name': 'SomeName',
        'inventory': 500,
    }
)
```

### 4. Creating a Table

```python
import boto3
from botocore.exceptions import ClientError

def create_table(table_name):
    dynamodb = boto3.resource('dynamodb')
    
    try:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'pk',
                    'KeyType': 'HASH'  # Partition key
                },
                {
                    'AttributeName': 'sk',
                    'KeyType': 'RANGE'  # Sort key (optional)
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'pk',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'sk',
                    'AttributeType': 'S'
                }
            ],
            BillingMode='PAY_PER_REQUEST'  # On-demand billing
        )
        
        # Wait for table to be created
        table.wait_until_exists()
        print(f"Table {table_name} created successfully!")
        return table
        
    except ClientError as e:
        print(f"Error creating table: {e}")
        return None
```

### 5. Basic Operations

**Put Item:**
```python
table = dynamodb.Table('YourTableName')

table.put_item(
    Item={
        'pk': 'user#123',
        'sk': 'profile',
        'name': 'John Doe',
        'email': 'john@example.com',
        'age': 30
    }
)
```

**Get Item:**
```python
response = table.get_item(
    Key={
        'pk': 'user#123',
        'sk': 'profile'
    }
)

if 'Item' in response:
    item = response['Item']
    print(item)
```

**Query Items:**
```python
from boto3.dynamodb.conditions import Key

response = table.query(
    KeyConditionExpression=Key('pk').eq('user#123')
)

items = response['Items']
for item in items:
    print(item)
```

**Scan Table:**
```python
response = table.scan()
items = response['Items']
for item in items:
    print(item)
```

### 6. Error Handling

```python
from botocore.exceptions import ClientError

try:
    response = table.get_item(
        Key={'pk': 'user#123', 'sk': 'profile'}
    )
except ClientError as e:
    print(f"Error: {e.response['Error']['Code']}")
    print(f"Message: {e.response['Error']['Message']}")
```

### 7. Best Practices

1. **Use the Resource interface** for most operations (simpler syntax)
2. **Handle exceptions** properly using `ClientError`
3. **Use batch operations** for multiple items
4. **Configure retry policies** for production applications
5. **Use pagination** for large result sets

### 8. Complete Example Class

```python
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

class DynamoDBHelper:
    def __init__(self, table_name, region='us-east-1'):
        self.dynamodb = boto3.resource('dynamodb', region_name=region)
        self.table = self.dynamodb.Table(table_name)
    
    def put_item(self, item):
        try:
            self.table.put_item(Item=item)
            return True
        except ClientError as e:
            print(f"Error putting item: {e}")
            return False
    
    def get_item(self, key):
        try:
            response = self.table.get_item(Key=key)
            return response.get('Item')
        except ClientError as e:
            print(f"Error getting item: {e}")
            return None
    
    def query_items(self, partition_key, partition_value):
        try:
            response = self.table.query(
                KeyConditionExpression=Key(partition_key).eq(partition_value)
            )
            return response['Items']
        except ClientError as e:
            print(f"Error querying items: {e}")
            return []

# Usage
db = DynamoDBHelper('MyTable')
db.put_item({'pk': 'user#1', 'name': 'Alice'})
item = db.get_item({'pk': 'user#1'})
```

This setup gives you everything you need to start working with DynamoDB in Python using Boto3. The resource interface is generally recommended for most use cases due to its simplicity and Pythonic design.Based on the AWS documentation I've retrieved, here's a comprehensive guide on how to set up DynamoDB with Python:

## Setting up DynamoDB with Python

### 1. Installation and Prerequisites

**Install Boto3 (AWS SDK for Python):**
```bash
pip install boto3
```

**Configure AWS Credentials:**
You need to set up your AWS credentials. You can do this in several ways:

- **AWS CLI configuration:**
  ```bash
  aws configure
  ```
  This will prompt you to enter:
  - AWS Access Key ID
  - AWS Secret Access Key
  - Default region name (e.g., `us-east-1`)
  - Default output format (e.g., `json`)

- **Environment variables:**
  ```bash
  export AWS_ACCESS_KEY_ID="your-access-key"
  export AWS_SECRET_ACCESS_KEY="your-secret-key"
  export AWS_DEFAULT_REGION="us-east-1"
  ```

- **IAM roles** (if running on AWS services like EC2, Lambda)

### 2. Basic Setup and Connection

**Simple connection to DynamoDB:**
```python
import boto3

# Create a DynamoDB client (low-level interface)
dynamodb = boto3.client('dynamodb')

# Or create a DynamoDB resource (high-level interface)
dynamodb = boto3.resource('dynamodb')

# List existing tables
paginator = dynamodb.get_paginator("list_tables")
page_iterator = paginator.paginate(Limit=10)

print("DynamoDB tables in your account:")
for page in page_iterator:
    for table_name in page.get("TableNames", []):
        print(f"- {table_name}")
```

### 3. Two Main Interfaces

#### **Client Interface (Low-level)**
- Provides 1-to-1 mapping to DynamoDB API
- Uses DynamoDB JSON format (requires type specification)
- More verbose but offers complete functionality

```python
import boto3

dynamodb = boto3.client('dynamodb')

# Put item using client interface
dynamodb.put_item(
    TableName='YourTableName',
    Item={
        'pk': {'S': 'id#1'},
        'sk': {'S': 'cart#123'},
        'name': {'S': 'SomeName'},
        'inventory': {'N': '500'},
    }
)
```

#### **Resource Interface (High-level)**
- More Pythonic and convenient
- Automatic data type handling
- Simplified syntax

```python
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('YourTableName')

# Put item using resource interface
table.put_item(
    Item={
        'pk': 'id#1',
        'sk': 'cart#123',
        'name': 'SomeName',
        'inventory': 500,
    }
)
```

### 4. Creating a Table

```python
import boto3
from botocore.exceptions import ClientError

def create_table(table_name):
    dynamodb = boto3.resource('dynamodb')
    
    try:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'pk',
                    'KeyType': 'HASH'  # Partition key
                },
                {
                    'AttributeName': 'sk',
                    'KeyType': 'RANGE'  # Sort key (optional)
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'pk',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'sk',
                    'AttributeType': 'S'
                }
            ],
            BillingMode='PAY_PER_REQUEST'  # On-demand billing
        )
        
        # Wait for table to be created
        table.wait_until_exists()
        print(f"Table {table_name} created successfully!")
        return table
        
    except ClientError as e:
        print(f"Error creating table: {e}")
        return None
```

### 5. Basic Operations

**Put Item:**
```python
table = dynamodb.Table('YourTableName')

table.put_item(
    Item={
        'pk': 'user#123',
        'sk': 'profile',
        'name': 'John Doe',
        'email': 'john@example.com',
        'age': 30
    }
)
```

**Get Item:**
```python
response = table.get_item(
    Key={
        'pk': 'user#123',
        'sk': 'profile'
    }
)

if 'Item' in response:
    item = response['Item']
    print(item)
```

**Query Items:**
```python
from boto3.dynamodb.conditions import Key

response = table.query(
    KeyConditionExpression=Key('pk').eq('user#123')
)

items = response['Items']
for item in items:
    print(item)
```

**Scan Table:**
```python
response = table.scan()
items = response['Items']
for item in items:
    print(item)
```

### 6. Error Handling

```python
from botocore.exceptions import ClientError

try:
    response = table.get_item(
        Key={'pk': 'user#123', 'sk': 'profile'}
    )
except ClientError as e:
    print(f"Error: {e.response['Error']['Code']}")
    print(f"Message: {e.response['Error']['Message']}")
```

### 7. Best Practices

1. **Use the Resource interface** for most operations (simpler syntax)
2. **Handle exceptions** properly using `ClientError`
3. **Use batch operations** for multiple items
4. **Configure retry policies** for production applications
5. **Use pagination** for large result sets

### 8. Complete Example Class

```python
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

class DynamoDBHelper:
    def __init__(self, table_name, region='us-east-1'):
        self.dynamodb = boto3.resource('dynamodb', region_name=region)
        self.table = self.dynamodb.Table(table_name)
    
    def put_item(self, item):
        try:
            self.table.put_item(Item=item)
            return True
        except ClientError as e:
            print(f"Error putting item: {e}")
            return False
    
    def get_item(self, key):
        try:
            response = self.table.get_item(Key=key)
            return response.get('Item')
        except ClientError as e:
            print(f"Error getting item: {e}")
            return None
    
    def query_items(self, partition_key, partition_value):
        try:
            response = self.table.query(
                KeyConditionExpression=Key(partition_key).eq(partition_value)
            )
            return response['Items']
        except ClientError as e:
            print(f"Error querying items: {e}")
            return []

# Usage
db = DynamoDBHelper('MyTable')
db.put_item({'pk': 'user#1', 'name': 'Alice'})
item = db.get_item({'pk': 'user#1'})
```

This setup gives you everything you need to start working with DynamoDB in Python using Boto3. The resource interface is generally recommended for most use cases due to its simplicity and Pythonic design.

"""