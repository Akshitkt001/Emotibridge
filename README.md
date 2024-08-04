# Emotibridge

## Overview

**Emotibridge** is an advanced video processing application designed to enhance video content by removing background noise, transcribing and translating audio, and generating speech from translated text. This application leverages state-of-the-art machine learning models and various Python libraries to deliver high-quality results.

### Features

- **Background Noise Removal**: Clean audio by removing unwanted background noise.
- **Transcription and Translation**: Convert audio to text and translate it into multiple languages.
- **Speech Generation**: Generate speech from translated text.
- **User Interface**: Interactive UI with progress indicators and text editing capabilities.

### Demo Video

![Emotibridge Demo](https://example.com/demo-video-link)

## Technologies Used

- **Programming Language**: Python
- **Libraries and Frameworks**: PyTorch, TTS, pydub, SpeechRecognition
- **GUI Framework**: Tkinter
- **Audio Processing**: pydub
- **Machine Learning**: PyTorch for model training and inference

## Installation

To get started with Emotibridge, follow these steps:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Akshitkt001/Emotibridge.git
   cd Emotibridge
   Set Up Virtual Environment

   python -m venv venv
   source venv/bin/activate  # On Windows  use`venv\Scripts\activate`
1. **Install Dependencies**

   ```bash
   pip install -r requirements.txt 
   python main.py #Run the Application 

Configuration
Update the configuration files as needed to set paths for models and other resources. Make sure to adjust any settings specific to your environment.

## Usage

### Open the Application

Launch the application by running the `main.py` script. The GUI will present the following screens:

- **Main Screen**: Displays the application title and a "Take me to app" button.
- **Processing Screen**: Allows users to input video files, select languages, and start processing.
- **Output Screen**: Displays the final processed video along with editable translated text.

### Input Video

Upload your video file using the file input section.

### Select Languages

Choose the input and target languages from the dropdown menus.

### Process Video

Click the "Process" button to start the background noise removal, transcription, translation, and speech generation.

### View Results

After processing, review the translated text and generated speech, and view the final video output.

## API Documentation

### Endpoints

- **/process-video**: Processes the uploaded video, performs transcription, translation, and speech generation.
  - **Method**: POST
  - **Parameters**:
    - `video_file`: The video file to be processed.
    - `input_language`: Language of the original video audio.
    - `target_language`: Language to translate the audio into.

### Examples

For detailed API usage examples, refer to the [FastAPI documentation](https://fastapi.tiangolo.com/).

## Model Links

- **TTS Model**: [Link to TTS model](#)
- **Translation Model**: [Link to translation model](#)

## Tools and Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [PyTorch Documentation](https://pytorch.org/docs/stable/index.html)
- [pydub Documentation](https://pydub.com/)
- [SpeechRecognition Documentation](https://pypi.org/project/SpeechRecognition/)
- [Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)

## Contributing

Contributions to Emotibridge are welcome! If you find a bug or want to add a new feature, please follow these steps:

1. Fork the repository.
2. Create a new branch (e.g., `git checkout -b feature/your-feature`).
3. Make your changes.
4. Commit your changes (e.g., `git commit -am 'Add new feature'`).
5. Push to the branch (e.g., `git push origin feature/your-feature`).
6. Create a new Pull Request.

## License

This project is licensed under the Apache License - see the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries or issues, please contact:

- **Akshit Kumar Tiwari** - [GitHub Profile](https://github.com/Akshitkt001)
- **Email**: [your-email@example.com]
