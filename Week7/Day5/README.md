Parallel Execution

Parallel execution allows multiple tasks to run simultaneously rather than sequentially. It is useful when tasks are independent of each other and helps improve speed, efficiency, and scalability. In LangGraph, multiple branches can execute in parallel, reducing the overall workflow execution time.

Subgraphs

Subgraphs are smaller workflows embedded within a larger workflow. A subgraph is a graph embedded inside another graph.
Instead of creating one huge workflow, we break it into smaller reusable workflows.

Fan-Out Pattern

Fan-Out is a workflow pattern where a single task or input is divided into multiple independent branches. Each branch performs a different task simultaneously. Fan-Out helps distribute workload and enables parallel processing. It is commonly used when a problem can be broken into smaller independent subtasks.

Fan-In Pattern

Fan-In is the opposite of Fan-Out. It collects and combines outputs from multiple branches into a single node or result. Fan-In is useful when information from different sources needs to be aggregated before proceeding. It ensures that all branch results are available for final processing.

Map-Reduce

Map-Reduce is a processing strategy used to handle large or complex tasks efficiently.

Map Phase:
The original task is divided into smaller independent tasks that can run separately. Each task processes a portion of the work.

Reduce Phase:
The results from all mapped tasks are collected and combined into a final output.