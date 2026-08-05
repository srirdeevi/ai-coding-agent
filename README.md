# Architecture

                AI Coding Agent

                      |
                      v

              Repository Layer
                      |
        +-------------+-------------+
        |                           |
        v                           v
    File Discovery             File Reading

                      |
                      v

             Code Intelligence

        +-------------+-------------+
        |                           |
        v                           v

    Code Search              AST Analyzer

                                |
                    +-----------+-----------+
                    |           |           |
                    v           v           v

                Classes     Functions    Imports


# Build the Agent Brain
Use Case

    User Question

      |

    Planner

      |

    Need:
       1. Search for authentication keywords
       2. Read matching files
       3. Analyze classes/functions
       4. Generate answer

         |

    Execute Tools

      |

    Response

## Add LLM Reasoning Layer
    Question
    |
    v
    LLM Planner
    |
    |
    +------------+
    |            |
    v            v
    Search Tool   Analyze Tool
    |
    v
    Context
    |
    v
    LLM Response
