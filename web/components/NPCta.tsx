"use client";

import Image from "next/image";

export default function NPCta() {
  return (
    <div className="bg-np-navy text-white rounded-xl p-8 text-center space-y-4">
      {/* Logo */}
      <div className="flex items-center justify-center mb-2">
        <Image src="/logo.png" alt="National Positions" width={120} height={36} className="object-contain brightness-0 invert" />
      </div>

      <h2 className="text-2xl font-bold">
        Want help turning this audit into revenue?
      </h2>
      <p className="text-blue-200 max-w-xl mx-auto text-sm leading-relaxed">
        Our Marketing Automation team can rebuild your flows, improve
        deliverability, launch SMS, optimize forms, refine segmentation, and
        manage Klaviyo on an ongoing basis — so you can focus on growing your
        brand.
      </p>
      <div className="flex flex-col sm:flex-row gap-3 justify-center pt-2">
        <a
          href="https://www.nationalpositions.com/contact"
          target="_blank"
          rel="noopener noreferrer"
          className="bg-np-red hover:bg-red-700 transition-colors text-white font-semibold px-8 py-3 rounded-lg"
        >
          Schedule a Free Consultation →
        </a>
        <a
          href="https://www.nationalpositions.com"
          target="_blank"
          rel="noopener noreferrer"
          className="border border-blue-400 text-blue-200 hover:text-white hover:border-white transition-colors font-semibold px-8 py-3 rounded-lg"
        >
          Learn More
        </a>
      </div>
      <p className="text-xs text-blue-300 pt-2">
        Audit results are diagnostic estimates only and are not guarantees of
        performance. National Positions is a full-service digital marketing
        agency.
      </p>
    </div>
  );
}
