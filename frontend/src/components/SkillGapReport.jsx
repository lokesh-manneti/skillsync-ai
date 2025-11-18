import React from "react";

// Helper to get Tailwind classes for match status
const getBadgeClasses = (status) => {
  switch (status) {
    case "Matched":
      return "bg-mint-green text-green-900"; // Your brand's 'Mint Green'
    case "Partial":
      return "bg-warning-amber bg-opacity-20 text-yellow-900"; // Your brand's 'Warning Amber'
    case "Missing":
      return "bg-error-red bg-opacity-10 text-red-900"; // Your brand's 'Error Red'
    default:
      return "bg-gray-100 text-gray-500";
  }
};

function SkillGapReport({ report }) {
  if (!report) return null;

  return (
    <div>
      <h3 className="text-lg font-semibold text-dark-700">
        Your Skill Match Score:
      </h3>
      {/* Score */}
      <div className="my-2 text-6xl font-bold bg-gradient-to-r from-ocean-blue to-royal-purple text-transparent bg-clip-text">
        {report.skill_match_score.toFixed(1)}%
      </div>
      {/* Summary */}
      <p className="text-base text-gray-500 mb-8 max-w-2xl">
        {report.analysis_summary}
      </p>

      <h3 className="text-lg font-semibold text-dark-700 mb-4">
        Detailed Skill Analysis:
      </h3>
      <ul className="space-y-4">
        {report.skill_comparison.map((skill, index) => (
          <li key={index} className="border border-gray-200 rounded-lg p-4">
            <div className="flex justify-between items-center mb-2">
              <span className="text-base font-bold text-dark-900">
                {skill.skill_name}
              </span>
              <span
                className={`px-3 py-1 rounded-full text-xs font-bold ${getBadgeClasses(
                  skill.match_status
                )}`}
              >
                {skill.match_status}
              </span>
            </div>
            <p className="text-sm text-gray-500 mb-3">{skill.justification}</p>

            {/* Learning Plan Accordion */}
            {skill.learning_plan && skill.learning_plan.length > 0 && (
              <details className="group">
                <summary className="cursor-pointer text-sm font-medium text-ocean-blue hover:text-royal-purple">
                  View Learning Plan
                </summary>
                <div className="mt-4 pt-4 border-t border-gray-200">
                  <h4 className="text-sm font-semibold text-dark-700 mb-3">
                    Personalized Plan (
                    {skill.learning_plan.reduce(
                      (acc, step) => acc + step.estimated_hours,
                      0
                    )}{" "}
                    estimated hours)
                  </h4>
                  <ol className="list-decimal list-inside space-y-3 text-sm text-gray-500">
                    {skill.learning_plan.map((step, i) => (
                      <li key={i}>
                        <strong className="text-dark-700">
                          {step.step_title}
                        </strong>{" "}
                        ({step.estimated_hours} hrs): {step.details}
                      </li>
                    ))}
                  </ol>
                </div>
              </details>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default SkillGapReport;
