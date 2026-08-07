import os
import sys
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#065F46"))
        
        # Header (on pages after cover)
        if self._pageNumber > 1:
            self.drawString(54, 750, "CropPro.Ai | Complete Rookie-to-Expert Blueprint & Judge Defense Handbook")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.75)
            self.line(54, 742, 558, 742)
            
        # Footer
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(54, 36, "Precision Agriculture Decision Engine & Agro-Climatic Intelligence Platform")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 36, page_str)
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 48, 558, 48)
        
        self.restoreState()

def build_pdf():
    pdf_filename = "CropPro_AI_Complete_Rookie_To_Expert_Guide.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette
    PRIMARY = colors.HexColor("#065F46")     # Deep Forest Green
    SECONDARY = colors.HexColor("#047857")   # Emerald Green
    ACCENT = colors.HexColor("#D97706")      # Amber Accent
    DARK_TEXT = colors.HexColor("#0F172A")   # Slate 900
    MUTED_TEXT = colors.HexColor("#334155")  # Slate 700
    BG_LIGHT = colors.HexColor("#F0FDF4")    # Light Sage
    BG_WARN = colors.HexColor("#FFFBEB")     # Light Amber

    # Custom Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=PRIMARY,
        alignment=TA_LEFT,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=SECONDARY,
        alignment=TA_LEFT,
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'H1Header',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=PRIMARY,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2Header',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=SECONDARY,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=DARK_TEXT,
        alignment=TA_LEFT,
        spaceAfter=6
    )

    body_bold = ParagraphStyle(
        'BodyDarkBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    question_style = ParagraphStyle(
        'JudgeQuestion',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#92400E"),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    answer_style = ParagraphStyle(
        'JudgeAnswer',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.2,
        leading=13.5,
        textColor=DARK_TEXT,
        spaceAfter=8
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#1E293B"),
        backColor=colors.HexColor("#F1F5F9"),
        borderColor=colors.HexColor("#CBD5E1"),
        borderWidth=0.5,
        borderPadding=6,
        spaceAfter=8
    )

    story = []

    # Title Banner
    story.append(Paragraph("🌱 CropPro.Ai: Complete Rookie-to-Expert Guide", title_style))
    story.append(Paragraph("A Comprehensive Blueprint for Building Machine Learning Applications & Judge Defense Handbook", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=PRIMARY, spaceBefore=0, spaceAfter=15))

    # SECTION 1: FUNDAMENTALS
    story.append(Paragraph("📚 Section 1: Core Machine Learning Concepts for Beginners", h1_style))
    story.append(Paragraph(
        "Before building a machine learning project, every developer must understand these fundamental concepts:",
        body_style
    ))

    concepts_data = [
        [Paragraph("Concept", body_bold), Paragraph("Definition & Real-World Analogy", body_bold), Paragraph("CropPro.Ai Application", body_bold)],
        [
            Paragraph("<b>Features ($X$)</b>", body_style),
            Paragraph("Input signals or variables fed into the model to make predictions.", body_style),
            Paragraph("10 inputs: $N, P, K$, Temp, Humidity, pH, Rainfall, Soil EC, Elevation, Market Index.", body_style)
        ],
        [
            Paragraph("<b>Target Label ($y$)</b>", body_style),
            Paragraph("The ground-truth outcome or answer the model aims to predict.", body_style),
            Paragraph("34 Crop Classes (e.g., <i>Ginger, Sugarcane, Cotton, Soybean, Rice</i>).", body_style)
        ],
        [
            Paragraph("<b>Supervised Classification</b>", body_style),
            Paragraph("Predicting a discrete category (crop type) based on labeled training data.", body_style),
            Paragraph("Multi-class classification predicting 1 of 34 distinct crop categories.", body_style)
        ],
        [
            Paragraph("<b>Gradient Boosting (XGBoost)</b>", body_style),
            Paragraph("An ensemble of decision trees where each tree iteratively fixes errors of prior trees.", body_style),
            Paragraph("Outperformed Random Forest with 99.26% accuracy on complex soil interactions.", body_style)
        ],
        [
            Paragraph("<b>SHAP Explainability</b>", body_style),
            Paragraph("Game-theoretic method quantifying exact feature contributions.", body_style),
            Paragraph("Explains WHY Ginger won (e.g. Potassium 100 kg/ha favored rhizome growth).", body_style)
        ]
    ]

    t_concepts = Table(concepts_data, colWidths=[110, 210, 184])
    t_concepts.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BG_LIGHT),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_concepts)
    story.append(Spacer(1, 14))

    # SECTION 2: END-TO-END ML LIFECYCLE
    story.append(Paragraph("🔄 Section 2: Standard 8-Step Machine Learning Project Lifecycle", h1_style))
    story.append(Paragraph(
        "Building an industry-grade ML application follows an 8-stage engineering workflow:",
        body_style
    ))

    flow_data = [
        [
            Paragraph("<b>1. Problem Definition</b>", body_bold),
            Paragraph("Identify the agricultural challenge: Farmers need data-driven crop selection considering soil nutrients, climate stress, and commercial ROI.", body_style)
        ],
        [
            Paragraph("<b>2. Data Collection</b>", body_bold),
            Paragraph("Gather ground-truth agronomic benchmarks from <b>Soil Health Card Scheme (Govt. of India / MAHAGRI), ICAR, and IMD</b> across 33 districts of Maharashtra.", body_style)
        ],
        [
            Paragraph("<b>3. Data Preprocessing</b>", body_bold),
            Paragraph("Synthesize 272,000 baseline samples using Gaussian distributions (`data_pipeline.py`). Perform `LabelEncoder` transformations on crop labels.", body_style)
        ],
        [
            Paragraph("<b>4. Model Selection</b>", body_bold),
            Paragraph("Evaluate multiple classifiers. Select **XGBoost Classifier** for its superior handling of non-linear feature dependencies and multi-class optimization.", body_style)
        ],
        [
            Paragraph("<b>5. Model Training</b>", body_bold),
            Paragraph("Train XGBoost model on 80% train split (217,600 rows) with multi-class log-loss objective and softmax probability output (`ml_engine.py`).", body_style)
        ],
        [
            Paragraph("<b>6. Model Evaluation</b>", body_bold),
            Paragraph("Validate on 20% holdout test set (54,400 rows). Achieved **99.26% test accuracy** with clean confusion matrix metrics.", body_style)
        ],
        [
            Paragraph("<b>7. Explainable AI</b>", body_bold),
            Paragraph("Integrate `shap.TreeExplainer` to calculate marginal feature attributions and compute Confidence Advantage vs. runner-up candidate.", body_style)
        ],
        [
            Paragraph("<b>8. Deployment & REST API</b>", body_bold),
            Paragraph("Expose trained model (`xgb_model.pkl`) via **FastAPI REST API** (`main.py`) and connect to a responsive **Streamlit Daylight UI** (`app.py`).", body_style)
        ]
    ]

    t_flow = Table(flow_data, colWidths=[130, 374])
    t_flow.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor("#F8FAFC")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_flow)
    story.append(Spacer(1, 14))

    # SECTION 3: SYSTEM TECHNICAL SPECS
    story.append(Paragraph("🧪 Section 3: CropPro.Ai Technical Specifications", h1_style))
    
    spec_data = [
        [Paragraph("Feature Parameter", body_bold), Paragraph("Unit", body_bold), Paragraph("Agronomic Role & Physiological Impact", body_bold)],
        [Paragraph("Nitrogen ($N$)", body_style), Paragraph("kg/ha", body_style), Paragraph("Drives vegetative biomass synthesis & leaf canopy formation.", body_style)],
        [Paragraph("Phosphorus ($P$)", body_style), Paragraph("kg/ha", body_style), Paragraph("Stimulates early root development, tillering & flowering.", body_style)],
        [Paragraph("Potassium ($K$)", body_style), Paragraph("kg/ha", body_style), Paragraph("Drives rhizome, fruit, tuber starch accumulation & drought tolerance.", body_style)],
        [Paragraph("Temperature", body_style), Paragraph("°C", body_style), Paragraph("Determines enzyme activation and thermal growth window.", body_style)],
        [Paragraph("Humidity", body_style), Paragraph("%", body_style), Paragraph("Governs transpiration rates and micro-climate disease pressure.", body_style)],
        [Paragraph("Soil pH", body_style), Paragraph("pH scale", body_style), Paragraph("Controls nutrient solubility and root absorption efficiency.", body_style)],
        [Paragraph("Annual Rainfall", body_style), Paragraph("mm", body_style), Paragraph("Satisfies physiological water consumption requirements.", body_style)],
        [Paragraph("Soil EC", body_style), Paragraph("dS/m", body_style), Paragraph("Measures electrical conductivity & root salinity osmotic stress.", body_style)],
        [Paragraph("Elevation", body_style), Paragraph("meters", body_style), Paragraph("Reflects topographical altitude suitability & chilling hours.", body_style)],
        [Paragraph("Market Index", body_style), Paragraph("1-10 Scale", body_style), Paragraph("Incorporates economic commercial demand & price resilience.", body_style)]
    ]

    t_specs = Table(spec_data, colWidths=[120, 60, 324])
    t_specs.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BG_LIGHT),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_specs)
    story.append(Spacer(1, 14))

    story.append(PageBreak())

    # SECTION 4: JUDGE DEFENSE HANDBOOK
    story.append(Paragraph("🛡️ Section 4: Hackathon & Competition Judge Q&A Defense Handbook", h1_style))
    story.append(Paragraph(
        "Use these bulletproof, technically rigorous answers during panel Q&A sessions:",
        body_style
    ))

    qna_list = [
        (
            "Q1: Why did you choose XGBoost over Random Forest or Deep Learning (Neural Networks)?",
            "<b>Answer:</b> Agricultural tabular datasets are characterized by structured, non-linear feature interactions (e.g. High Nitrogen is beneficial only if sufficient Rainfall and Potassium are present). Random Forests treat decision trees independently, whereas XGBoost sequentially minimizes residual errors using gradient boosting. Deep Learning requires vast homogeneous datasets and acts as a black box. XGBoost achieved <b>99.26% test accuracy</b> with fast inference times (<15ms) and native compatibility with SHAP TreeExplainer for full decision transparency."
        ),
        (
            "Q2: How do you justify using a 272,000 row synthetic dataset? Is it realistic?",
            "<b>Answer:</b> Raw agricultural surveys are often sparse and incomplete across micro-regions. To solve data scarcity while preserving factual accuracy, we anchored our dataset generator (`data_pipeline.py`) around verified agronomic centroids sourced from the <b>Soil Health Card Scheme (Govt. of Maharashtra / MAHAGRI), ICAR, and IMD</b> across all 33 districts. We applied Gaussian distribution sampling around these real-world means to simulate realistic soil variance while preventing overfitting."
        ),
        (
            "Q3: How does your AI explain WHY a crop was recommended over others?",
            "<b>Answer:</b> We integrated <b>SHAP (SHapley Additive exPlanations)</b> based on cooperative game theory. SHAP measures the exact marginal contribution of each soil/climate input parameter. Furthermore, our engine calculates the <b>Confidence Advantage</b>: $\\text{Advantage Delta} = \\text{Confidence}_{\\text{Winner}} - \\text{Confidence}_{\\text{Runner-Up}}$, producing a plain-English agronomic rationale explaining why the top choice outranked competitor crops."
        ),
        (
            "Q4: How does your system account for real-world environmental stress like Drought or High Salinity?",
            "<b>Answer:</b> We embedded interactive climate stress toggles (Drought Mitigation Mode, High Salinity Warning Mode, and Market ROI Mode). When activated, the backend REST API (`/predict`) dynamically applies mathematical penalty multipliers to high-water consuming crops (e.g., Sugarcane) or salinity-sensitive crops, favoring resilient alternatives (e.g., Bajra or Jowar) to ensure real-world field viability."
        ),
        (
            "Q5: Why did you decouple the system into FastAPI (Backend) and Streamlit (Frontend)?",
            "<b>Answer:</b> Decoupling enforces industry-standard <b>Separation of Concerns</b>. The FastAPI backend serves as a stateless microservice handling model inference, location databases, and SHAP calculations. This allows any external client — such as a Flutter mobile app, IoT field sensors, or web dashboards — to consume recommendations via standard REST endpoints (`/predict`, `/universal-locations`) without duplicating model logic."
        ),
        (
            "Q6: How does this project directly assist smallholder farmers in organic agriculture?",
            "<b>Answer:</b> Beyond predicting crops, CropPro.Ai features a <b>4-Quadrant Zero-Synthetic Organic Profitability Advisory</b>. It provides targeted recommendations for Bio-Fertilizer Substitution (e.g., FYM + Neem Cake + Trichoderma), Biological Pest Control (e.g., Neem oil / Dashparni Arka), and Natural Intercropping (e.g., Legumes for Nitrogen fixation). This reduces synthetic fertilizer costs by 30-40%, directly boosting net farm profit margins."
        )
    ]

    for q_text, a_text in qna_list:
        card_content = [
            Paragraph(q_text, question_style),
            Spacer(1, 2),
            Paragraph(a_text, answer_style)
        ]
        t_card = Table([[card_content]], colWidths=[504])
        t_card.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), BG_WARN),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#FCD34D")),
            ('LINELEFT', (0,0), (-1,-1), 4, ACCENT),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 12),
            ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ]))
        story.append(t_card)
        story.append(Spacer(1, 8))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated: {pdf_filename}")

if __name__ == '__main__':
    build_pdf()
