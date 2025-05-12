# LL(1), SLR(1) Parser - Application

## 🔗 Live Demo

Check out the Hugging Face apps here:

- 👉 [LL(1) Parser Live on Hugging Face](https://huggingface.co/spaces/Neha13/cc1)  
- 👉 [SLR(1) Parser Live on Hugging Face](https://huggingface.co/spaces/Neha13/CC)

---

## 📌 Overview

This is a user-friendly **LL(1) and SLR(1) Parser Visualizer** built using **Python** and **Streamlit**. The applications allow users to input context-free grammars, generate parsing tables, and simulate parsing of input strings with detailed visual feedback — perfect for students and educators in compiler design and automata theory.


---

## 🔍 Features

- ✅ **Grammar Input**: Define grammar rules easily.
- 🔁 **Grammar Augmentation** (LL(1)): Automatically adds a new start symbol.
- 📚 **FIRST and FOLLOW Sets** (LL(1))
- 🔢 **Parsing Table Construction** for LL(1) and SLR(1)
- 🧪 **Input String Parsing Simulation** with detailed transitions
- 📊 **Step-by-Step Parsing Trace**
- 🌐 **Deployed on Hugging Face Spaces** using Streamlit

---

## 🛠️ Technologies Used

- Python
- Streamlit
- Pandas
- Custom parsing algorithms

---

## 🚀 Installation (Local)

Follow the steps below to set up the application locally:

1. Clone the repository:
   ```bash
   git clone https://github.com/neha13rana/Parser-LL1-SLR1-Application.git
   cd Parser-LL1-SLR1-Application
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the applications:
   - **LL(1) Parser**:
     ```bash
     streamlit run LL1.py
     ```

   - **SLR(1) Parser**:
     ```bash
     streamlit run SLR1.py
     ```

---
