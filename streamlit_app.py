import streamlit as st

st.title("🎈 My Streamlit new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

if 'upload_button_clicked' not in st.session_state:
    st.session_state.upload_button_clicked = False

def click_upload_button():
    st.session_state.upload_button_clicked = True

st.button('Upload Document', on_click=click_upload_button)

if st.session_state.upload_button_clicked:
    uploaded_file = st.file_uploader("Choose a file", type=['docx']) # Specify accepted file types

    if uploaded_file is not None:
        st.success(f"File '{uploaded_file.name}' uploaded successfully!")
        # You can now process the uploaded_file, e.g., read its content
        # For example, to read as text:
        # content = uploaded_file.read().decode("utf-8")
        # st.write(content)

from docx import Document
from docx.shared import Pt
from docx.shared import Inches


def convert_transcript(input_path, output_path):

    doc = Document(input_path)
    new_doc = Document()

    style = new_doc.styles['Normal']
    font = style.font
    font.name = 'Arial'
    font.size = Pt(10)
    
    sections = new_doc.sections
    for section in sections:
        section.top_margin = Inches(0.5)
        section.bottom_margin = Inches(0.5)
        section.left_margin = Inches(0.5)
        section.right_margin = Inches(0.5)

    p = new_doc.add_paragraph()

    top_labels = [
        "Platform:",
        "Date:",
        "Event Title:",
        "Length:",
        "Type of Recording:",
        "Transcript:",
        "Saved Clip:",
        "Public Link:"
    ]
    for label in top_labels:
        run_label = p.add_run(label)
        run_label.bold = True
        run_space = p.add_run(" ")
        run_space.bold = False
        run_space.add_break()

    run_video = p.add_run("(VIDEO)")
    run_video.add_break()
    run_video.add_break()

    run_transcript = p.add_run("TRANSCRIPT:")
    run_transcript.bold = True
    run_transcript.add_break()

    p.add_run().add_break()

    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    i = 0

    while i < len(paragraphs):
        
        line = paragraphs[i]
        if "(" in line and ")" in line:
            try:
                speaker_part, rest = line.split("(", 1)
                timestamp = rest.split(")")[0].strip()
                speaker_name = speaker_part.strip().upper()

                dialogue = ""
                if i + 1 < len(paragraphs) and "(" not in paragraphs[i + 1]:
                    dialogue = paragraphs[i + 1].strip()
                    i += 1

                run_speaker = p.add_run(f"[{timestamp}] {speaker_name}: ")
                run_speaker.bold = True
                p.add_run(dialogue)
                p.add_run().add_break()
                p.add_run().add_break()

            except Exception:
                p.add_run(line)
                p.add_run().add_break()
                p.add_run().add_break()

        else:
            p.add_run(line)
            p.add_run().add_break()
            p.add_run().add_break()

        i += 1

    new_doc.save(output_path)
    print(f"✅ Converted file saved as: {output_path}")

convert_transcript("C:/Users/djycm/Downloads/REV Example Mod.docx", "C:/Users/djycm/Downloads/transcript_converted3.docx")