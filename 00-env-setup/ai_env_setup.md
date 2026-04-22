# AI Development Environment Setup Guide (Windows)

This guide provides a clean, reliable setup for using: - Virtual
Environment (venv) - Jupyter Notebook - Sentence Transformers - ChromaDB

------------------------------------------------------------------------

## Step 1: Create Project Folder

``` bash
mkdir ai_project
cd ai_project
```

------------------------------------------------------------------------

## Step 2: Create Virtual Environment

``` bash
python -m venv ai
```

------------------------------------------------------------------------

## Step 3: Activate Virtual Environment

``` bash
ai\Scripts\activate
```

Expected:

    (ai) C:\ai_project>

------------------------------------------------------------------------

## Step 4: Install Required Packages

``` bash
pip install --upgrade pip
pip install jupyter ipykernel sentence-transformers chromadb pandas numpy scikit-learn
pip install matplotlib seaborn
```

------------------------------------------------------------------------

## Step 5: Register venv as Jupyter Kernel (CRITICAL)

``` bash
python -m ipykernel install --user --name=ai --display-name "Python (ai)"
```

------------------------------------------------------------------------

## Step 6: Launch Jupyter Notebook

``` bash
jupyter notebook
```

⚠️ Always launch AFTER activating venv.

------------------------------------------------------------------------

## Step 7: Select Correct Kernel

In Jupyter: - Click Kernel (top right) - Select: Python (ai)

------------------------------------------------------------------------

## Step 8: Verify Environment

``` python
import sys
print(sys.executable)
```

Expected:

    ...\ai\Scripts\python.exe

------------------------------------------------------------------------

## Step 9: Test Installation

``` python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
print("Embedding model loaded")
```

------------------------------------------------------------------------

## Debug Tip

Always install using:

``` python
import sys
!{sys.executable} -m pip install package_name
```

------------------------------------------------------------------------

## Golden Rules

-   Always activate venv before installing
-   Always select correct kernel
-   Never mix Anaconda + venv
