"use client";

import React, { useState } from "react";
import CVUpload from "@/components/CVUpload";
import JobCard from "@/components/JobCard";
import CoachChat from "@/components/CoachChat";
import { searchJobs, matchJob, getRateLimitStatus } from "@/lib/api";
import { Search, Briefcase, Sparkles, CheckCircle } from "lucide-react";

export default function Home() {
	const [cvAnalysis, setCvAnalysis] = useState<any>(null);
	const [query, setQuery] = useState("");
	const [jobs, setJobs] = useState<any[]>([]);
	const [page, setPage] = useState<number>(1);
	const [perPage] = useState<number>(10);
	const [pagination, setPagination] = useState<any | null>(null);
	const [isSearching, setIsSearching] = useState(false);
	const [selectedJobId, setSelectedJobId] = useState<string | null>(null);
	const [matchResult, setMatchResult] = useState<any>(null);
	const [isMatching, setIsMatching] = useState(false);
	const [remainingMatches, setRemainingMatches] = useState<number | null>(null);

	const runSearch = async (q: string, p: number) => {
		setIsSearching(true);
		try {
			const results = await searchJobs(q, { page: p, perPage });
			setJobs(results.hits || []);
			setPagination(results.pagination || null);
		} catch (err) {
			console.error(err);
		} finally {
			setIsSearching(false);
		}
	};

	const handleSearch = async (e: React.FormEvent) => {
		e.preventDefault();
		if (!query.trim()) return;
		setPage(1);
		await runSearch(query, 1);
	};

	const handleMatch = async (jobId: string) => {
		if (!cvAnalysis) {
			alert("Vänligen ladda upp ditt CV först!");
			return;
		}

		setSelectedJobId(jobId);
		setIsMatching(true);
		setMatchResult(null);

		try {
			const result = await matchJob(cvAnalysis, jobId);
			setMatchResult(result);
			if (result.remaining_matches !== undefined) {
				setRemainingMatches(result.remaining_matches);
			}
		} catch (err: any) {
			console.error(err);
			const errorMessage =
				err?.response?.data?.detail || "Kunde inte matcha jobbet. Försök igen.";
			alert(errorMessage);
			setSelectedJobId(null);
		} finally {
			setIsMatching(false);
		}
	};

	return (
		<main className='min-h-screen bg-white'>
			{/* Header */}
			<header className='bg-white backdrop-blur-lg border-b border-gray-200 sticky top-0 z-10 shadow-sm'>
				<div className='max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between'>
					<div className='flex items-center gap-3'>
						<div className='bg-linear-to-br from-green-500 to-cyan-500 p-2.5 rounded-xl shadow-lg shadow-cyan-500/20'>
							<Briefcase className='text-white w-5 h-5' />
						</div>
						<div>
							<h1 className='text-xl font-bold text-gray-900'>
								AI Karriärcoach
							</h1>
							<p className='text-xs text-gray-600'>
								Din personliga jobbmatchare
							</p>
						</div>
					</div>
					<div className='flex items-center gap-3'>
						{cvAnalysis && (
							<div className='flex items-center gap-2 text-sm text-green-600 font-medium bg-green-50 px-4 py-2 rounded-full border border-green-200 shadow-sm'>
								<CheckCircle className='w-4 h-4' />
								<span>CV Analyserat</span>
							</div>
						)}
						{remainingMatches !== null && (
							<div className='text-sm text-gray-600 font-medium bg-gray-100 px-4 py-2 rounded-full border border-gray-200 shadow-sm'>
								<span>{remainingMatches} matchningar kvar</span>
							</div>
						)}
					</div>
				</div>
			</header>

			<div className='max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8'>
				<div className='grid grid-cols-1 lg:grid-cols-12 gap-8 lg:h-[calc(100vh-8rem)]'>
					{/* Left Column: CV & Search */}
					<div
						className='lg:col-span-7 space-y-6 lg:overflow-y-auto lg:pr-4'
						style={{ scrollbarGutter: "stable" }}
					>
						{/* CV Section */}
						{!cvAnalysis && (
							<section className='bg-white/70 backdrop-blur-sm p-8 rounded-2xl shadow-lg border border-gray-200/50'>
								<div className='flex items-center gap-2 mb-6'>
									<div className='bg-blue-100 text-blue-600 rounded-lg w-8 h-8 flex items-center justify-center font-bold text-sm'>
										1
									</div>
									<h2 className='text-xl font-bold text-gray-900'>
										Börja med att ladda upp ditt CV
									</h2>
								</div>
								<CVUpload onAnalysisComplete={setCvAnalysis} />
							</section>
						)}

						{/* Search Section */}
						<section className='bg-white/70 backdrop-blur-sm p-8 rounded-2xl shadow-lg border border-gray-200/50'>
							<div className='flex items-center gap-2 mb-6'>
								{cvAnalysis && (
									<div className='bg-blue-100 text-blue-600 rounded-lg w-8 h-8 flex items-center justify-center font-bold text-sm'>
										2
									</div>
								)}
								<h2 className='text-xl font-bold text-gray-900'>
									{cvAnalysis ? "Sök efter jobb" : "Sök efter jobb"}
								</h2>
							</div>
							{!cvAnalysis && (
								<div className='mb-4 p-3 bg-amber-50 border border-amber-200 rounded-lg text-sm text-amber-800'>
									💡 Ladda upp ditt CV först för att få AI-matchning och
									personliga tips
								</div>
							)}
							<form onSubmit={handleSearch} className='flex gap-3 mb-6'>
								<div className='relative flex-1'>
									<Search className='absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 w-5 h-5' />
									<input
										type='text'
										placeholder='T.ex. Javautvecklare Stockholm'
										className='w-full pl-12 pr-4 py-3.5 rounded-xl border border-gray-300 focus:ring-2 focus:ring-cyan-500 focus:border-transparent outline-none transition-all bg-white shadow-sm text-gray-900 placeholder:text-gray-400'
										value={query}
										onChange={(e) => setQuery(e.target.value)}
									/>
								</div>
								<button
									type='submit'
									disabled={isSearching}
									className='bg-linear-to-r from-green-500 to-cyan-500 text-white px-8 py-3.5 rounded-full font-semibold hover:from-green-600 hover:to-cyan-600 transition-all disabled:opacity-50 shadow-lg shadow-cyan-500/30 hover:shadow-xl hover:shadow-cyan-500/40 cursor-pointer'
								>
									{isSearching ? "Söker..." : "Sök"}
								</button>
							</form>

							<div className='space-y-4'>
								{jobs.map((job) => (
									<JobCard
										key={job.id}
										job={job}
										onMatch={handleMatch}
										isSelected={selectedJobId === job.id}
									/>
								))}
								{jobs.length === 0 && !isSearching && query && (
									<p className='text-center text-gray-500 py-8'>
										Inga jobb hittades.
									</p>
								)}
								{pagination && (
									<div className='flex items-center justify-between pt-4 border-t border-gray-200'>
										<div className='text-sm text-gray-600'>
											Sida {pagination.page} av {pagination.total_pages}
										</div>
										<div className='flex gap-2'>
											<button
												type='button'
												disabled={!pagination.has_prev || isSearching}
												onClick={async () => {
													const nextPage = Math.max(
														1,
														(pagination.page || page) - 1
													);
													setPage(nextPage);
													await runSearch(query, nextPage);
												}}
												className='px-4 py-2 rounded-full border border-gray-300 text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50'
											>
												Föregående
											</button>
											<button
												type='button'
												disabled={!pagination.has_next || isSearching}
												onClick={async () => {
													const nextPage = (pagination.page || page) + 1;
													setPage(nextPage);
													await runSearch(query, nextPage);
												}}
												className='px-4 py-2 rounded-full bg-linear-to-r from-green-500 to-cyan-500 text-white font-semibold hover:from-green-600 hover:to-cyan-600 disabled:opacity-50'
											>
												Nästa
											</button>
										</div>
									</div>
								)}
							</div>
						</section>
					</div>

					{/* Right Column: Coach / Match Results */}
					<div
						className='lg:col-span-5 lg:overflow-y-auto lg:pl-4'
						style={{ scrollbarGutter: "stable" }}
					>
						{selectedJobId ? (
							<CoachChat
								result={matchResult}
								isLoading={isMatching}
								job={jobs.find((j) => j.id === selectedJobId)}
							/>
						) : (
							<div className='bg-linear-to-br from-white to-cyan-50/30 rounded-2xl shadow-lg border border-gray-200/50 p-10 text-center lg:sticky lg:top-0'>
								<div className='bg-linear-to-br from-green-100 to-cyan-100 w-20 h-20 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-lg'>
									<Sparkles className='text-cyan-600 w-10 h-10' />
								</div>
								<h3 className='text-2xl font-bold text-gray-900 mb-3'>
									Din AI Karriärcoach
								</h3>
								<p className='text-gray-600 leading-relaxed'>
									Välj ett jobb i listan för att se hur väl din profil matchar
									och få personliga tips på hur du kan öka dina chanser.
								</p>
							</div>
						)}
					</div>
				</div>
			</div>
		</main>
	);
}
