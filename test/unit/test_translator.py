from src.translator import translate_content

non_english = [
    # --- Non-English posts ---
    {"post": "Dies ist eine Nachricht auf Deutsch", "expected_answer": (False, "This is a German message")},
    {"post": "Hier ist dein erstes Beispiel.", "expected_answer": (False, "This is your first example.")},
    {"post": "Bonjour, comment allez-vous aujourd’hui ?", "expected_answer": (False, "Hello, how are you today?")},
    {"post": "¿Cuál es la capital de Francia?", "expected_answer": (False, "What is the capital of France?")},
    {"post": "これはニューラルネットワークの構造に関する質問です。", "expected_answer": (False, "This is a question about the structure of neural networks.")},
    {"post": "이 실험의 목적은 무엇입니까?", "expected_answer": (False, "What is the purpose of this experiment?")},
    {"post": "请解释量子纠缠的概念。", "expected_answer": (False, "Please explain the concept of quantum entanglement.")},
    {"post": "ما هو تعريف الذكاء الاصطناعي؟", "expected_answer": (False, "What is the definition of artificial intelligence?")},
    {"post": "Какова цель этого исследования?", "expected_answer": (False, "What is the goal of this study?")},
    {"post": "कृपया इस समीकरण का अर्थ समझाइए।", "expected_answer": (False, "Please explain the meaning of this equation.")},
    {"post": "Qual é a diferença entre aprendizado supervisionado e não supervisionado?", "expected_answer": (False, "What is the difference between supervised and unsupervised learning?")},
    {"post": "Come si calcola la derivata di una funzione?", "expected_answer": (False, "How do you calculate the derivative of a function?")},
    {"post": "Bir hipotezi nasıl test edersiniz?", "expected_answer": (False, "How do you test a hypothesis?")},
    {"post": "Wat zijn de voordelen van hernieuwbare energie?", "expected_answer": (False, "What are the advantages of renewable energy?")},
    {"post": "Vilka faktorer påverkar den ekonomiska tillväxten?", "expected_answer": (False, "Which factors affect economic growth?")},
    {"post": "Mitkä ovat tietorakenteiden päätyypit?", "expected_answer": (False, "What are the main types of data structures?")},
    {"post": "Mi a mesterséges intelligencia célja az orvostudományban?", "expected_answer": (False, "What is the purpose of artificial intelligence in medicine?")},
    {"post": "এইটা একটি প্রশ্ন।", "expected_answer": (False, "This is a question.")},
]

english = [
    # --- English posts ---
    {"post": "What is the difference between supervised and unsupervised learning?", "expected_answer": (True, "What is the difference between supervised and unsupervised learning?")},
    {"post": "How does Bayes’ theorem affect the interpretation of probability in statistical inference?", "expected_answer": (True, "How does Bayes’ theorem affect the interpretation of probability in statistical inference?")},
    {"post": "Here are Maxwell’s equations: $$\\nabla \\cdot \\mathbf{E} = \\frac{\\rho}{\\epsilon_0}, \\quad \\nabla \\times \\mathbf{B} = \\mu_0 \\mathbf{J} + \\mu_0 \\epsilon_0 \\frac{\\partial \\mathbf{E}}{\\partial t}$$ How can these equations be derived from the fundamental laws of electromagnetism?", "expected_answer": (True, "Here are Maxwell’s equations: $$\\nabla \\cdot \\mathbf{E} = \\frac{\\rho}{\\epsilon_0}, \\quad \\nabla \\times \\mathbf{B} = \\mu_0 \\mathbf{J} + \\mu_0 \\epsilon_0 \\frac{\\partial \\mathbf{E}}{\\partial t}$$ How can these equations be derived from the fundamental laws of electromagnetism?")},
    {"post": "What is the role of the activation function in a neural network?", "expected_answer": (True, "What is the role of the activation function in a neural network?")},
    {"post": "Which methods are used in this analysis?", "expected_answer": (True, "Which methods are used in this analysis?")},
    {"post": "What are the key elements of research design?", "expected_answer": (True, "What are the key elements of research design?")},
    {"post": "This algorithm is important in data science.", "expected_answer": (True, "This algorithm is important in data science.")},
    {"post": "What are the main assumptions of the theory of relativity?", "expected_answer": (True, "What are the main assumptions of the theory of relativity?")},
    {"post": "What is the purpose of artificial intelligence in medicine?", "expected_answer": (True, "What is the purpose of artificial intelligence in medicine?")},
    {"post": "Which factors affect economic growth?", "expected_answer": (True, "Which factors affect economic growth?")},
    {"post": "How is this model trained?", "expected_answer": (True, "How is this model trained?")},
    {"post": "Is this Newton’s equation?", "expected_answer": (True, "Is this Newton’s equation?")},
    {"post": "What is the main objective of this research?", "expected_answer": (True, "What is the main objective of this research?")},
]

unintelligible = [
    # --- Unintelligible / malformed posts ---
    {"post": "???!!!!", "expected_answer": (False, "???!!!!")},
    {"post": "1234 @#$%", "expected_answer": (False, "1234 @#$%")},
    {"post": "Bonjour hello こんにちは", "expected_answer": (False, "Bonjour hello こんにちは")},
    {"post": "ThisIsOneRunTogetherWithoutSpacesAndMistake", "expected_answer": (True, "ThisIsOneRunTogetherWithoutSpacesAndMistake")},  # here treat as English
    {"post": "¿¿¿ ??? ???", "expected_answer": (False, "¿¿¿ ??? ???")}
]

def test_chinese():
    is_english, translated_content = translate_content("这是一条中文消息")
    assert is_english == False
    assert translated_content == "This is a Chinese message"

def test_llm_normal_response():
    for post in non_english:
        is_english, translated_content = translate_content(post["post"])
        assert is_english == post["expected_answer"][0]
        assert translated_content == post["expected_answer"][1]

    for post in english:
        is_english, translated_content = translate_content(post["post"])
        assert is_english == post["expected_answer"][0]
        assert translated_content == post["expected_answer"][1]

def test_llm_gibberish_response():
    for post in unintelligible:
        is_english, translated_content = translate_content(post["post"])
        assert is_english == post["expected_answer"][0]
        assert translated_content == post["expected_answer"][1]