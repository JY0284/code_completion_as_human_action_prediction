# Represent Code as Action Sequence for Predicting Next Method Call

This repository implements the approach described in the paper **[Represent Code as Action Sequence for Predicting Next Method Call](https://dl.acm.org/doi/abs/10.1145/3545258.3545263)**. The core concept is to model method calls in Python code as "actions" similar to human actions, **leveraging both the coding context and method invocation sequences to predict future method calls**. This approach enhances the accuracy and **context-awareness** of code completion tools.

## Overview

Code completion is an essential feature in modern IDEs, directly boosting developer productivity. This project focuses on utilizing large-scale Python code repositories to predict the next method call a developer might write. Inspired by natural language processing (NLP) models, we treat code as sequences of actions, combining coding context (project, file, function) with method invocations and their parameters.

The method proposed and implemented in this repository shows a **32.36% improvement** over baseline models such as GPT-2(powerful when writing the paper) , particularly in next-method-call token prediction.

## Key Features

- **Contextual Action Modeling**: 
  - Code is modeled as a sequence of actions, including the context (project, file, and function structure), allowing the model to understand the developer's intent better.
  
- **Transformer-Based Predictions**: 
  - A GPT-like architecture is used to predict the next method call based on the past sequence of actions.
  
- **Action Extraction Tools**: 
  - Provides utilities for parsing Python code into Abstract Syntax Trees (ASTs) and extracting method calls, assignments, and other relevant actions.

- **Data Processing and Analysis**: 
  - Tools to collect, preprocess, and analyze large Python codebases, making this approach scalable for large-scale experiments.

## Repository Structure

```
├── README.md                              # Project description and usage instructions
├── Represent_Code_as_Action_Sequence_for_Predicting_Next_Method_Call_draft.pdf  # Paper draft
├── slides_internetware_2022_Represent Code as Action Sequence for Predicting Next Method Call.pdf # Conference slides
├── sample/py_demo.py                      # Example for quick demonstration of the idea
└── src/analysis/                          # Core analysis and model scripts
```

The repository also includes a paper draft and the slides used in the Internetware 2022 conference for a deeper understanding of the work.

## How It Works

1. **Action Extraction**:  
   - The `call_extractor.py` script parses Python code into ASTs. It then extracts method calls and related actions, such as assignments, and models them as action sequences. Each action contains attributes like context, actor, and parameters.
   
2. **Modeling**:  
   - The extracted action sequences are flattened and processed into a format suitable for transformer-based models. We use a fine-tuned GPT-2 to predict the next method call based on past actions.

## Training the Model

To train (or fine-tune) the model for method call prediction:
1. First, collect and prepare Python project files.
2. Then, run the scripts under the `src/analysis/` folder to extract the action sequences and prepare the training data.
3. Finally, feed the processed data into the transformer-based model (such as GPT) for training.

For more details, refer to the original paper or the provided slides.