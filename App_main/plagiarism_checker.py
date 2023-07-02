from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from App_main.models import ResearchPaperModel
import PyPDF2


def check_single_paper(input_paper_file):
    # Read the input paper from the PDF file
    input_paper_text = extract_text_from_pdf(input_paper_file)

    # Preprocess the input paper
    processed_input = preprocess_text(input_paper_text)

    # Retrieve all research papers from the database
    research_papers = ResearchPaperModel.objects.all()

    # Initialize variables for tracking the highest similarity score and the related research paper
    highest_similarity_score = 0.0
    related_research_paper = None

    # Calculate similarity scores and find the highest score
    for paper in research_papers:
        processed_paper_text = preprocess_text(extract_text_from_pdf(paper.file.path))
        similarity_score = calculate_similarity_score(processed_input, processed_paper_text)
        if similarity_score > highest_similarity_score:
            highest_similarity_score = similarity_score
            related_research_paper = paper

    # Print the highest similarity score and the related research paper
    if related_research_paper is not None:
        return highest_similarity_score

    else:
        print("No matching research paper found.")


def preprocess_text(text):
    # Implement your text preprocessing logic here
    processed_text = text.lower()
    return processed_text


def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(pdf_reader.pages)
    text = ""
    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text


def calculate_similarity_score(input_text, paper_text):
    # Calculate similarity score using cosine similarity
    vectorized = TfidfVectorizer()
    tfidf_matrix = vectorized.fit_transform([input_text, paper_text])
    similarity_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return similarity_score
