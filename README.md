# Student Homework Checker

This project is a **Streamlit-based web application** designed to assist teachers or evaluators in providing feedback on student homework. It integrates with **GPT-4o-mini** to analyze uploaded homework files, provide feedback, and assign a score based on the specified criteria.

---

## Features

- **Upload Homework**: Supports various file types, including `.py`, `.html`, `.css`, `.js`, `.txt`, and `.ipynb`.
- **Teacher Type Selection**: Choose between two teacher types:
  - **Polite**: Provides kind and constructive feedback.
  - **Strict**: Offers critical and honest feedback, scoring rigorously.
- **Dynamic API Integration**: Enter your **OpenAI API key** directly in the app to enable functionality.
- **Customizable Task Description**: Add a custom task description to match the specific homework requirements.
- **AI-Powered Feedback**: Uses **GPT-4o-mini** to:
  - Analyze the uploaded file content.
  - Provide structured feedback.
  - Score the homework out of 100.
- **Wide Layout and Custom Styling**:
  - Gradient or image background for a professional look.
  - Responsive and user-friendly interface.

---

## Technologies Used

- **Streamlit**: Web application framework for building interactive apps.
- **OpenAI API**: GPT-4o-mini model for intelligent analysis and feedback generation.
- **CSS**: Custom styling for headers, backgrounds, and widgets.
- **Python**: Core programming language for implementing functionality.

---

## Installation and Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/student-homework-checker.git
   cd student-homework-checker
   ```

2. **Install Required Libraries**:
   Ensure you have Python 3.8+ installed, then run:
   ```bash
   pip install streamlit openai
   ```

3. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

4. **Enter Your API Key**:
   - When the app starts, enter your **OpenAI API key** in the provided input box to enable the AI functionality.

---

## How to Use

1. Launch the application using `streamlit run app.py`.
2. Enter your **OpenAI API key**.
3. Upload a homework file in the supported formats.
4. Select the **teacher type** (Polite or Strict).
5. Enter a task description (optional) to guide the evaluation.
6. View the **feedback and score** provided by the AI-powered evaluator.

---

## File Structure

```plaintext
student-homework-checker/
│
├── app.py                 # Main application script
├── assets/                # Folder for background images (if used)
├── requirements.txt       # List of required libraries
└── README.md              # Project documentation
```

---

## Customization

### Background
To customize the background:
1. Replace the image URL in the `body` section of the CSS in `app.py`.
2. Or use a gradient by modifying the `background` property.

### Task Instructions
Modify the task instructions in the `analyze_homework` function to fit your use case.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Screenshots

1. **Home Page**:
   - Clean interface with options to upload files and select teacher type.
2. **Feedback Display**:
   - AI-generated feedback with a score and clear formatting.

---

## Contributions

Contributions are welcome! Please open an issue or submit a pull request on GitHub.
