# AI Career Coach

An intelligent career coaching web application that analyzes your CV, searches for matching jobs from Arbetsförmedlingen, and provides AI-powered recommendations to help you land your dream job.

## Features

- **CV Analysis**: Upload your CV (PDF) and get AI-powered analysis of your skills and experience
- **Job Search**: Search thousands of jobs from Arbetsförmedlingen's database
- **Smart Matching**: AI agent analyzes job requirements and matches them against your profile
- **Personalized Coaching**: Get tailored advice on how to improve your match score
- **Missing Skills Detection**: Identify gaps in your skillset for each job
- **Rate Limiting**: Built-in protection to manage API costs (10 matches per session)
- **Modern UI**: Clean, responsive design with green-cyan gradient theme

## Architecture

### Backend (FastAPI + Python)

- **Three AI Agents** powered by Google Gemini:
  - `cv_analyst`: Analyzes CV and extracts skills, experience, and qualifications
  - `job_analyst`: Analyzes job postings to identify requirements
  - `career_coach`: Matches candidates to jobs and provides coaching advice
- **Security Features**: Input validation, rate limiting, PDF validation (max 10MB, 50 pages)
- **API Integration**: Arbetsförmedlingen Job Search API

### Frontend (Next.js + React + Tailwind CSS)

- **Modern UI**: Pill-shaped buttons, gradient themes, smooth animations
- **Dual-column Layout**: Independent scrolling for CV/Jobs and Coach analysis
- **Real-time Updates**: Loading states and progress indicators
- **Rate Limit Display**: Shows remaining job matches in header

## Getting Started

### Prerequisites

- Python 3.13+ (backend)
- Node.js 18+ (frontend)
- Google Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))

### Installation

1. **Clone the repository**

```bash
git clone <your-repo-url>
cd ai-career-coach
```

2. **Set up the backend**

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

3. **Set up the frontend**

```bash
cd ../frontend
npm install
```

### Running the Application

1. **Start the backend** (from `backend/` directory):

```bash
source ../.venv/bin/activate  # If not already activated
uvicorn app.main:app --reload --port 8000
```

Backend will be available at `http://localhost:8000`

2. **Start the frontend** (from `frontend/` directory):

```bash
npm run dev
```

Frontend will be available at `http://localhost:3000`

## Usage

1. **Upload your CV**: Click "Ladda upp CV" and select your PDF resume
2. **Search for jobs**: Enter keywords (e.g., "Python Developer", "UX Designer") and click search
3. **Get AI coaching**: Click "Analysera match" on any job card to get personalized feedback
4. **Apply**: Click "Visa annonsen på Arbetsförmedlingen" to view the full job posting and apply

## Security & Rate Limiting

- **Session-based rate limiting**: 10 job matches per 24-hour session (tracked by IP + User-Agent)
- **PDF validation**: Maximum 10MB file size, 50 pages
- **Input sanitization**: Query validation and job ID validation
- **Quota protection**: Handles Google API quota errors gracefully

## Tech Stack

### Backend

- FastAPI 0.115.6
- LangChain 0.3.13
- Google Gemini AI (`gemini-2.5-flash-lite`)
- PyPDF2 for PDF extraction
- Python 3.13

### Frontend

- Next.js 16.0.3
- React 19.2.0
- Tailwind CSS 4
- TypeScript 5
- Lucide Icons

## Project Structure

```
ai-career-coach/
├── backend/
│   ├── app/
│   │   ├── agents/           # AI agents (cv_analyst, job_analyst, career_coach)
│   │   ├── api/              # API routes
│   │   ├── core/             # Configuration
│   │   ├── middleware/       # Rate limiter
│   │   ├── services/         # AF API, PDF service
│   │   └── utils/            # Validators
│   ├── .env.example          # Environment template
│   └── requirements.txt      # Python dependencies
├── frontend/
│   ├── app/                  # Next.js app router
│   ├── components/           # React components
│   └── lib/                  # API client
└── README.md
```

## Environment Variables

### Backend (`backend/.env`)

```
GOOGLE_API_KEY=your_api_key_here
AF_API_BASE_URL=https://jobsearch.api.jobtechdev.se
```

**Important**: Never commit `.env` files to version control!

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.

## Acknowledgments

- [Arbetsförmedlingen](https://arbetsformedlingen.se) for the Job Search API
- [Google Gemini](https://ai.google.dev/) for AI capabilities
- Built for Swedish job seekers

## Known Issues & Future Improvements

- [ ] Add user authentication
- [ ] Save match history to database
- [ ] Export coaching advice as PDF
- [ ] Multi-language support
- [ ] Advanced filtering options
- [ ] Email notifications for new matching jobs

## Support

For issues or questions, please open an issue on GitHub.

---

**Made with AI**
