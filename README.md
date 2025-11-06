# 🧩 Git_Quick_Task

## 🎯 Objective
This exercise assesses your understanding of **Git fundamentals and branch management**, your ability to **use AI tools effectively**, and your skills in **writing technical reports with LaTeX**.  
The final submission is a **public GitHub repository link** (no Pull Request required).
### Please do not spend more than 2 hours on this task! 
If you are familiar with the above tools, it should take **around 1 hour** to complete — then you can focus on other, more meaningful tasks.

---

## 📘 Repository Structure
This repository contains two base branches:

- **main** — Task description and final deliverables.  
- **report** — A LaTeX report template (in the `report/` folder).

---

## 🧱 Your Tasks

1. **Create a branch named `code`**  
   Create a new branch `code` for development.  
   You must **develop a simple game using AI tools only**.  
   *(Examples: 2048, Snake, Tank Battle—keep it simple.)*

2. **Make at least 5 meaningful commits**  
   Each commit should have a clear purpose (e.g., add feature, fix bug, update docs, refactor).  
   Do not mix unrelated changes in a single commit.  
   If you’re unsure how to plan commits or write messages, you may use AI assistance or refer to this post (ZJU internal access required):  
   https://www.cc98.org/topic/6098599
   Again, you do not have to build a perfect game; it can have many bugs, as long as it runs and has at least five meaningful commits. This task isn’t a competition—save your time for more important things!

3. **Merge into `main`**  
   After development, merge `code` into `main` so **all source code and the final report** are on `main`.

4. **Write your report**  
   Switch to the `report` branch and use the LaTeX template to complete your report.  
   The report must include:
   - A brief introduction to your project;  
   - **All AI prompts** used during development;  
   - The last 3–5 lines from `git log --oneline`;  

   Compile to `report.pdf` and place it in the root of the `main` branch.

5. **Final Submission**  
   Make your GitHub repository public and submit **the repository link**.  
   Ensure the following branches remain:
   - `main` — code and report  
   - `report` — LaTeX source code
   - `code` — complete development history

---

## 💡 Tips
- Use `git log --graph --oneline --all` to visualize branch history.  
- Run `git status` before committing to check for untracked or modified files.  
- In the `report` branch, use `.gitignore` to exclude `.aux`, `.log`, `.pdf`, etc.

---

**✅ Final Deliverable: a public GitHub repository link**
