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

```bash
git clone https://github.com/neha13rana/LL1-Parser-App.git
cd LL1-Parser-App
pip install -r requirements.txt

1) For LL1

streamlit run LL1.py

2) For SLR1

streamlit run SLR1.py
