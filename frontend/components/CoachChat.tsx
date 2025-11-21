import React from "react";
import {
	Sparkles,
	AlertTriangle,
	CheckCircle2,
	ExternalLink,
} from "lucide-react";

interface MatchResult {
	match_score: number;
	reasoning: string;
	missing_skills: string[];
	advice: string;
}

interface Job {
	id: string;
	headline: string;
	employer: { name: string };
	workplace_address: { municipality: string };
	webpage_url?: string;
}

interface CoachChatProps {
	result: MatchResult;
	isLoading: boolean;
	job?: Job;
}

export default function CoachChat({ result, isLoading, job }: CoachChatProps) {
	if (isLoading) {
		return (
			<div className='bg-white/70 backdrop-blur-sm rounded-2xl shadow-lg p-8 border border-gray-200/50 animate-pulse'>
				<div className='h-8 bg-gray-200 rounded-lg w-1/3 mb-6'></div>
				<div className='h-5 bg-gray-200 rounded-lg w-full mb-3'></div>
				<div className='h-5 bg-gray-200 rounded-lg w-2/3'></div>
			</div>
		);
	}

	if (!result) return null;

	const getScoreGradient = (score: number) => {
		if (score >= 80) return "from-green-500 to-emerald-600";
		if (score >= 50) return "from-yellow-500 to-orange-500";
		return "from-red-500 to-rose-600";
	};

	const getScoreLabel = (score: number) => {
		if (score >= 80) return "Utmärkt matchning!";
		if (score >= 50) return "Bra matchning";
		return "Viss matchning";
	};

	return (
		<div className='bg-white/70 backdrop-blur-sm rounded-2xl shadow-lg border border-gray-200/50 overflow-hidden'>
			<div className='bg-linear-to-r from-green-500 to-cyan-500 p-5 text-white flex items-center gap-3'>
				<div className='bg-white/20 p-2 rounded-lg backdrop-blur-sm'>
					<Sparkles className='w-6 h-6' />
				</div>
				<div>
					<h2 className='font-bold text-xl'>AI Karriärcoach</h2>
					<p className='text-green-100 text-sm'>Personlig analys & råd</p>
				</div>
			</div>

			<div className='p-6 space-y-6'>
				{/* Score Bar */}
				<div className='space-y-3'>
					<div className='flex items-center justify-between'>
						<span className='text-sm font-semibold text-gray-700'>
							Matchningspoäng
						</span>
						<span className='text-3xl font-bold text-gray-900'>
							{result.match_score}%
						</span>
					</div>
					<div className='relative h-8 bg-gray-200 rounded-full overflow-hidden shadow-inner'>
						<div
							className={`h-full bg-linear-to-r ${getScoreGradient(
								result.match_score
							)} rounded-full transition-all duration-1000 ease-out shadow-lg`}
							style={{ width: `${Math.max(result.match_score, 15)}%` }}
						></div>
						{result.match_score >= 20 ? (
							<div className='absolute inset-0 flex items-center justify-end pr-3'>
								<span className='text-xs font-bold text-white drop-shadow-md'>
									{getScoreLabel(result.match_score)}
								</span>
							</div>
						) : (
							<div className='absolute inset-0 flex items-center pl-3'>
								<span className='text-xs font-bold text-gray-700'>
									{getScoreLabel(result.match_score)}
								</span>
							</div>
						)}
					</div>
				</div>

				{/* Reasoning */}
				<div className='bg-white rounded-xl p-5 border border-gray-200 shadow-sm'>
					<h3 className='font-bold text-gray-900 mb-3 flex items-center gap-2'>
						<div className='w-1.5 h-5 bg-cyan-500 rounded-full'></div>
						Varför denna matchning?
					</h3>
					<p className='text-gray-700 text-sm leading-relaxed'>
						{result.reasoning}
					</p>
				</div>

				{/* Missing Skills */}
				{result.missing_skills && result.missing_skills.length > 0 && (
					<div className='bg-orange-50 rounded-xl p-5 border border-orange-200 shadow-sm'>
						<h3 className='font-bold text-orange-800 mb-3 flex items-center gap-2'>
							<div className='bg-orange-500 p-1 rounded-lg'>
								<AlertTriangle size={14} className='text-white' />
							</div>
							Saknade färdigheter
						</h3>
						<ul className='list-none text-sm text-orange-700 space-y-2'>
							{result.missing_skills.map((skill, idx) => (
								<li key={idx} className='flex items-start gap-2'>
									<span className='text-orange-500 font-bold'>•</span>
									<span>{skill}</span>
								</li>
							))}
						</ul>
					</div>
				)}

				{/* Advice */}
				<div className='bg-linear-to-br from-cyan-50 to-green-50 rounded-xl p-5 border border-cyan-200 shadow-sm'>
					<h3 className='font-bold text-cyan-800 mb-3 flex items-center gap-2'>
						<div className='bg-cyan-500 p-1 rounded-lg'>
							<CheckCircle2 size={14} className='text-white' />
						</div>
						Tips för att lyckas
					</h3>
					<p className='text-sm text-cyan-900 leading-relaxed'>
						{result.advice}
					</p>
				</div>

				{/* Apply Button - Direct link to Arbetsförmedlingen */}
				{job?.webpage_url && (
					<a
						href={job.webpage_url}
						target='_blank'
						rel='noopener noreferrer'
						className='w-full bg-linear-to-r from-green-500 to-cyan-500 text-white py-4 rounded-xl font-bold text-center hover:from-green-600 hover:to-cyan-600 transition-all shadow-lg hover:shadow-xl cursor-pointer flex items-center justify-center gap-2'
					>
						Visa annonsen på Arbetsförmedlingen
						<ExternalLink size={20} />
					</a>
				)}
			</div>
		</div>
	);
}
