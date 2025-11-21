import React from "react";
import { MapPin, Building, ArrowRight } from "lucide-react";

interface Job {
	id: string;
	headline: string;
	employer: { name: string };
	workplace_address: { municipality: string };
	description: { text_snippet: string };
}

interface JobCardProps {
	job: Job;
	onMatch: (jobId: string) => void;
	isSelected: boolean;
}

export default function JobCard({ job, onMatch, isSelected }: JobCardProps) {
	return (
		<div
			className={`bg-white rounded-xl shadow-md border transition-all hover:shadow-xl hover:-translate-y-0.5 ${
				isSelected
					? "ring-2 ring-cyan-500 border-cyan-500 shadow-cyan-200"
					: "border-gray-200 hover:border-cyan-300"
			}`}
		>
			<div className='p-5'>
				<h3 className='font-bold text-lg text-gray-900 mb-2 line-clamp-2'>
					{job.headline}
				</h3>
				<div className='flex items-center gap-4 text-sm text-gray-600 mb-3'>
					<div className='flex items-center gap-1.5'>
						<Building size={15} className='text-gray-400' />
						<span>{job.employer?.name || "Okänd arbetsgivare"}</span>
					</div>
					<div className='flex items-center gap-1.5'>
						<MapPin size={15} className='text-gray-400' />
						<span>{job.workplace_address?.municipality || "Plats saknas"}</span>
					</div>
				</div>
				<p className='text-sm text-gray-600 mb-4 line-clamp-2 leading-relaxed'>
					{job.description?.text_snippet}
				</p>
				<button
					onClick={() => onMatch(job.id)}
					className='w-full flex items-center justify-center gap-2 bg-linear-to-r from-green-500 to-cyan-500 text-white py-2.5 rounded-full hover:from-green-600 hover:to-cyan-600 transition-all font-semibold text-sm shadow-md hover:shadow-lg cursor-pointer'
				>
					Matcha mot mitt CV <ArrowRight size={16} />
				</button>
			</div>
		</div>
	);
}
